"""Start Here PDF: python3 guide/make_guide.py → ../1-SELL-THIS/Brief-to-Approved-Start-Here.pdf
Run after build.py. Takes a fresh screenshot of the built app, embeds fonts, prints A4 with Chromium."""
import base64, pathlib, os
from playwright.sync_api import sync_playwright
W = pathlib.Path(__file__).resolve().parent; SRC = W.parent; SELL = SRC.parent / '1-SELL-THIS'
NM = SRC / 'node_modules'
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
face = lambda fam, w, p: f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b64(NM/p)}) format('woff2')}}"
fonts = (face('Inter Variable', '100 900', '@fontsource-variable/inter/files/inter-latin-wght-normal.woff2') +
         face('Newsreader', '400', '@fontsource/newsreader/files/newsreader-latin-400-normal.woff2'))
app = SELL / 'Brief-to-Approved.html'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('PW_CHROMIUM') or None)
    pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=1.5, color_scheme='light')
    pg.goto(app.as_uri() + '#overview'); pg.wait_for_timeout(600)
    shot = pg.screenshot(type='jpeg', quality=86); pg.close()
    html = (W / 'start-here.html').read_text().replace('/*FONTS*/', fonts).replace('__SHOT__', 'data:image/jpeg;base64,' + base64.b64encode(shot).decode()).replace('__MARK__', 'data:image/svg+xml;base64,' + b64(SRC / 'brand/out/bta-mark.svg'))
    tmp = SELL / '.start-here.tmp.html'; tmp.write_text(html)
    pg = b.new_page(color_scheme='light'); pg.goto(tmp.as_uri()); pg.wait_for_timeout(400)
    pg.pdf(path=str(SELL / 'Brief-to-Approved-Start-Here.pdf'), format='A4', print_background=True, prefer_css_page_size=True)
    tmp.unlink(); b.close()
print('guide →', SELL / 'Brief-to-Approved-Start-Here.pdf')
