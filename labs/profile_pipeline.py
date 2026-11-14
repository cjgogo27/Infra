import argparse,json,platform
from pathlib import Path
import torch
from torch import nn
p=argparse.ArgumentParser()
p.add_argument('--output-dir',default='lab-results/profile')
a=p.parse_args();out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
torch.manual_seed(7);torch.set_num_threads(1)
model=nn.Sequential(nn.Linear(256,512),nn.GELU(),nn.Linear(512,64)).eval()
def pipeline():
    with torch.profiler.record_function('prepare_inputs'): x=torch.randn(8,256)
    with torch.profiler.record_function('policy_forward'): y=model(x)
    with torch.profiler.record_function('postprocess'): z=y.clamp(-1,1).tolist()
    return z
with torch.inference_mode():
    for _ in range(20):pipeline()
    with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU],record_shapes=True) as prof:
        for _ in range(10):pipeline()
prof.export_chrome_trace(str(out/'pipeline.json.trace'))
names={'prepare_inputs','policy_forward','postprocess'}
rows=[{'stage':e.key,'calls':e.count,'cpu_total_us':e.cpu_time_total,
 'self_cpu_us':e.self_cpu_time_total} for e in prof.key_averages() if e.key in names]
result={'scope':'measured CPU profiler capture; inclusive stage costs, not unprofiled latency',
 'torch':torch.__version__,'platform':platform.platform(),'threads':1,'iterations':10,'stages':rows}
(out/'summary.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
