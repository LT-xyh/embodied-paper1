# Adjacent-Field Method Transfer Search

**Status:** ACTIVE STRATEGY AUTHORITY  
**Date:** 2026-09-22  
**Binding context:** `RESEARCH_BRIEF.md`

## Motivation

Two substrate-first waves and one baseline-first robot-method search produced no Paper-1 candidate.

The useful result of the last pass is that a mature execution substrate is now available in principle:

- robomimic;
- robosuite;
- MuJoCo;
- low-dimensional state/action observations;
- standard PyTorch BC / BC-RNN;
- closed-loop success as a real control metric.

Do not spend another pass searching only inside recent robotics papers for a tiny unused method gap.

Instead, search adjacent ML fields for mechanisms that may transfer to robot imitation/control.

## Search order

Use this order:

```text
adjacent ML mechanism
-> why robot control creates a specific failure mode
-> robot-specific adaptation
-> 2025-2026 robotics novelty audit
-> executable robomimic pilot
-> second benchmark path
```

The contribution must be stronger than "apply method X to robotics".

## Adjacent fields to inspect

Search recent work, primarily 2024-2026, from areas such as:

- sequence modeling;
- offline reinforcement learning;
- supervised learning under distribution shift;
- representation learning;
- continual / online adaptation;
- optimization and regularization;
- uncertainty-aware prediction;
- test-time adaptation;
- causal / invariant learning;
- curriculum and sample scheduling;
- temporal abstraction;
- decision-focused learning;
- model-based learning;
- efficient fine-tuning;
- other ML fields with mechanisms plausibly relevant to robot policies.

Do not force one of these families if the literature closes the gap.

## Source-method requirement

For every considered adjacent method identify:

1. exact source paper;
2. source venue/year;
3. original problem the method solves;
4. core mathematical or algorithmic mechanism;
5. what assumption changes in robot imitation/control;
6. why a direct transplant is insufficient;
7. what robot-specific adaptation is required;
8. what policy-level behavior would falsify the hypothesis.

A candidate that only changes dataset, modality, model size, or benchmark is rejected.

## Robot-specific novelty requirement

A survivor must contain a robotics-specific scientific claim such as:

- interaction dynamics make the source assumption fail;
- closed-loop compounding error changes the source mechanism;
- multi-modal action distributions require a different objective;
- temporal credit / intervention structure changes the learning rule;
- embodiment or task variation creates a structured invariance requirement;
- control stability or rollout feedback creates an objective unavailable in ordinary supervised learning.

These are examples, not mandatory themes.

The claim must remain meaningful even if robomimic is replaced by another benchmark.

## Mandatory dual novelty audit

Every survivor must pass both:

### A. Source-field audit
Show that the proposed adaptation is not already the standard form of the adjacent ML method.

### B. Robotics audit
Search 2025-2026 robot-learning literature for the same mechanism under different terminology.

Reject if the closest robot paper already contains the core mechanism.

Do not revive any family in `RESEARCH_BRIEF.md -> Accumulated Negative Evidence`.

## Execution substrate

Prefer the conditionally admitted stack:

- robomimic v0.5.x;
- robosuite v1.5.x;
- MuJoCo;
- low-dimensional Lift / Can / Square;
- standard PyTorch BC or BC-RNN.

A clean isolated environment may be planned, but this selection pass does not install it.

Alternative primary stacks are allowed only if they are demonstrably lower risk.

## Minimal P0 requirement

Every final candidate must have a 1-3 day falsification pilot.

The pilot must specify:

- exact baseline;
- exact tasks;
- minimal code diff;
- primary policy/control metric;
- expected runtime;
- CPU/DCU path;
- positive criterion;
- kill criterion.

Primary evidence must include closed-loop policy behavior such as success or return.

Action MSE, classifier AUC, or offline correlation alone is insufficient.

## Second evaluation path

Every survivor must identify a concrete second path, preferably:

- Meta-World MT1/ML1;
- another robomimic task family;
- another lightweight MuJoCo benchmark;
- or another independent mature stack.

The method should not require redesign for the second path.

## Publication bar

A final candidate must plausibly support:

- one clear method/mechanism contribution;
- multiple tasks;
- one independent second evaluation path;
- standard ablations;
- no real robot requirement for the core claim;
- a credible CCF-B / CAS-Zone-3 paper within 1-2 months.

Reject a candidate if its likely paper would read as:

- "we applied X to robomimic";
- "we changed one loss and got +Y%";
- "we benchmarked method X on robots";
- "we found another dataset artifact".

## Breadth control

Search broadly but retain at most **2** candidates.

Top-1 or zero is valid.

For each rejected near-miss, record only the decisive collision.

## Required report

Write:

`idea-stage/ADJACENT_FIELD_METHOD_REPORT.md`

Required sections:

1. **Adjacent ML Mechanism Landscape**
2. **Robot-Specific Failure Modes**
3. **Candidate Adaptations**
4. **Source-Field Novelty Audit**
5. **2025-2026 Robotics Novelty Audit**
6. **Static Execution Admission**
7. **Second Evaluation Path**
8. **Final Shortlist: at most Top-2**
9. **Recommended P0**, or **NO CANDIDATE**

For each survivor include:

- source method and paper;
- precise robotics-specific hypothesis;
- robot-specific method adaptation;
- closest robotics prior;
- exact baseline/runtime;
- exact tasks;
- minimal implementation diff;
- 1-3 day pilot;
- policy/control metric;
- compute/storage estimate;
- strongest reviewer objection;
- grow criterion;
- kill criterion;
- second evaluation path;
- publication fit;
- PhD-extension potential.

## Stop rule

Selection only.

Do NOT:

- install runtimes;
- implement methods;
- launch training;
- run simulator experiments;
- download large datasets/checkpoints;
- start another autonomous full pipeline.

Update `MANIFEST.md`, commit, push, and stop after the report.
