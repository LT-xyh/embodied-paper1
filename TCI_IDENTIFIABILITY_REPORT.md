# TCI consequence identifiability preflight

**Verdict: `REVISE — TCI CONSEQUENCE IDENTIFIABILITY`**

## Scope and frozen hypothesis

This gate tests only whether the proposed TCI measurement can be queried from cloned states and whether equal-norm actions generate a reproducible temporal consequence signal. It does not test TCI training or policy improvement. The exact TCI quantity is the real simulator consequence difference `D_H = G_H(a_hat)-G_H(a_i)` after restoring the same wrapper state, with H in {1,4,12}; no likelihood, preference, confidence, or policy score is used.

The executable policy action in this preflight is a frozen deterministic state-only scripted approach controller. It is explicitly a measurement stub, not a BC-RNN checkpoint. This limitation is material: the gate establishes the intervention substrate and measurement protocol, but not identifiability for the intended trained recurrent policy family.

## Frozen variables and action construction

The environment is robosuite 1.5.2 Lift/Panda/BASIC with state-only observations and MuJoCo 3.3.0. Each state is canonicalized with `sim.forward()` and forced observable refresh before capture. Restoration uses `mujoco.mj_getState`/`mj_setState` with `mjSTATE_INTEGRATION`, explicit simulator control/force/warm-start buffers, wrapper counters and metadata, RNG state, and observable/controller numeric state. Every branch is restored and evaluated in a fresh subprocess.

The chosen action is `clip(4*(cube_pos-eef_pos), -0.35, 0.35)` in translation, zero rotation, and neutral gripper. Four alternatives are fixed-angle orthogonal rotations (`theta=0.25`) of the translation vector. Their absolute norm and distance to the chosen action are fixed by construction; all alternatives pass action-bound checks without post-rotation clipping. Candidate order is independently permuted with seed `20260928 + state_ordinal*7919`.

## Data and independence

There are 40 unique captured states (four seeds, two episodes per seed, timesteps 0/3/6/9/12). Whole episodes are assigned to splits: seeds 100/102 train (20 states), seeds 101/103 test (20 states). Native-state SHA-256 overlap is zero, duplicate underlying states are absent, and each state has five candidates and three horizons. Chosen-action positions are 6, 8, 8, 8, and 10, so the chosen action is not encoded by a fixed candidate position.

## Reproducibility and leakage evidence

The fresh-process same-action null control has maximum consequence error `0.0` and maximum restored-observation error `0.0` at tolerance `1e-10`. Alternate actions are executed by real simulator stepping from independently restored states. The leakage audit finds no use of state/episode/timestep identifiers, candidate position, trajectory id, or raw action norm as a signal. The exact serialized snapshots, intervention branches, split manifest, and fixed-RNG consequence-shuffle control are preserved beside this report.

## Consequence results

The test split has five-way chance top-1 `0.20`. The chosen action is top-1 under the immediate H=1 consequence in 5/20 states (`0.25`) and under the H=12 multi-horizon consequence in 5/20 states (`0.25`). The paired difference is `0.00` (bootstrap CI `[0.00, 0.00]` in the machine-readable result), so the longer horizon does not improve over the immediate signal. The shuffled-consequence control is `0.30`, within the declared near-chance tolerance. Train scores are 0/20 immediate and 1/20 multi-horizon. The required sign inversion event (`D_1` versus `D_12`, margin 0.005) occurs in 0/40 states, including 0/20 held-out states.

These results show technically reproducible consequences and no obvious leakage, but they do not show the frozen TCI temporal inversion or a cross-state temporal advantage. Because the controller is also a scripted stub rather than the intended BC-RNN, the evidence cannot distinguish a failure of the TCI hypothesis from a failure of this measurement policy. Under the gate contract this is a concrete revision requirement, not authorization to tune the method or rename the signal.

## Required revision before a scientific pilot

A future rerun must use the actual intended deterministic BC-RNN policy artifact, freeze its recurrent state, and repeat the same cloned-state protocol without changing the action construction, horizons, split rule, or controls. It must pre-register whether temporal consequence ranking improves over H=1 and whether inversion is present on held-out states. No TCI training, BC-RNN modification, full imitation evaluation, image observation, or LIBERO run was performed here.

## Resource and provenance record

Runtime: Python 3.10.21 in `/tmp/aris_p0_env`, NumPy 2.2.6, MuJoCo 3.3.0, robosuite 1.5.2, Torch CPU 2.5.1 available but unused. New downloads: 0 bytes. GPU/DCU: not used. Video: not used. A simulator was used only for this bounded preflight. The old pre-canonicalization artifacts are superseded by the current run and are not used for the verdict.

Independent final Astra audit is required before this verdict can be finalized; its receipt will be appended after review.

## Independent final audit

A fresh independent read-only audit was completed by `gpt-6-astra`, reasoning `medium`, thread `/root/tci_final_audit`, recorded in `p0-tci-identifiability/INDEPENDENT_ASTRA_AUDIT.md`. The reviewer independently checked all 200 branch records: maximum full-vector norm and chosen-distance mismatch were approximately `1.11e-16`; replay null errors were zero; state hashes, split separation, and leakage controls were clean. The reviewer confirmed the held-out H=1 and H=12 top-1 rates were both 0.25, inversion was 0/40, and the shuffled control was 0.30 near chance. The reviewer therefore finalized **`REVISE — TCI CONSEQUENCE IDENTIFIABILITY`**: the stub/BC-RNN mismatch prevents PASS, while FAIL would overinterpret the null result. A successor gate must use the actual deterministic BC-RNN, frozen recurrent state, episode-clustered uncertainty, and a preregistered horizon set.
