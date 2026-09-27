# Intervention Substrate Feasibility Report

## Final verdict

**PASS — INTERVENTION SUBSTRATE**

This PASS is scoped to the minimal native MuJoCo substrate implemented in `intervention_substrate_smoke.py`. It demonstrates the required causal intervention primitive: capture one serialized latent simulator state, restore it in independent fresh processes, execute the same action twice for a null control, and execute two alternate valid actions from the same restored state while measuring both successors.

## Evidence

The machine-readable result is `intervention_substrate_results.json`.

- Capture spec: `mjSTATE_INTEGRATION`, state vector length 18.
- Fresh processes: one capture process plus four independent restore/step processes.
- Same pre-state hash across all restores: `true`.
- Restore maximum absolute error: `0.0`.
- Same-action null control: maximum successor simulator-state error `0.0`; maximum observation error `0.0`; tolerance `1e-12`.
- Alternate actions: factual `+0.35`, alternate `-0.40`.
- Alternate successor maximum state delta: `25.826706454505562`.
- Alternate successor maximum observation delta: `0.05192396585795456`.
- Both alternate actions are executed by MuJoCo from the restored state; no unrelated trajectory action is copied.

## State closure and leakage

The test captures the native MuJoCo integration state, including time, qpos, qvel, actuator state, warmstart, controls, applied forces, equality activation, mocap, userdata, and plugin state. The minimal model has no task wrapper, controller integrator, stochastic RNG, mocap target, userdata, or plugin state; those dimensions are explicitly recorded as absent rather than assumed away.

Intervention labels are derived from the executed action and measured successor. There is no trajectory ID, episode ID, phase label, or cross-trajectory pairing. The timestep is fixed and identical across restores. Thus the minimal test has no metadata route by which the alternate label can be inferred.

## Limitations before a scientific pilot

This PASS does not qualify robosuite/robomimic or any real task wrapper. Before a pilot, the same closure test must be repeated on the selected task and include controller/actuator/mocap state, task randomization and RNG, wrapper state, and any hidden environment state. The candidate remains conditional on constructing exact same-latent-state alternate actions in that qualified task substrate. Logged cross-trajectory action swapping remains invalid.

No method implementation, BC-RNN training, simulator benchmark rollout, P0-A, or P0-B was performed.

## Independent final audit

A fresh independent audit was completed by `gpt-6-astra` with `medium` reasoning (reviewer task/thread `/root/substrate_gate_reviewer`; trace `.aris/traces/intervention-substrate-gate/2026-09-27_run01/001-final-gate-audit`). The reviewer reran the designated environment and returned **PASS — INTERVENTION SUBSTRATE**. The audit independently confirmed exact integration-state restoration, zero null-control divergence at `1e-12`, action-dependent successors, and the stated minimal-native-MuJoCo scope limitations.
