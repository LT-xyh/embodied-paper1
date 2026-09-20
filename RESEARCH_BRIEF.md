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

## Accumulated Negative Evidence

The following directions have already been investigated and are not default continuation routes:

* **ReplayVLA / closed-loop corruption persistence**: the scientific hypothesis was not falsified, but LIBERO runtime/provenance/bootstrap cost prevented timely scientific validation.
* **Segment/state-action mixed-quality demonstration filtering**: crowded by S2I, SCIZOR, DataMIL, and adjacent 2025-2026 work.
* **Counterfactual visual/language shortcut diagnostics**: crowded by LIBERO-CF, LIBERO-VIFO, and adjacent work.
* **Generic VLA safety benchmarking**: crowded by LIBERO-Safety, LIBERO-VIFO, and related 2026 evaluation work.
* **Generic world-model evaluator calibration, shift degradation, ranking, or action-following diagnosis**: crowded by WorldEval, WorldGym, WorldEcho/WorldSync, IRASim, and decision-centric evaluation work.
* **Common-random-number coupling for world-model policy comparison as the primary contribution**: estimator-level variance reduction is too generic and historically established to carry the main robotics contribution by itself.
* **Generic recovery/retry, adaptive action-chunk horizons, and active factor evaluation**: direct 2026 prior work substantially covers these claims.
* **Contact-topology/contact-flow/contact-graph cross-embodiment transfer as the main novelty**: KITE, ContactFlow, TopoRetarget, C2Dex, and adjacent 2026 work substantially narrow the novelty gap. The stronger contact-feasibility-boundary claim also lacks a clean public DCU/CPU-compatible 1-3 day falsification path.

Future direction discovery must not repackage these routes unless genuinely new evidence changes either the novelty assessment or the execution assessment.

The next reselection pass must use a **substrate-first** process: verify executable public artifacts before promoting a scientific idea to the final shortlist.

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

## Current Next Output

Perform a **substrate-first research-direction reselection** under the separate authority in `idea-stage/SUBSTRATE_FIRST_RESELECTION.md`.

The next pass must first identify public datasets, released trajectories, checkpoints, simulator-state logs, evaluation traces, or lightweight runtimes that can produce scientific evidence under the current hardware constraints. Only after static execution admission may research ideas be generated from those substrates.

The final shortlist may contain Top-3, Top-2, Top-1, or zero candidates. Do not retain weak candidates merely to fill a quota.

Every retained candidate must pass both:

* **scientific admission**: a precise falsifiable claim with a non-overlapping 2025-2026 novelty gap;
* **static execution admission**: an exact public substrate and a credible 1-3 day pilot that does not require CUDA-specific porting, runtime reconstruction, real-robot data, or large-model training before scientific evidence.

Do NOT implement methods.

Do NOT install benchmark runtimes.

Do NOT download large datasets or checkpoints.

Do NOT launch simulator, GPU, or real-robot experiments.

STOP after the substrate-grounded shortlist and static execution admission.

