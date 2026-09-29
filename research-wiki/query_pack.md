# Research Wiki Query Pack

_Auto-generated. Do not edit._

## Project Direction
**Problem**

Select a new Paper-1 research direction in Embodied AI / Robot Learning.

The primary objective is the fastest credible path to a publishable paper, rather than continuation of existing engineering work.

**Background**

A previous ShiftVLA / ReplayVLA direction investigated persistent effects of closed-loop observation corruption in VLA policies.

The scientific hypothesis was NOT falsified.

The route was paused because LIBERO runtime, provenance and bootstrap integration consumed excessive engineering effort before scientific validation could begin.

Treat this as an engineering-risk lesson, not as scientific evidence against VLA or robustness research.

Do NOT automatically continue ReplayVLA.

Existing ShiftVLA code may be reused only when reuse materially shortens the newly selected scientific route.

**Non-goals**

For Paper-1, do not prioritize:

* training a foundation VLA from scratch;
* real-robot-only research;
* low-level systems optimization as the main scientific contribution;
* new CUDA kernel engineering;
* simulator infrastructure as the main contribution;
* continuing ReplayVLA solely because existing code already exists.
## Failed Ideas (avoid repeating)
- **Action-affordance representation geometry**:
- **Outcome-dependent censoring in ArmnetBench**:
- **ASCC action-swap auxiliary supervision**:
- **Support-corrected bounded behavior cloning**:
- **CAEA candidate-action preference**:
- **Reset-distribution policy ranking**:
- **Rater-context interaction in social navigation preferences**:
- **Temporal Consequence Inversion**:
- **Transition-surprise-triggered recurrent reset**:
## Key Papers (24 total)
- [paper:alian2026_haptile_hapticinformed_visiontactilelanguageaction] HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning: Prior work relevant to the current VLA problem-space map; exact thesis to be refined from metadata and paper evidence.
- [paper:chen2026_worldecho_robotic_world] WorldEcho: Do Robotic World Models Really Follow Actions?: Prior work relevant to the current VLA problem-space map; exact thesis to be refined from metadata and paper evidence.
- [paper:domae2026_embodiment_gap_robot] The Embodiment Gap in Robot Foundation Models: Prior work relevant to the current VLA problem-space map; exact thesis to be refined from metadata and paper evidence.
- [paper:fan2025_longvla_unleashing_longhorizon] Long-VLA: Unleashing Long-Horizon Capability of Vision Language Action Model for Robot Manipulation: Prior work relevant to the current VLA problem-space map; exact thesis to be refined from metadata and paper evidence.
- [paper:gao2026_gated_memory_policy] Gated Memory Policy: Prior work relevant to the current VLA problem-space map; exact thesis to be refined from metadata and paper evidence.
- [paper:he2026_rct_robotcollected_touchvisionlanguage] RCT: A Robot-Collected Touch–Vision–Language Dataset for Tactile Generalization: Prior work relevant to the current VLA problem-space map; exact thesis to be refined from metadata and paper evidence.
- [paper:hu2025_carol_contextaware_adaptation] CARoL: Context-aware Adaptation for Robot Learning: Prior work relevant to the current VLA problem-space map; exact thesis to be refined from metadata and paper evidence.
- [paper:ji2026_vane_reliable_testtime] VANE: Reliable Test-Time Training for Vision-Language-Action Models: Prior work relevant to the current VLA problem-sp
## Recent Relationships (10 total)
  idea:ascc_action_swap_auxiliary --inspired_by--> paper:quevedo2025_worldgym_world_model
  idea:caea_score_identifiability --inspired_by--> paper:quevedo2025_worldgym_world_model
  idea:transition_surprise_reset --inspired_by--> paper:gao2026_gated_memory_policy
  idea:context_causal_bc --inspired_by--> paper:hu2025_carol
  idea:armnet_censoring --inspired_by--> paper:selvaraj2026_armnetbench_benchmark
  idea:armnet_censoring --tested_by--> exp:armnet-p0.5
  idea:tci_temporal_consequence_inversion --tested_by--> exp:tci-bcrnn-gate
  idea:caea_score_identifiability --tested_by--> exp:caea-score-gate
  idea:tci_temporal_consequence_inversion --tested_by--> exp:tci-identifiability
  idea:transition_surprise_reset --tested_by--> exp:transition-p0-runtime
