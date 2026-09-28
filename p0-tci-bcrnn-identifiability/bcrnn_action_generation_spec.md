# Policy-faithful BC-RNN action specification

The factual policy is a frozen, deterministic, single-layer 64-hidden-unit
PyTorch GRU behavior-cloning policy. It was trained once on 12 generated Lift
demonstration episodes from seeds 200--207 and validated on four disjoint
episodes from seeds 206--207; evaluation states use seeds 100--103, so no
evaluation state is in the demonstration data.

At each evaluation state, the observation history starts at episode reset and
ends at the captured decision point. The history is normalized with the frozen
training mean and standard deviation, passed through the GRU, and the final
hidden state and tanh action are the actual policy decision. The hidden state is
not initialized randomly and is not replaced by a scripted controller.

The four alternatives are the existing TCI construction: fixed-angle
(`theta=0.25` radians) orthogonal rotations of the seven-dimensional chosen
action. For every state, all five actions are valid normalized robosuite
actions, alternatives have the same norm and the same distance to the chosen
action, and no clipping is applied after construction. Across 200 alternative
vectors, the maximum per-state norm mismatch is `3.89e-15` and the maximum
within-state chosen-distance mismatch is `4.72e-16`.
