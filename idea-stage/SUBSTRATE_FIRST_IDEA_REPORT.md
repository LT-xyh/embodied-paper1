# Substrate-First Research-Direction Reselection Report

**Date:** 2026-09-20  
**Search cutoff:** 2026-09-20 (including work released through September 2026)  
**Binding contract:** [RESEARCH_BRIEF.md](../RESEARCH_BRIEF.md) and [SUBSTRATE_FIRST_RESELECTION.md](SUBSTRATE_FIRST_RESELECTION.md)  
**Status:** design-only shortlist; no implementation, runtime installation, dataset/checkpoint download, simulator, GPU job, or real-robot experiment was run.

The selection criterion was an executable public substrate first, followed by a static execution admission and an aggressive 2025–2026 novelty screen. The report deliberately stops at a shortlist. It does not authorize implementation.

## 1. Executable Substrate Landscape

The sizes below are release metadata or HTTP HEAD observations. No large artifact was downloaded.

| Substrate and exact public artifact | Tasks / embodiment | Available variables | Policy or simulator needed for the minimum pilot? | Software / accelerator boundary | Storage gate | Decision |
|---|---|---|---|---|---|---|
| [ArmnetBench v0.1 SO-101](https://huggingface.co/datasets/armnet/armnetbench_v01_lerobot_so101) and [bimanual release](https://huggingface.co/datasets/armnet/armnetbench_v01_lerobot_bimanual_so101) | 8 single-arm tasks plus bimanual tasks; SO-101; 2,499 single-arm episodes and 1,127,881 frames | LeRobot v3.0 Parquet, 6-D action/state, RGB video (optional), next.reward, next.done, task/policy/embodiment, success_class (successful, suboptimal, failure), success_cutoff_time | No policy checkpoint or simulator for the metadata/state/action pilot; videos are not needed initially | Python, PyArrow/Pandas, standard PyTorch or CPU statistical code; no CUDA, FlashAttention, Triton, or custom kernels | Non-video files are about 58 MB (single-arm) and 65 MB (bimanual); full releases are about 60.6 GB and 43.3 GB because of videos | **Pass** for an offline, metadata-first pilot |
| [SocNavData2026](https://github.com/SocNavData/SocNavData2026), associated with the [2025 ALT paper](https://arxiv.org/abs/2509.01251) | 4,427 social-navigation trajectories (182 real, 4,245 simulated), 4,402 rated trajectories; multiple scenes, tasks, and raters | Robot pose/speed/drive/shape, goal and task context, humans/objects/environment, rater IDs and ratings; repeated ratings under different contexts | No policy or simulator for rating-model analysis; the released RNN is only a comparison baseline | JSON/Python/NumPy or standard PyTorch; CPU/DCU sufficient; no CUDA-specific dependency | Repository-linked raw/labeled artifacts are roughly 373 MB/290 MB by HTTP metadata; ratings and split files are small | **Pass** for an offline, CPU-first pilot |
| [Frontier Robotics Pack](https://huggingface.co/datasets/solsticestudioai/frontier-robotics-pack) | 1,000 synthetic episodes; pick/place, drawer, peg-in-hole and deformable tasks across 3 embodiments | Episode/task/embodiment, instruction, action interface, trajectory summaries, success/failure, failure reason, recovery count, progress, counterfactual branches and metrics; frames are not included | No policy or simulator for table-level analysis | Small JSON/Parquet-style artifact; standard Python/PyTorch; no accelerator requirement | 35.3 MB | **Passes substrate gate; novelty gate later rejects it** |
| [REASSEMBLE](https://researchdata.tuwien.ac.at/records/0ewrv-8cb44/files/data.zip?download=1) | 4,551 Franka demonstrations (4,035 success/516 failure), 17 objects; RGB, event, audio, force/torque and robot state | Multimodal timestamps, action/segment labels, success/failure, contact and force signals | No policy/simulator for alignment analysis, but the full multimodal archive is needed for the strongest test | HDF5/h5py/NumPy/PyTorch can run on CPU; no CUDA requirement | Public archive is about 58.9 GB; a small subset is possible, but the minimum reliable multimodal test is not a small artifact | **Conditional; novelty and storage screen reject it** |
| [CompoSuite](https://datadryad.org/dataset/doi:10.5061/dryad.9cnp5hqps) | 256 compositional tasks and multiple robots | HDF5 transitions, rewards, terminals/timeouts and task factors | Offline reader is possible, but the intended cross-embodiment pilot needs large archives | Standard readers exist, but no small artifact | About 250.64 GB total; per-robot archives are about 16 GB | **Hard reject for the 1–3 day substrate gate and direct-prior collision** |

The two surviving substrate families expose an experimentally meaningful variable that is not itself a renamed score: outcome-dependent sequence censoring in ArmnetBench, and rater/context-dependent preference generation in SocNavData2026.

## 2. Rejected Substrates and Exact Rejection Reasons

| Substrate / direction | Exact rejection reason |
|---|---|
| Cross-Embodiment Offline RL ([paper](https://arxiv.org/abs/2602.18025), [code](https://github.com/haruki-abe/cross_embodiment_offline_rl)) | The release advertises datasets of 500 GB or more, with individual datasets above 80 GB, and a CUDA/JAX training stack. It violates the small offline-first gate before any scientific test. |
| RoboMIND / Robo-ValueRL | Multi-terabyte or hundreds-of-GB releases and direct mixed-quality/value-learning claims. This is both operationally too large and inside the excluded generic data-quality/value category. |
| DROID and similar large teleoperation corpora | Tens of thousands of trajectories with no small, outcome-labeled slice that supports the proposed mechanism; downloading the corpus is not justified before evidence. |
| REBOOT and REIM | Their central claims are recovery trajectories, recovery actors, or runtime failure-risk monitoring. The binding brief explicitly excludes generic recovery/retry directions. |
| BotFails, Robotics Failure Benchmark, BridgeDataV2-Fail, ViFailback, SafeManip and ProcVLM | Generic failure detection, safety monitoring, progress/value, or correction is already crowded and does not provide a non-overlapping mechanism. |
| OmniNavBench, RoboDojo and REALM | The smallest credible pilot requires Isaac Sim/Isaac Lab, NVIDIA CUDA or Dockerized simulation assets. This fails the no-runtime-reconstruction and no-NVIDIA-only gate. |
| RoCo, BEHAVIOR and other multi-terabyte multimodal releases | Storage and simulator/state-replay requirements exceed the contract; no evidence justifies that infrastructure work. |
| Contact/topology transfer proposals | KITE, ContactFlow, TopoRetarget and C2Dex already cover contact-flow/topology/graph transfer. A new benchmark or metric would not beat those claims under this contract. |
| Generic world-model evaluator proposals | WorldEval, WorldGym, IRASim, WorldEcho and the 2026 decision-centric evaluation position already cover shift, calibration, ranking and action-following failure modes. No surviving proposal uses a world-model evaluator as its main novelty. |
| Frontier Robotics Pack as a final direction | The artifact is executable, but a representation-by-perturbation table is confounded by synthetic generator factors and is too close to MESA-style benchmark factor analysis. It is retained only as an initial hypothesis to reject. |
| REASSEMBLE as a final direction | The alignment mechanism is plausible, but M2R2 already uses REASSEMBLE for temporal action segmentation and ContactWorld studies cross-modal compatibility/long-horizon robustness. The remaining distinction would be a fragile timestamp metric on a 58.9 GB archive. |
| CompoSuite as a final direction | Large storage fails the hard gate, while compositional/cross-embodiment learning and data-generation claims are already explicit in CompoSuite follow-up work and [MESA](https://www.pair.toronto.edu/MESA/). |

### Mandatory closest-prior anchor screen

Every initial candidate was checked against the required anchors. None proposes segment/state-action demonstration filtering (S2I, SCIZOR, DataMIL), visual-shortcut or counterfactual language diagnosis (LIBERO-CF, LIBERO-VIFO), generic VLA safety (LIBERO-Safety), world-model shift/calibration/ranking/action-following evaluation (WorldEval, WorldGym, IRASim, WorldEcho, and the decision-centric position), or contact-topology transfer (KITE, ContactFlow, TopoRetarget, C2Dex). A candidate that can only be described using one of those mechanisms is rejected before the shortlist.

## 3. Scientific Variables and Gaps Enabled by the Surviving Substrates

### ArmnetBench

The release makes the following variables jointly observable without video inference: policy identity/type, task, embodiment, sequence length, action/state prefixes, terminal reward/done, human outcome class, and the documented success_cutoff_time processing rule. Successful and suboptimal episodes are end-trimmed at a human cutoff, while failures are not. That creates a testable informative-censoring intervention:

- observed sequence versus fixed-horizon padding/masking;
- naïve time/length features versus censoring-aware weighting;
- held-out outcome prediction and calibration;
- policy ranking stability after removing label-dependent horizon information.

This is a mechanism about how outcome labels change the observed trajectory distribution. It is not demonstration filtering, a new benchmark score, or a world-model evaluator.

### SocNavData2026

The labeled release exposes trajectory geometry, task/context, and rater identity together. The same trajectory can be rated under different contextual conditions, which permits a rater-by-context decomposition:

- geometry: clearance, speed, path length, jerk, goal distance and interaction events;
- context: task type, scene and nearby-agent configuration;
- rater: repeated rating identity and between-rater variance;
- outcome: held-out rating, preference ordering and variance components.

The test is whether stable normative profiles and context-dependent geometry weights explain ratings beyond the released aggregate ALT model. This is a preference-generation mechanism, not a renamed social-cost metric.

## 4. Initial Candidate Hypotheses (five before rejection)

### Candidate A — Outcome-dependent censoring in robot rollouts (ArmnetBench)

**Precise hypothesis.** End-trimming successful/suboptimal episodes at a human success_cutoff_time while retaining full failure horizons creates informative censoring. A learner that sees the observed horizon will overstate early outcome predictability and can change policy rankings; fixed-horizon masking or inverse-censoring weighting should remove that artifact.

| Closest prior | Exact prior claim | What it already solves | Non-overlapping claim here | Distinguishing experiment | Difference type |
|---|---|---|---|---|---|
| [ArmnetBench v0.1 (2026)](https://arxiv.org/abs/2607.24481) and its [dataset card](https://huggingface.co/datasets/armnet/armnetbench_v01_lerobot_so101) | Releases 3,118 core episodes across 7 policies and 12 tasks with successful/suboptimal/failure labels and a common evaluation budget; the card documents end-trimming at success_cutoff_time. | Provides the labeled, multi-policy, multi-task substrate and a fair comparison protocol. | Tests whether the release procedure itself leaks outcome through sequence length and whether a censoring-aware learner changes rankings. ArmnetBench does not claim or test this mechanism. | Train the same small sequence classifier/value probe under observed, fixed-horizon, and inverse-censoring views; evaluate held-out success_class, calibration and policy ranking with task/policy controls and episode-clustered bootstrap. | **Scientific mechanism:** informative censoring in embodied logs, not a metric replacement. |
| [UR-VC (2026)](https://arxiv.org/abs/2607.12892) | Corrects noisy time-derived progress labels using nearest-state retrieval because physical progress can slip or be non-monotonic. | Addresses proxy-label noise in progress estimation. | Corrects label-dependent observation length and evaluates outcome/ranking bias; it does not study censoring induced by success-dependent cutoffs. | Add a matched fixed-horizon intervention to show a ranking/calibration gap that UR-VC's state retrieval cannot explain. | **Scientific mechanism:** different causal source of bias. |
| [Trajectory truncation (2023)](https://arxiv.org/abs/2304.04660) | Studies uncertainty-driven trajectory truncation for offline RL. | Shows that truncation can be useful for learning efficiency. | Tests annotation/outcome-dependent censoring in a robot benchmark with human outcome classes, rather than uncertainty-based truncation. | Keep truncation policy fixed and vary only whether the observed horizon depends on outcome. | **Scientific mechanism:** different truncation cause and robot evaluation consequence. |

**Reviewer rejection to anticipate.** “This is only a benchmark audit or a metric change.” The claim is defensible only if the pre-registered intervention changes a sequence learner's held-out predictions/rankings and the effect reproduces across tasks and policy families; a descriptive length table is insufficient.

**Positive result.** An outcome-conditioned horizon signal predicts labels or changes policy ranking, and fixed-horizon/censoring-aware training removes the gap across held-out tasks/policies.

**Kill result.** Horizon distributions are matched, no ranking/calibration gap appears, or the correction is unstable and confined to one task.

### Candidate B — Rater/context interaction as the source of social-navigation preference variance (SocNavData2026)

**Precise hypothesis.** Aggregate ALT scores hide stable rater-specific normative profiles and context-dependent weights on trajectory geometry. A hierarchical rater/context model should improve leave-rater-out and leave-context-out prediction and expose a reproducible preference trade-off.

| Closest prior | Exact prior claim | What it already solves | Non-overlapping claim here | Distinguishing experiment | Difference type |
|---|---|---|---|---|---|
| [ALT / SocNavData (2025)](https://arxiv.org/abs/2509.01251) and [public repository](https://github.com/SocNavData/SocNavData2026) | Learns an aggregate trajectory metric from robot state, task/context and human ratings; reports a public RNN baseline and releases 4,427 trajectories/4,402 ratings. | Establishes a public social-navigation dataset and an aggregate learned metric. | Estimates latent rater random effects and rater-by-context interactions, then tests whether geometry weights change by normative profile. | Fit aggregate ALT, fixed-effects context model and hierarchical rater/context model; use leave-rater-out, leave-context-out, ranking correlation, variance decomposition and clustered bootstrap/permutation. | **Scientific mechanism:** latent preference generation and interaction, not a new score name. |
| [A General Social Cost Layer (2026)](https://link.springer.com/article/10.1007/s12369-026-01384-0) | Adds a hand-designed general social-cost layer to a navigation planner and validates proxemics/task scenarios with human studies. | Provides a planner-level way to encode social context. | Explains why the same geometry can receive different ratings across raters and contexts; does not model rater identity or latent preference variance. | Hold planner and geometry fixed; test whether a rater/context-conditioned preference model predicts held-out ratings beyond a single social-cost layer. | **Scientific mechanism:** preference heterogeneity, not planner-layer engineering. |

**Reviewer rejection to anticipate.** “The data are sparse and this is only a niche social metric.” The direction survives only if the rater effect and interaction are stable under leave-rater-out and scene/task controls; otherwise it is killed.

**Positive result.** Rater random effects and context interactions are reproducible, improve held-out rating/ranking prediction, and change the geometry trade-off in a way that aggregate ALT cannot represent.

**Kill result.** Random effects collapse, ratings are explained entirely by scene/task, or the improvement vanishes under rater/context holdouts.

### Candidate C — Action-interface × perturbation interaction in the Frontier Robotics Pack

**Precise hypothesis.** Action interfaces (joint, Cartesian, gripper abstraction) interact with domain randomization and task family to change failure modes; the interaction is larger than either main effect.

**Closest prior and rejection.** [MESA (2026)](https://www.pair.toronto.edu/MESA/) already evaluates semantic/spatial/compositional axes and reports action-representation/pretraining effects. The Frontier pack has only 1,000 synthetic summary rows and no frames, so a table of action-interface effects cannot separate generator artifacts from a mechanism. The proposed experiment would be a benchmark/metric analysis, not a non-overlapping mechanism. **Reject.**

### Candidate D — Timestamp alignment as a multimodal failure mechanism in REASSEMBLE

**Precise hypothesis.** Small event/RGB/audio/force timestamp offsets degrade segment-boundary and success prediction, with a non-monotonic optimum due to contact dynamics.

| Closest prior | Exact prior claim | What it already solves | Non-overlapping claim here | Distinguishing experiment | Difference type |
|---|---|---|---|---|---|
| M2R2 (2025, REASSEMBLE-based) | Uses REASSEMBLE for multimodal temporal action segmentation. | Establishes the dataset and segmentation task. | Treats alignment offset as an intervention and tests a causal performance curve rather than adding modalities. | Shift one stream by controlled offsets, shuffle only timestamps, and evaluate held-out boundaries/success across objects. | Scientific mechanism in principle. |
| [ContactWorld (2026)](https://arxiv.org/abs/2606.13877) | Finds representation structure, cross-modal compatibility and long-horizon robustness matter in vision-tactile world models. | Establishes cross-modal compatibility as a performance factor. | Isolates acquisition-time synchronization as the factor, without training a world model. | Compare aligned versus offset streams under the same lightweight classifier. | Scientific mechanism, but close to the prior. |

**Rejection.** Full multimodal access is about 58.9 GB and the remaining claim is a narrow alignment metric adjacent to M2R2/ContactWorld. It does not meet the preferred 1–3 day small-substrate gate, so it is not shortlisted.

### Candidate E — Factor-support gaps in compositional offline control (CompoSuite)

**Precise hypothesis.** Missing combinations of robot embodiment and task factors, rather than total transition count, dominate compositional offline value error.

**Closest prior and rejection.** CompoSuite itself provides compositional tasks and factorized offline transitions; [Cross-Embodiment Offline RL (2026)](https://arxiv.org/abs/2602.18025) explicitly targets heterogeneous robot datasets, and MESA evaluates compositional/semantic/spatial generalization. Testing support coverage on a 250.64 GB archive would be a large-data benchmark analysis with direct prior collision. **Reject.**

## 5. Aggressive 2025–2026 Novelty Rejection

| Candidate | Static gate | Closest-prior collision | Decision |
|---|---|---|---|
| A. Armnet censoring mechanism | Pass: non-video state/action/metadata slice is tens of MB; CPU/offline; no simulator | Armnet releases labels/trimming but does not test outcome-dependent censoring; UR-VC addresses a different time-proxy problem | **Retain** |
| B. SocNav rater/context mechanism | Pass: public JSON/rating artifacts under 0.4 GB; CPU/offline; no simulator | ALT aggregates context; GSCL adds a planner cost layer; neither models latent rater profiles and interactions | **Retain** |
| C. Frontier action-interface interaction | Pass substrate | MESA and synthetic factor benchmarks already cover action representation and factor effects; no causal pairing in the artifact | **Reject** |
| D. REASSEMBLE alignment | Conditional storage pass only | M2R2 and ContactWorld are too close; full archive is 58.9 GB | **Reject** |
| E. CompoSuite support gaps | Fail storage and scope gate | CompoSuite, cross-embodiment offline RL and MESA already cover the core claim | **Reject** |

The two retained claims explicitly beat the mandatory anchors by changing the scientific object: they study data-generation/annotation mechanisms (censoring and preference heterogeneity), rather than filtering demonstrations, diagnosing language shortcuts or generic safety, or evaluating a world-model evaluator.

## 6. Final Shortlist (at most Top-3)

Only two directions survive. No third candidate has enough novelty and execution evidence under the contract.

| Rank | Direction | Core falsifiable claim | Why it is the best current substrate | Main risk |
|---|---|---|---|---|
| **Top-1** | **Outcome-dependent censoring in ArmnetBench robot rollouts** | Success-dependent end trimming leaks outcome through horizon; fixed-horizon or censoring-aware learning removes the resulting prediction/ranking bias | Exact 2026 public release, state/action/labels in small non-video files, multi-policy and multi-task controls, no simulator | Could collapse to a benchmark-specific preprocessing artifact; must reproduce across tasks/policies |
| **Top-2** | **Rater/context interaction in SocNavData2026** | Social-navigation preference is generated by stable rater profiles whose geometry weights change with context; aggregate scores conceal this | Public ratings with rater/context/trajectory variables, CPU/offline analysis, direct leave-rater/context-out falsification | Sparse repeated ratings or scene confounding could make the latent effects unstable |

**Verdict:** retain Top-1 and Top-2 for a subsequent approval gate. The report stops here. Neither direction is implementation-authorized.

## STATIC EXECUTION ADMISSION — Top-1 Armnet censoring

- **Exact public artifact:** [single-arm dataset](https://huggingface.co/datasets/armnet/armnetbench_v01_lerobot_so101), [bimanual dataset](https://huggingface.co/datasets/armnet/armnetbench_v01_lerobot_bimanual_so101), and [paper](https://arxiv.org/abs/2607.24481).
- **Checkpoint:** none required; the pilot is an offline probe over released sequences.
- **Files and labels:** meta/info.json; selected meta/episodes/*.parquet and data/*.parquet; action/state arrays; next.reward, next.done; task, policy and embodiment IDs; success, success_class, and documented success_cutoff_time. Videos are excluded from the admission pilot.
- **Policy/simulator requirement:** none.
- **Packages/runtime:** Python, PyArrow/Pandas, NumPy, scikit-learn or standard PyTorch; no NVIDIA-only package, FlashAttention, Triton, custom CUDA, LIBERO/RoboCasa, or exact simulator state restore.
- **Storage:** approximately 58 MB non-video for single-arm (about 65 MB for bimanual); do not fetch the 60.6/43.3 GB video releases before the metadata pilot.
- **Hardware:** CPU or standard PyTorch on the available DCU; no GPU job is needed.
- **Minimal steps:** inventory episode metadata; construct observed and fixed-horizon prefix views; fit the same small sequence/value probe; apply inverse-censoring weights; evaluate held-out outcomes and policy rankings.
- **Independent variable:** observation/censoring protocol (observed, fixed-horizon, masked, inverse-censoring).
- **Dependent variables:** held-out success-class prediction, calibration, horizon leakage, and policy ranking stability.
- **Controls:** task, policy family, embodiment, episode count, prefix budget, and random seed; cluster all inference by episode/task.
- **Statistics:** episode/task-clustered bootstrap, paired permutation of censoring protocol, calibration curves and rank correlation; report confidence intervals rather than one aggregate score.
- **Positive criterion:** a reproducible observed-versus-fixed-horizon gap that disappears under censoring-aware treatment across held-out tasks or policies.
- **Kill criterion:** no gap after controls, or the effect is confined to one task/policy and cannot be reproduced with a pre-registered subset.
- **Admission verdict:** **ADMIT for design-only pilot planning; implementation remains unauthorized.**

## STATIC EXECUTION ADMISSION — Top-2 SocNav rater/context mechanism

- **Exact public artifact:** [SocNavData2026 repository](https://github.com/SocNavData/SocNavData2026) and [ALT paper](https://arxiv.org/abs/2509.01251); use the repository's labeled/rating JSON and split artifacts.
- **Checkpoint:** none required; the released RNN is an optional baseline, not a dependency.
- **Files and labels:** trajectory JSON with robot pose/speed/drive/shape, humans/objects/environment, goal/task/context, rater ID, rating and split metadata.
- **Policy/simulator requirement:** none for offline preference modeling.
- **Packages/runtime:** Python JSON/NumPy/scikit-learn or standard PyTorch; mixed-effects implementation may be CPU-only; no CUDA-specific runtime.
- **Storage:** repository-linked raw/labeled artifacts are approximately 373 MB/290 MB by HTTP metadata; rating and split files are much smaller. No video or simulator asset is required.
- **Hardware:** CPU or standard PyTorch on the available DCU.
- **Minimal steps:** reproduce the released aggregate ALT baseline on the labeled subset; fit fixed-effects and hierarchical rater/context models; run leave-rater-out and leave-context-out tests; decompose rating variance.
- **Independent variables:** rater identity, context/task, and geometry/context interaction terms.
- **Dependent variables:** held-out rating, pairwise/ranking agreement, variance components, and context-specific geometry weights.
- **Controls:** trajectory, scene, task type, number of ratings, geometry feature normalization, and split seed.
- **Statistics:** hierarchical uncertainty intervals, leave-rater/context-out evaluation, scene/task-clustered bootstrap, and permutation tests for rater/context interactions.
- **Positive criterion:** stable rater random effects and context interactions improve held-out rater/context prediction beyond aggregate ALT and survive scene/task controls.
- **Kill criterion:** random effects collapse, no interaction survives holdout, or gains disappear after matching scene/task geometry.
- **Admission verdict:** **ADMIT for design-only pilot planning; implementation remains unauthorized.**

## Stop condition

The substrate-first contract is satisfied at the retained shortlist. No candidate method was implemented, no runtime was installed, no large dataset or checkpoint was downloaded, and no simulator, GPU, or real-robot experiment was launched.

