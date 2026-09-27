# Conditional Final Proposal: Action-Swap Consequence Consistency

**Status: PROCEED WITH CAUTION TO PILOT**

A recurrent imitation policy may confuse visually aliased prefixes whose recent actions caused different hidden object states. The proposed robot-specific mechanism forms *valid same-latent-state executable action interventions* and trains the recurrent hidden state to predict whether the action-conditioned successor feature will diverge. The claim is narrower than generic predictive memory: pairwise consequence comparisons should improve closed-loop control under partial observability beyond recurrence, next-state prediction, transition-surprise reset, generic action-conditioned contrastive learning, and adaptive-memory controls.

The independent `gpt-6-astra` reviewer (xhigh; task/thread `/root/independent_reviewer`) found a narrow novelty margin against PAM, MEMBOT, JEPA Policy, CIVIL, transition-surprise memory, and especially CAPE (arXiv:2606.07304). Logged-action swaps alone are invalid because they confound latent state and can create malformed/leaky tuples. The proposal survives only conditionally on exact cloned-state simulator interventions with freshly observed alternate successors and episode-held-out evaluation. If that substrate cannot be built after runtime qualification, verdict becomes **ABANDON / RE-IDEATE**.

No pilot was run in this discovery session: `SKIPPED — RUNTIME NOT QUALIFIED`.
