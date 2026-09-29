# Tactile Behavioral Proxy Audit

Date: 2026-09-29  
Final gate: **PASS — TACTILE BEHAVIORAL PROXY**

This is a resource and measurement-identifiability gate. No dataset was downloaded, no runtime was installed, and no policy, simulator, or robot experiment was run.

## Decision

The public proxy is **task-disjoint offline action/trajectory evaluation on FreeTacMan**. The input contains synchronized wrist and visuo-tactile observations; the target contains time-aligned TCP pose/orientation and gripper distance trajectories. A small set of task categories can be selected without downloading the full release. The minimum comparison is vision-only versus vision-plus-tactile behavior cloning, evaluated on held-out episodes and held-out task categories where available. Report action error at multiple horizons and a trajectory-level distance such as normalized pose/gripper error; label this an offline behavioral proxy, not closed-loop task success.

This passes because the metric is downstream of tactile perception and measures the policy's predicted control sequence. It does not authorize a scientific method or claim that offline action error predicts real-robot success.

## Phase 1 resource audit

| Resource | Public data and license | Code / splits / checkpoints | Behavioral signal | Hardware dependence | Gate assessment |
|---|---|---|---|---|---|
| **RCT** | Public Figshare release; CC BY 4.0; 29,279 DIGIT frames, 1,832 press sequences, force/depth, material photos and descriptors | Public split-generation and evaluation code; no policy checkpoint or action trajectory | Tactile-to-text/vision retrieval, material/category probes; no action or task outcome | Collection used a robot arm and DIGIT sensors, but released files can be consumed without hardware | **Supporting resource only.** Strong leakage-controlled tactile benchmark, not a behavioral proxy by itself. |
| **HapTile** | Public project is described as synchronized fingertip tactile, vision, language, and action trajectories over contact-rich tasks; exact public download size/license were not independently verifiable in this audit | Paper reports two policy baselines, but public code/checkpoint/split details were not sufficiently verifiable | Action-conditioned imitation and policy benchmarking are claimed by the paper | Collection uses custom fingertip tactile sensors and haptic teleoperation; consumption may be hardware-free if files are released | **Promising but unverified.** Do not make it the sole substrate until download and split provenance are confirmed. |
| **ForeTac-VLA** | 2026 paper reports tactile forecasting and four real-world tasks; public data/code/checkpoint availability was not verified | Method and real-robot results are recent; reproducible public training/evaluation entry point not established here | Real-world task success in the paper, but not currently reproducible from confirmed public files | Requires tactile VLA setup and real manipulation for the reported result | **Prior work anchor only.** Not a current low-cost proxy. |
| **FreeTacMan** | Public Hugging Face release, MIT license, approximately 50.3 GB total; >10k trajectories / 50 tasks and >3M visuo-tactile pairs | Public GitHub code includes preprocessing, tactile pretraining, ACT policy training and inference; trajectory files expose task categories and TCP/gripper channels; no independent official task-disjoint split was found | Action prediction and trajectory-level imitation are directly measurable; source paper reports real policy success, but our proxy remains offline | Data were collected with a wearable/custom tactile system and motion capture, but no new hardware is required to consume released files | **Pass with scope restriction.** Use a small task subset and episode/task-disjoint split; do not claim closed-loop success. |

## Why FreeTacMan is behavioral

The target is an action trajectory, not a tactile label or embedding. Given an observation window, a policy predicts future TCP pose/orientation and gripper commands. Held-out action error and trajectory distance therefore test whether tactile input changes control-relevant prediction under a distribution shift. The proxy cannot establish contact completion, collision avoidance, or task success because there is no verified lightweight closed-loop environment for the released sensor stream. Those claims are explicitly out of scope.

## Minimum reproducible proxy

1. Download only a predeclared small subset of FreeTacMan task files, with byte counts and hashes recorded before use.
2. Split by complete episode; reserve at least one task category or object/configuration family for test if the metadata supports it. Never split adjacent frames across train and test.
3. Train a small vision-only BC baseline and a matched vision-plus-tactile BC baseline using the released preprocessing path. A frozen or low-capacity encoder is acceptable for the first gate.
4. Evaluate one-step and multi-step action error, normalized trajectory distance, and per-task confidence intervals across at least three seeds. Report the tactile marginal after matching observation history and parameter count as closely as practical.
5. Kill the proxy if task/episode identifiers are absent, if the selected subset cannot be separated without leakage, or if the tactile stream cannot be aligned to actions without undocumented calibration.

## Resource and reproducibility judgment

The full 50.3 GB release is larger than a one-day toy dataset, but it is still a finite public download and the official structure permits task-level selection. A minimum pilot can use a small predeclared subset; the full release is not required for the gate or for a first scientific question. Standard PyTorch is sufficient for a small BC model. No custom tactile hardware, proprietary data, simulator reconstruction, GPU-specific kernel, or real robot is required for the offline proxy.

The strongest objection is that offline action prediction can reward copying demonstrator trajectories without proving physical grounding. The protocol addresses this only partially through task/episode-disjoint splits and trajectory-level horizons. Any later paper must either add an independently validated closed-loop surrogate or narrow its claim to control-relevant offline generalization.

## Backup-space status

The cross-embodiment execution gap was not entered because the tactile gate passed. It remains the documented fallback if FreeTacMan subset access, leakage-resistant splitting, or action alignment fails during a later preflight. No cross-embodiment method search is authorized by this report.

## Reviewer gate

Fresh independent review: `gpt-6-astra / medium`, thread `/root/tactile_proxy_reviewer`, read-only and no downloads or experiments. The reviewer judged this a **conditional PASS for an explicitly offline behavioral proxy**, while rejecting any claim that action prediction is closed-loop success or causal physical grounding. The reviewer requires a frozen Git/Hugging Face revision, file hashes and byte counts, 3–5 contact-diverse tasks, complete-episode and object/task-disjoint splits, timestamp/calibration/frame audits, and matched RGB+proprio versus RGB+tactile BC controls. If action labels, timestamps, or leakage-resistant splits are absent, the gate must be downgraded to `FAIL — TACTILE BEHAVIORAL PROXY` before any pilot.

The reviewer’s strongest objection is that logged-action prediction may reward demonstrator style and have no monotonic relationship to task success; hidden sensor calibration and coordinate conventions are a second risk. These objections narrow the scientific claim and define the preflight kill rules; they do not invalidate the proxy category permitted by the commitment contract.

## Sources

- [RCT project and download](https://faerber-lab.github.io/RCT/)
- [HapTile paper](https://arxiv.org/abs/2606.04825)
- [ForeTac-VLA paper](https://arxiv.org/abs/2609.20980)
- [FreeTacMan project](https://opendrivelab.com/FreeTacMan)
- [FreeTacMan code](https://github.com/OpenDriveLab/FreeTacMan)
- [FreeTacMan dataset card](https://huggingface.co/datasets/OpenDriveLab/FreeTacMan)
