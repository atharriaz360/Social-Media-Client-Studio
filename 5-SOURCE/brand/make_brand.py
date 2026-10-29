"""brief to approved. brand: python3 brand/make_brand.py → brand/out/*.svg + icon PNGs.
Needs: npm install (Newsreader font + playwright), pip install fonttools brotli.
Letters are outlined into paths, so the SVGs need no fonts to view."""
import pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
W = pathlib.Path(__file__).resolve().parent
OUT = W / 'out'; OUT.mkdir(exist_ok=True)
NM = W.parent / 'node_modules'
f = TTFont(NM / '@fontsource/newsreader/files/newsreader-latin-500-normal.woff2')
gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm
def glyph(ch):
    n = cmap[ord(ch)]; pen = SVGPathPen(gs); gs[n].draw(pen); b = BoundsPen(gs); gs[n].draw(b)
    return pen.getCommands(), b.bounds, gs[n].width
def text_path(txt, size, x, baseline):
    out, cx = [], x; s = size / upm
    for ch in txt:
        if ch == ' ': cx += gs[cmap[32]].width * s; continue
        d, _, w = glyph(ch)
        out.append(f'<path transform="translate({cx:.2f} {baseline}) scale({s:.5f} {-s:.5f})" d="{d}"/>'); cx += w * s
    return ''.join(out), cx
GRAD = '<defs><radialGradient id="g" cx=".3" cy=".25" r=".85"><stop offset="0" stop-color="#cbb9f2"/><stop offset=".55" stop-color="#9a82da"/><stop offset="1" stop-color="#7d65c4"/></radialGradient></defs>'
def mark(size=64, pad=0, rx=None, bg=None):
    d, (x0, y0, x1, y1), _ = glyph('B'); c = size / 2; r = c - pad
    s = (r * 1.3) / upm; gw, gh = (x1 - x0) * s, (y1 - y0) * s
    tx, ty = c - gw / 2 - x0 * s, c + gh / 2 + y0 * s
    shape = f'<rect width="{size}" height="{size}" rx="{rx}" fill="url(#g)"/>' if rx is not None else f'<circle cx="{c}" cy="{c}" r="{r}" fill="url(#g)"/>'
    back = f'<rect width="{size}" height="{size}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{GRAD}{back}{shape}<path transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f} {-s:.5f})" d="{d}" fill="#fff"/></svg>'
(OUT / 'bta-mark.svg').write_text(mark(64))
(OUT / 'bta-icon.svg').write_text(mark(64, rx=14))
(OUT / 'bta-icon-maskable.svg').write_text(mark(64, pad=0, rx=0))
def logo(ink, sub):
    body, end = text_path('brief to approved.', 30, 64, 34)
    small, end2 = text_path('Content Studio', 15, 64, 56)
    w = int(max(end, end2) + 6)
    m = mark(48).replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">', '<g transform="translate(0 6)">').replace('</svg>', '</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 64">{m}<g fill="{ink}">{body}</g><g fill="{sub}">{small}</g></svg>'
(OUT / 'bta-logo.svg').write_text(logo('#221e2c', '#6f6879'))
(OUT / 'bta-logo-dark.svg').write_text(logo('#f3effa', '#9c94ad'))
import base64
b64 = lambda q: base64.b64encode(q.read_bytes()).decode()
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    def png(svg, name, px, bg='transparent'):
        pg = b.new_page(viewport={'width': px, 'height': px})
        pg.set_content(f'<html><body style="margin:0;background:{bg}"><img src="data:image/svg+xml;base64,{b64(OUT/svg)}" style="width:{px}px;height:{px}px;display:block"></body></html>')
        pg.screenshot(path=str(OUT / name), omit_background=(bg == 'transparent')); pg.close()
    png('bta-icon.svg', 'icon-180.png', 180, '#FBF8F4'); png('bta-icon.svg', 'icon-192.png', 192); png('bta-icon.svg', 'icon-512.png', 512)
    png('bta-icon-maskable.svg', 'icon-maskable-512.png', 512)
    for name, svg in (('bta-logo.png', 'bta-logo.svg'), ('bta-logo-on-dark.png', 'bta-logo-dark.svg')):
        pg = b.new_page(viewport={'width': 900, 'height': 192}, device_scale_factor=1)
        bg = '#FBF8F4' if 'dark' not in svg else '#121019'
        pg.set_content(f'<html><body style="margin:0;background:{bg};display:grid;place-items:center;height:192px"><img src="data:image/svg+xml;base64,{b64(OUT/svg)}" style="height:128px"></body></html>')
        pg.screenshot(path=str(OUT / name)); pg.close()
    b.close()
import shutil
BR = W.parent.parent / '4-BRAND'; BR.mkdir(exist_ok=True)
for x in OUT.iterdir(): shutil.copy(x, BR / x.name)
print('brand →', sorted(x.name for x in OUT.iterdir()))
