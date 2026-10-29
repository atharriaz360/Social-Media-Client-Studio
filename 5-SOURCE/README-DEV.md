# brief to approved. Client Studio: developer notes

## Setup (once)

```
npm install
pip install playwright fonttools brotli
```

## Build steps

Run these from inside `5-SOURCE`:

| Command | What it does |
|---|---|
| `python3 brand/make_brand.py` | Logo, mark and app icons into `brand/out/` and `../4-BRAND/` (letters outlined, no fonts needed to view) |
| `python3 build.py` | Writes `../1-SELL-THIS/Brief-to-Approved.html` (+ `LICENSE.txt`, `Documents/`), `../2-HOST-ONLINE/*` (index, manifest, service worker, icons, Documents) and `../3-HOST-DEMO/index.html` |
| `python3 guide/make_guide.py` | Writes the 2-page dark Start Here PDF `../1-SELL-THIS/Brief-to-Approved-Start-Here.pdf` (clickable online link, fresh app screenshot) |

Optional: set `PW_CHROMIUM=/path/to/chrome` to use a specific Chromium for the guide and release test.

## Source layout

- `src/shell.html`: page skeleton (sidebar, top bar, dialogs, command menu, demo bar). Pre-paint theme script in `<head>`.
- `src/styles.css`: all styles. Fonts injected at `/*FONTS*/`, hero art at `__HERO_ART__`.
- `src/app.js`: all logic. `StudioCore` (next step, metrics, revise, validate, demo seed) first, then views, actions, events, init.
- `src/img/`: original SVG art, embedded as data URIs by `build.py` (`ART`).
- `docs/`: buyer documents copied into `Documents/` by the build (PDF guide, client documents, editable HTML, XLSX).
- `listing/`: scripts for the Etsy hero image and listing video (see `listing/README.md`).

## Releasing an update

1. Bump `VERSION` in `build.py` (and `package.json`).
2. `npm run build && npm test && npm run test:release`
3. `python3 guide/make_guide.py` if the overview changed.
4. `npm run pack`, then re-upload to Etsy.

Data key `brief-approved-studio-v2` (schema 2) and UI key `brief-approved-ui-v5` must stay the same.

## Release checks and packaging

`npm test` runs the 18 core checks and the 9-route render check against `src/app.js`.
`npm run test:release` opens the built file in Chromium: single-file check, all routes, escaped input,
approve + revision reset, backup/clear/restore, pre-paint theme, phone width on every route, demo never saves,
no browser errors. Screenshots go to `test-results/`.
`npm run pack` zips the HTML, Start Here PDF, licence and Documents, verifying each entry byte for byte.
