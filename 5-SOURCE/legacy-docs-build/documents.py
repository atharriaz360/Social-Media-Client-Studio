from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from xml.sax.saxutils import escape
import json, shutil, html

ROOT=Path('/Users/macbook/Documents/Codex/2026-10-26/wh'); OUT=ROOT/'outputs/Client-Studio-v2'; AS=OUT/'assets'
F=Path('/System/Library/Fonts/Supplemental')
for n,f in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf'),('Display','Georgia.ttf'),('Italic','Georgia Italic.ttf')]: pdfmetrics.registerFont(TTFont(n,str(F/f)))
INK='#252332'; PURPLE='#6550A6'; LAV='#EBE5FA'; PAPER='#F7F6F2'; MUTED='#706C7B'; LINE='#E4DFE9'; YELLOW='#F7EC9D'; GREEN='#E4EFDF'
W,H=595.28,841.89
def fill(c,color):c.setFillColor(HexColor(color))
def box(c,x,y,w,h,color,r=12):fill(c,color);c.roundRect(x,y,w,h,r,fill=1,stroke=0)
def txt(c,s,x,y,size=11,font='Body',color=INK):fill(c,color);c.setFont(font,size);c.drawString(x,y,s)
def para(c,s,x,y,w,size=10.5,leading=16,color=INK,font='Body'):
 p=Paragraph(escape(s).replace('\n','<br/>'),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=HexColor(color)))
 _,h=p.wrap(w,800);assert y-h>45,('overflow',s[:50],y,h);p.drawOn(c,x,y-h);return y-h
