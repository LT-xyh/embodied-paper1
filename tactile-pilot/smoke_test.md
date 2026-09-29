# Smoke test

The one-episode smoke test passed before multi-seed training.

- Loader decoded Camera1/Camera2 and trajectory rows.
- Example episode: 179 next-step samples, 199 input features for vision/proprio, 7 action targets.
- Test episode contact stratification produced 16 contact samples.
- A two-iteration MLP fit and evaluation returned finite `(179, 7)` predictions.
- The smoke test used no GPU, simulator, or physical hardware and is not scientific evidence.
- Full pilot configuration is frozen in `pilot_config.json`.
