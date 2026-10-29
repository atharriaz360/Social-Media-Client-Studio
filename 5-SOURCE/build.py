"""brief to approved. build: python3 build.py  →  ../1-SELL-THIS/Brief-to-Approved.html (+ LICENSE, Documents),
../2-HOST-ONLINE/* (index, manifest, service worker, icons, Documents) and ../3-HOST-DEMO/index.html.
Needs: npm install (fonts), Python 3.9+. Run brand/make_brand.py first if brand/out is missing."""
import base64, hashlib, json, pathlib, shutil
VERSION = '4.0'
W = pathlib.Path(__file__).resolve().parent
NM = W / 'node_modules'
SELL, HOST, DEMO = W.parent / '1-SELL-THIS', W.parent / '2-HOST-ONLINE', W.parent / '3-HOST-DEMO'
B = W / 'brand' / 'out'
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
face = lambda fam, w, p: f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b64(NM/p)}) format('woff2')}}\n"
fonts = (face('Inter Variable', '100 900', '@fontsource-variable/inter/files/inter-latin-wght-normal.woff2') +
         face('Newsreader', '400', '@fontsource/newsreader/files/newsreader-latin-400-normal.woff2') +
         face('Newsreader', '500', '@fontsource/newsreader/files/newsreader-latin-500-normal.woff2'))
IMG = W / 'src/img'
def svg(n):
    photo = IMG / f'{n}.jpg'
    return 'data:image/jpeg;base64,' + b64(photo) if photo.exists() else 'data:image/svg+xml;base64,' + b64(IMG / f'{n}.svg')
css = (W / 'src/styles.css').read_text().replace('/*FONTS*/', fonts).replace('__HERO_ART__', svg('hero-art'))
art = json.dumps({k: svg(k) for k in ('soup', 'menu', 'coffee', 'studio-art', 'thumb-soup', 'thumb-coffee', 'thumb-menu', 'thumb-approval')})
js = f"const ART={art};\n" + (W / 'src/app.js').read_text().replace('__VERSION__', VERSION)
shell = (W / 'src/shell.html').read_text().replace('__VERSION__', VERSION)
fav = 'data:image/svg+xml;base64,' + b64(B / 'bta-icon.svg')
def page(online, demo=False):
    head = f'<link rel="icon" type="image/svg+xml" href="{fav}">\n'
    head += ('<link rel="manifest" href="manifest.webmanifest">\n<link rel="apple-touch-icon" href="icons/icon-180.png">' if online
             else f'<link rel="apple-touch-icon" href="data:image/png;base64,{b64(B/"icon-180.png")}">')
    return shell.replace('<!--PWA-->', head).replace('/*CSS*/', css).replace('/*JS*/', js.replace("'__DEMO__'", "'1'" if demo else "'0'"))
def docs(dst):
    d = dst / 'Documents'; shutil.rmtree(d, ignore_errors=True); shutil.copytree(W / 'docs', d)
SELL.mkdir(exist_ok=True); DEMO.mkdir(exist_ok=True); (HOST / 'icons').mkdir(parents=True, exist_ok=True)
(SELL / 'Brief-to-Approved.html').write_text(page(False))
(SELL / 'LICENSE.txt').write_text((W / 'LICENSE.txt').read_text().replace('__VERSION__', VERSION))
docs(SELL); docs(HOST); docs(DEMO)
(DEMO / 'index.html').write_text(page(False, True).replace('<title>brief to approved. · Client Studio</title>', '<title>brief to approved. · Live Demo</title>'))
idx = page(True); (HOST / 'index.html').write_text(idx); H = hashlib.sha1(idx.encode()).hexdigest()[:8]
for f in ['icon-180.png', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png']:
    (HOST / 'icons' / f).unlink(missing_ok=True); shutil.copy(B / f, HOST / 'icons' / f)
(HOST / 'manifest.webmanifest').write_text(json.dumps({
    "name": "brief to approved. Client Studio", "short_name": "Client Studio", "id": "./", "start_url": "./", "scope": "./",
    "display": "standalone", "orientation": "any", "background_color": "#FBF8F4", "theme_color": "#FBF8F4",
    "description": "Private, offline content studio: client brief, content plan, versioned approvals and reports.",
    "categories": ["productivity", "business"],
    "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
              {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
              {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, indent=1))
FILES = ['./', './index.html', './manifest.webmanifest', './icons/icon-180.png', './icons/icon-192.png', './icons/icon-512.png', './icons/icon-maskable-512.png']
(HOST / 'sw.js').write_text(f"""// brief to approved. offline cache v{VERSION}
const C='briefapproved-v{VERSION}-{H}';const FILES={json.dumps(FILES)};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(C).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('briefapproved-v')&&x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))}});
self.addEventListener('fetch',e=>{{if(e.request.method!=='GET'||!e.request.url.startsWith(self.location.origin))return;
 e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(hit=>{{const net=fetch(e.request).then(r=>{{if(r&&r.ok){{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp))}}return r}}).catch(()=>hit||caches.match('./index.html'));return hit||net}}))}});
""")
(HOST / '_headers').write_text("/sw.js\n  Cache-Control: no-cache\n/index.html\n  Cache-Control: no-cache\n")
print('built v' + VERSION, (SELL / 'Brief-to-Approved.html').stat().st_size // 1024, 'KB')
