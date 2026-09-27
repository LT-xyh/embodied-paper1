# Intervention Substrate Feasibility Gate

This folder contains the narrow feasibility test for the Action-Swap Consequence Consistency proposal. It does not implement the proposal or train a policy.

Run with:

```bash
/tmp/aris_p0_env/bin/python p0-intervention-substrate/intervention_substrate_smoke.py
```

The script first captures a complete `mjSTATE_INTEGRATION` vector, serializes it, then restores that vector with `mj_setState` in independent fresh subprocesses. It performs a mandatory same-action null control and an alternate-action intervention. The evidence JSON records restoration error, null-control equality, successor differences, state closure, and leakage controls.
