# ArmnetBench P0.5 paper-admission result

**Verdict: PIVOT**

Date: 2026-09-21. Effort: balanced. Assurance: draft.

Binding authority: `idea-stage/ARMNET_P05_GENERALIZATION_ADMISSION.md`, read together with `AGENTS.md`, `RESEARCH_BRIEF.md`, and `idea-stage/ARMNET_P0_RESULT.md`.

## Synchronization and execution boundary

The initial working tree was clean. `git pull --ff-only` fast-forwarded local `main`, and local HEAD and authoritative remote `main` both equalled `286827ac8ad655735e4ffdaa31a5b3e85a27b581` before research edits.

This bounded run reused the single-arm non-video cache and existing NumPy/PyArrow installation. It trained only small CPU logistic probes. No GPU/DCU, simulator, video, VLA inference, checkpoint, new runtime installation, or real robot was used. No candidate method or paper-scale implementation is admitted.

**Execution deviation:** the initial combined analysis script downloaded and computed the bimanual comparison before formally adjudicating Gate A. This did not respect the authority's sequential gate requirement. Those results are disclosed below as prematurely computed internal evidence, not as proof of compliant gate progression. Once the hard-kill evidence was reviewed, no Gate C search or additional scientific scope was opened. Subsequent computation only corrected output completeness, literal log(length), and Kendall tau-a accounting, and completed required bootstrap reporting for the same bounded comparisons.

## Representation and analysis

Each complete released state/action sequence is linearly interpolated at K=32 equally spaced normalized-time positions. This yields 384 features for single-arm and 768 for bimanual. Content-only receives no frame count, duration, padding mask, original frame index, terminal reward, terminal flag, or outcome field. The matched augmented probe adds natural log(frame count). Feature means/scales are fitted separately in each training fold.

Both probes use the same L2 logistic objective (penalty 0.002), 650 full-batch gradient steps, learning rate 0.14, threshold 0.5, and no hyperparameter search. Held-out grouping is task or learned `policy_type` (seven policy families, not necessarily unique checkpoints). Human ground truth is `success_class == successful`; failure and suboptimal are negative. Teleoperation is excluded. Full released content retains endpoint pose and motion shape, so this is removal of the explicit duration channel, not proof that all duration information is absent from content.

Brier-difference intervals use 1,000 paired cluster resamples of fixed out-of-fold predictions: task clusters for leave-task-out, policy-family clusters for leave-policy-out. Policy ranking uses mean leave-task-out predictions, compared with strict-human-success means on the same episodes. Ranking intervals resample task clusters 1,000 times. They do not refit models and are not causal or deployment-shift intervals. Permutation is one seeded shuffle of log length within each task × policy family, with content and labels unchanged; it is a diagnostic control, not a calibrated permutation significance test. No equal-prefix evidence is used.

## Gate A — support association survives, paper admission fails

Population: 2,099 learned episodes, eight tasks, seven policy families. All 46 mixed task × policy strata have shorter **mean** successful trajectories. The success-oriented negative standardized-horizon AUC is 0.900620; raw positive-horizon AUC is 0.099380. The shuffled raw-horizon AUC is 0.498146. Thus the within-stratum association remains.

| Split | Feature condition | AUC | Balanced accuracy | Brier | ECE (10 bins) |
|---|---|---:|---:|---:|---:|
| Leave-task-out | Content only | 0.938574 | 0.837395 | 0.075394 | 0.037384 |
| Leave-task-out | Content + log length | 0.952395 | 0.862274 | 0.066286 | 0.031635 |
| Leave-policy-out | Content only | 0.962832 | 0.922928 | 0.051749 | 0.022986 |
| Leave-policy-out | Content + log length | 0.967169 | 0.926739 | 0.047554 | 0.019220 |

Adding length reduces Brier by 0.009108 (task-cluster 95% interval [0.003256, 0.018666]) and 0.004195 (policy-cluster interval [0.001405, 0.007502]). The within-stratum shuffled-length model gives leave-task AUC 0.940089 and Brier 0.074321, so it does not reproduce the full single-arm gain.

However, content-only already matches the seven-policy human ordering: Spearman 1.000000, Kendall tau-a 1.000000, zero disagreements among 21 pairs. Adding length swaps only pi0 and grootn1.7: Spearman 0.964286, tau-a 0.904762, one disagreement. Their augmented evaluator means are extremely close. Task-cluster Spearman intervals are [0.678571, 1.000000] versus [0.750000, 1.000000]; disagreement intervals are [0, 5] versus [0, 4]. These broad, overlapping marginal intervals do not establish stable ranking harm, nor are they a paired significance test. Calibration improves against released human labels rather than revealing a deployment failure.

The statistical support-channel subtest passes, but the stronger paper-admission claim fails: a robust downstream distortion beyond a known length proxy is not established. The authority explicitly kills weak/inconsistent ranking/calibration consequences or a reduction to that known issue.

## Gate B — prematurely computed internal evidence; insufficient replication

