# Baseline-First / Method-First Research Search

**Status:** ACTIVE STRATEGY RESET AUTHORITY  
**Date:** 2026-09-21  
**Binding context:** `RESEARCH_BRIEF.md`

## Why this strategy exists

Two rounds of substrate-first search plus bounded Armnet experiments failed to produce a Paper-1 candidate. The repeated failure mode was:

- a real public artifact exists;
- a small statistical effect is measurable;
- but the strongest claim is benchmark QA, data curation, or a mechanism already covered by 2025-2026 work.

Do not run a third version of that process.

The next route starts from a **mature executable policy-learning stack** and searches for a **small method-level contribution** that can change actual policy learning/evaluation behavior.

The target remains:
- CCF B or above, or CAS Zone 3 or above;
- ideally complete experiments + draft in 1-2 months;
- 2-3 months acceptable;
- no >6 month core-hypothesis path.

## Core strategy

Use this order:

```text
mature baseline/runtime
-> execution admission
-> direct 2025-2026 method-gap audit
-> small method hypothesis
-> minimal training/control pilot
-> shortlist
```

A candidate must be a plausible **method or mechanistic learning contribution**, not another dataset observation.

## Phase 1 — Baseline/runtime admission

Search for 3-5 mature robot-learning stacks that could support fast policy-learning experiments.

Examples to inspect, not assumptions:
- RoboMimic / robosuite / MuJoCo-style manipulation stacks;
- Meta-World-style manipulation;
- Minari / D4RL-style offline robot-control datasets;
- lightweight LeRobot policy training paths;
- other mature Gymnasium/MuJoCo robot-learning environments;
- state-based manipulation baselines with optional later visual extension.

For every stack verify from primary documentation/repository:

1. exact repository and maintained revision/tag if available;
2. supported Python version;
3. simulator/runtime dependency;
4. whether the simulator can run CPU-only;
5. whether policy training uses standard PyTorch only;
6. whether NVIDIA CUDA, FlashAttention, Triton, Isaac, or custom CUDA is required;
7. whether headless rendering is optional for a state-based pilot;
8. dataset/checkpoint sizes;
9. smallest benchmark/task that can produce a meaningful policy-learning result;
10. install/runtime complexity;
11. estimated first smoke-test complexity;
12. estimated 1-3 day pilot compute on CPU or Hygon DCU.

### Baseline hard reject

Reject a stack if the first scientific pilot requires:
- NVIDIA-only runtime;
- FlashAttention/Triton/custom CUDA;
- Isaac Sim / Isaac Lab as a mandatory dependency;
- complex renderer/bootstrap reconstruction;
- >100 GB prerequisite download;
- a large VLA checkpoint;
- real robot access;
- substantial simulator surgery.

### Simulator policy

A simulator is now allowed only when all are true:
- mature and actively used;
- self-contained installation path;
- state-based reset/step/evaluate path exists without vision rendering;
- no NVIDIA-specific runtime is required;
- no exact-state restoration or provenance reconstruction is needed;
- the scientific pilot can be executed without modifying simulator internals.

This is a deliberate relaxation of the previous no-simulator preference.

## Phase 2 — Method-gap search

Only after at least one baseline stack passes execution admission, search 2025-2026 literature for method gaps that can be tested on it.

The method must change one of:
- policy learning;
- representation learning;
- action prediction;
- credit assignment;
- generalization;
- adaptation;
- data efficiency;
- uncertainty-aware decision making;
- temporal modeling;
- control robustness;

and must have a credible policy-level or control-level evaluation.

Do not force any specific family if direct prior work closes the gap.

### Existing negative families remain banned

Do not repackage:
- mixed-quality demonstration filtering / segment selection;
- generic recovery/retry;
- generic adaptive action chunking;
- generic active-factor evaluation;
- generic VLA safety;
- generic visual/language shortcut diagnosis;
- generic world-model evaluator calibration/ranking;
- common-random-number comparison;
- contact-topology/contact-flow transfer;
- Armnet length leakage / benchmark preprocessing;
- SocNav rater modeling;
- HIL boundary cleanup as dataset QA.

## Phase 3 — Candidate admission

A candidate may enter the shortlist only if all are true:

### Scientific
- precise falsifiable hypothesis;
- direct closest 2025-2026 prior audit;
- method-level delta, not metric/benchmark/data QA;
- at least one experiment that would clearly distinguish it from the closest prior;
- positive and kill criteria defined in advance.

### Execution
- exact admitted baseline stack;
- exact tasks/datasets;
- exact baseline algorithm;
- minimal code changes required;
- no unsupported kernel/runtime;
- 1-3 day falsification pilot;
- expected memory/storage/compute class;
- no real robot dependency for the core claim.

### Evaluation
The minimum pilot must include a policy/control metric, for example:
- rollout success;
- return;
- task completion;
- action prediction plus at least one downstream control metric;
- cross-task or cross-domain policy generalization.

Pure offline classifier AUC or descriptive correlation is not enough.

## Replication requirement

For final Paper-1 candidacy, identify:
- a second task family, robot family, or benchmark that can test the same method without rewriting the method;
- preferably a second independent benchmark stack if feasible.

This second path may be planned rather than executed at selection time, but it must be concrete and technically plausible.

## Scope control

Search broadly but retain at most **2 candidates**.

Returning **1** or **0** is valid.

However, unlike the previous substrate-first search, do not reject a strong method solely because its first pilot uses one mature simulator. Reject it only if the simulator/runtime itself is high risk or the claim has no plausible second evaluation path.

## Required report

Write:

`idea-stage/BASELINE_FIRST_METHOD_REPORT.md`

Required sections:

1. **Executable Baseline Landscape**
2. **Rejected Baselines and Exact Runtime Reason**
3. **Admitted Baseline Stack(s)**
4. **2025-2026 Method-Gap Landscape**
5. **Candidate Methods**
6. **Closest-Prior Rejection**
7. **Static Pilot Design**
8. **Final Shortlist: at most Top-2**
9. **Recommended next P0**, or **NO CANDIDATE**

For every survivor include:
- exact hypothesis;
- method change;
- exact baseline implementation;
- exact benchmark/tasks;
- closest prior;
- why the method is not already covered;
- minimal implementation diff;
- 1-3 day pilot;
- policy/control metric;
- compute/storage estimate;
- Hygon/DCU compatibility;
- runtime risk;
- strongest reviewer objection;
- positive criterion;
- kill criterion;
- second evaluation path;
- likely publication fit;
- longer-term PhD extension.

## Execution boundary for this pass

This is still a selection pass.

Do NOT:
- run paper-scale training;
- launch long GPU/DCU jobs;
- download large datasets/checkpoints;
- modify simulator internals;
- implement candidate methods.

Small static compatibility checks and repository inspection are allowed if they do not require heavy installation.

Update `MANIFEST.md`, commit, push, and stop after the report.
