"""Listing video v4 (14.6 s, 1440x1080, 30 fps, H.264 High, no audio).
Hook (cool, clutter) -> phone drops in, real checks toggle -> real approval typed + recorded -> tablet: real counter 1/3 -> 2/3
-> tablet calendar + phone reports -> exact hero end card. All screens are real captures from capture_all.py.
python3 capture_all.py --interactions && python3 video.py -> /tmp/claude-0/v/Listing-Video.mp4 + contact.jpg"""
import base64, io, json, subprocess, sys
sys.path.insert(0, '/tmp/claude-0/r')
from PIL import Image, ImageFilter, ImageEnhance
from comp import phone_screen, tablet_screen
from playwright.sync_api import sync_playwright
V = '/tmp/claude-0/v/'; SS = V + 'ss/'; R = '/tmp/claude-0/r/'; F = '/tmp/claude-0/w/'
W, H, FPS, DUR = 1440, 1080, 30, 14.6
T = json.load(open(SS + 'taps.json'))
def uri(im, w=None, q=90):
    if w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=q); return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
b64f = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
PH = ['ov0', 'ed1', 'ed2', 'saved', 'ap0', 'dlg0'] + [f'type{i:02d}' for i in range(T['phone_typeN'])] + ['ap1']
imgs = {f'p_{k}': uri(phone_screen(SS + f'phone_{k}.png', False), 680) for k in PH}
imgs['p_reports'] = uri(phone_screen(R + 'screens/phone-light-reports.png', False), 680)
for k in ['ov0', 'ov1']: imgs[f't_{k}'] = uri(tablet_screen(SS + f'tablet_{k}.png', False), 1700)
imgs['t_cal'] = uri(tablet_screen(R + 'screens/tablet-light-calendar.png', False), 1700)
hero = Image.open(V + 'hero.jpg').convert('RGB')
imgs['hero'] = uri(hero, 1600, 93)
cool = ImageEnhance.Brightness(ImageEnhance.Color(hero.resize((800, 600)).filter(ImageFilter.GaussianBlur(9))).enhance(.25)).enhance(.62)
imgs['cool'] = uri(cool, 800, 88)
pf = lambda k: [T[k][0] / 393, (T[k][1] + 54) / 852]              # phone css -> screen fraction (status bar 54 pt)
TAPS = {'run': pf('phone_run'), 'facts': pf('phone_facts'), 'tab': [267 / 393, (750 + 54) / 852], 'rec': pf('phone_rec'),
        'ev': pf('phone_ev'), 'recbtn': pf('phone_recbtn'), 'star': [783 / 1180, (T['tablet_star'][1] + 17 + 24) / 820]}   # label + value block of 'Approved now'
