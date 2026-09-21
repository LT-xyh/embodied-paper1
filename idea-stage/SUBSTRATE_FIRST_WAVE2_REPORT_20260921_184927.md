# Substrate-First Research-Direction Reselection — Wave 2

**Date:** 2026-09-21 18:49 +0800
**Binding authority:** [`RESEARCH_BRIEF.md`](../RESEARCH_BRIEF.md) and [`SUBSTRATE_FIRST_WAVE2.md`](SUBSTRATE_FIRST_WAVE2.md)
**Scope:** public Embodied AI / Robot Learning artifacts available through September 2026; static selection only
**Execution status:** no candidate implementation, runtime installation, dataset/checkpoint download, simulator, GPU/DCU job, or real-robot experiment

## Decision

**Final shortlist: zero candidates.**

**Recommended next P0: `NO CANDIDATE`.** The current public substrates contain useful evidence, but every mechanism that could be tested cheaply either has a direct 2025–2026 prior, collapses to benchmark or data-collection QA, or cannot obtain independent first evidence without a large multimodal artifact or simulator. The contract explicitly prefers zero over padding a Top-2 list.

This is a research-selection result, not a claim that no future direction exists. A new reselection pass should wait for a genuinely independent small artifact or a new scientific question outside the accumulated negative-evidence families.

## 1. Evidence-Rich Substrate Landscape

The search began from executable public artifacts and then asked what falsifiable variable each artifact supports. No file was downloaded. Links below are primary dataset, project, or paper pages.

