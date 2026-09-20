# Robotics Idea Discovery Report

**Direction**: Research-direction reselection from `RESEARCH_BRIEF.md`
**Date**: 2026-09-20
**Pipeline**: research-lit -> idea-creator (robotics framing) -> novelty triage -> provisional reviewer synthesis
**Assurance**: draft; no experiments or implementation performed

## Robotics Problem Frame

- Embodiment: single-arm tabletop manipulation is the default target; no real robot is assumed.
- Task family: imitation learning, policy robustness, failure diagnosis, and policy evaluation.
- Observation/action: RGB or RGB-D observations with low-dimensional end-effector or action-chunk interfaces, depending on the selected benchmark.
- Learning regime: frozen-policy evaluation or lightweight behavior cloning; no foundation-model pretraining.
- Available assets: public datasets, public benchmark suites, and mature open implementations. This workspace contains no existing experiment harness.
- Compute: 2 x Hygon DCU K100, 64 GB each; prefer standard PyTorch and avoid CUDA-specific kernels.
- Safety and execution: simulation/offline first; real-robot work requires explicit approval.

## Landscape and Eliminated Directions

Recent anchors include SIMPLER (CoRL 2025) for simulation-based evaluation of real manipulation policies, LIBERO-CF for counterfactual language-versus-vision diagnosis, LIBERO-Safety for perturbation and safety evaluation, WorldEval (2025) and IRASim (ICCV 2025) for learned policy/world-model evaluation, and DataMIL (2025), SCIZOR (2025), ICLR 2025 data-scaling work, and ICRA 2025 mixed-quality demonstration studies for data composition.

Eliminate or strongly downrank: new foundation VLA pretraining; generic VLM/VLA application to a standard benchmark; real-robot-only sim-to-real claims; large-scale diffusion-policy pretraining; simulator or runtime reconstruction as the contribution; and CUDA/Triton-specific methods unavailable by default on the target DCU platform.

## Ranked Top-3 Candidates

### 1. Segment-level mixed-quality demonstration selection for imitation learning

- **Hypothesis**: selecting state-action segments by a shift-aware utility or recoverability score improves out-of-distribution success and failure recovery at fixed retained-data and training budgets.
- **Embodiment / benchmark**: single-arm tabletop manipulation; RoboMimic or ManiSkill offline demonstrations, subject to public loader availability.
- **Closest prior work and novelty delta**: DataMIL, SCIZOR, ICLR 2025 scaling-law work, and ICRA 2025 mixed-quality demonstrations make data curation crowded. The defensible delta is a controlled segment-level test tied to recovery and distribution shift, comparing random, trajectory-level, and segment-level selection at equal sample count and compute.
- **Minimum falsifiable pilot**: inject labeled observation/action corruption or layout shift into public demonstrations; train the same small BC model with the three selection policies; report success, failure/recovery rate, OOD generalization, retained data, and preprocessing cost.
- **Compute / risk**: low to medium compute; standard PyTorch and likely DCU-compatible. Main risk is incremental novelty and dataset-loader friction.
- **Positive grow criterion**: segment selection improves OOD success or recovery at equal data and training budget across at least two task families.
- **Negative kill criterion**: gains disappear at equal sample count, or are fully explained by retaining more successful trajectories.
- **Reviewer rejection risk**: “This is another data-filtering heuristic.” The paper must isolate a mechanism and include strict budget-matched controls.
- **Publication potential**: credible empirical/data-centric CoRL, ICRA, IROS, or RA-L route if the mechanism and failure analysis are strong.
- **Longer-term extension**: adaptive data valuation, active demonstration repair, and quality-aware policy training.
- **Hardware required**: no.

### 2. Counterfactual instruction-adherence and visual-shortcut diagnostics for frozen policies

