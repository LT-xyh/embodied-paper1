# Substrate-First Reselection — Wave 2

**Status:** ACTIVE RESEARCH-SELECTION AUTHORITY
**Date:** 2026-09-21
**Binding context:** `RESEARCH_BRIEF.md`

## Why this wave is different

Previous searches repeatedly found real but paper-weak effects tied to one benchmark, one preprocessing rule, or one analysis convention. This wave must favor research questions whose scientific claim survives beyond one dataset implementation.

A final candidate should preferably have:
- a method or mechanism contribution, not benchmark QA;
- a clean public execution path;
- at least one independent replication path identified before ranking;
- a 1–3 day falsification pilot;
- a plausible 1–2 month route to a complete paper.

Do not revive any route listed under **Accumulated Negative Evidence** in `RESEARCH_BRIEF.md`.

## Phase 1 — search for evidence-rich substrates

Search public Embodied AI / Robot Learning artifacts through September 2026.

Prioritize substrates with one or more of:
- paired or repeated-condition trajectories;
- explicit interventions or controlled perturbations;
- multiple policy families on the same tasks;
- multiple robot embodiments under a shared schema;
- success/failure plus dense state/action trajectories;
- train/test domain shifts already packaged in the release;
- multiple independent datasets supporting the same scientific variable;
- small low-dimensional state/action data that allow lightweight learning experiments.

Prefer:
- offline trajectories;
- released embeddings/features;
- small or selectively downloadable datasets;
- standard PyTorch / NumPy / sklearn paths;
- CPU or Hygon-DCU-compatible code.

Strongly penalize:
- simulator/runtime reconstruction;
- NVIDIA-only code;
- FlashAttention/Triton/custom CUDA;
- >100 GB prerequisite downloads;
- real robot dependency;
- large VLA inference as the first evidence source;
- one-off benchmark quirks.

## Phase 2 — candidate generation

Generate hypotheses only after identifying the executable evidence.

Candidate families may include:
- lightweight imitation learning / behavior cloning;
- offline policy learning;
- trajectory representation;
- temporal credit or progress modeling;
- cross-policy/cross-task generalization;
- selective prediction / uncertainty only when the claim is stronger than generic calibration;
- data interventions with paired evidence;
- cross-embodiment learning only when execution is low-risk;
- other Embodied AI / Robot Learning mechanisms supported by public artifacts.

VLA is optional. Do not force a VLA direction.

## Hard scientific gate

A candidate may enter the final shortlist only if:

1. the hypothesis is falsifiable;
2. closest 2025–2026 prior work is directly compared;
3. the contribution is more than:
   - a metric rename,
   - a benchmark audit,
   - a statistical association,
   - a standard hierarchical model,
   - a standard variance-reduction trick,
   - a dataset-specific preprocessing fix;
4. the proposed experiment distinguishes the claim from the closest prior;
5. the strongest result would still matter if one benchmark were removed.

If the claim fundamentally depends on one dataset's idiosyncratic annotation or preprocessing, reject it.

## Hard replication gate

Before ranking a candidate, identify one of:

### A. Direct independent replication
A second independently released dataset can test the same mechanism with no major runtime work.

### B. Built-in independent domains
One release contains sufficiently distinct robots/tasks/domains and the paper claim is explicitly about cross-domain generalization, with a credible external replication path identified.

Candidates with **no replication path** may not enter the final shortlist.

Do not count:
- single-arm and bimanual variants from the same release pipeline as independent datasets;
- train/test splits of the same benchmark as independent replication.

## Hard execution gate

For every final candidate specify:

- exact repo/dataset/checkpoint;
- exact files/fields needed;
- download size;
- policy inference needed or not;
- simulator needed or not;
- CUDA-specific dependency or not;
- minimal pilot steps;
- CPU/DCU compatibility;
- expected first-evidence time;
- positive criterion;
- kill criterion.

Reject any candidate whose first credible evidence requires:
- simulator reconstruction;
- CUDA-specific porting;
- large-model training;
- large checkpoint inference with unsupported kernels;
- real-robot collection.

## Breadth control

Do not generate a long list.

Search broadly, but retain **at most 2** candidates.

Returning 1 or 0 is preferred to weak padding.

For every rejected near-miss, record only the decisive reason.

## Required final report

Write:

`idea-stage/SUBSTRATE_FIRST_WAVE2_REPORT.md`

Required sections:

1. **Evidence-Rich Substrate Landscape**
2. **High-Value Rejections**
3. **Candidate Hypotheses**
4. **Closest 2025–2026 Prior Audit**
5. **Replication Admission**
6. **Static Execution Admission**
7. **Final Shortlist: at most Top-2**
8. **One recommended next P0**, or **NO CANDIDATE**

For each survivor include:

- precise claim;
- exact novelty;
- direct prior;
- primary substrate;
- independent replication substrate/path;
- minimal 1–3 day pilot;
- compute/storage;
- reviewer rejection risk;
- publication ceiling;
- PhD-extension potential;
- kill criteria.

## Stop rule

Research selection only.

Do NOT:
- implement a candidate;
- install heavy runtimes;
- download large datasets/checkpoints;
- launch simulator/GPU jobs;
- start a P0 automatically.

Update `MANIFEST.md`, commit, push, and stop after the Wave-2 report.
