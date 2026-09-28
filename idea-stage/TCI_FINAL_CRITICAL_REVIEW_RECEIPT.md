# TCI Final Critical-Review Receipt — 2026-09-28

## Reviewer identity and route

- Actual thread identity: `/root/third_direction_critical_review`
- Requested reviewer route: `gpt-6-astra / medium`
- Review independence: `same-family`
- Acceptance status: `provisional`
- Scope: final critical review of the narrowed **Temporal Consequence Inversion (TCI)** survivor in `idea-stage/IDEA_REPORT.md`.
- LCBG was not reconsidered as a survivor; it remains rejected.
- No implementation, installation, download, training, simulator rollout, or pilot was performed.

## Exact verdict

**TCI — PROCEED WITH CAUTION.**

TCI is a scientifically identifiable intervention diagnostic, but it is not yet established as a substantive mechanism. In its current form, a sign reversal between short- and long-horizon task-progress differences can still be read as a finite-horizon credit/robustness metric. It should survive only to a tightly bounded, runtime-qualified pilot with predeclared controls and an explicit mechanism-versus-metric decision gate.

## What is identifiable

At a verified cloned wrapper state `s_t`, the selected deterministic action `a_hat` is an observed behavior. For executable alternatives `a_i`, real branch rollouts define `G_H(s_t,a)` and `D_H(i)=G_H(s_t,a_hat)-G_H(s_t,a_i)`. A TCI event is a preregistered, margin-qualified sign reversal between `H_short` and `H_long`.

This object does **not** require, and must not imply, a policy likelihood, candidate-action preference, confidence, or utility. The paper must say that `a_hat` was selected by the frozen policy and that alternatives are measurement controls. It must not say that the policy preferred `a_hat` over `a_i`, nor infer a counterfactual policy score from action distance.

The current finite alternative set supports only a **sampled lower bound** on regret: report the loss relative to the best tested valid alternative, conditional on the tested set and feasibility filter. Do not call it global regret, optimal regret, causal regret over the action space, or a policy preference.

## Main scientific concern

The strongest reviewer objection is that TCI merely renames finite-horizon advantage disagreement: hand-designed progress functionals, horizons, margins, and action neighborhoods can manufacture reversals, while PACE and related credit/replanning work already studies short-versus-long temporal value. A result that correlates with failure but adds no held-out information beyond one-step progress, contact state, action norm, and demonstration distance is a new metric or benchmark, not a mechanism.

To earn a mechanism claim, TCI must show that a **pre-outcome, same-state, real-transition temporal ordering reversal** predicts later failure across at least Lift and Can, survives fixed horizon/margin sensitivity checks, and adds held-out predictive information over non-interventional controls. If those conditions fail, downgrade the contribution to descriptive evaluation and abandon it as a Paper-1 direction.

## Leakage and protocol requirements

1. Select states and episode splits before observing branch outcomes or future failure labels. Do not enrich the sample with “impending failures” after rollout. Use all pre-indexed held-out states or a label-independent contact/phase stratum; use future failure only as an evaluation label.
2. Restore complete simulator, wrapper, controller, task-randomization, and RNG state in fresh processes. Verify same-state null replay at the declared tolerance before collecting alternatives.
3. Execute `a_hat` and 4–8 valid alternatives from the exact same state, using common random seeds per branch. Match action norm/radius and report the validity/feasibility attrition rather than silently dropping difficult alternatives.
4. Freeze `G_H`, `H_short`, `H_long`, margins, control rate, and action-domain conventions before reading outcomes. Repeat at least two fixed horizon pairs; do not tune the pair to maximize AUC.
5. Keep episode-level train/validation/test separation. Fit no threshold, alternative set, or progress normalization on test outcomes.

## Closest-prior boundaries

- **PACE:** learned phase-progress credit and policy distillation. TCI must remain a frozen-policy, real-branch diagnostic; it cannot claim a new critic, credit learner, or generic long-horizon value method.
- **PACT/MILE:** counterfactual intervention/advantage signals used for correction or intervention learning. TCI has no human intervention target and no learned correction policy; generic counterfactual advantage language is disallowed.
- **RoboMD and RoboART:** vulnerability search/prediction under semantic/environment or perturbation variations. TCI must isolate balanced executable action branches at one physical state and demonstrate temporal ordering information beyond vulnerability or distance scores.
- **CMA:** matched-history audits at verified-identical present states. TCI must not become another history-sensitivity or warranted-choice audit; the contribution is the temporal sign reversal of real successor outcomes with the selected action held fixed.
- **Reflective VLA:** consequence-conditioned policy learning. TCI must not add consequence memory, prediction loss, or adaptive policy machinery.
- **Regret-guided replanning / When Should a Robot Replan?:** scheduling replans under drift. TCI must not claim a replanning rule; it measures a pre-failure diagnostic before any intervention.
- **One-step progress, action-distance, contact, and nearest-demonstration controls:** these are mandatory baselines. A reversal that is explained by any of them is not a TCI mechanism.

## Minimum 1–3 day pilot

Use the existing state-only robomimic/robosuite/MuJoCo path only after task-specific closure qualification. On held-out Lift and Can states, pre-index 30–50 states per task (or all states in a fixed small split if fewer), spanning success and failure trajectories without using future labels for selection. For each state, run the selected action plus 4–8 equal-radius, valid alternatives in fresh processes with common seeds. Evaluate at two fixed short/long horizon pairs, for example `(1,8)` and `(2,16)`, with a task-scale margin frozen in advance.

Report paired inversion prevalence, sampled-best-alternative lower-bound loss, earliest inversion-to-failure lead time, and held-out failure AUC. Compare against one-step progress, action norm/distance, contact indicators, nearest-demonstration distance, random alternative rank, and a simple next-state/action-conditioned predictor if already available. Use bootstrap intervals clustered by episode and require replication in both tasks. No training or full suite is justified at this stage.

## Decision criteria

- **Positive / survive to expansion:** inversion prevalence and lead time replicate on Lift and Can; the predeclared event adds at least 0.10 held-out failure AUC (or a similarly predeclared incremental metric) over the strongest non-interventional control; effect remains directionally stable across both horizon pairs and margin checks; same-state null replay and alternative validity pass.
- **Null / downgrade and stop:** inversions are observable but add no held-out information over one-step progress, contact, action distance, or nearest-demonstration controls. This supports only a descriptive finite-horizon metric; do not develop it as Paper-1.
- **Negative / abandon:** no replication across tasks, strong horizon/margin dependence, selection leakage, failed state closure, invalid/norm-unmatched alternatives, or gains that disappear under shuffled/random alternatives. Do not tune, rename, or rescue with a learned score, consequence loss, memory module, or replanning policy.

## Final recommendation

TCI may proceed to exactly one runtime-qualified, bounded pilot under the gates above. It is not implementation-authorized by this receipt alone. LCBG remains **ABANDON** as a standalone direction and may appear only as a preregistered control. The pilot must decide whether TCI is a causal temporal mechanism or merely finite-horizon/robustness accounting; absent incremental cross-task evidence, terminate the direction.
