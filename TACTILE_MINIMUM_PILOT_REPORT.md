# Minimum Tactile Scientific Pilot Report

Date: 2026-09-29
Branch: `p0/tactile-minimum-pilot`
Final verdict pending independent artifact review: **FAIL — MINIMUM TACTILE SCIENTIFIC PILOT**

## Scope and resource accounting

The pilot tested the frozen hypothesis on a predeclared FreeTacMan subset. It downloaded 192,054,263 bytes across 138 files from the pinned dataset revision, used no simulator, GPU, physical hardware, or full 50 GB release, and installed only a local CPU Python environment with imageio/imageio-ffmpeg/scikit-learn.

The downloaded subset contains 44 complete episodes from Stamp, UsbPlug, and FragileCup. Camera1 is the decoded visuo-tactile stream; Camera2 is the scene/wrist vision stream. Trajectories contain TCP position, Euler orientation, and gripper distance. All videos are 30 fps with zero frame-count mismatches. A data-only synchronization audit found nine episodes whose trajectory/video duration ratio exceeded 1.5%; they were excluded before the corrected training run and are listed in `split_manifest.json`. The corrected qualified set contains 35 episodes.

## Frozen protocol

The target is the next-step delta of the seven action channels. Inputs are 8x8 RGB visual features plus seven proprioceptive channels, optionally concatenated with 8x8 RGB tactile features. The model is a matched small `sklearn` MLPRegressor with one hidden layer of 32 units, Adam, 35 iterations, and seeds 0, 1, 2. Conditions are:

1. vision/proprioception;
2. vision/proprioception plus genuine tactile;
3. vision/proprioception plus shuffled tactile.

Contact is frozen before model fitting as a tactile Camera1 mean absolute pixel change from the first frame above 0.012, sustained for three frames. It is an evaluation stratification proxy, not an input label or force ground truth. Primary split is complete-episode 75/25 within task; secondary split holds out all FragileCup episodes as a task shift.

## Results

The first same-index run is preserved under `tactile-pilot/invalid_sync_run/` and is not scientific evidence because of the duration mismatch. The corrected qualified-set run is the decisive minimum result. Lower MAE is better.

| split | seed | baseline contact MAE | genuine tactile contact MAE | genuine Δ | shuffled tactile contact MAE |
|---|---:|---:|---:|---:|---:|
| primary | 0 | 0.0896 | 0.1775 | +0.0879 | 0.5485 |
| primary | 1 | 0.0879 | 0.1682 | +0.0803 | 0.4056 |
| primary | 2 | 0.0641 | 0.2392 | +0.1751 | 0.4796 |

Genuine tactile also worsened primary non-contact MAE by +0.1314, +0.0617, and +0.0785. The shuffled control was substantially worse than baseline, showing that the tactile stream is not an inert extra dimension, but it does not establish a useful contact-conditioned gain. The task-heldout split was unstable across seeds; genuine and shuffled tactile were close in all three seeds and had no consistent contact-specific advantage.

## Frozen-hypothesis decision

H1 requires a reproducible positive contact-phase improvement. The primary split fails that requirement in all three seeds. The effect is not a contact-localized gain, and the task-heldout result is not stable. Therefore the pilot does not support the claim that synchronized tactile information improves held-out action prediction during contact phases in this proxy. The final scientific verdict is `FAIL — MINIMUM TACTILE SCIENTIFIC PILOT`.

This is an offline behavioral-proxy result only. It says nothing about closed-loop robot success, causal physical grounding, real-world transfer, or universal tactile usefulness. The negative evidence must not be rescued by larger architectures, extra epochs, contact redefinition, or full-dataset download.

## Audit and artifact index

- Resource pin and URLs: `tactile-pilot/resource_manifest.json`
- Downloaded file hashes and exact bytes: `tactile-pilot/subset_manifest.json`
- Episode/frame/synchronization audit: `tactile-pilot/dataset_audit.json`
- Frozen split: `tactile-pilot/split_manifest.json`
- Synchronization, calibration, and leakage notes: `tactile-pilot/sync_calibration_leakage_audit.md`
- Configuration and smoke gate: `tactile-pilot/pilot_config.json`, `tactile-pilot/smoke_test.md`
- Seed-level raw metrics: `tactile-pilot/seed_level_metrics.json`, `tactile-pilot/training_evaluation_log.jsonl`
- Aggregate deltas: `tactile-pilot/pilot_summary.json`
- Kill analysis: `tactile-pilot/scientific_kill_analysis.md`
- Invalid pre-repair run: `tactile-pilot/invalid_sync_run/`

## Independent review

The requested `gpt-6-astra / medium` reviewer was capacity-unavailable. The actual independent artifact review was performed by `gpt-6-luna / max`, thread `/root/tactile_pilot_reviewer_retry`, with no experiments or downloads. It confirmed the corrected artifacts are mutually consistent and finalized `FAIL — MINIMUM TACTILE SCIENTIFIC PILOT`. A REVISE is allowed only for a concrete technical or measurement defect that preserves the frozen H1; the reviewer found none, and a negative scientific result cannot be converted into REVISE by tuning.
