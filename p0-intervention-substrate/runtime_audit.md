# Intervention Substrate Runtime Audit

## Scope

This gate used only the minimum runtime needed to test exact MuJoCo state capture, restoration, and executable alternate actions. No robomimic/robosuite installation, dataset, checkpoint, video, policy, training, renderer, or GPU/DCU job was used.

## Runtime

- Environment: `/tmp/aris_p0_env` (pre-existing isolated environment)
- Python: 3.10.21
- NumPy: 2.2.6
- PyTorch: 2.5.1 CPU build (not used by the smoke test)
- MuJoCo Python: 3.3.0
- glfw: 2.10.2
- absl-py: 2.5.0
- etils: 1.13.0
- PyOpenGL: 3.1.10
- CUDA/DCU: not used
- Renderer/display: not used

## Runtime changes made in this gate

Installed into `/tmp/aris_p0_env` only:

```text
mujoco==3.3.0 (installed --no-deps)
glfw==2.10.2
absl-py==2.5.0
etils==1.13.0
PyOpenGL==3.1.10
```

The MuJoCo wheel transfer was reported by pip as 6.5 MB; glfw 248 kB; absl-py 137 kB; etils 170 kB; PyOpenGL 3.2 MB. Pip did not retain cache files or exact HTTP byte counters, so these are installer-reported rounded payload sizes, not an invented exact-byte total. No repository runtime files were modified.

## State-closure scope

The test uses native MuJoCo with no task wrapper, controller, actuator/mocap policy layer, stochastic RNG, equality schedule, userdata, or plugins. It captures `mjSTATE_INTEGRATION`, which includes time, qpos, qvel, actuator state, warmstart, controls, applied forces, equality activation, mocap, userdata, and plugin state. The minimal model has no nonzero wrapper/task state to capture. A robosuite task must repeat this audit for controller integrators, mocap targets, wrapper state, task randomization, and any environment RNG before a scientific pilot.
