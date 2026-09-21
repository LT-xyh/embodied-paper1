# Overnight Autonomous Research Contract

**Status:** ACTIVE OVERNIGHT AUTONOMY POLICY  
**Date:** 2026-09-21  
**Applies to:** ARIS `/research-pipeline` runs in this repository  
**Binding context:** `RESEARCH_BRIEF.md` and `idea-stage/BASELINE_FIRST_METHOD_SEARCH.md`

## Goal

Use one unattended overnight ARIS run to move from the current baseline-first strategy to the strongest bounded scientific evidence that can be obtained safely by morning.

The run may autonomously:

1. identify mature executable robot-learning baselines;
2. select at most one primary method candidate;
3. implement a minimal falsification pilot;
4. run bounded experiments;
5. perform adversarial review and bounded fixes;
6. produce a research handoff report.

The run must **not** autonomously turn a weak result into a paper direction.

## ARIS mode

Use:

- `AUTO_PROCEED=true`
- `HUMAN_CHECKPOINT=false`
- `AUTO_WRITE=false`
- `CODE_REVIEW=true`
- `COMPACT=true`
- `REVIEWER_DIFFICULTY=hard`
- `ARXIV_DOWNLOAD=false`
- resumable run-state / watchdog behavior when available.

`AUTO_PROCEED=true` does not override the scientific gates below.

## Stage 1 — baseline-first selection gate

The idea stage must follow `idea-stage/BASELINE_FIRST_METHOD_SEARCH.md`, not generic dataset phenomenon mining.

Before implementation, a candidate must have all of:

- a mature baseline/runtime with a credible local execution path;
- no mandatory NVIDIA-only CUDA, FlashAttention, Triton, Isaac, or custom CUDA;
- a method-level delta rather than benchmark QA;
- a direct 2025-2026 closest-prior comparison;
- a real policy/control metric;
- a 1-3 day falsification design;
- a concrete second evaluation path;
- no revival of any family in `RESEARCH_BRIEF.md -> Accumulated Negative Evidence`.

If zero candidates pass, stop the pipeline after Stage 1 with `NO CANDIDATE`. Do not invent a weak candidate merely because `AUTO_PROCEED=true`.

## Stage 2 — minimal implementation authorization

If exactly one strongest candidate passes Stage 1, the run may implement only the minimum code required for a falsification pilot.

Prefer:

- state-based observations before vision;
- behavior cloning / lightweight policy learning before large models;
- existing public baseline code;
- isolated local environments;
- standard PyTorch, NumPy, Gymnasium, MuJoCo, or similarly mature CPU-compatible paths.

Do not:

- modify simulator internals;
- reconstruct LIBERO/RoboCasa-style bootstrap/provenance stacks;
- train a foundation model;
- download a large VLA checkpoint;
- start real-robot work;
- introduce custom kernels;
- change system packages as root.

### Runtime kill rule

Reject the selected baseline and stop or use the already-admitted backup candidate if:

- two unrelated runtime/bootstrap blockers appear before scientific evidence;
- environment setup consumes more than roughly 45 minutes of active repair;
- the smallest reset/step or dataset-loading smoke test cannot be made reliable without substantial infrastructure work.

Infrastructure failure is not scientific evidence.

## Overnight compute budget

This is a bounded pilot night, not a full paper experiment campaign.

Limits:

- total new download payload: **25 GB maximum**;
- any single checkpoint: **10 GB maximum**;
- no video-heavy dataset download unless the selected hypothesis explicitly requires vision and the smallest required slice is within budget;
- at most **2 concurrent experiment jobs**;
- at most **8 scheduled experiment jobs** total before the final review;
- use CPU first for smoke tests;
- use at most **one DCU** for the first accelerator smoke/training job;
- the second DCU may be used only after the first scientific run is healthy, for an independent seed/task/ablation;
- total accelerator budget: **8 DCU-hours** across both devices;
- no single first-line training job should be scheduled for more than **2 hours** before a positive intermediate signal exists.

If the budget is exhausted, stop and report the best evidence obtained. Do not silently expand the budget.

## Scientific experiment gate

The minimum pilot must contain a policy/control consequence, such as:

- rollout success;
- return;
- task completion;
- downstream control after action-prediction training;
- cross-task or cross-domain policy generalization.

Pure classifier AUC, descriptive correlation, or dataset statistics are insufficient.

Pre-register in the experiment log:

- primary independent variable;
- primary policy/control metric;
- baseline;
- positive grow criterion;
- kill criterion.

## Negative-result behavior

If the primary candidate hits its pre-registered kill criterion:

1. record the negative result;
2. do not rescue it by redefining the claim;
3. do not convert it into benchmark QA;
4. one structural pivot is allowed only if:
   - the alternative was already admitted in Stage 1;
   - it uses the same mature baseline stack or an equally low-risk stack;
   - it remains inside the overnight compute budget.

Otherwise stop with `PIVOT / NO SURVIVING CANDIDATE`.

## Review loop

After initial scientific evidence:

- use the ARIS auto-review loop;
- maximum **3 substantive fix/review rounds** for this overnight run;
- fixes may improve experimental controls, implementation correctness, or a method already admitted;
- reviewer feedback may not authorize an unrelated new research direction;
- if two consecutive rounds add no new scientific finding, stop or structurally pivot according to ARIS iteration-log policy;
- a same-family reviewer score is provisional evidence, not final human acceptance.

## Git safety

Before implementation:

- start from a clean tree synchronized with authoritative `main`;
- create and work on branch:
  `aris/overnight-baseline-first-20260921`;
- never force-push;
- never merge to `main`;
- preserve all existing authority and negative-evidence files;
- commit compact code, configs, logs, and reports;
- do not commit datasets, checkpoints, caches, virtual environments, or large model artifacts;
- push the overnight branch when credentials allow.

## Required morning outputs

Always write:

`OVERNIGHT_REPORT.md`

If Stage 1 completes, also write/update:

`idea-stage/BASELINE_FIRST_METHOD_REPORT.md`

If experiments run, preserve the normal ARIS artifacts, including where applicable:

- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_TRACKER.md`
- `refine-logs/EXPERIMENT_RESULTS.md`
- `review-stage/AUTO_REVIEW.md`
- `NARRATIVE_REPORT.md`

`OVERNIGHT_REPORT.md` must state:

1. final status: `NO CANDIDATE`, `PIVOT`, `PILOT NEGATIVE`, `PILOT INCONCLUSIVE`, or `PILOT POSITIVE — HUMAN REVIEW REQUIRED`;
2. chosen baseline/runtime;
3. chosen method hypothesis;
4. exact closest prior and claimed delta;
5. what was implemented;
6. all experiments actually run;
7. primary policy/control results;
8. compute/download usage;
9. runtime blockers;
10. reviewer rounds and unresolved objections;
11. exact branch and HEAD;
12. whether remote branch was pushed;
13. the single recommended human decision for the morning.

## Hard stop

The overnight run ends after the bounded review loop and research handoff.

Do not:

- write the final paper automatically;
- claim the direction is accepted for Paper-1;
- merge to `main`;
- start real-robot experiments;
- start a second full research pipeline;
- continue looping after the bounded review budget.

A positive overnight result means only:

`PILOT POSITIVE — HUMAN REVIEW REQUIRED`.
