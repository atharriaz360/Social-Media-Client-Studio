"""Pack the Etsy deliverable: python3 pack.py -> ../Brief-to-Approved-v<VERSION>.zip (contents of 1-SELL-THIS). Run build first."""
import pathlib, zipfile, re
W = pathlib.Path(__file__).resolve().parent
VERSION = re.search(r"VERSION = '([^']+)'", (W / 'build.py').read_text()).group(1)
SELL = W.parent / '1-SELL-THIS'
out = W.parent / f'Brief-to-Approved-v{VERSION}.zip'
for old in W.parent.glob('Brief-to-Approved-v*.zip'): old.unlink()
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in sorted(SELL.rglob('*')):
        if f.is_file() and not f.name.startswith('.'): z.write(f, 'Brief-to-Approved/' + str(f.relative_to(SELL)))
print('packed', out.name, out.stat().st_size // 1024, 'KB')
