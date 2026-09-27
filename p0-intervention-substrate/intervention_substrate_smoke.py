#!/usr/bin/env python3
"""Fresh-process exact-state capture/restore and action intervention test."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, tempfile
import numpy as np
import mujoco

XML = r'''<mujoco model="intervention_substrate">
  <option timestep="0.002" integrator="RK4" gravity="0 0 -9.81" iterations="50" tolerance="1e-12"/>
  <default><joint damping="0.15" armature="0.02"/><geom density="500"/></default>
  <worldbody><body name="slider" pos="0 0 0.15">
    <joint name="hinge" type="hinge" axis="0 1 0" pos="0 0 0"/>
    <geom name="payload" type="box" size="0.08 0.08 0.08"/>
  </body></worldbody>
  <sensor><jointpos joint="hinge"/><jointvel joint="hinge"/></sensor>
  <actuator><motor name="motor" joint="hinge" gear="1" ctrllimited="true" ctrlrange="-1 1"/></actuator>
</mujoco>'''
SPEC = mujoco.mjtState.mjSTATE_INTEGRATION

def digest(a): return hashlib.sha256(np.asarray(a, dtype=np.float64).tobytes()).hexdigest()

def model_data():
    m = mujoco.MjModel.from_xml_string(XML); return m, mujoco.MjData(m)

def capture():
    m, d = model_data(); d.qpos[:] = [0.23]; d.qvel[:] = [-0.11]; d.ctrl[:] = [0.0]; mujoco.mj_forward(m, d)
    n = mujoco.mj_stateSize(m, SPEC); s = np.zeros(n); mujoco.mj_getState(m, d, s, SPEC)
    return {"state_spec": "mjSTATE_INTEGRATION", "state": s.tolist(), "state_hash": digest(s), "state_size": int(n), "time": float(d.time), "qpos": d.qpos.tolist(), "qvel": d.qvel.tolist(), "model_nq": int(m.nq), "model_nv": int(m.nv), "model_nu": int(m.nu), "nuserdata": int(m.nuserdata), "nmocap": int(m.nmocap), "nplugin": int(m.nplugin)}

def restore_step(state_path, action):
    m, d = model_data(); payload = json.load(open(state_path)); s = np.asarray(payload["state"], dtype=np.float64)
    if len(s) != mujoco.mj_stateSize(m, SPEC): raise RuntimeError("state size mismatch")
    mujoco.mj_setState(m, d, s, SPEC); mujoco.mj_forward(m, d)
    restored = np.zeros(len(s)); mujoco.mj_getState(m, d, restored, SPEC)
    restore_err = float(np.max(np.abs(restored - s)))
    d.ctrl[:] = [action]; mujoco.mj_step(m, d)
    obs = np.concatenate([d.qpos.copy(), d.qvel.copy(), d.sensordata.copy(), d.xpos[1].copy()])
    post = np.zeros(len(s)); mujoco.mj_getState(m, d, post, SPEC)
    return {"action": float(action), "pre_state_hash": digest(s), "restore_max_abs_error": restore_err, "post_state": post.tolist(), "post_state_hash": digest(post), "observation": obs.tolist(), "qpos": d.qpos.tolist(), "qvel": d.qvel.tolist(), "sensordata": d.sensordata.tolist(), "time": float(d.time)}

def fresh_restore(state_path, action):
    p = subprocess.run([sys.executable, __file__, "--restore", state_path, str(action)], check=True, text=True, capture_output=True)
    return json.loads(p.stdout)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--capture", action="store_true"); ap.add_argument("--restore"); ap.add_argument("action", nargs="?", type=float); args = ap.parse_args()
    if args.capture: print(json.dumps(capture(), sort_keys=True)); return
    if args.restore: print(json.dumps(restore_step(args.restore, args.action), sort_keys=True)); return
    capproc = subprocess.run([sys.executable, __file__, "--capture"], check=True, text=True, capture_output=True)
    cap = json.loads(capproc.stdout)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as f:
        json.dump(cap, f); f.flush()
        a, ap_ = 0.35, -0.40
        null1, null2 = fresh_restore(f.name, a), fresh_restore(f.name, a)
        factual, alternate = fresh_restore(f.name, a), fresh_restore(f.name, ap_)
    same_pre = all(x["pre_state_hash"] == cap["state_hash"] for x in [null1, null2, factual, alternate])
    restore_err = max(x["restore_max_abs_error"] for x in [null1, null2, factual, alternate])
    null_state_err = float(np.max(np.abs(np.array(null1["post_state"]) - np.array(null2["post_state"]))))
    null_obs_err = float(np.max(np.abs(np.array(null1["observation"]) - np.array(null2["observation"]))))
    alt_state_delta = float(np.max(np.abs(np.array(factual["post_state"]) - np.array(alternate["post_state"]))))
    alt_obs_delta = float(np.max(np.abs(np.array(factual["observation"]) - np.array(alternate["observation"]))))
    result = {"verdict": "PASS — INTERVENTION SUBSTRATE" if same_pre and restore_err <= 1e-12 and null_state_err <= 1e-12 and null_obs_err <= 1e-12 and alt_state_delta > 1e-9 and alt_obs_delta > 1e-9 else "FAIL — INTERVENTION SUBSTRATE", "fresh_processes": 5, "capture": cap, "same_pre_state": same_pre, "restore_max_abs_error": restore_err, "null_control": {"max_state_abs_error": null_state_err, "max_observation_abs_error": null_obs_err, "tolerance": 1e-12}, "alternate_intervention": {"factual_action": a, "alternate_action": ap_, "max_state_delta": alt_state_delta, "max_observation_delta": alt_obs_delta}, "state_closure": {"captured": "mjSTATE_INTEGRATION", "includes": ["time", "qpos", "qvel", "act", "warmstart", "ctrl", "qfrc_applied", "xfrc_applied", "eq_active", "mocap", "userdata", "plugin state"], "model_task_wrapper_state": "none in minimal native MuJoCo substrate", "rng": "no stochastic calls"}, "leakage_audit": {"trajectory_id": "none", "episode_id": "none", "phase": "none", "timestep": "fixed and identical", "intervention_label_source": "executed action and measured successor", "cross_trajectory_swap": False}, "evidence": {"null_1": null1, "null_2": null2, "factual": factual, "alternate": alternate}}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__": main()
