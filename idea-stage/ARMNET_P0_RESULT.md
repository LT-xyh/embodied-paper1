# ArmnetBench P0 Result

**Final verdict: P0 SURVIVES — LEVEL 1**

ArmnetBench's [official release documentation](https://huggingface.co/datasets/armnet/armnetbench_v01_lerobot_so101) states that learned-policy rollouts receive human `successful`/`failure`/`suboptimal` labels and that successful or suboptimal episodes with a labelled `success_cutoff_time` are end-trimmed. In the released single-arm non-video files, 2,099 learned-policy episodes form 46 mixed `task × policy_type` strata; every one has shorter strict-success episodes, with a median success-minus-non-success difference of -213.65 frames and median absolute standardized difference 3.418. A length-only CPU baseline remains strongly predictive under leave-task-out (AUC 0.933) and leave-policy-out (0.930), while equal-duration prefixes reduce this to 0.562 and 0.656. The learned evaluator comparison changes policy ordering by seven pairwise inversions relative to the full length-augmented evaluator. This is more than a pooled descriptive correlation, but the released artifact has no cutoff values or deterministic source link to the original untrimmed rollout, so the result is a reproducible released-support leakage association rather than a causal post-processing estimate.

## P0-A — artifact truth

The checked `main` release contains 2,499 single-arm episodes, 400 teleoperation episodes, and 2,099 learned-policy episodes. Learned-only labels are 1,532 failures, 515 strict successes, and 52 suboptimal outcomes. The episode table releases `length`, `tasks`, `success`, `success_class`, `policy_repo_id`, and `policy_type`; the frame files release `action`, `observation.state`, `frame_index`, `episode_index`, `task_index`, `next.reward`, and `next.done`. All 2,499 metadata lengths matched counted frame rows; every episode had one final `next.done`; and reward sums matched the strict-success indicator.

`success_cutoff_time` is absent as a released field. The card's processing note is the primary evidence for the trimming semantics. No original source repository/recording identifier, untrimmed trajectory, or cutoff value was found. Pre-trim/cutoff recoverability is therefore **NONE**. The exact field/path audit is in [`p0-armnet/artifact_audit.md`](../p0-armnet/artifact_audit.md).

P0-A passes because task, policy, outcome, and released horizon are identifiable; learned and teleoperated rollouts are separable; the documented trimming rule is primary-source evidence; 46 controlled strata contain both outcome classes; and the non-video artifact is within the download gate. The provenance limitation prevents Level 2.

## P0-B — CPU leakage sanity test

The analysis used only episode metadata and 6-D state/action summary statistics. It excluded teleoperation, image streams, policy checkpoints, simulators, and accelerators. The full cross-held-out results are in [`p0-armnet/results.json`](../p0-armnet/results.json) and [`p0-armnet/results.md`](../p0-armnet/results.md).

| Feature set | Leave-task-out AUC | Leave-policy-out AUC |
|---|---:|---:|
| Length only | 0.9329 | 0.9304 |
| Non-length summary | 0.8061 | 0.8779 |
| Non-length summary + length | 0.9372 | 0.9543 |
| Equal-duration prefix, 100 frames | 0.5622 | 0.6565 |
| Equal-duration prefix, 200 frames | 0.5337 | 0.6885 |

All 46 mixed strata had shorter successes. On the common 100-frame subset, a cross-fitted learned evaluator changed seven pairwise policy orderings when full released features were replaced by equal-duration-prefix features; removing length from full summaries changed four. The official human-labelled leaderboard was used only as a reference and was not altered.

## Authority boundary

Paper-1 implementation is **NO**. No second-dataset replication path was searched for because the authority permits that narrow search only after Level 2; no replication path is established in this run. The bounded result does not authorize method development, video access, simulator work, GPU/DCU jobs, VLA inference, or paper-scale experiments.

Exact dataset bytes written: **57,647,719**. GPU/DCU: **none**. Simulator: **none**. Video: **none**. The lightweight `pyarrow` package was installed only in `/tmp/armnet-p0-site` as permitted by the active authority; no system package or repository runtime was changed.
