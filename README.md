# brief to approved. Client Studio: v4.0

Social media manager planner app: client brief, content plan, versioned approvals and reports. Offline single HTML file. Sold on Etsy by KaelLabs.

| Folder | What it's for |
|---|---|
| `1-SELL-THIS/` | Upload `Brief-to-Approved-Digital-Download.zip` to Etsy as the digital file. It contains the app, `Brief-to-Approved-Start-Here.pdf`, `LICENSE.txt` and `Documents/`. |
| `2-HOST-ONLINE/` | Buyer's online/phone version (installable, saves on the device). Live at https://social-media-client-studio-2-online.vercel.app (linked in the Start Here PDF). |
| `3-HOST-DEMO/` | Optional live demo (fictional client, nothing saved). |
| `4-BRAND/` | Logo, mark and app icons. |
| `5-SOURCE/` | App source, tests, Start Here generator (`guide/`), listing image/video scripts (`listing/`). See `5-SOURCE/README-DEV.md`. |
| `6-ETSY-LISTING/` | `Listing/`: 10 photos in upload order + `Listing-Video.mp4`. `Etsy-Listing-Kit.md`: title, 13 tags, alt text, description. `_Screens-Latest/`: real app screenshots used by the images. |

## Rebuild everything

```
cd 5-SOURCE
npm install
npm run build && npm test && npm run test:release
python3 guide/make_guide.py        # Start Here PDF
npm run pack                       # ZIP, byte-verified
```
