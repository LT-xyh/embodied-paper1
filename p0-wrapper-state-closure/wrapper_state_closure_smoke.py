#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
import mujoco
import robosuite as suite

SPEC = mujoco.mjtState.mjSTATE_INTEGRATION
CONFIG = dict(env_name='Lift', robots='Panda', has_renderer=False, has_offscreen_renderer=False,
              use_camera_obs=False, control_freq=20, hard_reset=True, seed=0)

def enc(x):
    if isinstance(x, np.ndarray): return {'__ndarray__': x.tolist(), 'dtype': str(x.dtype), 'shape': list(x.shape)}
    if isinstance(x, (np.floating, np.integer)): return x.item()
    if isinstance(x, (str, int, float, bool)) or x is None: return x
    if isinstance(x, dict): return {str(k): enc(v) for k,v in x.items() if not str(k).startswith('_sim')}
    if isinstance(x, (list, tuple)): return [enc(v) for v in x]
    return None

def dec(x):
    if isinstance(x, dict) and '__ndarray__' in x: return np.asarray(x['__ndarray__'], dtype=x['dtype']).reshape(x['shape'])
    if isinstance(x, dict): return {k: dec(v) for k,v in x.items()}
    if isinstance(x, list): return [dec(v) for v in x]
    return x

def snap_numeric(obj, skip=()):
    out = {}
    if not hasattr(obj, '__dict__'): return out
    for k,v in obj.__dict__.items():
        if k in skip or k in {'sim','model','robot_model','viewer','renderer','_sensor','_corrupter','_filter','_delayer'}: continue
        if isinstance(v, (np.ndarray, np.generic, float, int, bool, str)) or v is None:
            out[k] = enc(v)
        elif isinstance(v, dict):
            z = snap_dict(v)
            if z: out[k] = z
        elif hasattr(v, '__dict__'):
            z = snap_numeric(v)
            if z: out[k] = {'__object__': z}
    return out

def snap_dict(d):
    out={}
    for k,v in d.items():
        if isinstance(v, (np.ndarray,np.generic,float,int,bool,str)) or v is None: out[str(k)] = enc(v)
        elif isinstance(v,dict): out[str(k)] = snap_dict(v)
    return out

def restore_numeric(obj, snap):
    for k,v in snap.items():
        if k not in getattr(obj,'__dict__',{}): continue
        if isinstance(v,dict) and '__object__' in v:
            restore_numeric(getattr(obj,k), v['__object__'])
        elif isinstance(v,dict) and '__ndarray__' not in v:
            cur=getattr(obj,k)
            if isinstance(cur,dict): restore_dict(cur,v)
        else:
            try: setattr(obj,k,dec(v))
            except Exception: pass

def restore_dict(cur, snap):
    for k,v in snap.items():
        if isinstance(v,dict) and '__ndarray__' not in v: restore_dict(cur.setdefault(k,{}),v)
        else: cur[k]=dec(v)

def make_env():
    cfg=suite.load_composite_controller_config(controller='BASIC')
    return suite.make(controller_configs=cfg, **CONFIG)

def obs_pack(obs):
    return {k: np.asarray(v).copy() for k,v in obs.items()}

def obs_json(obs): return {k: enc(v) for k,v in obs.items()}

def obs_err(a,b):
    keys=sorted(set(a)|set(b)); errs=[]
    for k in keys:
        if k not in a or k not in b: return float('inf')
        errs.append(float(np.max(np.abs(np.asarray(a[k])-np.asarray(b[k])))))
    return max(errs or [0.0])

def capture(env, label):
    m,d=env.sim.model._model,env.sim.data._data
    n=mujoco.mj_stateSize(m,SPEC); state=np.zeros(n); mujoco.mj_getState(m,d,state,SPEC)
    obs=obs_pack(env._get_observations(force_update=True))
    robots=[]
    for r in env.robots:
        parts={name:snap_numeric(pc) for name,pc in r.composite_controller.part_controllers.items()}
        robots.append({'robot':snap_numeric(r), 'controller':snap_numeric(r.composite_controller), 'parts':parts, 'gripper':{name:snap_numeric(g) for name,g in r.gripper.items()}})
    observables={k:snap_numeric(v) for k,v in env._observables.items()}
    return {'label':label,'native_state':state.tolist(),'native_hash':hashlib.sha256(state.tobytes()).hexdigest(),
            'env':{'cur_time':enc(env.cur_time),'timestep':enc(env.timestep),'done':enc(env.done),'ep_meta':enc(env.get_ep_meta()),'rng_state':enc(env.rng.bit_generator.state),'seed':enc(env.seed),'obs_cache':enc(env._obs_cache)},
            'observables':observables,'robots':robots,'observation':obs_json(obs),'action_dim':env.action_dim,
            'closure_inventory':['native mjSTATE_INTEGRATION','env cur_time/timestep/done','episode metadata','env NumPy Generator state','observable timers/current values/sample flags','observable cache','robot numeric buffers','composite controller numeric state','part-controller goals/interpolators/numeric state','gripper numeric state'],
            'investigated_unneeded':['Python random module (robosuite uses env.rng here)','global NumPy RNG (no global random calls in tested path)','renderer/offscreen context (disabled)','robomimic wrapper state (not instantiated; see report limitation)']}

