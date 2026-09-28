# Independent Astra Audit — TCI consequence-identifiability preflight

## Reviewer identity and scope

- Model: `gpt-6-astra`
- Reasoning effort: `medium`
- Thread identity: `/root/tci_final_audit`
- Audit mode: independent, read-only, evidence-only; no code or experiment changes
- Inputs reviewed: `TCI_IDENTIFIABILITY_REPORT.md`, the machine-readable result, split manifest, intervention provenance, leakage audit, action and horizon specifications, `refine-logs/FINAL_PROPOSAL.md`, `refine-logs/EXPERIMENT_PLAN.md`, and `idea-stage/TCI_FINAL_CRITICAL_REVIEW_RECEIPT.md`.

## Exact gate verdict

**REVISE — TCI CONSEQUENCE IDENTIFIABILITY**

The intervention substrate is reproducible and the bookkeeping is substantially clean. The exact scientific TCI gate cannot pass because the executable policy is explicitly a scripted state-only measurement stub rather than the intended deterministic BC-RNN, and this run shows neither a temporal advantage over H=1 nor any preregistered H=1/H=12 sign inversion. It should not be declared a failure of the BC-RNN hypothesis, because the intended policy family was not measured; it therefore requires a controlled rerun before a scientific pilot.

## Evidence audit

### Unique-state independence and split

The manifest contains 40 distinct native integration-state SHA-256 values, with `duplicate_underlying_states=false` and zero train/test native-hash overlap. Whole episodes are kept in one split (seeds 100/102 train; 101/103 test), giving 20 states per split. Candidate order is randomized and the chosen candidate occupies all five positions (counts 6, 8, 8, 8, 10), so fixed-position metadata cannot explain rankings.

This supports identity and split separation. It does not make the 40 rows IID: five timesteps from each episode remain temporally correlated, and only four seeds/two episodes per seed are represented. Any later confidence interval must remain episode-clustered and must not treat state rows as independent replicates.

### Exact action construction and equal norm

The action specification and source implement a chosen 7-D Panda BASIC action and four fixed-angle orthogonal rotations (`theta=0.25`) in the normalized 7-D controller space, with no post-rotation clipping. I independently checked all 200 branch records in `intervention_provenance.json`: the maximum full-vector norm error between each alternative and its chosen action is approximately `1.11e-16`, and the maximum alternative-to-chosen distance mismatch is approximately `1.11e-16`. All components remain within the normalized [-1, 1] executable bounds. Thus equal norm and equal radius are supported by the stored actions. The alternatives are valid measurement interventions, subject to the scope limitation that all are generated around the scripted action.

### Fresh-process replay and state closure

The implementation launches a separate Python worker subprocess per captured state; each worker constructs a fresh environment, restores the serialized MuJoCo integration state plus wrapper/controller/RNG state, and runs two same-action null branches before alternatives. The stored null control reports maximum consequence error 0.0 and maximum restored-observation error 0.0 at tolerance `1e-10`. This is strong evidence for deterministic replay and wrapper closure in this environment.

The evidence establishes branch reproducibility, not external simulator or cross-version generality. It also uses the same scripted continuation controller after the first intervention at H=4 and H=12.

### Temporal versus immediate evidence

The held-out test set has five-way chance top-1 accuracy 0.20. Chosen-action top-1 is 0.25 at H=1 and 0.25 at H=12; the paired multi-minus-immediate difference is exactly 0.00 with bootstrap interval [0.00, 0.00]. The multi-horizon score exceeds chance only in the weak descriptive sense recorded by the result, not relative to H=1. The registered inversion event (`sign(D_1) != sign(D_12)`, both magnitudes > 0.005) occurs in 0/40 states, including 0/20 test states.

Therefore this run supplies no evidence for the frozen temporal-inversion claim and no evidence that longer-horizon consequence ranking adds information beyond the immediate consequence. Train results (0/20 immediate, 1/20 multi-horizon) do not rescue the held-out null.

### Shuffled control

The fixed-RNG within-state consequence shuffle gives test top-1 0.30, versus chance 0.20. Under the report's declared near-chance tolerance this is treated as near chance; it is not a positive control result. Because the unshuffled temporal score is only 0.25, the shuffled result does not reveal a hidden strong signal. The analysis must retain this control and report its tolerance explicitly in any successor run.

### Leakage

The leakage artifacts state that state ID, episode ID, timestep, trajectory ID, candidate position, and raw action norm are not used as predictive features; chosen positions are randomized; consequence rows are generated after state/action selection; and native-state overlap is zero. I found no evidence in the reviewed artifacts of post-outcome state selection or policy likelihood/preference scoring. This supports a clean measurement protocol. The limited number of correlated within-episode states remains a variance/generalization concern, not an observed leakage defect.

### Frozen hypothesis and policy mismatch

The proposal freezes the observed selected action, real same-state successor functional `G_H`, finite alternatives, and a margin-qualified short/long sign reversal. The preflight preserves those definitions and explicitly avoids preference, likelihood, confidence, or global-regret claims.

However, `action_generation_spec.md`, `intervention_provenance.json`, and the result all identify the policy as a deterministic state-only approach controller, with `not_bc_rnn=true`. The experiment plan requires the intended state-only robomimic BC-RNN for the main pilot. Because the measured controller has no recurrent hidden state and is not the intended policy artifact, zero inversion could reflect the controller's smooth scripted geometry rather than a negative result for TCI on BC-RNN decisions. Conversely, the exact replay and action geometry do not establish that a BC-RNN rerun will produce a signal.

A secondary protocol discrepancy is that this preflight uses H={1,4,12}, while the plan's main pilot names primary/sensitivity pairs such as (1,8) and (2,16). This does not invalidate the bounded substrate test, but the successor BC-RNN run must freeze and preregister one consistent horizon set before reading outcomes.

## Required revision

Run the same cloned-state, fresh-process, equal-radius, episode-held-out protocol with the actual deterministic BC-RNN checkpoint and frozen recurrent state. Preserve the current action construction, split rule, controls, and leakage safeguards; predeclare the horizon/margin set and test whether H>1 improves over H=1 and whether inversions occur on held-out Lift and Can states. Do not tune the controller, margins, horizons, or state selection to manufacture inversions. If the BC-RNN rerun also has zero inversion and no incremental held-out prediction, terminate TCI as a mechanism direction and downgrade any remaining result to descriptive finite-horizon evaluation.

## Final independent conclusion

The substrate passes replay, action-validity, split, and leakage checks. The consequence-identifiability/scientific gate remains **REVISE** because the only measured policy is a scripted stub and the observed temporal evidence is exactly null (and inversion is absent). This is insufficient for **PASS**, while **FAIL** would overinterpret a policy-family mismatch as a falsification of TCI.

