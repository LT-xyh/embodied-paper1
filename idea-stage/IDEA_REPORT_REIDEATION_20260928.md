# Structural re-ideation after the TCI policy-faithful failure

**Date:** 2026-09-28
**Branch:** `idea/reideation-20260928`
**Status:** selection and admission only; no research method has been implemented or trained in this cycle.

## Decision

The policy-faithful TCI gate failed on a frozen, trained BC-RNN: held-out consequence inversion was at chance-to-weak signal, shuffled consequences were indistinguishable, and multi-horizon consequences did not improve over the immediate consequence. The independent fallback review confirmed that this is a scientific null rather than a technical defect. ASCC, CAEA, and all renamed action-swap, consequence-gated memory, score/preference, or transition-surprise variants are therefore excluded.

This re-ideation used the qualified robosuite/MuJoCo state-only substrate only as an execution possibility. No local literature PDFs were present; local files contributed prior negative evidence and runtime facts, while recent literature was checked against primary publisher, proceedings, project, and arXiv pages. The current pass generated four method families and retained one conditional Track-A hypothesis for an independent reviewer and a cheap measurement gate. The other families were rejected before implementation.

## Robotics problem frame

State-only behavior cloning exposes a concrete closed-loop failure: the policy is trained on bounded controller commands, while many policy heads represent an unbounded Gaussian and then clip or squash the command at execution. If demonstrations spend substantial mass near an action bound, the likelihood used for training and the action actually executed describe different distributions. The question is whether support-correct policy learning changes closed-loop contact behavior, rather than merely reducing one-step action error.

The candidate substrate is a small recurrent or feed-forward state policy in robosuite/robomimic-style normalized action coordinates. The first measurement is the existence of boundary mass and a measurable difference between the native policy distribution and the executed action. If either is absent, the candidate is killed without a pilot.

## Literature landscape and freshness findings

Recent work makes several attractive alternatives poor Paper-1 bets:

