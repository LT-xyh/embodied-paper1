# Track-A P0 Admission — Transition-Surprise Recurrent-State Invalidation

**Status:** CONDITIONAL GO / P0 ONLY  
**Date:** 2026-09-23  
**Parent selection:** `idea-stage/TRACK_A_RAL_METHOD_REPORT.md`  
**Parent commit:** `06f2ee04ea3048e585270c31199458710559f14c`

## P0 scientific question

Does an action-conditioned physical transition residual identify moments when a BC-RNN's carried recurrent state should be **fully invalidated**, such that hard state reset improves post-disturbance closed-loop recovery beyond:

1. no extra reset;
2. the same reset budget placed at unrelated times;
3. a simple non-predictive raw state-change trigger; and
4. soft attenuation of the same recurrent state at the same surprise events?

This is a Track-A incremental-method P0, not a Track-B new-paradigm claim.

## Fresh-prior correction

The selection report must be read together with two very recent 2026 papers:

- **StateMem: Single-State Residual Memory with Adaptive Inference for Vision-Language-Action Policies**, arXiv:2609.22684. It uses prediction error to update persistent memory and to route/refresh stale cached prefixes.
- **PredVLA: A Sub-Million-Parameter Predictive-Coding Policy for Robot Manipulation**, arXiv:2608.26673. It uses sensory prediction error for online recurrent latent correction.

Therefore the following broad claims are **not admissible**:

- "prediction error improves policy memory";
- "surprise should update robot-policy state";
- "stale memory can be corrected from prediction error".

The only admissible Track-A claim is the narrower **hard-invalidation timing** claim:

> For recurrent imitation policies exposed to unexpected physical dynamics events, action-conditioned transition surprise can identify when pre-event recurrent state should be discarded rather than merely retained or attenuated.

Before implementation, perform one final read-only freshness search for direct work matching:
- action/state transition residual;
- recurrent hidden-state hard reset/invalidation;
- robot manipulation / imitation;
- disturbance recovery.

If a direct prior is found, return `PIVOT — DIRECT PRIOR` without implementing.

## Repository and Git boundary

Start from synchronized authoritative `main`.

Create and work only on:

`p0/transition-surprise-reset`

Do not merge to `main`.

Never force-push.

Commit compact code, configs, results, and reports only. Do not commit environments, datasets, checkpoints, caches, or large rollout artifacts.

## Runtime admission

Preferred stack:

- robomimic v0.5.x;
- robosuite v1.5.x;
- MuJoCo;
- low-dimensional state-only BC-RNN;
- Lift and Can proficient-human demonstrations.

The earlier compatibility environment used older packages and emitted a NumPy ABI warning. Do not treat that environment as a clean scientific runtime.

A fresh isolated environment is allowed.

### Runtime kill

Stop with `PIVOT — RUNTIME` if:

- a clean state-only reset/step/train/evaluate path cannot be established within roughly 45 minutes of active repair;
- two unrelated bootstrap/runtime blockers appear;
- scientific execution requires renderer work, simulator internals surgery, NVIDIA-specific kernels, or unsupported custom extensions.

Infrastructure failure is not scientific evidence.

## Data and compute boundary

Allowed:

- public low-dimensional robomimic Lift and Can demonstrations;
- CPU-only training/evaluation;
- standard PyTorch;
- up to 8 CPU cores;
- up to 36 hours total wall-clock for the complete P0;
- under 5 GB new data/artifacts;
- no video.

Do not use GPU/DCU unless CPU training is unexpectedly prohibitive and the standard PyTorch DCU path works without code changes. If DCU use becomes necessary, record it explicitly; do not optimize kernels.

## Trigger definition

For transition ((s_t,a_t,s_{t+1})):

1. fit a small one-step predictor (hat{s}_{t+1}=f(s_t,a_t)) using only the training split;
2. predict only stable low-dimensional physical channels needed for the test, including object and end-effector state; document exact channels;
3. compute a channel-normalized residual after observing (s_{t+1});
4. if the frozen residual score exceeds threshold (	au), reset the BC-RNN hidden and cell state **before** computing (a_{t+1}).

The policy weights and BC-RNN training objective remain unchanged.

### Threshold calibration

Do not tune (	au) on disturbed-test success.

Calibrate from a disjoint clean nominal calibration set.

Prefer an episode-level false-alarm calibration: choose (	au) so that no more than roughly 5% of clean calibration episodes contain any surprise reset.

Freeze the predictor, normalization, and threshold before disturbed test rollouts.

## Controlled disturbance

Use one reproducible exogenous physical event after grasp and during transport.

Preferred implementation:

- a brief MuJoCo external force/impulse on the manipulated object;
- randomized sign and eligible transport step from a fixed seed schedule;
- target approximately 3 cm lateral displacement within one control interval or another pre-registered magnitude that produces a visible but recoverable state transition.

Do not choose perturbation magnitude separately for each inference arm.

Do not directly teleport objects unless the standard external-force path proves unavailable and the alternative is explicitly documented before results are inspected.

Use identical environment seeds and exogenous disturbance schedules across inference arms.

## Mandatory inference arms

### A0 — Native
Unmodified BC-RNN plus its normal native recurrent reset schedule.

### A1 — Transition-surprise hard reset
The proposed method.

At a trigger, clear the recurrent hidden and cell state before the next action.

### A2 — Count-matched random hard reset
For each paired environment seed, use the number of additional resets observed in A1 but place them at residual-independent eligible times.

This tests whether reset frequency alone explains the gain.

### A3 — Raw state-change trigger
Use a simple non-predictive physical-change score, e.g. normalized (|s_{t+1}-s_t|) over the same physical channels.

Calibrate its threshold on clean calibration rollouts to a comparable nominal false-reset rate.

