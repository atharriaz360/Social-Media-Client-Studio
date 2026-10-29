"""Composite real screens into green-screen device photos.
plate(plate_id, S, devices, canvas=(3000,2250), offset=(ox,oy)) -> numpy BGR canvas
devices: list of dicts in component order (largest area first): {kind, ranges(optional)}
Screens are generated to the exact quad aspect so nothing is stretched."""
import numpy as np, cv2
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
BG = '/mnt/user-data/uploads/Brief-to-Approved/5-SOURCE/_Canva-BG/'
FONT = '/tmp/claude-0/w/inter-latin-wght-normal.woff2'

def load(pid, S):
    bg = cv2.imread(BG + f'{pid}.jpg')
    bg = cv2.resize(bg, None, fx=S, fy=S, interpolation=cv2.INTER_LANCZOS4)
    bl = cv2.GaussianBlur(bg, (0, 0), 1.2)
    bg = cv2.addWeighted(bg, 1.35, bl, -0.35, 0)   # gentle sharpen after upscale
    b, g, r = [bg[:, :, i].astype(np.float32) for i in range(3)]
    k = np.clip((g - np.maximum(r, b) - 40) / 60, 0, 1)
    lab, n = ndimage.label(k > 0.5)
    sizes = ndimage.sum(k > 0.5, lab, range(1, n + 1))
    comps = [lab == i + 1 for i in np.argsort(sizes)[::-1] if sizes[i] > 3000 * S * S]
    return bg, k, comps

def quad(m, top=(.4, .62), bot=(.38, .6), lef=(.25, .75), rig=(.25, .75)):
    ys, xs = np.where(m); X0, X1, Y0, Y1 = xs.min(), xs.max(), ys.min(), ys.max()
    wx, wy = X1 - X0, Y1 - Y0
    def fx(rng, fn):
        cols = range(int(X0 + rng[0] * wx), int(X0 + rng[1] * wx))
        pts = np.array([(x, fn(np.where(m[:, x])[0])) for x in cols if m[:, x].any()], float)
        return np.polyfit(pts[:, 0], pts[:, 1], 1)
    def fy(rng, fn):
        rows = range(int(Y0 + rng[0] * wy), int(Y0 + rng[1] * wy))
        pts = np.array([(fn(np.where(m[y, :])[0]), y) for y in rows if m[y, :].any()], float)
        return np.polyfit(pts[:, 1], pts[:, 0], 1)
    T, B, L, R = fx(top, np.min), fx(bot, np.max), fy(lef, np.min), fy(rig, np.max)
    def inter(lx, ly):
        a, b = lx; c, d = ly; y = (a * d + b) / (1 - a * c); return (c * y + d, y)
    return np.float32([inter(T, L), inter(T, R), inter(B, R), inter(B, L)])

def aspect(q):  # height / width of the screen in its own plane (approx.)
    w = (np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3])) / 2
    h = (np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])) / 2
    return h / w

def _icons(d, xr, cy, s, ink, dim, wifi=True, signal=True):
    x = xr
    bw, bh = 25 * s, 12 * s   # battery (drawn right to left)
    x -= bw + 3 * s
    d.rounded_rectangle((x, cy - bh / 2, x + bw, cy + bh / 2), radius=3.6 * s, outline=dim, width=max(2, int(1.3 * s)))
    d.rounded_rectangle((x + 2.3 * s, cy - bh / 2 + 2.3 * s, x + bw - 4.6 * s, cy + bh / 2 - 2.3 * s), radius=2 * s, fill=ink)
    d.rounded_rectangle((x + bw + 1.3 * s, cy - 2.7 * s, x + bw + 3.2 * s, cy + 2.7 * s), radius=1 * s, fill=dim)
    if wifi:
        x -= 7 * s + 17 * s; cx, cw = x + 8.5 * s, cy + 6.5 * s
        for r in (12 * s, 8 * s):
            d.arc((cx - r, cw - r, cx + r, cw + r), start=225, end=315, fill=ink, width=max(2, int(3 * s)))
        r = 4.3 * s; d.pieslice((cx - r, cw - r, cx + r, cw + r), start=225, end=315, fill=ink)
    if signal:
        x -= 7 * s + 18 * s
        for i in range(4):
            h = (4.5 + i * 3) * s; bx = x + i * 5.7 * s
            d.rounded_rectangle((bx, cy + 6 * s - h, bx + 3.6 * s, cy + 6 * s), radius=1 * s, fill=ink)

