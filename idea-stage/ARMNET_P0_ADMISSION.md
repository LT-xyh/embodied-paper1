# ArmnetBench P0 Scientific Admission

**Status:** ACTIVE BOUNDED P0 AUTHORIZATION  
**Date:** 2026-09-20  
**Binding context:** `RESEARCH_BRIEF.md`, `idea-stage/SUBSTRATE_FIRST_RESELECTION.md`, and `idea-stage/SUBSTRATE_FIRST_IDEA_REPORT.md`

## Decision entering P0

The ArmnetBench outcome-dependent censoring direction is **CONDITIONAL GO for P0 only**.

This document authorizes one bounded CPU/offline admission run. It does **not** authorize full method development, video download, GPU training, simulator execution, or a paper-scale experiment suite.

The P0 question is:

> Does ArmnetBench's outcome-dependent episode trimming create a reproducible trajectory-length / observation-support leakage that materially affects downstream learned outcome evaluation after controlling for task and policy?

The paper-level claim is **not** merely that trajectory length can correlate with quality. That phenomenon is already adjacent to prior robot-preference work that controls trajectory length to prevent quality proxies.

The only potentially useful scientific direction is narrower:

> Outcome-dependent post-processing in a robot benchmark can inject target information into the released trajectory support and bias downstream learned evaluators or rankings.

P0 exists to kill this claim cheaply if the released artifact cannot support it.

---

## Execution mode

Run P0-A and, only if P0-A passes, immediately continue to P0-B in the **same execution session**.

Do not stop for human confirmation between P0-A and P0-B.

If any mandatory kill condition is met, stop immediately, record **PIVOT**, commit the evidence/report, and do not continue with additional analyses.

### Allowed

- Read public documentation, repository files, Hugging Face dataset metadata, Parquet/JSON metadata, and source mappings.
- Download only the smallest non-video ArmnetBench files needed for this audit.
- Use HTTP range/HEAD requests when useful.
- Download the non-video single-arm metadata/state/action subset if its verified size remains small.
- Use CPU Python analysis.
- Create minimal analysis scripts, tables, CSV/JSON summaries, and plots required for P0.
- Use `pandas`, `pyarrow`, `numpy`, `scipy`, `scikit-learn`, and `matplotlib` if needed.
- If one of those lightweight CPU packages is missing, install it in an isolated local environment only. Do not alter system packages.
- Commit P0 scripts and compact derived results that are appropriate for Git.
- Keep downloaded dataset artifacts out of Git.

### Forbidden

- Video download.
- Full 60+ GB ArmnetBench release download.
- Bimanual data unless the single-arm P0 passes and a tiny metadata-only check is needed for confirmation.
- GPU jobs.
- DCU-specific optimization.
- Torch model training unless a later authority explicitly permits it.
- Simulator execution.
- Real-robot execution.
- LIBERO, RoboCasa, Isaac Sim, MuJoCo environment reconstruction.
- Large checkpoint download.
- VLA inference.
- New paper method implementation.
- Expanding into another research direction during this run.

### Download budget

The default P0 download budget is **250 MB total**.

If the required non-video evidence unexpectedly exceeds 250 MB, stop with **PIVOT / substrate gate failed** unless the excess is only a clearly documented small metadata file and remains below 500 MB total.

Never download video merely to rescue the direction.

---

# P0-A — Artifact Truth Audit

P0-A determines whether the scientific question is identifiable from the public release.

## A1. Verify the actual published schema

Inspect the official ArmnetBench paper, dataset card, repository/data files, and Hugging Face metadata.

Determine exactly where the following exist, if anywhere:

- `success`
- `success_class`
- `success_cutoff_time`
- episode length / frame count
- `task`
- policy identity
- policy type
- embodiment identity
- source repository identity
- source episode index or equivalent provenance
- `next.reward`
- `next.done`
- action
- robot state

Do not infer that a field exists because it is described in prose.

For every field, record:

- exact file/path;
- exact column/key;
- whether it is per-episode or per-frame;
- whether it is directly released or only mentioned in processing documentation.

## A2. Verify post-processing semantics

Establish from primary sources whether:

- successful episodes are end-trimmed;
- suboptimal episodes are end-trimmed;
- failure episodes are left at their original horizon;
- trimming uses a human-provided or derived `success_cutoff_time`;
- the released trajectory length therefore depends on the outcome/annotation path.

