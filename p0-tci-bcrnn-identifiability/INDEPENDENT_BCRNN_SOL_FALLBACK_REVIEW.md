# Independent BC-RNN TCI scientific-pilot review (GPT-6-Sol fallback)

## Reviewer identity and route

- Model: `gpt-6-sol`
- Reasoning effort: `medium`
- Thread identity: `/root/tci_bcrnn_scientific_review_sol_fallback`
- Review mode: independent, read-only, evidence-only; no experiments or code changes
- Requested primary route: `gpt-6-astra`
- Astra status: two review attempts were unavailable because of model-capacity failure; this document is the explicitly labeled Sol fallback review.

## Exact gate verdict

**`FAIL — TCI CONSEQUENCE IDENTIFIABILITY`**

This is a scientific null for the frozen TCI temporal mechanism after the policy-faithful rerun, rather than a technical protocol defect. The intended trained recurrent policy is present and measurable, the cloned-state and intervention controls pass, and the held-out result has no multi-horizon gain or registered temporal inversion. The earlier scripted-policy scope defect is therefore repaired; it does not justify another BC-RNN rerun or method rescue.

## Evidence reviewed

I read `BC_RNN_TCI_IDENTIFIABILITY_REPORT.md`, the complete `p0-tci-bcrnn-identifiability/` artifact set (action and horizon specifications, checkpoint metadata, training results, intervention provenance, state snapshots, split manifest, leakage audit, consequence records, result JSON, and gate source), the original `TCI_IDENTIFIABILITY_REPORT.md`, `refine-logs/FINAL_PROPOSAL.md`, `refine-logs/EXPERIMENT_PLAN.md`, `idea-stage/TCI_FINAL_CRITICAL_REVIEW_RECEIPT.md`, and the prior independent Astra audit for the predecessor scripted-policy gate.

## Policy fidelity and hidden-state repeatability

- The checkpoint is an ordinary deterministic single-layer 64-unit PyTorch GRU with a seven-dimensional tanh action head. The factual policy for all measurements is the trained network, not the scripted expert used only to generate demonstrations and evaluation trajectories.
- Training uses a fixed seed and one frozen configuration. The recorded train/validation action RMSE values are `0.00230` and `0.00511`; validation predicted-action standard deviation is `0.1173`, so the policy is not action-degenerate.
- Each decision action is obtained from the canonical observation history from reset through the captured timestep, normalized with frozen training statistics. The hidden state and action are reconstructed twice before branch evaluation. Across all 40 states, maximum repeated hidden-state error, repeated-action error, and stored-action error are all `0.0`.
- At H=4 and H=12, the same frozen BC-RNN is queried on each branch's subsequent observation with the branch-specific recurrent state. Thus the measured multi-horizon consequence is a policy continuation, not the predecessor scripted continuation.

These checks satisfy the policy-faithfulness requirement for this gate.

## Intervention, replay, and independence controls

- There are 40 unique captured states. Evaluation seeds 100--103 are disjoint from demonstration seeds 200--207; whole episodes are assigned to train/test (20 states each), with zero native-state hash overlap and no duplicate underlying state.
- Each state has the selected action plus four fixed-angle orthogonal alternatives. The recorded maximum norm mismatch is `3.89e-15`, and maximum within-state chosen-distance mismatch is `4.72e-16`; all candidates remain within normalized action bounds and no post-rotation clipping occurs.
- Every candidate is restored and executed in a fresh subprocess with the complete recorded simulator, wrapper, controller, observable, and RNG state. The same-action null has maximum consequence error `0.0` and maximum restored-observation error `0.0` at tolerance `1e-10`.
- Candidate order is randomized; the chosen action occupies all five positions with counts `6, 8, 8, 8, 10`. The leakage audit reports no use of state ID, episode ID, timestep, trajectory metadata, candidate position, or raw action norm; the hidden state is recomputed from history and is not used to score alternatives.

These are passed technical controls. They do not establish a positive TCI effect.

## Immediate, multi-horizon, shuffled, and inversion results

The declared consequence is `G_H = -distance(eef,cube) + 4*(cube_z-cube_z_at_capture) + 0.1*cumulative_reward`, with H in `{1,4,12}`. On the held-out 20-state split:

| measure | top-1 |
|---|---:|
| immediate H=1 | 0.35 |
| rank-aggregated H={1,4,12} | 0.35 |
| within-state shuffled consequence | 0.15 |

Five-way chance is `0.20`. The paired multi-horizon minus immediate difference is exactly `0.00` with bootstrap interval `[-0.20, 0.20]`. The genuine immediate relation is above chance and separates from the shuffled control, so the measurement is not empty. However, the longer horizon supplies no advantage over H=1. The preregistered margin-qualified sign change between `D_1` and `D_12` occurs in `0/40` states, including `0/20` held-out states. Train states also have zero inversion; their immediate and multi-horizon top-1 rates (`0.20` and `0.40`) cannot rescue the held-out temporal claim.

The correct interpretation is a real immediate consequence signal with a null temporal-inversion result. It does not support TCI's frozen claim that longer temporal consequence changes the action ranking or yields the registered inversion.

## Scientific decision and consequence

The predecessor gate was `REVISE` because it measured a scripted state-only stub rather than the intended BC-RNN. This rerun removes that technical scope objection and preserves the same state closure, action geometry, split, leakage, replay, and consequence definitions. Since the genuine trained recurrent policy still shows no held-out temporal advantage and no inversion, the remaining failure is scientific: the frozen TCI mechanism is not identifiable in this bounded pilot.

Under the proposal's own decision rule, the direction should be **abandoned**. Do not increase recurrent capacity, retune horizons or margins, add an auxiliary loss, redefine `G_H`, change the action neighborhood, or rename the immediate signal into a rescued TCI mechanism. The immediate consequence relation may be retained as descriptive evidence, but it cannot support the proposed temporal mechanism or authorize a larger TCI suite.

## Review boundary

This review makes no claim about real-robot behavior, Can, TCI training, or broader policy families. It decides only the policy-faithful Lift BC-RNN TCI consequence-identifiability gate represented by the immutable artifacts above. No code, checkpoint, result, or runtime state was modified.