def phone_screen(app_png, dark):
    """iPhone 15 Pro status bar (54 pt) above the real app capture + home indicator. @3x."""
    app = Image.open(app_png).convert('RGB'); W = app.width; SB = 162
    top = app.getpixel((W // 2, 3))
    img = Image.new('RGB', (W, app.height + SB), top); img.paste(app, (0, SB))
    d = ImageDraw.Draw(img); ink = (245, 245, 247) if dark else (14, 14, 18); dim = (150, 150, 156) if not dark else (170, 170, 176)
    f = ImageFont.truetype(FONT, 51)
    try: f.set_variation_by_axes([600])
    except Exception: pass
    cy = 88; d.text((W * 0.175, cy), '9:41', font=f, fill=ink, anchor='mm')
    _icons(d, W - 66, cy, 3, ink, dim)
    hw = 405; H = img.height
    d.rounded_rectangle((W / 2 - hw / 2, H - 38, W / 2 + hw / 2, H - 23), radius=8, fill=ink if not dark else (235, 235, 240))
    return img

def tablet_screen(app_png, dark):
    """iPad status bar (24 pt) above the real app capture + home indicator. @2x."""
    app = Image.open(app_png).convert('RGB'); W = app.width; SB = 48
    top = app.getpixel((W // 2, 3))
    img = Image.new('RGB', (W, app.height + SB), top); img.paste(app, (0, SB))
    d = ImageDraw.Draw(img); ink = (245, 245, 247) if dark else (14, 14, 18); dim = (150, 150, 156)
    f = ImageFont.truetype(FONT, 27)
    try: f.set_variation_by_axes([600])
    except Exception: pass
    cy = 25; d.text((40, cy), '9:41  Mon 2 Nov', font=f, fill=ink, anchor='lm')
    _icons(d, W - 36, cy, 2, ink, dim, signal=False)
    hw = 640; H = img.height
    d.rounded_rectangle((W / 2 - hw / 2, H - 22, W / 2 + hw / 2, H - 12), radius=5, fill=ink)
    return img

def composite(bg, k, comps, quads, screens, pads):
    H, W = bg.shape[:2]
    out = bg.astype(np.float32)
    b, g, r = [bg[:, :, i].astype(np.float32) for i in range(3)]
    mask_all = np.zeros((H, W), np.float32)
    for m, q, scr, pad in zip(comps, quads, screens, pads):
        s = cv2.cvtColor(np.asarray(scr), cv2.COLOR_RGB2BGR); h, w = s.shape[:2]
        cen = q.mean(0); qq = cen + (q - cen) * (1 + pad / np.linalg.norm(q - cen, axis=1, keepdims=True))
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(qq))
        warp = cv2.warpPerspective(s, M, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        near = ndimage.binary_dilation(m, iterations=6)
        a = (cv2.GaussianBlur(k, (0, 0), 0.8) * near)
        spill = np.minimum(g, np.maximum(r, b))
        out[:, :, 1] = np.where(near & (k < 0.5), spill, out[:, :, 1])
        # glass: soft diagonal reflection + faint top sheen, screens only
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        x0, y0 = qq[:, 0].min(), qq[:, 1].min(); x1, y1 = qq[:, 0].max(), qq[:, 1].max()
        u = ((xx - x0) / max(1, x1 - x0) + (yy - y0) / max(1, y1 - y0)) / 2
        refl = np.clip(1 - u / 0.55, 0, 1) ** 2 * 26
        warp = warp + refl[..., None]
        out = out * (1 - a[..., None]) + warp * a[..., None]
        mask_all = np.maximum(mask_all, a)
    return np.clip(out, 0, 255).astype(np.uint8), mask_all

def place(img, mask, CW, CH, ox, oy, grain=3.0, seed=7):
    H, W = img.shape[:2]
    padL, padR = max(0, ox), max(0, CW - (ox + W)); padT, padB = max(0, oy), max(0, CH - (oy + H))
    ext = cv2.copyMakeBorder(img, padT, padB, padL, padR, cv2.BORDER_REPLICATE)
    me = cv2.copyMakeBorder(mask, padT, padB, padL, padR, cv2.BORDER_CONSTANT, value=0)
    if padL or padR or padT or padB:
        blur = cv2.GaussianBlur(ext, (0, 0), 40)
        wm = np.zeros(ext.shape[:2], np.float32); wm[padT:padT + H, padL:padL + W] = 1
        wm = cv2.GaussianBlur(wm, (0, 0), 25); wm[padT + 60:padT + H - 60, padL + 60:padL + W - 60] = 1
        ext = (ext * wm[..., None] + blur * (1 - wm[..., None])).astype(np.uint8)
    x0, y0 = max(0, -ox), max(0, -oy)
    c = ext[y0:y0 + CH, x0:x0 + CW]; mm = me[y0:y0 + CH, x0:x0 + CW]
    gr = np.random.default_rng(seed).normal(0, grain, (CH, CW)).astype(np.float32)
    return np.clip(c.astype(np.float32) + (gr * (1 - mm))[..., None], 0, 255).astype(np.uint8)
