#!/usr/bin/env python3
"""Bounded TCI consequence-identifiability preflight.

This script is deliberately a measurement gate, not a TCI training method.  It
uses the already-qualified native robosuite wrapper snapshot path and a small,
fully deterministic state-only controller solely to make the chosen action
observable before a real BC-RNN checkpoint is available.  Every branch is
restored from a serialized wrapper state in a fresh subprocess.
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

# Keep the bounded preflight CPU-only and single-threaded in every fresh worker.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("MUJOCO_GL", "disable")

import numpy as np
import mujoco
import robosuite as suite

ROOT = Path(__file__).resolve().parent
OUT = ROOT
SPEC = mujoco.mjtState.mjSTATE_INTEGRATION
CONFIG_BASE = dict(
    env_name="Lift",
    robots="Panda",
    has_renderer=False,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    control_freq=20,
    hard_reset=True,
)
HORIZONS = (1, 4, 12)
MAX_HORIZON = max(HORIZONS)
ALT_COUNT = 4
THETA = 0.25
ACTION_NORM_EPS = 0.05
PROGRESS_MARGIN = 0.005
CONTROLLER_SCALE = 4.0
SEEDS = (100, 101, 102, 103)
EPISODES_PER_SEED = 2
CAPTURE_STEPS = (0, 3, 6, 9, 12)
SPLIT_TRAIN_EPISODES = {"seed100_ep0", "seed100_ep1", "seed102_ep0", "seed102_ep1"}


def enc(x: Any) -> Any:
    if isinstance(x, np.ndarray):
        return {"__ndarray__": x.tolist(), "dtype": str(x.dtype), "shape": list(x.shape)}
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    if isinstance(x, dict):
        return {str(k): enc(v) for k, v in x.items() if not str(k).startswith("_sim")}
    if isinstance(x, (list, tuple)):
        return [enc(v) for v in x]
    return None


def dec(x: Any) -> Any:
    if isinstance(x, dict) and "__ndarray__" in x:
        return np.asarray(x["__ndarray__"], dtype=x["dtype"]).reshape(x["shape"])
    if isinstance(x, dict):
        return {k: dec(v) for k, v in x.items()}
    if isinstance(x, list):
        return [dec(v) for v in x]
    return x


def snap_numeric(obj: Any, skip: tuple[str, ...] = ()) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if not hasattr(obj, "__dict__"):
        return out
    ignored = {
        "sim", "model", "robot_model", "viewer", "renderer", "_sensor",
        "_corrupter", "_filter", "_delayer",
    } | set(skip)
    for k, v in obj.__dict__.items():
        if k in ignored:
            continue
        if isinstance(v, (np.ndarray, np.generic, float, int, bool, str)) or v is None:
            out[k] = enc(v)
        elif isinstance(v, dict):
            z = snap_dict(v)
            if z:
                out[k] = z
        elif hasattr(v, "__dict__"):
            z = snap_numeric(v)
            if z:
                out[k] = {"__object__": z}
    return out


def snap_dict(d: dict[Any, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, (np.ndarray, np.generic, float, int, bool, str)) or v is None:
            out[str(k)] = enc(v)
        elif isinstance(v, dict):
            out[str(k)] = snap_dict(v)
    return out


def restore_numeric(obj: Any, snap: dict[str, Any]) -> None:
    for k, v in snap.items():
        if k not in getattr(obj, "__dict__", {}):
            continue
        if isinstance(v, dict) and "__object__" in v:
            restore_numeric(getattr(obj, k), v["__object__"])
        elif isinstance(v, dict) and "__ndarray__" not in v:
            cur = getattr(obj, k)
            if isinstance(cur, dict):
                restore_dict(cur, v)
        else:
            try:
                setattr(obj, k, dec(v))
            except Exception:
                pass


def restore_dict(cur: dict[Any, Any], snap: dict[str, Any]) -> None:
    for k, v in snap.items():
        if isinstance(v, dict) and "__ndarray__" not in v:
            restore_dict(cur.setdefault(k, {}), v)
        else:
            cur[k] = dec(v)


def make_env(seed: int):
    cfg = suite.load_composite_controller_config(controller="BASIC")
    cfg = copy.deepcopy(cfg)
    kwargs = dict(CONFIG_BASE)
    kwargs["seed"] = int(seed)
    return suite.make(controller_configs=cfg, **kwargs)


def obs_pack(obs: Any) -> dict[str, np.ndarray]:
    return {k: np.asarray(v).copy() for k, v in obs.items()}


def obs_json(obs: dict[str, np.ndarray]) -> dict[str, Any]:
    return {k: enc(v) for k, v in obs.items()}


def obs_err(a: dict[str, Any], b: dict[str, Any]) -> float:
    keys = sorted(set(a) | set(b))
    errs = []
    for k in keys:
        if k not in a or k not in b:
            return float("inf")
        errs.append(float(np.max(np.abs(np.asarray(dec(a[k])) - np.asarray(dec(b[k]))))))
    return max(errs or [0.0])


def capture(env: Any, label: str, episode_id: str, timestep: int) -> dict[str, Any]:
    # Canonicalize derived MuJoCo quantities before freezing the state.  A
    # preceding controller step may leave site/observable caches stale until a
    # forward pass; recording after this explicit forward makes the replay
    # target itself reproducible.
    env.sim.forward()
    env._update_observables(force=True)
    model, data = env.sim.model._model, env.sim.data._data
    n = mujoco.mj_stateSize(model, SPEC)
    state = np.zeros(n, dtype=np.float64)
    mujoco.mj_getState(model, data, state, SPEC)
    obs = obs_pack(env._get_observations(force_update=True))
    robots = []
    for robot in env.robots:
        parts = {
            name: snap_numeric(pc)
            for name, pc in robot.composite_controller.part_controllers.items()
        }
        robots.append({
            "robot": snap_numeric(robot),
            "controller": snap_numeric(robot.composite_controller),
            "parts": parts,
            "gripper": {name: snap_numeric(g) for name, g in robot.gripper.items()},
        })
    observables = {k: snap_numeric(v) for k, v in env._observables.items()}
    return {
        "label": label,
        "episode_id": episode_id,
        "timestep": int(timestep),
        "seed": int(env.seed),
        "native_state": state.tolist(),
        "native_hash": hashlib.sha256(state.tobytes()).hexdigest(),
        "env": {
            "cur_time": enc(env.cur_time),
            "timestep": enc(env.timestep),
            "done": enc(env.done),
            "ep_meta": enc(env.get_ep_meta()),
            "rng_state": enc(env.rng.bit_generator.state),
            "seed": enc(env.seed),
            "obs_cache": enc(env._obs_cache),
        },
        "observables": observables,
        "robots": robots,
        "sim_aux": {
            "ctrl": np.asarray(data.ctrl).copy().tolist(),
            "qfrc_applied": np.asarray(data.qfrc_applied).copy().tolist(),
            "xfrc_applied": np.asarray(data.xfrc_applied).copy().tolist(),
            "qacc_warmstart": np.asarray(data.qacc_warmstart).copy().tolist(),
            "qacc": np.asarray(data.qacc).copy().tolist(),
        },
        "observation": obs_json(obs),
        "action_dim": int(env.action_dim),
        "closure_api": "mujoco.mj_getState/mj_setState(mjSTATE_INTEGRATION) plus explicit data control/force buffers",
    }


def apply_snapshot(env: Any, snapshot: dict[str, Any]) -> None:
    model, data = env.sim.model._model, env.sim.data._data
    vec = np.asarray(snapshot["native_state"], dtype=np.float64)
    mujoco.mj_setState(model, data, vec, SPEC)
    mujoco.mj_forward(model, data)
    e = snapshot["env"]
    env.cur_time = dec(e["cur_time"])
    env.timestep = dec(e["timestep"])
    env.done = dec(e["done"])
    env.set_ep_meta(dec(e["ep_meta"]))
    env.rng.bit_generator.state = dec(e["rng_state"])
    env._obs_cache = dec(e["obs_cache"])
    for k, v in snapshot["observables"].items():
        if k in env._observables:
            restore_numeric(env._observables[k], v)
    for robot, sr in zip(env.robots, snapshot["robots"]):
        restore_numeric(robot, sr["robot"])
        restore_numeric(robot.composite_controller, sr["controller"])
        for name, part in sr["parts"].items():
            if name in robot.composite_controller.part_controllers:
                restore_numeric(robot.composite_controller.part_controllers[name], part)
        for name, gv in sr["gripper"].items():
            if name in robot.gripper:
                restore_numeric(robot.gripper[name], gv)
    aux = snapshot.get("sim_aux", {})
    for name in ("ctrl", "qfrc_applied", "xfrc_applied", "qacc_warmstart"):
        if name in aux and hasattr(data, name):
            arr = np.asarray(aux[name], dtype=np.float64)
            getattr(data, name)[:] = arr
    env.sim.forward()
    # mj_forward updates warm-start/control fields. Restore the complete
    # integration vector once more after derived quantities are refreshed; no
    # raw state index is interpreted here.
    mujoco.mj_setState(model, data, vec, SPEC)
    if "qacc" in aux and hasattr(data, "qacc"):
        data.qacc[:] = np.asarray(aux["qacc"], dtype=np.float64)
    env._update_observables(force=True)


def policy_action(obs: dict[str, np.ndarray]) -> np.ndarray:
    """Frozen deterministic state-only controller used only for this preflight.

    It is intentionally not a trained TCI method or a likelihood model.  The
    first three dimensions move toward the observed cube, the next three keep
    the current orientation command neutral, and the gripper command is neutral.
    """
    delta = np.asarray(obs["cube_pos"], dtype=np.float64) - np.asarray(obs["robot0_eef_pos"], dtype=np.float64)
    translation = np.clip(CONTROLLER_SCALE * delta, -0.35, 0.35)
    action = np.concatenate([translation, np.zeros(3, dtype=np.float64), np.zeros(1, dtype=np.float64)])
    return np.clip(action, -1.0, 1.0)


def orthogonal_basis(u: np.ndarray, count: int) -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for axis in np.eye(len(u), dtype=np.float64):
        v = axis.copy()
        v -= float(np.dot(v, u)) * u
        for q in basis:
            v -= float(np.dot(v, q)) * q
        n = float(np.linalg.norm(v))
        if n > 1e-10:
            basis.append(v / n)
        if len(basis) == count:
            break
    if len(basis) != count:
        raise RuntimeError("could not construct deterministic action basis")
    return basis


def construct_candidates(a_hat: np.ndarray) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    norm = float(np.linalg.norm(a_hat))
    if norm < ACTION_NORM_EPS:
        raise ValueError(f"chosen action norm {norm:.8f} below predeclared threshold")
    u = a_hat / norm
    basis = orthogonal_basis(u, ALT_COUNT)
    alternatives = []
    for i, v in enumerate(basis):
        alt = norm * (math.cos(THETA) * u + math.sin(THETA) * v)
        if np.any(alt < -1.0 - 1e-12) or np.any(alt > 1.0 + 1e-12):
            raise ValueError("equal-radius action leaves normalized executable domain")
        alternatives.append(alt)
    # Equal-norm means both ||a_i|| == ||a_hat|| and ||a_i-a_hat|| is fixed.
    expected_delta = 2.0 * norm * math.sin(THETA / 2.0)
    candidates = [{"role": "chosen", "action": a_hat.tolist()}]
    candidates.extend({"role": f"alt_{i}", "action": a.tolist()} for i, a in enumerate(alternatives))
    return candidates, {
        "definition": "normalized 7D robosuite controller vector; alternatives are fixed-angle rotations of the selected action",
        "absolute_action_norm": norm,
        "theta_radians": THETA,
        "expected_delta_norm": expected_delta,
        "action_bounds": [-1.0, 1.0],
        "validity": "all components inside normalized robosuite action bounds; no clipping after construction",
        "representation": "Panda BASIC composite controller action [xyz, rotation xyz, gripper]",
    }


def progress(obs: dict[str, np.ndarray], baseline: dict[str, float], cumulative_reward: float) -> float:
    dist = float(np.linalg.norm(np.asarray(obs["gripper_to_cube_pos"], dtype=np.float64)))
    cube_z = float(np.asarray(obs["cube_pos"], dtype=np.float64)[2])
    # Frozen task-progress functional: approach distance, lift displacement,
    # and observed environment reward; all are real task/environment quantities.
    return -dist + 4.0 * (cube_z - baseline["cube_z"]) + 0.1 * cumulative_reward


def run_branch(snapshot: dict[str, Any], action: np.ndarray) -> dict[str, Any]:
    env = make_env(int(snapshot["seed"]))
    env.reset()
    apply_snapshot(env, snapshot)
    obs0 = obs_pack(env._get_observations(force_update=True))
    expected = {k: dec(v) for k, v in snapshot["observation"].items()}
    restore_obs_error = obs_err(obs_json(obs0), expected)
    baseline = {"cube_z": float(np.asarray(obs0["cube_pos"])[2])}
    cumulative_reward = 0.0
    horizon_rows: dict[str, Any] = {}
    ret = env.step(np.asarray(action, dtype=np.float64))
    obs = obs_pack(ret[0])
    cumulative_reward += float(ret[1])
    done = bool(ret[2])
    for h in range(1, MAX_HORIZON + 1):
        if h > 1 and not done:
            cont = policy_action(obs)
            ret = env.step(cont)
            obs = obs_pack(ret[0])
            cumulative_reward += float(ret[1])
            done = bool(ret[2])
        if h in HORIZONS:
            horizon_rows[str(h)] = {
                "G": progress(obs, baseline, cumulative_reward),
                "eef_cube_distance": float(np.linalg.norm(np.asarray(obs["gripper_to_cube_pos"]))),
                "cube_z": float(np.asarray(obs["cube_pos"])[2]),
                "cumulative_reward": float(cumulative_reward),
                "done": bool(done),
                "observation": obs_json(obs),
            }
    env.close()
    return {
        "restore_observation_error": float(restore_obs_error),
        "horizons": horizon_rows,
        "action": action.tolist(),
    }


def worker(path: str) -> None:
    snapshot = json.load(open(path, "r", encoding="utf-8"))
    candidates = snapshot["candidates"]
    chosen = np.asarray(next(c["action"] for c in candidates if c["role"] == "chosen"), dtype=np.float64)
    null1 = run_branch(snapshot, chosen)
    null2 = run_branch(snapshot, chosen)
    branches = []
    for pos, candidate in enumerate(candidates):
        result = run_branch(snapshot, np.asarray(candidate["action"], dtype=np.float64))
        branches.append({"position": pos, "role": candidate["role"], "action": candidate["action"], "result": result})
    null_state = []
    for h in HORIZONS:
        a = null1["horizons"][str(h)]
        b = null2["horizons"][str(h)]
        null_state.append(max(abs(float(a["G"]) - float(b["G"])), abs(float(a["cube_z"]) - float(b["cube_z"]))))
    print(json.dumps({
        "state_id": snapshot["state_id"],
        "episode_id": snapshot["episode_id"],
        "timestep": snapshot["timestep"],
        "native_hash": snapshot["native_hash"],
        "candidate_order": [c["role"] for c in candidates],
        "branches": branches,
        "null": {
            "max_consequence_error": float(max(null_state or [0.0])),
            "max_restore_observation_error": float(max(null1["restore_observation_error"], null2["restore_observation_error"])),
        },
    }, sort_keys=True))


def generate_states() -> list[dict[str, Any]]:
    states: list[dict[str, Any]] = []
    seen_hashes: set[str] = set()
    for seed in SEEDS:
        for ep in range(EPISODES_PER_SEED):
            episode_id = f"seed{seed}_ep{ep}"
            env = make_env(seed + ep * 1000)
            env.reset()
            for t in range(max(CAPTURE_STEPS) + 1):
                obs = obs_pack(env._get_observations(force_update=True))
                if t in CAPTURE_STEPS:
                    snap = capture(env, f"{episode_id}_t{t}", episode_id, t)
                    snap["state_id"] = f"state_{len(states):03d}"
                    obs = {k: np.asarray(dec(v)) for k, v in snap["observation"].items()}
                    a_hat = policy_action(obs)
                    candidates, action_spec = construct_candidates(a_hat)
                    order_rng = np.random.default_rng(20260928 + len(states) * 7919)
                    order = order_rng.permutation(len(candidates)).tolist()
                    snap["candidates"] = [candidates[i] for i in order]
                    snap["action_spec"] = action_spec
                    snap["chosen_action"] = a_hat.tolist()
                    snap["baseline"] = {"cube_z": float(np.asarray(obs["cube_pos"])[2])}
                    if snap["native_hash"] not in seen_hashes:
                        seen_hashes.add(snap["native_hash"])
                        states.append(snap)
                action = policy_action(obs)
                ret = env.step(action)
                if bool(ret[2]):
                    break
            env.close()
    return states


def rank_score(values: list[float]) -> list[float]:
    order = np.argsort(np.asarray(values, dtype=np.float64), kind="mergesort")
    ranks = np.empty(len(values), dtype=np.float64)
    ranks[order] = np.arange(len(values), dtype=np.float64)
    return ranks.tolist()


def bootstrap_diff(a: list[float], b: list[float], seed: int = 20260929, n: int = 2000) -> dict[str, float]:
    if not a or not b:
        return {"mean_a": float("nan"), "mean_b": float("nan"), "mean_diff": float("nan"), "ci_low": float("nan"), "ci_high": float("nan")}
    rng = np.random.default_rng(seed)
    aa, bb = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    diffs = []
    for _ in range(n):
        idx = rng.integers(0, len(aa), size=len(aa))
        diffs.append(float(np.mean(aa[idx]) - np.mean(bb[idx])))
    return {
        "mean_a": float(np.mean(aa)),
        "mean_b": float(np.mean(bb)),
        "mean_diff": float(np.mean(aa) - np.mean(bb)),
        "ci_low": float(np.quantile(diffs, 0.025)),
        "ci_high": float(np.quantile(diffs, 0.975)),
    }


def analyze(records: list[dict[str, Any]], states: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {s["state_id"]: s for s in states}
    state_metrics = []
    candidate_count = ALT_COUNT + 1
    for rec in records:
        rows = rec["branches"]
        chosen_idx = next(i for i, row in enumerate(rows) if row["role"] == "chosen")
        g = {str(h): [float(row["result"]["horizons"][str(h)]["G"]) for row in rows] for h in HORIZONS}
        chosen_g = {str(h): g[str(h)][chosen_idx] for h in HORIZONS}
        immediate_pick = int(np.argmax(g["1"]))
        multi_scores = np.zeros(candidate_count, dtype=np.float64)
        for h in HORIZONS:
            multi_scores += np.asarray(rank_score(g[str(h)]), dtype=np.float64)
        multi_pick = int(np.argmax(multi_scores))
        inversion_flags = []
        inversion_deltas = []
        for i, row in enumerate(rows):
            if i == chosen_idx:
                continue
            d1 = chosen_g["1"] - g["1"][i]
            d12 = chosen_g["12"] - g["12"][i]
            inv = (d1 > PROGRESS_MARGIN and d12 < -PROGRESS_MARGIN) or (d1 < -PROGRESS_MARGIN and d12 > PROGRESS_MARGIN)
            inversion_flags.append(bool(inv))
            inversion_deltas.append({"role": row["role"], "D1": d1, "D12": d12, "inversion": bool(inv)})
        state_metrics.append({
            "state_id": rec["state_id"],
            "episode_id": rec["episode_id"],
            "timestep": rec["timestep"],
            "split": "train" if rec["episode_id"] in SPLIT_TRAIN_EPISODES else "test",
            "chosen_position": chosen_idx,
            "immediate_pick_position": immediate_pick,
            "multi_pick_position": multi_pick,
            "immediate_top1": immediate_pick == chosen_idx,
            "multi_top1": multi_pick == chosen_idx,
            "inversion_any": any(inversion_flags),
            "inversion_count": int(sum(inversion_flags)),
            "inversion_deltas": inversion_deltas,
            "G": g,
            "chosen_G": chosen_g,
        })
    def split(name: str) -> list[dict[str, Any]]:
        return [m for m in state_metrics if m["split"] == name]
    train, test = split("train"), split("test")
    # Shuffled controls preserve each state's consequence multiset but break its
    # consequence-to-action mapping. Candidate ordering remains randomized.
    rng = np.random.default_rng(20260930)
    shuffled_top1 = []
    for m in test:
        chosen_pos = int(m["chosen_position"])
        values = list(m["G"]["12"])
        perm = rng.permutation(len(values))
        shuffled_values = [values[int(i)] for i in perm]
        shuffled_top1.append(int(np.argmax(shuffled_values)) == chosen_pos)
    test_immediate = [bool(m["immediate_top1"]) for m in test]
    test_multi = [bool(m["multi_top1"]) for m in test]
    train_immediate = [bool(m["immediate_top1"]) for m in train]
    train_multi = [bool(m["multi_top1"]) for m in train]
    chosen_positions = [int(m["chosen_position"]) for m in state_metrics]
    position_counts = {str(i): int(chosen_positions.count(i)) for i in range(candidate_count)}
    all_null_errors = [float(r["null"]["max_consequence_error"]) for r in records]
    all_restore_errors = [float(r["null"]["max_restore_observation_error"]) for r in records]
    duplicates = len({s["native_hash"] for s in states}) != len(states)
    train_hashes = {s["native_hash"] for s in states if s["episode_id"] in SPLIT_TRAIN_EPISODES}
    test_hashes = {s["native_hash"] for s in states if s["episode_id"] not in SPLIT_TRAIN_EPISODES}
    return {
        "state_count": len(states),
        "candidate_count_per_state": candidate_count,
        "horizons": list(HORIZONS),
        "unique_native_state_count": len({s["native_hash"] for s in states}),
        "duplicate_underlying_states": bool(duplicates),
        "train_state_count": len(train),
        "test_state_count": len(test),
        "train_test_native_hash_overlap": len(train_hashes & test_hashes),
        "candidate_position_counts_for_chosen_action": position_counts,
        "candidate_order_uniformity": {"expected_each": len(states) / candidate_count, "max_abs_deviation": max(abs(v - len(states) / candidate_count) for v in position_counts.values())},
        "null_control": {"max_consequence_error": max(all_null_errors or [0.0]), "max_restore_observation_error": max(all_restore_errors or [0.0]), "tolerance": 1e-10},
        "chance_top1": 1.0 / candidate_count,
        "top1": {
            "train_immediate": float(np.mean(train_immediate or [float("nan")])),
            "train_multi_horizon": float(np.mean(train_multi or [float("nan")])),
            "test_immediate": float(np.mean(test_immediate or [float("nan")])),
            "test_multi_horizon": float(np.mean(test_multi or [float("nan")])),
            "test_shuffled_consequence": float(np.mean(shuffled_top1 or [float("nan")])),
            "test_multi_minus_immediate": bootstrap_diff([float(x) for x in test_multi], [float(x) for x in test_immediate]),
        },
        "temporal_test": {
            "test_multi_horizon_exceeds_immediate": bool(np.mean(test_multi or [0.0]) > np.mean(test_immediate or [0.0])),
            "test_multi_horizon_exceeds_chance": bool(np.mean(test_multi or [0.0]) > 1.0 / candidate_count),
            "test_shuffled_near_chance": bool(abs(np.mean(shuffled_top1 or [0.0]) - 1.0 / candidate_count) <= 0.15),
        },
        "inversion": {
            "all_state_prevalence": float(np.mean([m["inversion_any"] for m in state_metrics] or [float("nan")])),
            "train_prevalence": float(np.mean([m["inversion_any"] for m in train] or [float("nan")])),
            "test_prevalence": float(np.mean([m["inversion_any"] for m in test] or [float("nan")])),
            "margin": PROGRESS_MARGIN,
            "definition": "sign(D_1) != sign(D_12) with both magnitudes > margin; D_H = G_H(chosen)-G_H(alternative)",
        },
        "state_metrics": state_metrics,
        "policy_scope": {
            "policy": "deterministic state-only scripted controller used as a measurement stub",
            "not_bc_rnn": True,
            "no_likelihood_or_preference": True,
            "continuation": "after first candidate action, the same deterministic controller is stepped for remaining horizons",
        },
    }


def run_collection() -> None:
    states = generate_states()
    if len(states) < 32:
        raise RuntimeError(f"BLOCKED: only {len(states)} unique states; refusing to fabricate a preflight sample")
    with tempfile.TemporaryDirectory(prefix="tci-preflight-") as td:
        records = []
        for s in states:
            path = Path(td) / f"{s['state_id']}.json"
            path.write_text(json.dumps(s), encoding="utf-8")
            proc = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker", str(path)], text=True, capture_output=True, check=False)
            if proc.returncode != 0:
                raise RuntimeError(f"worker failed for {s['state_id']}: {proc.stderr[-2000:]}")
            lines = [line for line in proc.stdout.splitlines() if line.strip()]
            try:
                records.append(json.loads(lines[-1]))
            except Exception as exc:
                raise RuntimeError(f"worker JSON parse failed for {s['state_id']}: {proc.stdout[-2000:]} / {proc.stderr[-2000:]}") from exc
    # Keep snapshots and exact action/candidate provenance together; this is the
    # replayable intervention record, not a duplicated training table.
    snapshots_path = OUT / "state_snapshots.jsonl"
    with snapshots_path.open("w", encoding="utf-8") as f:
        for s in states:
            f.write(json.dumps(s, sort_keys=True) + "\n")
    manifest = {
        "split_rule": "whole underlying episode stays in one split; train episodes are seed100/102, test episodes seed101/103",
        "state_count": len(states),
        "unique_native_hash_count": len({s["native_hash"] for s in states}),
        "states": [{"state_id": s["state_id"], "episode_id": s["episode_id"], "timestep": s["timestep"], "native_hash": s["native_hash"], "split": "train" if s["episode_id"] in SPLIT_TRAIN_EPISODES else "test"} for s in states],
        "duplicate_state_check": len({s["native_hash"] for s in states}) == len(states),
        "candidate_records_per_state": ALT_COUNT + 1,
        "horizons": list(HORIZONS),
    }
    (OUT / "unique_state_split_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    provenance = {
        "action_generation": {
            "policy": "deterministic state-only approach controller; exact code in tci_identifiability_smoke.py",
            "controller_scale": CONTROLLER_SCALE,
            "alternative_count": ALT_COUNT,
            "theta_radians": THETA,
            "equal_norm_definition": "absolute action norm and distance-to-chosen are fixed by orthogonal rotation; no clipping",
            "candidate_order": "per-state deterministic permutation seeded by 20260928 + state_ordinal*7919",
        },
        "horizons": list(HORIZONS),
        "states": [{"state_id": s["state_id"], "native_hash": s["native_hash"], "episode_id": s["episode_id"], "timestep": s["timestep"], "candidate_order": [c["role"] for c in s["candidates"]], "candidates": s["candidates"], "action_spec": s["action_spec"]} for s in states],
        "records": records,
    }
    (OUT / "intervention_provenance.json").write_text(json.dumps(provenance, indent=2, sort_keys=True), encoding="utf-8")
    results = analyze(records, states)
    (OUT / "tci_identifiability_results.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    (OUT / "raw_consequence_records.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
    leakage = {
        "candidate_order_randomized": True,
        "chosen_position_counts": results["candidate_position_counts_for_chosen_action"],
        "candidate_order_used_as_feature": False,
        "state_id_used_as_feature": False,
        "episode_id_used_as_feature": False,
        "timestep_used_as_feature": False,
        "trajectory_id_used_as_feature": False,
        "raw_action_norm_used_as_temporal_signal": False,
        "duplicate_underlying_states": results["duplicate_underlying_states"],
        "train_test_native_hash_overlap": results["train_test_native_hash_overlap"],
        "policy_action_always_candidate_zero": False,
        "metadata_only_control": "candidate position is randomized; deterministic position baseline is chance-level by construction",
        "raw_mujoco_index_semantics": "none inferred; state capture/restoration uses mujoco.mj_getState/mj_setState with mjSTATE_INTEGRATION",
        "consequence_shuffling": "within-state consequence rows permuted with fixed RNG 20260930",
    }
    (OUT / "leakage_audit.json").write_text(json.dumps(leakage, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"state_count": len(states), "results": results["top1"], "temporal": results["temporal_test"], "inversion": results["inversion"], "out": str(OUT)}, indent=2, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker")
    ap.add_argument("--collect", action="store_true")
    args = ap.parse_args()
    if args.worker:
        worker(args.worker)
    else:
        run_collection()


if __name__ == "__main__":
    main()
