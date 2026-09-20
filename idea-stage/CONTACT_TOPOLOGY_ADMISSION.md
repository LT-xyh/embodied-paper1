# Pre-Implementation Admission Audit: Contact-Topology Transfer Boundary

**Contract:** [`RESEARCH_BRIEF.md`](../RESEARCH_BRIEF.md) is binding.

**Audit date:** 2026-09-20

**Scope:** read-only novelty and execution admission audit for the retained direction. No code, environment, checkpoint, simulator, GPU job, or external repository was changed or started.

## Verdict

**PIVOT**

The proposed failure-boundary claim is narrower than the average-transfer claims in the literature, but it is not yet a defensible Paper-1 novelty gap under a strict standard. The direct 2026 neighborhood now contains contact-pattern intent, contact-flow conditioning, interaction-graph retargeting, contact-consistent reconstruction, and morphology-aligned cross-hand policies. A paper that only adds a graph mismatch score would be a terminology or metric change. The stronger causal claim would require a controlled intervention on *realizable* contact transitions and held-out transfer failures.

The cheapest public substrate does not provide that pilot within the project constraints. BAR-X is the closest artifact, but its public HDF5 schema lists actions, simulator states, observations, and representation annotations—not contact arrays or success/failure labels—and its policy evaluation is pinned to NVIDIA CUDA 12.1 and FlashAttention 2.5.5. Recovering contact transitions from states therefore requires RoboCasa/MuJoCo replay, while measuring transfer failure requires policy inference or released per-rollout outcomes. That is a runtime and CUDA gate, rather than a 1–3 day offline pilot.

This direction is not implementation-authorized. The first-pass and second-pass candidate reports remain non-authorizing.

## Claim under audit

The only admissible scientific claim was:

> After controlling for visual appearance, task identity, end-effector trajectory/representation quality, and ordinary morphology/kinematic distance, mismatch in realizable contact-mode transitions between source and target embodiments predicts a systematic transfer failure boundary.

The claim is admissible only if “contact topology” is an operational, target-capability variable and the result is a controlled, out-of-sample failure law. “Contact matters,” “topology matters,” a new contact metric, a contact-aware controller, a new representation, or a benchmark wrapper is insufficient.

## Mandatory prior-work audit

The table records the variable each work actually studies, the contact information it uses, its control structure, and the remaining distinction. “No boundary” means that the work reports transfer success, quality, or robustness; it does not establish a conditional failure threshold after the controls in the proposed claim.

