"""Start Here PDF: python3 guide/make_guide.py → ../1-SELL-THIS/Brief-to-Approved-Start-Here.pdf
Run after build.py. Dark navy + gold KaelLabs layout, clickable online link (no QR), fresh app screenshot, embedded fonts."""
import base64, pathlib, os, re
from playwright.sync_api import sync_playwright
W = pathlib.Path(__file__).resolve().parent; SRC = W.parent; SELL = SRC.parent / '1-SELL-THIS'
NM = SRC / 'node_modules'
ONLINE = 'https://social-media-client-studio-2-online.vercel.app'
VERSION = re.search(r"VERSION = '([^']+)'", (SRC / 'build.py').read_text()).group(1)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
face = lambda fam, w, p, s='normal': f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{s};src:url(data:font/woff2;base64,{b64(NM/p)}) format('woff2')}}"
fonts = (face('Inter Variable', '100 900', '@fontsource-variable/inter/files/inter-latin-wght-normal.woff2') +
         face('Newsreader', '400', '@fontsource/newsreader/files/newsreader-latin-400-normal.woff2'))
KMARK = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800"><rect width="800" height="800" fill="#f5f0e8"/>'
         '<polygon points="216,104 305,104 305,697 216,697" fill="#0e1e3f"/><polygon points="305,340 305,463 527,650 580,587 340,395" fill="#0e1e3f"/>'
         '<polygon points="267,369 527,149 580,212 320,431" fill="#c8a862"/></svg>')
app = SELL / 'Brief-to-Approved.html'
out = SELL / 'Brief-to-Approved-Start-Here.pdf'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('PW_CHROMIUM') or None)
    pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=1.5, color_scheme='light')
    pg.goto(app.as_uri() + '#overview'); pg.wait_for_timeout(700)
    shot = pg.screenshot(type='jpeg', quality=86); pg.close()
    html = ((W / 'start-here.html').read_text()
            .replace('/*FONTS*/', fonts)
            .replace('__SHOT__', 'data:image/jpeg;base64,' + base64.b64encode(shot).decode())
            .replace('__MARK__', 'data:image/svg+xml;base64,' + b64(SRC / 'brand/out/bta-mark.svg'))
            .replace('__KMARK__', 'data:image/svg+xml;base64,' + base64.b64encode(KMARK.encode()).decode())
            .replace('__URLTEXT__', ONLINE.replace('https://', ''))
            .replace('__URL__', ONLINE)
            .replace('__VERSION__', VERSION))
    tmp = SELL / '.start-here.tmp.html'; tmp.write_text(html)
    pg = b.new_page(color_scheme='dark'); pg.goto(tmp.as_uri()); pg.wait_for_timeout(500)
    pg.pdf(path=str(out), format='A4', print_background=True, prefer_css_page_size=True)
    tmp.unlink(); b.close()
print('guide →', out)
