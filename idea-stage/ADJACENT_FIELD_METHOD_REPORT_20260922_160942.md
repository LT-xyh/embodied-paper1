# Adjacent-Field Method Transfer Report

**Date:** 2026-09-22 16:09 (Asia/Shanghai)
**Authority:** `RESEARCH_BRIEF.md`, `idea-stage/ADJACENT_FIELD_METHOD_TRANSFER.md`
**Scope:** selection only; no installation, implementation, training, simulator execution, or checkpoint/data download.

## Decision

**Surviving candidates: 0.** No direction reaches the required combination of (i) a recent adjacent-ML mechanism, (ii) a non-transplant robot-specific scientific claim, (iii) a 1–3 day closed-loop falsification path, and (iv) an independent second benchmark path. The recommended action is **NO CANDIDATE**. No P0 is authorized.

The search covered sequence modeling, selective/conformal prediction, distributionally robust policy learning, test-time adaptation, and temporal/decision-aware control mechanisms released in 2024–2026. The robotics audit searched 2025–2026 terminology variants, including temporal imitation, state-space policy, conformal safety/DAgger, concept drift, and test-time policy adaptation.

## Adjacent ML Mechanism Landscape

| Mechanism considered | Exact source work and claim | Why it appears relevant to robot control | Decisive audit result |
|---|---|---|---|
| Selective state-space sequence modeling | Mamba, “Linear-Time Sequence Modeling with Selective State Spaces,” ICLR 2024. Input-dependent SSM parameters selectively retain/forget sequence content while giving linear-time recurrent inference. [paper](https://arxiv.org/abs/2312.00752) | A closed-loop controller must retain task-relevant history while observations become aliased after contact or occlusion. | The mechanism is already the core of robot temporal policies MTIL and Mamba Policy; a new BC-RNN backbone would be architecture transplantation. [MTIL](https://arxiv.org/abs/2505.12410), [Mamba Policy](https://github.com/SageCao1125/Mamba-Policy) |
| Online selective conformal prediction | Sale & Ramdas, “Online Selective Conformal Inference: Errors and Solutions,” TMLR 2025. It restores selection-conditional coverage under sequential selection by preserving calibration exchangeability. [paper](https://openreview.net/pdf?id=PjIQwFyP07) | Closed-loop action/state queries are selected based on current rollout difficulty, so iid calibration assumptions fail. | Robot safety and interactive imitation already apply conformal regions to future policy errors or expert queries; a robot abstention/query wrapper is generic safety/uncertainty work and is excluded by the brief. [sparse-feedback safety](https://arxiv.org/abs/2501.04823), [ConformalDAgger](https://mlanthology.org/iclrw/2025/zhao2025iclrw-conformalized/) |
| Distributionally robust policy learning under concept drift | Wang et al., “Distributionally Robust Policy Learning under Concept Drifts,” ICML 2025. It estimates worst-case policy value when the conditional outcome relationship drifts. [paper](https://proceedings.mlr.press/v267/wang25cm.html) | Contact dynamics, friction, and embodiment can change the action-outcome relation while state marginals remain similar. | The source method already is policy learning under drift; a robomimic adaptation would change domain/benchmark without a new control mechanism. No robot-specific 2025–2026 claim was found that would make the adaptation scientifically distinct. |
| Test-time adaptation with action-entropy regularization | “Test-time Adapted Reinforcement Learning with Action Entropy Regularization,” ICML 2025. It adapts an RL policy at deployment using entropy-regularized test-time updates. [paper](https://openreview.net/forum?id=Xv1jY6U0pT) | A controller sees unlabeled rollout states and could update its action distribution online. | Direct online adaptation of a BC policy is a test-time/uncertainty transplant; related robot work already uses conformal filtering, test-time compute, or online policy adaptation. It also needs interaction feedback unavailable in the required offline-first state-only pilot. |
| Decision-/trajectory-level uncertainty filtering | Recent ML work combines calibrated trajectory risk with policy optimization; e.g. conformal trajectory filtering in DoublyAware (2025). [paper](https://www.dfki.de/web/forschung/projekte-publikationen/publikation/16370) | A rollout-level risk signal could change which action sequence is executed, rather than only calibrating one-step error. | This is already a robot control mechanism and collides with accumulated negative evidence on generic uncertainty, safety, recovery, and action-following diagnostics. It cannot be retained as an adjacent-field transfer.

## Robot-Specific Failure Modes

The potentially transferable assumptions and their robotics changes were explicit in screening:

1. **Long-history sufficiency:** Mamba assumes a compact recurrent state can preserve task-relevant information. Contact-induced partial observability makes this a control-stability question, but MTIL already makes full-history selective SSM the robot claim.
2. **Exchangeable calibration:** conformal methods assume a valid calibration relation. Closed-loop intervention and state selection break exchangeability, but existing robot safety and ConformalDAgger papers already make this adaptation.
3. **Conditional drift:** concept-drift policy learning assumes a specified perturbation family. Friction/geometry changes are a plausible robot instantiation, yet applying the estimator to robomimic would only change the data-generating process.
4. **Unlabeled deployment adaptation:** test-time RL assumes an online update signal. A state-only BC rollout supplies no reward or expert label, so a valid adaptation requires a new feedback mechanism; adding entropy or a confidence threshold is a generic uncertainty/safety wrapper.
5. **Trajectory risk selection:** trajectory-level filtering changes which closed-loop action is executed, but the same idea is already present in robot risk-aware planning and is within the brief’s excluded evaluator/safety families.

## Candidate Adaptations and Rejection Log

The five candidates below were the initial pool. Each has a concrete falsification sketch, but none passed admission.

### C1 — Contact-gated selective-state memory for BC-RNN (REJECTED)

* **Source mechanism:** Mamba selective SSM (ICLR 2024), input-conditioned state updates.
* **Proposed robot adaptation:** gate recurrent memory updates using contact/velocity change points so the hidden state resets only at interaction transitions; the hypothesis is reduced compounding error on contact-rich tasks.
* **Closest robotics prior:** MTIL (RA-L 2025) already encodes full history with Mamba on robomimic/LIBERO; Mamba Policy (IROS 2025) supplies a second selective-SSM policy line.
* **Exact robomimic P0 that would have been run:** state-only BC-RNN versus contact-gated SSM on Lift, Can, and Square; 3 seeds, 50 closed-loop episodes/task; success rate and failure-step distribution; CPU/DCU standard PyTorch, one to two days.
* **Second path:** Meta-World MT1 Pick-Place and Door with the same recurrent interface.
* **Kill:** no success improvement at matched parameter count or gains only on action MSE. **Admission failure:** the gating is a small architectural variant of an already robot-specific SSM mechanism; it fails the non-transplant rule.

### C2 — Selection-valid conformal action-set controller (REJECTED)

* **Source mechanism:** online selective conformal inference (TMLR 2025), selection-conditional coverage under sequential selection.
* **Proposed robot adaptation:** calibrate action intervals only at predicted intervention points and test whether coverage tracks rollout failure risk under contact events.
* **Closest robotics prior:** Learning Robot Safety from Sparse Human Feedback (2025) uses conformal state regions for policy errors; ConformalDAgger (ICLR 2025 workshop) uses conformal intervals to query experts.
* **Exact robomimic P0 that would have been run:** freeze BC/BC-RNN, calibrate on held-out Lift/Can rollouts, compare conformal-triggered query/stop policy with fixed-threshold and no-trigger baselines using closed-loop success, intervention count, and false-safe rate.
* **Second path:** Meta-World MT1 with the same state/action calibration wrapper.
* **Kill:** coverage does not predict failures, or success gains require excessive interventions. **Admission failure:** it is generic uncertainty/safety/interactive imitation, explicitly crowded and excluded.

### C3 — Concept-drift robust BC objective (REJECTED)

* **Source mechanism:** ICML 2025 distributionally robust policy learning under concept drift; worst-case conditional-outcome policy value.
* **Proposed robot adaptation:** estimate a contact-conditioned drift set and optimize worst-case success across friction/geometry perturbations while preserving nominal performance.
* **Closest robotics prior:** no single paper closed the exact state-only robomimic formulation, but the source already claims robust policy learning under conditional drift; robot instantiation would be a benchmark/domain substitution.
* **Exact robomimic P0 that would have been run:** BC versus drift-robust BC on nominal and fixed MuJoCo friction/pose perturbation suites for Lift, Can, Square; closed-loop success and worst-case drop.
* **Second path:** Meta-World MT1 under object-mass and friction perturbations.
* **Kill:** robustness gain disappears on held-out perturbations or nominal success drops beyond a fixed margin. **Admission failure:** no robot-specific mechanism beyond applying an existing robust policy learner to a robot dataset; this reads as “we applied X to robomimic.”

### C4 — Reward-free test-time entropy adaptation for BC (REJECTED)

* **Source mechanism:** ICML 2025 TARL, test-time policy updates with action-entropy regularization.
* **Proposed robot adaptation:** use temporal consistency of state-only demonstrations as a reward-free update signal and adapt only a small action head during rollout.
* **Closest robotics prior:** conformal safety/query methods and dynamic test-time compute scaling already address deployment-time policy uncertainty/compute; the proposed update has no validated robot feedback signal.
* **Exact robomimic P0 that would have been run:** frozen BC-RNN versus entropy-adapted head on held-out initial-state perturbations, measuring success, action variance, and post-adaptation degradation.
* **Second path:** Meta-World MT1 under camera/state noise.
* **Kill:** adaptation destabilizes closed-loop success or needs privileged reward. **Admission failure:** direct test-time adaptation plus uncertainty regularization, with no non-overlapping robot mechanism.

### C5 — Conformal trajectory-risk selector for action chunks (REJECTED)

* **Source mechanism:** sequential conformal/trajectory risk selection, instantiated by recent risk-filtering control work such as DoublyAware (2025).
* **Proposed robot adaptation:** calibrate chunk-level risk on contact-phase signatures and select among BC-RNN action chunks using a rollout-aware guarantee.
* **Closest robotics prior:** DoublyAware uses conformal prediction to filter candidate trajectories; ConformalDAgger and robot safety conformal work cover the deployment-risk use case.
* **Exact robomimic P0 that would have been run:** fixed BC-RNN chunk policy versus calibrated selector on Lift/Square, measuring success, premature termination, and calibration under perturbation.
* **Second path:** Meta-World MT1.
* **Kill:** selector cannot improve success at fixed action budget or only changes a metric. **Admission failure:** generic safety/risk filtering and action-chunk selection are accumulated negative-evidence families.

## Source-Field Novelty Audit

The source papers already contain the mechanism each candidate would claim: selective input-dependent state updates, selection-valid conformal calibration, worst-case conditional-drift policy learning, test-time entropy adaptation, or trajectory-risk filtering. The proposed robot changes either instantiate the source assumptions on robot data or add a thin wrapper. None changes the learning theorem/objective in a way that is specific to closed-loop control while remaining reusable across benchmarks.

## 2025–2026 Robotics Novelty Audit

The decisive collisions are concrete: MTIL and Mamba Policy cover selective SSM temporal imitation; robot conformal safety and ConformalDAgger cover calibrated deployment errors and expert querying; recent test-time compute/risk-filtering work covers deployment-time policy selection. Searching terminology variants therefore did not reveal an independent mechanism gap. The remaining concept-drift idea has no robotics-specific adaptation beyond perturbing the benchmark and is rejected on the source-field audit.

## Static Execution Admission

The conditionally admitted substrate is available in principle (`robomimic` v0.5.x, `robosuite` v1.5.x, MuJoCo, state-only BC/BC-RNN). No runtime was installed or executed in this pass. All five rejected sketches could fit a 1–3 day pilot, but execution feasibility cannot rescue a novelty collision. Since no candidate passed, there is no authorized implementation diff, P0 run, dataset/checkpoint download, or simulator launch.

## Second Evaluation Path

Meta-World MT1 was retained as the standard second-path template in the rejected sketches. No survivor reached the stage where a second benchmark path could be admitted.

## Final Shortlist: at most Top-2

**Empty.** Retaining any of C1–C5 would violate at least one mandatory gate.

## Recommended P0

**NO CANDIDATE.** Stop selection here and do not start a P0. A new search should introduce a genuinely different adjacent mechanism or new evidence that changes one of the collision findings; it should not repackage these five directions.
