# Research brief for the human researcher

## What question we are studying

We are looking for a small, publishable method for embodied AI or robot learning that can be tested on a mature simulation stack in one to three days. The current preferred baseline is state-only behavior cloning in robosuite/robomimic-style tasks.

## What the latest idea did

Temporal Consequence Inversion (TCI) asked whether the physical consequences of nearby alternative actions could reveal which action a recurrent behavior-cloning policy chose, without assuming a policy likelihood. A real trained BC-RNN was evaluated from reconstructed histories and frozen hidden states. The test used equal-norm executable alternatives, fresh-process wrapper restoration, held-out underlying states, multi-horizon consequences, and shuffled controls.

## Evidence against it

On 40 unique states, held-out immediate and multi-horizon top-1 inversion were only weakly above chance and multi-horizon information gave no temporal advantage. Shuffled consequences were comparable. An independent fallback review judged the result a scientific null, so TCI is abandoned. ASCC action-swap supervision and CAEA deterministic-policy preference are also permanently excluded.

## What was searched next

The post-TCI structural search considered bounded-support behavior cloning, delay-calibrated BC, contact-transition gradient routing, phase/speed conditioning, and control-informed action metrics. Delay and phase mechanisms are directly covered by recent work such as Delay-Aware Diffusion Policy, RAPAC-DP, RACE, SAIL, and GAP. Gradient routing and physical loss variants are either direct prior work or generic optimizer/loss changes.

## Current result

The only conditional survivor, support-corrected bounded BC, was rejected by an independent `gpt-6-luna / max` review. The frozen deterministic BC-RNN already uses bounded tanh actions, and recent truncated-Gaussian and robot clipping work cover the proposed distribution change. A deliberately saturating trace showed that boundary mass can be generated, but it did not show that the frozen baseline suffers a support mismatch. Therefore no candidate is authorized for a scientific pilot.

## What happens next

The repository now preserves a complete zero-candidate re-ideation report and reviewer receipt. A future search must change the scientific object rather than rename TCI, add another memory/reset rule, tune action horizons, or swap a loss. Before substantial implementation, any new candidate must define an identifiable measurement, a direct prior boundary, and a cheap closed-loop kill test.

## Concepts to learn next

The useful concepts here are covariate shift in behavior cloning, bounded action distributions, recurrent-policy state, intervention controls, independent state-level train/test splits, and the distinction between an engineering fix and a scientific mechanism.
