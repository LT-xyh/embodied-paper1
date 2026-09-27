# Action-Swap Consequence Consistency Minimum Scientific Pilot

## Final verdict

**FAIL — SCIENTIFIC PILOT**.

The intervention substrate and preprocessing path were valid, but the minimum experiment did not establish the proposed mechanism. Genuine same-state intervention targets were available; ASCC did not produce a stable mechanistic or behavioral advantage over controls, and the shuffled intervention control did not materially weaken the result. The independent audit also found a fatal pilot-construction defect: the intended robot-joint cue mutated state index 0 (simulation time), not a robot joint, and the two records were duplicated before the train/test split.

## Preflight and task construction

The pilot used robosuite v1.5.2 Lift/Panda/BASIC, state-only and no renderer. The policy input retained only robot joint positions/velocities and gripper positions/velocities. Cube object pose and object/task state were hidden. The history length was three. The final two timesteps shared the same policy-facing robot observation while the hidden cube x state differed; the first timestep was a real restored robot-joint cue state. No metadata, timestep, episode id, intervention id, reward, or target information entered the policy observation.

Preprocessing qualification passed: the direct deterministic mask has zero repeated-processing error, no normalization or hidden cache, and inherits fresh-process zero-error evidence from the wrapper closure gate.

## Genuine interventions

For each hidden class, a complete wrapper state was serialized. The same state was restored independently for factual `[+1.0,0,0,0,0,0,-1.0]` and alternate `[-1.0,0,0,0,0,0,-1.0]` actions. The consequence target was derived from the measured post-step cube/eef distance ordering. State hashes and both measured successors are in `action_swap_pilot_results.json`.

The two hidden classes produced opposite consequence labels: class -1 target 0 and class +1 target 1. Thus the target was not a copied cross-trajectory label.

## Conditions and metrics

- A: BC-RNN
- B: BC-RNN + ordinary masked next-state/consequence auxiliary
- C: BC-RNN + scalar transition-surprise auxiliary
- D: BC-RNN + ASCC consequence-class auxiliary
- Negative: same ASCC loss with shuffled intervention labels

Three seeds were trained for 160 epochs on 48 train / 16 held-out examples per seed. Mechanistic metrics are consequence-class accuracy and a descriptive hidden-state probe. Behavioral metric is final action-sign accuracy for the relevant x decision.

Across seeds, all conditions were near chance on behavior (roughly 0.375–0.50) and showed no stable ASCC advantage. ASCC mechanistic accuracy was `[0.4375, 0.375, 0.50]`; shuffled ASCC was identical. BC, next-state, and transition-surprise controls were indistinguishable within this pilot. Hidden probes reached only 0.50–0.625. Because each of the two exact class records was repeated 32 times before the row-wise split, the train/test rows were not independent; this further invalidates any positive or negative generalization claim.

## Interpretation

The chain `genuine same-state intervention → better alias-sensitive representation → better policy decisions` stops after the first link. The intervention is genuine, but the proposed ASCC objective did not separate from ordinary auxiliary losses or shuffled labels. The result is therefore a negative scientific pilot, not runtime evidence. The current candidate should not be scaled into a full experiment suite without a new hypothesis and a substantially less degenerate data construction.

The bounded pilot is intentionally small and has only two latent classes, duplicated rows, and a defective cue. These defects mean the result is not a clean scientific falsification of every possible ASCC implementation. They do establish that this pilot instance cannot support the mechanism or justify scaling. The correct action is to stop the current candidate rather than rescue it by broadening the method.

No full LIBERO evaluation, image experiment, BC-RNN paper-scale training, P0-A, or P0-B was run.

## Independent review

A fresh independent reviewer (`gpt-6-astra`, `medium`, thread `/root/action_swap_pilot_reviewer`) returned **FAIL — SCIENTIFIC PILOT**. The reviewer confirmed credible intervention provenance but found the time-index cue bug, duplicated non-independent rows, no ASCC-vs-shuffled separation, and no supported mechanism chain. The reviewer’s rerun was unavailable because its own environment lacked MuJoCo; this is disclosed and no rerun is claimed.
