# Research Brief

## Problem

Select a new Paper-1 research direction in Embodied AI / Robot Learning.

The primary objective is the fastest credible path to a publishable paper, rather than continuation of existing engineering work.

## Publication Goal

Target at least one of:

* CCF B conference or above;
* CAS Zone 3 journal or above.

Timeline:

* ideal: complete experiments and first draft within 1-2 months;
* acceptable: 2-3 months;
* avoid directions whose core hypothesis realistically requires more than 6 months to validate.

## Compute Constraints

Available compute:

* 2 × Hygon DCU K100, 64 GB each;
* standard PyTorch Transformer workloads run normally.

Do not assume support for:

* NVIDIA-specific CUDA paths;
* FlashAttention;
* Triton-only kernels;
* CUDA-specific Mamba implementations;
* custom CUDA extensions unless compatibility is demonstrated first.

## Research Direction

Primary field:

* Embodied AI;
* Robot Learning.

VLA is preferred but NOT mandatory.

The following families should compete fairly:

* Vision-Language-Action models;
* imitation learning / behavior cloning;
* robot policy learning;
* world models;
* embodied evaluation and diagnostics;
* data-centric robot learning;
* VLM-conditioned robot policies.

Do not favor VLA merely because previous work used VLA.

## Execution Constraints

Strongly prefer:

* simulation-first or offline-data-first research;
* public datasets and benchmarks;
* mature public implementations;
* no real robot requirement for the core scientific claim;
* minimal falsifiable pilots executable within 1-3 days;
* lightweight adaptation, diagnosis, data or evaluation methods rather than foundation-model pretraining.

Strongly penalize directions requiring:

* invasive simulator modification;
* fragile renderer/runtime engineering;
* exact simulator-state restoration;
* new environment/bootstrap infrastructure;
* large-scale VLA pretraining;
* inaccessible private robot datasets;
* CUDA-specific kernels unavailable on the current DCU platform.

## Background

A previous ShiftVLA / ReplayVLA direction investigated persistent effects of closed-loop observation corruption in VLA policies.

The scientific hypothesis was NOT falsified.

The route was paused because LIBERO runtime, provenance and bootstrap integration consumed excessive engineering effort before scientific validation could begin.

Treat this as an engineering-risk lesson, not as scientific evidence against VLA or robustness research.

Do NOT automatically continue ReplayVLA.

Existing ShiftVLA code may be reused only when reuse materially shortens the newly selected scientific route.

## Engineering Stop Rules

1. Define a minimal falsifiable pilot before substantial implementation.
2. Prefer hypotheses that can be supported or killed within 1-3 days.
3. Do not serially repair multiple unrelated infrastructure blockers before obtaining scientific evidence.
4. Do not build a new runtime/bootstrap stack when a mature public implementation exists.
5. Ignore sunk engineering cost.
6. Infrastructure failure is not scientific evidence.
7. Do not silently convert a failed scientific hypothesis into a generic engineering contribution.
8. If the minimum pilot itself requires substantial simulator or runtime reconstruction, reconsider the research direction.

## Idea Evaluation Criteria

Every serious candidate must specify:

* scientific hypothesis;
* closest recent prior work, especially from 2025-2026;
* exact novelty relative to prior work;
* public benchmark or dataset;
* available baseline implementation;
* minimum falsifiable pilot;
* estimated implementation effort;
* estimated compute cost;
* DCU compatibility;
* runtime/infrastructure risk;
* positive grow criterion;
* negative kill criterion;
* strongest likely reviewer rejection argument;
* publication potential;
* longer-term extension potential toward stronger venues and PhD research.

## Literature Scope

Prioritize recent work from:

* CoRL;
* RSS;
* ICRA;
* IROS;
* RA-L / T-RO;
* relevant CVPR / ICCV / ECCV;
* relevant NeurIPS / ICML / ICLR;
* recent arXiv work when sufficiently relevant.

Pay special attention to work published or released in 2025-2026.

## Non-Goals

For Paper-1, do not prioritize:

* training a foundation VLA from scratch;
* real-robot-only research;
* low-level systems optimization as the main scientific contribution;
* new CUDA kernel engineering;
* simulator infrastructure as the main contribution;
* continuing ReplayVLA solely because existing code already exists.

## Desired First Output

Perform research-direction discovery from scratch.

Produce:

* a current literature landscape;
* important crowded or low-value directions that should be eliminated;
* the strongest Top-3 candidates;
* novelty assessment for each;
* minimum falsifiable pilot for each;
* implementation and runtime risk;
* compute/DCU compatibility;
* strongest rejection risk;
* publication potential;
* longer-term research extension.

Do NOT implement methods.

Do NOT install benchmark runtimes.

Do NOT launch GPU experiments.

STOP after the Top-3 research-direction report.

