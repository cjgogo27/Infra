import argparse, copy, json, random
from pathlib import Path
import torch
from torch import nn
p=argparse.ArgumentParser()
p.add_argument('--output',default='lab-results/checkpoint.pt')
a=p.parse_args()
torch.set_num_threads(1)
torch.use_deterministic_algorithms(True)
def setup():
    m=nn.Sequential(nn.Linear(8,16),nn.Tanh(),nn.Linear(16,2))
    o=torch.optim.AdamW(m.parameters(),lr=1e-3)
    s=torch.optim.lr_scheduler.StepLR(o,step_size=3,gamma=.8)
    return m,o,s
def step(m,o,s):
    x=torch.randn(4,8);y=torch.randn(4,2)
    x=x*(.9+.2*random.random())
    o.zero_grad(set_to_none=True)
    loss=(m(x)-y).square().mean()
    loss.backward();o.step();s.step()
    return loss.item()
torch.manual_seed(17);random.seed(17)
m,o,s=setup()
for _ in range(5): step(m,o,s)
state=copy.deepcopy({'model':m.state_dict(),'optimizer':o.state_dict(),
 'scheduler':s.state_dict(),'torch_rng':torch.get_rng_state(),
 'python_rng':random.getstate(),'step':5})
path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
tmp=path.with_suffix('.tmp')
torch.save(state,tmp);tmp.replace(path)
expected=[step(m,o,s) for _ in range(3)]
m2,o2,s2=setup()
# Load only this script's locally generated checkpoint.
loaded=torch.load(path,map_location='cpu',weights_only=True)
m2.load_state_dict(loaded['model']);o2.load_state_dict(loaded['optimizer'])
s2.load_state_dict(loaded['scheduler'])
torch.set_rng_state(loaded['torch_rng']);random.setstate(loaded['python_rng'])
actual=[step(m2,o2,s2) for _ in range(3)]
assert expected==actual,(expected,actual)
for x,y in zip(m.parameters(),m2.parameters()): torch.testing.assert_close(x,y,rtol=0,atol=0)
result={'scope':'deterministic CPU synthetic training, fresh model/optimizer objects',
 'resume_step':loaded['step'],'continuation_steps':3,'losses_match':True,
 'parameters_exactly_match':True,'losses':actual,'torch':torch.__version__}
path.with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
