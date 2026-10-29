"""Text overlays for listing images (same style as the existing set). python3 overlay.py [names]"""
import sys, base64
from playwright.sync_api import sync_playwright
R = '/tmp/claude-0/r/'; F = '/tmp/claude-0/w/'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
FONTS = (f"@font-face{{font-family:NR;src:url(data:font/woff2;base64,{b64(F+'newsreader-latin-500-normal.woff2')})}}"
         f"@font-face{{font-family:IN;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F+'inter-latin-wght-normal.woff2')})}}")
CHECK = '<svg viewBox="0 0 24 24" width="1em" height="1em"><circle cx="12" cy="12" r="12" fill="#6A4FC4"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
IMG = {
 '03-Content-Board': dict(pos='left', w=1000, chip='Posts scattered across DMs and docs?', h='Every post,<br><em>draft to live.</em>',
     sub='One card per post moves through six clear stages, on desktop and phone.',
     bullets=['List or board view', 'Search, filter, export CSV', 'Due date + version on every card']),
 '05-Calendar-Reports': dict(pos='top', chip='Where did the month go?', h='Plan the month. <em>Report what happened.</em>',
     sub='Stage-coloured calendar on iPad, plus post results that calculate themselves.',
     chips=['Rate by reach, calculated', 'Blank stays blank, never a fake zero', 'Print or save as PDF']),
 '06-Phone': dict(pos='right', w=1000, chip='Away from your desk?', h='Made for your<br><em>phone,</em> too.',
     sub='Every view adapts to a phone screen, in light or dark mode.',
     bullets=['All 9 views fit phone screens', 'Light and dark mode', 'Add it to your Home Screen']),
 '10-Private-Offline': dict(pos='left', w=900, chip='Client data in another cloud app?', h='Private by design.<br><em>Works offline.</em>',
     sub='One HTML file. Your work saves in your browser: no account, no sign-up.',
     bullets=['No account, no subscription', 'One-click JSON backup and restore', 'Export content to CSV'],
     note='Browser storage can be cleared. Export a backup after each session.'),
}
CSS = """*{margin:0;padding:0;box-sizing:border-box}body{width:3000px;height:2250px;position:relative;overflow:hidden;font-family:IN;color:#1C1533}
.t{position:absolute}.chip{display:inline-flex;align-items:center;gap:20px;background:rgba(255,255,255,.92);border:2px solid #E6DCF3;border-radius:999px;
padding:18px 36px;font-size:44px;font-weight:500;color:#3B3150;box-shadow:0 10px 30px rgba(40,20,80,.08)}.chip i{width:16px;height:16px;border-radius:50%;background:#D65C50;display:block}
h1{font-family:NR;font-weight:500;font-size:150px;line-height:1.02;letter-spacing:-.012em;margin-top:44px}h1 em{font-style:italic;color:#5536B0}
.sub{font-size:56px;line-height:1.35;color:#4B4460;margin-top:40px}ul{list-style:none;margin-top:56px}li{display:flex;align-items:center;gap:30px;font-size:54px;font-weight:500;margin-bottom:34px}
li svg{font-size:62px;flex-shrink:0}.note{font-size:36px;color:#6F6880;margin-top:30px}
.chips{position:absolute;left:0;right:0;bottom:130px;display:flex;justify-content:center;gap:30px}
.chips div{display:flex;align-items:center;gap:22px;background:rgba(255,255,255,.94);border-radius:999px;padding:26px 46px;font-size:50px;font-weight:600;box-shadow:0 14px 40px rgba(40,20,80,.12)}
.chips svg{font-size:54px}"""
def html(name, d):
    plate = 'data:image/png;base64,' + b64(R + f'plate_{name}.png')
    body = f'<div class="chip"><i></i>{d["chip"]}</div><h1>{d["h"]}</h1><p class="sub">{d["sub"]}</p>'
    if 'bullets' in d: body += '<ul>' + ''.join(f'<li>{CHECK}<span>{b}</span></li>' for b in d['bullets']) + '</ul>'
    if 'note' in d: body += f'<p class="note">{d["note"]}</p>'
    if d['pos'] == 'left': box = f'<div class="t" style="left:150px;top:300px;width:{d["w"]}px">{body}</div>'
    elif d['pos'] == 'right': box = f'<div class="t" style="right:110px;top:150px;width:{d["w"]}px">{body}</div>'
    else: box = f'<div class="t" style="left:0;right:0;top:90px;text-align:center"><style>h1{{font-size:132px;margin-top:34px}}.sub{{margin-top:26px}}</style>{body}</div>'
    if 'chips' in d: box += '<div class="chips">' + ''.join(f'<div>{CHECK}<span>{c}</span></div>' for c in d['chips']) + '</div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}</style></head><body style="background:url({plate})">{box}</body></html>'
names = sys.argv[1:] or list(IMG)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 3000, 'height': 2250})
    for n in names:
        open(R + f'ov_{n}.html', 'w').write(html(n, IMG[n])); pg.goto('file://' + R + f'ov_{n}.html'); pg.wait_for_timeout(400)
        pg.screenshot(path=R + f'{n}.png'); print('rendered', n)
    b.close()
from PIL import Image
for n in names:
    im = Image.open(R + f'{n}.png').convert('RGB'); im.save(R + f'{n}.jpg', quality=92, subsampling=0); im.resize((1350, 1012)).save(R + f'v_{n}.jpg', quality=85)
