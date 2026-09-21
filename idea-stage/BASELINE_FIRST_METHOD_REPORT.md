# Baseline-First / Method-First Research Report

**Date:** 2026-09-21 20:59 +0800
**Binding authorities:** [`RESEARCH_BRIEF.md`](../RESEARCH_BRIEF.md), [`BASELINE_FIRST_METHOD_SEARCH.md`](BASELINE_FIRST_METHOD_SEARCH.md), [`OVERNIGHT_RESEARCH_CONTRACT.md`](../OVERNIGHT_RESEARCH_CONTRACT.md)
**Branch:** `aris/overnight-baseline-first-20260921`
**Stage-1 decision:** **`NO CANDIDATE`**
**Scope:** method-level robot-learning search through September 2026; no candidate implementation or scientific pilot

## 1. Executable Baseline Landscape

The search started from maintained training and evaluation stacks rather than from a new dataset phenomenon. Primary documentation and repository tags were checked without cloning or downloading data.

| Stack and revision | Python and runtime | CPU/headless and kernel gate | Dataset/checkpoint boundary | Smallest meaningful control test | Admission |
|---|---|---|---|---|---|
| [`robomimic`](https://github.com/ARISE-Initiative/robomimic) `v0.5.0` (`ae5799f`) + [`robosuite`](https://github.com/ARISE-Initiative/robosuite) `v1.5.2` (`824ac14`) + MuJoCo | robomimic's maintained Docker path documents Python 3.9; robosuite documents Python 3.10 and MuJoCo Python bindings. | Headless training with or without a GPU is documented; low-dimensional observations need no renderer, FlashAttention, Triton, Isaac, or custom CUDA. | The robomimic Hugging Face card reports `v1.5/lift/mh/low_dim_v15.hdf5` at 50.7 MB. No checkpoint is required for BC. | Lift or Can low-dimensional state/action BC, then closed-loop success in the native robosuite task. | **Conditionally admitted primary stack.** A pre-existing environment passed an import plus state-only reset/one-step smoke check; its NumPy warning requires a clean isolated environment before any future pilot. |
| [`Meta-World`](https://github.com/Farama-Foundation/Metaworld) `v3.1.1` (`7ea2b501`) + Gymnasium/MuJoCo | `>=3.10,<3.14`; the release pins MuJoCo 3.3.0 and Gymnasium. | The API exposes state observations and synchronous MT1/MT10/MT50 paths; CPU state execution is plausible and no NVIDIA-only path is required. | No dataset or checkpoint is needed for online state-policy training; exact training code is external to the environment package. | MT1 reach/push or ML1 train/test goal variation with success/return. | **Backup candidate stack.** It was not installed in the current base environment, so no scientific candidate could claim an independently exercised path this round. |
| [`Minari`](https://github.com/Farama-Foundation/Minari) `v0.5.4` (`d234142`) + Gymnasium-Robotics | `>=3.11`; NumPy 2, Gymnasium, and optional HDF5/Arrow/Hugging Face extras are specified in `pyproject.toml`. | Offline episode iteration is CPU-only; policy learning and closed-loop evaluation require a second algorithm/environment stack. | Dataset sizes are selected per Minari release; no dataset was downloaded. Minari is a format/library, not a complete policy baseline. | Load a small offline episode set, train an existing BC/IQL implementation, and evaluate in a matching environment. | **Rejected as a standalone baseline.** It does not by itself supply the policy learner and adds an untested integration boundary. |
| [`LeRobot`](https://huggingface.co/docs/lerobot/index) `v0.6.1` (`7e241bd`) | `>=3.12`; core pins include PyTorch 2.7+, torchvision, NumPy 2, OpenCV, and dataset/video extras. | The library exposes ACT and other policies and can evaluate in simulation, but the documented dataset format is synchronized video plus action/state. Video decoding, ffmpeg/torchcodec, and policy extras are additional runtime surfaces. | Existing datasets are streamed from the Hub; a small state-only artifact and exact checkpoint size were not established. | ACT on a small simulation dataset with policy rollout success. | **Rejected for this overnight pass.** It is mature, but the first reproducible path here is video/data-loader heavy and the current DCU environment lacks a clean LeRobot training dependency set. |
| [`ManiSkill`](https://github.com/mani-skill/ManiSkill) `v3.0.1` (`a4a4f927`) | Python version is environment-dependent; installation requires SAPIEN and Vulkan setup. | CPU simulation is supported for one environment, but the official support table and installation path expose Vulkan/SAPIEN integration risk; parallel GPU simulation is a separate path. | Demonstrations and benchmark assets are public; no asset was downloaded. | One state-mode task with reset/step/evaluate, then a policy rollout. | **Rejected for the overnight baseline.** The Vulkan/bootstrap surface is unnecessary when robosuite already provides a simpler state-only path. |

The conditional primary stack is scientifically useful because the same low-dimensional policy can be trained and evaluated with a real success metric. The smoke check used the pre-existing `/public/home/xuyinghao/tmp/shiftvla-libero-dcu` environment (`robomimic 0.2.0`, `robosuite 1.4.0`, MuJoCo 3.7.0, Torch 2.7.1 with DCU build), with rendering disabled. It completed `Lift/Panda` reset and one zero-action step. This was a runtime compatibility check, not a method experiment. A NumPy 2.2.6 versus compiled NumPy 1.x warning was recorded and no repair was attempted.

## 2. Rejected Baselines and Exact Runtime Reason

| Baseline | Exact reason for rejection or deferral |
|---|---|
| LeRobot v0.6.1 | The smallest documented policy path still crosses the LeRobotDataset/video stack and optional `av`/torchcodec/diffusion dependencies. It is not a clean state-only first pilot on the current environment, and a large VLA checkpoint is unnecessary for the method question. |
| ManiSkill v3.0.1 | The state path can be CPU-only, but installation requires SAPIEN/Vulkan setup and creates a second simulator bootstrap surface. The contract rejects this when a mature MuJoCo path is already available. |
| Minari v0.5.4 alone | Minari supplies storage and episode iteration, not a complete policy-training/evaluation method. Combining it with an unverified learner would make infrastructure the first result. |
| Meta-World v3.1.1 | It remains a plausible independent evaluation path, but it was not installed or smoke-tested in the existing environment. It is therefore recorded as a backup, not as evidence for a candidate. |
| robomimic v0.5.0 as an immediate install | The public release is admitted in principle, but the current environment contains an older robomimic/robosuite pair and a NumPy ABI warning. No package replacement or system-level repair is authorized when Stage 1 has no surviving scientific method. |

## 3. Admitted Baseline Stack(s)

The only admitted primary baseline is:

* **Policy:** robomimic low-dimensional BC or BC-RNN, with the unmodified standard training and rollout scripts.
* **Environment:** robosuite `v1.5.2` and MuJoCo Python, headless state observations.
* **Primary task:** Lift low-dimensional; Can or Square is the second task if the first pilot is healthy.
* **Primary artifact:** `v1.5/lift/mh/low_dim_v15.hdf5`, 50.7 MB as documented by the public dataset card.
* **Policy metric:** closed-loop task success, with episode return and action error only as secondary diagnostics.
* **Compute path:** CPU first; standard PyTorch only; one DCU could be used later only after a healthy CPU smoke test.
* **Independent path:** Meta-World MT1/ML1 state tasks, or robomimic Can/Square with a held-out task family, depending on the admitted method.

This is a conditional baseline admission, not an implementation authorization. Because no method candidate passed the scientific and replication gates below, Stage 2 was not entered.

## 4. 2025–2026 Method-Gap Landscape

The following primary works were used as closest-prior anchors. The search was deliberately method-first and excluded the accumulated negative families in `RESEARCH_BRIEF.md`.

| 2025–2026 work | Exact method claim | Consequence for a small robomimic/Meta-World method |
|---|---|---|
| [Compose Your Policies!](https://proceedings.iclr.cc/paper_files/paper/2026/hash/f7fc38fdd95fd146a471791b93ff9f12-Abstract-Conference.html), ICLR 2026 | General Policy Composition combines distributional scores of multiple pretrained diffusion/flow policies at test time and reports gains on Robomimic, PushT, RoboTwin, and real robots. | A state-policy ensemble/composition pilot would be a direct reimplementation or modality substitution. |
| [Beyond Imitation: Self-Improving Robot Policies via Off-Policy Q-Planning](https://arxiv.org/abs/2608.21204), 2026 | A frozen BC policy proposes action chunks while a small Q-function scores them and absorbs successful and failed deployment rollouts for self-improvement. | A low-dimensional frozen-BC plus Q selector is the same mechanism, while the published method already supplies the policy-level claim. |
| [Action-Effect Memory Pretraining](https://arxiv.org/abs/2606.12499), 2026 | Interleaved vision/action history is masked and compressed into a compact action-effect memory injected into Diffusion Policy and ManiFlow; gains are shown on RoboTwin2.0, RMBench, and real robots. | Replacing vision with state and using a small auxiliary predictor would be a narrow architecture ablation without an independent mechanism. |
| [Improving Robotic Imitation Learning via Trajectory Standardization](https://arxiv.org/abs/2606.22907), 2026 | Information-standardized resampling uses velocity/acceleration to replace uniform downsampling and reports policy success gains and lower training cost. | Temporal resampling is already a method-level preprocessing claim and is too close to the accumulated data-selection/preprocessing negative family. |
| [Set-Supervised Diffusion Policy](https://set-supervised-diffusion-policy.github.io/), RSS 2026 | Contrastive positive/negative action chunks from human corrections train a diffusion policy to use intervention feedback. | A correction-pair loss on robomimic would revive HIL correction or boundary cleanup rather than supply a new mechanism. |
| [ActionFlow](https://www.dfki.de/en/web/research/projects-and-publications/publication/15720) and [Equivariant diffusion policy](https://journals.sagepub.com/doi/abs/10.1177/02783649261424445), 2024/2026 | Spatial symmetry/equivariance is built into generative robot policies and evaluated on manipulation tasks. | A small equivariant head is a direct architectural replication and would require a geometry/vision implementation path not justified by the overnight gate. |
| [Demystifying Robot Diffusion Policies](https://proceedings.iclr.cc/paper_files/paper/2026/hash/122ea6470232ee5e79a2649243348005-Abstract-Conference.html), ICLR 2026 | Diffusion policies are shown to behave like action retrieval; an explicit Action Lookup Table matches performance and supplies OOD-distance detection. | Retrieval-plus-residual or nearest-neighbor policy proposals are already covered at the mechanism level. |

## 5. Candidate Methods

Five candidates were considered after the baseline admission. They were deliberately small enough to test in 1–3 days, but none survived the direct-prior and independent-replication audit.

### C1 — State-only action-effect memory for BC

* **Hypothesis:** a compact encoder of recent `(state, action)` history, trained to predict the next state and action, improves closed-loop success on partially observed manipulation compared with BC-RNN using the same parameter budget.
* **Method change:** add a small causal history encoder and an auxiliary next-state/action loss; keep robomimic's BC action head and rollout code unchanged.
* **Pilot:** Lift and Can low-dimensional tasks, with held-out initial states and success as the primary metric; Meta-World ML1 would test goal variation.
* **Cost:** approximately 1–2 CPU/DCU days after the baseline is installed; no vision or checkpoint is needed.
* **Decision:** reject. AEM already claims action-effect history pretraining as a transferable policy representation, while Mamba/full-history policy work covers the temporal mechanism. The state-only version changes modality and scale, not the scientific mechanism.

### C2 — Distribution-level composition of state policies

* **Hypothesis:** combining action distributions from independently trained BC policies improves success on states where either parent policy is locally uncertain.
* **Method change:** a test-time composition operator over two standard robomimic BC heads, with no additional policy training.
* **Pilot:** train two seeds or task-specialized policies on Lift/Can; compare each parent, greedy selection, and composition by closed-loop success and action smoothness.
* **Cost:** less than one day once policies exist; no extra data.
* **Decision:** reject. General Policy Composition (ICLR 2026) already claims the same test-time distribution-level composition mechanism and evaluates Robomimic. A state-only composition would be a direct replication.

### C3 — Frozen BC plus a low-dimensional Q selector

* **Hypothesis:** a lightweight Q-function can select among frozen BC action proposals and improve rollout success using failed episodes without updating the actor.
* **Method change:** add a critic and proposal scoring to robomimic BC; retain the actor.
* **Pilot:** Lift/Can offline demonstrations plus bounded simulated rollouts, measuring success before and after Q updates and against filtered SFT.
* **Cost:** 1–3 days, but it requires an online rollout loop and careful reward/reset handling.
* **Decision:** reject. Q-Planning (2026) states and tests this exact frozen-BC/Q-only self-improvement mechanism, including failure rollouts. The large-VLA scale is not the only overlap; the core scientific claim is already taken.

### C4 — Information-weighted state trajectory resampling

* **Hypothesis:** resampling state/action trajectories by velocity and acceleration information improves closed-loop success at a fixed training-step budget.
* **Method change:** replace uniform temporal sampling in the standard BC dataloader.
* **Pilot:** robomimic Lift/Can with fixed-step training and success/episode length as policy metrics; Meta-World reach/push as an external path.
* **Cost:** less than one day and CPU-only.
* **Decision:** reject. ISR (2026) already makes this exact velocity/acceleration-based resampling claim. It is also a data preprocessing result adjacent to the accumulated data-selection ban, not a distinct policy-learning mechanism.

### C5 — Contrastive correction loss for action chunks

* **Hypothesis:** paired undesired and corrected action chunks can improve policy success without discarding the negative action.
* **Method change:** add a set/contrastive loss to a diffusion or chunked BC head.
* **Pilot:** requires paired human corrections or a controlled intervention generator, then closed-loop insertion/assembly success.
* **Cost:** at least 2–3 days plus correction data and a reliable intervention environment.
* **Decision:** reject. SDP (RSS 2026) already claims the method and uses paired correction chunks; the remaining delta is HIL data handling, explicitly excluded by the negative-evidence contract.

## 6. Closest-Prior Rejection

| Candidate | Exact prior claim | What the prior already solves | Non-overlapping claim considered | Distinguishing experiment | Difference type | Gate result |
|---|---|---|---|---|---|---|
| C1 state-only action-effect memory | AEM (2026) learns compact interleaved vision/action history with masked action-effect reconstruction and injects it into policies. | Temporal interaction representation and downstream policy gains are already demonstrated across policy families and non-Markovian tasks. | A smaller state-only auxiliary loss might produce the same gain without visual pretraining. | Compare BC-RNN and the auxiliary model on robomimic plus Meta-World held-out goals. | Modality/scale ablation, not a new mechanism. | Reject. |
| C2 state-policy composition | GPC (ICLR 2026) composes distributional scores of multiple diffusion/flow policies at test time and reports Robomimic gains. | Test-time policy composition and its policy-level benefit are already claimed. | The same operator might work for lightweight state BC heads. | Parent-versus-composed closed-loop success on Lift/Can and Meta-World. | Direct replication with a smaller policy family. | Reject. |
| C3 frozen BC plus Q selector | Q-Planning (2026) freezes BC, scores sampled action chunks with Q, and improves from failed rollouts by Q-only updates. | The actor/critic asymmetry and failure absorption mechanism are already solved. | A small state-only version could isolate the mechanism from large VLA capacity. | Frozen BC, Q selector, filtered SFT, and success after bounded online rollouts. | Scale reduction, not a non-overlapping scientific claim; also online-loop dependent. | Reject. |
| C4 information-weighted resampling | ISR (2026) uses velocity/acceleration information to resample trajectories and reports policy success gains. | The preprocessing mechanism and control consequence are already claimed. | A state-only robomimic study could test whether the result survives without real-robot video. | Fixed-step BC with uniform versus information-weighted sampling and rollout success. | Dataset/preprocessing transfer. | Reject. |
| C5 correction-set loss | SDP (RSS 2026) trains diffusion policies from paired undesired and human-corrected action chunks. | Contrastive correction supervision and its success benefit are already demonstrated. | A simulator-generated pair would remove human intervention. | Generate paired alternatives in robosuite and compare chunk losses. | HIL replacement/data-generation variant; directly within a banned family. | Reject. |

No candidate has a method-level delta that remains after granting its closest prior. The failures are named prior collisions, not generic statements that the area is crowded.

## 7. Static Pilot Design

The table below records the smallest falsification experiment that would have been run if each method had passed. None was implemented or run.

| Candidate | Baseline/task | Policy/control metric | Positive criterion | Kill criterion | Independent path | Status |
|---|---|---|---|---|---|---|
| C1 | robomimic BC-RNN on Lift and Can | mean closed-loop success over fixed-seed rollouts | at least 10 percentage points on both tasks with no success loss on a held-out initial-state split | no improvement on either task or gain only in action MSE | Meta-World ML1 goal variation | Not admitted after AEM prior |
| C2 | two robomimic BC policies on Lift/Can | success and episode return | composition improves both parent policies on held-out seeds | composition no better than the best parent | Meta-World MT1/ML1 | Not admitted after GPC prior |
| C3 | robomimic BC plus Q selector on Lift/Can | success after bounded simulated rollouts | monotonic success gain from failures over frozen BC and filtered SFT | no gain after two Q update rounds or instability | Can/Square or Meta-World | Not admitted after Q-Planning prior |
| C4 | robomimic BC dataloader on Lift/Can | success at fixed optimizer steps | at least 10 percentage points with equal sample and compute budgets | no success gain or gain disappears under task holdout | Meta-World reach/push | Not admitted after ISR prior |
| C5 | chunked BC/diffusion on a correction-pair task | task success and correction count | success gain at equal positive-label count | no gain or requires HIL boundary cleanup | independent correction dataset | Not admitted after SDP prior and HIL ban |

The conditional robomimic stack passed only a compatibility smoke test:

```text
MUJOCO_GL=disable
robosuite Lift / Panda / OSC_POSE
has_renderer=False, has_offscreen_renderer=False, use_camera_obs=False
reset -> state observation -> one zero-action step -> close
```

It returned the expected state keys and a finite reward. This is not evidence for any candidate method. No dataset, checkpoint, simulator modification, policy training, rollout evaluation, GPU job, or DCU job was started.

## 8. Final Shortlist: at most Top-2

**Zero candidates survive.** The conditional baseline is executable, but no method candidate simultaneously clears:

1. a non-overlapping 2025–2026 method claim;
2. a real policy/control metric;
3. a concrete independent second evaluation path; and
4. the overnight runtime and negative-evidence gates.

`AUTO_PROCEED=true` cannot override this scientific stop. No Stage 2 implementation, auto-review loop, or paper-writing stage is authorized.

## 9. Recommended next P0

**`NO CANDIDATE`.** Do not start a P0 automatically. A future pass may reuse the conditional robomimic stack only after a new method hypothesis has a named non-overlapping prior delta and a second benchmark that tests the same mechanism. Do not revive trajectory filtering, HIL boundary cleanup, generic recovery/Q selection, action-chunk scheduling, contact transfer, world-model evaluation, Armnet leakage, or SocNav rater modeling.

## Reproducibility and source boundary

All literature and runtime claims were checked against primary project pages, repository tags, package metadata, official dataset cards, and primary 2025–2026 papers or project pages. No arXiv PDF was downloaded. No dataset or checkpoint was downloaded. The only executed code was the pre-existing state-only robosuite reset/step smoke check described above. The report is a Stage-1 selection artifact and does not claim Paper-1 acceptance.
