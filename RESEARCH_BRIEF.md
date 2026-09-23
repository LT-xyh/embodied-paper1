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
* **ArmnetBench outcome-dependent trajectory-support leakage**: P0 confirmed a strong length/outcome association, but P0.5 found only small incremental predictive gains after preserving full trajectory content, no robust policy-ranking distortion, weak/non-specific bimanual replication, and no causal pre-trim counterfactual. Treat this as benchmark-specific QA / known length-proxy behavior, not a Paper-1 route.
* **SocNavData2026 rater/context heterogeneity**: executable offline substrate, but rater consistency and context dependence are already central to the source work; a hierarchical rater/context analysis would be too close to standard HRI preference modeling for the current Embodied AI / Robot Learning Paper-1 target.

Future direction discovery must not repackage these routes unless genuinely new evidence changes either the novelty assessment or the execution assessment.

The next reselection pass must use a **substrate-first** process: verify executable public artifacts before promoting a scientific idea to the final shortlist.

## Strategy Reset After Wave 2

Two substrate-first waves failed to produce a Paper-1 candidate under the previous hard gates. This is evidence that continuing to mine public datasets for small offline effects is unlikely to be the fastest path.

The next search therefore changes strategy:

* move from **substrate-first phenomenon discovery** to **baseline-first method discovery**;
* start from a mature robot-learning training/evaluation stack that is actually executable on the available hardware;
* seek a small method or mechanism contribution that changes policy learning or control performance, rather than another benchmark audit;
* permit a lightweight mature simulator when it is self-contained, CPU-compatible or standard-PyTorch-compatible, and does not require NVIDIA-specific kernels or substantial runtime reconstruction;
* keep the first falsification pilot bounded to 1-3 days.

The previous "avoid simulator" rule is relaxed only for mature, low-risk simulators with a simple reset/step/evaluate path. LIBERO-style bootstrap/provenance reconstruction remains strongly disfavored.

## Strategy Reset After Baseline-First Internal Search

The overnight baseline-first search admitted a practical `robomimic + robosuite + MuJoCo` state-only stack, but found zero method candidates after direct 2025-2026 robotics-prior audit. This is evidence that continuing to search only inside recent robot-learning methods is unlikely to produce a fast novel Paper-1 direction.

The next search changes the source of novelty:

* keep the mature robot-learning baseline stack as the execution substrate;
* search **adjacent machine-learning fields** for transferable mechanisms that are not yet established in robot imitation/control;
* require a robot-specific scientific adaptation or mechanism, not a direct transplant;
* validate novelty against both the source ML literature and 2025-2026 robot-learning literature;
* retain the 1-3 day policy-level falsification requirement.

This strategy is called **Adjacent-Field Method Transfer**.

## Strategy Reset After Adjacent-Field Search

The adjacent-field method-transfer pass also returned zero candidates. This confirms that the current admission bar is effectively calibrated to a strong conference-style method novelty standard.

The publication objective, however, is disjunctive: **CCF B-or-above OR CAS Zone 3-or-above**. Optimizing only for the stronger conference novelty bar can therefore be slower than necessary.

The next step is not another idea search. It is a **venue-first contribution-bar recalibration**:

* identify realistic current CAS Zone 3-or-above journal targets in robotics / embodied intelligence / intelligent systems;
* inspect recent 2024-2026 papers from those venues, especially robot learning, manipulation, imitation learning, robustness, and embodied intelligence;
* infer what contribution structures those venues actually accept;
* separate a fast-journal contribution bar from a higher-upside conference contribution bar;
* only after this calibration should a new Paper-1 candidate search resume.

The recalibration may permit a technically meaningful incremental method, combination, or systematic empirical contribution if that contribution is demonstrably consistent with the target venue and is not a direct reimplementation of prior work.

## Track-A Publication Strategy

Venue-first recalibration concluded **FAST-JOURNAL BAR ADOPTED**.

Paper-1 now has two explicit bars:

* **Track A — primary / fastest route:** RA-L-first CAS Zone 3-or-above journal strategy. A technically meaningful robot-specific incremental method or principled combination is admissible if it changes closed-loop behavior, avoids direct prior collision, and is supported by a strong multi-task experiment package.
* **Track B — secondary / upside route:** retain the stronger CCF-B conference method-novelty bar. Track-B claims must be evaluated separately and are not required for Paper-1 success.

For Track A, do not reject a candidate merely because every component exists somewhere in prior literature. Reject it when the **combined robot-specific formulation and claimed effect** are already established by direct prior work, or when the contribution collapses to a trivial loss swap, benchmark change, or implementation detail.

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

Perform a **RA-L-first Track-A Method Search** under `idea-stage/TRACK_A_RAL_METHOD_SEARCH.md`.

Generate at most three serious hypotheses from concrete robot-learning failure modes. The search should prefer the already admitted `robomimic + robosuite + MuJoCo` state-only BC/BC-RNN stack and plan a second evaluation path such as Meta-World.

The purpose is to select **one bounded 1-3 day P0**, not to demand a CCF-B-level new mechanism.

Do NOT implement or train during this selection pass.

STOP after the Track-A shortlist and P0 recommendation.