GOLD_L, GOLD_D = '#A47A22', '#E6C681'
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:NR;src:url(data:font/woff2;base64,{b64f(F + 'newsreader-latin-500-normal.woff2')})}}
@font-face{{font-family:IN;font-weight:100 900;src:url(data:font/woff2;base64,{b64f(F + 'inter-latin-wght-normal.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:{W}px;height:{H}px;overflow:hidden;background:#000;font-family:IN}}
.L{{position:absolute;left:0;top:0;will-change:transform,opacity}}
#cool,#hero{{width:{W}px;height:{H}px;object-fit:cover}}
#warm{{width:{W}px;height:{H}px;background:radial-gradient(ellipse 55% 60% at 22% 18%,#FFFBF4 0%,rgba(255,251,244,0) 70%),
 radial-gradient(ellipse 60% 70% at 85% 95%,#CDB8EE 0%,rgba(205,184,238,0) 70%),linear-gradient(150deg,#F6EEF9 0%,#E7DAF6 55%,#D9C8F1 100%)}}
#light{{width:{W}px;height:{H}px;background:radial-gradient(ellipse 45% 40% at 30% 25%,rgba(255,240,214,.55),rgba(255,240,214,0) 70%);mix-blend-mode:soft-light}}
.dev{{position:absolute;left:0;top:0;transform-origin:50% 50%}}
.phone{{width:350px;height:752px;border-radius:62px;padding:5px;background:linear-gradient(135deg,#6B6A70,#2B2B2F 22%,#8C8B91 48%,#2A2A2E 72%,#5E5D63);
 box-shadow:0 60px 90px -30px rgba(38,18,78,.55),0 18px 36px -10px rgba(38,18,78,.28),inset 0 0 0 1px rgba(255,255,255,.25)}}
.phone .bz{{width:100%;height:100%;border-radius:57px;background:#050506;padding:10px}}
.phone .sc{{position:relative;width:330px;height:722px;border-radius:47px;overflow:hidden;background:#fff}}
.phone .isl{{position:absolute;left:50%;top:11px;width:104px;height:30px;margin-left:-52px;border-radius:20px;background:#000;z-index:5}}
.btn{{position:absolute;background:linear-gradient(90deg,#3A3A3E,#7A797F);border-radius:3px}}
.tab{{width:880px;height:628px;border-radius:40px;padding:4px;background:linear-gradient(135deg,#8E8D93,#3A3A3E 30%,#9A999F 55%,#3B3B3F 80%,#6E6D73);
 box-shadow:0 70px 110px -36px rgba(38,18,78,.55),0 20px 40px -12px rgba(38,18,78,.28),inset 0 0 0 1px rgba(255,255,255,.25)}}
.tab .bz{{width:100%;height:100%;border-radius:36px;background:#050506;padding:22px}}
.tab .sc{{position:relative;width:828px;height:576px;border-radius:16px;overflow:hidden;background:#fff}}
.tab .cam{{position:absolute;left:50%;top:-14px;width:7px;height:7px;margin-left:-3px;border-radius:50%;background:#1d1d24}}
.sc img{{position:absolute;left:0;top:0;width:100%;height:auto;opacity:0}}
.glass{{position:absolute;inset:0;z-index:6;pointer-events:none;background:linear-gradient(118deg,rgba(255,255,255,.16) 0%,rgba(255,255,255,.04) 28%,rgba(255,255,255,0) 42%)}}
.tap{{position:absolute;z-index:7;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:50%;opacity:0;
 background:radial-gradient(circle,rgba(40,24,90,.32) 0 36%,rgba(40,24,90,.12) 37% 100%);border:2px solid rgba(255,255,255,.75)}}
.ring{{position:absolute;z-index:7;width:128px;height:54px;margin:-27px 0 0 -64px;border-radius:14px;border:3px solid {GOLD_L};opacity:0;box-shadow:0 0 0 8px rgba(196,154,60,.18)}}
.cap{{position:absolute;opacity:0}}
.lab{{font-size:44px;font-weight:650;letter-spacing:.01em;color:{GOLD_L};white-space:nowrap}}
.bar{{display:flex;gap:10px;margin:18px 0 22px}}.bar i{{display:block;width:70px;height:8px;border-radius:4px;background:rgba(90,60,150,.16)}}.bar i.on{{background:linear-gradient(90deg,#C49A3C,#E6C681)}}
.hd{{font-family:NR;font-weight:500;font-size:66px;line-height:1.02;letter-spacing:-.012em;color:#1B1236}}.hd em{{font-style:italic;color:{GOLD_L}}}
#c1,#c2{{left:705px;top:300px;width:447px}}
.top{{left:288px;width:864px;top:58px;text-align:center}}.top .bar{{justify-content:center}}.top .hd{{font-size:72px}}
.wash{{width:{W}px;height:330px;background:linear-gradient(180deg,rgba(246,239,250,.92) 0%,rgba(246,239,250,.78) 62%,rgba(246,239,250,0) 100%);opacity:0}}
#hook{{left:288px;width:864px;top:118px;text-align:center}}
.kick{{display:inline-block;font-size:44px;font-weight:600;color:#fff;padding:12px 30px;border-radius:999px;background:rgba(255,255,255,.14);border:1.5px solid rgba(255,255,255,.35)}}
#hook h1{{font-family:NR;font-weight:500;font-size:112px;line-height:.98;letter-spacing:-.015em;color:#fff;margin-top:34px;text-shadow:0 6px 30px rgba(0,0,0,.25)}}
#hook h1 em{{font-style:italic;color:{GOLD_D}}}
.mess{{position:absolute;left:0;top:0;white-space:nowrap;font-size:44px;font-weight:550;color:#2A2238;background:rgba(255,255,255,.93);
 padding:16px 28px 16px 26px;border-radius:22px;box-shadow:0 24px 50px -14px rgba(0,0,0,.45);display:flex;align-items:center;gap:18px}}
.mess i{{width:18px;height:18px;border-radius:50%;display:block;flex-shrink:0}}
#grain{{width:{W}px;height:{H}px;opacity:.07;mix-blend-mode:overlay;pointer-events:none}}
</style></head><body>
<img id="cool" class="L" src="{imgs['cool']}"><div id="warm" class="L"></div><div id="light" class="L"></div>
<div id="tabD" class="dev tab"><div class="bz"><div class="sc" id="tsc"><div class="cam"></div>
 <img id="t_ov0" src="{imgs['t_ov0']}"><img id="t_ov1" src="{imgs['t_ov1']}"><img id="t_cal" src="{imgs['t_cal']}"><div class="ring" id="ring"></div><div class="glass"></div></div></div></div>
<div id="phD" class="dev phone"><div class="btn" style="left:-3px;top:150px;width:4px;height:34px"></div><div class="btn" style="left:-3px;top:205px;width:4px;height:62px"></div>
 <div class="btn" style="left:-3px;top:280px;width:4px;height:62px"></div><div class="btn" style="right:-3px;top:225px;width:4px;height:96px"></div>
 <div class="bz"><div class="sc" id="psc"><div class="isl"></div>{''.join(f'<img id="{k}" src="{v}">' for k, v in imgs.items() if k.startswith('p_'))}
 <div class="tap" id="tap"></div><div class="glass"></div></div></div></div>
<div class="L wash" id="wash"></div>
<div id="m0" class="mess"><i style="background:#D65C50"></i>Re: Re: caption FINAL v3</div>
<div id="m1" class="mess"><i style="background:#3B82F6"></i>“Looks good” · which version?</div>
<div id="m2" class="mess"><i style="background:#2F9E6A"></i>brief_notes (2).docx</div>
<div id="m3" class="mess"><i style="background:#E0A42B"></i>Approved? Check the DMs</div>
<div id="hook" class="cap"><span class="kick">Social media planner app</span><h1>Approvals lost<br><em>in DMs?</em></h1></div>
<div id="c1" class="cap"><div class="lab">Step 1 · Checks</div><div class="bar"><i class="on"></i><i></i><i></i><i></i></div><div class="hd">Checks first.<br><em>Then the yes.</em></div></div>
<div id="c2" class="cap"><div class="lab">Step 2 · Approvals</div><div class="bar"><i class="on"></i><i class="on"></i><i></i><i></i></div><div class="hd">Every yes,<br><em>on record.</em></div></div>
<div id="c3" class="cap top"><div class="lab">Step 3 · Progress</div><div class="bar"><i class="on"></i><i class="on"></i><i class="on"></i><i></i></div><div class="hd">Watch the yeses <em>add up.</em></div></div>
<div id="c4" class="cap top"><div class="lab">Step 4 · Plan &amp; report</div><div class="bar"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></div><div class="hd">Your month, <em>at a glance.</em></div></div>
<img id="hero" class="L" src="{imgs['hero']}">
<svg id="grain" class="L"><filter id="n"><feTurbulence id="tb" type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="1"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
<script>
const TAPS={json.dumps(TAPS)}, TYPEN={T['phone_typeN']};
const $=id=>document.getElementById(id), cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)), lerp=(a,b,p)=>a+(b-a)*p;
const oc=x=>1-Math.pow(1-cl(x),3), ioc=x=>{{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}}, oq=x=>1-Math.pow(1-cl(x),5);
const seg=(t,a,b,f=oc)=>f((t-a)/(b-a));
function dev(el,w,h,cx,cy,s,rot=0,op=1,ry=0){{el.style.transform=`translate(${{cx-w/2}}px,${{cy-h/2}}px) perspective(1800px) rotateY(${{ry}}deg) rotate(${{rot}}deg) scale(${{s}})`;el.style.opacity=op}}
function cap(id,t,a,b){{const e=$(id),i=seg(t,a,a+.45),o=1-seg(t,b-.3,b,ioc);e.style.opacity=Math.min(i,o);e.style.transform=`translateY(${{(1-i)*26}}px)`}}
// screen timeline: [time, id] crossfades 0.25 s
const PS=[[0,'p_ov0'],[3.2,'p_ed1'],[3.92,'p_ed2'],[4.22,'p_saved'],[4.82,'p_ap0'],[5.32,'p_dlg0']];
for(let i=0;i<TYPEN;i++)PS.push([5.62+i*.085,'p_type'+String(i).padStart(2,'0')]);
PS.push([6.5,'p_ap1'],[9.25,'p_reports']);
const TS=[[0,'t_ov0'],[8.32,'t_ov1'],[9.12,'t_cal']];
const TP=[[3.05,'run'],[3.77,'facts'],[4.67,'tab'],[5.17,'rec'],[5.47,'ev'],[6.35,'recbtn']];
function screens(list,t,xf){{let cur=0;for(let i=0;i<list.length;i++)if(t>=list[i][0])cur=i;
 for(const [,id] of list)$(id).style.opacity=0;const [t0,id]=list[cur];const p=cur?cl((t-t0)/xf):1;
 $(id).style.opacity=1;if(cur&&p<1){{$(list[cur-1][1]).style.opacity=1;$(id).style.opacity=p}}}}
window.setT=function(t){{
 const bs=1+.01*t; $('cool').style.transform=`scale(${{1.04+.01*t}})`; $('warm').style.transform=`scale(${{bs}})`;
 const warm=seg(t,2.2,2.95,ioc); $('warm').style.opacity=warm; $('light').style.opacity=warm;
 // hook
 const ho=1-seg(t,2.15,2.45,ioc); $('hook').style.opacity=ho; $('hook').style.transform=`translateY(${{-seg(t,2.15,2.45)*30}}px)`;
 const M=[[-120,600,-3],[110,712,2.5],[-140,824,-1.5],[120,926,2]];
 M.forEach(([o,y,r],i)=>{{const e=$('m'+i),w=e.offsetWidth,x=cl(720-w/2+o,300,1140-w),d=Math.sin(t*1.3+i)*6,fly=seg(t,2.2+i*.07,2.75+i*.07,ioc);
  const tx=lerp(x,486-w/2,fly),ty=lerp(y+d,560,fly),s=lerp(1,.18,fly);e.style.opacity=(1-seg(t,2.55+i*.07,2.8+i*.07))*(1);
  e.style.transform=`translate(${{tx}}px,${{ty}}px) rotate(${{r*(1-fly)}}deg) scale(${{s}})`}});
 // phone: drop from top 2.2-2.85, push-in 4.6-5.4, exit 6.95-7.45, back for step 4 (9.05-9.7)
 let ph={{x:486,y:540,s:1,r:0,o:1}};
 if(t<2.2)ph.o=0;
 else if(t<7){{const d=seg(t,2.2,2.9,oq);ph.y=lerp(-460,540,d);ph.r=lerp(-7,0,seg(t,2.2,3.05,oq));ph.s=lerp(1.08,1,d);
  const pi=seg(t,4.6,5.4,ioc);ph.s=lerp(ph.s,1.1,pi);ph.y=lerp(ph.y,520,pi)}}
 else if(t<9.05){{const e=seg(t,6.95,7.5,ioc);ph.s=lerp(1.1,.9,e);ph.x=lerp(486,140,e);ph.y=lerp(520,600,e);ph.o=1-seg(t,7.0,7.45)}}
 else{{const d=seg(t,9.05,9.7,oq);ph={{x:990,y:lerp(-420,700,d),s:.8,r:lerp(6,0,seg(t,9.05,9.85,oq)),o:1}}}}
 if(t>=11.75){{const e=seg(t,11.75,12.3,ioc);ph.y+=e*40;ph.o*=1-e}}
 dev($('phD'),350,752,ph.x,ph.y,ph.s,ph.r,ph.o);
 // tablet: glides in from right 7.0-7.65, push-in to counter 7.85-8.6, pull back + left 9.0-9.6
 let tb={{x:720,y:650,s:1,o:0,ry:0}};
 if(t>=6.95){{const g=seg(t,6.95,7.7,oq);tb.x=lerp(1500,720,g);tb.ry=lerp(-24,0,g);tb.o=seg(t,6.95,7.2);
  const pi=seg(t,7.85,8.65,ioc);const fx=(TAPS.star[0]-.5)*880,fy=(TAPS.star[1]-.5)*628;tb.s=lerp(1,1.32,pi);tb.x-=fx*(tb.s-1);tb.y-=fy*(tb.s-1)+pi*30;
  const pb=seg(t,9.0,9.65,ioc);tb.s=lerp(tb.s,.86,pb);tb.x=lerp(tb.x,680,pb);tb.y=lerp(tb.y,660,pb)}}
 if(t>=11.75){{const e=seg(t,11.75,12.3,ioc);tb.y+=e*40;tb.o*=1-e}}
 dev($('tabD'),880,628,tb.x,tb.y,tb.s,0,tb.o,tb.ry);
 const rg=$('ring');rg.style.left=TAPS.star[0]*100+'%';rg.style.top=(TAPS.star[1]*100)+'%';rg.style.opacity=seg(t,8.15,8.4)*(1-seg(t,8.85,9.05));
 rg.style.transform=`scale(${{1+.05*Math.sin(Math.max(0,t-8.15)*7)}})`;
 // stage push-in for step 4
 const sp=1+.03*seg(t,9.6,11.8,x=>x);if(t>9.6){{for(const id of ['phD','tabD'])$(id).style.transform=`translate(720px,650px) scale(${{sp}}) translate(-720px,-650px) `+$(id).style.transform}}
 screens(PS,t,.25); screens(TS,t,.3);
 // taps: ripple appears 0.15 s before the screen change
 const tp=$('tap');tp.style.opacity=0;for(const [ts,k] of TP){{const l=t-ts;if(l>=0&&l<.42){{tp.style.left=TAPS[k][0]*100+'%';tp.style.top=TAPS[k][1]*100+'%';
  tp.style.opacity=l<.12?l/.12:1-(l-.12)/.3;tp.style.transform=`scale(${{.7+l*1.4}})`}}}}
 $('wash').style.opacity=seg(t,6.95,7.3)*(1-seg(t,11.6,11.9));
 cap('c1',t,2.45,4.6);cap('c2',t,4.72,6.95);cap('c3',t,7.12,8.95);cap('c4',t,9.15,11.85);
 // end: hero crossfade + 2.5% push-in
 const he=seg(t,11.95,12.3,ioc);$('hero').style.opacity=he;$('hero').style.transform=`scale(${{1+.025*seg(t,11.95,14.6,x=>x)}})`;
 $('tb').setAttribute('seed',Math.floor(t*30)%17+1);
}};
window.textBoxes=()=>[...document.querySelectorAll('.cap,.mess')].filter(e=>+getComputedStyle(e).opacity>.5).map(e=>{{const r=e.getBoundingClientRect();return [e.id,Math.round(r.left),Math.round(r.right)]}});
</script></body></html>"""
open(V + 'video.html', 'w').write(html)
N = round(DUR * FPS); out = V + 'Listing-Video.mp4'
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'png', '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                       '-movflags', '+faststart', '-an', '-r', str(FPS), out], stdin=subprocess.PIPE)
bad = []; SHEET = [round(i * (N - 1) / 15) for i in range(16)]; thumbs = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}); pg.goto('file://' + V + 'video.html'); pg.wait_for_timeout(1200)
    for n in range(N):
        t = n / FPS; pg.evaluate(f'setT({t})'); png = pg.screenshot(type='png'); ff.stdin.write(png)
        if n % 6 == 0:
            for idn, l, r in pg.evaluate('textBoxes()'):
                if l < 288 - 2 or r > 1152 + 2: bad.append((round(t, 2), idn, l, r))
        if n in SHEET: thumbs.append(Image.open(io.BytesIO(png)).convert('RGB').resize((360, 270)))
        if n == N - 1: Image.open(io.BytesIO(png)).convert('RGB').save(V + 'last.png')
    b.close()
ff.stdin.close(); ff.wait()
sheet = Image.new('RGB', (360 * 4, 270 * 4))
for i, im in enumerate(thumbs): sheet.paste(im, ((i % 4) * 360, (i // 4) * 270))
sheet.save(V + 'contact.jpg', quality=85)
print('frames', N, 'text outside safe zone:', sorted(set((x[1]) for x in bad)) or 'none', bad[:6])
