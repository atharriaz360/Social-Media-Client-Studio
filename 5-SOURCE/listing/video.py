"""Listing video v3: hook (6 loose ends) -> all solved at once -> 6-feature tour on real screens -> hero end card.
python3 video.py  -> Listing-Video.mp4 (1440x1080, 30 fps, 15 s, H.264, no audio)"""
import subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
V = '/tmp/claude-0/v/'; F = '/tmp/claude-0/w/'
W, H, FPS, DUR = 1440, 1080, 30, 15.0
SER = F + 'newsreader-latin-500-normal.woff2'; SANS = F + 'inter-latin-wght-normal.woff2'
def font(path, size, wght=None):
    f = ImageFont.truetype(path, size)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f
F_H = font(SER, 82); F_K = font(SANS, 26, 650); F_C = font(SANS, 31, 560); F_P = font(SANS, 30, 650)
INK = (28, 21, 51); PLUM = (36, 23, 74); LIL = (126, 98, 214)
plates = {k: Image.open(V + f'plates/{k}.png').convert('RGB')
          for k in ['overview', 'content', 'calendar', 'approvals', 'brief', 'reports', 'dark']}
hero = Image.open('/mnt/user-data/outputs/01-Hero-v2.jpg').convert('RGB')
hook_bg = ImageEnhance.Color(plates['overview']).enhance(0.55)
hook_bg = ImageEnhance.Brightness(hook_bg).enhance(0.93)

ease = lambda x: 0 if x <= 0 else 1 if x >= 1 else 0.5 - 0.5 * math.cos(math.pi * x)
def zoom(img, z, cx=0.5, cy=0.78):
    IW, IH = img.size
    w, h = IW / z, IH / z; x = (IW - w) * cx; y = (IH - h) * cy
    return img.crop((int(x), int(y), int(x + w), int(y + h))).resize((W, H), Image.LANCZOS)

def text_c(d, y, s, f, fill, alpha=255):
    tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y), s, font=f, fill=fill + (alpha,))

def check(d, x, y, s, col):
    d.line([(x, y + s * .55), (x + s * .38, y + s * .9), (x + s, y + s * .1)], fill=col, width=max(3, int(s / 5)), joint='curve')

CHIPS = [['brief buried in email', 'which version?', 'facts checked?'],
         ['approved in DMs?', 'photo rights?', 'report due Friday']]
def draw_chips(ov, p_solve, alpha):
    d = ImageDraw.Draw(ov)
    for r, row in enumerate(CHIPS):
        widths = [d.textlength(t, font=F_C) + 92 for t in row]; gap = 18
        x = (W - sum(widths) - gap * (len(row) - 1)) / 2; y = 238 + r * 70
        for t, w in zip(row, widths):
            pop = 1 + 0.08 * math.sin(math.pi * min(1, p_solve * 1.0)) if 0 < p_solve < 1 else 1
            h = 56 * pop; yy = y - (h - 56) / 2; ww = w * pop; xx = x - (ww - w) / 2
            solved = p_solve >= 0.35
            bg = (PLUM if solved else (255, 255, 255)) + (int(alpha * (245 if solved else 235)),)
            d.rounded_rectangle((xx, yy, xx + ww, yy + h), radius=h / 2, fill=bg,
                                outline=(LIL if solved else (226, 214, 240)) + (alpha,), width=2)
            if solved: check(d, xx + 22, yy + 17, 22, (201, 184, 255, alpha))
            else: d.ellipse((xx + 26, yy + 22, xx + 38, yy + 34), fill=(214, 92, 80, alpha))
            d.text((xx + 58, yy + 11), t, font=F_C, fill=((255, 255, 255) if solved else (52, 44, 70)) + (alpha,))
            x += w + gap

def pill(d, y, s, alpha):
    tw = d.textlength(s, font=F_P); x = (W - tw - 56) / 2
    d.rounded_rectangle((x, y, x + tw + 56, y + 54), radius=27, fill=PLUM + (int(alpha * .95),))
    d.text((x + 28, y + 10), s, font=F_P, fill=(255, 255, 255, alpha))

TOUR = [('content', 'Every post, draft to live.'), ('calendar', 'Your month at a glance, on iPad.'),
        ('approvals', 'A yes for this exact version.'), ('brief', 'One brief. Every answer.'),
        ('reports', 'Reports that do the math.'), ('dark', 'Desktop + phone. Light & dark.')]
T0, SEG = 3.3, 1.5; TEND = T0 + SEG * len(TOUR)

def frame(t):
    if t < 3.3:  # hook + all-at-once solve
        sp = ease((t - 1.9) / 0.5)              # 1.9-2.4s: all chips flip together
        bgmix = ease((t - 2.2) / 0.6)
        base = Image.blend(hook_bg, plates['approvals'], bgmix)
        img = zoom(base, 1.16 + 0.03 * (t / 3.3))
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        text_c(d, 44, 'SOCIAL MEDIA MANAGER PLANNER APP', F_K, (74, 47, 152))
        a1 = int(255 * (1 - ease((t - 2.0) / 0.15))); a2 = int(255 * ease((t - 2.15) / 0.2))
        if a1: text_c(d, 98, 'Approvals lost in DMs?', F_H, INK, a1)
        if a2: text_c(d, 98, 'All handled. In one app.', F_H, INK, a2)
        calpha = int(255 * (1 - ease((t - 2.85) / 0.4)))
        if calpha: draw_chips(ov, sp, calpha)
        if t < 2.0: pill(d, 980, '6 loose ends', int(255 * ease(t / 0.3)))
        elif t < 3.1: pill(d, 980, '0 loose ends · all done at once', int(255 * (1 - ease((t - 2.85) / 0.25))))
        img = img.convert('RGBA'); img.alpha_composite(ov); return img.convert('RGB')
    if t < TEND:  # feature tour
        i = min(len(TOUR) - 1, int((t - T0) / SEG)); lt = t - T0 - i * SEG
        key, cap = TOUR[i]
        Z0 = {'calendar': (1.0, .62)}.get(key, (1.22, .78))
        img = zoom(plates[key], Z0[0] + 0.05 * ease(lt / SEG), 0.5, Z0[1])
        if lt < 0.25:
            pk = TOUR[i - 1][0] if i else None
            prev = (zoom(plates[pk], 1.05, .5, .62) if pk == 'calendar' else zoom(plates[pk], 1.27)) if i else zoom(plates['approvals'], 1.19)
            img = Image.blend(prev, img, ease(lt / 0.25))
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        a = int(255 * min(ease(lt / 0.3), 1 - ease((lt - SEG + 0.2) / 0.2)))
        text_c(d, 56, f'{i + 1:02d} / {len(TOUR):02d}', F_K, (74, 47, 152), a)
        text_c(d, 102, cap, F_H, INK, a)
        img = img.convert('RGBA'); img.alpha_composite(ov); return img.convert('RGB')
    lt = t - TEND  # end card
    img = zoom(hero, 1.0 + 0.02 * ease(lt / (DUR - TEND)), 0.5, 0.5)
    if lt < 0.35: img = Image.blend(zoom(plates['dark'], 1.27), img, ease(lt / 0.35))
    return img

N = int(DUR * FPS)
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart', '-an',
                      V + 'Listing-Video.mp4'], stdin=subprocess.PIPE)
for n in range(N):
    fr = frame(n / FPS); p.stdin.write(fr.tobytes())
    if n in (0, 45, 66, 80, 100, 150, 200, 260, 320, 370, 420): fr.save(V + f'f{n:03d}.jpg', quality=85)
p.stdin.close(); p.wait(); print('done', p.returncode)