* Delay-aware imitation is no longer an open generic gap. **Delay-Aware Diffusion Policy** explicitly conditions training and inference on measured latency and corrects trajectories ([arXiv:2512.07697](https://arxiv.org/abs/2512.07697)); **RAPAC-DP** conditions a compensation pathway on pending actions under delayed execution and reports RoboMimic results ([arXiv:2608.15924](https://arxiv.org/abs/2608.15924)); and **RACE** changes imitation targets, timing, and test-time chunk search for faster execution ([ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/fab80bb9d97e9b9ff5c19f91f72838c6-Abstract-Conference.html)). A delay-calibration BC proposal would be a direct or near-direct execution variant.
* Multi-task conflict routing is crowded. **LMoE-DP** combines language-conditioned representations, mixture-of-experts action distributions, and gradient modulation for multi-task manipulation ([arXiv:2510.24055](https://arxiv.org/abs/2510.24055)); **FoAM** adds foresight to multi-task imitation ([AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/38911)); **GAP** estimates motion-transition phases and modulates proprioceptive gradients in vision-proprioception policies across simulation and real robots ([arXiv:2602.12032](https://arxiv.org/abs/2602.12032)); and recent robot RL work already resolves objective-gradient conflicts ([arXiv:2509.14816](https://arxiv.org/abs/2509.14816)). A PCGrad/CAGrad or contact-phase gradient swap would be an optimizer/loss change, not a distinct mechanism.
* Phase and execution-speed ideas are also occupied by **SAIL** ([CoRL 2025](https://proceedings.mlr.press/v305/arachchige25a.html)), **RACE**, and the recent phase-aware policy literature. A monotonic phase latent or speed-conditioned BC would not have a sufficiently narrow non-overlapping claim.
* Physical/control-informed losses have direct neighbors, including **Stable-BC** ([RA-L 2025 DOI](https://doi.org/10.1109/LRA.2025.3526439)) and physics-informed imitation/control work. A Jacobian-weighted MSE is therefore rejected as a loss swap unless a future reviewer finds an interaction that changes closed-loop behavior beyond reweighting.

The remaining bounded-action question is anchored by **Truncated Gaussian Policy for Debiased Continuous Control** ([AAAI 2025](https://ojs.aaai.org/index.php/AAAI/article/view/33988)), which analyzes boundary bias in continuous-control RL, and **Understanding Behavior Cloning with Action Quantization** ([arXiv:2603.20538](https://arxiv.org/abs/2603.20538)), which analyzes quantized action labels. Neither source establishes a support-correct bounded likelihood for state-only robot behavior cloning with a closed-loop manipulation claim. That is a narrow, conditional novelty boundary rather than proof of novelty.

## Generated hypotheses and aggressive rejection

### Candidate A — Support-Corrected Bounded Behavior Cloning (conditional survivor)

**Failure mode.** A policy head places probability outside the executable normalized action cube and clips it, so the learned density, mean, and executed action disagree near contact or controller saturation.

**Hypothesis.** When expert action mass is near a real controller bound, a native bounded distribution (scale-adjusted truncated Gaussian or an equivalent bounded parameterization) produces a different closed-loop failure profile from a clipped Gaussian/tanh BC policy, because its likelihood and executed command share the same support. The prediction is specifically a reduction in boundary-induced contact failures, not a generic MSE improvement.

**Exact method delta.** Keep observation encoder, recurrent state, data, split, optimizer budget, and deterministic evaluation protocol fixed. Replace the unbounded Gaussian/clipped action head with a support-matched bounded head; train by exact bounded log likelihood and execute the bounded mean. Pre-register the boundary fraction, one-step action error, saturation frequency, and task success. No hidden-command/censoring assumption is made.

**Closest prior already solves.** The AAAI-2025 truncated-Gaussian paper identifies boundary bias and proposes scale-adjusted truncation for RL sampling. The 2026 action-quantization analysis studies quantization error and sample complexity. Standard robomimic BC exposes normalized bounded targets but does not make the executed policy distribution support-matched in the proposed state-only closed-loop comparison.

**Non-overlapping Track-A claim.** A support-matched bounded policy head changes closed-loop manipulation only when demonstrator mass lies near controller bounds; the effect is measurable by a boundary-stratified causal comparison against a frozen clipped-Gaussian BC baseline.

**Minimum P0.** First run an offline boundary-semantic preflight on independently generated Lift/Can/Square demonstrations: report per-dimension mass at `|a|>=0.8`, `|a|>=0.95`, and exact clipping, and verify that the action stored in the dataset is the command passed to the wrapper. If boundary mass is below 5% on every task or the executed action is already support-matched, stop. Otherwise train deterministic baseline and bounded-head policies on disjoint demonstrations, evaluate 3 seeds per task with the same initial states, and stratify success by boundary-heavy versus interior decisions. Primary metric is paired task success; secondary metrics are boundary action error, saturation count, contact/object-drop rate, and nominal success.

**Positive criterion.** The bounded policy must improve paired success on at least two of three tasks, with the gain concentrated in boundary-heavy decisions, while not reducing interior-state success by more than 5 percentage points and while passing an equal-compute ablation against a tanh-squashed head.

**Kill criterion.** Kill if boundary mass is absent, if bounded and clipped policies produce the same executed actions, if gains occur only in one-step MSE, if the effect is not boundary-stratified, or if a simple tanh/squash control matches it. Do not rescue with a new distribution, temperature tuning, or a larger model.

**Mechanism versus benchmark.** This is a mechanism claim about support mismatch and closed-loop action saturation. It is not a benchmark or metric change, but the novelty margin is narrow and the reviewer may still classify it as a distribution/loss swap.

### Candidate B — Delay-calibrated state-only BC (rejected)

**Exact prior claim.** Delay-Aware Diffusion Policy trains with measured inference delay and corrected trajectories; RAPAC-DP conditions on pending actions to compensate delayed cloud execution; RACE explicitly retimes and searches action chunks for latency.

**Already solved.** These works establish that observation/execution delay changes the control problem and provide training or runtime compensation.

**Proposed difference.** Estimate a fixed 0–3-step actuator delay from proprioceptive traces and condition a BC-RNN on that estimate.

**Distinguishing experiment.** Compare vanilla BC, delay-conditioned BC, and pending-action compensation under matched fixed and stochastic delays on Lift/Can.

**Rejection.** The mechanism is a direct state-only specialization of an already crowded latency-compensation family; the experiment would mainly change architecture and substrate. It is not retained.

### Candidate C — Contact-transition gradient routing (rejected)

**Exact prior claim.** Recent multi-task manipulation policies use expert specialization and gradient modulation to address task conflict; GAP explicitly estimates motion-transition phases and reduces proprioceptive gradient magnitude during those phases; multi-objective robot RL uses gradient-conflict resolution.

**Already solved.** The prior family already establishes that routing or projecting conflicting task/objective gradients can improve robot policy training.

**Proposed difference.** Apply PCGrad only around gripper-transition samples in a shared pose/gripper BC-RNN.

**Distinguishing experiment.** Compare vanilla, global PCGrad, and contact-window PCGrad on multi-task Lift/Can/Square.

**Rejection.** This is a conditional optimizer/loss modification whose scientific mechanism is not separable from generic gradient surgery. It is not retained.

### Candidate D — Local controllability-weighted BC (rejected)

**Exact prior claim.** Stable-BC and physics-informed imitation/control use control-theoretic or physical constraints to shape supervised policies.

**Already solved.** Physical feasibility and stability can already be injected into imitation objectives.

**Proposed difference.** Weight action error by a finite-difference local end-effector Jacobian or controllability Gramian.

**Distinguishing experiment.** Compare Euclidean MSE, per-dimension normalization, and the local physical metric under the same data and model.

**Rejection.** The proposed change is a loss/metric swap with no independent causal mechanism beyond reweighting; it fails the project admission rule.

## Measurement-first admission audit for Candidate A

1. **Quantity:** the conditional action distribution and deterministic executed mean under normalized action bounds.
2. **Existence:** a bounded head can expose a normalized density and bounded mean; this must be implemented without treating a clipped distance as likelihood.
3. **Direct access:** the head parameters, sampled/mean action, and post-wrapper action are directly logged.
4. **Identifiability:** boundary-stratified paired rollouts and exact action logging distinguish support mismatch from ordinary approximation error.
5. **Surrogate check:** no latent pre-clipped command or heuristic action preference is used.
6. **Leakage audit:** split by whole demonstration episode; evaluate with randomized seeds and matched initial states; do not stratify on outcomes used for tuning.
7. **Negative controls:** interior-only states, tanh-squashed BC, temperature-matched bounded head, and action replay through the same controller.
8. **Cheapest kill:** boundary-mass/provenance preflight before any policy training.

## Current admission status

The independent review returned **`ZERO`**. Candidate A is rejected as an action-head/loss swap because scale-adjusted truncated Gaussian already exists and the preferred deterministic BC-RNN baseline already uses a bounded tanh output. Candidate B is a direct latency prior; Candidate C is GAP-equivalent gradient routing; Candidate D is a control-informed loss swap. The boundary preflight is preserved as a diagnostic only: its boundary mass came from a deliberately saturating legal trace and does not establish support mismatch for the frozen BC-RNN baseline. No scientific policy comparison is authorized. No TCI repair, ASCC/CAEA resurrection, delay variant, phase variant, or gradient-surgery variant is permitted.

## Evidence and reproducibility

* TCI policy-faithful negative: `p0-tci-bcrnn-identifiability/BC_RNN_TCI_IDENTIFIABILITY_REPORT.md`, commit `fac9e3209510f513d6ee443f24761176efbf2ba1`.
* Independent TCI fallback receipt: `p0-tci-bcrnn-identifiability/INDEPENDENT_BCRNN_SOL_FALLBACK_REVIEW.md`.
* Native and wrapper intervention substrates remain reusable infrastructure only; they are not scientific evidence for Candidate A.
* No local paper corpus was available for this pass. No package/runtime was installed or repaired, no dataset or checkpoint was downloaded, and no GPU/DCU job or policy-training rollout was launched. The existing qualified CPU robosuite runtime was used only for the bounded boundary-mass diagnostic; that diagnostic is not a scientific policy comparison.
* Independent receipt: `p0-support-bounded-bc/INDEPENDENT_REIDEATION_REVIEW.md`, reviewer `gpt-6-luna / max`, thread `/root/reideation_candidate_review`, verdict `ZERO`.
