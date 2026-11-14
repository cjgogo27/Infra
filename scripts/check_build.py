
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


class LanguageParser(HTMLParser):
 def __init__(self): super().__init__(); self.options=set(); self.lang=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html': self.lang=a.get('lang')
  if tag=='option' and a.get('value','').startswith('/Infra/'): self.options.add(a['value'])
sources=Path('src/content/docs')
for source in list(sources.rglob('*.md'))+list(sources.rglob('*.mdx')):
 rel=source.relative_to(sources).with_suffix('')
 if rel.parts[0]=='en': continue
 route='' if str(rel)=='index' else rel.as_posix()+'/'
 expected={'/Infra/'+route,'/Infra/en/'+route}
 for prefix,language in [('', 'zh-CN'),('en/', 'en')]:
  htmlfile=Path('dist')/prefix/route/'index.html'
  parser=LanguageParser();parser.feed(htmlfile.read_text(encoding='utf-8'))
  assert parser.lang==language,(htmlfile,parser.lang)
  assert parser.options==expected,(htmlfile,parser.options,expected)
print('PASS: all 34 page pairs have correct language and matching switch targets')
