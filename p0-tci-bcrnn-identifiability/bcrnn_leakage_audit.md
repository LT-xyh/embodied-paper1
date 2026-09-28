# BC-RNN TCI leakage audit

The policy was trained only on demonstration seeds 200--207. Evaluation uses
40 unique native states from seeds 100--103; whole episodes remain in one
evaluation split (seeds 100/102 train, 101/103 test), and train/test native
hash overlap is zero. Evaluation identifiers, timestep, candidate position,
trajectory metadata, and action norm are not policy or analysis features.

Candidate order is randomized with the frozen per-state seed formula and the
chosen action occupies all five positions (6, 8, 8, 8, 10). The policy hidden
state is reconstructed from the pre-decision observation history, checked twice,
and then held fixed for the candidate query; alternatives never query or alter
the policy to manufacture a score. Consequences are generated only after the
state and action are fixed. The shuffled control permutes consequence rows
within state using seed 20260930.

Fresh subprocess restoration uses the qualified MuJoCo integration-state API
plus wrapper, controller, RNG, observable, and simulator auxiliary state. No
image observations, policy likelihood, preference score, or outcome-dependent
state selection is used.