| Substrate | What is publicly documented | First-test boundary | Static decision |
|---|---|---|---|
| [VISTA-UMI-5K](https://huggingface.co/datasets/TeleEmbodied/VISTA-UMI-5K), [VISTA paper](https://arxiv.org/abs/2606.04708) | 5,000 UMI trajectories over 30 tasks in LeRobot v3.0; state/action and episode structure are exposed; the card reports 6,449,242 rows and 31.4 GB, and says trajectories were physically validated for three robot embodiments. | A state/action-only slice may be selectively readable, but the physical-validation labels and deployment target are part of VISTA's own contribution. A complete independent pilot would need validation metadata and/or replay outputs that are not shown as a small bounded artifact. | Substrate exists, but the obvious mechanism is already VISTA's claim and would be curation/benchmark analysis. Reject as a final direction. |
| [ManipArena](https://huggingface.co/datasets/ManipArena/maniparena-dataset) | 20 real-robot and 3 simulation bimanual tasks; LeRobot trajectories with 56-D tabletop or 62-D mobile state/action, plus language annotations; simulation counts were refreshed in May 2026. | Metadata/data can be selected without video, but the public training release is demonstration-heavy and does not expose a paired outcome/intervention variable sufficient for a new mechanism. | Good substrate for later baselines; the likely questions are benchmark or representation comparisons already covered by the release. Reject. |
| [AgiBot World 2026 Theme 3](https://www.agibot.com/article/231/detail/95.html), [dataset card](https://huggingface.co/datasets/agibot-world/AgiBotWorld2026) | The September release reports 11,430 real trajectories over 14 tasks, 1,024 successful and 1,369 failed policy rollouts, 98,159 subtask intervals, 26,493 disturbance segments, 5,795 error-state segments, and 10,684 human-intervention segments. The card exposes LeRobot episode/data/meta structure and recommends a roughly 7 GB sample. | Rich process labels exist, but no small byte-bounded non-video slice containing the state/action plus all intervention annotations was admitted. The full release is large and image-heavy; a first test would need careful sparse retrieval and schema verification. | High-value future substrate, but not a current 1–3 day admitted pilot. Candidate claims also collide with HIL credit assignment, progress, recovery, and failure-learning work. Reject. |
| [RSS 2026 Challenge Phase 1](https://huggingface.co/datasets/Cocoyawn32/Challenge-phase1-dataset) | Three bimanual YAM/GELLO tasks; 3,209 episodes and 8,635,032 frames at 60 Hz; expert, failure, and success-plus-HIL subsets; per-frame `observation.commander_state` identifies inference/teleop and the card documents a takeover discontinuity of up to about 0.2 rad per joint. The API-declared non-video payload for one `insert-mouse-battery/success-and-hil-data` subset is 33,280,178 bytes (31,847,026 data + 1,433,152 meta), before any download. | A CPU state/action boundary analysis is technically cheap and does not need video. A separate AGIBOT path exists in principle. | Strong substrate, but the apparent claim is a handoff artifact or intervention-credit correction. That is not sufficiently distinct from PACT/TRANSIC/HIL methods and would be viewed as dataset QA unless a new causal policy-learning result were demonstrated. Reject. |
| [PRISM](https://tengbo-yu.github.io/PRISM/), [paper](https://arxiv.org/abs/2608.17962) | 25+ industrial contact-rich tasks, more than 5,000 robot trajectories and an equivalent number of human demonstrations, three robot platforms, RGB-D, tactile, 6-axis force/torque, and proprioception; the release reports roughly 27M image frames. | The force/state channels are scientifically useful, but a small public state/force-only artifact and exact file sizes are not documented on the project page. Full multimodal use is not a small first substrate. | Temporal-rate or teleoperation-interface hypotheses would be sensor-fusion or data-quality comparisons already claimed in PRISM/related tactile work. Reject. |
| [Hoi!](https://bonndata.uni-bonn.de/dataset.xhtml?persistentId=doi%3A10.60507%2FFK2%2FQODWTV&version=1.0), [paper](https://arxiv.org/abs/2512.04884) | 3,048 sequences, 381 articulated objects, 38 environments, and four embodiments (human hand, wrist-camera hand, UMI gripper, Hoi! gripper) with synchronized force/tactile streams. The official repository says the dataset is too large to download and asks users to select files. | Cross-view force/action analysis would require a carefully selected multimodal subset and substantial synchronization checks. | Cross-embodiment contact/force transfer is directly adjacent to Hoi!, ViTacWorld, ForceVLA, Tactile-Force Alignment, and the brief's excluded contact-topology family. Reject. |
| [KinDER](https://arxiv.org/abs/2604.25788), [code](https://github.com/Princeton-Robot-Planning-and-Learning/kindergarden) | RSS 2026 benchmark with 25 procedurally generated environments, Gymnasium code, demonstrations, and 13 implemented baselines over five physical-reasoning families. | Any intervention that tests the proposed physical mechanism requires the KinDER simulator or generated environments. | Violates the no-simulator first-evidence boundary; its benchmark axes and baselines already define the obvious claims. Reject. |
| [HUI360](https://arxiv.org/abs/2608.11051) plus SSUP-HRI | 4,310 tracks, over 1M curated annotations, nine environments, and 6M annotations generated for the independent SSUP-HRI dataset; images are available on request. | CPU sequence models can run on annotations, but the object is human-interaction anticipation rather than a robot-learning mechanism. | A calibrated anticipation metric or location-shift result is benchmark/metric work, not a new embodied learning mechanism. Reject. |

The search also checked [ROBORMBENCH](https://arxiv.org/abs/2609.05401), [WANDA](https://wanda.lecar-lab.org/), [ViTacWorld](https://arxiv.org/abs/2607.22530), [OmniNavBench](https://github.com/AutoLab-SAI-SJTU/OmniNavBench), [NavSpace](https://github.com/TidalHarley/NavSpace), and [RW-RL-HIL-Dataset](https://huggingface.co/datasets/BodenAI/RW-RL-HIL-Dataset). Each either lands inside accumulated negative evidence (language/evaluator diagnosis, world-model/contact evaluation, generic recovery, or benchmark auditing) or violates the small-runtime gate.

## 2. High-Value Rejections

| Initial substrate-backed hypothesis | Decisive rejection |
|---|---|
| **Handoff discontinuity as a hidden label in human-in-the-loop post-training** (Challenge Phase 1 → AGIBOT World 2026) | The Challenge card exposes a real discontinuity, but the scientific delta is a controller-switch correction. [PACT](https://arxiv.org/abs/2606.03949) already uses intervention-induced preferences and progress-aware credit correction; [TRANSIC](https://proceedings.mlr.press/v270/jiang25a.html) already uses online correction for sim-to-real; [REIM](https://github.com/CC-robotics/REIM) and related 2026 work cover recovery and intervention deployment. A masking/weighting ablation would be a release QA or a standard HIL variant. |
| **Contact-event temporal-rate invariance** (PRISM → Hoi!/ViTacWorld) | PRISM itself makes synchronized force/tactile streams and interface comparisons a contribution. [ViTacWorld](https://arxiv.org/abs/2607.22530), [Tactile-Force Alignment](https://arxiv.org/abs/2601.20321), [FreeTacMan](https://opendrivelab.com/FreeTacMan), and Hoi! already establish multimodal contact grounding and alignment. A downsampling curve or lag metric would be a metric/sensor-fusion change; the full data path is also too large for the required first test. |
| **Embodiment-conditioned feasibility score transfer** (VISTA-UMI-5K → PRISM/ManipArena) | VISTA explicitly validates trajectories on three embodiments, uses embodiment-conditioned physical-validation scores, and reports that the scores predict deployment success. Relearning the same score or testing its threshold on another release is direct replication of the source paper or generic data curation. |
| **Process-level progress/value factorization from disturbance intervals** (AGIBOT World 2026 → Challenge Phase 1) | AGIBOT's release already makes subtask completion, errors, disturbances, and interventions the advertised learning signals. PACT, Guardian, REIM, and the broader HIL/recovery literature already target progress, risk, credit assignment, or correction. A lightweight value probe would be statistical association or generic recovery. |
| **Physical-reasoning factor curriculum** (KinDER → ManipArena) | KinDER already isolates five physical-reasoning axes and ships 13 baselines. A new curriculum or factor score would need the simulator and would be a benchmark method comparison. ManipArena does not provide a matching independent causal factor, so its replication path is not scientifically independent. |

Additional near-misses were rejected for the same reasons: [REBOOT](https://nanayawoa.github.io/REBOOT/) is explicitly a recovery-from-failure benchmark; [GRAPE](https://github.com/aiming-lab/GRAPE) already uses paired chosen/rejected trajectories; [OmniNavBench](https://github.com/AutoLab-SAI-SJTU/OmniNavBench) requires Isaac Sim/NVIDIA CUDA; and [RoboTacDex](https://arxiv.org/abs/2606.31836) is an announced dataset rather than a small, stable artifact with an independent mechanism test.

## 3. Candidate Hypotheses Before Aggressive Rejection

The following five hypotheses were generated only after the substrate scan. They are recorded so the next pass does not repeat the search, but none is a survivor.

### H1 — Boundary-aware intervention learning

Use `commander_state` to separate autonomous frames, pre-takeover transition frames, and human correction frames. Hypothesis: controller-switch discontinuities produce a distinct false-error signal; removing or modeling the boundary should improve offline action prediction and downstream correction transfer across Challenge Phase 1 and AGIBOT World 2026.

Primary substrate: one or more Challenge Phase 1 non-video task subsets. Independent path: AGIBOT World 2026 Theme 3 intervention segments. Minimum pilot: CPU state/action jump audit, boundary-masked versus boundary-aware linear/MLP action probes, leave-task-out and leave-subset-out error. Cost estimate: 0.5–1 day, tens of MB for one task plus sparse metadata. No simulator or policy inference is required.

**Decision:** reject. The boundary is a credible artifact, but the proposed scientific result is an intervention-data correction and is too close to PACT/TRANSIC/recovery work. A positive result would still be a dataset-collection QA result unless a full policy-learning consequence were added; adding that consequence violates the 1–3 day bounded gate.

### H2 — Contact-event sampling invariance

Use force/state streams from PRISM and a selected Hoi!/ViTacWorld-compatible subset to test whether contact-event detection and action prediction degrade discontinuously when high-rate force is resampled to camera/action rate. Hypothesis: the relevant variable is event aliasing, not total modality count, and a rate-aware lightweight encoder should transfer across tasks.

Primary substrate: PRISM force/torque and proprioception. Independent path: Hoi! or ViTacWorld public tactile/action data. Minimum pilot: event-window classification and next-state prediction at native, downsampled, and phase-aligned rates, with object/task holdouts. Cost estimate: 1–3 days if state/force-only slices are public; otherwise unbounded because the released multimodal artifact is large. No policy inference is needed.

**Decision:** reject. PRISM, Hoi!, ViTacWorld, TaF-VLA, and FreeTacMan already make synchronized contact sensing/alignment the central contribution. The remaining experiment is a rate/metric ablation and cannot clear the Wave-2 mechanism gate.

### H3 — Cross-embodiment feasibility as a deployment variable

Use VISTA's per-embodiment validation metadata and a second robot dataset to test whether a trajectory-quality score transfers only after conditioning on embodiment-specific reachability and collision margins. Hypothesis: a global quality score systematically misranks demonstrations under a new embodiment.

Primary substrate: VISTA-UMI-5K. Independent path: PRISM or ManipArena state/action data. Minimum pilot: compare global versus embodiment-conditioned score ranking on held-out tasks and robot families. Cost estimate: 1–2 days if validation fields are released; otherwise requires replay or the VISTA runtime. No new training is needed.

**Decision:** reject. VISTA already validates and ranks trajectories per embodiment and reports deployment predictivity. Any residual result is a direct source-paper replication or generic curation. This also approaches the accumulated mixed-quality/data-selection ban.

### H4 — Intervention-phase value decomposition

Use AGIBOT's subtask intervals, disturbances, errors, and human interventions to test whether process-level labels improve offline value estimation over terminal success. Hypothesis: disturbance-conditioned phase labels identify where a policy loses recoverability earlier than terminal outcomes.

Primary substrate: AGIBOT World 2026 Theme 3. Independent path: Challenge Phase 1's failure/success/HIL subsets. Minimum pilot: terminal-only versus phase-supervised CPU value/progress probe under task holdout and intervention-time calibration. Cost estimate: 1–3 days if annotation/state slices are small. No simulator or VLA inference is required.

**Decision:** reject. This is generic progress/risk/recovery learning, explicitly crowded by PACT, Guardian, REIM, and the accumulated negative evidence. The labels are the dataset's advertised contribution; the pilot would be benchmark analysis unless a new deployment mechanism were added.

### H5 — Physical-reasoning factorization across substrates

Use KinDER's factor-isolated tasks and ManipArena's bimanual tasks to test whether a factorized state/action representation predicts failure transfer across constraint families better than task-specific BC.

Primary substrate: KinDER demonstrations and benchmark metadata. Independent path: ManipArena simulation tasks. Minimum pilot: CPU behavior-cloning probes on released demonstrations, factor holdouts, and task/embodiment transfer. Cost estimate: at least 2–3 days plus benchmark setup. KinDER's causal test requires its simulator; ManipArena's factors do not match KinDER's five axes.

**Decision:** reject. The primary artifact is a simulator benchmark, which violates the no-simulator first-evidence rule, and the independent path is not an independent measurement of the same mechanism. Any score improvement would be a benchmark/representation change.

## 4. Closest 2025–2026 Prior Audit

| Candidate | Exact prior claim | What the prior already solves | Non-overlapping claim considered | Distinguishing experiment | Difference type | Outcome |
|---|---|---|---|---|---|---|
| H1 boundary-aware intervention learning | PACT (2026) uses intervention-induced preferences and a progress model to reassign credit; TRANSIC (CoRL 2025) learns residual policies from online correction; REIM (2026) trains recovery with intervention-risk triggers. | Intervention timing, correction actions, and recovery credit are already operationalized. | The Challenge's documented controller-switch jump could be a data-generation artifact that contaminates the transition label. | Mask/retain boundary frames and test held-out action/value transfer across two independently released HIL datasets. | A mechanism-shaped data issue, but the proposed remedy is a standard preprocessing/control correction and would be benchmark QA without deployment evidence. | Reject. |
| H2 contact-event sampling invariance | Hoi! (CVPR 2026) provides force-grounded cross-view articulated manipulation; ViTacWorld (2026) predicts action-conditioned visuo-tactile outcomes; TaF-VLA (2026) aligns tactile observations with force. | Multimodal contact grounding, synchronization, and tactile-force representation are already solved at the method level. | High-rate contact-event aliasing could explain cross-task transfer failures independently of modality count. | Native versus downsampled force/state event probes on PRISM and Hoi!/ViTacWorld. | Mostly a sampling/metric ablation; no distinct learning mechanism remains. | Reject. |
| H3 embodiment-conditioned feasibility | VISTA (2026) replays UMI trajectories on three embodiments, computes embodiment-conditioned physical-validation scores, and reports deployment predictivity. | Physical feasibility scoring and cross-embodiment data curation are already the claimed contribution. | A global score might fail under a genuinely unseen embodiment even when validation quality is high. | Re-rank the same trajectories across a second public release with reachability-aware controls. | Direct replication / data-selection heuristic, not a new mechanism. | Reject. |
| H4 intervention-phase value | AGIBOT World 2026 advertises subtask completion, disturbance, error, and intervention annotations; PACT (2026) explicitly corrects terminal credit using progress and intervention preferences; Guardian/REIM cover failure reasoning and recovery. | Fine-grained process feedback and recovery-oriented value learning are already covered. | A phase boundary could be a transferable recoverability state variable beyond terminal reward. | Train terminal-only and phase-supervised probes with task holdout on AGIBOT and Challenge. | Statistical association or generic progress/recovery method. | Reject. |
| H5 physical-reasoning factorization | KinDER (RSS 2026) isolates five physical-reasoning families and ships 13 baselines; ManipArena (CVPR 2026 workshop) supplies bimanual tasks and language annotations. | Factor-isolated benchmark evaluation and baseline comparison already exist. | A shared representation might transfer constraint structure across task families. | Cross-factor BC on KinDER demonstrations and ManipArena simulation tasks. | Benchmark/representation change; simulator-dependent. | Reject. |

None of the five has a non-overlapping claim that remains scientifically meaningful after the closest prior is granted. The mandatory negative families in `RESEARCH_BRIEF.md` were not revived: no segment filtering, visual/language shortcut diagnosis, generic VLA safety, generic world-model evaluation, common-random-number comparison, recovery/retry, active factor evaluation, contact-topology transfer, Armnet leakage, or SocNav rater modeling is retained.

## 5. Replication Admission

The candidate paths were checked before ranking. A second release was required to expose the same scientific variable, not merely another robot dataset.

| Candidate | Primary substrate | Independent path | Same variable available? | Admission |
|---|---|---|---|---|
| H1 | Challenge Phase 1 `commander_state`, state/action, HIL subsets | AGIBOT World Theme 3 intervention segments | Broadly yes, but the AGIBOT boundary schema and transition semantics are not yet verified in a small slice | Not admitted after prior collision |
| H2 | PRISM force/torque + state | Hoi! or ViTacWorld visuo-tactile-action streams | Partially; sensor rates, tasks, and labels differ, and selected file sizes are not bounded | Not admitted |
| H3 | VISTA physical-validation scores and UMI trajectories | PRISM or ManipArena | No: the independent releases do not expose the same VISTA validation score/embodiment replay fields | Fails hard replication gate |
| H4 | AGIBOT process annotations | Challenge failure/HIL metadata | Broadly yes, but both paths are HIL/recovery data and the mechanism is already covered | Not admitted after prior collision |
| H5 | KinDER factor-isolated simulator tasks | ManipArena simulation tasks | No: task factors and outcome definitions are not shared | Fails hard replication gate |

Thus no candidate reaches the final ranking. A dataset from the same release family, a train/test split, or a second task subset was not counted as independent replication.

## 6. Static Execution Admission

No final candidate passes all required fields. The following checks explain why:

| Candidate | Exact files/fields | Download/storage | Policy inference | Simulator | CUDA/runtime | First evidence |
|---|---|---|---|---|---|---|
| H1 | Challenge `meta/{info,episodes,episodes_stats,tasks}.jsonl`, `data/*.parquet`, `observation.commander_state`, joint state/action; AGIBOT episode/subtask/intervention annotations | One Challenge task's API-declared non-video subset is about 33.3 MB; AGIBOT complete state/annotation slice not bounded | No | No | NumPy/PyArrow CPU is enough | 0.5–1 day, but scientific novelty fails |
| H2 | PRISM force/torque, proprioception, timestamps; Hoi!/ViTac tactile/force/action streams | Full releases are multimodal and large; a <=100 MB state/force subset is not documented | No | No | CPU possible after extraction | 1–3 days only if selective files are published; current artifact gate fails |
| H3 | VISTA state/action plus physical-validation/replay fields | VISTA card reports 31.4 GB total; required validation fields and target-embodiment replay are not a small verified slice | No for offline probe | Replay/runtime likely required | VISTA pipeline includes MuJoCo/Mink replay | Not admitted |
| H4 | AGIBOT `episodes`, subtask, disturbance, error, intervention annotations plus state/action | Full release/sample is large; no bounded first slice verified | No | No for probe, but data conversion is nontrivial | CPU possible | 1–3 days only after schema and size audit; prior collision kills it |
| H5 | KinDER demonstrations, factor metadata, environment/task definitions | Dataset/checkpoint links public | No | Yes, for the causal factor test | Gymnasium environment setup | Beyond the no-simulator gate |

No simulator, GPU/DCU job, VLA inference, checkpoint, heavy runtime, or download was started. The exact API-size observation for the Challenge subset is metadata only and contributes zero downloaded bytes.

## 7. Final Shortlist: at most Top-2

**Zero survivors.** There is no candidate name to recommend. Retaining H1 or H4 would revive generic HIL/recovery or benchmark QA; retaining H2 or H3 would revive crowded contact/cross-embodiment data-curation claims; retaining H5 would violate the simulator gate and lack independent variables.

The strongest available substrates for a later, separately authorized search are AGIBOT World Theme 3 and the RSS Challenge Phase 1 dataset. They are recorded as substrate leads only, not as directions. Any future proposal must introduce a mechanism outside the accumulated negative list and must first prove a small, non-video, independently replicated artifact slice.

## 8. One Recommended Next P0

**`NO CANDIDATE`.** Do not start a P0 automatically. Do not implement H1–H5. A future pass should re-open only after a new independent release exposes either (a) a non-HIL paired intervention mechanism with a bounded state/action artifact or (b) a new cross-domain variable whose closest 2025–2026 prior is not a benchmark, data-curation, contact, recovery, or evaluator diagnosis paper.

## Reproducibility and source boundary

All evidence in this report came from public dataset cards, official project pages, official repositories, and arXiv abstracts/pages. No local research file was modified before this report, no web artifact was downloaded, and no claim relies on a hidden checkpoint or simulator run. The report is a design-only reselection record; it does not authorize implementation or experiments.
