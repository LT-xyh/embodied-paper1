# Wrapper State Closure Qualification Report

## Final verdict

**PASS — WRAPPER STATE CLOSURE**

This PASS covers the tested robosuite v1.5.2 Lift/Panda/BASIC stack with state-only observations and no renderer. It does not claim robomimic preprocessing closure or LIBERO closure.

## Test protocol

The smoke script constructs the real robosuite environment, captures a complete wrapper-level snapshot, serializes it, and restores it in independent fresh subprocesses. Each restore applies native MuJoCo integration state plus environment counters, episode metadata, RNG state, observable caches/timers/current values, robot buffers, composite/part-controller numeric state, and gripper state. It then executes a real environment step.

Three states were tested:

1. `early`: immediately after reset;
2. `evolved`: after five nontrivial environment steps;
3. `transition-proxy`: after fifteen additional controller/environment steps. A successful Lift transition was not reached by this bounded smoke sequence, so this label is explicitly a transition-proxy rather than a claimed success boundary.

## Results

| State | Same pre-state | Null state error | Null observation error | Reward equal | Done equal | Alternate state delta | Alternate observation delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| early | true | 0.0 | 0.0 | true | true | 0.2769165035 | 0.0289234694 |
| evolved | true | 0.0 | 0.0 | true | true | 0.2658094648 | 0.0281759412 |
| transition-proxy | true | 0.0 | 0.0 | true | true | 0.1445663420 | 0.0158536557 |

Tolerance for null state/observation comparisons: `1e-10`. Every restore used a separate fresh subprocess. The captured native state length was 241 for this model. Alternate actions were valid 7D robosuite actions and were executed by `env.step`; no unrelated trajectory action was substituted.

## Leakage and closure conclusion

The intervention label is the executed action, and the consequence target is the fresh successor observation/state. No trajectory ID, episode ID, phase label, or cross-trajectory pairing enters the target. Environment RNG and observable/controller buffers are explicitly included in the snapshot. Native physical task/object state is carried by the integration state; wrapper reward/done/task outputs are recomputed by the fresh environment.

The gate therefore establishes a reproducible wrapper-level intervention substrate for this state-only robosuite task. Before a scientific pilot, the exact selected benchmark must repeat this closure audit if it adds robomimic preprocessing, image observations, stochastic task randomization, or different controllers. The result authorizes design of the minimum scientific Action-Swap pilot only; it does not authorize training or P0-A/P0-B.

## Independent final audit

A fresh independent `gpt-6-astra` reviewer at `medium` reasoning audited and reran the evidence in the designated environment. The reviewer returned **PASS — WRAPPER STATE CLOSURE**, while explicitly limiting the result to this minimal native robosuite stack and noting that robomimic/LIBERO, renderer, stochasticity beyond the tested path, and policy-level scientific validity remain untested.
