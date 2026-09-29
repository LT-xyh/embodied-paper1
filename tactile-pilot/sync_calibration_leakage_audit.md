# Dataset and synchronization audit

- Episodes audited: 44; synchronization-qualified episodes used for training: 35; tasks: ['Stamp', 'UsbPlug', 'FragileCup'].
- Episodes with trajectory/video span mismatch above 1.5% are excluded before model fitting and listed in `split_manifest.json`.
- CSV action columns: TCP position (3), Euler orientation (3), gripper distance (1).
- Decoded Camera1 is the visuo-tactile stream; Camera2 is the scene/wrist visual stream.
- All checked videos are 640x480 RGB at 30 fps; qualified trajectory timestamps match video duration within tolerance.
- Pairing uses same-index frames and trajectory rows after exact count check; any mismatch is recorded in `dataset_audit.json`.
- Contact is frozen before training as tactile Camera1 mean absolute pixel change from the first frame > 0.012, sustained for 3 frames. This is an evaluation stratification proxy, not an input label or ground-truth force/contact sensor.
- Primary split is complete-episode 75/25 within each task. Secondary split holds out all FragileCup episodes as a task shift.
- Trajectory hashes and per-episode frame counts are in `dataset_audit.json`; split membership is in `split_manifest.json`.

## Leakage checks

No qualified episode is present in both primary train and test. All frames from an episode remain together. Camera calibration metadata is not supplied as a model feature. Task and episode identifiers are not supplied as model features. Near-duplicate detection is limited to exact trajectory-file hashes at this stage; any duplicate hash across split would block training.
