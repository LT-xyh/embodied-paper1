#!/usr/bin/env python3
"""Small, CPU-only boundary-mass preflight for a bounded-action BC question.

This is an admission measurement, not a policy method or scientific rollout. It
generates a few deterministic state-only demonstration traces, records the exact
normalized action handed to the robosuite wrapper, and reports whether the trace
contains enough mass near the action cube boundary to make a support-mismatch
hypothesis testable.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("MUJOCO_GL", "disable")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "p0-tci-identifiability"))
import tci_identifiability_smoke as substrate  # noqa: E402

SEEDS = (310, 311, 312)
STEPS = 20
BOUND = 0.8
EXACT_BOUND = 0.99


def expert_action(obs: dict[str, np.ndarray]) -> np.ndarray:
    # This deliberately probes the existing normalized action domain.  It is
    # not a policy candidate; it only provides legal traces with boundary mass.
    delta = np.asarray(obs["cube_pos"], dtype=np.float64) - np.asarray(obs["robot0_eef_pos"], dtype=np.float64)
    translation = np.clip(20.0 * delta, -1.0, 1.0)
    return np.concatenate([translation, np.zeros(4, dtype=np.float64)])


def main() -> None:
    rows = []
    for seed in SEEDS:
        env = substrate.make_env(seed)
        env.reset()
        for step in range(STEPS):
            obs = substrate.obs_pack(env._get_observations(force_update=True))
            action = expert_action(obs)
            # The row is the exact object passed to env.step, before controller
            # processing; no latent pre-clipped command is assumed.
            rows.append({"seed": seed, "step": step, "action": action.tolist()})
            result = env.step(action)
            if bool(result[2]):
                break
        env.close()
    actions = np.asarray([r["action"] for r in rows], dtype=np.float64)
    result = {
        "format": "bounded-action boundary-mass preflight",
        "runtime": {"python": sys.version, "numpy": np.__version__},
        "seeds": list(SEEDS),
        "steps_requested": STEPS,
        "row_count": int(len(rows)),
        "action_dim": int(actions.shape[1]),
        "min": actions.min(axis=0).tolist(),
        "max": actions.max(axis=0).tolist(),
        "fraction_abs_ge_0.8": np.mean(np.abs(actions) >= BOUND, axis=0).tolist(),
        "fraction_abs_ge_0.99": np.mean(np.abs(actions) >= EXACT_BOUND, axis=0).tolist(),
        "exact_bound_rows": int(np.sum(np.any(np.abs(actions) >= EXACT_BOUND, axis=1))),
        "legal_action_all_rows": bool(np.all(np.abs(actions) <= 1.0 + 1e-12)),
        "provenance": "actions are the exact arrays passed to the real robosuite env.step; no separate latent command is recorded",
        "scientific_use": "measurement only; no policy training, comparison, or rollout claim",
        "rows": rows,
    }
    out = Path(__file__).with_name("boundary_preflight_results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
