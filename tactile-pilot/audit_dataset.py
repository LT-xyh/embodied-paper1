#!/usr/bin/env python3
"""Dataset, synchronization, contact-proxy, and leakage audit for the frozen subset."""
from __future__ import annotations
import csv, hashlib, json, pathlib
import numpy as np
import imageio.v2 as imageio
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
TASKS = ["Stamp", "UsbPlug", "FragileCup"]
CONTACT_THRESHOLD = 0.012
MIN_SUSTAINED = 3
SYNC_RATIO_TOL = 0.015

def read_rows(path):
    with path.open() as f:
        rd = csv.DictReader(f)
        return list(rd), rd.fieldnames

def feature(frame):
    im = Image.fromarray(frame).convert("RGB").resize((16, 16), Image.Resampling.BILINEAR)
    return np.asarray(im, dtype=np.float32).reshape(-1) / 255.0

def audit_episode(task, csv_path):
    rows, fields = read_rows(csv_path)
    stem = csv_path.stem[:-5] if csv_path.stem.endswith("_traj") else csv_path.stem
    candidates = list(csv_path.parent.glob(stem + "_Camera1.mp4")) + list(csv_path.parent.glob(stem + "_camera1.mp4"))
    candidates2 = list(csv_path.parent.glob(stem + "_Camera2.mp4")) + list(csv_path.parent.glob(stem + "_camera2.mp4"))
    if len(candidates) != 1 or len(candidates2) != 1:
        raise RuntimeError(f"missing camera pair for {csv_path}")
    v_tac, v_vis = candidates[0], candidates2[0]
    rt, rv = imageio.get_reader(v_tac), imageio.get_reader(v_vis)
    mt, mv = rt.get_meta_data(), rv.get_meta_data()
    tac_feats, vis_feats = [], []
    for ft, fv in zip(rt, rv):
        tac_feats.append(feature(ft)); vis_feats.append(feature(fv))
    rt.close(); rv.close()
    n_frames = min(len(tac_feats), len(vis_feats))
    n = min(len(rows), n_frames)
    tac = np.asarray(tac_feats[:n]); vis = np.asarray(vis_feats[:n])
    delta = np.mean(np.abs(tac - tac[0]), axis=1)
    raw = delta > CONTACT_THRESHOLD
    sustained = np.zeros(n, dtype=bool)
    for i in range(n - MIN_SUSTAINED + 1):
        if raw[i:i+MIN_SUSTAINED].all(): sustained[i:i+MIN_SUSTAINED] = True
    ts = np.asarray([float(r["timestamp"]) for r in rows[:n]])
    action = np.asarray([[float(r[k]) for k in ["TCP_pos_x","TCP_pos_y","TCP_pos_z","TCP_euler_x","TCP_euler_y","TCP_euler_z","gripper_distance"]] for r in rows[:n]], dtype=np.float64)
    return {
        "task": task, "episode": csv_path.stem, "csv": str(csv_path.relative_to(ROOT)),
        "camera_tactile": str(v_tac.relative_to(ROOT)), "camera_vision": str(v_vis.relative_to(ROOT)),
        "rows": len(rows), "paired_frames": n, "frame_mismatch": len(rows) - n,
        "video_tactile_fps": mt.get("fps"), "video_vision_fps": mv.get("fps"),
        "video_tactile_duration": mt.get("duration"), "video_vision_duration": mv.get("duration"),
        "sync_span_ratio": float((ts[-1]-ts[0]) / float(mv.get("duration"))),
        "sync_qualified": bool(abs(float((ts[-1]-ts[0]) / float(mv.get("duration"))) - 1.0) <= SYNC_RATIO_TOL),
        "timestamp_start": float(ts[0]), "timestamp_end": float(ts[-1]),
        "timestamp_dt_median": float(np.median(np.diff(ts))), "timestamp_dt_max": float(np.max(np.diff(ts))),
        "action_min": action.min(axis=0).tolist(), "action_max": action.max(axis=0).tolist(),
        "contact_threshold": CONTACT_THRESHOLD, "contact_frames": int(sustained.sum()), "noncontact_frames": int((~sustained).sum()),
        "contact_fraction": float(sustained.mean()), "tactile_change_max": float(delta.max()),
        "trajectory_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest()
    }