This tests whether the learned action-conditioned transition model contributes information beyond observing a large state change.

### A4 — Surprise-triggered soft decay
Use the same A1 trigger times, but attenuate recurrent state instead of clearing it:

`h <- alpha * h`
`c <- alpha * c`

Use one pre-registered alpha, default `0.25`, fixed before test results.

This is mandatory because recent StateMem/PredVLA work makes generic prediction-error-driven memory correction insufficient novelty. The P0 must test whether **hard invalidation** itself matters.

### Diagnostic A5 — Oracle event reset
On disturbed episodes only, optionally reset immediately after the known injected event.

This is an upper-bound diagnostic and is not part of the publishable method.

## Native-reset consistency

The standard BC-RNN native horizon reset schedule must remain identical across all arms.

Additional P0 resets are layered on top of that schedule only.

Document the exact robomimic native reset semantics from source before running experiments.

## Phase P0-A — one-seed mechanism screen

Run one trained policy seed per task first.

Tasks:

- Lift;
- Can.

For each task, run A0-A4 on:

- nominal episodes;
- disturbed episodes.

Use at least 20 paired rollout seeds per condition and arm.

Run A5 on disturbed episodes if inexpensive.

### P0-A continue rule

Continue to P0-B only if all are true:

- A1 disturbed success is directionally better than A0 on both tasks;
- A1 is directionally better than A2 on both tasks;
- nominal A1 success does not collapse;
- event recall and false-reset behavior are plausible;
- A3 does not make the learned transition model obviously unnecessary;
- A4 does not make hard invalidation obviously unnecessary.

If this screen fails clearly, stop with `PIVOT`.

Do not rescue the method by retuning thresholds on test outcomes.

## Phase P0-B — three-seed confirmation

Only if P0-A passes.

Train/evaluate three policy seeds per task.

Use at least 30 paired rollout seeds per:

- task;
- policy seed;
- inference arm;
- nominal/disturbed condition.

Required primary metric:

- closed-loop task success.

Required secondary diagnostics:

- episode return;
- recovery steps after disturbance;
- object drops;
- contact/task failure modes;
- trigger latency relative to disturbance;
- per-episode additional reset count;
- nominal false-reset episode rate;
- transition-residual distributions.

Action MSE may be reported only as a diagnostic.

## Final positive criterion

Return `P0 POSITIVE — TRACK-A CANDIDATE` only if all of the following hold:

1. **Native comparison**
   - Under disturbance, A1 improves absolute success over A0 by at least **10 percentage points on both Lift and Can**.

2. **Reset-timing comparison**
   - A1 improves over A2 by at least **5 points on both tasks**.
   - Effect direction versus A0 and A2 is positive across all three policy seeds on both tasks.

3. **Prediction-residual value**
   - A1 is not worse than A3 on either task and shows a meaningful advantage on at least one task.
   - If raw state change performs equivalently everywhere, return `PIVOT`: the learned predictor is not justified.

4. **Hard-invalidation value**
   - A1 is not worse than A4 on either task and shows a meaningful advantage on at least one task.
   - If soft decay performs equivalently everywhere, return `PIVOT` for the current novelty claim: the result reduces to generic prediction-error memory correction.

5. **Nominal safety**
   - nominal success drop versus A0 is no more than **5 points per task**.

6. **Trigger quality**
   - at least **80%** of injected events trigger within two control steps;
   - no more than **5%** of nominal test episodes receive any additional surprise reset.

7. **Mechanistic coherence**
   - event-local recovery diagnostics support the claimed stale-memory mechanism rather than only a global success shift.

No single p-value is sufficient.

## Hard kill conditions

Return `PIVOT` if any occur:

- direct prior found during freshness search;
- runtime gate fails;
- disturbance cannot be reproduced cleanly;
- either task lacks closed-loop benefit;
- random matched resets explain the gain;
- raw state-change trigger explains the gain;
- soft decay explains the gain;
- only action MSE improves;
- results depend on one seed;
- nominal false resets/regression exceed bounds;
- gains require post-hoc threshold or disturbance tuning;
- scientific interpretation becomes generic memory gating / prediction-error correction already covered by recent work.

## Required outputs

Create:

- `p0-transition-surprise/README.md`
- `p0-transition-surprise/environment_audit.md`
- `p0-transition-surprise/prior_freshness.md`
- `p0-transition-surprise/analysis.py`
- `p0-transition-surprise/results.json`
- `p0-transition-surprise/results.md`
- `idea-stage/TRACK_A_RAL_P0_RESULT.md`

Add minimal implementation/config files as needed under `p0-transition-surprise/` or a clearly isolated source location.

Update `MANIFEST.md`.

Do not commit downloaded demonstrations, trained checkpoints, environments, raw rollout dumps, or large figures.

## Final verdict

Return exactly one:

- `PIVOT — DIRECT PRIOR`
- `PIVOT — RUNTIME`
- `PIVOT`
- `P0 POSITIVE — TRACK-A CANDIDATE`

Even `P0 POSITIVE — TRACK-A CANDIDATE` does not authorize the full RA-L experiment suite. It authorizes an independent scientific review and a later expansion decision.

## Final report fields

At completion report:

1. exact verdict;
2. final prior-freshness result, explicitly discussing StateMem, PredVLA, GMP, AURA-Mem, MILES, and ResTacVLA;
3. exact runtime versions;
4. exact data downloaded and byte count;
5. exact trained policy seeds;
6. P0-A result;
7. P0-B result if entered;
8. A0-A4 success results by task/seed/condition;
9. trigger recall and nominal false-reset rate;
10. recovery diagnostics;
11. CPU/DCU hours used;
12. files changed;
13. branch name;
14. full commit SHA;
15. confirmation remote candidate branch equals that SHA.

Stop after the verdict.
