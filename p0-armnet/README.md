# ArmnetBench bounded P0

This directory contains the reproducible, CPU-only P0 audit authorized by `idea-stage/ARMNET_P0_ADMISSION.md`. It is a release-support leakage test, not a candidate method implementation.

## Reproduction

1. Create an external temporary data directory. Do not place it in Git:

   ```bash
   DATA_ROOT=$(mktemp -d /tmp/armnet-p0-data.XXXXXX)
   ```

2. Download only the non-video `data/` and `meta/` files and verify the manifest. The committed downloader refuses `videos/` paths and checks the API-declared size:

   ```bash
   python3 -m venv /tmp/armnet-p0-venv
   /tmp/armnet-p0-venv/bin/pip install --target /tmp/armnet-p0-site pyarrow
   PYTHONPATH=/tmp/armnet-p0-site python3 p0-armnet/download_nonvideo.py --root "$DATA_ROOT"
   ```

   At the 2026-09-20 audit, this produced 124 files and exactly 57,647,719 bytes. The downloaded root contains `DOWNLOAD_MANIFEST.json`; it must not be committed.

3. Run the analysis:

   ```bash
   PYTHONPATH=/tmp/armnet-p0-site python3 p0-armnet/analysis.py \
     --data-root "$DATA_ROOT" --out-dir p0-armnet
   ```

The script reads episode metadata and state/action Parquet only. It excludes `policy_type=teleoperated`, checks frame lengths and terminal fields, reports within-task/policy horizon effects, runs length-only/non-length/length-augmented CPU logistic baselines, evaluates equal-duration prefixes at 100 and 200 frames, and reports cross-held-out task/policy results. If the first-order test is real, it also computes cross-fitted learned-evaluator policy scores; it never runs a policy or simulator.

## Reproducibility boundary

The release documents outcome-dependent trimming but does not release `success_cutoff_time` values or a deterministic source link to original untrimmed recordings. Results therefore support at most **P0 SURVIVES — LEVEL 1** (released-support leakage), never a causal post-processing claim. The human-labelled ArmnetBench leaderboard is not modified or recomputed as ground truth.
