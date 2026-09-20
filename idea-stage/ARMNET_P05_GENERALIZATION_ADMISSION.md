# ArmnetBench P0.5 Paper-Admission Gate

**Status:** ACTIVE BOUNDED AUTHORIZATION
**Date:** 2026-09-20
**Parent evidence:** `idea-stage/ARMNET_P0_RESULT.md`
**Parent commit:** `c8784c0bc99be0b35fb4ef4a658719b8bda89b2a`

## Purpose

P0 found a strong released-support signal, but not yet a Paper-1 claim.

Observed single-arm evidence:
- 2,099 learned-policy episodes;
- 46 mixed task × policy strata;
- successes shorter in all 46 strata;
- length-only AUC 0.933 leave-task-out / 0.930 leave-policy-out;
- non-length summary AUC 0.806 / 0.878;
- non-length summary + length AUC 0.937 / 0.954;
- pre-trim/cutoff provenance: NONE.

Important correction: the equal-duration-prefix drop is not a pure censoring effect because it removes both endpoint information and genuine late-trajectory behavior.

Mandatory prior: RoboMeter (RSS 2026) fixes compared trajectories to the same length T to prevent preference models from using trajectory length as a proxy for quality. Therefore "trajectory length can proxy quality" is not sufficient novelty.

The only potentially useful claim is:

> Outcome-conditioned dataset construction can inject label information into released robot-trajectory support, inflate learned evaluator performance, and distort policy comparison unless the evaluator is support-invariant.

This run decides whether that stronger claim survives.

## Execution

Run all gates in one session. Do not ask for confirmation between gates.

No full method development is authorized.

Allowed:
- reuse existing single-arm non-video data;
- download ArmnetBench bimanual non-video data only, if verified <=100 MB;
- CPU-only analysis;
- narrow web/repository search for an independent replication dataset;
- download one independent non-video replication artifact only if the required files are <=100 MB.

Forbidden:
- video;
- GPU/DCU jobs;
- simulator execution;
- VLA inference;
- large checkpoints;
- full reward-model training;
- broad idea discovery;
- LIBERO/RoboCasa/Isaac reconstruction.

Total new download budget: 200 MB.

## Gate A — isolate the support/length channel

Use the full released single-arm trajectory while removing absolute duration.

Required representation:
1. take state/action sequence;
2. map frame position to normalized time in [0,1];
3. interpolate each channel to K=32 fixed points;
4. expose no original frame count, duration, padding mask, or original frame index;
5. standardize inside training folds only.

Use a simple regularized CPU model.

Compare matched models:
- content-only: time-normalized full-trajectory representation;
- content + log(length).

Evaluate:
- leave-task-out AUC and balanced accuracy;
- leave-policy-out AUC and balanced accuracy;
- Brier score / calibration;
- bootstrap confidence interval for the improvement from adding length.

Also test within task × policy strata whether standardized relative horizon predicts strict success. Include a negative control that permutes length within task × policy.

Recompute learned evaluator policy scores for content-only and content+length. Compare each directly to human strict-success policy ranking using:
- Spearman;
- Kendall tau;
- pairwise disagreement count versus human order;
- task-cluster bootstrap where feasible.

Do not use equal-prefix performance as the primary evidence for censoring.

### Gate A kill

PIVOT if:
- adding length to full-trajectory duration-invariant content gives negligible held-out gain;
- within-stratum relative horizon loses the effect;
- permutation controls reproduce the gain;
- ranking/calibration effects are weak or inconsistent;
- or the result reduces to RoboMeter's already-known length-proxy issue.

## Gate B — bimanual internal replication

Run only if Gate A survives.

First verify:
- same outcome-dependent trimming rule;
- learned rollouts separable from teleoperation;
- task/policy/outcome/length available;
- non-video download <=100 MB.

Then replicate only:
1. within task × policy horizon/outcome effect;
2. time-normalized content-only versus content+length;
3. policy ranking/calibration comparison if sample size permits.

Bimanual is INTERNAL replication only because it shares the ArmnetBench collection/release pipeline.

Strongly favor PIVOT if bimanual contradicts the single-arm result.

## Gate C — independent replication search

Run only if Gates A/B survive.

Search narrowly for an independent public robot dataset with documented:
- success/failure or quality labels;
- episode length/support;
- outcome-dependent end trimming, success-based early termination, annotation-dependent clipping, or equivalent endpoint handling;
- small/selectively downloadable non-video artifacts;
- no simulator/GPU requirement for the first test.

For each candidate record:
- repository/data card;
- year;
- robot/tasks;
- labels;
- episode length;
- exact trimming/termination mechanism;
- whether pre-trim data exist;
- required runtime;
- non-video size;
- whether the same leakage test is actually possible.

Mandatory checks:
- RoboMeter / RBM-1M processing and source datasets;
- LeRobot releases with explicit successes/failures and trim/early-stop semantics;
- small ManiSkill/Minari-style offline releases if applicable;
- `adityx23/icl-dataset`, while distinguishing task-balancing exclusion of long successes from within-trajectory endpoint trimming.

Classify independent replication as exactly one:
- DIRECT
- MECHANISTIC-NEIGHBOR
- NONE

Do not accept a dataset merely because successful episodes are shorter. The mechanism must be documented.

If a DIRECT dataset can be tested with <=100 MB non-video download, run the smallest replication. Otherwise document it only.

## Paper-level novelty check

Explicitly compare the proposed claim to RoboMeter:

1. What does RoboMeter already prevent or acknowledge?
2. What remains new here?
3. Is the remaining claim genuinely about dataset-construction bias / evaluator deployment mismatch / ranking distortion, or only a length-control heuristic?
4. Does evidence generalize beyond one Armnet release pipeline?
5. Would a skeptical CoRL/ICRA/RA-L reviewer see this as a scientific finding or benchmark QA?

If the strongest remaining result is Armnet-specific preprocessing QA, return PIVOT.

## Final verdict

Return exactly one:

### PIVOT
Use if Gate A fails, bimanual contradicts the result, no meaningful downstream effect survives, no credible independent replication path exists, or novelty collapses to the known length-proxy issue.

### P0.5 SURVIVES — INTERNAL REPLICATION ONLY
Use if Gate A is strong and bimanual replicates, but no DIRECT independent dataset is found. Full Paper-1 implementation remains unauthorized.

### P0.5 SURVIVES — PAPER-ADMISSION CANDIDATE
Use only if:
- Gate A cleanly isolates an independent support/length channel;
- bimanual is consistent;
- learned evaluator ranking/calibration is materially affected relative to human outcomes;
- a DIRECT independent replication substrate is found or executed;
- and the novelty is stronger than RoboMeter's equal-length precaution.

This verdict still requires a final scientific admission decision before paper-scale work.

## Required outputs

Create:
- `p0-armnet/p05_analysis.py`
- `p0-armnet/p05_results.json`
- `p0-armnet/p05_results.md`
- `p0-armnet/p05_replication_search.md`
- `idea-stage/ARMNET_P05_RESULT.md`

Update:
- `MANIFEST.md`
- `p0-armnet/README.md` only if needed.

Do not commit downloaded datasets, caches, or environments.

Final report must state:
1. verdict;
2. Gate A result;
3. Gate B result;
4. Gate C classification;
5. key content-only vs content+length metrics;
6. key bimanual metrics;
7. ranking/calibration consequence versus human outcomes;
8. novelty distinction from RoboMeter;
9. new downloaded bytes;
10. GPU/simulator/video usage;
11. files changed;
12. full commit SHA;
13. confirmation remote main equals that SHA.

Stop after the P0.5 verdict.
