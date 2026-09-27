# Wrapper State-Closure Inventory

| Component | Captured/restored | Evidence / disposition |
|---|---:|---|
| Native MuJoCo integration state | Yes | `mjSTATE_INTEGRATION`, length 241 for Lift/Panda model; serialized and restored with `mj_setState` |
| `env.cur_time`, `env.timestep`, `env.done` | Yes | Explicit scalar snapshot |
| Episode metadata (`_ep_meta`) | Yes | JSON-encoded snapshot via `get_ep_meta` / `set_ep_meta` |
| Environment RNG | Yes | `env.rng.bit_generator.state` |
| Python global RNG | Investigated, unnecessary here | Tested path uses `env.rng`; no Python `random` calls in smoke path |
| Global NumPy RNG | Investigated, unnecessary here | No global NumPy random calls in smoke path |
| Observable cache and timers | Yes | `_obs_cache`; observable current value, delay, timer, sampled/enabled/active fields |
| Robot numeric buffers | Yes | Robot attributes including recent action/position/torque and end-effector buffers |
| Composite controller numeric state | Yes | Controller numeric fields and applied-action bookkeeping |
| Part-controller state | Yes | OSC goals, references, update flags, interpolator numeric state |
| Gripper state | Yes | Numeric gripper fields including current action and rotation offset |
| Task/object bookkeeping | Physical part: yes | Object/task physical state is in native integration state; Lift reward/done recomputed by fresh wrapper |
| Wrapper reset/task sampling | Seed/config captured; reset not used for replay | Fresh wrapper is constructed identically, then snapshot is applied; no reset sampling after restore |
| Action history / temporal buffers | Yes where present | Numeric robot/controller buffers recursively captured |
| robomimic preprocessing | Not instantiated | This gate uses the smallest real robosuite-compatible stack; robomimic wrapper qualification remains a follow-up if selected |
| Renderer/offscreen context | Disabled and unnecessary | `has_renderer=False`, `has_offscreen_renderer=False`, `use_camera_obs=False` |
| Camera/render RNG | Not applicable | No image observation path in this gate |
| Plugins/mocap/equality state | Native state includes them | Model reports no mocap/plugins in this Lift configuration; integration state still captures corresponding fields |