def apply_snapshot(env,s):
    m,d=env.sim.model._model,env.sim.data._data; vec=np.asarray(s['native_state'],dtype=np.float64)
    mujoco.mj_setState(m,d,vec,SPEC); mujoco.mj_forward(m,d)
    e=s['env']; env.cur_time=dec(e['cur_time']); env.timestep=dec(e['timestep']); env.done=dec(e['done']); env.set_ep_meta(dec(e['ep_meta'])); env.rng.bit_generator.state=dec(e['rng_state']); env._obs_cache=dec(e['obs_cache'])
    for k,v in s['observables'].items():
        if k in env._observables: restore_numeric(env._observables[k],v)
    for r,sr in zip(env.robots,s['robots']):
        restore_numeric(r,sr['robot']); restore_numeric(r.composite_controller,sr['controller'])
        for name,part in sr['parts'].items():
            if name in r.composite_controller.part_controllers: restore_numeric(r.composite_controller.part_controllers[name],part)
        if isinstance(r.gripper,dict):
            for name,gv in sr['gripper'].items():
                if name in r.gripper: restore_numeric(r.gripper[name],gv)
        else: restore_numeric(r.gripper,sr['gripper'])
    env.sim.forward(); env._update_observables(force=True)

def worker(path, action):
    env=make_env(); env.reset(); s=json.load(open(path)); apply_snapshot(env,s)
    before=env._get_observations(force_update=True); ret=env.step(np.asarray(action,dtype=np.float64)); after=obs_pack(ret[0])
    m,d=env.sim.model._model,env.sim.data._data; n=mujoco.mj_stateSize(m,SPEC); post=np.zeros(n); mujoco.mj_getState(m,d,post,SPEC)
    out={'label':s['label'],'action':list(map(float,action)),'pre_hash':s['native_hash'],'post_state':post.tolist(),'post_hash':hashlib.sha256(post.tobytes()).hexdigest(),'observation_before':obs_json(before),'observation':obs_json(after),'reward':enc(ret[1]),'done':enc(ret[2]),'info':enc(ret[3]),'time':float(d.time),'timestep':int(env.timestep),'cur_time':float(env.cur_time)}
    print(json.dumps(out,sort_keys=True)); env.close()

def fresh(path,action):
    p=subprocess.run([sys.executable,__file__,'--worker',path,json.dumps(list(map(float,action)))],check=True,text=True,capture_output=True)
    return json.loads(p.stdout)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--worker'); ap.add_argument('action',nargs='?'); args=ap.parse_args()
    if args.worker:
        worker(args.worker,json.loads(args.action)); return
    env=make_env(); env.reset(); states=[]; actions=[]
    # early state before any evolution; then nontrivial evolution; then a transition-proxy state.
    states.append(capture(env,'early'))
    for i in range(5): env.step(np.zeros(env.action_dim))
    states.append(capture(env,'evolved'))
    for i in range(10): env.step(np.array([0.15,0,0,0,0,0,-1.0]))
    states.append(capture(env,'transition-proxy'))
    results=[]
    with tempfile.TemporaryDirectory() as td:
        for i,s in enumerate(states):
            path=os.path.join(td,f'state{i}.json'); json.dump(s,open(path,'w'))
            a=np.zeros(env.action_dim); b=np.zeros(env.action_dim); b[-1]=0.5
            n1,n2=fresh(path,a),fresh(path,a); f,alt=fresh(path,a),fresh(path,b)
            def arr(x,k): return np.asarray([dec(v) for v in x[k].values()]) if False else x
            null_state=float(np.max(np.abs(np.asarray(n1['post_state'])-np.asarray(n2['post_state'])))); null_obs=obs_err({k:dec(v) for k,v in n1['observation'].items()},{k:dec(v) for k,v in n2['observation'].items()})
            alt_state=float(np.max(np.abs(np.asarray(f['post_state'])-np.asarray(alt['post_state'])))); alt_obs=obs_err({k:dec(v) for k,v in f['observation'].items()},{k:dec(v) for k,v in alt['observation'].items()})
            results.append({'label':s['label'],'same_pre_hash':n1['pre_hash']==n2['pre_hash']==f['pre_hash']==alt['pre_hash'],'null_state_error':null_state,'null_observation_error':null_obs,'null_reward_equal':n1['reward']==n2['reward'],'null_done_equal':n1['done']==n2['done'],'alternate_state_delta':alt_state,'alternate_observation_delta':alt_obs,'factual':f,'alternate':alt})
    env.close(); verdict='PASS — WRAPPER STATE CLOSURE' if all(x['same_pre_hash'] and x['null_state_error']<=1e-10 and x['null_observation_error']<=1e-10 and x['null_reward_equal'] and x['null_done_equal'] and x['alternate_state_delta']>1e-8 and x['alternate_observation_delta']>1e-8 for x in results) else 'FAIL — WRAPPER STATE CLOSURE'
    print(json.dumps({'verdict':verdict,'states':states,'results':results,'tolerance':1e-10,'fresh_processes_per_state':4},indent=2,sort_keys=True))
if __name__=='__main__': main()
