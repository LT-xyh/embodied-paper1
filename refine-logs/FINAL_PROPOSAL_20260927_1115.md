# Final Proposal — Causal Action-Effect Alignment (CAEA)

## Status
PROCEED WITH CAUTION TO A LATER PILOT. This is a discovery artifact, not an implementation authorization. The score-identifiability gate is mandatory.

## Claim
For a fixed policy history and exactly cloned physical state, a policy's preference among equal-radius executable actions should predict short-horizon task-relevant successor value and imminent failure better than distance, nearest-demonstration, random, next-state-prediction, transition-surprise, contrastive-representation, and adaptive-memory controls.

## Scientific contribution
The contribution is a causal audit of the policy–environment decision relation using real same-state simulator interventions. It does not propose a recurrent-memory module, predictive auxiliary loss, learned world model, or generic robustness score. The result may be negative and would then reject the claim.

## Hard admission gate
A BC-RNN or policy used in the pilot must expose an identifiable candidate-action preference score under a fixed state/history (e.g., a properly defined log-density or stochastic candidate probability). If no such score exists, CAEA is undefined and must be abandoned rather than replaced by action distance or a newly invented score.

## Distinguishing evidence
Use exact wrapper-level cloning and fresh subprocesses. Hold history and state fixed, sample balanced equal-radius perturbations, measure real successor value/contact outcomes, and test held-out cross-task/seed rank alignment and failure lead time. Preregister horizon, tolerances, contact filters, and action candidate generation.

## Closest priors
CMA (2609.27247) audits history changes and warranted choices; WorldEcho/WorldSync (2608.24885) diagnose and train learned action-conditioned world models; PACT (2606.03949) uses counterfactual advantage for human-feedback credit correction. CAEA differs by fixing history and testing frozen-policy preference against ground-truth physical consequences without policy training.

## Scope
Primary substrate: state-only robomimic/robosuite/MuJoCo BC-RNN on Lift and Can. No VLA pretraining, video, real robot, or simulator modification is required.
