# Independent problem-space review

Date: 2026-09-29  
Reviewer model: `gpt-6-astra`  
Reasoning: `medium`  
Reviewer thread: `/root/problem_space_reviewer`  
Scope: problem-space assessment only; no implementation, downloads, training, or experiments.

## Ranking

1. **Contact-rich tactile and physical grounding** — strongest conditional space.
2. **Cross-embodiment execution gap** — important but more crowded and more expensive.
3. **Reliable test-time adaptation for VLA deployment** — important but has the highest direct-prior and runtime risk.

## Review

### Contact-rich tactile and physical grounding

Importance is high because material and contact-state shifts are deployment-critical and are poorly represented by vision alone. RCT provides 29,279 tactile frames from 122 materials and three DIGIT sensors with contact-sequence and material-held-out protocols; its results expose severe frame-split leakage and low held-out-material retrieval. HapTile, TVL, ViTacWorld, PRISM, and ForeTac-VLA cover sensors, data collection, and reactive or predictive tactile fusion. The remaining defensible question is behavioral: does predicting future contact add generalization beyond reactive tactile fusion under held-out materials and contact sequences?

Saturation is medium-high and direct collision is medium. Generic tactile fusion, a new tactile encoder, or a new sensor would collide with recent work. A frozen-encoder or small-head study remains plausible if the public data expose an action or contact-state behavior proxy. The cheapest falsification is a schema audit followed by a three-seed held-out-material/held-out-sequence comparison between current-frame, short-history, and future-contact representations. Kill the space if no behavior proxy exists or if future prediction gives no robust gain across material draws. A negative result would establish that predictive contact modeling is unnecessary under a leakage-controlled protocol.

### Cross-embodiment execution gap

Importance is very high. The Embodiment Gap survey separates reusable semantics/perception, interfaces/data, and cross-embodiment correspondence, and recommends reporting adaptation effort rather than success alone. Learning Action Priors, Being-H0.5, CEI, OpenVLA, and OXE-AugE already establish strong cross-embodiment mechanisms. The remaining question is causal attribution: can visual appearance, action parameterization, kinematics/gripper, and adaptation cost be independently separated?

Generic scorecards are saturated. A factorial intervention study could remain novel, but public OXE-AugE is approximately 1 TB and actual interface/calibration differences are difficult to reproduce. The cheapest falsification is a small frozen-policy simulation study with matched visual, action-interface, and kinematic perturbations; kill if effects cannot be independently manipulated or reduce to known embodiment ordering. Negative results would show that public logs cannot identify the source of the embodiment gap.

### Reliable test-time adaptation and continual VLA deployment

Importance is high, but the direct-prior risk is highest. VANE isolates candidate updates and commits them only when future visual evidence supports them; RoboTTT establishes fast-weight context scaling and reports large long-horizon gains; FlowDAgger provides few-shot latent-space correction while freezing the base policy; ADPro and related work cover adjacent adaptation. The remaining question is when unlabeled interaction improves a policy without forgetting, temporal contamination, or adapting to a shortcut.

The cheapest falsification is offline stream replay with strict pre/post windows, comparing no adaptation, batch adaptation, and reversible candidate updates on more than one task or embodiment. Kill if only a VANE-like gate wins or gains disappear outside one stream. The space is feasible only with a small checkpoint and a mature simulator; modern VLA adaptation stacks may exceed the 1–3 day and DCU constraints.

The reviewer recommends tactile/physical grounding first, conditional on a behavior-level proxy; otherwise all three spaces should be rejected rather than rescued by a new method name.
