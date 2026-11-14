
from pathlib import Path
from html.parser import HTMLParser
class Parser(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src') and v and v.startswith('/Infra/'):
    self.links.append(v.split('#')[0].split('?')[0])
bad=[]
for p in Path('dist').rglob('*.html'):
 parser=Parser();parser.feed(p.read_text(encoding='utf-8'))
 for url in parser.links:
  target=Path('dist')/url.removeprefix('/Infra/')
  if not target.is_file() and not (target/'index.html').is_file():bad.append((str(p),url))
assert not bad,bad[:10]
html=Path('dist/appendix/calculator/index.html').read_text(encoding='utf-8')
assert 'BF16 权重' in html and 'addEventListener' in html
print('PASS: rendered HTML internal links/assets and calculator runtime')
