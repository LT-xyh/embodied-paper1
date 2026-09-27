# CAEA Policy Candidate-Score Identifiability Gate

## Verdict

`FAIL — POLICY CANDIDATE-SCORE IDENTIFIABILITY`

This gate does not test CAEA performance. It tests whether the frozen proposal
has a scientifically interpretable, reproducibly queryable score
`s_pi(a | h_t)`. The answer is no for the intended policy family as currently
specified. The proposal names a possible likelihood or margin but does not
freeze a policy distribution, checkpoint, configuration, or executable score
path. The repository contains no BC-RNN/robomimic implementation or checkpoint,
and the relevant Python runtimes are not installed. Switching to
`BC_RNN_GMM` to obtain a likelihood would redefine the policy family and is
outside this gate.

## Scope and immutable inputs

- branch: `p0/caea-score-identifiability`
- discovery baseline: `89844a52b939232bbd3192e40859cd1ecd3fd23d`
- proposal inputs: `idea-stage/IDEA_REPORT.md`, `refine-logs/FINAL_PROPOSAL.md`,
  `refine-logs/EXPERIMENT_PLAN.md`
- no training, CAEA loss, scientific rollout, full simulator evaluation, or
  large download was performed

## Phase 1 — recovered score definition

The proposal uses the phrases “action likelihood/margin”, “properly defined
log-density or stochastic candidate probability”, and “policy action ranking”.
It does not select one of them, identify a checkpoint, or provide a policy
configuration. Therefore the exact current score is **undefined**, rather than
an admissible heuristic.

The intended substrate is described as state-only robomimic/robosuite/MuJoCo
BC-RNN. The repository has no tracked BC-RNN or robomimic source, policy
checkpoint, config, or inference script. `robomimic`, `torch`, `mujoco`, and
`robosuite` are also unavailable in the active Python environment.

The official robomimic source distinguishes two materially different paths:

1. `BC_RNN` creates `RNNActorNetwork`; `get_action` calls `forward_step` and
   returns a tanh-bounded action tensor. It does not return a distribution or
   `log_prob`.
2. `BC_RNN_GMM` is selected only when `gmm.enabled` is true. Its
   `RNNGMMActorNetwork.forward_train` constructs a
   `MixtureSameFamily` distribution, and the algorithm computes
   `dists.log_prob(actions)`.

Sources inspected: [robomimic `bc.py`](https://raw.githubusercontent.com/ARISE-Initiative/robomimic/master/robomimic/algo/bc.py),
[policy networks](https://raw.githubusercontent.com/ARISE-Initiative/robomimic/master/robomimic/models/policy_nets.py),
and [robomimic algorithm documentation](https://github.com/ARISE-Initiative/robomimic/blob/master/docs/introduction/implemented_algorithms.md).

## Mathematical semantics

For ordinary `BC_RNN`, the source path is equivalent to

`a_hat_t = tanh(f_theta(o_{<=t}, h_t))`,

with the recurrent state updated by `forward_step`. There is no native
definition of `p_theta(a | h_t)` or `s_pi(a | h_t)` for arbitrary candidate
actions. The tempting quantity `-||a - a_hat_t||^2` is a post-hoc distance,
not a policy probability, preference, confidence, or likelihood; using it
would violate the gate.

For the separate GMM variant, a possible native score would be

`s_pi(a | h_t) = log sum_k pi_k(h_t) N(a; mu_k(h_t), diag(sigma_k(h_t)^2))`,

with any tanh change-of-variables handled by the implementation. That quantity
is scientifically meaningful only after a concrete `BC_RNN_GMM` configuration
and checkpoint are frozen. None is present in the CAEA proposal or repository,
so it cannot be adopted as a rescue.

## Phase 3 — same-hidden-state candidate query

Status: `NOT EXECUTED — no frozen policy object/checkpoint/runtime`.

No valid query can establish identical `(h_t, a)` scores, ordering
invariance, batch-versus-single consistency, or non-mutating repeated queries
without an actual policy object. Running a synthetic arbitrary network would
not establish semantics for the intended BC-RNN family and was not substituted.

## Phase 4 — candidate-set invariance

Status: `NOT EXECUTED — score undefined`.

The proposal does not define a normalized candidate-set score. There is no
policy implementation on which to compare `{a1,a2}` with `{a1,a2,a3,a4}` or
reordered candidate sets. A set-dependent ranking introduced for this gate
would be a new heuristic.

## Phase 5 — leakage audit

The intended likelihood, if a native distribution existed, would be computable
before stepping the environment. That is only a conditional statement; the
current proposal has no extractable score path to audit. No successor state,
outcome, success label, trajectory identifier, episode identifier, or future
signal was used to manufacture one.

## Phase 6 — action-domain audit

The official `RNNActorNetwork` applies `tanh`, so its output is in the policy's
normalized action domain. The local project has no resolved config or wrapper
path connecting that output to robosuite controller scaling, clipping, gripper
conventions, or environment actions. Consequently the end-to-end action-domain
mapping is unverified. This is a second independent reason that a CAEA score
cannot currently be claimed reproducible.

## Required evidence summary

| Gate item | Result | Evidence |
|---|---|---|
| Exact proposed score | FAIL | proposal lists alternatives but freezes none |
| Native score for intended BC-RNN | FAIL | ordinary `BC_RNN` returns deterministic action only |
| Frozen policy/checkpoint | FAIL | no local code, config, checkpoint, or runtime |
| Same-hidden-state query | NOT EXECUTED | no policy object to query |
| Candidate-set invariance | NOT EXECUTED | no score exists |
| Pre-outcome leakage | CONDITIONAL ONLY | no score extraction path exists |
| Action-domain mapping | FAIL / UNVERIFIED | no local controller mapping |

## Scientific decision

The hard prerequisite fails. CAEA is therefore abandoned for this proposal:

`ABANDON CAEA / RE-IDEATE`

Do not rename the score, tune around the failure, use action distance, switch
silently to GMM, or proceed to the CAEA scientific pilot. A future direction
would require a separately frozen probabilistic policy family and checkpoint,
with a native pre-outcome log-density and explicit action-domain mapping. That
would be a new admission decision, not a repair of this gate.

## Independent audit

Fresh independent audit: `gpt-6-astra / medium`, thread
`/root/caea_score_gate_reviewer`. Verdict: `ACCEPT-FAIL-GATE` (confirming the
final FAIL verdict; no revision requested). The reviewer confirmed that the
ordinary `BC_RNN` factory path is deterministic and that `BC_RNN_GMM` is a
distinct recurrent GMM policy selected by `gmm.enabled`. It specifically
rejected imposing Gaussian noise around a deterministic mean or treating MSE
distance as an energy, because those choices add an untrained variance/base
measure and would invent a new score. A deterministic Dirac policy has no
ordinary finite Lebesgue log-density for arbitrary candidate actions.
