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

The structural reset on 2026-09-29 mapped policy diagnostics, robustness, long-horizon behavior, temporal abstraction, multimodal grounding, non-ASCC context, data quality, failure analysis, embodiment transfer, representation behavior, inference-time adaptation, and evaluation sampling. Context-Causal BC is the only conditional survivor. It still needs a crossed texture-by-dynamics intervention, episode-disjoint leakage controls, and a renderer-qualified preflight. The CPU state-only preflight measured dynamics labels successfully, but EGL and OSMesa rendering failed, so no visual causal pilot is authorized.

The final reset verdict is **BLOCKED — BROADER RESEARCH SCOPE REQUIRED**. A future search must open an external empirical object or first qualify a vision/renderer substrate. It must not rename TCI, add another memory/reset rule, tune action horizons, route gradients, change action support, or swap a loss.

## Current problem-space discovery result (2026-09-29)

The broader VLA discovery cycle mapped twelve structurally different problem spaces and then deepened three: tactile/physical grounding, cross-embodiment execution, and reliable test-time adaptation. An independent `gpt-6-astra / medium` review ranked tactile/physical grounding first, cross-embodiment execution second, and test-time adaptation third. This is a problem-space decision, not a method or pilot authorization.

The recommended space is **tactile/physical grounding**, conditional on finding a public behavior-level proxy that can test whether future-contact or contact-sequence information improves closed-loop decisions on held-out materials or contact sequences. RCT provides a useful leakage-controlled tactile retrieval substrate, while HapTile and ForeTac-VLA show that synchronized tactile/action data and future tactile prediction are active directions. The immediate kill rule is to reject this space if the available data cannot connect representation quality to behavior, or if a short comparison against current-frame and short-history baselines shows no robust held-out-material or held-out-contact benefit.

The fallback is **cross-embodiment execution**, using a small frozen-policy study with independently manipulated visual, action, and kinematic factors. It remains high-impact but has a heavier interface and data burden. **Reliable test-time adaptation** is deferred because VANE, RoboTTT, and related work make direct novelty and runtime risk substantially higher. No new method, runtime repair, dataset download, training run, or simulator pilot is authorized by this result.

## Tactile proxy commitment (2026-09-29)

The resource gate passed conditionally through FreeTacMan. It provides public MIT-licensed visuo-tactile trajectories, TCP/gripper action channels, public preprocessing and policy code, and a task-organized release. The full release is about 50.3 GB, so the minimum pilot must use a predeclared 3–5-task subset with complete-episode and object/task-disjoint splits, frozen revisions, hashes, and byte counts. RCT remains a supporting perception benchmark; it does not contain action trajectories.

The independent `gpt-6-astra / medium` review accepted this only as an explicitly offline behavioral proxy. It rejected any claim that action prediction establishes closed-loop success or causal physical grounding. The focused idea search therefore recommends one question: whether tactile input has a phase-specific control value during contact entry, sustained contact, and release under leakage-resistant splits. The next authorized step is the **minimum offline scientific pilot** for that question. If action alignment, split independence, or phase labels fail, record `PIVOT — ACCESS`; if the tactile marginal disappears, record a null and do not add a new method.

## Minimum tactile pilot result (2026-09-29)

The pilot downloaded only 192,054,263 bytes from the pinned FreeTacMan release. A synchronization audit excluded nine episodes whose trajectory duration differed from the video by more than 1.5%; the corrected run used 35 qualified episodes, complete-episode splits, three seeds, a vision/proprioception baseline, genuine tactile, and shuffled tactile. On the primary episode-disjoint split, genuine tactile worsened contact action MAE in every seed (+0.0879, +0.0803, +0.1751; lower is better), and also worsened non-contact MAE. Shuffled tactile was worse still, showing correspondence matters but not that tactile improves control prediction.

The final verdict is **FAIL — MINIMUM TACTILE SCIENTIFIC PILOT**. This is negative evidence against the frozen contact-conditioned hypothesis in this offline proxy. It does not mean tactile sensing is useless in general and does not justify larger models, redefining contact, downloading the full dataset, or claiming anything about closed-loop robot success. The independent Astra reviewer was unavailable; the actual artifact review was completed by `gpt-6-luna / max` and confirmed the negative result.

## Concepts to learn next

The useful concepts here are covariate shift in behavior cloning, causal nuisance interventions, system identification, episode-disjoint train/test splits, context leakage, and the distinction between a diagnostic finding and a new mechanism.
