# Structural-reset independent review (Paper-1)

- Reviewer thread: `/root/structural_reset_review`
- Runtime model: Codex GPT-6 family (exact deployment identifier unavailable in-agent context)
- Reasoning setting: default/medium (no explicit override)
- Scope: literature-grounded structural review only; no implementation or experiments run.
- Date: 2026-09-28

## A — Context-Causal BC

**Verdict: CAUTION; eligible only for a tightly scoped minimum pilot after tightening.**

Closest overlaps include [CARoL (RA-L 2025)](https://arxiv.org/abs/2506.07006), which infers context from state transitions for adaptation, and [Dynamics as Prompts](https://arxiv.org/abs/2410.20357), which uses interaction history for dynamics system identification and sim-to-real adaptation. History-conditioned/recurrent BC and domain randomization are standard.

The defensible non-overlap is an imitation-learning setting with an explicit intervention that independently swaps visual texture while holding dynamics fixed, plus crossed texture/dynamics evaluation. This asks whether transfer gains require causally identifiable dynamics context rather than texture-correlated context. It is an evaluation/causal-audit delta, not a new context-encoder mechanism.

Identifiability risks: probe-free decoding is still an auxiliary readout and may reward texture leakage; held-out dynamics decoding does not show that the policy uses causal context; rendering and transition cues can remain confounded; a self-supervised system-ID target can make the result tautological.

Cheapest kill: train the context encoder under randomized dynamics and independent nuisance; test held-out dynamics decoding and policy success on the 2x2 crossed texture x dynamics matrix, with texture-only/context-only and recurrent-BC/no-auxiliary controls. Kill if decoding survives swaps but transfer gain disappears, or if recurrent BC/no-auxiliary matches it.

Strongest objection: known auxiliary system-ID plus BC, with novelty resting mainly on the audit. It needs strict interventions, multiple tasks/seeds, and controls to be publishable. Feasibility is moderate in `/tmp/aris_p0_env` (robosuite 1.5.2, MuJoCo 3.3.0, Torch 2.5.1), but missing robomimic/torchvision should not trigger infrastructure repair.

## B — Action-Affordance Representation Geometry

**Verdict: ZERO for Paper-1 (at most a diagnostic pilot).**

The proposal overlaps predictive/action-conditioned visual representations, including [VPP (ICML 2025)](https://arxiv.org/abs/2412.14803), [FRAM](https://arxiv.org/abs/2609.30965), R3M/VC-1 affordance features, and newer action-model representation evaluations. The delta is a post-hoc scalar comparing feature change on executed transitions with matched nuisance change, then correlating the score with frozen linear-policy transfer.

Identifiability is weak: nuisance matching, temporal distance, camera motion, feature scale, whitening, and encoder choice can dominate. Correlation with transfer does not establish causal predictive value. Cheapest kill: preregister the score, whiten/normalize features, and evaluate across encoders/tasks; kill if rank correlation fails to beat linear-probe accuracy consistently or changes under normalization/matching. Strongest objection: an incremental, cherry-pickable benchmark metric with no new loss or mechanism and uncertain cross-task generalization.

## C — Reset-Distribution Policy Ranking

**Verdict: ZERO.**

Stratified resets, paired bootstrap, coverage curves, and phase/outcome metrics overlap existing best-practice guidance, MESA-style evaluation, LIBERO-Plus/robustness suites, and evaluation papers. Any delta is a reproducibility audit of ranking stability, not a new mechanism or falsifiable scientific explanation.

The measurements mainly expose sampling variance and depend on the chosen reset support; no causal hypothesis is identified. Cheapest kill: literature check plus a small repeated-reset replication; likely confirms known instability without a novel result. Strongest objection: benchmark-only and incremental, with no model insight.

## Final routing

Only A proceeds to a narrowly scoped **CAUTION** minimum pilot. B and C are **ZERO/ABANDON** for Paper-1.
