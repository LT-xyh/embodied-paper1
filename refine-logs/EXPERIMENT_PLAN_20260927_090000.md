# Conditional Experiment Plan: Action-Swap Consequence Consistency

## Gate 0: prior freshness and runtime

Search PAM, MEMBOT, JEPA Policy, StateMem, PredVLA, MemoryVLA, PHASER, CIVIL, CAGE, ReViWo, and 2025-2026 action-conditioned predictive-policy papers. Stop on an exact paired action-swap/consequence-divergence recurrent-BC prior. Qualify robomimic/robosuite/MuJoCo in an isolated environment before any training.

## P0 (not executed)

- Primary: robomimic Lift, Can, Square, state-only BC-RNN.
- Perturbation: deterministic observation dropout/occlusion and alias splits built from valid adjacent trajectory pairs.
- Conditions: A0 BC-RNN; A1 next-state-prediction auxiliary; A2 action-swap consequence objective; A3 equal-parameter random-pair control; A4 adaptive-memory/PAM-inspired control if public code is available.
- Seeds: 3; fixed normalization and episode seeds.
- Metrics: success/return, alias-split success, nominal success, hidden-state linear probe, false separation/false attraction, wall time.
- Positive: A2 ≥10 percentage-point gain on alias split over A0/A1 and both controls, ≤2-point nominal regression, replicated on all three tasks.
- Kill: no gain, gain disappears under equal parameters/consequence-matched negatives, invalid pair rate >10%, or direct prior collision.
- Budget after authorization: ≤3 days, <5 GB artifacts, CPU-first.

## Independent path

Replicate the same hypothesis on Meta-World reach/push tasks using the mature offline/CPU path. No VLA checkpoint or video is required for the minimum scientific claim.

## Current status

`SKIPPED — RUNTIME NOT QUALIFIED`; no implementation, downloads, or experiments authorized in this discovery run.
