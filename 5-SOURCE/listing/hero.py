"""01-Hero on _Canva-BG/image.png (mock UI, title and pill inpainted out; vases kept): HTML MacBook + iPhone around real captures.
Desktop screen captured at the owner MacBook Chrome size: 1588x910 CSS (80% zoom), 2540x1456 px.
python3 hero.py -> /tmp/claude-0/r/01-Hero.jpg (3000x2250, sRGB, <1 MB) + hero.html"""
import base64, io, sys
sys.path.insert(0, '/tmp/claude-0/r')
from comp import phone_screen
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright
R = '/tmp/claude-0/r/'; F = '/tmp/claude-0/w/'; BG = '/home/claude/bta/5-SOURCE/_Canva-BG/image.png'
APP = 'file:///home/claude/bta/1-SELL-THIS/Brief-to-Approved.html'
def uri(im, w=None, q=92):
    if w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=q); return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
f64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
import cv2, numpy as np, json
def plate():
    im = cv2.imread(BG).astype(np.float32); H, W = im.shape[:2]; m = np.zeros((H, W), np.float32)
    for x0, y0, x1, y1 in [(228, 50, 800, 238), (228, 240, 1000, 618), (172, 556, 240, 600), (390, 612, 625, 675)]: m[y0:y1, x0:x1] = 1
    ref = im[:, 960:1024]; base = np.repeat(cv2.GaussianBlur(ref.mean(1, keepdims=True), (0, 0), 4), W, 1)
    sd = (ref - cv2.GaussianBlur(ref, (0, 0), 3)).std(); n = cv2.GaussianBlur(np.random.default_rng(7).normal(0, 1, (H, W)).astype(np.float32), (0, 0), .7)
    fill = base + (n / n.std() * sd * .9)[..., None]; k = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
    out = np.clip(im * (1 - k) + fill * k, 0, 255).astype(np.uint8)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).resize((3000, 2241), Image.LANCZOS).crop((0, 0, 3000, 2241))
bg = plate()
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={'width': 1588, 'height': 910}, device_scale_factor=1.6, color_scheme='light')
    c.add_init_script("try{localStorage.setItem('brief-approved-ui-v5'," + json.dumps(json.dumps({'theme': 'light', 'focus': False, 'layout': 'list'})) + ")}catch(e){}")
    pg = c.new_page(); pg.goto(APP + '#overview'); pg.wait_for_timeout(1500); pg.screenshot(path=F + 'lap_1588.png'); b.close()
