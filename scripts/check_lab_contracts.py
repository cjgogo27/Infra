import ast
from pathlib import Path
tree=ast.parse(Path('labs/benchmark.py').read_text(encoding='utf-8'))
peaks=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='max_memory_allocated']
profiles=[n for n in ast.walk(tree) if isinstance(n,ast.If) and isinstance(n.test,ast.Attribute) and n.test.attr=='trace']
assert len(peaks)==1 and len(profiles)==1
assert peaks[0].lineno < profiles[0].lineno, 'Peak sampling must precede profiler'
results=[n for n in ast.walk(tree) if isinstance(n,ast.Dict)]
assert any(isinstance(k,ast.Constant) and k.value=='peak_allocated_bytes' and isinstance(v,ast.Name) and v.id=='peak_allocated' for d in results for k,v in zip(d.keys,d.values)), 'Report must use the frozen snapshot'
for file in Path('labs').glob('*.py'): ast.parse(file.read_text(encoding='utf-8'))
print('PASS: benchmark memory snapshot precedes optional profiling; lab syntax checked (no GPU execution)')
