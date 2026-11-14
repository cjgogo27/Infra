
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]/'src/content/docs'
def page(path,title,body,order=1):
 p=ROOT/'en'/path;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text('---\ntitle: '+json.dumps(title)+'\nsidebar:\n  order: '+str(order)+'\n---\n\n'+body.strip()+'\n',encoding='utf-8')
def section(folder,n,title,scene,terms,plain,body,question,answer):
 source=(ROOT/f'{folder}/{n:02d}.md').read_text(encoding='utf-8')
 refs=re.findall(r'\d+\. \[([^\]]+)\]\((https://[^)]+)\)',source)
 references='\n\n'.join(f'{i+1}. [Reference {i+1}: {url.split("/")[2]}]({url})' for i,(_,url) in enumerate(refs))
 page(f'{folder}/{n:02d}.md',title,
 f'Estimated reading: 12–18 minutes. Suggested prerequisite: the previous section in this chapter; use a reading guide to enter a new chapter.\n\n## The engineering problem\n\n{scene}\n\n> Keep this question in mind: {question}\n\n**{terms}**\n\n> **In one sentence: {plain}**\n\n{body}\n\n<details>\n<summary>Self-check: answer before expanding</summary>\n\n{question}\n\n{answer}\n\n</details>\n\n## References\n\n'+references,n)