The non-video bimanual tree was verified as 64 files / 64,351,279 bytes, below 100 MB. It contains 1,219 episodes, including 200 teleoperated episodes excluded from probes, and 1,019 learned episodes across four tasks. There are 209 strict successes, 756 failures, and 54 suboptimal outcomes. All recorded metadata lengths match frame counts; terminal flags and reward checks have no mismatches. State/action has 24 combined channels.

The shared Armnet outcome-dependent trimming rule is the documented mechanism under examination; this run does not recover pre-trim trajectories or per-episode cutoff values. The released artifacts alone cannot identify how much of the observed length association is due to trimming rather than genuine completion speed. Bimanual remains internal replication of the same collection/release pipeline.

| Split | Feature condition | AUC | Balanced accuracy | Brier | ECE (10 bins) |
|---|---|---:|---:|---:|---:|
| Leave-task-out | Content only | 0.715931 | 0.559894 | 0.204737 | 0.196019 |
| Leave-task-out | Content + log length | 0.721413 | 0.566531 | 0.201371 | 0.193324 |
| Leave-policy-out | Content only | 0.924455 | 0.829689 | 0.093805 | 0.053839 |
| Leave-policy-out | Content + log length | 0.925731 | 0.830306 | 0.092937 | 0.052448 |

All 25 mixed strata have shorter mean successful trajectories; negative standardized-horizon AUC is 0.857745 (raw positive-horizon 0.142255; shuffled raw-horizon 0.472275). The association replicates, but the consequential evaluator effect does not.

Leave-task Brier gain is only 0.003367, interval [-0.000144, 0.008471]; leave-policy gain is 0.000868, interval [0.000375, 0.001497]. The shuffled-length model achieves Brier 0.200877 and AUC 0.719954, reproducing the small calibration gain at least as well as real length. With only four tasks, uncertainty is substantial. Both models produce exactly the same policy order: Spearman 0.392857, tau-a 0.333333, seven disagreements against human outcomes. The existing poor ordering is not attributable to adding length in this comparison.

**Gate B does not support admission:** the first-order horizon association is consistent, but the stronger ranking/calibration mechanism fails to replicate. It cannot justify opening Gate C.

## Gate C and novelty

**Classification: NONE — not entered after hard kill.** This is a run disposition, not evidence that no independent dataset exists. The required search-status artifact explicitly lists the conditional checks as not executed. Independent dataset bytes: zero.

The binding authority states that RoboMeter already acknowledges length as a quality proxy and fixes compared trajectories to equal T to prevent its use. The strongest proposed distinction would be a documented outcome-conditioned construction mechanism causing evaluator deployment mismatch and robust policy-ranking distortion beyond one pipeline. This run establishes neither a pre-trim causal counterfactual nor independent generalization, and the only observed single-arm rank swap is weak. Time normalization retains full released endpoint content and is a cleaner control than equal-prefix truncation, but that control alone is not a new scientific mechanism.

A skeptical CoRL/ICRA/RA-L reviewer could reasonably regard the surviving result as Armnet-specific preprocessing QA plus known length-proxy behavior. It is insufficient for Paper-1 admission. **PIVOT; stop this direction at P0.5.**

## Download accounting and reproduction

Exact new dataset artifact payload: **64,351,279 bytes**, all bimanual `data/` and `meta/`; no independent artifact, video, or checkpoint. Reused single-arm payload: 57,647,719 bytes, not a new download. HTTP headers, API tree responses, and transport overhead are not included in artifact payload accounting; exact network-wire bytes were not instrumented. No claim of an exact all-network byte total is made.

Downloaded manifests were retained outside Git. SHA-256 of single-arm `DOWNLOAD_MANIFEST.json`: `90d346ff21aa2e7f459781b92e884190853a3e6ad50864da68cbb078fefc6253`; bimanual: `c365dc4bea41f621b6409f365106123076434cf2a1b634736f24209f73dcfd56`. Data were resolved at mutable `main`, so a future download must verify its own manifest; this run does not claim an immutable upstream revision. The script does not perform downloads.

Using the existing external caches and dependencies, the recorded numerical comparison is reproduced by:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=/tmp/armnet-p0-site \
  python3 p0-armnet/p05_analysis.py \
  --single-root "$(cat /tmp/armnet-p0-data.path)" \
  --bimanual-root "$(cat /tmp/armnet-p05-bimanual-data.path)" \
  --out-dir p0-armnet
```

This command reproduces already-computed comparisons; it is not authorization to repeat or extend research after PIVOT. The bimanual flag is optional and should only be used when the gate is authorized. Generated outputs contain all fold metrics, stratum summaries, human-policy comparisons, and cluster intervals. NumPy floating-point reductions may differ at roundoff scale across CPU/BLAS configurations.

Files in this result commit: `p0-armnet/p05_analysis.py`, `p0-armnet/p05_results.json`, `p0-armnet/p05_results.md`, `p0-armnet/p05_replication_search.md`, `idea-stage/ARMNET_P05_RESULT.md`, and `MANIFEST.md`. No data, caches, or environment are committed.
