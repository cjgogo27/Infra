import argparse,copy,json,math
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--output',default='lab-results/replay.json')
a=p.parse_args()
sample={'schema_version':1,'clock':'monotonic_ms_same_process','observation_ms':1000,
 'now_ms':1040,'deadline_ms':100,'image':{'shape':[1,3,32,32],'dtype':'uint8','channels':'RGB'},
 'state':{'joint_order':['j1','j2','j3','j4','j5','j6'],'unit':'rad','values':[0.0]*6},
 'action':{'shape':[4,6],'unit':'rad','mode':'absolute','chunk_start_ms':1040,
 'step_ms':20,'values':[[0.01*i]*6 for i in range(4)]}}
def validate(s):
    if s['schema_version']!=1 or s['clock']!='monotonic_ms_same_process':raise ValueError('schema/clock mismatch')
    if s['image']!={'shape':[1,3,32,32],'dtype':'uint8','channels':'RGB'}:raise ValueError('image contract mismatch')
    state=s['state'];action=s['action']
    if state['unit']!='rad' or action['unit']!='rad':raise ValueError('wrong_unit: radians required')
    if state['joint_order']!=['j1','j2','j3','j4','j5','j6']:raise ValueError('joint order mismatch')
    if len(state['values'])!=6 or action['shape']!=[4,6] or len(action['values'])!=4 or any(len(r)!=6 for r in action['values']):raise ValueError('wrong_shape: expected state[6], action[4,6]')
    if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in state['values']+[x for row in action['values'] for x in row]):raise ValueError('non-finite values')
    if action['mode']!='absolute' or action['step_ms']!=20:raise ValueError('action semantics mismatch')
    age=s['now_ms']-s['observation_ms']
    if not 0<=age<=s['deadline_ms'] or action['chunk_start_ms']<s['now_ms']:raise ValueError('stale: expired observation or chunk')
    return age
cases={'valid':sample}
for name in ['wrong_unit','wrong_shape','stale']:cases[name]=copy.deepcopy(sample)
cases['wrong_unit']['action']['unit']='deg'
cases['wrong_shape']['action']['values'][0]=[0.0]*5
cases['stale']['now_ms']=1200
rows=[]
for name,s in cases.items():
    try:
        age=validate(s);row={'case':name,'accepted':True,'observation_age_ms':age}
    except ValueError as e:row={'case':name,'accepted':False,'reason':str(e)}
    assert row['accepted']==(name=='valid')
    rows.append(row)
result={'scope':'synthetic metadata and actions only; no robot connection or policy evaluation',
 'sample':sample,'synthetic_timeline_ms':{'exposure':1000,'decode_done':1005,
 'align_done':1007,'preprocess_done':1010,'policy_done':1035,'dispatch':1040},
 'cases':rows}
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
