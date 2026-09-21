#!/usr/bin/env python3
"""CPU-only ArmnetBench P0.5 Gate A/B analysis.

The content representation resamples the complete state/action sequence to
K=32 normalized time points. The model never receives the original frame
count, duration, padding mask, or frame index unless the explicit
content+length condition is selected.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pyarrow.parquet as pq


K = 32
SEED = 20260921


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -40.0, 40.0)))


def fit_logistic(x: np.ndarray, y: np.ndarray, steps: int = 650, lr: float = 0.14) -> dict[str, Any] | None:
    if len(y) == 0 or len(np.unique(y)) < 2:
        return None
    mean = np.nanmean(x, axis=0)
    scale = np.nanstd(x, axis=0)
    scale[~np.isfinite(scale) | (scale < 1e-8)] = 1.0
    xs = np.nan_to_num((x - mean) / scale, nan=0.0, posinf=0.0, neginf=0.0)
    design = np.column_stack([np.ones(len(xs)), xs])
    theta = np.zeros(design.shape[1], dtype=float)
    reg = 2e-3
    for _ in range(steps):
        p = sigmoid(design @ theta)
        grad = (design.T @ (p - y)) / len(y)
        grad[1:] += reg * theta[1:]
        theta -= lr * grad
    return {"theta": theta, "mean": mean, "scale": scale}


def predict(model: dict[str, Any] | None, x: np.ndarray) -> np.ndarray:
    if model is None:
        return np.full(len(x), np.nan)
    xs = np.nan_to_num((x - model["mean"]) / model["scale"], nan=0.0, posinf=0.0, neginf=0.0)
    return sigmoid(np.column_stack([np.ones(len(xs)), xs]) @ model["theta"])


def auc(y: np.ndarray, score: np.ndarray) -> float | None:
    mask = np.isfinite(score)
    y = np.asarray(y)[mask].astype(int)
    score = np.asarray(score)[mask]
    pos, neg = int(y.sum()), int(len(y) - y.sum())
    if pos == 0 or neg == 0:
        return None
    order = np.argsort(score, kind="mergesort")
    sorted_score = score[order]
    ranks = np.empty(len(score), dtype=float)
    i = 0
    while i < len(sorted_score):
        j = i + 1
        while j < len(sorted_score) and sorted_score[j] == sorted_score[i]:
            j += 1
        ranks[order[i:j]] = (i + 1 + j) / 2.0
        i = j
    return float((ranks[y == 1].sum() - pos * (pos + 1) / 2.0) / (pos * neg))


def balanced_accuracy(y: np.ndarray, score: np.ndarray) -> float | None:
    mask = np.isfinite(score)
    y = np.asarray(y)[mask].astype(int)
    score = np.asarray(score)[mask]
    if len(y) == 0 or len(np.unique(y)) < 2:
        return None
    pred = (score >= 0.5).astype(int)
    return float(0.5 * (np.mean(pred[y == 0] == 0) + np.mean(pred[y == 1] == 1)))


def brier(y: np.ndarray, score: np.ndarray) -> float | None:
    mask = np.isfinite(score)
    if not np.any(mask):
        return None
    return float(np.mean((np.asarray(score)[mask] - np.asarray(y)[mask]) ** 2))


def ece(y: np.ndarray, score: np.ndarray, bins: int = 10) -> float | None:
    mask = np.isfinite(score)
    y, score = np.asarray(y)[mask], np.asarray(score)[mask]
    if len(y) == 0:
        return None
    out = 0.0
    for lo, hi in zip(np.linspace(0.0, 1.0, bins, endpoint=False), np.linspace(0.0, 1.0, bins + 1)[1:]):
        select = (score >= lo) & ((score < hi) if hi < 1 else (score <= hi))
        if np.any(select):
            out += float(np.mean(select)) * abs(float(np.mean(score[select])) - float(np.mean(y[select])))
    return out


def rankdata(values: Iterable[float]) -> np.ndarray:
    values = np.asarray(list(values), dtype=float)
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and values[order[j]] == values[order[i]]:
            j += 1
        ranks[order[i:j]] = (i + 1 + j) / 2.0
        i = j
    return ranks


def spearman(a: list[float], b: list[float]) -> float | None:
    if len(a) < 2:
        return None
    ra, rb = rankdata(a), rankdata(b)
    if np.std(ra) < 1e-12 or np.std(rb) < 1e-12:
        return None
    return float(np.corrcoef(ra, rb)[0, 1])


def kendall_tau_a(a: list[float], b: list[float]) -> float | None:
    if len(a) < 2:
        return None
    concordant = discordant = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            left = a[i] - a[j]
            right = b[i] - b[j]
            if left * right > 0:
                concordant += 1
            elif left * right < 0:
                discordant += 1
    total = len(a) * (len(a) - 1) // 2
    return float((concordant - discordant) / total) if total else None


def bootstrap_group_difference(y: np.ndarray, a: np.ndarray, b: np.ndarray, groups: list[str], rng: np.random.Generator, n_boot: int = 1000) -> list[float | None]:
    valid = np.isfinite(a) & np.isfinite(b)
    y, a, b = y[valid], a[valid], b[valid]
    groups = np.asarray(groups)[valid]
    unique = np.asarray(sorted(set(groups)))
    if len(unique) == 0:
        return [None, None, None]
    diffs = np.empty(n_boot)
    for i in range(n_boot):
        chosen = rng.choice(unique, size=len(unique), replace=True)
        sel = np.concatenate([np.flatnonzero(groups == g) for g in chosen])
        diffs[i] = np.mean((a[sel] - y[sel]) ** 2) - np.mean((b[sel] - y[sel]) ** 2)
    observed = float(np.mean((a - y) ** 2) - np.mean((b - y) ** 2))
    return [observed, float(np.quantile(diffs, 0.025)), float(np.quantile(diffs, 0.975))]


def load_episode_metadata(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    info = json.loads((root / "meta/info.json").read_text())
    p = root / "meta/episodes/chunk-000/file-000.parquet"
    columns = ["episode_index", "tasks", "length", "success", "success_class", "policy_repo_id", "policy_type"]
    rows = pq.read_table(p, columns=columns).to_pylist()
    episodes = []
    for row in rows:
        episodes.append({
            "episode_index": int(row["episode_index"]),
            "task": row["tasks"][0] if row.get("tasks") else "<missing>",
            "length_metadata": int(row["length"]),
            "success": int(row["success"]),
            "success_class": str(row["success_class"]),
            "policy_repo_id": str(row.get("policy_repo_id") or ""),
            "policy_type": str(row.get("policy_type") or ""),
        })
    return episodes, info


def load_sequences(root: Path, episodes: list[dict[str, Any]]) -> tuple[dict[int, np.ndarray], dict[str, Any]]:
    max_id = max(e["episode_index"] for e in episodes)
    chunks: list[list[np.ndarray]] = [[] for _ in range(max_id + 1)]
    counts = np.zeros(max_id + 1, dtype=np.int64)
    done_counts = np.zeros(max_id + 1, dtype=np.int64)
    done_last = np.full(max_id + 1, -1, dtype=np.int64)
    reward_sum = np.zeros(max_id + 1, dtype=float)
    data_files = sorted((root / "data").glob("chunk-*/file-*.parquet"))
    state_dim = action_dim = None
    for path in data_files:
        table = pq.read_table(path, columns=["action", "observation.state", "frame_index", "episode_index", "next.reward", "next.done"])
        action_col = table["action"].combine_chunks()
        state_col = table["observation.state"].combine_chunks()
        action_dim = action_col.type.value_type if hasattr(action_col.type, "value_type") else action_dim
        actions = np.asarray(action_col.values.to_numpy(), dtype=float).reshape(-1, len(action_col.values) // len(action_col))
        states = np.asarray(state_col.values.to_numpy(), dtype=float).reshape(-1, len(state_col.values) // len(state_col))
        # Fixed-size list lengths are inferred without relying on metadata names.
        if action_col.type.list_size if hasattr(action_col.type, "list_size") else False:
            actions = np.asarray(action_col.values.to_numpy(), dtype=float).reshape(-1, action_col.type.list_size)
        if state_col.type.list_size if hasattr(state_col.type, "list_size") else False:
            states = np.asarray(state_col.values.to_numpy(), dtype=float).reshape(-1, state_col.type.list_size)
        # Armnet uses variable-length list columns; infer channel width from the first row.
        if actions.shape[1] != len(action_col[0]):
            actions = np.asarray(action_col.values.to_numpy(), dtype=float).reshape(-1, len(action_col[0]))
        if states.shape[1] != len(state_col[0]):
            states = np.asarray(state_col.values.to_numpy(), dtype=float).reshape(-1, len(state_col[0]))
        frame = np.asarray(table["frame_index"].to_numpy(), dtype=np.int64)
        eid = np.asarray(table["episode_index"].to_numpy(), dtype=np.int64)
        reward = np.asarray(table["next.reward"].to_numpy(), dtype=float)
        done = np.asarray(table["next.done"].to_numpy(), dtype=bool)
        values = np.concatenate([states, actions], axis=1)
        starts = np.r_[0, 1 + np.flatnonzero(eid[1:] != eid[:-1])]
        ends = np.r_[starts[1:], len(eid)]
        for start, end in zip(starts, ends):
            episode_id = int(eid[start])
            chunks[episode_id].append(values[start:end])
        for episode_id in np.unique(eid):
            select = eid == episode_id
            counts[episode_id] += int(np.sum(select))
            done_counts[episode_id] += int(np.sum(done[select]))
            if np.any(done[select]):
                done_last[episode_id] = int(frame[select][np.flatnonzero(done[select])[-1]])
            reward_sum[episode_id] += float(np.sum(reward[select]))
    sequences = {i: np.concatenate(parts, axis=0) for i, parts in enumerate(chunks) if parts}
    metadata_by_id = {e["episode_index"]: e for e in episodes}
    length_mismatches = [i for i, e in metadata_by_id.items() if counts[i] != e["length_metadata"]]
    done_mismatches = [i for i, e in metadata_by_id.items() if done_counts[i] != 1 or done_last[i] != e["length_metadata"] - 1]
    reward_mismatches = [i for i, e in metadata_by_id.items() if abs(reward_sum[i] - (1.0 if e["success_class"] == "successful" else 0.0)) > 1e-6]
    return sequences, {"data_files": len(data_files), "length_mismatches": length_mismatches, "done_mismatches": done_mismatches, "reward_mismatches": reward_mismatches, "total_frames_counted": int(np.sum(counts)), "state_action_dim": int(next(iter(sequences.values())).shape[1])}


def normalized_content(sequence: np.ndarray) -> np.ndarray:
    if len(sequence) == 1:
        return np.repeat(sequence, K, axis=0).reshape(-1)
    old_t = np.linspace(0.0, 1.0, len(sequence))
    new_t = np.linspace(0.0, 1.0, K)
    return np.stack([np.interp(new_t, old_t, sequence[:, d]) for d in range(sequence.shape[1])], axis=1).reshape(-1)


def make_records(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    episodes, info = load_episode_metadata(root)
    sequences, checks = load_sequences(root, episodes)
    records = []
    for episode in episodes:
        if episode["policy_type"] == "teleoperated":
            continue
        seq = sequences[episode["episode_index"]]
        record = dict(episode)
        record["length"] = len(seq)
        record["log_length"] = math.log(len(seq))
        record["content"] = normalized_content(seq)
        record["y"] = int(episode["success_class"] == "successful")
        records.append(record)
    counts = Counter(r["success_class"] for r in records)
    return records, {"info": {k: info.get(k) for k in ["robot_type", "total_episodes", "total_frames", "total_tasks", "fps"]}, "episodes_total": len(episodes), "learned_episodes": len(records), "teleoperated_excluded": len(episodes) - len(records), "outcome_counts_learned": dict(counts), "checks": checks}


def crossfit(records: list[dict[str, Any]], feature_key: str, group_key: str) -> dict[str, Any]:
    scores = np.full(len(records), np.nan)
    folds = []
    for group in sorted({r[group_key] for r in records}):
        test = np.asarray([i for i, r in enumerate(records) if r[group_key] == group], dtype=int)
        train = np.asarray([i for i, r in enumerate(records) if r[group_key] != group], dtype=int)
        x_train = np.asarray([records[i][feature_key] for i in train])
        y_train = np.asarray([records[i]["y"] for i in train])
        x_test = np.asarray([records[i][feature_key] for i in test])
        y_test = np.asarray([records[i]["y"] for i in test])
        scores[test] = predict(fit_logistic(x_train, y_train), x_test)
        folds.append({"held_out": group, "n": int(len(test)), "positive": int(y_test.sum()), "auc": auc(y_test, scores[test]), "brier": brier(y_test, scores[test]), "ece": ece(y_test, scores[test])})
    y = np.asarray([r["y"] for r in records])
    return {"scores": scores, "n_scored": int(np.isfinite(scores).sum()), "auc": auc(y, scores), "balanced_accuracy": balanced_accuracy(y, scores), "brier": brier(y, scores), "ece": ece(y, scores), "folds": folds}


def bootstrap_relative_length(records: list[dict[str, Any]], rng: np.random.Generator) -> dict[str, Any]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        groups[(r["task"], r["policy_type"])].append(r)
    z_values = []
    labels = []
    strata = []
    rows = []
    for key, rs in sorted(groups.items()):
        lengths = np.asarray([r["length"] for r in rs], dtype=float)
        mean, sd = float(np.mean(lengths)), float(np.std(lengths))
        z = (lengths - mean) / sd if sd > 1e-8 else np.zeros(len(rs))
        y = np.asarray([r["y"] for r in rs])
        if len(np.unique(y)) < 2:
            continue
        z_values.extend(z.tolist()); labels.extend(y.tolist()); strata.extend([" || ".join(key)] * len(rs))
        success, non = z[y == 1], z[y == 0]
        rows.append({"task": key[0], "policy_type": key[1], "n": len(rs), "successful": int(y.sum()), "non_successful": int((1 - y).sum()), "relative_horizon_success_mean": float(np.mean(success)), "relative_horizon_non_success_mean": float(np.mean(non)), "relative_horizon_auc": auc(y, z)})
    actual = auc(np.asarray(labels), np.asarray(z_values))
    permuted = np.asarray(z_values, dtype=float).copy()
    start = 0
    for row in rows:
        n = row["n"]
        permuted[start : start + n] = rng.permutation(permuted[start : start + n])
        start += n
    permutation_auc = auc(np.asarray(labels), permuted)
    return {"mixed_strata": len(rows), "strata": rows, "pooled_relative_horizon_auc": actual, "within_stratum_permuted_length_auc": permutation_auc, "all_strata_have_shorter_success": all(r["relative_horizon_success_mean"] < r["relative_horizon_non_success_mean"] for r in rows)}


def evaluate_variant(records: list[dict[str, Any]], variant: str) -> dict[str, Any]:
    for r in records:
        if variant == "content":
            r["features"] = r["content"]
        elif variant == "content_plus_length":
            r["features"] = np.concatenate([r["content"], [r["log_length"]]])
        else:
            raise ValueError(variant)
    task = crossfit(records, "features", "task")
    policy = crossfit(records, "features", "policy_type")
    return {"leave_task_out": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in task.items()}, "leave_policy_out": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in policy.items()}}


def ranking_consequence(records: list[dict[str, Any]], task_scores: dict[str, np.ndarray]) -> dict[str, Any]:
    policies = sorted({r["policy_type"] for r in records})
    human = {p: float(np.mean([r["y"] for r in records if r["policy_type"] == p])) for p in policies}
    rows = []
    for p in policies:
        idx = [i for i, r in enumerate(records) if r["policy_type"] == p]
        rows.append({"policy_type": p, "n": len(idx), "human_strict_success_rate": human[p], **{name: float(np.mean(score[idx])) for name, score in task_scores.items()}})
    consequence = {}
    for name in task_scores:
        valid = [r for r in rows if np.isfinite(r[name])]
        score_values = [r[name] for r in valid]
        truth_values = [r["human_strict_success_rate"] for r in valid]
        disagreement = 0
        for i in range(len(valid)):
            for j in range(i + 1, len(valid)):
                if (score_values[i] - score_values[j]) * (truth_values[i] - truth_values[j]) < 0:
                    disagreement += 1
        consequence[name] = {"spearman": spearman(score_values, truth_values), "kendall_tau_a": kendall_tau_a(score_values, truth_values), "pairwise_disagreement_vs_human": disagreement, "order_high_to_low": [r["policy_type"] for r in sorted(valid, key=lambda r: r[name], reverse=True)]}
    return {"policy_scores": rows, "metrics_vs_human": consequence}


def clean(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items() if k != "scores"}
    if isinstance(value, list):
        return [clean(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def run_dataset(root: Path, rng: np.random.Generator) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    records, summary = make_records(root)
    content = crossfit([dict(r) for r in records], "content", "task")
    for r in records:
        r["features"] = np.concatenate([r["content"], [r["log_length"]]])
    plus = crossfit(records, "features", "task")
    content_policy = crossfit([dict(r) for r in records], "content", "policy_type")
    plus_policy = crossfit(records, "features", "policy_type")
    content_result = {"leave_task_out": content, "leave_policy_out": content_policy}
    plus_result = {"leave_task_out": plus, "leave_policy_out": plus_policy}
    task_boot = bootstrap_group_difference(np.asarray([r["y"] for r in records]), content["scores"], plus["scores"], [r["task"] for r in records], rng)
    policy_boot = bootstrap_group_difference(np.asarray([r["y"] for r in records]), content_policy["scores"], plus_policy["scores"], [r["policy_type"] for r in records], rng)
    ranking = ranking_consequence(records, {"content_only": content["scores"], "content_plus_length": plus["scores"]})
    boot = {name: {metric: [] for metric in ["spearman", "kendall_tau_a", "pairwise_disagreement_vs_human"]} for name in ["content_only", "content_plus_length"]}
    tasks = sorted({r["task"] for r in records})
    task_ids = {t: [i for i, r in enumerate(records) if r["task"] == t] for t in tasks}
    for _ in range(1000):
        ids = [i for t in rng.choice(tasks, len(tasks), replace=True) for i in task_ids[t]]
        metrics = ranking_consequence([records[i] for i in ids], {"content_only": content["scores"][ids], "content_plus_length": plus["scores"][ids]})["metrics_vs_human"]
        for name in boot:
            for metric in boot[name]:
                if metrics[name][metric] is not None:
                    boot[name][metric].append(metrics[name][metric])
    ranking["task_cluster_bootstrap_95ci"] = {name: {metric: np.quantile(values, [0.025, 0.975]).tolist() for metric, values in metrics.items()} for name, metrics in boot.items()}
    relative = bootstrap_relative_length(records, rng)
    perm_records = [dict(r) for r in records]
    by_stratum: dict[tuple[str, str], list[int]] = defaultdict(list)
    for i, r in enumerate(perm_records):
        by_stratum[(r["task"], r["policy_type"])].append(i)
    perm_lengths = np.asarray([r["log_length"] for r in perm_records])
    for ids in by_stratum.values():
        perm_lengths[ids] = rng.permutation(perm_lengths[ids])
    for i, r in enumerate(perm_records):
        r["features"] = np.concatenate([r["content"], [perm_lengths[i]]])
    perm_task = crossfit(perm_records, "features", "task")
    result = {
        "summary": summary,
        "relative_horizon": relative,
        "gate_a": {
            "content_only": content_result,
            "content_plus_length": plus_result,
            "length_added_brier_difference_content_minus_plus": {"leave_task_out_bootstrap": task_boot, "leave_policy_out_bootstrap": policy_boot},
            "within_task_policy_permuted_length": {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in perm_task.items() if k != "scores"},
            "ranking_consequence": ranking,
        },
    }
    return result, records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--single-root", type=Path, required=True)
    parser.add_argument("--bimanual-root", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("p0-armnet"))
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    single, _ = run_dataset(args.single_root, rng)
    bimanual = None
    if args.bimanual_root:
        bimanual, _ = run_dataset(args.bimanual_root, rng)
    new_bytes = 0
    if args.bimanual_root and (args.bimanual_root / "DOWNLOAD_MANIFEST.json").exists():
        new_bytes = int(json.loads((args.bimanual_root / "DOWNLOAD_MANIFEST.json").read_text())["downloaded_bytes"])
    result = {"settings": {"K": K, "seed": SEED, "target": "strict success versus failure/suboptimal", "new_downloaded_bytes": new_bytes, "video_used": False, "gpu_used": False, "simulator_used": False}, "single_arm": single, "bimanual": bimanual}
    result = clean(result)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "p05_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    lines = ["# ArmnetBench P0.5 Results", "", f"K={K} normalized time points; target is strict success versus failure/suboptimal; new downloaded bytes={new_bytes}; no video/GPU/simulator.", "", "## Gate A — single-arm", "", "| Variant | Leave-task AUC | Leave-policy AUC | Leave-task balanced accuracy | Leave-policy balanced accuracy | Leave-task Brier | Leave-policy Brier | Leave-task ECE | Leave-policy ECE |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name, key in [("content-only", "content_only"), ("content+log(length)", "content_plus_length")]:
        a = result["single_arm"]["gate_a"][key]
        lines.append(f"| {name} | {a['leave_task_out']['auc']} | {a['leave_policy_out']['auc']} | {a['leave_task_out']['balanced_accuracy']} | {a['leave_policy_out']['balanced_accuracy']} | {a['leave_task_out']['brier']} | {a['leave_policy_out']['brier']} | {a['leave_task_out']['ece']} | {a['leave_policy_out']['ece']} |")
    lines += ["", f"Relative-horizon summary: {result['single_arm']['relative_horizon']}", "", "## Gate B — bimanual", ""]
    if bimanual:
        lines.append("| Variant | Leave-task AUC | Leave-policy AUC | Leave-task balanced accuracy | Leave-policy balanced accuracy | Leave-task Brier | Leave-policy Brier |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for name, key in [("content-only", "content_only"), ("content+log(length)", "content_plus_length")]:
            a = result["bimanual"]["gate_a"][key]
            lines.append(f"| {name} | {a['leave_task_out']['auc']} | {a['leave_policy_out']['auc']} | {a['leave_task_out']['balanced_accuracy']} | {a['leave_policy_out']['balanced_accuracy']} | {a['leave_task_out']['brier']} | {a['leave_policy_out']['brier']} |")
        lines += ["", f"Bimanual relative-horizon summary: {result['bimanual']['relative_horizon']}"]
    else:
        lines.append("Not run.")
    lines += ["", "## Ranking consequence", "", json.dumps(result["single_arm"]["gate_a"]["ranking_consequence"], indent=2), ""]
    (args.out_dir / "p05_results.md").write_text("\n".join(lines))
    print(json.dumps({"new_downloaded_bytes": new_bytes, "single_learned": single["summary"]["learned_episodes"], "single_mixed_strata": single["relative_horizon"]["mixed_strata"], "bimanual_learned": bimanual["summary"]["learned_episodes"] if bimanual else None}, indent=2))


if __name__ == "__main__":
    main()
