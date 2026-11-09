"""Pack the Etsy deliverable: python3 pack.py -> ../1-SELL-THIS/Brief-to-Approved-Digital-Download.zip
Run build.py and guide/make_guide.py first. Replaces the previous ZIP; verifies every entry byte for byte."""
import pathlib, zipfile
W = pathlib.Path(__file__).resolve().parent
SELL = W.parent / '1-SELL-THIS'
NAME = 'Brief-to-Approved-Digital-Download.zip'
FILES = ['Brief-to-Approved.html', 'Brief-to-Approved-Start-Here.pdf', 'LICENSE.txt',
         'Documents/Client-Documents.pdf', 'Documents/Visual-Field-Guide.pdf',
         'Documents/Editable-Documents.html', 'Documents/Spreadsheet-Companion.xlsx']
for old in list(W.parent.glob('Brief-to-Approved-v*.zip')) + list(SELL.glob('*.zip')): old.unlink()
out = SELL / NAME; tmp = SELL / (NAME + '.tmp')
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in FILES: z.write(SELL / f, f)
with zipfile.ZipFile(tmp) as z:
    assert z.testzip() is None and sorted(z.namelist()) == sorted(FILES)
    for f in FILES: assert z.read(f) == (SELL / f).read_bytes(), f
tmp.replace(out)
mb = out.stat().st_size / 1e6
assert mb < 20, 'Etsy limit is 20 MB per file'
print('packed', out.name, f'{mb:.2f} MB,', len(FILES), 'files, byte-verified')
