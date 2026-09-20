# ArmnetBench P0-A Artifact Truth Audit

Audit date: 2026-09-20. Primary sources: the [official dataset card](https://huggingface.co/datasets/armnet/armnetbench_v01_lerobot_so101), the [ArmnetBench release site](https://armnet-dev.github.io/armnetbench-v0.1/), and [arXiv:2607.24481](https://arxiv.org/abs/2607.24481). The checked revision was `main` at the audit time. Only the non-video `data/` and `meta/` files were downloaded.

## Download and schema boundary

The Hugging Face tree contained 124 non-video files in the selected `data/` and `meta/` paths. The downloader verified every file against the API-declared size and SHA-256 manifest. The exact dataset bytes written were **57,647,719**. No path beginning with `videos/` was requested or written. The public card reports a 60.6 GB total release because it includes video; that release was not downloaded.

`meta/info.json` reports LeRobot v3.0, 20 FPS, 2,499 episodes, 1,127,881 frames, 8 tasks, the single-arm `so-101` robot type, and the data/video path templates. `meta/episodes/chunk-000/file-000.parquet` contains 2,499 episode rows. The 120 files under `data/chunk-000/` contain the frame rows. `meta/tasks.parquet` maps the eight task indices to canonical task strings.

## Published fields actually inspected

| Requested field | Exact released path and key | Granularity | Directly released? | Audit finding |
|---|---|---|---|---|
| `success` | `meta/episodes/chunk-000/file-000.parquet:success` | episode | yes, `int64` | 0/1 strict-success flag |
| `success_class` | `meta/episodes/chunk-000/file-000.parquet:success_class` | episode | yes, string | `successful`, `failure`, or `suboptimal` |
| `success_cutoff_time` | no Parquet/JSON key in the checked `data/` or `meta/` files | episode/documentation | no | Mentioned in the card's processing notes, not released as a value |
| episode length / frame count | `meta/episodes/...:length`; `data/...:frame_index` | episode and frame | yes | Metadata length exactly matched counted frame rows for all 2,499 episodes; `frame_index` ended at `length - 1` |
| `task` | `meta/episodes/...:tasks`; `meta/tasks.parquet:task`; frame `task_index` | episode and frame | yes | Episode task list plus explicit task-index mapping |
| policy identity | `meta/episodes/...:policy_repo_id` | episode | yes | Evaluated policy repository string; empty for teleoperation per the card |
| policy type | `meta/episodes/...:policy_type` | episode | yes | Seven learned types plus `teleoperated` |
| embodiment identity | `meta/info.json:robot_type` | dataset | yes | `so-101`; no per-episode embodiment column |
| source repository identity | no released source-rollout repository key | — | no | `policy_repo_id` identifies the evaluated model, not the original rollout recording |
| source episode index / equivalent provenance | released `episode_index`, `dataset_from_index`, `dataset_to_index` | release/data index | partial only | These are release-local indices; no original source-recording ID or deterministic source link was released |
| `next.reward` | `data/chunk-000/file-*.parquet:next.reward` | frame | yes, `float32` | Sparse terminal reward; the checked sum was 1 only for strict successes and 0 otherwise |
| `next.done` | `data/chunk-000/file-*.parquet:next.done` | frame | yes, `bool` | Exactly one true terminal per episode, always on the final frame |
| action | `data/chunk-000/file-*.parquet:action` | frame | yes, `float32[6]` | Six commanded joint positions |
| robot state | `data/chunk-000/file-*.parquet:observation.state` | frame | yes, `float32[6]` | Six joint-position channels |

The data-card schema also exposes three camera streams, but none was read by P0. The official card documents that successful and suboptimal episodes with a labelled `success_cutoff_time` are end-trimmed to remove trailing idle frames, while policy rollouts receive human outcome labels. It separately states that teleoperation episodes are always `successful` and `success=1`. The release does not provide the cutoff value itself.

## Outcome and confound audit

The full single-arm table has 2,499 episodes: 400 teleoperation and 2,099 learned-policy rollouts. The learned-only population has 1,532 `failure`, 515 `successful`, and 52 `suboptimal` episodes. The 2,099 learned episodes span all eight tasks and seven learned policy types. There are 46 meaningful `task × policy_type` strata containing both strict-success and non-success outcomes; exact counts for every stratum are in `results.json`.

The primary P0-B population therefore excludes teleoperation and uses the documented learned-policy labels. No simulator, policy checkpoint, VLA inference, image feature, GPU/DCU job, or video was needed.

## Pre-trim recoverability

**Recoverability: NONE.** The release has a release-local episode index and evaluated-policy repository/type, but no original source repository/recording ID, no original untrimmed trajectory, and no released cutoff value. The public documentation establishes an outcome-dependent release-processing rule, but the checked artifact cannot deterministically reconstruct the pre-trim counterfactual. P0 therefore cannot support a causal post-processing claim; its maximum interpretation is a released-support leakage association.

## P0-A decision

P0-A **passes**. All six hard-kill checks are avoided: task/policy/outcome/length are identifiable; learned rollouts are separable from teleoperation; outcome-dependent trimming is documented in the primary release card; no video or simulator is needed; the non-video download is 57,647,719 bytes; and 46 controlled strata contain both outcome classes. The provenance limitation is recorded as `NONE`, so the strongest possible final level is Level 1.
