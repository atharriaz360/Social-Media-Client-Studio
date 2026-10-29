# brief to approved. Client Studio: v4.0

A private, offline content studio for social media managers (client brief, content plan, versioned approvals, reports). Sold on Etsy by KaelLabs.

| Folder | What it's for |
|---|---|
| `1-SELL-THIS/` | Upload to Etsy as digital files: `Brief-to-Approved-Digital-Download.zip` (contains `Brief-to-Approved.html`, `Brief-to-Approved-Start-Here.pdf`, `LICENSE.txt`, `Documents/`) |
| `2-HOST-ONLINE/` | Drag the whole folder onto app.netlify.com/drop. It becomes the buyer's phone link (installable, works offline). Not deployed yet |
| `3-HOST-DEMO/` | Optional live demo (example client, nothing saved). Drag onto a NEW Netlify site |
| `4-BRAND/` | Logo, mark and app icons |
| `5-SOURCE/` | Source code, tests, guide and brand scripts (see `5-SOURCE/README-DEV.md`) |
| `6-ETSY-LISTING/` | Listing images (10 JPGs + video), `_Review/` sheets, and `Etsy-Listing-Kit.md` (optimized title, 13 tags, image alt text, full description) |
| `_ARCHIVE-2026-10-29-old-listing/` | Old Edition-02 listing images, research, release review. Safe to delete after new listing ships |

## Rebuild everything

```
cd 5-SOURCE
npm install                        # restores node_modules
python3 brand/make_brand.py        # only if the logo changes
npm run build && npm test && npm run test:release
python3 guide/make_guide.py        # Start Here PDF
npm run pack
```

## Before publishing

Old listing images archived 2026-10-29. Read `_ARCHIVE-2026-10-29-old-listing/6-ETSY-LISTING/Release-Review.md` (Etsy AI-instructions rule). Re-run `npm run pack` so the ZIP matches the current build.
