# VLA Problem-Space Discovery Report

Date: 2026-09-29  
Final status: **READY FOR PROBLEM-SPACE COMMITMENT**  
No scientific pilot, method implementation, policy training, large checkpoint download, or GPU experiment was run.

## Scope and evidence boundary

The previous program ended with `BLOCKED — BROADER RESEARCH SCOPE REQUIRED`. This pass therefore selected a research object before considering a mechanism. It mapped twelve structurally different spaces, checked recent 2025–2026 work, recorded open resources and falsification costs, and treated ASCC, CAEA, TCI, bounded-action BC, latency, gradient routing, truncated Gaussian, generic evaluator calibration, and Context-Causal BC as accumulated evidence rather than fresh ideas.

The persistent wiki now contains 24 paper records, 10 idea records (9 negative and 1 unresolved), 5 experiment records, and a 4,356-character query pack. The failed ideas and runtime pivots remain in the graph so future searches do not repeat them.

## Landscape map

| Problem space | Recent evidence | What systems can do | Remaining scientific question | Decision |
|---|---|---|---|---|
| VLA evaluation and capability boundaries | [VLA-Arena](https://arxiv.org/abs/2512.22539) covers 170 tasks and orthogonal task, language, and visual difficulty; [Colosseum V2](https://arxiv.org/abs/2605.27759) covers 28 tasks, 13 categories, two morphologies; [ROEP](https://doi.org/10.3390/s26154757) audits runtime fidelity and failure semantics | Compare open policies across structured perturbations and expose memorization, visual shortcuts, and rank reversals | Which measurement predicts deployment rather than another benchmark score? | **Reject:** evaluation-only and generic calibration are saturated and already negative in the project. |
| Robustness and failure analysis | [SO-101 failure/recovery benchmark](https://arxiv.org/abs/2606.08881), [SafeVLA-Bench](https://safevla.org/), RoboTwin 2.0-Plus, FPC-VLA | Taxonomize failures, safety violations, and recovery outcomes | Can a failure signal identify a causal intervention opportunity? | **Reject as a standalone space:** generic failure, safety, and recovery evaluation are accumulated negative evidence. |
| Cross-embodiment execution gap | [Embodiment Gap](https://arxiv.org/abs/2608.18433), [OXE-AugE](https://oxe-auge.github.io/), [Learning Action Priors](https://arxiv.org/abs/2606.26095), [Being-H0.5](https://arxiv.org/abs/2601.12993), CEI | Share data, representations, action priors, and policies across robot bodies; OXE-AugE reports 4.4M augmented trajectories | Can visual shift, action interface, kinematics/gripper, and adaptation cost be separated before target-robot data? | **Survive as Space A, rank 2.** |
| Long-horizon behavior and task planning | [Long-VLA](https://arxiv.org/abs/2508.19958), VLABench, SkillNet, CALVIN, BEHAVIOR, RoboDojo | Chain subtasks, use phase-aware inputs, and evaluate long sequences | Which failure is planning, memory, or execution? | **Reject for this paper:** crowded, often foundation-model or simulator heavy, and close to excluded memory/recovery work. |
| Action chunking and temporal abstraction | ACT, diffusion policies, Delay-Aware Diffusion Policy, RAPAC-DP, RACE, RTC/VLASH | Predict action chunks and reduce latency | What temporal abstraction failure remains after current latency and chunk-search work? | **Reject:** direct recent prior collisions are already recorded in the research brief. |
| Language grounding and text indispensability | [InstructMove](https://arxiv.org/abs/2608.22990), [MESA](https://www.pair.toronto.edu/MESA/), ManipBench, IntentVLA, ARC | Test category, attribute, spatial, compositional, and language dependence | Do policies use language when visual affordances are ambiguous? | **Reject for Paper-1:** benchmarks now directly instantiate the key gap; a metric-only extension is insufficient. |
| Data quality and data composition | [Data Scaling Laws](https://arxiv.org/abs/2410.18647), ReMix, SIEVE, DataMIL, SCIZOR | Measure data volume, mixture, and quality effects | Which data property causes a closed-loop gain? | **Reject:** accumulated mixed-quality and data-selection evidence is crowded. |
| Inference-time adaptation and continual deployment | [VANE](https://arxiv.org/abs/2608.09448), [RoboTTT](https://arxiv.org/abs/2607.15275), [FlowDAgger](https://microsoft.github.io/FlowDAgger/), ADPro | Update fast weights or isolated candidates from unlabeled streams or human correction | When is adaptation causally safe, reversible, and worth its compute? | **Survive as Space B, rank 3.** |
| Tactile and physical grounding | [RCT](https://arxiv.org/abs/2606.31694), [HapTile](https://arxiv.org/abs/2606.04825), [ForeTac-VLA](https://arxiv.org/abs/2609.20980), TVL, ViTacWorld, PRISM | Align touch, force, language, and action; model contact or forecast tactile states | Does future-contact information improve behavior-level generalization beyond reactive tactile fusion? | **Survive as Space C, rank 1 conditionally.** |
| World models × VLA | WorldGym, WorldEcho, VideoVLA, RISE, structured-planner work | Predict visual consequences and use imagined rollouts or compositional world models | Do imagined metrics predict real closed-loop control? | **Reject:** generic evaluator degradation, action-following, and ranking are accumulated negative evidence. |
| Memory and partial observability | StateMem, PredVLA, GMP, AURA-Mem, MEMBOT, MILES | Select, compress, or update history and memory during policy execution | Which memory event is causally necessary for control? | **Reject:** this is the exhausted recurrent-memory neighborhood. |
| Sim-to-real and OOD shift | [Colosseum V2](https://arxiv.org/abs/2605.27759), GeneralVLA, OXE-AugE, LIBERO-Plus, RoboTwin | Evaluate visual, language, action, morphology, and task shifts | Which shift factor drives a policy failure? | **Fold into Space A or C:** standalone shift benchmarks are crowded; causal decomposition is the remaining question. |

## Problem-space cards

### Space A — Cross-embodiment execution gap

#### Problem

Robot foundation models reuse data and visual-language representations across bodies, yet successful representation transfer does not guarantee executable control on a new arm, gripper, camera, action parameterization, or calibration.

#### Why it matters

Embodiment adaptation is the practical bottleneck between open robot-policy checkpoints and deployment. A paper that identifies which mismatch causes the loss would help researchers choose data collection and adaptation budgets.

#### Evidence the problem is real

The [Embodiment Gap survey](https://arxiv.org/abs/2608.18433) explicitly separates semantics/perception, interfaces/data, and cross-embodiment correspondence and reports that success rate alone hides adaptation work. OXE-AugE shows that large augmentation improves unseen-robot transfer, while Learning Action Priors and Being-H0.5 introduce stronger shared action or human-centric priors. OpenVLA exposes public checkpoints and OXE data, and CEI provides a cross-embodiment interface line.

#### Current approaches

Current systems use canonical action spaces, action priors, robot augmentation, interface learning, visual-language pretraining, and target-robot fine-tuning. They generally report aggregate success across embodiments rather than independently manipulating the visual, interface, and kinematic factors.

#### Remaining gap

The open problem is attribution: whether a failure comes from visual appearance, action semantics, kinematics/gripper, calibration, or insufficient target data. A defensible future study would be an explanatory intervention matrix, not another general-purpose policy architecture.

#### Open ecosystem

OpenVLA provides a 7B checkpoint and fine-tuning code; Open X-Embodiment provides broad robot data; OXE-AugE provides public augmentation code and a very large dataset; Colosseum V2 and ManiSkill provide simulated morphology and shift evaluation; CEI provides a cross-embodiment interface implementation.

#### Research accessibility

Engineering difficulty is medium-high because action scaling, camera convention, kinematics, and calibration must be held apart. A small simulation study may fit moderate compute, but OXE-AugE is approximately 1 TB and real target-robot claims require hardware or a faithful simulator. Cheapest experiment: 2–4 days if a small frozen checkpoint and controlled simulator are already qualified. This project currently lacks a qualified visual renderer, so it is not the fastest route.

#### Thesis potential and saturation risk

It can support an empirical or evaluation paper if the attribution question is identified cleanly. Saturation and direct-collision risk are high for scorecards and moderate for a carefully controlled factor study. A negative result would still show that public logs cannot identify the source of the embodiment gap.

#### Cheapest falsification

Use one frozen policy and matched trajectories while varying visual appearance, action parameterization, and kinematic or gripper configuration separately. Reject the space if effects cannot be independently manipulated or simply reproduce known embodiment ordering.

### Space B — Reliable test-time adaptation and continual VLA deployment

#### Problem

VLA policies encounter unlabeled deployment streams that differ from training data. Updating the policy online may improve performance, but can also contaminate future evidence, forget prior skills, or optimize a shortcut that does not survive closed-loop consequences.

#### Why it matters

Deployment cannot assume repeated labeled demonstrations. A reliable adaptation rule could reduce target-robot data requirements while preserving prior behavior and providing an interpretable decision about when an update is trusted.

#### Evidence the problem is real

VANE reports that a shared adaptation space can mix incompatible task corrections and therefore isolates candidate updates and commits only after future evidence. RoboTTT scales test-time fast-weight context to 8K timesteps and reports large gains on long tasks. FlowDAgger adapts generative policies from human correction while freezing the base. These results establish both opportunity and failure modes.

#### Current approaches

Methods include test-time training, fast weights, future-prediction losses, latent action inversion, online human correction, and deployment-specific adapters. Results are task and embodiment dependent, and modern stacks are often large or GPU-specific.

#### Remaining gap

The problem-space question is when adaptation is causally beneficial, reversible, and free from temporal leakage. A future study should distinguish no adaptation, offline batch adaptation, and reversible online updates under future-only evaluation windows.

#### Open ecosystem

OpenVLA and SmolVLA provide public checkpoints; SimplerEnv and LIBERO provide simulation; VANE, RoboTTT, and FlowDAgger provide recent protocols or code; Open X-Embodiment and Bridge-like datasets provide deployment streams.

#### Research accessibility

Engineering difficulty is high because one must maintain strict pre/post windows, model state snapshots, optimizer state, and forgetting metrics. 1–3 day falsification is plausible only with a small checkpoint and CPU-compatible simulator. Large VLA inference and test-time updates may exceed the available DCU path.

#### Thesis potential and saturation risk

This could support a strong empirical or method paper, but direct-prior risk is highest. A result that only reproduces VANE-like isolation would not be a new problem contribution. A negative result limiting unlabeled adaptation would still be useful.

#### Cheapest falsification

Replay a small offline stream through a frozen checkpoint and measure post-update success, future-window performance, and forgetting. Reject if gains vanish outside one stream or if the only winning condition is already the mechanism of VANE.

### Space C — Contact-rich tactile and physical grounding

#### Problem

Vision-language-action policies often cannot observe contact state, material properties, force, slip, or occluded geometry. Tactile and force signals can expose these variables, but it is unclear which physical information transfers to unseen materials and whether predicting future contact helps behavior.

#### Why it matters

Contact-rich manipulation is where visual policies most often fail: grasping, pressing, folding, insertion, and material handling depend on latent physical state. Better physical grounding would improve reliability without requiring a foundation model trained from scratch.

#### Evidence the problem is real

RCT contains 29,279 tactile frames from 122 materials, seven categories, and three DIGIT sensors, with held-out contact-sequence and material protocols. It reports a 17.7-point drop when contact-sequence overlap is removed and only 25.1 ± 6.1% held-out-material retrieval. HapTile adds synchronized tactile, haptic, language, and action trajectories for contact-rich imitation. ForeTac-VLA reports future tactile forecasting gains over reactive baselines. TVL, ViTacWorld, and PRISM show that multimodal physical grounding is an active area.

#### Current approaches

Recent work collects new tactile datasets, aligns tactile with language or vision, adds tactile tokens to VLA backbones, and forecasts future contact states. The field now has mature leakage-controlled tactile representation protocols, but behavior-level transfer is less consistently measured.

#### Remaining gap

The strongest unresolved question is whether future-contact information is necessary for behavior-level generalization beyond current-frame or short-history tactile input under held-out materials and contact sequences. This is a problem-space commitment, not an admitted method.

#### Open ecosystem

RCT provides public data, split files, and evaluation scripts; its dataset page documents material, sensor, position, and contact-sequence splits. HapTile provides contact-rich visuotactile-language-action data and baselines. TVL provides aligned touch-vision-language data. Small encoders and PyTorch sequence models can run offline without a simulator.

#### Research accessibility

Engineering difficulty is low-medium if data are downloaded selectively and existing encoders are frozen. GPU need is moderate for small heads and can be CPU-first for feature extraction; no robot or renderer is required for the first measurement. The critical data requirement is an action or contact-state behavior proxy. Cheapest falsification is 1–3 days: audit the public schema, then compare current-frame, short-history, and predictive representations on held-out materials and contact sequences over three seeds or material draws.

#### Thesis potential and saturation risk

The space can support an empirical or diagnostic paper, with a later method extension only if the behavior proxy shows a real gap. Saturation is medium-high: a new tactile encoder, sensor, or generic fusion loss collides directly with current work. The publishable boundary is a behavior-level necessity result under leakage-controlled splits. If no behavior proxy is available, the space must be rejected.

#### Cheapest falsification

Before any model work, inspect RCT and HapTile manifests for action, contact phase, force, and episode labels. If only tactile-to-text retrieval is possible, reject the space for this project because it cannot support a robot-control claim. If a behavior proxy exists, kill the space when future prediction has no robust gain across held-out materials or when gains disappear under contact-sequence disjointness.

### Space D — Evaluation, safety, and failure semantics (rejected)

The problem is real and open-source resources are unusually rich: VLA-Arena, ROEP, SafeVLA-Bench, SO-101 failure analysis, MESA, Colosseum V2, and RoboDojo all expose more structured axes than binary success. However, the project's accumulated negative evidence already rejects generic VLA safety, evaluator calibration, shift degradation, ranking, and action-following diagnosis. A new score or reset protocol would be a benchmark contribution without an identified mechanism. The cheapest falsification is literature saturation plus a repeated-reset replication, which is already sufficient to reject it for Paper-1.

### Space E — Long-horizon planning and memory (rejected)

Long-VLA, VLABench, SkillNet, CALVIN, BEHAVIOR, RoboDojo, world-model planners, and memory policies demonstrate that long horizons remain difficult. The open question is whether errors come from planning, memory, contact execution, or recovery. The available work already occupies each of these axes, and the project has explicit negative evidence against recurrent-memory and generic recovery variants. A graduate-student study would need a large benchmark and foundation-model stack. Reject before method ideation.

### Space F — Language grounding and compositional instruction following (rejected)

InstructMove makes language indispensable by constructing visually and physically plausible distractors; MESA, ManipBench, ARC, VLABench, and IntentVLA cover language dependence, spatial reasoning, and composition. The problem matters, but the benchmark gap is now directly populated. Any remaining contribution would need a new external data source or a causal intervention beyond benchmark construction, which fails the current 1–3 day and no-broad-benchmark constraints.

### Space G — Data scaling and composition (rejected)

Data Scaling Laws, ReMix, SIEVE, DataMIL, SCIZOR, and OXE-AugE establish strong data-volume, mixture, and embodiment-composition questions. This project already records mixed-quality selection as negative evidence. A new data filter or mixture schedule would collide directly with current work or become a dataset QA result. Reject.

### Space H — World models for VLA planning and evaluation (rejected)

WorldGym, WorldEcho, VideoVLA, RISE, and structured-planner work show that future prediction can aid planning while imagined rollouts accumulate error. The project has explicit negative evidence against generic world-model evaluator shift, calibration, ranking, and action-following diagnosis. A new world-model metric is not an open Paper-1 problem space under this governance. Reject.

### Space I — Action chunking, latency, and inference scheduling (rejected)

Delay-Aware Diffusion Policy, RAPAC-DP, RACE, RTC, and related systems cover latency compensation, chunk search, and asynchronous execution. The current brief explicitly marks adaptive horizons and generic latency directions as direct prior territory. Reject.

### Space J — Generic sim-to-real and domain-shift robustness (folded into A/C)

Colosseum V2, OXE-AugE, LIBERO-Plus, RoboTwin, and GeneralVLA cover visual, language, action, morphology, and task shifts. The remaining value lies in identifying a physical factor, such as embodiment interface or contact material, rather than reporting another aggregate robustness curve. Therefore this space is folded into cross-embodiment Space A and tactile Space C.

## Comparison of the three survivors

| Dimension | Space C: tactile/physical grounding | Space A: embodiment gap | Space B: test-time adaptation |
|---|---|---|---|
| Importance | High: contact and material failures are deployment-critical | Very high: determines whether robot foundation models can be reused | High: deployment lacks labels and distribution shifts |
| Remaining gap | Behavior-level necessity of future contact under held-out materials | Causal attribution of visual/interface/kinematic mismatch | Safe, reversible benefit of unlabeled adaptation |
| Novelty headroom | Medium, conditional on behavior proxy | Low-medium; generic protocol is crowded | Low; direct overlap with VANE/RoboTTT/FlowDAgger |
| Public resources | RCT, HapTile, TVL, split files and small encoders | OpenVLA, OXE, CEI, Colosseum; OXE-AugE is ~1 TB | OpenVLA/SmolVLA, SimplerEnv, recent adaptation code |
| Cheapest falsification | 1–3 days offline if action/contact proxy exists | 2–4 days with qualified simulator and interface controls | 3–7 days due online state and contamination controls |
| Engineering risk | Low-medium, no renderer required | Medium-high, calibration and action interfaces | High, online update and checkpoint/runtime burden |
| Negative-result value | Shows predictive contact is unnecessary or data split is limiting | Shows public logs cannot identify embodiment causes | Limits claims about unlabeled test-time learning |
| Recommendation | **Rank 1, conditional** | Rank 2 | Rank 3 |

## Final commitment

**Recommended problem space: contact-rich tactile and physical grounding, conditional on an available behavior-level proxy in RCT or HapTile.**

This space is preferred because it combines a real physical failure mode, a recent leakage-controlled public dataset, an offline-first measurement path, and a negative result that remains publishable as a boundary on predictive contact information. The commitment is to the problem space and its measurement question. It does not authorize a specific model, loss, sensor build, or scientific pilot.

The immediate next discovery cycle should focus on:

1. verifying the public action/contact-state schema and licensing of RCT and HapTile;
2. mapping the exact behavior proxies already used by tactile VLA papers;
3. checking 2026 concurrent work for any direct behavior-level predictive-contact claim;
4. defining a preregistered held-out-material and held-out-contact-sequence comparison;
5. abandoning the space immediately if the public data support only representation retrieval and no behavior proxy.

If that schema gate fails, the next choice is Space A, with a simulator-first causal embodiment attribution study. Space B remains a later option after a smaller checkpoint and runtime have been qualified.

## Concepts for the human researcher

Learn the difference between representation evaluation and behavior-level evaluation; episode, contact-sequence, and material-disjoint splits; leakage from correlated frames; tactile sensing variables such as force, slip, indentation, and contact phase; cross-embodiment action interfaces; and test-time adaptation with future-only evidence. Also learn how to separate a problem-space claim from a method claim: this report commits to a scientific question and measurable substrate, not to a new architecture.

## Next-cycle boundary

The next cycle may perform a schema and literature admission audit for Space C. It must not invent a final method, train a policy, download large checkpoints, run GPU experiments, repair EGL, or begin a full idea-discovery pipeline before the behavior-proxy gate passes.