- **Hypothesis**: ordinary task success conflates language adherence with visual shortcut use; paired counterfactual interventions expose failures and predict OOD behavior better than aggregate success.
- **Embodiment / benchmark**: tabletop manipulation; LIBERO-CF-style paired tasks, optionally combined with LIBERO-Safety perturbations or SIMPLER if existing scripts run unchanged.
- **Closest prior work and novelty delta**: LIBERO-CF directly establishes the problem, while LIBERO-Safety covers perturbation and semantic/physical safety. The possible delta is a reproducible decomposition of instruction sensitivity, visual shortcut reliance, and recovery under matched counterfactuals across frozen policies.
- **Minimum falsifiable pilot**: use released benchmark tasks and an accessible frozen checkpoint; compare matched instruction/image counterfactuals using action disagreement, task success, recovery latency, and calibration.
- **Compute / risk**: low compute, but high benchmark/runtime risk because prior LIBERO integration was costly. It is viable only with an existing, directly runnable harness.
- **Positive grow criterion**: counterfactual metrics reveal stable policy differences or predict OOD failures missed by ordinary success rate.
- **Negative kill criterion**: the result is only a benchmark wrapper, or the diagnostic adds no predictive or explanatory value beyond success rate.
- **Reviewer rejection risk**: “Evaluation-only and too close to LIBERO-CF.” The contribution must demonstrate a new measurable decomposition or validated predictive value.
- **Publication potential**: benchmark/diagnostic contribution for CoRL, ICRA, RSS workshop, or RA-L, conditional on clear separation from LIBERO-CF.
- **Longer-term extension**: causal policy audits, language grounding stress tests, and safety-aware deployment gates.
- **Hardware required**: no.

### 3. Calibration of learned world-model policy evaluators under shift

- **Hypothesis**: action-conditioned world-model scores can mis-rank policies under embodiment, visual, or dynamics shift; uncertainty and consistency calibration can reduce false acceptance of failing policies.
- **Embodiment / benchmark**: simulated manipulation or PushT/RoboMimic-style offline trajectories; WorldEval and IRASim are relevant anchors.
- **Closest prior work and novelty delta**: WorldEval and IRASim establish learned policy/world-model evaluation. The delta is a failure-aware calibration protocol that measures ranking correlation, calibration error, and failure recall against short-horizon simulator rollouts under controlled shifts.
- **Minimum falsifiable pilot**: use an existing checkpoint or small public model; rank several frozen policies with the evaluator, then compare rankings against short simulator rollouts across visual/dynamics shifts.
- **Compute / risk**: medium compute and medium infrastructure risk. Do not train a large world model for the pilot; absence of a usable public checkpoint is a kill condition.
- **Positive grow criterion**: calibrated uncertainty or consistency materially improves policy-selection rank correlation or false-failure recall under shift.
- **Negative kill criterion**: simple visual/action heuristics match the evaluator, or model quality dominates with no stable calibration effect.
- **Reviewer rejection risk**: “World-model quality/correlation has already been studied, and this is incremental.” The protocol must expose a previously unmeasured deployment failure mode.
- **Publication potential**: stronger upside for CoRL/RSS if the evaluator failure mode is robust and benchmarked; otherwise an evaluation paper.
- **Longer-term extension**: deployment gates, active test generation, and cross-simulator reliability studies.
- **Hardware required**: no.

## Recommendation and Stop Rule

Candidate 1 is the safest first scientific pilot under the brief. Candidate 3 has higher upside but requires an existing usable evaluator checkpoint. Candidate 2 is scientifically sharp but should be rejected if reproducing it requires rebuilding LIBERO infrastructure. This report stops at the Top-3 as required; no method implementation, benchmark installation, GPU run, or real-robot activity was performed.

## Sources Consulted

- SIMPLER, CoRL 2025: https://proceedings.mlr.press/v270/li25c.html
- LIBERO-CF: https://vla-cf.github.io/
- LIBERO-Safety: https://libero-safety.github.io/
- WorldEval: https://arxiv.org/abs/2505.19017
- IRASim, ICCV 2025: https://openaccess.thecvf.com/content/ICCV2025/papers/Zhu_IRASim_A_Fine-Grained_World_Model_for_Robot_Manipulation_ICCV_2025_paper.pdf
- DataMIL: https://arxiv.org/abs/2505.09603
- SCIZOR: https://arxiv.org/abs/2505.22626
- ICLR 2025 data scaling: https://proceedings.iclr.cc/paper_files/paper/2025/hash/88b7b2c896506daabc8d3fd587055167-Abstract-Conference.html
- ICRA 2025 mixed-quality demonstrations: https://doi.org/10.1109/ICRA55743.2025.11128787
