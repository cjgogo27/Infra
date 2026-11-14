import argparse, json, platform, time, statistics
from pathlib import Path
import torch
from torch import nn
p=argparse.ArgumentParser()
p.add_argument('--device',choices=['cpu','cuda'],default='cpu')
p.add_argument('--batch',type=int,default=8)
p.add_argument('--steps',type=int,default=100)
p.add_argument('--warmup',type=int,default=20)
p.add_argument('--threads',type=int,default=None)
p.add_argument('--compile',action='store_true')
p.add_argument('--trace',action='store_true')
p.add_argument('--output',default='lab-results/benchmark.json')
a=p.parse_args()
if a.batch<1 or a.steps<2 or a.warmup<0: p.error('invalid batch/steps/warmup')
if a.device=='cuda' and not torch.cuda.is_available(): p.error('CUDA unavailable')
if a.threads is not None:
    if a.threads < 1: p.error('threads must be positive')
    torch.set_num_threads(a.threads)
torch.manual_seed(7)
d=torch.device(a.device)
model=nn.Sequential(nn.Linear(256,512),nn.GELU(),nn.Linear(512,64)).to(d).eval()
x=torch.randn(a.batch,256,device=d)
candidate=torch.compile(model) if a.compile else model
def sync():
    if d.type=='cuda': torch.cuda.synchronize()
with torch.inference_mode():
    ref=model(x)
    got=candidate(x)
    torch.testing.assert_close(got,ref,rtol=1e-4,atol=1e-5)
    for _ in range(a.warmup): candidate(x)
    sync()
    if d.type=='cuda': torch.cuda.reset_peak_memory_stats()
    ms=[]
    for _ in range(a.steps):
        sync()
        start=time.perf_counter()
        candidate(x)
        sync()
        ms.append((time.perf_counter()-start)*1000)
    # Snapshot before profiling: the benchmark window must end here.
    peak_allocated = torch.cuda.max_memory_allocated() if d.type=='cuda' else None
    if a.trace:
        activities=[torch.profiler.ProfilerActivity.CPU]
        if d.type=='cuda': activities.append(torch.profiler.ProfilerActivity.CUDA)
        with torch.profiler.profile(activities=activities,record_shapes=True) as prof:
            for _ in range(5):
                with torch.profiler.record_function('toy_policy'): candidate(x)
            sync()
        Path(a.output).parent.mkdir(parents=True,exist_ok=True)
        prof.export_chrome_trace(str(Path(a.output).with_suffix('.json.trace')))
ordered=sorted(ms)
idx=.95*(len(ms)-1)
lo=int(idx); hi=min(lo+1,len(ms)-1)
p95=ordered[lo]+(ordered[hi]-ordered[lo])*(idx-lo)
result={
 'scope':'synthetic MLP inference, resident inputs, per-call synchronized wall time',
 'torch':torch.__version__,'python':platform.python_version(),'platform':platform.platform(),
 'device':a.device,'device_name':torch.cuda.get_device_name() if d.type=='cuda' else platform.processor(),
 'cuda_runtime':torch.version.cuda,'threads':torch.get_num_threads(),
 'batch':a.batch,'steps':a.steps,'warmup':a.warmup,'compiled':a.compile,
 'correctness':'assert_close passed','p50_ms':statistics.median(ms),'p95_ms':p95,
 'samples_per_second':a.batch*len(ms)/(sum(ms)/1000),
 'peak_allocated_bytes':peak_allocated,
 'raw_ms':ms}
Path(a.output).parent.mkdir(parents=True,exist_ok=True)
Path(a.output).write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='raw_ms'},indent=2))
