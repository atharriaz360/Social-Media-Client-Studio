# Listing image + video source
All screens are real captures of `1-SELL-THIS/Brief-to-Approved.html` (fictional demo data). Run in this order:
1. `capture_all.py`: 45 screens (desktop light/dark, tablet light, phone light/dark × 9 views) → `6-ETSY-LISTING/_Screens-Latest/`, plus the real interaction states the video uses (Run checks → Facts toggle → "Saved.", Record decision → typed evidence → "Approved · version 1", tablet counter 1/3 → 2/3) with tap coordinates. `--interactions` redoes only those states.
2. `build.py <name>` + `specs.py`: perspective-warps fresh device-size captures into the green-screen photos in `5-SOURCE/_Canva-BG/` (iPhone 15 Pro 393×852 pt @3x, iPad Air 11" 1180×820 pt @2x, MacBook Pro 14" @2x). `comp.py` adds status bars, glass reflection and grain.
3. `overlay.py`: headline layer for 04, 05, 06, 09. `allviews.py`: 02-All-Views (3×3 grid of desktop screens). `hero.html` + `render.py`: 01-Hero.
4. `video.py`: Listing-Video.mp4. 14.6 s, 1440×1080, 30 fps, H.264 High, no audio. Devices are rendered in HTML around the real screens. All text sits in the centre 4:5 zone (x 288–1152), checked on every 6th frame. It ends on the exact 01-Hero.
Scripts use build-workspace paths at the top (R, F, V, BG, APP). Point them at this project before re-running.
