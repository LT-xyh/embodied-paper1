# Final Prior-Freshness Search

**Gate result: no direct prior meeting the active contract's full four-part match was identified.** The search included StateMem, PredVLA, GMP, AURA-Mem, MILES, ResTacVLA, and close 2026 transition-surprise/context-reset and manipulation-recovery papers. Primary records checked:

- StateMem, *Single-State Residual Memory with Adaptive Inference for Vision-Language-Action Policies* (2026): https://arxiv.org/abs/2609.22684
- PredVLA, *A Sub-Million-Parameter Predictive-Coding Policy for Robot Manipulation* (2026): https://arxiv.org/abs/2608.26673
- GMP, *Gated Memory Policy* (2026): https://arxiv.org/abs/2604.18933
- AURA-Mem (2026): https://arxiv.org/abs/2606.02775
- MILES, *Making Imitation Learning Easy with Self-Supervision* (CoRL 2024): https://arxiv.org/abs/2410.19693
- ResTacVLA (2026): https://arxiv.org/abs/2607.03387
- Rewind-IL (2026): https://arxiv.org/abs/2604.16683
- PATCH, *Action-Chunk-Conditioned Latent Patch Innovation Monitoring for Robot Manipulation* (2026): https://arxiv.org/abs/2606.16690
- Prob-CADT, *Reliable Contexts for Decision Transformers in Stochastic MDPs* (2026): https://openreview.net/pdf?id=YvY0f8aVJP

## Closest collision risk: Prob-CADT

Prob-CADT is the closest transition-surprise/hard-reset method. It predicts the next transition conditioned on Decision Transformer context and action; calibrated surprise above threshold discards old trajectory context and re-anchors on the current observation. Its deterministic-limit D4RL MuJoCo appendix uses squared next-state prediction error. This overlaps strongly with the trigger-plus-hard-context-reset mechanism and rules out any broad claim that prediction-error-triggered context reset is new.

Under the admission authority's specific direct-prior test, however, its reported hard reset is of a Decision Transformer token/history context, not an LSTM hidden/cell state; its reported evaluation is offline RL/stochastic MDP and D4RL locomotion, not robot manipulation/imitation; and its deviation analysis is not the specified injected physical-disturbance recovery test. It matches transition surprise, but does not establish the full combination of recurrent hidden/cell invalidation, manipulation/imitation, and physical disturbance recovery. It is therefore recorded as a **critical cross-domain method neighbor**, not a direct collision under the four-part gate. Primary source: https://openreview.net/pdf?id=YvY0f8aVJP.

## Other close neighbors

- Rewind-IL combines manipulation recovery with clearing policy caches after physical checkpoint respawn, but its TIDE trigger is disagreement between overlapping action-chunk predictions; respawn and restart are coupled. It does not report an observed one-step physical transition residual triggering an isolated BC-RNN hidden/cell reset.
- PATCH uses action-conditioned visual latent-patch innovation during manipulation disturbances, but it preserves policy execution state and resumes the original policy without reset.
- MILES includes an LSTM policy with fixed-cadence hidden-state reset, not residual-event-triggered rollout invalidation.
- StateMem, PredVLA, GMP, AURA-Mem, and ResTacVLA make generic surprise-driven memory update/correction/gating inadmissible as a novelty claim; none in the checked primary records establishes the exact manipulation/imitation disturbance-recovery combination above.

The final independent reviewer was constrained to `gpt-6-luna` with max effort. The conclusion is narrow: **no direct prior found under the active contract; novelty risk remains high because Prob-CADT nearly shares the core trigger/reset abstraction in another policy family and task regime.**
