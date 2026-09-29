#!/usr/bin/env python3
"""Small CPU-only matched-feature pilot for the frozen tactile hypothesis."""
from __future__ import annotations
import json, pathlib, time
import numpy as np
import imageio.v2 as imageio
from PIL import Image
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
SEEDS = [0, 1, 2]
CONDS = ["vision_proprio", "vision_proprio_tactile", "vision_proprio_shuffled_tactile"]

def feat(frame):
    return np.asarray(Image.fromarray(frame).convert("RGB").resize((8,8), Image.Resampling.BILINEAR), dtype=np.float32).reshape(-1) / 255.0

def episode_arrays(rec):
    csvp = ROOT / rec["csv"]
    vals = []
    with csvp.open() as f:
        import csv
        for row in csv.DictReader(f):
            vals.append([float(row[k]) for k in ["TCP_pos_x","TCP_pos_y","TCP_pos_z","TCP_euler_x","TCP_euler_y","TCP_euler_z","gripper_distance"]])
    action=np.asarray(vals,dtype=np.float32)
    rt=imageio.get_reader(ROOT/rec["camera_tactile"]); rv=imageio.get_reader(ROOT/rec["camera_vision"])
    tac=[]; vis=[]
    for ft,fv in zip(rt,rv): tac.append(feat(ft)); vis.append(feat(fv))
    rt.close(); rv.close()
    n=min(len(action),len(tac),len(vis))-1
    # Predict the next action delta from the current synchronized observation.
    return {"episode":rec["episode"],"task":rec["task"],"vision":np.asarray(vis[:n]),"tactile":np.asarray(tac[:n]),"proprio":action[:n],"target":action[1:n+1]-action[:n],"contact":np.asarray([rec["contact_threshold"]]*n,dtype=np.float32)}

def load_all():
    audit=json.loads((ROOT/"dataset_audit.json").read_text())
    cache=ROOT/"features_cache.npz"
    meta=ROOT/"features_meta.json"
    arrays=[]
    for rec in audit["episodes"]:
        arrays.append(episode_arrays(rec))
    # Contact labels are recomputed from the cached per-frame tactile features using the frozen threshold.
    threshold=0.012
    for a in arrays:
        d=np.mean(np.abs(a["tactile"]-a["tactile"][0]),axis=1)
        raw=d>threshold; s=np.zeros(len(raw),dtype=bool)
        for i in range(max(0,len(raw)-2)):
            if raw[i:i+3].all(): s[i:i+3]=True
        a["contact"]=s
    # Save one compact cache for reproducibility and avoid decoding twice.
    flat={}; offsets={}; cur=0
    for a in arrays:
        offsets[a["episode"]]=[cur,cur+len(a["target"]),a["task"]]
        cur += len(a["target"])
        for k in ["vision","tactile","proprio","target","contact"]: flat.setdefault(k,[]).append(a[k])
    np.savez_compressed(cache, **{k:np.concatenate(v) for k,v in flat.items()})
    meta.write_text(json.dumps({"offsets":offsets,"threshold":threshold,"feature_size":192,"target":"next-step delta"},indent=2)+"\n")
    return np.load(cache), offsets

def gather(data, offsets, episodes):
    idx=[]; tasks=[]
    for ep in episodes:
        s,e,t=offsets[ep]; idx.extend(range(s,e)); tasks.extend([t]*(e-s))
    idx=np.asarray(idx,dtype=int)
    return {k:data[k][idx] for k in ["vision","tactile","proprio","target","contact"]}, np.asarray(tasks)

def shuffle_tactile(tac, owners, seed):
    rng=np.random.default_rng(seed); out=tac.copy(); donor=rng.permutation(len(tac))
    # Avoid the exact same row; this also destroys temporal correspondence.
    bad=donor==np.arange(len(tac)); donor[bad]=np.roll(donor,1)[bad]
    return out[donor]

def design(x, cond, shuffled=None):
    base=np.concatenate([x["vision"], x["proprio"]],axis=1)
    if cond=="vision_proprio": return base
    tac=x["tactile"] if shuffled is None else shuffled
    return np.concatenate([base,tac],axis=1)

def score(y, pred, mask):
    err=np.abs(y-pred)
    def mae(m): return float(err[m].mean()) if m.any() else None
    return {"overall_mae":mae(np.ones(len(y),dtype=bool)),"contact_mae":mae(mask),"noncontact_mae":mae(~mask),"n":int(len(y)),"contact_n":int(mask.sum()),"noncontact_n":int((~mask).sum())}

def run_split(data, offsets, split_name, train_eps, test_eps):
    tr,_=gather(data,offsets,train_eps); te,tasks=gather(data,offsets,test_eps)
    out=[]; runlog=[]
    for seed in SEEDS:
        scaler_x=StandardScaler(); scaler_y=StandardScaler();
        for cond in CONDS:
            shuf=None
            if cond.endswith("shuffled_tactile"):
                shuf=shuffle_tactile(te["tactile"],tasks,seed+100)
            Xtr=design(tr, "vision_proprio_tactile" if cond.endswith("tactile") else cond)
            Xte=design(te, "vision_proprio_tactile" if cond.endswith("tactile") else cond, shuf)
            Xtr=scaler_x.fit_transform(Xtr); Xte=scaler_x.transform(Xte)
            ytr=scaler_y.fit_transform(tr["target"])
            model=MLPRegressor(hidden_layer_sizes=(32,),activation="relu",solver="adam",batch_size=128,max_iter=35,random_state=seed,early_stopping=False,shuffle=True,tol=1e-5)
            t0=time.time(); model.fit(Xtr,ytr); pred=scaler_y.inverse_transform(model.predict(Xte)); elapsed=time.time()-t0
            m=score(te["target"],pred,te["contact"]); rec={"split":split_name,"seed":seed,"condition":cond,"seconds":elapsed,**m}; out.append(rec); runlog.append(rec)
            print(json.dumps(rec),flush=True)
    return out

def main():
    data,offsets=load_all(); split=json.loads((ROOT/"split_manifest.json").read_text())["split"]
    results=[]
    for name,s in split.items():
        results += run_split(data,offsets,name,s["train"],s["test"])
    (ROOT/"seed_level_metrics.json").write_text(json.dumps(results,indent=2)+"\n")
    (ROOT/"training_evaluation_log.jsonl").write_text("\n".join(json.dumps(r) for r in results)+"\n")
    # Aggregate deltas against matched vision/proprio per split and seed.
    summary=[]
    for split_name in sorted(set(r["split"] for r in results)):
      for seed in SEEDS:
        rows=[r for r in results if r["split"]==split_name and r["seed"]==seed]
        b=next(r for r in rows if r["condition"]=="vision_proprio")
        for c in ["vision_proprio_tactile","vision_proprio_shuffled_tactile"]:
          q=next(r for r in rows if r["condition"]==c)
          summary.append({"split":split_name,"seed":seed,"condition":c,"delta_contact_mae":q["contact_mae"]-b["contact_mae"],"delta_noncontact_mae":q["noncontact_mae"]-b["noncontact_mae"],"delta_overall_mae":q["overall_mae"]-b["overall_mae"],"contact_gain_over_baseline":b["contact_mae"]-q["contact_mae"],"noncontact_gain_over_baseline":b["noncontact_mae"]-q["noncontact_mae"]})
    (ROOT/"pilot_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps({"results":len(results),"summary":summary},indent=2))
if __name__=="__main__": main()
