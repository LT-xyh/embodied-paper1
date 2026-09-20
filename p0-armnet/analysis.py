#!/usr/bin/env python3
"""Bounded CPU-only ArmnetBench P0-B analysis.

The script reads only the non-video LeRobot files supplied with --data-root.
It intentionally uses episode metadata plus state/action summary statistics;
no policy, simulator, image, or deep model is used.
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


PREFIX_HORIZONS = (100, 200)
SUMMARY_DIM = 24  # mean and standard deviation for 6 state + 6 action values


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -40.0, 40.0)
    return 1.0 / (1.0 + np.exp(-z))


def fit_logistic(x: np.ndarray, y: np.ndarray, steps: int = 500, lr: float = 0.12) -> dict[str, Any] | None:
    """Small deterministic L2 logistic fit, sufficient for P0 baselines."""
    if len(y) == 0 or len(np.unique(y)) < 2:
        return None
    mean = np.nanmean(x, axis=0)
    scale = np.nanstd(x, axis=0)
    scale[~np.isfinite(scale) | (scale < 1e-8)] = 1.0
    xs = np.nan_to_num((x - mean) / scale, nan=0.0, posinf=0.0, neginf=0.0)
    design = np.column_stack([np.ones(len(xs)), xs])
    theta = np.zeros(design.shape[1], dtype=float)
    reg = 1e-3
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
    pos = int(y.sum())
    neg = len(y) - pos
    if pos == 0 or neg == 0:
        return None
    order = np.argsort(score, kind="mergesort")
    s = score[order]
    ranks = np.empty(len(s), dtype=float)
    i = 0
    while i < len(s):
        j = i + 1
        while j < len(s) and s[j] == s[i]:
            j += 1
        ranks[i:j] = (i + 1 + j) / 2.0
        i = j
    original_ranks = np.empty(len(ranks), dtype=float)
    original_ranks[order] = ranks
    rank_sum = float(original_ranks[y == 1].sum())
    return (rank_sum - pos * (pos + 1) / 2.0) / (pos * neg)


def balanced_accuracy(y: np.ndarray, score: np.ndarray) -> float | None:
    mask = np.isfinite(score)
    y = np.asarray(y)[mask].astype(int)
    pred = (np.asarray(score)[mask] >= 0.5).astype(int)
    if len(y) == 0 or len(np.unique(y)) < 2:
        return None
    out = []
    for cls in (0, 1):
        sel = y == cls
        out.append(float(np.mean(pred[sel] == cls)) if np.any(sel) else np.nan)
    return float(np.nanmean(out))


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


def bootstrap_mean_difference(a: np.ndarray, b: np.ndarray, rng: np.random.Generator, n_boot: int = 500) -> tuple[float, float, float]:
    observed = float(np.mean(a) - np.mean(b))
    if len(a) < 2 or len(b) < 2:
        return observed, float("nan"), float("nan")
    draws = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        draws[i] = np.mean(a[rng.integers(0, len(a), len(a))]) - np.mean(b[rng.integers(0, len(b), len(b))])
    return observed, float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))


def permutation_pvalue(a: np.ndarray, b: np.ndarray, rng: np.random.Generator, n_perm: int = 500) -> float | None:
    if len(a) == 0 or len(b) == 0:
        return None
    observed = abs(float(np.mean(a) - np.mean(b)))
    pooled = np.concatenate([a, b])
    count = 0
    for _ in range(n_perm):
        perm = rng.permutation(pooled)
        if abs(float(np.mean(perm[: len(a)]) - np.mean(perm[len(a) :]))) >= observed - 1e-12:
            count += 1
    return float((count + 1) / (n_perm + 1))


def load_episode_rows(root: Path) -> list[dict[str, Any]]:
    path = root / "meta/episodes/chunk-000/file-000.parquet"
    cols = ["episode_index", "tasks", "length", "success", "success_class", "policy_repo_id", "policy_type"]
    rows = pq.read_table(path, columns=cols).to_pylist()
    out = []
    for row in rows:
        task = row["tasks"][0] if row.get("tasks") else "<missing>"
        out.append(
            {
                "episode_index": int(row["episode_index"]),
                "task": task,
                "length_metadata": int(row["length"]),
                "success": int(row["success"]),
                "success_class": str(row["success_class"]),
                "policy_repo_id": str(row.get("policy_repo_id") or ""),
                "policy_type": str(row.get("policy_type") or ""),
            }
        )
    return out


def aggregate_features(root: Path, episodes: list[dict[str, Any]]) -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    by_id = {e["episode_index"]: e for e in episodes}
    acc: dict[int, dict[str, Any]] = {}
    for e in episodes:
        acc[e["episode_index"]] = {
            "count": 0,
            "done_count": 0,
            "done_frame": None,
            "reward_sum": 0.0,
            "sum": np.zeros(12),
            "sumsq": np.zeros(12),
            "prefix": {h: {"count": 0, "sum": np.zeros(12), "sumsq": np.zeros(12)} for h in PREFIX_HORIZONS},
        }
    files = sorted((root / "data").glob("chunk-*/file-*.parquet"))
    for path in files:
        table = pq.read_table(path, columns=["action", "observation.state", "frame_index", "episode_index", "next.reward", "next.done"])
        for row in table.to_pylist():
            eid = int(row["episode_index"])
            if eid not in by_id:
                continue
            x = np.asarray(row["observation.state"] + row["action"], dtype=float)
            item = acc[eid]
            item["count"] += 1
            item["sum"] += x
            item["sumsq"] += x * x
            item["reward_sum"] += float(row["next.reward"])
            if bool(row["next.done"]):
                item["done_count"] += 1
                item["done_frame"] = int(row["frame_index"])
            frame = int(row["frame_index"])
            for h in PREFIX_HORIZONS:
                if frame < h:
                    pref = item["prefix"][h]
                    pref["count"] += 1
                    pref["sum"] += x
                    pref["sumsq"] += x * x
    mismatches = []
    for eid, e in by_id.items():
        if acc[eid]["count"] != e["length_metadata"]:
            mismatches.append({"episode_index": eid, "metadata": e["length_metadata"], "data": acc[eid]["count"]})
    return acc, {"data_files": len(files), "length_mismatches": mismatches}


def summary(item: dict[str, Any], prefix: int | None = None) -> np.ndarray:
    src = item if prefix is None else item["prefix"][prefix]
    n = max(int(src["count"]), 1)
    mean = src["sum"] / n
    var = np.maximum(src["sumsq"] / n - mean * mean, 0.0)
    return np.concatenate([mean, np.sqrt(var)])


def make_records(episodes: list[dict[str, Any]], acc: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for e in episodes:
        if e["policy_type"] == "teleoperated":
            continue
        a = acc[e["episode_index"]]
        e = dict(e)
        e["length"] = int(a["count"])
        e["log_length"] = math.log1p(e["length"])
        e["full_summary"] = summary(a).tolist()
        e["prefix_summary"] = {str(h): summary(a, h).tolist() for h in PREFIX_HORIZONS if a["prefix"][h]["count"] == h}
        e["done_count"] = int(a["done_count"])
        e["done_frame"] = a["done_frame"]
        e["reward_sum"] = float(a["reward_sum"])
        e["y"] = int(e["success_class"] == "successful")
        records.append(e)
    return records


def frame_semantics_check(episodes: list[dict[str, Any]], acc: dict[int, dict[str, Any]]) -> dict[str, Any]:
    done_count_bad = []
    done_frame_bad = []
    reward_bad = []
    for e in episodes:
        a = acc[e["episode_index"]]
        if a["done_count"] != 1:
            done_count_bad.append(e["episode_index"])
        if a["done_frame"] != e["length_metadata"] - 1:
            done_frame_bad.append(e["episode_index"])
        expected = 1.0 if e["success_class"] == "successful" else 0.0
        if abs(a["reward_sum"] - expected) > 1e-6:
            reward_bad.append(e["episode_index"])
    return {"episodes_checked": len(episodes), "done_count_not_one": done_count_bad, "done_frame_not_last": done_frame_bad, "reward_sum_not_strict_success_indicator": reward_bad}


def crossfit(records: list[dict[str, Any]], feature_key: str, group_key: str) -> dict[str, Any]:
    scores = np.full(len(records), np.nan)
    fold_stats = []
    groups = sorted({r[group_key] for r in records})
    for group in groups:
        test_idx = [i for i, r in enumerate(records) if r[group_key] == group]
        train_idx = [i for i, r in enumerate(records) if r[group_key] != group]
        if not train_idx or len({records[i]["y"] for i in train_idx}) < 2:
            continue
        x_train = np.asarray([records[i][feature_key] for i in train_idx], dtype=float)
        y_train = np.asarray([records[i]["y"] for i in train_idx], dtype=int)
        x_test = np.asarray([records[i][feature_key] for i in test_idx], dtype=float)
        model = fit_logistic(x_train, y_train)
        scores[test_idx] = predict(model, x_test)
        fold_stats.append({"held_out": group, "n": len(test_idx), "positive": int(np.sum([records[i]["y"] for i in test_idx])), "auc": auc(np.asarray([records[i]["y"] for i in test_idx]), scores[test_idx]), "balanced_accuracy": balanced_accuracy(np.asarray([records[i]["y"] for i in test_idx]), scores[test_idx])})
    y = np.asarray([r["y"] for r in records], dtype=int)
    valid = np.isfinite(scores)
    return {"n_scored": int(valid.sum()), "auc": auc(y, scores), "balanced_accuracy": balanced_accuracy(y, scores), "folds": fold_stats, "scores": scores.tolist()}


def build_feature_sets(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for name, key_fn in {
        "length_only": lambda r: [r["log_length"]],
        "nonlength_summary": lambda r: r["full_summary"],
        "nonlength_plus_length": lambda r: [r["log_length"]] + r["full_summary"],
    }.items():
        out[name] = []
        for r in records:
            rr = dict(r); rr["features"] = key_fn(r); out[name].append(rr)
    for h in PREFIX_HORIZONS:
        subset = [r for r in records if str(h) in r["prefix_summary"]]
        for name, key_fn in {
            f"equal_prefix_{h}": lambda r: r["prefix_summary"][str(h)],
        }.items():
            out[name] = []
            for r in subset:
                rr = dict(r); rr["features"] = key_fn(r); out[name].append(rr)
    return out


def strata_report(records: list[dict[str, Any]], rng: np.random.Generator) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        groups[(r["task"], r["policy_type"])].append(r)
    rows = []
    for (task, policy), rs in sorted(groups.items()):
        ys = [r for r in rs if r["y"] == 1]
        ns = [r for r in rs if r["y"] == 0]
        if not ys or not ns:
            continue
        a = np.asarray([r["length"] for r in ys], dtype=float)
        b = np.asarray([r["length"] for r in ns], dtype=float)
        diff, lo, hi = bootstrap_mean_difference(a, b, rng)
        var_a = float(np.var(a, ddof=1)) if len(a) > 1 else 0.0
        var_b = float(np.var(b, ddof=1)) if len(b) > 1 else 0.0
        pooled_sd = math.sqrt(((len(a) - 1) * var_a + (len(b) - 1) * var_b) / max(len(a) + len(b) - 2, 1))
        smd = diff / pooled_sd if pooled_sd > 1e-12 else None
        rows.append({"task": task, "policy_type": policy, "n": len(rs), "successful": len(ys), "non_successful": len(ns), "length_success_mean": float(np.mean(a)), "length_non_success_mean": float(np.mean(b)), "mean_difference_success_minus_non": diff, "bootstrap_95ci": [lo, hi], "standardized_mean_difference": smd, "length_auc": auc(np.asarray([1] * len(a) + [0] * len(b)), np.asarray(list(a) + list(b))), "permutation_p": permutation_pvalue(a, b, rng)})
    diffs = np.asarray([x["mean_difference_success_minus_non"] for x in rows], dtype=float)
    summary = {"mixed_strata": len(rows), "strata_with_shorter_success": int(np.sum(diffs < 0)), "strata_with_longer_success": int(np.sum(diffs > 0)), "median_mean_difference_success_minus_non": float(np.median(diffs)) if len(diffs) else None, "median_abs_standardized_difference": float(np.median([abs(x["standardized_mean_difference"]) for x in rows if x["standardized_mean_difference"] is not None])) if rows else None}
    return rows, summary


def policy_evaluator_consequence(records: list[dict[str, Any]], h: int = 100) -> dict[str, Any]:
    prefix = [r for r in records if str(h) in r["prefix_summary"]]
    # Use identical examples for full and equal-prefix comparisons.
    common_ids = {r["episode_index"] for r in prefix}
    full_common = [r for r in records if r["episode_index"] in common_ids]
    variants = {
        "full_length_plus_summary": (full_common, lambda r: [r["log_length"]] + r["full_summary"]),
        "full_summary_without_length": (full_common, lambda r: r["full_summary"]),
        "equal_duration_prefix": (prefix, lambda r: r["prefix_summary"][str(h)]),
    }
    scores_by_variant: dict[str, dict[int, float]] = {}
    for name, (rs, fn) in variants.items():
        tmp = []
        for r in rs:
            rr = dict(r); rr["features"] = fn(r); tmp.append(rr)
        cf = crossfit(tmp, "features", "task")
        score_map = {r["episode_index"]: cf["scores"][i] for i, r in enumerate(tmp) if np.isfinite(cf["scores"][i])}
        scores_by_variant[name] = score_map
    policy_rows = []
    policies = sorted({r["policy_type"] for r in full_common})
    official = {}
    for p in policies:
        rs = [r for r in full_common if r["policy_type"] == p]
        official[p] = float(np.mean([r["y"] for r in rs]))
        row = {"policy_type": p, "n": len(rs), "human_strict_success_rate": official[p]}
        for name, score_map in scores_by_variant.items():
            vals = [score_map[r["episode_index"]] for r in rs if r["episode_index"] in score_map]
            row[f"evaluator_score_{name}"] = float(np.mean(vals)) if vals else None
        policy_rows.append(row)
    ranking = {}
    for name in variants:
        vals = [row[f"evaluator_score_{name}"] for row in policy_rows if row[f"evaluator_score_{name}"] is not None]
        truth = [row["human_strict_success_rate"] for row in policy_rows if row[f"evaluator_score_{name}"] is not None]
        order = [row["policy_type"] for row in sorted(policy_rows, key=lambda row: row[f"evaluator_score_{name}"], reverse=True) if row[f"evaluator_score_{name}"] is not None]
        ranking[name] = {"policies": [row["policy_type"] for row in policy_rows if row[f"evaluator_score_{name}"] is not None], "order_high_to_low": order, "spearman_vs_human": spearman(vals, truth)}
    reference_order = ranking["full_length_plus_summary"]["order_high_to_low"]
    flips = {}
    for name, info in ranking.items():
        order = info["order_high_to_low"]
        common = [p for p in reference_order if p in order]
        positions = {p: order.index(p) for p in common}
        inversions = sum(positions[a] > positions[b] for i, a in enumerate(common) for b in common[i + 1 :])
        flips[name] = int(inversions)
    return {"prefix_horizon": h, "n_common": len(full_common), "policy_scores": policy_rows, "ranking_vs_human": ranking, "pairwise_order_inversions_vs_full_length_plus_summary": flips}


def clean_for_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): clean_for_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean_for_json(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def downloaded_bytes(root: Path) -> int | None:
    manifest = root / "DOWNLOAD_MANIFEST.json"
    if not manifest.exists():
        return None
    payload = json.loads(manifest.read_text())
    return int(payload["downloaded_bytes"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, default=Path("p0-armnet"))
    args = ap.parse_args()
    rng = np.random.default_rng(20260920)
    episodes = load_episode_rows(args.data_root)
    acc, data_checks = aggregate_features(args.data_root, episodes)
    records = make_records(episodes, acc)
    frame_checks = frame_semantics_check(episodes, acc)
    if not records:
        raise RuntimeError("no learned-policy episodes")
    if data_checks["length_mismatches"]:
        raise RuntimeError(f"episode/data length mismatches: {data_checks['length_mismatches'][:3]}")
    strata, strata_summary = strata_report(records, rng)
    features = build_feature_sets(records)
    baseline_results = {}
    for name, rs in features.items():
        baseline_results[name] = {"n": len(rs), "positive": int(sum(r["y"] for r in rs)), "negative": int(len(rs) - sum(r["y"] for r in rs))}
        task_cv = crossfit(rs, "features", "task")
        policy_cv = crossfit(rs, "features", "policy_type")
        baseline_results[name]["held_out_task"] = {k: v for k, v in task_cv.items() if k != "scores"}
        baseline_results[name]["held_out_policy"] = {k: v for k, v in policy_cv.items() if k != "scores"}
    eval_result = policy_evaluator_consequence(records, h=100)
    outcome_counts = Counter(r["success_class"] for r in records)
    task_counts = Counter(r["task"] for r in records)
    policy_counts = Counter(r["policy_type"] for r in records)
    mixed_strata_counts = {f"{r['task']} || {r['policy_type']}": {"n": r["n"], "successful": r["successful"], "non_successful": r["non_successful"]} for r in strata}
    result = {
        "analysis": {"seed": 20260920, "population": "single-arm learned-policy rollouts only; teleoperation excluded", "prefix_horizons": list(PREFIX_HORIZONS), "summary_features": "mean and standard deviation of six state and six action channels; no explicit length", "downloaded_dataset_bytes": downloaded_bytes(args.data_root), "video_used": False, "gpu_used": False, "simulator_used": False},
        "schema_checks": {"episodes_total": len(episodes), "learned_episodes": len(records), "teleoperated_excluded": len(episodes) - len(records), "outcome_counts_learned": dict(outcome_counts), "task_counts_learned": dict(task_counts), "policy_type_counts_learned": dict(policy_counts), "mixed_strata_counts": mixed_strata_counts, "data_checks": data_checks, "frame_semantics": frame_checks},
        "horizon_strata": {"summary": strata_summary, "strata": strata},
        "baselines": baseline_results,
        "learned_evaluator_consequence": eval_result,
        "interpretation_guard": {"pretrim_provenance": "NONE", "maximum_level_due_to_provenance": "P0 SURVIVES — LEVEL 1", "official_human_leaderboard_untouched": True},
    }
    result = clean_for_json(result)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    s = result["horizon_strata"]["summary"]
    lines = [
        "# ArmnetBench P0-B CPU Leakage Sanity Test",
        "",
        "Population: 2,099 learned-policy single-arm episodes; teleoperation excluded. No images, policy inference, simulator, GPU, or video was used.",
        "",
        f"Outcome counts: {result['schema_checks']['outcome_counts_learned']}",
        f"Mixed task × policy strata: {s['mixed_strata']}; shorter-success strata: {s['strata_with_shorter_success']}; longer-success strata: {s['strata_with_longer_success']}; median success-minus-non-success length difference: {s['median_mean_difference_success_minus_non']}; median absolute standardized difference: {s['median_abs_standardized_difference']}.",
        "",
        "## Cross-held-out baseline results",
        "",
        "| Feature set | n | leave-task-out AUC | leave-policy-out AUC | leave-task-out balanced accuracy | leave-policy-out balanced accuracy |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, b in result["baselines"].items():
        lines.append(f"| {name} | {b['n']} | {b['held_out_task']['auc']} | {b['held_out_policy']['auc']} | {b['held_out_task']['balanced_accuracy']} | {b['held_out_policy']['balanced_accuracy']} |")
    lines += ["", "## Learned evaluator consequence", "", "The evaluator comparison is restricted to the common subset with at least 100 frames. Scores are cross-fitted by held-out task; the human strict-success rate is only a ground-truth reference.", "", "| Policy | n | human strict success | full + length | full without length | equal-duration prefix |", "|---|---:|---:|---:|---:|---:|"]
    for row in result["learned_evaluator_consequence"]["policy_scores"]:
        lines.append(f"| {row['policy_type']} | {row['n']} | {row['human_strict_success_rate']:.4f} | {row.get('evaluator_score_full_length_plus_summary')} | {row.get('evaluator_score_full_summary_without_length')} | {row.get('evaluator_score_equal_duration_prefix')} |")
    lines += ["", f"Pairwise order inversions relative to full + length: {result['learned_evaluator_consequence']['pairwise_order_inversions_vs_full_length_plus_summary']}"]
    lines += ["", "## Guarded interpretation", "", "The release documents outcome-dependent trimming, but no released `success_cutoff_time` column or deterministic link to the original untrimmed rollout was found in the inspected artifacts. Therefore the strongest allowable interpretation is released-support leakage association (Level 1), not a causal post-processing effect. See `artifact_audit.md`.", ""]
    (args.out_dir / "results.md").write_text("\n".join(lines))
    print(json.dumps({"learned_episodes": len(records), "mixed_strata": s["mixed_strata"], "shorter_success_strata": s["strata_with_shorter_success"], "downloaded_dataset_bytes": result["analysis"]["downloaded_dataset_bytes"], "results": str(args.out_dir / 'results.json')}, indent=2))


if __name__ == "__main__":
    main()
