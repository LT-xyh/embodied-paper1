# Independent re-ideation review: bounded-support BC, delay calibration, and contact-gradient routing

**Date:** 2026-09-28  
**Reviewer:** `gpt-6-luna`  
**Reasoning effort:** `max`  
**Task path:** `/root/reideation_candidate_review`  
**Scope:** read-only scientific and prior review after the policy-faithful TCI identifiability failure.  
**Verdict:** **`ZERO` / `ABANDON`** — retain none of Candidates A, B, or C as a Track-A RA-L direction.

This receipt records a literature and identifiability review. It does not train a policy, launch a rollout, alter a runtime, or run a new experiment. The existing `boundary_preflight_results.json` was read as context; its rows are commands passed to `env.step` from a scripted probe, not latent pre-controller commands from a trained Gaussian BC policy.

## Candidate A — Bounded-Distribution Behavior Cloning (reject)

The proposal replaces an unbounded or clipped Gaussian action head with a Beta or scale-adjusted truncated Gaussian head, trained by exact log likelihood on `[-1,1]` actions. Its intended claim is that support mismatch at action limits causes contact failures.

The distributional mechanism is already established. *Truncated Gaussian Policy for Debiased Continuous Control* (AAAI 2025, [paper](https://ojs.aaai.org/index.php/AAAI/article/view/33988), DOI `10.1609/aaai.v39i17.33988`) identifies boundary bias from unbounded Gaussian policies and proposes the same **scale-adjusted truncated Gaussian** family. The Beta solution is older still; bounded-support Beta policies were proposed for continuous control before this search. This makes the proposed head a known distribution choice, not a new robot-learning mechanism.

There is also a close robot-specific prior for the proposed failure explanation. *Two-Steps Diffusion Policy for Robotic Manipulation via Genetic Denoising* (NeurIPS 2025, [arXiv:2510.21991](https://arxiv.org/abs/2510.21991)) studies Robomimic and D4RL manipulation, explicitly analyzes normalized `[-1,1]` actions, and attributes poor diffusion inference to clipping-induced out-of-distribution intermediate states. Its paper reports that higher clipping frequency tracks lower return and proposes an inference strategy that reduces clipping and selects lower out-of-distribution trajectories. BDBC would reuse that known support-mismatch explanation while changing the action head and training likelihood.

The preferred project substrate does not freeze the proposed baseline. Official robomimic v0.5.0 states that actions lie in `[-1,1]` and that most networks use a final tanh ([policy source](https://raw.githubusercontent.com/ARISE-Initiative/robomimic/v0.5.0/robomimic/models/policy_nets.py), lines 1–7). The ordinary `RNNActorNetwork` applies `tanh` to its action output (lines 629–635). The ordinary state-only `BC_RNN` used for the failed TCI gate is therefore deterministic and natively bounded. A Gaussian/GMM branch is a different policy configuration. In that branch, robomimic already exposes `use_tanh` and a `TanhWrappedDistribution` with bounded samples and the change-of-variables log-probability correction ([distribution source](https://raw.githubusercontent.com/ARISE-Initiative/robomimic/v0.5.0/robomimic/models/distributions.py), lines 9–41). `BC_Gaussian` and `BC_GMM` train with negative log likelihood ([BC source](https://raw.githubusercontent.com/ARISE-Initiative/robomimic/v0.5.0/robomimic/algo/bc.py), lines 231–297). Thus a valid comparison must first choose and freeze a probabilistic baseline; silently replacing ordinary `BC_RNN` with a Gaussian/GMM policy would change the policy family.

The support-mismatch hypothesis is not identifiable from boundary labels alone. A recorded action at `1` or `-1` can be a legal demonstrator command, a value intentionally normalized to the action cube, or a post-controller clip. The existing boundary probe records only the exact legal array passed to `env.step` and has no separate raw command. It cannot establish censoring or an out-of-bound sample. With robomimic's default low-noise evaluation, Gaussian policies emit an almost deterministic bounded mean, so there may be no executed clipping event to cause the proposed failure. If stochastic evaluation is enabled to manufacture out-of-bound samples, any gain can instead be a change in noise, variance, or decoding behavior.

For these reasons A is a head/distribution and loss swap, with no distinct robot-specific mechanism under the current statement. It is not admitted as a Track-A method.

### A's minimum admissibility and kill conditions

No scientific P0 should run under the current specification. A future **diagnostic-only** preflight could proceed only after all of the following are frozen:

1. a named Gaussian/GMM baseline and checkpoint, its stochastic or deterministic decode mode, and the exact controller action path;
2. a measured pre-controller action and the executed post-controller action, so out-of-bound sampling and clipping rates are observable;
3. a preregistered boundary-mass floor on held-out policy states; if the baseline produces no material out-of-bound mass, the support-mismatch hypothesis is not testable;
4. controls consisting of the clipped unbounded Gaussian, robomimic's correctly transformed tanh-Gaussian, and the proposed truncated/Beta head, with matched architecture, mean, variance, and decode mode;
5. contact-stratified closed-loop outcomes showing that any gain is concentrated in episodes with measured clipping and survives deterministic mean/mode decoding.

Kill before training if any action-domain or raw-command provenance is missing. Kill after a diagnostic if BDBC improves only NLL or action MSE, improves only under stochastic decoding, fails to beat both clipping and tanh controls, has no boundary-stratified contact benefit, or works on only one task/seed. A positive result under those controls would still be an empirical action-head study; it would require a new novelty argument before Track-A admission.

## Candidate B — Delay-calibrated BC (direct-prior reject)

The proposed idea is already the central claim of *Delay-Aware Diffusion Policy: Bridging the Observation-Execution Gap in Dynamic Tasks* (arXiv:2512.07697, revised March 2026, [paper](https://arxiv.org/abs/2512.07697)). That work uses measured inference delay during training and inference, delay-compensates trajectories, conditions the policy on delay, and explicitly states that the pattern is architecture-agnostic and transfers beyond diffusion policies. Restricting the same procedure to a state-only BC policy or contact tasks does not create a new mechanism.

The collision is reinforced by *Why Does Action Chunking Improve Behavioral Cloning Performance in Robotic Control?* (arXiv:2608.02547, [paper](https://arxiv.org/abs/2608.02547)), which directly analyzes delayed BC policies and randomized delay ensembles in simulation and on robots. It treats delay as a core temporal policy variable and shows that delayed policies can capture much of action-chunking's benefit. A generic delay-calibrated BC proposal therefore fails the direct-prior test. No P0 should run. A contact-phase-specific actuator model would be a newly specified candidate, not a repair of B.

## Candidate C — Contact-transition gradient routing (direct/near-prior reject)

The exact optimization pattern is present in *When would Vision-Proprioception Policies Fail in Robotic Manipulation?* (arXiv:2602.12032, accepted ICLR 2026, [paper](https://arxiv.org/abs/2602.12032)). GAP estimates motion-transition phase probabilities from proprioception and scales modality-specific behavior-cloning gradients by those probabilities. The paper evaluates MetaWorld and RoboSuite tasks, one- and dual-arm real systems, and VLA-compatible policies. Routing or reweighting gradients on contact transitions is a narrow relabeling of this transition-conditioned gradient adjustment unless it introduces a materially different causal object and control law.

The surrounding contact literature further reduces the novelty margin. *Contact-Guided Exploration for Non-Prehensile Locomanipulation with Multi-Critic RL* (RA-L 2025, [project page](https://tolomeis.github.io/contact-guided-exp/)) uses a dedicated contact critic with scheduled weighting and decay. *Contact-Aware Neural Dynamics* (CVPR 2026, [paper](https://arxiv.org/abs/2601.12796)) uses a contact predictor to condition a learned dynamics model, while *Learning to Act Through Contact* (2025, [paper](https://arxiv.org/abs/2510.03599)) makes explicit contact phases and goals central to policy learning. A contact-transition router with the stated scope is therefore either the same phase-conditioned gradient mechanism as GAP or a generic auxiliary-loss/parameter-routing variant. No P0 should run.

## Final decision

`ZERO` / `ABANDON`: none of A, B, or C is a substantive Track-A RA-L direction as currently defined.

- A has a potentially measurable engineering effect, but its core distribution and clipping mechanism are established, its preferred baseline is not frozen, and its support-mismatch premise is not identifiable from the available action provenance.
- B is directly covered by delay-aware imitation and delayed-policy/action-chunking work.
- C is directly covered by transition-conditioned gradient adjustment and is further surrounded by contact-conditioned critics and dynamics methods.

Do not launch a method P0 for any candidate. Re-open only with a newly specified robot-specific mechanism that survives a fresh primary-prior audit and a pre-implementation identifiability gate.
