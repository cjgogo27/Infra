from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def page(path,title,body,order=1):
 p=ROOT/'src/content/docs'/path
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text('---\ntitle: '+json.dumps(title,ensure_ascii=False)+'\nsidebar:\n  order: '+str(order)+'\n---\n\n'+body.strip()+'\n',encoding='utf-8')
def section(folder,n,title,scene,term,plain,body,question,answer,refs):
 page(f'{folder}/{n:02d}.md',title,
 f'预计阅读：12–18 分钟｜建议先读：本章前一节；每章首节可从阅读路线进入。\n\n## 现场问题\n\n{scene}\n\n> 带着问题读：{question}\n\n**{term}**\n\n> **一句话听懂：{plain}**\n\n{body}\n\n<details>\n<summary>自测：先回答，再展开</summary>\n\n{question}\n\n{answer}\n\n</details>\n\n## 参考资料\n\n'+ '\n\n'.join(f'{i+1}. [{label}]({url})' for i,(label,url) in enumerate(refs)),n)
