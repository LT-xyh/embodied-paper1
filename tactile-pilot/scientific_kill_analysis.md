# Scientific kill analysis

The frozen H1 required a consistent tactile improvement over the matched vision/proprio baseline during contact, a weaker benefit outside contact, loss of the effect under shuffled tactile, and survival of leakage/synchronization audits.

## Synchronization correction

The first same-index run was invalidated before interpreting its metrics because nine episodes had trajectory/video duration ratios above the frozen 1.5% synchronization tolerance. Those raw metrics remain under `invalid_sync_run/` and are not scientific evidence. The corrected run excluded those episodes using only the data-integrity audit, before rerunning the models.

## Observed evidence from the corrected run

- Primary episode-disjoint split: genuine tactile contact MAE was worse than baseline for all three seeds (+0.0879, +0.0803, +0.1751; lower is better).
- Primary split non-contact MAE was also worse (+0.1314, +0.0617, +0.0785).
- Primary genuine tactile therefore has no positive contact benefit and no contact-specific advantage.
- Shuffled tactile was substantially worse than baseline, so tactile correspondence affects the predictor, but this does not imply useful information or support H1.
- Task-heldout results were unstable across seeds; genuine and shuffled tactile were nearly indistinguishable in the first two seeds and both failed to provide a stable contact-conditioned effect.

## Decision boundary

The frozen H1 is not supported by the corrected minimum pilot. The result is recorded as negative evidence. No architecture, split, contact threshold, epoch count, or metric was changed after seeing the corrected result, and no larger run is authorized to rescue it.