| Work | Variable actually studied | Contact topology or modes | Transfer result and controls | Does it already establish the proposed mechanism? | Remaining distinction and risk |
|---|---|---|---|---|---|
| [CEI: Unified Interface](https://arxiv.org/abs/2601.09163) | Functional similarity (Directional Chamfer Distance), FK trajectory alignment, synthesized observations/actions. | Manually selected functional points/directions; no discrete contact-mode transition graph. | Transfer across 16 simulated embodiments and real gripper/hand tasks; compares alignment ablations, not a failure boundary. | **No**, but it already explains failures as unstable geometry/contact and shows task/embodiment difficulty. | A conditional transition-capability law could differ, but it must beat CEI while holding its functional alignment fixed; otherwise it is a new metric. |
| [BAR-X / Behavior-Aligned Representations](https://arxiv.org/abs/2607.27549) | Language motions, end-effector traces, and object boxes as VLA auxiliary representations. | No contact topology; EEF traces can correlate with contact without identifying feasible modes. | RoboCasa-X cross-embodiment transfer and sim-to-real progress; representation/data-size ablations, no contact intervention or failure law. | **No.** | The candidate must show where BARs cease to transfer after EEF quality and morphology are matched; a contact feature appended to BAR-X is only a metric/feature change. |
| [Transferring Contact, Not Just Motion](https://arxiv.org/abs/2606.15516) | Calibrated force-position interface, per-finger load descriptors, and compliant control. | Contact load/force is explicit; no source-target transition-feasibility boundary. | Cross-hand compliant grasping with calibrated sensing and a hybrid force-position controller; force is a required modality. | **No**, but it establishes that contact feedback can improve cross-hand transfer. | A sensor-free diagnostic would be narrower, but must show predictive capability before force control; otherwise it is an offline contact metric. |
| [Cloak](https://tml.stanford.edu/cloak/) | Removing the end-effector from wrist-view attention; FK/IK retargeting. | No contact modes; explicitly removes visual embodiment cues. | Zero-shot transfer to unseen grippers, arms, and hands; source-vs-unseen comparisons, not contact-controlled failures. | **No.** | A topology effect after visual masking would be distinct only with matched trajectories and a target capability intervention. |
| [TopoRetarget](https://arxiv.org/abs/2606.16272) | Sparse hand-object interaction graph, Laplacian deformation, directional/kinematic/non-penetration constraints. | Yes: which keypoints touch and local interaction relationships. | Contact precision/alignment, penetration, Pen-Spin learning, and zero-shot Wuji transfer; no causal failure boundary. | **No**, but it already preserves a contact graph during retargeting. | The candidate must predict residual failures when the desired graph is infeasible; using its graph as the proposed variable without a boundary is overlap. |
| [GraspGraphNet](https://arxiv.org/abs/2607.11031) | URDF-derived hand graph, forward kinematics, dynamic world-edge message passing, executable grasp pose/joint state. | Topology-aware kinematic graph and evolving robot-object edges. | Multi-hand and finger-removal grasp success; no controlled source-target failure boundary or visual controls. | **No**, but it shows topology-aware policy generation can handle hand variation. | A residual transition boundary must predict failure beyond its graph-conditioned policy; otherwise it is another graph representation. |
| [CEDex](https://arxiv.org/abs/2509.24661) | Human-like contact representation, topological merging, SDF/physics-aware grasp optimization. | Contact maps/representations, mainly for single-grasp synthesis. | 500K-object/four-gripper grasp generation and validation; no temporal mode graph or transfer-failure law. | **No**, but it covers contact-map-to-grasp transfer. | A transition-level claim must be temporal and predictive, not a different contact map for grasp synthesis. |
| [HOWTransfer](https://arxiv.org/abs/2606.10743) | 3-D hand motion, temporal contact intervals, grasp hypotheses, and trajectory edits from video. | Contact onset/intervals; not a target feasibility graph. | 86% trajectory-transfer success and preference study; no morphology/visual/kinematic causal isolation. | **No**, but contact timing is already a transfer signal. | A boundary over realizable transitions must beat contact-onset retargeting, not rename intervals as modes. |
| [DexGrasp-Zero](https://yliangwu.github.io/DexGrasp-Zero/docs/) | Morphology-aligned anatomical graph, motion primitives, physical-property injection, activation masks. | Hand graph and physical constraints; no task contact-mode transition boundary. | Four training hands to unseen hands with YCB and real platforms; ablates physical priors/motion primitives, not controlled failure threshold. | **No**, but it already links morphology constraints to zero-shot success. | Candidate must explain failures after its ordinary morphology/kinematic distance is controlled; a graph distance is not enough. |
| [Scaling Cross-Embodiment World Models](https://arxiv.org/abs/2511.01177) | Embodiment-invariant particle state/action and graph world model; embodiment count and sim/real mixture. | Particle interaction geometry, not discrete contact modes. | Generalization to unseen hands and varied DOF; scale/co-training findings, no transfer-failure boundary. | **No**, but it claims a shared physical-interaction interface. | A failure boundary could be scientifically distinct, but the evidence must be from held-out capability transitions rather than another shared state representation. |

The mandatory anchors therefore do not make the claim impossible by themselves, but they make the novelty margin narrow. In particular, TopoRetarget, GraspGraphNet, CEDex, DexGrasp-Zero, and Transferring Contact already cover graph/contact/force mechanisms; the candidate cannot claim contact structure as such.

## Additional 2026 direct-neighbor search through September

These works were not optional “generic related work”; they materially change the novelty decision.

| Work | What it adds | Boundary/control status | Admission implication |
|---|---|---|---|
| [KITE](https://arxiv.org/abs/2606.22113) | Learns contact-pattern interaction intent and an embodiment-specific action decoder; transfers among parallel grippers, dexterous hands, and composite embodiments. | Reports zero-shot success and an interaction-intent ablation; no visual/EEF/kinematic-matched failure frontier. | The proposed mechanism must explain failures that KITE’s contact-intent decoder cannot, not merely show contact patterns are useful. Its project page says code is still forthcoming. |
| [ContactFlow](https://arxiv.org/abs/2607.26579) and [release repository](https://github.com/rpl-bonn/contactflow) | Object-centric 3-D contact-point trajectories condition a video world model across human and robot embodiments. | Transfer/verification success; large video-model inference, no discrete feasibility boundary. | Contact trajectory is already a strong embodiment-agnostic interaction variable; a contact-mode graph must add a falsifiable boundary, not another conditioning signal. |
| [C2Dex](https://arxiv.org/abs/2608.07045) | Stable object-side contacts, interaction-geometry constraints, and residual RL for monocular-video-to-dexterous transfer. | End-to-end trajectory success and real replay; no controlled failure boundary. | A temporal transition diagnosis must outperform its contact-consistency objective and avoid becoming a retargeting method. |
| [A4A](https://ru-arcl.github.io/a4a/) | Language-conditioned future trajectories of interaction-relevant 3-D points for VLA pretraining and cross-embodiment transfer. | Matched supervision comparisons and transfer success; no realizability boundary. | Evolving interaction geometry is already a transfer bridge; the candidate must isolate discrete feasibility, not future motion quality. |
| [TactAlign](https://arxiv.org/abs/2602.13579) | Cross-sensor tactile latent alignment for human-to-robot transfer on pivoting, insertion, lid closing, and screwing. | Contact-rich transfer success; tactile data and sensors, no topology boundary. | Supports the claim that contact information matters, but also shows a sensor-based route the proposed offline-only route must explicitly exclude. |
| [Cloak](https://tml.stanford.edu/cloak/) plus the [body-blind interface study](https://github.com/A-SHOJAEI/body-blind-action-interface) | Visual masking versus a causal body-information ladder; the latter reports a threshold where body-channel leakage collapses transfer. | The body-blind study is explicitly causal and scene-controlled, but its boundary is body information, not contact transitions. | It raises the standard for “failure boundary”: a contact claim needs the same intervention and held-out controls, not a post-hoc correlation. |
| [Cross-Embodiment Measurement Standard](https://github.com/A-SHOJAEI/cross-embodiment-measurement-standard) | Acceptance gate, class-prior/distance controls, strong probes, independent units, leakage and episode-split checks. | Explicitly targets false cross-embodiment claims; not a contact mechanism. | Any future pilot must pass its style of trivial-baseline, independent-unit, and leakage controls. |
| [EmbodiSteer](https://arxiv.org/abs/2606.12965) | Training-free joint-space guidance and collision-aware steering for Cartesian policies. | Collision/success improvements across nine simulated robots; no contact-mode graph. | Controls ordinary kinematic/collision constraints that otherwise masquerade as topology mismatch. |
| [Cross-Embodiment Gripper Benchmark](https://doi.org/10.1109/LRA.2026.3677707) | Transfer-time, energy, payload, and grasp metrics across mechanically distinct grippers. | Benchmark/metric study, not a mechanism. | Confirms that a different metric alone is not an acceptable contribution. |

The earlier mandatory data-selection and world-model anchors remain screened out as documented in [`IDEA_REPORT.md`](IDEA_REPORT.md): S2I/SCIZOR/DataMIL cover data selection; LIBERO-CF/VIFO/Safety cover visual/language/safety diagnostics; WorldEval/WorldGym/IRASim/WorldEcho and the decision-centric position cover generic world-model evaluation, action following, ranking, and uncertainty. None rescues this contact-topology direction or supplies its missing labels.

## Operational definition required by the claim

The following definition is precise enough to audit, but the required target-capability and outcome artifacts are not currently public in a CPU-ready form.

### Contact-mode node

For embodiment `e`, timestep `t`, and task object `o`, define the semantic contact set as:

```text
C_t^e = {(r, b, p): dist(r, b) <= delta_c,
          b is the task object or environment,
          p is an object-surface bin}
```

Here `r` is a robot link grouped into a morphology-independent role (`palm`, `distal-pad`, `lateral-pad`, or `support`), `b` is an object/environment body, and `p` is a fixed object-surface bin. The role map must be frozen from the URDF/MJCF before looking at outcomes; exact link IDs are not comparable across embodiments. Use `delta_c = 0.01 * d_o`, where `d_o` is the object bounding-box diagonal, unless the simulator exposes a solved contact flag, in which case that flag is used.

Define the phase label `phase_t` by a deterministic finite-state rule over a three-frame window:

* `no-contact`: `C_t` is empty, with no decreasing nearest-contact distance;
* `approach`: `C_t` is empty and nearest-contact distance decreases by at least `0.01 * d_o` in one sample;
* `first-contact`: `C_t` is nonempty and `C_(t-1)` is empty;
* `stable-contact`: the role/body set has Jaccard similarity at least 0.8 for three consecutive samples and relative tangential speed is at most `0.02 * d_o / delta_t`;
* `sliding-contact`: a contact set persists for three samples and relative tangential speed exceeds `0.02 * d_o / delta_t`;
* `support-contact`: an object/environment pair persists for three samples while the object is supported, with or without a robot-object pair;
* `regrasp`: a stable-contact window is followed by a role-set Jaccard similarity below 0.5 while the object remains within the task workspace;
* `release`: a stable-contact window is followed by an empty contact set for three samples.

The node is the pair `(phase_t, C_t)`. A directed edge from timestep `t` to `t+1` is recorded for every adjacent pair after collapsing self-loops; edge weights are the source rollout frequency or dwell-normalized mass. The graph is a **task-conditioned contact-mode transition graph**, not a generic contact distance.

### Source-target mismatch

Let `E_s_req` be the directed edges in successful source demonstrations for the same task/object family. Let `E_t_feas` be the union of edges reachable by the target embodiment in a capability probe from matched initial states, using the target action limits and the same object/environment. The capability probe must be fixed before outcomes and may use only a finite, documented action lattice; it cannot be selected after observing failures. Define the primary mismatch as weighted directed edge recall loss:

```text
d_topo(s, t) = 1 -
    sum_{edge in E_s_req} weight_s(edge) * I[edge in E_t_feas]
    / sum_{edge in E_s_req} weight_s(edge)
```

This is a predictor, not the scientific contribution. The scientific test is whether it predicts held-out transfer failure after controls. An offline overlap of observed source and target graphs, without a target capability probe, must be labeled `d_obs` and cannot be called realizable mismatch.

### Sensing and simulator requirements

Force or tactile sensing is **not** required for the discrete mode definition. Simulator contact pairs, signed gap/contact distance, geom/body IDs, poses, and relative velocities are sufficient; solved normal impulse can be retained as a secondary feature. Real force regulation is outside the claim. If an offline file has only RGB, actions, and EEF states, the definition is not measurable. If it has simulator states plus the matching model/configuration, contacts can be recomputed by MuJoCo, but that is simulator replay and not pure offline analysis. BAR-X documents states and fixed evaluation-condition artifacts but does not publish the contact arrays or outcome labels required by this definition.

## Cheapest public substrates audited

| Substrate | Public artifact evidence | Contact/state/outcome suitability | Hardware and runtime gate | Decision |
|---|---|---|---|---|
| [BARX code](https://github.com/ajaysridhar0/barx), [raw HDF5](https://huggingface.co/datasets/ajaysri/barx-raw-hdf5), RoboCasa-X | 23,400 demonstrations, six embodiments, four tasks; raw files contain actions, `states`, RGB, EEF/gripper states, annotations, and episode metadata. Evaluation bundles contain fixed scene/simulator states. | Multiple embodiments and states are useful, but the documented HDF5 fields do not include contact arrays or transfer success/failure labels. A policy-failure pilot needs replay plus policy inference. | Official release: Linux x86-64/Python 3.10, CUDA 12.1, about 70 GiB for quick start; training/evaluation extra pins FlashAttention 2.5.5 to Torch CUDA 12.1 and NVIDIA. Full raw archive is about 284 GiB; kitchen assets add about 8.8 GiB after extraction. | **Reject as a first-step pilot.** CPU state parsing alone cannot test transfer failure; the policy/runtime path violates the DCU admission rule. |
| [CEI project](https://cross-embodiment-interface.github.io/) | Paper/project page reports 16 simulated embodiments and six real tasks with tables/videos. | No public raw trajectory/contact/outcome artifact or runnable CPU checkpoint was found on the project page. | Reproduction would require reconstructing the authors' synthesis and policy stack. | **Reject.** |
| [TopoRetarget implementation](https://github.com/0iui0/toporetarget) | Lightweight unofficial CPU-oriented retargeter; keypoints, object poses, object mesh; simple hand models and optional MuJoCo/PPO. | It produces references, not target policy success/failure or simulator contact-mode labels. | Could run with NumPy/SciPy/trimesh/Torch, but it does not test the audited claim. | **Reject as non-diagnostic.** |
| [CEDex code/data](https://github.com/GeorgeWuzy/CEDex-Grasp) | Contact maps and single-grasp data for multiple hands. | Grasp pose keys and object names, not temporal source-target transitions or transfer outcomes. | Python 3.8, Torch CUDA 12.4, PyTorch3D, Isaac Gym, and custom `pointnet_lib`; incompatible with the no-port/no-install gate. | **Reject.** |
| [Cloak release](https://github.com/Stanford-TML/cloak) | Public code, optional checkpoints, and DROID extrinsics. | Visual masking and VLA transfer, no contact-mode failure labels. | GPU policy server/checkpoint and deployment stack; no CPU-only contact-boundary artifact. | **Reject.** |
| [KITE project](https://kite-manip.github.io/) | Reports MuJoCo results over five embodiments and three tasks. | Contact-pattern intent and success are reported, but the page says code is forthcoming; raw trajectories/labels are unavailable for an audit pilot. | No reproducible public artifact path yet. | **Reject.** |
| [ContactFlow release](https://github.com/rpl-bonn/contactflow) | Public release for a large video world model conditioned on contact flow. | Contact trajectories and transfer verification are present conceptually, but not a small labelled simulator table for failure-boundary regression. | Large video-model inference; not a standard-PyTorch CPU/DCU pilot. | **Reject.** |
| [TactAlign](https://yswi.github.io/tactalign/) | Project page reports tactile cross-sensor transfer and links code as coming soon. | Requires tactile observations and paired task data, contrary to the offline simulator-state route. | Hardware/sensor and unavailable code/data. | **Reject.** |

## Would-be smallest falsification pilot (not admitted)

This is the smallest design that would test the claim if the artifact and hardware gates were cleared. It is recorded to make the rejection concrete; it is not an instruction to run it.

* **Repository and artifacts:** BARX release [`ajaysridhar0/barx`](https://github.com/ajaysridhar0/barx); raw subset selected by `scripts/download_raw_data.py --dataset xp_900 --task pnp`; fixed condition bundles under `evaluation/conditions/`; the released Joint Reps checkpoint named `step-050000-epoch-15-loss=0.2577.pt`; and the `mg_pnp_lite` VQ tokenizer. Exact subset files must be fixed by the manifest before any run.
* **Embodiments and tasks:** source `IIWA` and `UR5e`, target `Panda` and `Jaco`; `pnp_counter_to_sink` and `pnp_sink_to_counter`. Use the same 100-condition protocol and task/object split for every target pair.
* **Policy inference:** required for a transfer-failure dependent variable; no admissible CPU/DCU policy path is documented.
* **Simulator execution:** required twice—MuJoCo/RoboCasa replay to extract contact pairs and a target capability probe, and policy rollout to obtain failure/success. Offline HDF5 parsing alone is insufficient.
* **Packages:** the pinned BARX stack, MuJoCo 3.1.1, RoboCasa/robosuite, h5py, PyTorch, and the policy's FlashAttention 2.5.5 extra. This list itself fails the project hardware gate.
* **Disk:** official walkthrough is approximately 70 GiB plus about 8.8 GiB extracted kitchen assets; the complete raw archive is approximately 284 GiB. The public docs do not give a verified small-subset size, so a bounded 1–3 day disk budget cannot be claimed without downloading it.
* **Compute and wall clock:** contact extraction would be CPU-sized once a working simulator exists; VLA policy inference is NVIDIA/CUDA-specific. There is no honest DCU/CPU wall-clock estimate for the complete pilot.
* **Independent variable:** `d_topo`, constructed only from the pre-registered mode graph and target capability probe.
* **Controls:** same task/object/scene seed and camera; visual masking or identical rendered background; EEF pose-trace DTW/Chamfer matched or covaried; representation reconstruction quality; DOF/link/workspace/kinematic distance; source policy/checkpoint; target action budget; and episode-blocked splits. Run a no-contact-graph control using only kinematic/visual predictors.
* **Dependent variable:** binary target transfer success as primary; first irreversible failure step and required-edge completion as secondary.
* **Statistical test:** hierarchical episode-blocked logistic regression with task and source/target random effects, `failure ~ d_topo + d_kin + d_vis + d_EEF + d_repr`; compare against the control-only model by a pre-registered likelihood-ratio/permutation test and bootstrap by independent episodes and embodiment pairs. Estimate a threshold only on held-out embodiment pairs.
* **Positive criterion:** the topology term has a 95% episode/embodiment bootstrap interval excluding zero, improves held-out AUC by at least 0.10 over the strongest control-only model, and the estimated failure boundary remains monotone in a held-out pair.
* **Kill criterion:** no incremental held-out predictive value after controls; no target capability edge set; no outcome labels; or any need to port FlashAttention, emulate CUDA, alter a VLA architecture, rebuild RoboCasa/LIBERO, train a large policy, or collect real data.

The pilot fails at the artifact/runtime gate before implementation. Running a smaller graph-overlap analysis would produce `d_obs` without transfer failures and would not falsify the stated mechanism.

## Admission decision and pivot condition

The direction should be pivoted before implementation. A future re-admission would require **both**:

1. a public, CPU-capable artifact containing source/target state or contact metadata plus independent transfer success/failure outcomes for at least two contact-rich tasks and multiple embodiments; and
2. a preregistered capability intervention showing that `d_topo` predicts held-out failures beyond the controls above, with the result surviving the cross-embodiment measurement-standard checks.

Until those two conditions are met, do not install BAR-X, download its checkpoints or raw archive, reconstruct RoboCasa, or launch experiments for this direction.

## Sources inspected

* [BARX README](https://github.com/ajaysridhar0/barx), [BARX installation](https://raw.githubusercontent.com/ajaysridhar0/barx/main/docs/installation.md), [BARX raw-data format](https://raw.githubusercontent.com/ajaysridhar0/barx/main/dataset/README.md), and [raw HDF5 dataset card](https://huggingface.co/datasets/ajaysri/barx-raw-hdf5)
* [CEI](https://cross-embodiment-interface.github.io/), [BAR-X](https://ajaysridhar.com/barx/), [Transferring Contact](https://arxiv.org/abs/2606.15516), [Cloak](https://tml.stanford.edu/cloak/), [TopoRetarget](https://toporetarget2026.github.io/TopoRetarget/), [GraspGraphNet](https://arxiv.org/abs/2607.11031), [CEDex](https://github.com/GeorgeWuzy/CEDex-Grasp), [HOWTransfer](https://arxiv.org/abs/2606.10743), [DexGrasp-Zero](https://yliangwu.github.io/DexGrasp-Zero/docs/), and [Scaling Cross-Embodiment World Models](https://arxiv.org/abs/2511.01177)
* [KITE](https://arxiv.org/abs/2606.22113), [ContactFlow](https://arxiv.org/abs/2607.26579), [C2Dex](https://arxiv.org/abs/2608.07045), [A4A](https://ru-arcl.github.io/a4a/), [TactAlign](https://arxiv.org/abs/2602.13579), [body-blind interface](https://github.com/A-SHOJAEI/body-blind-action-interface), [cross-embodiment measurement standard](https://github.com/A-SHOJAEI/cross-embodiment-measurement-standard), and [EmbodiSteer](https://arxiv.org/abs/2606.12965)