Record the exact evidence.

## A3. Determine whether the counterfactual pre-trim trajectory is recoverable

Check whether the released data provide a deterministic link back to the original, untrimmed source episode.

The strongest case is:

```text
released episode
-> source repo / source episode
-> original full trajectory
-> published cutoff
```

Classify recoverability as exactly one:

- **FULL**: original full trajectory and cutoff/linkage are public and cheaply retrievable;
- **PARTIAL**: source linkage exists but cutoff or original idle tail is not directly recoverable;
- **NONE**: the released artifact contains only the already-trimmed trajectory with no usable public counterfactual.

Do not reconstruct missing tails from assumptions.

## A4. Verify policy/outcome confounds

Inventory outcome counts by:

- task;
- policy identity;
- policy type;
- teleoperation vs learned policy;
- success class.

Teleoperation episodes are **not** admissible as the primary leakage test if they are successful by construction.

The P0-B primary analysis must use learned-policy rollouts only.

## P0-A hard kill conditions

Stop with **PIVOT** before P0-B if any of these hold:

1. the public release does not allow reliable identification of task, policy, outcome class, and episode length;
2. learned-policy rollouts cannot be separated from teleoperation;
3. outcome-dependent trimming cannot be established from primary release evidence;
4. the only usable evidence would require video or simulator reconstruction;
5. the required non-video files exceed the bounded download gate;
6. the artifact is too small or too confounded to form at least two meaningful `(task, policy)` strata containing more than one outcome class.

`success_cutoff_time` being absent as a released column is **not by itself an automatic kill**. If trimming semantics are documented and the released trajectories support a clean length-leakage test, P0-B may proceed, but the final claim must be limited accordingly.

If pre-trim trajectories are not recoverable, explicitly downgrade the maximum interpretation from **causal post-processing effect** to **released-support leakage association**.

---

# P0-B — CPU Leakage Sanity Test

Run only if P0-A passes.

Use the smallest available non-video single-arm subset.

## B1. Analysis population

Primary population:

- learned-policy rollouts only;
- exclude teleoperation;
- single-arm ArmnetBench;
- strata defined primarily by `task × policy identity` or, if sample size requires, `task × policy_type`.

Do not pool all episodes first and call the pooled correlation evidence.

Report the number of episodes and outcome classes in every retained stratum.

Drop strata that do not contain meaningful outcome variation.

## B2. First-order leakage test

Define released episode horizon using the actual released frame count or duration.

Test within strata:

```text
released_horizon ~ success_class
```

Required outputs:

- horizon distributions by outcome;
- standardized effect sizes;
- simple within-stratum tests;
- clustered or stratified confidence intervals;
- a pooled model only after task/policy controls are included.

The goal is not significance hunting. The goal is to establish whether released observation support is outcome-dependent after obvious confounds are controlled.

## B3. Minimal prediction baselines

Use lightweight CPU baselines only.

At minimum compare:

1. **Length-only**
   - episode frame count / duration only.

2. **Non-length summary**
   - simple state/action summary statistics that do not directly encode the termination time when avoidable.

3. **Non-length summary + length**

4. **Equal-duration prefix**
   - choose one or more fixed prefix horizons;
   - include only episodes with enough available frames for that prefix;
   - do not expose the original termination location through padding masks, frozen tails, or explicit sequence length.

Do **not** use ordinary right-padding as the primary anti-leakage intervention. Padding/masks can preserve the original endpoint.

A simple logistic / multinomial regression, linear model, tree baseline, or similarly small estimator is sufficient. Do not introduce a deep sequence model in P0.

## B4. Split discipline

Random episode splitting alone is insufficient.

Use at least:

- held-out task evaluation where sample size permits;
- held-out policy evaluation where sample size permits;
- grouped/clustered resampling by task and episode;
- within-stratum analysis.

The purpose is to distinguish benchmark-wide leakage from one-policy or one-task quirks.

## B5. Downstream evaluator consequence

Only if B2/B3 show a real leakage effect, test whether it changes a **learned evaluator-derived** policy comparison.

Keep terminology precise:

- ArmnetBench's human-labelled leaderboard is ground truth for this audit;
- the analysis concerns rankings/scores produced by a learned outcome evaluator trained on the released trajectories.

Compare evaluator-derived policy scores/rankings under:

- full released trajectory features;
- equal-duration-prefix features;
- length-removed / censoring-aware feature sets when identifiable.

