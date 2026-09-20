# Substrate-First Research-Direction Reselection

**Status:** ACTIVE RESELECTION CONTRACT  
**Date:** 2026-09-20  
**Binding context:** `RESEARCH_BRIEF.md`

## Purpose

The next Paper-1 direction search must reverse the previous idea-first workflow.

Previous passes repeatedly found scientifically interesting ideas whose minimum pilots later failed because the closest 2026 literature was too crowded, the required labels were not public, or the available runtime depended on NVIDIA CUDA / FlashAttention / simulator reconstruction.

This pass therefore uses the following order:

```text
public executable substrate
-> static execution admission
-> scientific variables actually present
-> candidate hypothesis
-> 2025-2026 novelty audit
-> final shortlist
```

No candidate may enter the final shortlist before its substrate is statically admitted.

## Phase 1 — Discover executable substrates first

Search for public Embodied AI / Robot Learning substrates such as:

* offline robot datasets;
* released policy trajectories;
* success/failure-labelled rollouts;
* simulator-state logs;
* released predictions or evaluation traces;
* pretrained checkpoints;
* lightweight public simulators;
* standard-PyTorch policy implementations;
* embodied/VLA datasets that can be analyzed without running the original policy.

For each substrate, verify from the actual repository, data card, paper appendix, or official documentation:

1. exact repository and canonical artifact location;
2. publication / release year;
3. tasks and embodiments;
4. observation modalities;
5. action representation;
6. labels actually present;
7. simulator states actually present;
8. success/failure outcomes actually present;
9. whether pretrained policy inference is required;
10. whether simulator execution is required;
11. required software stack;
12. NVIDIA CUDA requirement;
13. FlashAttention / Triton / custom CUDA requirement;
14. approximate download size;
15. whether a useful pilot can run on CPU or standard PyTorch on Hygon DCU;
16. known installation/runtime risks.

Do not infer undocumented fields.

## Hard execution gate

Reject a substrate as the starting point for Paper-1 if the minimum scientific pilot requires, before obtaining evidence:

* NVIDIA-only CUDA software;
* FlashAttention;
* Triton-only implementations;
* custom CUDA porting;
* rebuilding LIBERO/RoboCasa-style runtime infrastructure;
* exact simulator-state restoration;
* large foundation-model training;
* real-robot data collection;
* substantial new manual annotation;
* downloading hundreds of GB before the hypothesis can be tested.

Prefer, in order:

1. offline files with the needed variables and outcomes;
2. released trajectories / predictions / evaluation traces;
3. lightweight replay without neural policy inference;
4. standard-PyTorch-only inference already documented to run without CUDA-specific kernels.

A slightly lower publication ceiling with a clean pilot is preferable to a higher-upside idea with unresolved runtime compatibility.

## Phase 2 — Build an executable substrate landscape

Retain approximately 5-10 substrates only after the hard execution gate.

For every retained substrate, list the scientific variables that already exist in the public artifacts, for example:

* success/failure;
* failure type;
* recovery;
* task complexity;
* embodiment;
* object state;
* scene state;
* language;
* policy family;
* trajectory structure;
* temporal consistency;
* action uncertainty;
* demonstration quality;
* intervention;
* calibration.

Do not invent a research idea before this inventory is complete.

## Phase 3 — Generate scientific questions from admitted substrates

Generate hypotheses only from variables and interventions that are actually available or cheaply derivable from admitted substrates.

VLA is preferred but not mandatory. Imitation learning, policy diagnostics, data-centric robot learning, world models, representation analysis, generalization, and other Embodied AI / Robot Learning directions should compete fairly.

The primary contribution must be more than:

* a dataset analysis with no general scientific claim;
* a renamed metric;
* a benchmark wrapper;
* a standard statistical trick;
* another robustness table;
* another generic evaluation suite.

## Mandatory exclusions from prior reselection

Do not repackage the following as the main novelty unless new evidence materially changes the prior decision:

* ReplayVLA-style LIBERO runtime interventions;
* segment/state-action demonstration filtering;
* generic mixed-quality demonstration selection;
* counterfactual visual/language shortcut diagnosis;
* generic VLA safety benchmarking;
* generic world-model evaluator shift degradation;
* generic world-model uncertainty calibration;
* generic world-model action-following diagnosis;
* common-random-number policy comparison;
* generic failure recovery/retry;
* generic adaptive action chunking;
* generic active factor evaluation;
* contact-topology / contact-flow / contact-graph transfer.

The full rationale is recorded in `RESEARCH_BRIEF.md`, `idea-stage/IDEA_REPORT.md`, and `idea-stage/CONTACT_TOPOLOGY_ADMISSION.md`.

## Scientific admission

Before a candidate enters the final shortlist, it must specify:

1. precise falsifiable hypothesis;
2. closest direct 2025-2026 prior work, searched through September 2026;
3. exact claim already covered by each closest prior;
4. the candidate's non-overlapping scientific claim;
5. the experiment that distinguishes the new claim from the closest prior;
6. why the difference is a mechanism/method/scientific finding rather than terminology or metric choice;
7. strongest likely reviewer rejection argument;
8. positive grow criterion;
9. negative kill criterion.

If the novelty collapses after direct-neighbor inspection, reject the candidate before implementation.

## Static execution admission

Every final candidate must identify:

1. exact public repository / dataset / checkpoint;
2. exact files or artifact class required for the minimum pilot;
3. exact labels or fields used by the hypothesis;
4. whether policy inference is needed;
5. whether simulator execution is needed;
6. required packages and runtime family;
7. expected storage class;
8. CPU / Hygon DCU compatibility;
9. minimum implementation steps;
10. primary independent variable;
11. primary dependent variable;
12. controls;
13. statistical test or evaluation rule;
14. positive criterion;
15. kill criterion.

Fundamental hardware/runtime compatibility may not be deferred until after ranking.

## Search and publication objective

Search relevant work through **2026-09-20**, prioritizing CoRL, RSS, ICRA, IROS, RA-L/T-RO, relevant CVPR/ICCV/ECCV, NeurIPS/ICML/ICLR, and strong recent arXiv work.

Optimize jointly for:

```text
scientific novelty
x falsifiability
x executable substrate maturity
x time-to-first-evidence
x publication potential
```

Project target remains:

* ideally complete experiments + first draft in 1-2 months;
* 2-3 months acceptable;
* CCF B or above OR CAS Zone 3 or above;
* potential to extend toward stronger Embodied AI / Robot Learning work.

## Required output

Write:

`idea-stage/SUBSTRATE_FIRST_IDEA_REPORT.md`

The report must contain:

1. **Executable Substrate Landscape**
2. **Rejected Substrates and Exact Rejection Reasons**
3. **Scientific Variables/Gaps Enabled by Surviving Substrates**
4. **Initial Candidate Hypotheses**
5. **Aggressive 2025-2026 Novelty Rejection**
6. **Final Shortlist of at Most Top-3**
7. A separate **STATIC EXECUTION ADMISSION** section for every retained candidate

Returning Top-2, Top-1, or zero candidates is valid and preferable to retaining weak candidates.

Update `MANIFEST.md`.

## Stop rule

This is a research-selection task only.

Do NOT:

* install runtimes;
* download large datasets/checkpoints;
* implement candidate methods;
* launch simulators;
* launch GPU jobs;
* start real-robot experiments.

STOP after the substrate-grounded shortlist and static execution admission.

No candidate is implementation-authorized by this contract.
