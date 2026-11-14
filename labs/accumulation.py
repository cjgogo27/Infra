import copy, json
from pathlib import Path
import torch
from torch import nn
torch.manual_seed(13)
torch.set_num_threads(1)
base=nn.Linear(3,1).double()
x=torch.randn(8,3,dtype=torch.float64)
y=torch.randn(8,1,dtype=torch.float64)
def gradient(chunks,wrong=False):
    model=copy.deepcopy(base)
    for indices in chunks:
        losses=(model(x[indices])-y[indices]).square()
        # Global valid-token mean; padding is represented by absent indices.
        loss=losses.mean()/len(chunks) if wrong else losses.sum()/sum(len(c) for c in chunks)
        loss.backward()
    return torch.cat([p.grad.flatten() for p in model.parameters()])
full=gradient([list(range(8))])
weighted=gradient([list(range(2)),list(range(2,8))])
wrong=gradient([list(range(2)),list(range(2,8))],wrong=True)
# Planned accumulation=4, but final window contains only 2 microbatches / 3 tokens.
tail_ref=gradient([[0,1,2]])
tail=gradient([[0],[1,2]])
torch.testing.assert_close(full,weighted,rtol=1e-12,atol=1e-12)
torch.testing.assert_close(tail_ref,tail,rtol=1e-12,atol=1e-12)
assert not torch.allclose(full,wrong,rtol=1e-6,atol=1e-6)
result={'full_vs_weighted_max_error':(full-weighted).abs().max().item(),
 'wrong_mean_max_error':(full-wrong).abs().max().item(),
 'tail_window_max_error':(tail_ref-tail).abs().max().item(),
 'dtype':'float64','scope':'CPU, one output per valid token, no AMP or DDP'}
Path('lab-results').mkdir(exist_ok=True)
Path('lab-results/accumulation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
