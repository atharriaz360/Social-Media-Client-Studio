"""Package tested buyer files; verify every archive entry against its source."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import re
ROOT = Path(__file__).resolve().parent.parent
SELL = ROOT / '1-SELL-THIS'
DOCS = sorted(p.relative_to(SELL).as_posix() for p in (SELL / 'Documents').rglob('*') if p.is_file() and p.name != '.DS_Store')
FILES = ('Brief-to-Approved.html', 'Brief-to-Approved-Start-Here.pdf', 'LICENSE.txt', *DOCS)
html = (SELL / FILES[0]).read_text()
version = re.search(r"VERSION = '([^']+)'", (ROOT / '5-SOURCE/build.py').read_text()).group(1)
assert f'v{version}' in html, 'Rebuild before packaging'
for name in FILES:
    assert (SELL / name).stat().st_size > 0, f'Missing or empty: {name}'
target = SELL / 'Brief-to-Approved-Digital-Download.zip'
temporary = target.with_suffix('.tmp')
try:
    with ZipFile(temporary, 'w', ZIP_DEFLATED) as archive:
        for name in FILES:
            archive.write(SELL / name, name)
    with ZipFile(temporary) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(FILES)
        for name in FILES:
            assert archive.read(name) == (SELL / name).read_bytes(), name
    temporary.replace(target)
finally:
    temporary.unlink(missing_ok=True)
print(f'Packed and byte-verified: {target} ({len(FILES)} files)')
