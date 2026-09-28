# Experiment Plan — Temporal Consequence Inversion (TCI)

## Execution status
NOT EXECUTED — discovery only. Do not install runtimes, download data/checkpoints, train policies, or launch simulator rollouts from this plan.

## Gate 0: preflight authorization and state selection
Use only the already-qualified native MuJoCo intervention and robosuite wrapper-closure substrate. Before a scientific pilot, freeze the state-selection rule and future failure target using an episode/time split. Do not select states because they later fail. Verify the policy emits a deterministic action and use that action as the observed treatment; do not query candidate likelihood or preference.

## Gate 1: six-state preflight (future authorization required)
For Lift and Can, audit three early/contact/branching states per task. Restore each state twice in fresh subprocesses, execute the same action, and verify simulator state, observation, reward, done, and task fields. Generate four norm-matched valid alternatives before looking at outcomes. Record action commands, all horizons, task-progress components, wrapper/RNG hashes, and branch provenance. Kill immediately on replay drift, invalid alternatives, or missing future-target separation.

## Main pilot (only after Gate 1 and final review)
Use state-only robomimic `BC_RNN`, two tasks (Lift and Can), three frozen policy seeds when available, and 30–50 held-out states per task. At every state execute `a_hat` and 4–8 predeclared valid alternatives from independent fresh subprocesses with common random seeds. Use short horizons 1 and 2 and long horizons 8 and 16 control steps. The first horizon pair is primary; the second is a preregistered sensitivity check.

## Metrics
Primary: temporal inversion prevalence and failure-onset lead time. Secondary: finite-set long-horizon deficit of `a_hat` relative to the tested alternatives, one-step and long-horizon `G_H`, contact/stage validity, selected-action boundary margin, and task-stratified bootstrap intervals. Treat finite-set deficit as a lower bound over sampled alternatives.

## Controls and analyses
Fit a held-out failure model with TCI indicators plus one control family at a time: one-step progress; action norm; nearest-demonstration distance; contact/stage labels; random alternative rank; and an offline next-state predictor if available. Cluster uncertainty by episode and policy seed. Include the rejected LCBG basin descriptors only as controls. Report no policy preference, likelihood, confidence, or global regret.

## Decision rule
Proceed only if the same-sign pre-failure effect replicates on Lift and Can, the held-out AUC exceeds the strongest non-interventional control by at least 0.10, and the effect is stable over the preregistered horizon/margin sensitivity. A null result (no incremental held-out signal) abandons the direction. A negative result (drift, leakage, invalid alternatives, one-task-only effect, or control explanation) is a hard kill. Do not retune, rename, or start another candidate in the same run.

## Resources and risks
CPU-first, max four cores, 1–3 days for the pilot, and <5 GB new artifacts. No video, GPU/DCU, large checkpoint, VLA inference, or simulator-internal modification. The principal scientific risks are finite-horizon credit overlap with PACE, progress-functional arbitrariness, alternative-set lower-bound bias, and selection leakage; all are addressed by frozen definitions, held-out future targets, matched alternatives, common seeds, and explicit negative interpretation.
