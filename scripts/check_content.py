from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
docs=root/'src/content/docs'
files=list(docs.rglob('*.md'))+list(docs.rglob('*.mdx'))
routes={'/Infra/'}
for p in files:
    rel=p.relative_to(docs).with_suffix('').as_posix()
    routes.add('/Infra/'+rel+'/')
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
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(files)} pages, {len(chapters)} sections; internal links and section structure checked')
