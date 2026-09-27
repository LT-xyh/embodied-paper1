# Wrapper State-Closure Runtime Audit

## Stack

- robosuite source: v1.5.2, commit `824ac14cefcfb7ec125fe5eb2e0bad7364466154`, loaded from `/tmp/robosuite-src-closure` via `PYTHONPATH`
- environment: robosuite `Lift`, one Panda, BASIC composite controller
- renderer: disabled; camera observations disabled
- Python: 3.10.21
- NumPy: 2.2.6
- PyTorch: 2.5.1 CPU build (not used by the closure test)
- MuJoCo: 3.3.0
- SciPy: 1.15.3
- robosuite support dependencies installed in the pre-existing isolated environment: glfw 2.10.2, absl-py 2.5.0, etils 1.13.0, PyOpenGL 3.1.10, termcolor 3.3.0, Pillow 12.3.0, tqdm 4.70.1, opencv-python-headless 5.0.0.93, numba 0.67.0, llvmlite 0.49.0

## Changes made for this gate

Only the isolated `/tmp/aris_p0_env` and `/tmp/robosuite-src-closure` were used. No repository runtime package was modified. The source checkout was obtained because the package index connection failed; no dataset, checkpoint, video, or GPU/DCU resource was used.

Pip-reported payloads during this gate were approximately: Pillow 6.9 MB, SciPy 37.7 MB, tqdm 80 kB, OpenCV headless 61.2 MB, numba 3.8 MB, llvmlite 59.9 MB, termcolor 7.7 kB. These are installer-reported rounded transfer sizes; exact protocol-byte accounting was not retained. MuJoCo and earlier substrate dependencies were already present from the previous gate.

## Runtime qualification result

The designated environment instantiated Lift/Panda and executed multi-step controller/environment evolution in fresh subprocesses. No renderer or image path was used.