import os
MAC = '/home/claude/bta/5-SOURCE/listing/mac-overview.png'   # owner's real Mac screenshot (browser bar + extension button cropped)
lap = Image.open(MAC if os.path.exists(MAC) else F + 'lap_1588.png')
ph = phone_screen(R + 'screens/phone-light-overview.png', False)
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:NR;src:url(data:font/woff2;base64,{f64(F+'newsreader-latin-500-normal.woff2')})}}
@font-face{{font-family:NI;src:url(data:font/woff2;base64,{f64(F+'newsreader-latin-500-italic.woff2')})}}
@font-face{{font-family:IN;font-weight:100 900;src:url(data:font/woff2;base64,{f64(F+'inter-latin-wght-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:3000px;height:2250px;position:relative;overflow:hidden;font-family:IN;background:#EEECE8 url({uri(bg,3000,92)}) top/3000px auto no-repeat}}
.L{{position:absolute;inset:0}}
.warm{{background:radial-gradient(ellipse 50% 60% at 6% 25%,rgba(255,226,186,.30),rgba(255,226,186,0) 70%),radial-gradient(ellipse 70% 50% at 55% 70%,rgba(176,150,230,.10),rgba(176,150,230,0) 70%)}}
.vig{{background:radial-gradient(ellipse 80% 80% at 50% 50%,rgba(0,0,0,0) 60%,rgba(70,55,40,.14) 100%)}}
.brand{{position:absolute;top:70px;right:646px;height:72px;display:flex;align-items:center;font-size:32px;font-weight:700;letter-spacing:.05em;color:#111}}
.brand b{{color:#B8892E;font-weight:800}}
.top{{position:absolute;left:0;right:0;top:70px;text-align:center;color:#1D1838}}
.kick{{height:72px;display:inline-flex;align-items:center;gap:22px;font-weight:700;font-size:42px;letter-spacing:.2em;color:#3B2585}}
.kick .rb{{display:inline-flex;align-items:center;gap:14px;height:72px;padding:0 30px 0 26px;border-radius:999px;color:#24163F;letter-spacing:.16em;font-weight:800;
 background:linear-gradient(180deg,#F6E3AE 0%,#E0BD6A 45%,#C79A3E 100%);box-shadow:0 14px 30px -12px rgba(140,98,24,.6),inset 0 2px 0 rgba(255,255,255,.6),inset 0 -2px 0 rgba(130,90,20,.35)}}
.kick .rb svg{{width:30px;height:30px;fill:#24163F}}
h1{{font-family:NR;font-weight:500;font-size:178px;line-height:.95;margin-top:40px;letter-spacing:-.015em}}
h1 em{{font-family:NI;font-style:italic;display:block;color:#5332B4}}
.sub{{margin-top:30px;font-weight:600;font-size:56px;color:#3A3352;letter-spacing:.005em}}.sub b{{color:#B48A33;font-weight:500;margin:0 18px}}
.lap{{position:absolute;left:640px;top:690px;width:1640px}}
.lid{{width:1640px;height:1005px;border-radius:44px 44px 14px 14px;padding:10px;background:linear-gradient(135deg,#C9C8CD,#77767C 28%,#D4D3D8 55%,#6A696F 82%,#A9A8AE);box-shadow:0 0 0 1.5px rgba(255,255,255,.6)}}
.bez{{width:100%;height:100%;border-radius:36px 36px 8px 8px;background:#060608;padding:36px 30px 30px;position:relative}}
.cam{{position:absolute;left:50%;top:12px;width:11px;height:11px;margin-left:-5px;border-radius:50%;background:#1b1b24;box-shadow:inset 0 0 0 3px #0c0c12}}
.scr{{width:1560px;height:909px;overflow:hidden;border-radius:6px;position:relative;background:#fff}}
.scr img{{width:100%;height:100%;object-fit:cover;object-position:top;display:block}}
.glass{{position:absolute;inset:0;background:linear-gradient(118deg,rgba(255,255,255,.14) 0%,rgba(255,255,255,.03) 30%,rgba(255,255,255,0) 44%);pointer-events:none}}
.base{{position:relative;margin:-2px -110px 0;height:52px;border-radius:4px 4px 36px 36px/4px 4px 52px 52px;background:linear-gradient(180deg,#E6E5EA 0%,#B3B2B8 40%,#7C7B81 100%);
 box-shadow:0 60px 70px -30px rgba(70,52,34,.45),0 22px 30px -12px rgba(70,52,34,.35)}}
.base:before{{content:'';position:absolute;left:50%;top:0;width:270px;height:20px;margin-left:-135px;border-radius:0 0 20px 20px;background:linear-gradient(180deg,#9C9BA1,#C3C2C8)}}
.phone{{position:absolute;left:2040px;top:900px;width:420px;height:888px;border-radius:74px;padding:6px;background:linear-gradient(135deg,#8A898F,#3A3A3E 22%,#ABAAB0 48%,#38383C 72%,#7A797F);
 box-shadow:-24px 56px 70px -26px rgba(70,52,34,.55),0 16px 30px -10px rgba(70,52,34,.35),inset 0 0 0 1.5px rgba(255,255,255,.35)}}
.phone .bz{{width:100%;height:100%;border-radius:68px;background:#050506;padding:12px}}
.phone .sc{{position:relative;width:384px;height:852px;border-radius:57px;overflow:hidden;background:#fff}}
.phone .sc img{{width:100%;height:100%;object-fit:cover;object-position:top;display:block}}
.isl{{position:absolute;left:50%;top:13px;width:118px;height:34px;margin-left:-59px;border-radius:20px;background:#000;z-index:3}}
.stage{{position:absolute;inset:0;transform:scale(1.07);transform-origin:1500px 1180px}}
.hi{{position:absolute;left:0;right:0;bottom:0;height:12px;background:#fff;z-index:2}}.hi:after{{content:"";position:absolute;left:50%;bottom:5px;width:132px;height:5px;margin-left:-66px;border-radius:3px;background:#111}}
.pill{{position:absolute;left:0;right:0;top:1890px;display:flex;justify-content:center}}
.pill div{{display:flex;gap:24px;align-items:center;font-weight:700;font-size:54px;letter-spacing:.01em;color:#fff;padding:30px 70px 30px 60px;border-radius:999px;
 background:linear-gradient(180deg,#3A2670 0%,#24163F 100%);box-shadow:0 22px 46px -16px rgba(36,22,63,.65),inset 0 2px 0 rgba(255,255,255,.14),0 0 0 3px rgba(224,189,106,.55)}}
.pill svg{{width:58px;height:58px}}
.pill i{{font-style:normal;opacity:.55}}
svg.g{{position:absolute;inset:0;opacity:.05;mix-blend-mode:multiply}}
</style></head><body>
<div class="L warm"></div><div class="L vig"></div><svg class="g" width="3000" height="2250"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
<div class="brand"><b>K</b>aelLabs</div>
<div class="top"><div class="kick"><span class="rb"><svg viewBox="0 0 24 24"><path d="M12 2l2.6 7.4L22 12l-7.4 2.6L12 22l-2.6-7.4L2 12l7.4-2.6Z"/></svg>REAL APP</span>FOR FREELANCE</div>
 <h1>Social Media Manager<em>Planner App</em></h1>
 <div class="sub">Brief<b>·</b>Calendar<b>·</b>Approvals<b>·</b>Reports</div></div>
<div class="stage"><div class="lap"><div class="lid"><div class="bez"><div class="cam"></div><div class="scr"><img src="{uri(lap,2600)}"><div class="glass"></div></div></div></div><div class="base"></div></div>
<div class="phone"><div class="bz"><div class="sc"><div class="isl"></div><img src="{uri(ph,1206)}"><div class="hi"></div><div class="glass"></div></div></div></div></div>
<div class="pill"><div><svg viewBox="0 0 24 24"><path d="M12 3v12m-5-5 5 5 5-5M5 20h14" stroke="#E6C46F" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>Instant Download</div></div>
</body></html>"""
open('/home/claude/bta/5-SOURCE/listing/hero.html', 'w').write(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 3000, 'height': 2250})
    pg.set_content(html); pg.wait_for_timeout(800); pg.screenshot(path=R + '01-Hero.png'); b.close()
im = Image.open(R + '01-Hero.png').convert('RGB')
q = 92
while True:
    im.save(R + '01-Hero.jpg', quality=q, subsampling=0)
    import os
    if os.path.getsize(R + '01-Hero.jpg') < 1_000_000 or q < 70: break
    q -= 4
im.save('/tmp/claude-0/v/hero.jpg', quality=93)
im.resize((1500, 1125)).save(R + 'v_01.jpg', quality=88); print('ok q', q, os.path.getsize(R + '01-Hero.jpg'))