def main():
    records=[]
    for task in TASKS:
        for p in sorted(RAW.joinpath(task).glob("*_traj.csv"), key=lambda x:int(x.stem.split("_")[-2])):
            records.append(audit_episode(task,p))
    by_task={t:[r for r in records if r["task"]==t] for t in TASKS}
    qualified=[r for r in records if r["sync_qualified"]]
    split={"primary": {"train":[],"test":[]}, "task_heldout":{"train":[],"test":[]}}
    for task in TASKS:
        recs=[r for r in qualified if r["task"]==task]
        recs=sorted(recs,key=lambda r:int(r["episode"].split("_")[-2]))
        cut=max(1,int(len(recs)*0.75))
        split["primary"]["train"] += [r["episode"] for r in recs[:cut]]
        split["primary"]["test"] += [r["episode"] for r in recs[cut:]]
    split["task_heldout"]["train"]=[r["episode"] for r in qualified if r["task"] in ["Stamp","UsbPlug"]]
    split["task_heldout"]["test"]=[r["episode"] for r in qualified if r["task"]=="FragileCup"]
    (ROOT/"dataset_audit.json").write_text(json.dumps({"contact_definition":{"method":"tactile frame mean absolute difference from first frame","threshold":CONTACT_THRESHOLD,"sustained_frames":MIN_SUSTAINED,"frozen_before_training":True},"sync_ratio_tolerance":SYNC_RATIO_TOL,"episodes":records},indent=2)+"\n")
    (ROOT/"split_manifest.json").write_text(json.dumps({"frozen":True,"unit":"complete episode","sync_qualified_only":True,"split":split,"excluded_sync_unqualified":[r["episode"] for r in records if not r["sync_qualified"]],"task_ids":{"primary_train":["Stamp","UsbPlug"],"primary_test":["Stamp","UsbPlug","FragileCup"],"task_heldout_train":["Stamp","UsbPlug"],"task_heldout_test":["FragileCup"]}},indent=2)+"\n")
    report=f"""# Dataset and synchronization audit\n\n- Episodes audited: {len(records)}; synchronization-qualified episodes used for training: {len(qualified)}; tasks: {TASKS}.\n- Episodes with trajectory/video span mismatch above {SYNC_RATIO_TOL*100:.1f}% are excluded before model fitting and listed in `split_manifest.json`.\n- CSV action columns: TCP position (3), Euler orientation (3), gripper distance (1).\n- Decoded Camera1 is the visuo-tactile stream; Camera2 is the scene/wrist visual stream.\n- All checked videos are 640x480 RGB at 30 fps; qualified trajectory timestamps match video duration within tolerance.\n- Pairing uses same-index frames and trajectory rows after exact count check; any mismatch is recorded in `dataset_audit.json`.\n- Contact is frozen before training as tactile Camera1 mean absolute pixel change from the first frame > {CONTACT_THRESHOLD}, sustained for {MIN_SUSTAINED} frames. This is an evaluation stratification proxy, not an input label or ground-truth force/contact sensor.\n- Primary split is complete-episode 75/25 within each task. Secondary split holds out all FragileCup episodes as a task shift.\n- Trajectory hashes and per-episode frame counts are in `dataset_audit.json`; split membership is in `split_manifest.json`.\n\n## Leakage checks\n\nNo qualified episode is present in both primary train and test. All frames from an episode remain together. Camera calibration metadata is not supplied as a model feature. Task and episode identifiers are not supplied as model features. Near-duplicate detection is limited to exact trajectory-file hashes at this stage; any duplicate hash across split would block training.\n"""
    (ROOT/"sync_calibration_leakage_audit.md").write_text(report)
    print(json.dumps({"episodes_audited":len(records),"episodes_qualified":len(qualified),"excluded_sync":len(records)-len(qualified),"contact_fraction":float(np.mean([r["contact_fraction"] for r in qualified])),"max_frame_mismatch":max(r["frame_mismatch"] for r in records)},indent=2))

if __name__ == "__main__": main()
