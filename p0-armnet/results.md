# ArmnetBench P0-B CPU Leakage Sanity Test

Population: 2,099 learned-policy single-arm episodes; teleoperation excluded. No images, policy inference, simulator, GPU, or video was used.

Outcome counts: {'failure': 1532, 'successful': 515, 'suboptimal': 52}
Mixed task × policy strata: 46; shorter-success strata: 46; longer-success strata: 0; median success-minus-non-success length difference: -213.64814814814815; median absolute standardized difference: 3.418479446304656.

## Cross-held-out baseline results

| Feature set | n | leave-task-out AUC | leave-policy-out AUC | leave-task-out balanced accuracy | leave-policy-out balanced accuracy |
|---|---:|---:|---:|---:|---:|
| length_only | 2099 | 0.9328883495145631 | 0.930441551436697 | 0.8275669314504266 | 0.8272751789742081 |
| nonlength_summary | 2099 | 0.8061157693439247 | 0.8779003628518192 | 0.681332744924978 | 0.7215596498970285 |
| nonlength_plus_length | 2099 | 0.9372352162400706 | 0.9542598313229381 | 0.8487968274982838 | 0.8791905707561047 |
| equal_prefix_100 | 2097 | 0.5621830686452114 | 0.6564703771344859 | 0.560295921402253 | 0.5894554495601367 |
| equal_prefix_200 | 1874 | 0.5336928397273225 | 0.6884754772685807 | 0.5150955366472607 | 0.5117637790051583 |

## Learned evaluator consequence

The evaluator comparison is restricted to the common subset with at least 100 frames. Scores are cross-fitted by held-out task; the human strict-success rate is only a ground-truth reference.

| Policy | n | human strict success | full + length | full without length | equal-duration prefix |
|---|---:|---:|---:|---:|---:|
| act | 329 | 0.2006 | 0.23066533911070533 | 0.21286882136953308 | 0.31677580577085257 |
| diffusion | 240 | 0.2208 | 0.27091036651143174 | 0.34511896728125874 | 0.2485733710674832 |
| grootn1.7 | 240 | 0.3458 | 0.4009552619362208 | 0.3031023929695492 | 0.2574324970627673 |
| molmoact2 | 479 | 0.1482 | 0.18067885852316332 | 0.17528588727017877 | 0.20138205054332228 |
| pi0 | 239 | 0.3640 | 0.34062928837196704 | 0.3871548968504261 | 0.2615283355179376 |
| pi0.5 | 240 | 0.4542 | 0.39824546730707494 | 0.41922353633608705 | 0.289687610144946 |
| smolvla | 330 | 0.1364 | 0.1778762898458149 | 0.21011297507805432 | 0.24222355595629358 |

Pairwise order inversions relative to full + length: {'full_length_plus_summary': 0, 'full_summary_without_length': 4, 'equal_duration_prefix': 7}

## Guarded interpretation

The release documents outcome-dependent trimming, but no released `success_cutoff_time` column or deterministic link to the original untrimmed rollout was found in the inspected artifacts. Therefore the strongest allowable interpretation is released-support leakage association (Level 1), not a causal post-processing effect. See `artifact_audit.md`.
