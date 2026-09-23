# Runtime Admission Audit

**Result: FAIL — `PIVOT — RUNTIME`.** The clean state-only reset/step/train/evaluate path required by `idea-stage/TRACK_A_RAL_P0_ADMISSION.md` was not established within the approximately 45-minute runtime-repair window. No scientific training or evaluation was started.

## Environment evidence

- Initial system interpreter: Python 3.13.13; PyTorch, MuJoCo, robomimic, robosuite, h5py, SciPy, and gym were absent.
- Isolated environment: `/tmp/aris_p0_env`, Python 3.10.21 (conda-forge).
- Successfully installed core: PyTorch 2.5.1, conda-forge CPU build (`pytorch` build `cpu_generic_py310_h50608de_15`; `libtorch` build `cpu_generic_h4d364f9_15`), NumPy 2.2.6. `torch.cuda.is_available()` returned `False`; PyTorch was capped at 4 threads for the check.
- Still absent when the runtime gate closed: SciPy, h5py, MuJoCo Python bindings, robomimic installation, robosuite installation, OpenCV, and Numba. Thus no state-only task construction, BC-RNN training, or evaluation smoke test could run.
- Source references only: robomimic v0.5.0 tag resolved to `ae5799f0fae05c4559ee1f9645b0f77eb5251929`; robosuite v1.5.2 tag resolved to `824ac14cefcfb7ec125fe5eb2e0bad7364466154`. The source checkouts were not installed as working runtime packages.

## Bootstrap blockers

1. The official PyTorch CPU wheel index repeatedly failed its TLS connection. Switching to the conda-forge CPU package succeeded for PyTorch itself, but a first broad dependency transaction was interrupted by incomplete package downloads; it also requested MuJoCo 3.3.0 from conda-forge, where that exact package was unavailable.
2. A subsequent minimal pip dependency transaction was manually stopped once the approximately 45-minute gate had elapsed. It had not reached installation or a runtime smoke test; its NumPy wheel transfer was incomplete.

The second attempt does not extend the authority's time budget. The runtime kill is infrastructure evidence only, not a scientific result.

## Resource/accounting boundary

- Dataset, checkpoint, and video bytes downloaded: **0**.
- Persisted package archive/partial payload bytes in the task-specific conda cache: **266,217,662**.
- Compressed Git pack payloads for the two source checkouts: **310,640,487** bytes total (robomimic 55,669,258; robosuite 254,971,229).
- Exact persisted payload subtotal: **576,858,149 bytes**. This is the sum of retained package archive/partial files and Git pack files; it excludes HTTP headers/metadata and the transient PyPI wheel response.
- The pip log recorded **17,253,376 bytes** received from the interrupted NumPy wheel before the incomplete-read error; this response was not retained in the package cache. Adding this observed stream payload gives a countable payload subtotal of **594,111,525 bytes**, still excluding HTTP headers/index metadata and other small metadata responses. Therefore 594,111,525 is an exact counted payload subtotal, not a claim that every protocol byte is recoverable.
- GPU/DCU used: **No**. Simulator or renderer launched: **No**. Video used: **No**.
- Policy seeds trained: **None**. P0-A/P0-B rollouts: **None**.

No runtime, cache, source checkout, dataset, checkpoint, or rollout artifact is part of the Git commit.
