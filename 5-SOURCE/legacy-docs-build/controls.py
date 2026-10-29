from pathlib import Path
import re
r=Path('/Users/macbook/Documents/Codex/2026-10-26/wh');b=r/'outputs/Client-Studio-v2'
arrow='<svg class="action-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
icons={
'book':'M5 4h11a3 3 0 0 1 3 3v13H7a3 3 0 0 1-3-3V6a2 2 0 0 1 1-2Zm2 0v13m0 0h12M10 8h6M10 11h4',
'folder':'M4 5h6l2 3h8v12H4V5Zm0 6h16M8 15h8M8 17h5',
'grid':'M4 3h16v18H4V3Zm0 5h16M4 13h16M4 17h16M10 8v13'}
extra='''
.action-arrow{width:18px;height:18px;display:inline-block;vertical-align:middle;flex-shrink:0}
.resource .icon{background:transparent;border-radius:0;width:24px;height:28px;color:#665185}
.resource .icon svg{width:24px;height:24px;stroke-width:1.7}
.resource .resource-top{gap:11px}.resource .link{border-top:1px solid #ebe6f0;padding:14px 0 0;font-weight:600;font-size:11px;color:#3e314f}
.resource .link .action-arrow{width:33px;height:33px;padding:8px;background:#eee8f6;border:1px solid #e1d7ef;border-radius:50%;transition:background .18s,transform .18s}
.resource:hover .link .action-arrow{background:#ddd1ee;transform:translateX(2px)}
.primary .action-arrow{width:18px;height:18px}.head-link .action-arrow,.nav-open .action-arrow{width:14px;height:14px;margin-left:7px}.secondary .action-arrow{width:15px;height:15px;margin-left:7px}
@media(max-width:650px){.resource .icon{display:none}.resource .link{font-size:10px}.resource .link .action-arrow{width:29px;height:29px;padding:7px}}
'''
for rel in ['START-HERE.html','Studio.html','Documents/Editable-Documents.html']:
 p=b/rel;t=p.read_text()
 t=t.replace('↗',arrow).replace('→',arrow)
 if rel=='START-HERE.html':
  t=t.replace('</style>',extra+'</style>')
  # Replace arbitrary folder/book/grid symbols with the same drawn icon family.
  t=t.replace('🗂️','').replace('▦','')
  t=re.sub(r'<span class="link">(.*?)<svg(.*?)</svg></span>',lambda m:'<span class="link">'+m[1]+'<svg'+m[2]+'</svg></span>',t)
  t=t.replace('<title>Welcome to your Client Studio · Brief to Approved</title>','<title>Client Studio · Refined Edition 02.2</title>')
  t=t.replace('THE CLIENT STUDIO / EDITION 02','THE CLIENT STUDIO / EDITION 02.2').replace('Client Studio Edition 02</span>','Client Studio Edition 02.2</span>')
 if rel=='Studio.html':t=t.replace('</head>','<style>'+extra+'</style></head>')
 p.write_text(t)
p=b/'assets/studio.js';t=p.read_text().replace('↗',arrow)
# Only remove decorative emoji in HTML, preserving data strings and text labels.
for old,new in [('📖','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="'+icons['book']+'"/></svg>'),('🗂️','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="'+icons['folder']+'"/></svg>'),('🧩','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="'+icons['grid']+'"/></svg>')]:
 # Avoid quotes inside single-quoted JS string literals by using a template literal.
 t=t.replace("'"+old+"'",'`'+new+'`')
p.write_text(t)
p=b/'assets/studio.css';p.write_text(p.read_text()+'\n.guide-card .emoji svg{width:30px;height:30px;color:#6550a6}.quiet .action-arrow{width:14px;height:14px}.secondary .action-arrow{width:14px;height:14px}\n')
final=(b/'START-HERE.html').read_text()
for path,prefix in [(r/'outputs/Brief-to-Approved/START-HERE.html','../Client-Studio-v2/'),(r/'work/brief-kit/v2/Etsy-START-HERE.html','Client-Studio-v2/')]:
 path.write_text(re.sub(r'(href|src)="(?!#|https?:)([^"]+)"',lambda m:m[1]+'="'+prefix+m[2]+'"',final))
(b/'Source/controls.py').write_text(Path(__file__).read_text())
print('Refined controls applied to welcome, workspace and editable documents; entry pages synchronized.')