Report rank correlations and any policy-order flips.

Do not claim that ArmnetBench's official human-labelled leaderboard itself changes.

---

# Interpretation levels

At the end, assign exactly one evidence level.

## LEVEL 0 — PIVOT

Use if:

- artifact truth fails;
- no meaningful length/outcome relation remains after task/policy controls;
- effect is confined to one task or one policy;
- equal-duration prefixes behave essentially the same as full trajectories;
- only a descriptive length table remains;
- downstream evaluator behavior is unaffected;
- or the conclusion collapses to the already-known observation that trajectory length can proxy quality.

## LEVEL 1 — RELEASE-SUPPORT LEAKAGE

Use if:

- outcome-dependent trimming is documented;
- released horizon carries reproducible label information across multiple controlled strata;
- but original pre-trim trajectories/cutoffs are not recoverable strongly enough for a causal intervention.

This level is interesting but **does not yet authorize Paper-1 implementation**.

## LEVEL 2 — POST-PROCESSING BIAS SIGNAL

Use only if:

- linkage/cutoff/pre-trim evidence permits a direct or near-direct intervention;
- the effect survives task/policy controls;
- equal-duration or pre-trim counterfactual analysis materially changes prediction/calibration or learned evaluator ranking;
- and the effect reproduces across multiple tasks/policies.

LEVEL 2 still requires a second independent dataset or equivalent replication path before final Paper-1 scientific admission.

---

# Quantitative grow / kill criteria

The P0 is intentionally conservative.

## Grow signal

A candidate can survive P0 only if all are true:

1. outcome-dependent trimming is documented from primary sources;
2. learned-policy-only strata show a consistent horizon/outcome effect across multiple tasks or policies;
3. length-only or length-augmented baselines carry nontrivial held-out signal;
4. an equal-duration-prefix analysis materially reduces that signal or changes learned evaluator behavior;
5. the result is not explained by teleoperation, one task, one policy, or a simple class-prior artifact.

No single p-value is sufficient.

## Immediate kill

Return **PIVOT** if any of these are observed:

- no robust within-task/policy horizon effect;
- equal-duration prefixes preserve essentially all of the alleged leakage effect;
- only teleoperation drives the result;
- one task/policy drives the result;
- the only finding is “longer/shorter trajectories correlate with outcomes”;
- learned evaluator scores/rankings are unchanged by the intervention;
- artifact provenance prevents any stronger interpretation and no generalizable mechanism remains.

---

# Replication search after P0

Do **not** begin a broad new idea search.

Only if P0 reaches LEVEL 2, perform a narrow read-only search for a **second independent robot dataset** with:

- success/failure or quality labels;
- released trajectory length/support;
- documented outcome-dependent trimming, early stop, success clipping, or annotation-dependent post-processing;
- small or selectively downloadable non-video artifacts;
- no simulator/GPU requirement for the first replication.

Do not download the second dataset during this P0 run unless it is trivially small (<100 MB) and needed only to verify schema.

Record candidate replication datasets in the report.

If no plausible second dataset exists, note that as a publication-risk blocker.

---

# Required files

Write compact, reproducible artifacts under:

`p0-armnet/`

At minimum:

- `p0-armnet/README.md` — exact reproduction steps;
- `p0-armnet/artifact_audit.md` — P0-A evidence and field/path table;
- `p0-armnet/analysis.py` — minimal CPU analysis if P0-B runs;
- `p0-armnet/results.json` — machine-readable key results if P0-B runs;
- `p0-armnet/results.md` — concise human-readable P0-B results if P0-B runs.

Final adjudication:

`idea-stage/ARMNET_P0_RESULT.md`

Update:

`MANIFEST.md`

Do not commit downloaded dataset binaries, cache files, virtual environments, or large generated artifacts.

---

# Final verdict

The final report must return exactly one:

- **PIVOT**
- **P0 SURVIVES — LEVEL 1**
- **P0 SURVIVES — LEVEL 2**

Then state:

- whether Paper-1 implementation is authorized: **NO**;
- whether a second-dataset replication path was found;
- exact files changed;
- exact downloaded byte count;
- whether any GPU/simulator/video was used;
- full commit SHA after committing/pushing the bounded P0 artifacts.

## Stop rule

This authority ends after the P0 verdict and optional read-only second-dataset replication search.

Do not proceed into full model development or paper-scale experiments without a new authority.
