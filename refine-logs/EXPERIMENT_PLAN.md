# Conditional Experiment Plan: Action-Swap Consequence Consistency

## Gate 0

Perform a fresh paper-level audit of PAM, MEMBOT, JEPA Policy, CIVIL, StateMem, PredVLA, MemoryVLA, PHASER, CAPE, and action-conditioned predictive-policy work. Stop on an exact paired action-consequence recurrent-BC prior. Qualify robomimic/robosuite/MuJoCo in an isolated environment before training.

## P0 (not executed)

Use a known-latent POMDP or cloned robosuite state. From one identical latent state, execute two valid alternate actions and freshly observe both successors. Do not use cross-trajectory logged swaps as interventions.

Conditions: A0 BC-RNN; A1 next-state auxiliary; A2 action-swap consequence objective; A3 transition-surprise/reset; A4 generic action-conditioned contrastive representation; A5 capacity-matched adaptive-memory/PAM control; A6 shuffled/invalid-swap control. Hold parameter count, data, seeds, and auxiliary-loss budget fixed.

Evaluate held-out alias interventions, fully observed nominal success, hidden-state probes, unseen action swaps, and invalid-pair sensitivity on three seeds. Positive criterion: at least 10 percentage-point alias-split gain over every control, no more than 2-point nominal loss, disappearance under shuffled swaps, and replication on Meta-World or another independent benchmark. Null means generic predictive auxiliary; invalid-pair or leakage-dependent gains kill the claim.

Budget after authorization: ≤3 days, CPU-first, <5 GB artifacts. No VLA checkpoint, video, runtime repair, simulator run, or training was performed here.

## Current status

`SKIPPED — RUNTIME NOT QUALIFIED`. Implementation remains unauthorized until the exact intervention substrate and runtime qualification are separately approved.
