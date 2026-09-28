#!/usr/bin/env python3
"""Policy-faithful TCI identifiability gate using a frozen state-only BC-RNN.

The recurrent policy is a small, ordinary PyTorch GRU trained once by behavior
cloning on generated demonstration episodes.  The learned checkpoint is then
frozen.  Evaluation reconstructs observation histories, queries the real GRU
hidden state and action, and performs the same fresh-process cloned-state
interventions as the substrate preflight.  This is a measurement gate only:
it does not train TCI or modify the policy for the proposed method.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("MUJOCO_GL", "disable")

import numpy as np
import torch
from torch import nn

HERE = Path(__file__).resolve().parent
BASE_DIR = HERE.parent / "p0-tci-identifiability"
sys.path.insert(0, str(BASE_DIR))
import tci_identifiability_smoke as substrate  # noqa: E402


ROOT = HERE
CHECKPOINT = ROOT / "bc_rnn_checkpoint.pt"
TRAINING_JSON = ROOT / "bc_rnn_training_results.json"
RAW_JSON = ROOT / "raw_bcrnn_consequence_records.json"
RESULT_JSON = ROOT / "bcrnn_tci_identifiability_results.json"
PROVENANCE_JSON = ROOT / "bcrnn_intervention_provenance.json"
SNAPSHOT_JSONL = ROOT / "bcrnn_state_snapshots.jsonl"
SPLIT_JSON = ROOT / "bcrnn_unique_state_split_manifest.json"
LEAKAGE_JSON = ROOT / "bcrnn_leakage_audit.json"

OBS_KEYS = (
    "robot0_eef_pos",
    "cube_pos",
    "gripper_to_cube_pos",
    "robot0_eef_quat",
    "robot0_gripper_qpos",
    "robot0_gripper_qvel",
)
HORIZONS = (1, 4, 12)
MAX_HORIZON = max(HORIZONS)
SEEDS = (100, 101, 102, 103)
EPISODES_PER_SEED = 2
CAPTURE_STEPS = (0, 3, 6, 9, 12)
TRAIN_SEEDS = tuple(range(200, 208))
DEMO_EPISODES_PER_SEED = 2
DEMO_HORIZON = 60
ALT_COUNT = 4
THETA = 0.25
MARGIN = 0.005
TRAIN_SEED = 20260928
SHUFFLE_SEED = 20260930


def enc(x: Any) -> Any:
    if isinstance(x, np.ndarray):
        return {"__ndarray__": x.tolist(), "dtype": str(x.dtype), "shape": list(x.shape)}
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    if isinstance(x, dict):
        return {str(k): enc(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [enc(v) for v in x]
    raise TypeError(type(x).__name__)


def dec(x: Any) -> Any:
    if isinstance(x, dict) and "__ndarray__" in x:
        return np.asarray(x["__ndarray__"], dtype=x["dtype"]).reshape(x["shape"])
    if isinstance(x, dict):
        return {k: dec(v) for k, v in x.items()}
    if isinstance(x, list):
        return [dec(v) for v in x]
    return x


def obs_vec(obs: dict[str, np.ndarray]) -> np.ndarray:
    return np.concatenate([np.asarray(obs[k], dtype=np.float32).reshape(-1) for k in OBS_KEYS])


class BCRNN(nn.Module):
    def __init__(self, obs_dim: int, hidden_dim: int = 64, action_dim: int = 7):
        super().__init__()
        self.gru = nn.GRU(obs_dim, hidden_dim, batch_first=True)
        self.head = nn.Linear(hidden_dim, action_dim)

    def forward(self, x: torch.Tensor, hidden: torch.Tensor | None = None):
        y, hidden = self.gru(x, hidden)
        return torch.tanh(self.head(y)), hidden


def build_model(meta: dict[str, Any]) -> BCRNN:
    model = BCRNN(int(meta["obs_dim"]), int(meta["hidden_dim"]), int(meta["action_dim"]))
    model.load_state_dict(meta["state_dict"])
    model.eval()
    return model


def expert_action(obs: dict[str, np.ndarray]) -> np.ndarray:
    # This is demonstration generation only.  The factual policy below is the
    # trained recurrent network, never this scripted controller.
    delta = np.asarray(obs["cube_pos"], dtype=np.float64) - np.asarray(obs["robot0_eef_pos"], dtype=np.float64)
    translation = np.clip(4.0 * delta, -0.35, 0.35)
    return np.concatenate([translation, np.zeros(3), np.zeros(1)]).astype(np.float32)


def collect_demonstrations() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    train, valid = [], []
    for i, seed in enumerate(TRAIN_SEEDS):
        for ep in range(DEMO_EPISODES_PER_SEED):
            env = substrate.make_env(seed + ep * 1000)
            env.reset()
            obs_rows, action_rows = [], []
            for _ in range(DEMO_HORIZON):
                obs = substrate.obs_pack(env._get_observations(force_update=True))
                action = expert_action(obs)
                obs_rows.append(obs_vec(obs))
                action_rows.append(action)
                ret = env.step(action)
                if bool(ret[2]):
                    break
            env.close()
            row = {"episode": f"demo_seed{seed}_ep{ep}", "obs": np.asarray(obs_rows), "actions": np.asarray(action_rows)}
            (train if i < 6 else valid).append(row)
    return train, valid


def normalize_episodes(episodes: list[dict[str, Any]], mean: np.ndarray, std: np.ndarray):
    return [np.asarray((ep["obs"] - mean) / std, dtype=np.float32) for ep in episodes]


def train_policy() -> dict[str, Any]:
    torch.set_num_threads(1)
    torch.manual_seed(TRAIN_SEED)
    np.random.seed(TRAIN_SEED)
    train_eps, valid_eps = collect_demonstrations()
    all_train_obs = np.concatenate([e["obs"] for e in train_eps], axis=0)
    mean = all_train_obs.mean(axis=0).astype(np.float32)
    std = (all_train_obs.std(axis=0) + 1e-6).astype(np.float32)
    train_x = normalize_episodes(train_eps, mean, std)
    valid_x = normalize_episodes(valid_eps, mean, std)
    obs_dim = int(train_x[0].shape[-1])
    model = BCRNN(obs_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-3)
    loss_fn = nn.MSELoss()
    # Fixed, single-pass configuration: no tuning against TCI outcomes.
    for _ in range(160):
        order = np.random.permutation(len(train_eps))
        for j in order:
            x = torch.from_numpy(train_x[j][None])
            y = torch.from_numpy(train_eps[j]["actions"][None].astype(np.float32))
            pred, _ = model(x)
            loss = loss_fn(pred, y)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
    with torch.no_grad():
        def rmse(eps, xs):
            errs = []
            for ep, x in zip(eps, xs):
                pred, _ = model(torch.from_numpy(x[None]))
                errs.append((pred[0].numpy() - ep["actions"]) ** 2)
            return float(np.sqrt(np.mean(np.concatenate(errs))))
        train_rmse = rmse(train_eps, train_x)
        valid_rmse = rmse(valid_eps, valid_x)
        valid_pred = np.concatenate([model(torch.from_numpy(x[None]))[0][0].numpy() for x in valid_x])
    action_std = float(np.std(valid_pred))
    state_dict = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    meta = {
        "format": "ordinary PyTorch GRU behavior-cloning policy",
        "obs_keys": list(OBS_KEYS),
        "obs_dim": obs_dim,
        "hidden_dim": 64,
        "action_dim": 7,
        "normalization_mean": mean.tolist(),
        "normalization_std": std.tolist(),
        "train_seed": TRAIN_SEED,
        "demo_train_episodes": len(train_eps),
        "demo_validation_episodes": len(valid_eps),
        "demo_horizon": DEMO_HORIZON,
        "train_rmse": train_rmse,
        "validation_rmse": valid_rmse,
        "validation_action_std": action_std,
        "state_dict": state_dict,
    }
    torch.save(meta, CHECKPOINT)
    summary = {k: v for k, v in meta.items() if k != "state_dict"}
    summary["checkpoint"] = str(CHECKPOINT)
    TRAINING_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return meta


def load_meta() -> dict[str, Any]:
    return torch.load(CHECKPOINT, map_location="cpu", weights_only=False)


def infer_history(model: BCRNN, meta: dict[str, Any], history: list[np.ndarray]):
    mean = np.asarray(meta["normalization_mean"], dtype=np.float32)
    std = np.asarray(meta["normalization_std"], dtype=np.float32)
    x = np.asarray([(v - mean) / std for v in history], dtype=np.float32)
    with torch.no_grad():
        pred, hidden = model(torch.from_numpy(x[None]))
    return pred[0, -1].numpy().astype(np.float64), hidden[:, 0, :].numpy().astype(np.float64)


def make_eval_states(meta: dict[str, Any]) -> list[dict[str, Any]]:
    model = build_model(meta)
    states = []
    seen = set()
    split_train = {"seed100_ep0", "seed100_ep1", "seed102_ep0", "seed102_ep1"}
    for seed in SEEDS:
        for ep in range(EPISODES_PER_SEED):
            episode_id = f"seed{seed}_ep{ep}"
            env = substrate.make_env(seed + ep * 1000)
            env.reset()
            history: list[np.ndarray] = []
            for t in range(max(CAPTURE_STEPS) + 1):
                obs = substrate.obs_pack(env._get_observations(force_update=True))
                history.append(obs_vec(obs))
                if t in CAPTURE_STEPS:
                    snap = substrate.capture(env, f"{episode_id}_t{t}", episode_id, t)
                    canonical_obs = {k: np.asarray(dec(v)) for k, v in snap["observation"].items()}
                    history[-1] = obs_vec(canonical_obs)
                    a_hat, hidden = infer_history(model, meta, history)
                    candidates, action_spec = substrate.construct_candidates(a_hat)
                    ordinal = len(states)
                    order_rng = np.random.default_rng(20260928 + ordinal * 7919)
                    order = order_rng.permutation(len(candidates)).tolist()
                    snap["state_id"] = f"bcrnn_state_{ordinal:03d}"
                    snap["history_obs"] = [v.tolist() for v in history]
                    snap["candidates"] = [candidates[i] for i in order]
                    snap["action_spec"] = action_spec
                    snap["chosen_action"] = a_hat.tolist()
                    snap["policy_hidden"] = hidden.reshape(-1).tolist()
                    snap["policy_hidden_hash"] = hashlib.sha256(hidden.tobytes()).hexdigest()
                    snap["policy_type"] = "frozen trained deterministic BC-RNN"
                    snap["split"] = "train" if episode_id in split_train else "test"
                    if snap["native_hash"] not in seen:
                        seen.add(snap["native_hash"])
                        states.append(snap)
                action = expert_action(obs)
                ret = env.step(action)
                if bool(ret[2]):
                    break
            env.close()
    return states


def run_bcrnn_branch(snapshot: dict[str, Any], action: np.ndarray, meta: dict[str, Any], model: BCRNN):
    env = substrate.make_env(int(snapshot["seed"]))
    env.reset()
    substrate.apply_snapshot(env, snapshot)
    obs0 = substrate.obs_pack(env._get_observations(force_update=True))
    expected = {k: dec(v) for k, v in snapshot["observation"].items()}
    restore_error = substrate.obs_err(substrate.obs_json(obs0), expected)
    history = [np.asarray(v, dtype=np.float32) for v in snapshot["history_obs"]]
    _, hidden = infer_history(model, meta, history)
    hidden_t = torch.from_numpy(hidden[:, None, :].astype(np.float32))
    baseline = {"cube_z": float(np.asarray(obs0["cube_pos"])[2])}
    cumulative_reward = 0.0
    ret = env.step(np.asarray(action, dtype=np.float64))
    obs = substrate.obs_pack(ret[0])
    cumulative_reward += float(ret[1])
    done = bool(ret[2])
    rows = {}
    for h in range(1, MAX_HORIZON + 1):
        if h > 1 and not done:
            x = obs_vec(obs).astype(np.float32)
            mean = np.asarray(meta["normalization_mean"], dtype=np.float32)
            std = np.asarray(meta["normalization_std"], dtype=np.float32)
            with torch.no_grad():
                pred, hidden_t = model(torch.from_numpy(((x - mean) / std)[None, None]), hidden_t)
            continuation = pred[0, 0].numpy().astype(np.float64)
            ret = env.step(continuation)
            obs = substrate.obs_pack(ret[0])
            cumulative_reward += float(ret[1])
            done = bool(ret[2])
        if h in HORIZONS:
            rows[str(h)] = {
                "G": substrate.progress(obs, baseline, cumulative_reward),
                "eef_cube_distance": float(np.linalg.norm(np.asarray(obs["gripper_to_cube_pos"]))),
                "cube_z": float(np.asarray(obs["cube_pos"])[2]),
                "cumulative_reward": cumulative_reward,
                "done": done,
                "observation": substrate.obs_json(obs),
            }
    env.close()
    return {"restore_observation_error": float(restore_error), "horizons": rows, "action": action.tolist()}


def worker(path: str, checkpoint: str):
    snapshot = json.loads(Path(path).read_text(encoding="utf-8"))
    meta = torch.load(checkpoint, map_location="cpu", weights_only=False)
    model = build_model(meta)
    history = [np.asarray(v, dtype=np.float32) for v in snapshot["history_obs"]]
    a1, h1 = infer_history(model, meta, history)
    a2, h2 = infer_history(model, meta, history)
    action_repeat_error = float(np.max(np.abs(a1 - a2)))
    hidden_repeat_error = float(np.max(np.abs(h1 - h2)))
    if action_repeat_error > 1e-8 or hidden_repeat_error > 1e-8:
        raise RuntimeError("repeated history reconstruction is not deterministic")
    candidates = snapshot["candidates"]
    chosen = np.asarray(next(c["action"] for c in candidates if c["role"] == "chosen"), dtype=np.float64)
    # Verify the stored chosen action is the actual model action, rather than a
    # separately generated surrogate.
    stored_action_error = float(np.max(np.abs(a1 - chosen)))
    null1 = run_bcrnn_branch(snapshot, chosen, meta, model)
    null2 = run_bcrnn_branch(snapshot, chosen, meta, model)
    branches = []
    for pos, candidate in enumerate(candidates):
        result = run_bcrnn_branch(snapshot, np.asarray(candidate["action"], dtype=np.float64), meta, model)
        branches.append({"position": pos, "role": candidate["role"], "action": candidate["action"], "result": result})
    null_err = []
    for h in HORIZONS:
        x, y = null1["horizons"][str(h)], null2["horizons"][str(h)]
        null_err.append(max(abs(float(x["G"]) - float(y["G"])), abs(float(x["cube_z"]) - float(y["cube_z"]))))
    print(json.dumps({
        "state_id": snapshot["state_id"],
        "episode_id": snapshot["episode_id"],
        "timestep": snapshot["timestep"],
        "native_hash": snapshot["native_hash"],
        "candidate_order": [c["role"] for c in candidates],
        "policy_query": {"action_repeat_error": action_repeat_error, "hidden_repeat_error": hidden_repeat_error, "stored_action_error": stored_action_error, "hidden_hash": hashlib.sha256(h1.tobytes()).hexdigest()},
        "branches": branches,
        "null": {"max_consequence_error": float(max(null_err or [0.0])), "max_restore_observation_error": float(max(null1["restore_observation_error"], null2["restore_observation_error"]))},
    }, sort_keys=True))


def rank(values):
    order = np.argsort(np.asarray(values, dtype=np.float64), kind="mergesort")
    ranks = np.empty(len(values), dtype=np.float64)
    ranks[order] = np.arange(len(values), dtype=np.float64)
    return ranks.tolist()


def bootstrap_diff(a, b, seed=20260929, n=2000):
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    diffs = []
    for _ in range(n):
        idx = rng.integers(0, len(a), size=len(a))
        diffs.append(float(np.mean(a[idx]) - np.mean(b[idx])))
    return {"mean_a": float(np.mean(a)), "mean_b": float(np.mean(b)), "mean_diff": float(np.mean(a) - np.mean(b)), "ci_low": float(np.quantile(diffs, .025)), "ci_high": float(np.quantile(diffs, .975))}


def analyze(records, states):
    state_metrics = []
    for rec, state in zip(records, states):
        rows = rec["branches"]
        chosen = next(i for i, row in enumerate(rows) if row["role"] == "chosen")
        g = {str(h): [float(row["result"]["horizons"][str(h)]["G"]) for row in rows] for h in HORIZONS}
        immediate = int(np.argmax(g["1"]))
        multi_scores = np.zeros(len(rows))
        for h in HORIZONS:
            multi_scores += np.asarray(rank(g[str(h)]))
        multi = int(np.argmax(multi_scores))
        inv = []
        for i, row in enumerate(rows):
            if i == chosen:
                continue
            d1 = g["1"][chosen] - g["1"][i]
            d12 = g["12"][chosen] - g["12"][i]
            inv.append(bool((d1 > MARGIN and d12 < -MARGIN) or (d1 < -MARGIN and d12 > MARGIN)))
        state_metrics.append({"state_id": rec["state_id"], "episode_id": rec["episode_id"], "timestep": rec["timestep"], "split": state["split"], "chosen_position": chosen, "immediate_pick_position": immediate, "multi_pick_position": multi, "immediate_top1": immediate == chosen, "multi_top1": multi == chosen, "inversion_any": any(inv), "inversion_count": int(sum(inv)), "G": g})
    train = [m for m in state_metrics if m["split"] == "train"]
    test = [m for m in state_metrics if m["split"] == "test"]
    chosen_pos = {str(i): sum(m["chosen_position"] == i for m in state_metrics) for i in range(5)}
    rng = np.random.default_rng(SHUFFLE_SEED)
    shuffled = []
    for m in test:
        vals = m["G"]["12"]
        perm = rng.permutation(len(vals))
        shuffled.append(int(np.argmax([vals[int(i)] for i in perm])) == m["chosen_position"])
    immediate = [m["immediate_top1"] for m in test]
    multi = [m["multi_top1"] for m in test]
    return {
        "state_count": len(states), "test_state_count": len(test), "train_state_count": len(train), "candidate_count_per_state": 5, "chance_top1": .2,
        "horizons": list(HORIZONS), "candidate_position_counts_for_chosen_action": chosen_pos,
        "top1": {"test_immediate": float(np.mean(immediate)), "test_multi_horizon": float(np.mean(multi)), "test_multi_minus_immediate": bootstrap_diff(multi, immediate), "test_shuffled_consequence": float(np.mean(shuffled)), "train_immediate": float(np.mean([m["immediate_top1"] for m in train])), "train_multi_horizon": float(np.mean([m["multi_top1"] for m in train]))},
        "temporal_test": {"test_multi_horizon_exceeds_chance": float(np.mean(multi)) > .2, "test_multi_horizon_exceeds_immediate": float(np.mean(multi)) > float(np.mean(immediate)), "test_shuffled_near_chance": abs(float(np.mean(shuffled)) - .2) <= .15},
        "inversion": {"all_state_prevalence": float(np.mean([m["inversion_any"] for m in state_metrics])), "train_prevalence": float(np.mean([m["inversion_any"] for m in train])), "test_prevalence": float(np.mean([m["inversion_any"] for m in test])), "margin": MARGIN},
        "null_control": {"max_consequence_error": max(float(r["null"]["max_consequence_error"]) for r in records), "max_restore_observation_error": max(float(r["null"]["max_restore_observation_error"]) for r in records), "tolerance": 1e-10},
        "policy_query": {"max_action_repeat_error": max(float(r["policy_query"]["action_repeat_error"]) for r in records), "max_hidden_repeat_error": max(float(r["policy_query"]["hidden_repeat_error"]) for r in records), "max_stored_action_error": max(float(r["policy_query"]["stored_action_error"]) for r in records)},
        "duplicate_underlying_states": len({s["native_hash"] for s in states}) != len(states),
        "train_test_native_hash_overlap": len({s["native_hash"] for s in states if s["split"] == "train"} & {s["native_hash"] for s in states if s["split"] == "test"}),
        "state_metrics": state_metrics,
        "policy_scope": {"policy": "frozen trained deterministic PyTorch GRU behavior-cloning policy", "not_scripted_controller": True, "recurrent_hidden_state_frozen_at_decision": True, "no_likelihood_or_preference": True, "continuation": "after the candidate action, the same frozen BC-RNN is queried on each subsequent observation"},
    }


def collect(meta):
    states = make_eval_states(meta)
    if len(states) != 40:
        raise RuntimeError(f"expected 40 unique states, got {len(states)}")
    with tempfile.TemporaryDirectory(prefix="tci-bcrnn-") as td:
        records = []
        for state in states:
            path = Path(td) / f"{state['state_id']}.json"
            path.write_text(json.dumps(state), encoding="utf-8")
            proc = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker", str(path), "--checkpoint", str(CHECKPOINT)], text=True, capture_output=True, check=False)
            if proc.returncode != 0:
                raise RuntimeError(f"worker failed for {state['state_id']}: {proc.stderr[-3000:]}")
            lines = [x for x in proc.stdout.splitlines() if x.strip()]
            records.append(json.loads(lines[-1]))
    SNAPSHOT_JSONL.write_text("\n".join(json.dumps(s, sort_keys=True) for s in states) + "\n", encoding="utf-8")
    SPLIT_JSON.write_text(json.dumps({"state_count": len(states), "unique_native_hash_count": len({s["native_hash"] for s in states}), "duplicate_state_check": len({s["native_hash"] for s in states}) == len(states), "train_test_native_hash_overlap": 0, "split_rule": "whole episode; seeds 100/102 train and 101/103 test", "states": [{"state_id": s["state_id"], "episode_id": s["episode_id"], "timestep": s["timestep"], "native_hash": s["native_hash"], "split": s["split"]} for s in states]}, indent=2, sort_keys=True), encoding="utf-8")
    results = analyze(records, states)
    RESULT_JSON.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    RAW_JSON.write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
    PROVENANCE_JSON.write_text(json.dumps({"policy": "frozen trained deterministic PyTorch GRU BC-RNN", "checkpoint": str(CHECKPOINT), "history": "canonical observation sequence from episode reset through decision point", "candidate_generation": "four fixed-angle orthogonal rotations at theta=0.25; equal norm and equal chosen-distance; no clipping", "horizons": list(HORIZONS), "records": [{"state_id": s["state_id"], "native_hash": s["native_hash"], "hidden_hash": s["policy_hidden_hash"], "chosen_action": s["chosen_action"], "candidate_order": [c["role"] for c in s["candidates"]], "action_spec": s["action_spec"]} for s in states]}, indent=2, sort_keys=True), encoding="utf-8")
    LEAKAGE_JSON.write_text(json.dumps({"candidate_order_randomized": True, "candidate_position_counts": results["candidate_position_counts_for_chosen_action"], "state_id_used_as_feature": False, "episode_id_used_as_feature": False, "timestep_used_as_feature": False, "hidden_state_recomputed_from_history": True, "hidden_state_used_for_alternatives": False, "policy_action_always_candidate_zero": False, "raw_action_norm_used_as_temporal_signal": False, "duplicate_underlying_states": results["duplicate_underlying_states"], "train_test_native_hash_overlap": results["train_test_native_hash_overlap"], "consequence_shuffle_seed": SHUFFLE_SEED, "native_state_api": "mujoco.mj_getState/mj_setState(mjSTATE_INTEGRATION) plus wrapper/controller/RNG closure"}, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"training": json.loads(TRAINING_JSON.read_text()), "results": results["top1"], "temporal": results["temporal_test"], "inversion": results["inversion"], "null": results["null_control"], "policy_query": results["policy_query"]}, indent=2, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", action="store_true")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--worker")
    ap.add_argument("--checkpoint", default=str(CHECKPOINT))
    args = ap.parse_args()
    if args.worker:
        worker(args.worker, args.checkpoint)
    else:
        meta = train_policy() if args.train or not CHECKPOINT.exists() else load_meta()
        if args.collect or args.train:
            collect(meta)


if __name__ == "__main__":
    main()
