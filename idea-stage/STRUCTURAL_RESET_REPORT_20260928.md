# Structural-reset research-direction report

Date: 2026-09-29
Branch: `idea/structural-reset-20260928`
Base evidence: `idea/reideation-20260928` at `c61bd215b6e910faa0975779bfe0d66e97fadb78`

## Verdict

**BLOCKED — BROADER RESEARCH SCOPE REQUIRED**

No candidate reaches `READY FOR MINIMUM SCIENTIFIC PILOT`. The only candidate that survived the structural screen is retained as **CAUTION / unresolved**, because its causal measurement has not passed the required crossed texture–dynamics preflight and its closest mechanisms are already present in context-aware adaptation literature. No scientific pilot, policy training, or full benchmark run was started.

## Why this was a structural reset

The frozen evidence branch rejected action-swap auxiliary supervision, consequence or transition-surprise memory, predictive recurrent-state regularization, CAEA score heuristics, TCI, bounded-action BC, latency changes, gradient routing, and truncated-Gaussian variants. The new search therefore changed at least two axes for every serious candidate: policy object, contribution type, observation or task regime, and evaluation question. Existing MuJoCo and robosuite replay infrastructure was treated as optional evidence rather than as a constraint.

## Landscape map

| Frame | Recent evidence | Open question | Decision |
|---|---|---|---|
| Policy evaluation and diagnostics | WorldGym and WorldEcho study world-model evaluation and action following ([WorldGym](https://arxiv.org/abs/2506.00613), [WorldEcho](https://arxiv.org/abs/2608.24885)); imagined-rollout ranking is itself sensitive to correction schedule ([Do Better Imagined Rollouts Mean Better Robot Control?](https://arxiv.org/abs/2609.02811)) | Which evaluator quantity predicts closed-loop outcomes? | Crowded by the project's accumulated negative evidence; no generic metric candidate retained. |
| Generalization and robustness | [Shortcut Learning in Generalist Robot Policies](https://proceedings.mlr.press/v305/xing25a.html), [UCAG-P](https://arxiv.org/abs/2608.26058), and [GAM](https://arxiv.org/abs/2606.17046) address shortcut or geometry transfer | Can a nuisance intervention identify causal transfer? | Only useful as a control in candidate A; standalone geometry and shortcut metrics rejected. |
| Long-horizon behavior | Scene-graph memory work targets task-relevant long-horizon state ([CVPR 2026 Scene Graphs](https://pengqinhe.github.io/Scene-Graph-CVPR2026-website/)); deployment-time reliability studies runtime coordination ([Deployment-Time Reliability](https://arxiv.org/abs/2603.11400)) | What internal object or phase state is necessary for recovery? | Memory mechanism is crowded and would reopen the excluded recurrent-memory neighborhood. |
| Action chunking and temporal abstraction | Delay-aware diffusion, RAPAC-DP, RACE, SAIL, and GAP are already documented in the frozen Track-A search | Does temporal abstraction fail for a measurable reason? | Direct-prior and loss/routing overlap; rejected. |
| Multimodal grounding and reasoning | [Action-Free Reasoning](https://proceedings.mlr.press/v305/clark25a.html), [IntentVLA](https://arxiv.org/abs/2605.14712), and [In-Context Imitation Learning with Visual Reasoning](https://arxiv.org/abs/2603.07530) use language or visual reasoning traces | When does reasoning improve control rather than narration? | Requires a VLA stack and a separate grounding dataset; no cheap Paper-1 pilot identified. |
| Memory and partial observability, excluding ASCC | [CARoL](https://arxiv.org/abs/2506.07006) and [Dynamics as Prompts](https://arxiv.org/abs/2410.20357) infer context from transitions or interaction history | Is context useful because it identifies dynamics, or because it leaks visual nuisance? | Candidate A isolates this question in imitation, but remains conditional. |
| Data quality and demonstration structure | Data Scaling Laws in Imitation Learning, SIEVE, and physics-based filtering study data quantity or quality | Which data property changes closed-loop behavior? | Generic filtering is accumulated negative evidence; no distinct measurement survived. |
| Failure analysis | [Fail2Progress](https://proceedings.mlr.press/v305/huang25d.html), [Sentinel](https://proceedings.mlr.press/v270/agia25a.html), RoboEXP, and FIDeL study failure or intervention signals | Can failures be assigned to a mechanism with an identifiable counterfactual? | A diagnostic paper could be viable only with a new externally validated benchmark; current candidates lacked that substrate. |
| Embodiment and task transfer | Cross-embodiment policies and embodiment scaling ([Doshi et al.](https://proceedings.mlr.press/v270/doshi25a.html), [Embodiment Scaling](https://proceedings.mlr.press/v305/ai25a.html)) study transfer across bodies | Which representation transfers behaviorally? | Representation geometry candidate B overlaps VPP, FRAM, R3M/VC-1, GAM, and RoboEXP. |
| Representation–behavior relationships | [VPP](https://proceedings.mlr.press/v267/hu25g.html), FRAM, and visual affordance encoders link features to action or future prediction | Does a local action-conditioned geometry score predict policy transfer? | B is a normalization-sensitive post-hoc metric; rejected for Paper-1. |
| Inference-time adaptation | [VANE](https://arxiv.org/abs/2608.09448), [RoboTTT](https://arxiv.org/abs/2607.15275), ADPro, and FlowDAgger adapt at deployment | Which update is safe under future-only evidence? | Strong area, but a new method needs a qualified VLA checkpoint and leakage-safe runtime; no minimum pilot was identifiable here. |
| Evaluation sampling and reset distributions | MESA and current best-practice work ([Robot Learning as an Empirical Science](https://arxiv.org/abs/2409.09491)) address evaluation variance and reproducibility | How stable are rankings under reset support? | Candidate C is benchmark hygiene without a new mechanism or identifiable scientific claim. |

The landscape leaves one conditional gap: context-aware adaptation has been studied primarily for RL or sim-to-real, while a controlled imitation-learning experiment could test whether dynamics context helps only when it is identifiable under an independent visual nuisance intervention. That is a narrower empirical question, not a claim of a new context encoder.

## Candidate A — Context-Causal BC (CAUTION)

### Scientific question and hypothesis

When behavior cloning operates under randomized dynamics and visual nuisance, does a short transition history improve transfer because it identifies dynamics, or because the model exploits texture or camera shortcuts? The hypothesis is that an explicit transition-context signal improves held-out-dynamics policy success only when texture and dynamics are independently crossed. A texture-only gain, or a context decoder that survives texture swaps while policy transfer does not, contradicts the proposed mechanism.

Contribution type: controlled empirical finding plus causal diagnostic for imitation learning. It is not presented as a new context-encoder architecture.

### Exact method and measurements

Train a small state or image recurrent BC policy with a self-supervised dynamics-context head from a short action-observation window. Evaluate a 2x2 matrix of training/evaluation conditions: two dynamics settings crossed with two independently randomized textures. Measure:

* held-out dynamics-parameter decoding accuracy from the context representation, using episode-disjoint probes;
* policy success and return for each texture–dynamics cell;
* the difference between matched-dynamics and crossed-dynamics performance;
* context invariance under texture-only changes and sensitivity under dynamics-only changes;
* leakage controls from texture-only and context-only inputs;
* recurrent-BC-without-auxiliary and shuffled-context controls.

The native quantities are simulator dynamics parameters, observations, actions, rewards, and episode identity. No policy likelihood, action preference, confidence, or logged cross-trajectory intervention is required. The causal interpretation is identifiable only if texture and dynamics are randomized independently, splits are episode-disjoint, and the mechanism-destroying controls remove the transition-context signal while preserving capacity.

### Closest prior and scientific delta

[CARoL](https://arxiv.org/abs/2506.07006) learns transition context for task adaptation in RL; [Dynamics as Prompts](https://arxiv.org/abs/2410.20357) uses interaction history for system identification and sim-to-real adaptation. Both already establish that interaction history can encode dynamics. The non-overlapping claim would be limited to an imitation-learning causal audit: under crossed nuisance and dynamics interventions, transition-derived context predicts policy transfer only when the context is invariant to texture and decodes held-out dynamics. This is an evaluation/causal-audit delta, not a new learning paradigm.

### Cheapest kill experiment

Use one Lift-like task, two friction or mass settings, two independently generated visual textures, three seeds, and episode-disjoint train/test splits. Compare ordinary recurrent BC, BC plus context head, texture-only, context-only, and shuffled-context controls. Kill the idea if either (a) the decoder remains accurate under texture swaps but the transfer gain disappears, (b) texture-only performs as well as the context model, or (c) the no-auxiliary recurrent baseline matches the context model within a preregistered equivalence margin.

### Resource and feasibility audit

The existing CPU environment `/tmp/aris_p0_env` contains robosuite 1.5.2, MuJoCo 3.3.0, and PyTorch 2.5.1. A state-only measurement preflight collected 360 transitions from two controlled friction settings and reached held-out linear decoding accuracy 1.000 after a random split. This only establishes that the state-only dynamics label is measurable; it does not establish visual nuisance independence or a policy-transfer effect. The same environment lacks robomimic and torchvision. Offscreen rendering failed in both EGL and OSMesa modes (`Cannot initialize a EGL device display` and an OSMesa GL binding error), so the required texture intervention is not currently executable without a dedicated renderer/runtime repair. No repair, download, training, or scientific rollout was performed.

### Independent review

The independent review in [`STRUCTURAL_RESET_INDEPENDENT_REVIEW.md`](../STRUCTURAL_RESET_INDEPENDENT_REVIEW.md) returned **CAUTION** for A. The requested route was `gpt-6-astra`, reasoning `medium`, thread `/root/structural_reset_review`; the agent receipt could not expose a deployment identifier, so this report records the route honestly rather than claiming a stronger receipt. The review's strongest objections are context leakage, rendering/transition confounds, and the possibility that the auxiliary system-identification target makes the result tautological. It recommends the same 2x2 crossed intervention and controls before any pilot.

Status: **unresolved; not READY**. The required cheapest preflight did not pass because the visual intervention could not be instantiated and the state-only preflight is insufficient.

## Candidate B — Action-Affordance Representation Geometry (ABANDON)

Question: can a frozen visual encoder's normalized feature displacement on an executed transition, relative to a matched nuisance displacement, predict frozen linear-policy transfer? Proposed measurement is a post-hoc scalar over feature differences and transfer rank correlation. It is identifiable numerically, but its interpretation depends on whitening, temporal matching, camera motion, and encoder choice. VPP, FRAM, R3M/VC-1 affordance representations, GAM, and RoboEXP already connect visual features to future or action structure. The delta is a metric normalization choice, so the independent review assigned **ZERO**. Cheapest replication would likely confirm a correlation without a causal claim. Abandon for Paper-1.

## Candidate C — Reset-Distribution Policy Ranking (ABANDON)

Question: how much do policy rankings change under stratified initial-state and task-parameter support? Proposed measurements are paired-bootstrap ranking intervals, phase/outcome curves, and reset-coverage curves. These quantities exist, but the idea has no new mechanism and no identifiable explanation beyond sampling variance. Existing evaluation best practices, MESA-style evaluation, LIBERO-Plus, and deployment reliability work already cover the concern. The independent review assigned **ZERO**. Abandon for Paper-1.

## Evidence gate

| Gate | Result | Evidence |
|---|---|---|
| Structural change | Pass | A changes task regime, contribution type, and causal evaluation object relative to the excluded BC-RNN neighborhood. |
| Novelty boundary | Conditional | A is distinct only as a crossed-nuisance imitation audit; CARoL and Dynamics as Prompts are close mechanisms. |
| Native measurement | Partial | Dynamics parameters and transitions exist; visual texture intervention could not run. |
| Leakage controls specified | Pass in design | Texture-only, context-only, shuffled-context, episode-disjoint, and crossed-cell controls are specified. |
| Cheapest preflight | Fail / incomplete | State-only decoding passed at 1.000 accuracy; renderer-backed 2x2 preflight was unavailable. |
| Independent Astra-medium review | Caution | Review supports only a tightly scoped conditional pilot, not READY. |
| Infrastructure feasibility | Fail for current minimum pilot | robosuite/MuJoCo state-only works; required offscreen visual path fails EGL and OSMesa initialization. |

Because the measurement and infrastructure gates are incomplete, advancing A would turn an unresolved causal question into a runtime-driven implementation effort. The correct outcome for this reset is the required blocked verdict.

## What broader axis must open next

The next search should open a genuinely external research object: either (1) a pre-specified empirical study with an existing public multimodal dataset and an independently maintained evaluator, or (2) a dedicated vision/renderer-qualified substrate that permits causal nuisance interventions before method selection. It should not reopen BC-RNN memory, action-distance, action-bound, latency, gradient-routing, or TCI variants. A future candidate must still pass the same measurement-first gate and obtain an independent Astra-medium review before implementation.

## Scope record

No foundation-model training, large checkpoint or dataset download, GPU job, full simulator sweep, or scientific pilot was launched. The only execution beyond static inspection was the small CPU state-only measurement preflight described above.
