# Experiment Plan — CAEA score-identifiability and cloned-state pilot

## Execution status
NOT EXECUTED — discovery only. Do not install runtimes or launch experiments from this report.

## Gate 0: score identifiability
Verify that the frozen state-only BC-RNN provides a candidate-action preference score at a fixed observation/history. If not, stop with `NO CANDIDATE`.

## Minimum pilot
Tasks: Lift and Can. Seeds: 3. Held-out cloned states: 30–50 per task. Candidate actions: policy action plus 4–8 equal-radius, balanced, contact-safe perturbations. Horizon: 5–10 steps, preregistered. Each candidate runs from an independently restored wrapper-level state in a fresh subprocess with common RNG conditions.

## Metrics
Primary: rank correlation between policy preference and measured successor value; top-1 causal regret; failure-onset lead time. Secondary: contact validity, task-progress delta, and calibration-stratified curves.

## Controls
Random ranking, nearest-demonstration/distance ranking, ordinary learned next-state predictor, transition-surprise ranking, contrastive/action-conditioned representation similarity, adaptive recurrent-memory baseline, and CMA-style history swap diagnostic. Report action-distance and contact-feature residuals.

## Decision rule
Positive only if alignment and failure lead-time improvements survive equal-radius, distance/contact, task, and seed controls. Null means policy score has no local causal relation despite unchanged task success. Negative means one-task-only, horizon/tolerance fragile, or fully explained by distance/contact/next-state/surprise; abandon without tuning or renaming.

## Cost and risk
CPU MuJoCo; approximately 1–3 days including instrumentation and analysis; under 5 GB artifacts. Main risk is score non-identifiability or metric-only framing. Existing native and wrapper state-closure infrastructure is sufficient if the gate passes.
