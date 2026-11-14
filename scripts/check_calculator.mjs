
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {transform} from 'esbuild';
const source=fs.readFileSync('src/components/Budget.astro','utf8').split('<script>')[1].split('</script>')[0];
const values={p:7,l:32,h:8,d:128,s:4096,b:1,f:40,a:2};
const inputs=Object.fromEntries(Object.entries(values).map(([k,v])=>[k,{value:String(v),checkValidity:()=>true}]));
const outputs={out:{textContent:''},speed:{textContent:''}};
let handler;
const root={
 querySelector:s=>inputs[s.slice(6,-1)]??outputs[s.slice(6,-1)],
 querySelectorAll:()=>Object.values(inputs),
 addEventListener:(_event,f)=>{handler=f;}
};
const code=(await transform(source,{loader:'ts'})).code;
vm.runInNewContext(code,{document:{querySelectorAll:()=>[root]}});
assert.match(outputs.out.textContent,/0.50 GiB/);
assert.match(outputs.speed.textContent,/1.25 倍/);
inputs.b.value='8';handler();
assert.match(outputs.out.textContent,/4.00 GiB/);
inputs.p.value='';handler();
assert.match(outputs.out.textContent,/有效数值/);
console.log('PASS: calculator defaults, changed concurrency and invalid input');
