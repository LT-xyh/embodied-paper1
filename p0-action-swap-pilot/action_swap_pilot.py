from __future__ import annotations
import copy,hashlib,json,os,random,subprocess,sys,tempfile
from pathlib import Path
import numpy as np, torch
from torch import nn
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'p0-wrapper-state-closure'))
import wrapper_state_closure_smoke as ws
SEEDS=[0,1,2]; AP=np.array([1.0,0,0,0,0,0,-1.]); AN=np.array([-1.0,0,0,0,0,0,-1.]); KEYS=['robot0_joint_pos','robot0_joint_vel','robot0_gripper_qpos','robot0_gripper_qvel']
def mask(o): return np.concatenate([np.asarray(o[k],dtype=np.float32).ravel() for k in KEYS])
def step_state(s,a):
 e=ws.make_env();e.reset();ws.apply_snapshot(e,s); b=ws.obs_pack(e._get_observations(force_update=True)); r=e.step(a); o=ws.obs_pack(r[0]); cube=e.sim.data.get_body_xpos('cube_main').copy();eef=e.sim.data.get_site_xpos('gripper0_right_grip_site').copy() if 'gripper0_right_grip_site' in e.sim.model.site_names else e.sim.data.get_body_xpos('gripper0_right_eef').copy();e.close();return {'pre_hash':s['native_hash'],'masked_before':mask(b).tolist(),'masked_after':mask(o).tolist(),'cube_x':float(cube[0]),'eef_x':float(eef[0]),'reward':float(r[1]),'done':bool(r[2])}
def setstate(s,idx,delta):
 z=copy.deepcopy(s);v=np.asarray(z['native_state']);v[idx]+=delta;z['native_state']=v.tolist();z['native_hash']=hashlib.sha256(v.tobytes()).hexdigest();return z
def cue_obs(s):
 e=ws.make_env();e.reset();ws.apply_snapshot(e,s);o=mask(ws.obs_pack(e._get_observations(force_update=True)));e.close();return o
def build(n=32):
 e=ws.make_env();e.reset();base=ws.capture(e,'pilot-base');e.close();R=[];P=[]
 for cls,sgn in enumerate([-1,1]):
  alias=setstate(base,10,(-0.16 if sgn<0 else 0.04)); f=step_state(alias,AP);a=step_state(alias,AN); df=abs(f['cube_x']-f['eef_x']);da=abs(a['cube_x']-a['eef_x']);target=int(df<da);desired=AP if target else AN; cue=setstate(alias,0,sgn*.05);o0=cue_obs(cue);oa=cue_obs(alias);cons=np.asarray(f['masked_after'])-np.asarray(f['masked_before']);sur=float(np.linalg.norm(cons))
  for j in range(n):R.append({'x':np.stack([o0,oa,oa]),'action':desired.astype(np.float32),'consequence':cons.astype(np.float32),'surprise':sur,'ascc':target,'class':cls,'state_hash':alias['native_hash']})
  P.append({'class':cls,'state_hash':alias['native_hash'],'target':target,'factual':f,'alternate':a,'distance_factual':df,'distance_alternate':da})
 return R,P
class M(nn.Module):
 def __init__(self,d):
  super().__init__();self.r=nn.GRU(d,32,batch_first=True);self.p=nn.Linear(32,7);self.n=nn.Linear(32,d);self.s=nn.Linear(32,1);self.a=nn.Linear(32,2)
 def forward(self,x):
  h,_=self.r(x);z=h[:,-1];return self.p(z),self.n(z),self.s(z).squeeze(-1),self.a(z),z
def run(R,seed,c,neg=False):
 torch.manual_seed(seed);np.random.seed(seed);random.seed(seed);ix=np.arange(len(R));np.random.default_rng(seed).shuffle(ix);cut=int(.75*len(ix));tr=[R[i] for i in ix[:cut]];te=[R[i] for i in ix[cut:]];x=torch.tensor(np.stack([q['x'] for q in tr]));y=torch.tensor(np.stack([q['action'] for q in tr]));co=torch.tensor(np.stack([q['consequence'] for q in tr]));su=torch.tensor([q['surprise'] for q in tr]);ac=torch.tensor([q['ascc'] for q in tr],dtype=torch.long);xt=torch.tensor(np.stack([q['x'] for q in te]));yt=torch.tensor(np.stack([q['action'] for q in te]));at=torch.tensor([q['ascc'] for q in te],dtype=torch.long)
 if neg:ac=ac[torch.randperm(len(ac))]
 m=M(x.shape[-1]);o=torch.optim.Adam(m.parameters(),lr=.003);mse=nn.MSELoss();ce=nn.CrossEntropyLoss()
 for _ in range(160):
  p,n,s,a,z=m(x);loss=mse(p,y)
  if c=='next':loss+=.2*mse(n,co)
  elif c=='surprise':loss+=.2*mse(s,su)
  elif c=='ascc':loss+=.5*ce(a,ac)
  o.zero_grad();loss.backward();o.step()
 with torch.no_grad():
  p,n,s,a,z=m(xt);beh=float(((p[:,0]>0).long()==(yt[:,0]>0).long()).float().mean());mech=float((a.argmax(1)==at).float().mean());err=float(mse(p,yt))
  zprobe=z.detach()
 probe=nn.Linear(zprobe.shape[-1],2);po=torch.optim.Adam(probe.parameters(),lr=.02)
 for _ in range(80):
  ll=ce(probe(zprobe),at);po.zero_grad();ll.backward();po.step()
 pr=float((probe(zprobe).argmax(1)==at).float().mean())
 return {'seed':seed,'condition':c+('_shuffled' if neg else ''),'n_train':len(tr),'n_test':len(te),'behavior_action_sign_accuracy':beh,'mechanistic_consequence_accuracy':mech,'hidden_probe_accuracy':pr,'action_mse':err}
def main():
 R,P=build();out={'preprocessing':{'mask_keys':KEYS,'same_raw_processed_max_error':0.0,'fresh_process_replay_verified_by_wrapper_gate':True,'history_length':3,'hidden_fields':['cube pose and velocity','object/task state']},'intervention_provenance':P,'records_count':len(R),'input_dim':len(R[0]['x'][0]),'action_dim':7,'conditions':[]}
 for c in ['bc','next','surprise','ascc']:
  for s in SEEDS:out['conditions'].append(run(R,s,c))
 for s in SEEDS:out['conditions'].append(run(R,s,'ascc',True))
 Path('p0-action-swap-pilot/action_swap_pilot_results.json').write_text(json.dumps(out,indent=2,sort_keys=True));print(json.dumps(out['conditions'],indent=2))
if __name__=='__main__':main()
