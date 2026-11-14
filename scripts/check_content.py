from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
docs=root/'src/content/docs'
files=list(docs.rglob('*.md'))+list(docs.rglob('*.mdx'))
routes={'/Infra/'}
for p in files:
    rel=p.relative_to(docs).with_suffix('').as_posix()
    routes.add('/Infra/'+(rel[:-5] if rel.endswith('index') else rel)+'/')
    if rel=='en/index': routes.add('/Infra/en/')
errors=[]
chapters=[p for p in files if re.match(r'0[1-6]-',p.relative_to(docs).as_posix())]
for p in files:
    s=p.read_text(encoding='utf-8')
    if not s.startswith('---\n'): errors.append(f'frontmatter missing: {p}')
    for link in re.findall(r'\]\((/Infra/[^)#]*)\)',s):
        if link.rstrip('/')+'/' not in routes: errors.append(f'broken route {p}: {link}')
    if p in chapters:
        for required in ['## 现场问题','一句话听懂','LabBot 落地','<details>','## 参考资料']:
            if required not in s: errors.append(f'missing {required}: {p}')
        if len(s)<900: errors.append(f'chapter too short: {p}')
assert len(chapters)==24,len(chapters)
english=[p for p in files if p.relative_to(docs).parts[0]=='en']
originals=[p for p in files if p not in english]
assert {p.relative_to(docs/'en').as_posix() for p in english}=={p.relative_to(docs).as_posix() for p in originals}, 'Missing translation'
for p in english:
    content=p.read_text(encoding='utf-8')
    if re.search(r'[\u4e00-\u9fff]',content): errors.append(f'Untranslated Chinese: {p}')
    if re.search(r'\]\(/Infra/(?!en/)',content): errors.append(f'English link exits locale: {p}')
    if re.match(r'0[1-6]-',p.relative_to(docs/'en').as_posix()):
        for required in ['## The engineering problem','In one sentence','LabBot in practice','<details>','## References']:
            if required not in content: errors.append(f'missing {required}: {p}')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(files)} pages, {len(chapters)} sections; internal links and section structure checked')
