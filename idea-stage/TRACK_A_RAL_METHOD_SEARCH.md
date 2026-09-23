# RA-L-First Track-A Method Search

**Status:** ACTIVE PAPER-1 SEARCH AUTHORITY  
**Date:** 2026-09-23  
**Binding context:** `RESEARCH_BRIEF.md`, `idea-stage/VENUE_FIRST_RECALIBRATION_REPORT.md`

## Objective

Select the fastest credible Paper-1 method direction under the adopted **Track A** contribution bar.

Primary publication target:

- RA-L-first;
- more generally, a verified CAS Zone 3-or-above robotics journal if the final fit is better.

This pass is intentionally less restrictive than the previous conference-style novelty gate.

A candidate does **not** need a completely new learning paradigm.

It may be:

- a technically meaningful incremental method;
- a principled combination of known components;
- a robot-specific formulation of a known learning idea;
- a lightweight adaptation whose interaction with closed-loop control is the scientific contribution.

It must still be more than:

- a direct reproduction;
- a trivial loss swap;
- a hyperparameter trick;
- a pure benchmark/domain substitution;
- dataset QA;
- a one-task empirical note.

## Primary execution substrate

Prefer:

- robomimic v0.5.x;
- robosuite v1.5.x;
- MuJoCo;
- state-only BC / BC-RNN;
- Lift, Can, Square as the initial multi-task family.

Plan, but do not execute in this pass, one independent second evaluation path:

- Meta-World MT1/ML1;
- another lightweight MuJoCo manipulation benchmark;
- or another mature state-based robot-control stack.

A different primary stack is allowed only if clearly lower risk.

## Search style

Do **not** generate a broad idea list.

Start from concrete failure modes of state-based imitation/control such as:

- covariate shift and compounding error;
- partial observability/history misuse;
- multi-modal demonstrations;
- state-dependent action ambiguity;
- task-phase imbalance;
- demonstration-to-rollout mismatch;
- robustness to controlled dynamics/state perturbation;
- overfitting to nominal initial-state distributions;
- policy confidence versus actual control failure;
- coordination between representation and action objective;
- other closed-loop failure modes supported by literature.

These are prompts, not required themes.

Generate at most **3 serious hypotheses**.

## Track-A novelty rule

For each hypothesis identify:

1. exact problem;
2. exact method delta;
3. closest 2025-2026 robotics prior;
4. what the prior already does;
5. what remains genuinely different;
6. why that difference should affect closed-loop behavior.

### Direct-collision rule

Reject when prior work already contains the same core formulation and claimed effect.

Known direct-collision families remain excluded, including:

- GPC-equivalent policy composition;
- Q-Planning-equivalent frozen-BC/Q selection;
- ISR-equivalent trajectory resampling;
- SDP-equivalent correction loss;
- MTIL/Mamba Policy-equivalent selective-SSM policy design;
- conformal robot-safety / ConformalDAgger-equivalent uncertainty control;
- distributionally robust offline imitation learning with the same robustness mechanism;
- every family listed under `Accumulated Negative Evidence`.

### Important relaxation

Do **not** reject merely because:

- every individual component has appeared separately;
- the method is an incremental extension rather than a new paradigm;
- the first pilot is state-only;
- the method would likely be below a top-conference novelty bar.

A **principled combination** is admissible when:

- the interaction between components solves a concrete robot-control failure mode;
- the combination is not already established by direct prior;
- ablations can isolate why the combination matters;
- the effect is measured in closed-loop control.

## Candidate structure

Every candidate must specify:

### Scientific hypothesis
A falsifiable statement about closed-loop behavior.

### Method
A concrete implementation change small enough for a 1-3 day P0.

### Closest prior
At least the strongest 2025-2026 robotics paper and any important adjacent-method source.

### Distinction
One concise sentence stating the non-overlapping contribution.

### Primary P0
Prefer robomimic Lift + Can initially.

Include:

- baseline;
- exact method variant;
- 2-3 seeds if feasible;
- fixed rollout count;
- primary success metric;
- secondary return/failure diagnostics;
- one targeted shift/generalization condition.

### Positive criterion
Use a pre-registered rule that would justify expansion.

Default target unless the candidate needs another justified threshold:

- meaningful success improvement on **both** initial tasks, not one;
- no material nominal regression;
- effect direction consistent across seeds;
- targeted generalization/shift result supports the proposed mechanism.

A single lucky seed is not enough.

### Kill criterion
Kill if:

- no closed-loop gain;
- gain only in action MSE;
- gain only on one task with no mechanistic explanation;
- gain disappears under matched compute/parameter control;
- implementation complexity exceeds the claimed incremental contribution;
- direct prior collision is discovered.

## Track-A expansion package

For a candidate that passes P0, the planned paper package must be plausible within 1-2 months:

- at least 3 robomimic task families or equivalent;
- multiple seeds;
- strong unmodified baseline(s);
- component ablations;
- compute/parameter-matched control;
- one controlled generalization or robustness test;
- one second evaluation path;
- reproducible configs/code;
- closed-loop success/return as the main result.

Real robot is desirable but **not mandatory for the core admission decision**. Do not invent a hardware plan the user does not have.

## Candidate scoring

Do not use an artificial numeric leaderboard.

For each candidate provide qualitative judgments on:

- scientific clarity;
- novelty safety for Track A;
- P0 speed;
- runtime risk;
- expected experiment burden;
- reviewer vulnerability;
- extension potential.

Then select at most **one recommended P0**.

You may retain up to 3 hypotheses in the report, but only one may be recommended for immediate P0.

If none has a credible RA-L-level incremental contribution, return `NO CANDIDATE`.

## Required report

Write:

`idea-stage/TRACK_A_RAL_METHOD_REPORT.md`

Required sections:

1. **Track-A Search Boundary**
2. **Three-or-Fewer Candidate Hypotheses**
3. **Direct-Prior Audit**
4. **Closed-Loop Mechanism Argument**
5. **Static Execution Admission**
6. **1-3 Day P0 Designs**
7. **Planned Full Track-A Experiment Package**
8. **Recommended P0**
9. **Why This Meets Track A But Not Necessarily Track B**

For the recommended P0 state exactly:

- hypothesis;
- method delta;
- closest prior;
- non-overlapping claim;
- primary baseline/tasks;
- implementation scope;
- seed/rollout plan;
- success criterion;
- kill criterion;
- second benchmark path;
- expected CPU/DCU/storage budget;
- strongest likely RA-L reviewer objection.

## Stop rule

This is a selection pass only.

Do NOT:

- install a new runtime;
- train policies;
- run scientific rollouts;
- implement method code;
- download datasets/checkpoints;
- invoke `/research-pipeline`;
- automatically start the recommended P0.

Update `MANIFEST.md`, commit, push, and stop after the report.