def base(c,num,label,total=14):
 fill(c,PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
 box(c,35,H-53,27,27,LAV,8);txt(c,'b',42,H-46,23,'Display',PURPLE)
 txt(c,'BRIEF TO APPROVED',73,H-38,8,'Bold');txt(c,label.upper(),W-210,H-38,8,'Body',MUTED)
 c.setStrokeColor(HexColor(LINE));c.line(35,45,W-35,45);txt(c,'CLIENT STUDIO / EDITION 02',35,28,7,'Bold',MUTED);txt(c,f'{num:02d} / {total:02d}',W-75,28,8,'Body',MUTED)
def title(c,kicker,title,sub):
 txt(c,kicker,35,744,9,'Bold',PURPLE)
 y=714
 for line in title.split('\n'):txt(c,line,35,y,31,'Display');y-=37
 return para(c,sub,35,y-1,510,11,17,MUTED)-25
def check(c,x,y,label,color=PURPLE):
 box(c,x,y-2,15,15,LAV,4);c.setStrokeColor(HexColor(color));c.setLineWidth(1.3);c.lines([(x+4,y+5,x+7,y+2),(x+7,y+2,x+12,y+10)]);txt(c,label,x+24,y+1,9,'Body')
def smallcard(c,x,y,w,h,kicker,heading,body,bg='#FFFFFF'):
 box(c,x,y-h,w,h,bg);txt(c,kicker,x+17,y-24,8,'Bold',PURPLE)
 yy=para(c,heading,x+17,y-40,w-34,17,21,INK,'Display')
 return para(c,body,x+17,yy-12,w-34,10,15,MUTED)
def workflow(c,y,labels):
 w=(525-12*(len(labels)-1))/len(labels)
 for i,l in enumerate(labels):
  x=35+i*(w+12);box(c,x,y-70,w,70,LAV if i%2==0 else '#FFFFFF',10);txt(c,f'0{i+1}',x+12,y-20,8,'Bold',PURPLE);para(c,l,x+12,y-31,w-24,11,14,INK,'Bold')
def mini_board(c,x,y,w):
 for i,(label,color) in enumerate([('DRAFT',LAV),('REVIEW',YELLOW),('APPROVED',GREEN)]):
  xx=x+i*(w/3+5);box(c,xx,y-150,w/3-7,150,'#FFFFFF',9);txt(c,label,xx+10,y-17,7,'Bold',MUTED);box(c,xx+9,y-94,w/3-25,62,color,6);txt(c,['An idea','A clear check','A lovely yes'][i],xx+16,y-67,8,'Bold');box(c,xx+9,y-125,w/3-25,18,PAPER,4)

chapters=[
('01 / THE STUDIO','A calmer place\nto do good work.','A practical local workspace for the journey from brief to approved content.',
 [('One home for the moving parts','Use Overview to see the work, Content board to edit it, Approvals to record decisions and Reports to review the results. The client brief gives every post a shared starting point.'),('Your first five minutes','Open Studio.html in a desktop browser. Start with the fictional Juniper example. Edit P001, complete its fact check, then record a practice approval. Change the caption again and see the approval clear.')],
 'Know what this is','A local browser workspace. It does not send approval requests, authenticate clients, sync accounts or publish posts. Keep those actions in your existing tools.','board'),
('02 / CLIENT CLARITY','Before the caption,\nask the useful question.','A clear brief gives the creative work something solid to stand on.',
 [('Ask for the essentials','Confirm the offer, audience, goal, voice, call to action, approver, timezone and usable assets. Record facts and restrictions in Client brief. Leave unknown information open and ask the client.'),('Choose a useful goal','For Juniper Cafe, the goal is to explain the weekday lunch offer to local office workers. Likes alone do not establish cafe visits. Ask what the client can measure before promising a result.')],
 'Try this question','What should someone understand or do after seeing this post? Ask for one answer, then use it to choose the content role.','facts'),
('03 / THE CONTENT PLAN','Give each idea\na little purpose.','Build a manageable plan around assets the client can actually provide.',
 [('Explain. Show. Invite.','Explain answers a useful question. Show demonstrates a real product or process. Invite gives one clear next step. Choose the mix around the goal; do not assume one ratio works for every client.'),('Keep the record together','Create a content card with a title, channel, planned date, role, caption and asset reference. A unique ID and version travel with that record. Calendar shows the dates without sending reminders.')],
 'Make it achievable','Start with three posts and available assets. A small plan you can deliver beats a full calendar built on missing photos and unconfirmed offers.','board'),
('04 / THE DRAFT','Make it sound\nlike them.','A strong caption is specific, clear and rooted in confirmed facts.',
 [('Use a voice cue','Write a few practical rules: warm, understated, short sentences, one action. Use approved writing samples when you have permission. Avoid generic hype that could belong to any business.'),('Edit for a single action','Ask the reader to do one thing: view the menu, save the tip or contact the business. Verify prices, hours, offer conditions and destinations. Do not invent testimonials, availability or performance claims.')],
 'The Juniper example','Instead of “the city’s best lunch, guaranteed in five minutes,” use “Ask us about today’s soup, served 12-3. Find the current menu at the counter.”','before'),
('05 / THE REVIEW','A beautiful draft\nstill needs a check.','Separate factual review, asset permission and client approval.',
 [('Facts checked','Compare every material claim with the client brief or a reliable confirmation. Open the destination link. Choose Facts checked only after doing the review, not because the copy sounds plausible.'),('Asset rights checked','Open the final asset and confirm it can be used for this client and channel. Check permission for people, brands and third-party material where relevant. A file in a shared folder is not automatically licensed.')],
 'Two checks. Then approval.','The workspace keeps the record at Review checks until both checkboxes are complete. These are self-recorded checks, not independent certification.','check'),
('06 / THE FINAL YES','Approval belongs\nto a version.','Keep the exact content and the decision attached to one another.',
 [('Ask outside the workspace','Send the content ID, version, caption, final asset and proposed date through your agreed client channel. Ask the named approver for Approved or Changes requested. Silence is not a recorded approval.'),('Record the real decision','In Approvals, enter the person, evidence reference and decision. The workspace stores the approved version. If you change the title, caption, channel, date, role, cover or asset, it increases the version and clears approval.')],
 'The important distinction','Recording a name is not identity verification. This local workspace stores an approval you received elsewhere; it does not replace an authenticated client portal.','version'),
('07 / FEEDBACK','Less guessing.\nBetter revisions.','Turn broad feedback into a clear decision and a bounded next step.',
 [('Make vague feedback concrete','If the client says “more premium,” ask which change they mean. Offer two directions: shorter copy with a close-up, or a warmer explanation of the service. Avoid endless rewrites around an undefined adjective.'),('Keep new scope visible','Separate corrections, voice changes and new work. If a request adds a campaign or channel, refer to your actual agreement. Confirm the added work, fee and date before starting it. This kit does not supply a legal contract.')],
 'A useful message','For this post, do you prefer a shorter product-led version or a warmer story-led version? I will revise once you confirm and send the new version for approval.','note'),
('08 / THE HANDOFF','Ready here.\nScheduled there.','Use the approved record to prepare a careful manual publishing handoff.',
 [('Check the final preview','Open the approved asset and copy. In your scheduler verify the account, date, timezone, crop, links, tags, subtitles and accessibility text. If the content changes materially, request approval again.'),('Record the live item','Choose Scheduled only after your scheduler confirms it. Once published, check the live item and add its URL. Choosing Published without an HTTP or HTTPS URL keeps the action at Add published URL.')],
 'No surprise automation','The app tracks your production stage. It does not connect to social accounts, send content, schedule posts, upload assets or verify that a URL is live.','workflow'),
('09 / THE REPORT','Good reports\nmake the next step clear.','Keep numbers honest, comparable and connected to a decision.',
 [('Match the source and period','Enter one post-level row for the reporting period. Record the platform source and extraction date. Use zero for a measured zero and leave unavailable figures blank. Do not mix plays, impressions and reach as if they were identical.'),('Know what the rate means','Interactions = likes + comments + saves + shares, only when all four are supplied. Interaction rate by reach = interactions / reach. A missing input or zero reach leaves the rate unavailable.')],
 'One sample calculation','Reach 800; likes 26; comments 4; saves 12; shares 6. Interactions = 48. Interaction rate by reach = 6.0%. These are fictional training figures.','chart'),
('10 / THE NEXT CYCLE','One observation.\nOne experiment.','A small, useful learning loop is better than an overconfident story.',
 [('Describe before interpreting','State what the data shows, then separate your interpretation. More saves on one post does not prove why people saved it. Summed reach across posts is not a count of unique people.'),('Agree one test','Choose a question, a comparable set of posts and a measure before starting. For Juniper, try another useful menu explainer and compare saves across similar posts. Small organic samples are noisy.')],
 'A client-ready update','The soup explainer received 12 saves in this sample. Next cycle, test another practical lunch explainer. Please confirm next week’s soup and send a current counter photo.','chart'),
('11 / YOUR WORK, SAFE','A little backup.\nA lot less worry.','Local storage is convenient. A downloaded backup gives you control.',
 [('Export after each session','The app saves in this browser when local storage is available. Browser settings, clearing data or moving files may affect access. Export JSON to keep the complete workspace. CSV exports the content plan only.'),('Import with care','Settings lets you restore a valid Studio v2 backup up to 5 MB and 500 posts. Import replaces the current workspace after confirmation. Backups can contain client information, so store and share them carefully.')],
 'A quick restore test','Export your fictional demo, create an empty workspace and import the backup. Check the client name, captions, approval versions and result figures. Practice before relying on the process for real work.','backup'),
('12 / YOUR FIRST CYCLE','Small checks.\nA strong finish.','Use this final pass at the point of work.',
 [('Before the final yes','Confirm the brief, date and timezone. Check facts and rights. Send the exact caption and asset with ID and version. Record the approver, evidence and matching version.'),('Before the report','Verify the live post and URL. Collect comparable figures. Keep missing data blank. Check one row by hand. State limits and agree one next experiment. Export the final workspace backup.')],
 'Leave the desk ready','Export a backup after the final changes. Keep the approved assets, client decisions and report in the client archive. Start the next cycle from a clear brief.','check')]

c=canvas.Canvas(str(OUT/'Documents/Visual-Field-Guide.pdf'),pagesize=(W,H));c.setTitle('Brief to Approved | Visual Field Guide');c.setAuthor('Brief to Approved / Studio Edition')
fill(c,INK);c.rect(0,0,W,H,fill=1,stroke=0)
txt(c,'THE CLIENT STUDIO COLLECTION',40,785,9,'Bold','#C3B5E0')
txt(c,'Good work.',40,695,57,'Display','#F8F5EF');txt(c,'A clear path.',40,627,57,'Italic','#D6C8EF')
para(c,'From client brief to approved content. A thoughtful companion for freelance social media managers.',43,580,330,13,20,'#D8D3E0')
box(c,35,170,525,330,LAV,22);c.drawImage(str(AS/'studio-art.png'),95,170,width=410,height=287,mask='auto')
txt(c,'THE VISUAL FIELD GUIDE',55,465,9,'Bold',PURPLE)
txt(c,'brief to approved.',40,103,22,'Display','#F7F6F2');txt(c,'EDITION 02 / 2026',40,68,8,'Bold','#B7ABCB');txt(c,'01 / 14',510,68,8,'Body','#B7ABCB');c.showPage()
base(c,2,'Your route through the studio');y=title(c,'A LITTLE ORIENTATION','Open it. Make it yours.','Start with the fictional example, then move to your own client work.')
workflow(c,y,['Client brief','Content plan','Review','Approval','Results']);y-=104
smallcard(c,35,y,250,160,'01 / THE WORKSPACE','Your creative desk.','Open Studio.html. The main navigation leads to focused views rather than one long spreadsheet.',LAV)
smallcard(c,305,y,255,160,'02 / THE DOCUMENTS','A client-ready collection.','Six editable document layouts: welcome, intake, strategy, content review, results and handoff.','#FFFFFF')
y-=185
txt(c,'Find the right page',35,y,17,'Display');y-=30
for idx,label in [(3,'The studio and first practice loop'),(4,'Brief, audience and client goal'),(5,'Plan the content'),(6,'Draft in the client voice'),(7,'Review facts and asset rights'),(8,'Record version-aware approval'),(9,'Handle feedback'),(10,'Schedule and publish manually'),(11,'Read the results'),(12,'Choose the next experiment'),(13,'Export and restore backups'),(14,'Final cycle checklist')]:
 txt(c,label,40,y,9,'Body',MUTED);txt(c,f'{idx:02d}',530,y,9,'Bold',PURPLE);y-=20
c.showPage()
for n,(kicker,head,sub,sections,notehead,notebody,art) in enumerate(chapters,3):
 base(c,n,'Field guide');y=title(c,kicker,head,sub)
 # Visual explanation strip varies with the task.
 if art=='board':mini_board(c,35,y,515)
 elif art=='version':
  smallcard(c,35,y,250,140,'VERSION 02','Approved','The named approver and evidence apply to this exact version.',GREEN)
  smallcard(c,305,y,255,140,'VERSION 03','Approval resets','An edited caption needs a fresh decision.',LAV)
 elif art=='chart':
  box(c,35,y-145,525,145,'#FFFFFF');txt(c,'A SMALL SAMPLE, CLEARLY LABELLED',55,y-25,8,'Bold',PURPLE)
  for j,(label,v) in enumerate([('Likes',26),('Comments',4),('Saves',12),('Shares',6)]):
   yy=y-52-j*22;txt(c,label,55,yy,9,'Body',MUTED);box(c,145,yy-2,300*(v/30),9,LAV,4);txt(c,str(v),470,yy,9,'Bold')
 elif art=='before':
  smallcard(c,35,y,250,145,'BEFORE','A claim without support','“The city’s best lunch, guaranteed in five minutes.”','#F5DED4')
  smallcard(c,305,y,255,145,'AFTER','A fact you can confirm','“Ask us about today’s soup, served 12-3.”',GREEN)
 elif art=='check':
  box(c,35,y-145,525,145,'#FFFFFF');txt(c,'THE SMALL THINGS THAT MATTER',55,y-27,9,'Bold',PURPLE)
  for j,l in enumerate(['Confirmed facts match the final copy','The final asset can be used','Approval is for the current version','The handoff is complete and recorded']):check(c,55,y-56-j*23,l)
 elif art=='facts':
  smallcard(c,35,y,250,145,'THE CLIENT SAYS','“We need more posts.”','A request for output. Ask which result the content should support.',LAV)
  smallcard(c,305,y,255,145,'A CLEARER BRIEF','“Explain weekday lunch.”','A defined audience, confirmed offer and useful direction.',YELLOW)
 elif art=='backup':
  workflow(c,y,['Export JSON','Store safely','Import copy','Check data']);
 elif art=='workflow':workflow(c,y,['Approved','Preview','Schedule','Verify URL'])
 else:
  box(c,35,y-145,525,145,LAV);txt(c,'A LITTLE MORE CLARITY',55,y-30,9,'Bold',PURPLE);para(c,'One specific question can save an entire round of guessing.',55,y-50,285,23,29,INK,'Display');c.drawImage(str(AS/'studio-art.png'),360,y-145,width=190,height=133,mask='auto')
 y-=185
 for i,(a,b) in enumerate(sections):
  xx=35+i*270;txt(c,f'0{i+1}',xx,y,9,'Bold',PURPLE);yy=para(c,a,xx,y-20,250,19,24,INK,'Display');para(c,b,xx,yy-15,245,11,17,MUTED)
 box(c,35,82,525,118,YELLOW if n%2==0 else LAV);txt(c,notehead,54,174,12,'Bold');para(c,notebody,54,155,485,10,15,INK)
 c.showPage()
c.save()

templates=[
 dict(kicker='01 / WELCOME PACKET',title='Good things start\nwith a clear hello.',intro='A warm welcome to your next content chapter.',fields=[('Your studio','[Your studio name and contact]'),('What we are making','[Agreed channels, content deliverables and reporting period]'),('How we will work together','[Where feedback happens, who approves and the agreed review window]'),('What we need to begin','[Brand materials, usable assets, confirmed offer and access arrangements]')],note='For [client name] / Prepared by [your name]'),
 dict(kicker='02 / CLIENT BRIEF',title='Tell us what\nmakes you, you.',intro='A few thoughtful answers make the creative work more focused.',fields=[('The offer and audience','[What do you sell, and who is the priority audience?]'),('The goal','[What should this content help people understand or do?]'),('The voice and facts','[Approved examples, confirmed claims and words to avoid]'),('The final yes','[Named approver, timezone, review dates and asset permissions]')],note='Confirm the completed brief with the client before drafting.'),
 dict(kicker='03 / STRATEGY SNAPSHOT',title='A little direction.\nA stronger story.',intro='One page to keep the content pointed at a useful goal.',fields=[('Our focus','[Audience, business goal and reporting period]'),('Our three content roles','[Explain: a helpful answer / Show: a real process / Invite: one next step]'),('What success will look like','[Available measure, source and realistic interpretation]'),('What we will test','[One content question, a comparison and a review date]')],note='Use confirmed facts. Keep assumptions visible.'),
 dict(kicker='04 / CONTENT REVIEW',title='One current version.\nOne lovely yes.',intro='Keep the review specific and the record easy to follow.',fields=[('The content','[ID, version, channel, planned date and timezone]'),('Caption and final asset','[Exact copy and accessible asset reference]'),('The review checks','[Facts checked / Asset rights checked / Links and preview checked]'),('The decision','[Approved or Changes requested / Name / Date / Evidence reference]')],note='Approval applies only to this exact version. Request a new decision after edits.'),
 dict(kicker='05 / MONTHLY REPORT',title='Here is what\nwe learned.',intro='Clear figures, honest context and a useful next step.',fields=[('The context','[Client, goal, reporting period, platforms and data extraction date]'),('What happened','[Published work and comparable measures, with missing data noted]'),('What it may mean','[Interpretations separated from facts; avoid unsupported causal claims]'),('The next good experiment','[One test, the measure, the date and the client input needed]')],note='Post-level reach is not additive unique audience. Sample numbers must be labelled.'),
 dict(kicker='06 / PROJECT HANDOFF',title='A thoughtful finish.\nA clear next step.',intro='Leave the work and the client in good hands.',fields=[('The delivered work','[Final approved assets, copy, IDs and live links]'),('Where everything lives','[Client folder, report, workspace backup and owner]'),('What remains open','[Pending decisions, unfinished deliverables and agreed next actions]'),('The final handover','[Access changes, retention arrangements and acknowledgement]')],note='Share only the intended client files. Keep private notes and other clients separate.')]
c=canvas.Canvas(str(OUT/'Documents/Client-Documents.pdf'),pagesize=(W,H));c.setTitle('Brief to Approved | Client Document Collection')
for i,p in enumerate(templates,1):
 base(c,i,'Editable client collection',6);y=title(c,p['kicker'],p['title'],p['intro'])
 c.drawImage(str(AS/(['coffee','soup','menu'][i%3]+'.png')),365,690,width=195,height=136,preserveAspectRatio=True,mask='auto') if False else None
 for j,(head,body) in enumerate(p['fields']):
  yy=y-j*108;box(c,35,yy-94,525,94,LAV if j==0 else '#FFFFFF');txt(c,f'0{j+1}',53,yy-24,9,'Bold',PURPLE);txt(c,head,84,yy-24,12,'Bold');para(c,body,84,yy-39,450,11,16,MUTED)
 txt(c,'MAKE THIS YOURS',35,110,8,'Bold',PURPLE);para(c,p['note'],35,95,520,9,14,MUTED);c.showPage()
c.save()

css='''*{box-sizing:border-box}body{margin:0;background:#eae6f1;color:#252332;font:14px/1.6 Arial}header{position:sticky;top:0;background:#252332;color:white;padding:14px 25px;display:flex;justify-content:space-between;align-items:center;z-index:3}header p{margin:0;font-size:12px}button,a.button{font:12px Arial;border:0;border-radius:7px;padding:11px 15px;background:#ebe5fa;color:#252332;cursor:pointer;text-decoration:none}main{max-width:820px;margin:28px auto}.page{background:#f7f6f2;padding:48px;margin:25px 0;min-height:1050px;border-radius:4px;box-shadow:0 8px 30px #25233212}.brand{display:flex;justify-content:space-between;font-size:10px;letter-spacing:2px;border-bottom:1px solid #ddd5e8;padding-bottom:20px}.kicker{font-size:10px;color:#6550a6;letter-spacing:2px;margin:45px 0 20px}h1{font:42px/1.1 Georgia;letter-spacing:-1px;max-width:550px}p{color:#706c7b}.field{background:white;border:1px solid #e5dfeb;padding:18px 22px;border-radius:12px;margin:18px 0}.field:first-of-type{background:#ebe5fa}.field h2{font-size:14px}.field p{min-height:40px;margin-bottom:0}.note{font-size:11px;margin-top:30px}[contenteditable=true]{outline:1px dashed #b8a9d1;outline-offset:4px}[contenteditable=true]:focus{outline:2px solid #6550a6}footer{font-size:10px;margin-top:40px;color:#8c819e}@media(max-width:650px){header{flex-wrap:wrap;gap:10px}.page{padding:25px;margin:15px 10px;min-height:0}h1{font-size:34px}}@media print{body{background:white}header{display:none}main{margin:0;max-width:none}.page{margin:0;padding:15mm;min-height:0;height:267mm;box-shadow:none;break-after:page}.page:last-child{break-after:auto}[contenteditable=true]{outline:none}.kicker{margin-top:30px}h1{font-size:36px}.field{padding:13px 18px;margin:13px 0}.field p{min-height:25px}.note{margin-top:20px}@page{size:A4;margin:12mm}}'''
body='<header><p><b>THE DOCUMENT STUDIO</b> / Click outlined text to edit. Save HTML to keep your edits.</p><div><a class="button" href="../Studio.html#library">Back to studio</a> <button id="save">Save edited HTML</button> <button id="print">Print / save PDF</button></div></header><main>'
for i,p in enumerate(templates,1):
 body+='<section class="page"><div class="brand"><b contenteditable="true">YOUR STUDIO NAME</b><span>CLIENT COLLECTION</span></div><div class="kicker">'+p['kicker']+'</div><h1 contenteditable="true">'+html.escape(p['title']).replace('\n','<br>')+'</h1><p contenteditable="true">'+p['intro']+'</p>'
 body+=''.join('<article class="field"><h2>'+head+'</h2><p contenteditable="true">'+html.escape(text)+'</p></article>' for head,text in p['fields'])
 body+='<p class="note">'+p['note']+'</p><footer contenteditable="true">[Your contact] / [Client name] / [Date]</footer></section>'
body+='</main>'
script='''document.getElementById('print').onclick=()=>window.print();document.getElementById('save').onclick=()=>{const blob=new Blob(['<!doctype html>'+document.documentElement.outerHTML],{type:'text/html'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='My-Client-Documents.html';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};document.querySelectorAll('[contenteditable]').forEach(el=>el.addEventListener('paste',ev=>{ev.preventDefault();const t=ev.clipboardData.getData('text/plain');const s=window.getSelection();if(!s.rangeCount)return;const r=s.getRangeAt(0);r.deleteContents();const n=document.createTextNode(t);r.insertNode(n);r.setStartAfter(n);r.collapse(true);s.removeAllRanges();s.addRange(r)}));'''
(OUT/'Documents/Editable-Documents.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Your client document studio</title><style>'+css+'</style>'+body+'<script>'+script+'</script></html>')
(OUT/'Source/Guide-Content.json').write_text(json.dumps(chapters,indent=2));(OUT/'Source/Client-Document-Content.json').write_text(json.dumps(templates,indent=2))
if not (OUT/'Documents/Spreadsheet-Companion.xlsx').exists():
 shutil.copy(ROOT/'outputs/Brief-to-Approved/02-Workspace/Client-Workspace.xlsx',OUT/'Documents/Spreadsheet-Companion.xlsx')
print('Created 14-page visual guide, 6-page client collection and editable document studio.')
