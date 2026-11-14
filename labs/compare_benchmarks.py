import json,sys
from pathlib import Path
if len(sys.argv)!=3:raise SystemExit('Usage: python labs/compare_benchmarks.py baseline.json candidate.json')
a,b=[json.loads(Path(p).read_text()) for p in sys.argv[1:]]
for key in ['device','device_name','platform','cuda_runtime','threads','compiled','torch','scope','steps','warmup']:
    if a[key]!=b[key]:raise SystemExit(f'Comparison condition differs: {key}')
rows=[]
for r in [a,b]:
    elapsed=sum(r['raw_ms'])
    rows.append({'batch':r['batch'],'mean_batch_ms':elapsed/len(r['raw_ms']),
      'amortized_ms_per_sample':elapsed/(len(r['raw_ms'])*r['batch']),
      'samples_per_second':r['batch']*len(r['raw_ms'])/(elapsed/1000),
      'p50_ms':r['p50_ms'],'p95_ms':r['p95_ms']})
print(json.dumps({'results':rows,'throughput_ratio':rows[1]['samples_per_second']/rows[0]['samples_per_second'],
 'interpretation':'amortized sample time is not request latency; two runs do not establish significance'},indent=2))
