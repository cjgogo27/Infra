import argparse,json,statistics,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--batch',type=int,default=1)
p.add_argument('--runs',type=int,default=3)
p.add_argument('--threads',type=int,default=1)
p.add_argument('--device',choices=['cpu','cuda'],default='cpu')
p.add_argument('--output-dir',default='lab-results/repeats')
a=p.parse_args()
if min(a.batch,a.runs,a.threads)<1:p.error('all counts must be positive')
out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
rows=[]
for i in range(a.runs):
    path=out/f'run-{i+1}.json'
    subprocess.run([sys.executable,str(Path(__file__).with_name('benchmark.py')),
        '--device',a.device,'--batch',str(a.batch),'--threads',str(a.threads),
        '--output',str(path)],check=True,stdout=subprocess.DEVNULL)
    rows.append(json.loads(path.read_text()))
rates=[r['samples_per_second'] for r in rows]
result={'scope':'independent subprocess runs; within-run p95 is not between-run uncertainty',
 'batch':a.batch,'device':a.device,'threads':a.threads,'runs':a.runs,
 'throughput_median':statistics.median(rates),'throughput_min':min(rates),
 'throughput_max':max(rates),'per_run':[{'p50_ms':r['p50_ms'],'p95_ms':r['p95_ms'],
 'samples_per_second':r['samples_per_second']} for r in rows]}
(out/'summary.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
