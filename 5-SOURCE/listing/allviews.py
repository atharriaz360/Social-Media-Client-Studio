"""02-All-Views: 3x3 grid of the 9 real desktop screens (light). python3 allviews.py -> 02-All-Views.jpg (3000x2250)"""
import base64
from playwright.sync_api import sync_playwright
from PIL import Image
R = '/tmp/claude-0/r/'; F = '/tmp/claude-0/w/'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
V = [('overview', 'Overview'), ('content', 'Content'), ('calendar', 'Calendar'), ('approvals', 'Approvals'), ('brief', 'Client brief'),
     ('assets', 'Assets'), ('reports', 'Reports'), ('library', 'Guide & templates'), ('settings', 'Settings')]
for k, _ in V:  # downscale once so the page stays light
    Image.open(R + f'screens/desktop-light-{k}.png').convert('RGB').resize((1520, 950), Image.LANCZOS).save(R + f'g_{k}.jpg', quality=92)
cards = ''.join(f'<figure><div class="s"><img src="data:image/jpeg;base64,{b64(R + f"g_{k}.jpg")}"></div>'
                f'<figcaption><b>{i + 1:02d}</b>{n}</figcaption></figure>' for i, (k, n) in enumerate(V))
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:NR;src:url(data:font/woff2;base64,{b64(F + 'newsreader-latin-500-normal.woff2')})}}
@font-face{{font-family:IN;font-weight:100 900;src:url(data:font/woff2;base64,{b64(F + 'inter-latin-wght-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:3000px;height:2250px;overflow:hidden;font-family:IN;color:#1C1533;position:relative;
background:radial-gradient(ellipse 60% 50% at 18% 8%,#FBF7FF 0%,rgba(251,247,255,0) 70%),radial-gradient(ellipse 70% 60% at 90% 100%,#D9C9F0 0%,rgba(217,201,240,0) 70%),linear-gradient(160deg,#F1E9FA,#E4D6F4)}}
body:after{{content:'';position:absolute;inset:0;opacity:.22;mix-blend-mode:multiply;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .55 0 0 0 0 .5 0 0 0 0 .62 0 0 0 .5 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
header{{position:absolute;top:96px;left:0;right:0;text-align:center}}
.k{{font-weight:700;font-size:40px;letter-spacing:.22em;color:#5A3FB0}}
h1{{font-family:NR;font-weight:500;font-size:132px;letter-spacing:-.012em;margin-top:18px;line-height:1}}h1 em{{color:#5536B0}}
.sub{{font-size:48px;color:#4B4460;margin-top:22px}}
.g{{position:absolute;left:255px;top:452px;display:grid;grid-template-columns:repeat(3,770px);column-gap:75px;row-gap:34px}}
figure .s{{width:770px;height:481px;border-radius:26px;overflow:hidden;border:7px solid #fff;
box-shadow:0 2px 0 rgba(255,255,255,.8) inset,0 30px 60px -18px rgba(52,28,104,.32),0 8px 18px rgba(52,28,104,.10);background:#fff}}
figure img{{width:100%;height:100%;display:block}}
figcaption{{font-size:46px;font-weight:600;margin-top:18px;display:flex;gap:18px;align-items:baseline}}
figcaption b{{color:#6A4FC4;font-weight:700}}
</style></head><body>
<header><div class="k">ALL-IN-ONE STUDIO</div><h1>Nine focused views. <em>Nothing extra.</em></h1>
<p class="sub">Real screens from the app, shown with fictional sample data.</p></header>
<div class="g">{cards}</div></body></html>"""
open(R + 'allviews.html', 'w').write(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 3000, 'height': 2250})
    pg.goto('file://' + R + 'allviews.html'); pg.wait_for_timeout(600); pg.screenshot(path=R + '02-All-Views.png'); b.close()
im = Image.open(R + '02-All-Views.png').convert('RGB'); im.save(R + '02-All-Views.jpg', quality=92, subsampling=0)
im.resize((1500, 1125)).save(R + 'v_02.jpg', quality=85); print('ok', im.size)
