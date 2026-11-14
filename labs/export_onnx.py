import argparse,json,time,statistics
from pathlib import Path
import numpy as np
import torch,onnx,onnxruntime as ort
from torch import nn
p=argparse.ArgumentParser()
p.add_argument('--output-dir',default='lab-results/export')
a=p.parse_args()
out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
torch.manual_seed(7);torch.set_num_threads(1)
model=nn.Sequential(nn.Linear(256,512),nn.GELU(),nn.Linear(512,64)).eval()
x=torch.randn(8,256)
with torch.inference_mode():
    expected=model(x).numpy()
    start=time.perf_counter()
    # Explicit legacy exporter keeps this fixed-shape introductory lab small.
    torch.onnx.export(model,(x,),str(out/'policy.onnx'),input_names=['features'],
        output_names=['actions'],opset_version=17,dynamo=False)
    export_ms=(time.perf_counter()-start)*1000
onnx.checker.check_model(onnx.load(out/'policy.onnx'))
options=ort.SessionOptions();options.intra_op_num_threads=1;options.inter_op_num_threads=1
start=time.perf_counter()
session=ort.InferenceSession(str(out/'policy.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
load_ms=(time.perf_counter()-start)*1000
inputs={'features':x.numpy()}
start=time.perf_counter();actual=session.run(None,inputs)[0]
first_ms=(time.perf_counter()-start)*1000
np.testing.assert_allclose(actual,expected,rtol=1e-4,atol=1e-5)
np.savez(out/'io.npz',features=inputs['features'],pytorch=expected,onnxruntime=actual)
def measure(fn):
    for _ in range(20):fn()
    values=[]
    for _ in range(50):
        start=time.perf_counter();fn();values.append((time.perf_counter()-start)*1000)
    return {'p50_ms':statistics.median(values),'p95_ms':float(np.percentile(values,95)),
      'samples_per_second':8*len(values)/(sum(values)/1000),'raw_ms':values}
with torch.inference_mode():pt=measure(lambda:model(x))
runtime=measure(lambda:session.run(None,inputs))
result={'torch':torch.__version__,'onnx':onnx.__version__,'onnxruntime':ort.__version__,
 'input_shape':[8,256],'output_shape':[8,64],'threads':1,'warmup':20,'steps':50,
 'exporter':'legacy torch.onnx.export(dynamo=False), opset 17, fixed shape',
 'correctness':'allclose passed (rtol=1e-4, atol=1e-5)',
 'max_abs_error':float(np.max(np.abs(actual-expected))),
 'export_ms':export_ms,'session_load_ms':load_ms,'first_ort_call_ms':first_ms,
 'pytorch':pt,'onnxruntime_cpu':runtime,
 'scope':'resident inputs, untrained toy MLP, no IO/queue; no speedup or policy-quality guarantee'}
(out/'report.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ['pytorch','onnxruntime_cpu']},indent=2))
print('PASS: policy.onnx, io.npz, report.json')
