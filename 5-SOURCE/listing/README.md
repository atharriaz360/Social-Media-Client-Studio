# Listing image + video source
All screens are real captures of `1-SELL-THIS/Brief-to-Approved.html` (fictional demo data). Run in this order:
1. `capture_all.py`: 45 screens (desktop light/dark, tablet light, phone light/dark × 9 views) → `6-ETSY-LISTING/_Screens-Latest/`, plus the real interaction states the video uses (Run checks → Facts toggle → "Saved.", Record decision → typed evidence → "Approved · version 1", tablet counter 1/3 → 2/3) with tap coordinates. `--interactions` redoes only those states.
2. `build.py <name>` + `specs.py`: perspective-warps fresh device-size captures into the green-screen photos in `5-SOURCE/_Canva-BG/` (iPhone 15 Pro 393×852 pt @3x, iPad Air 11" 1180×820 pt @2x, MacBook Pro 14" @2x). `comp.py` adds status bars, glass reflection and grain.
3. `overlay.py`: headline layer for 04, 05, 06, 09. `allviews.py`: 02-All-Views (3×3 grid of desktop screens). `hero.py`: 01-Hero on dark plate `_Canva-BG/9.jpg`, HTML MacBook + iPhone around real captures, KaelLabs mark top-right (writes `hero.html`). 07-Client-Brief: `overlay.py` framed screens on plate 8.
4. `video.py`: Listing-Video.mp4. 14.6 s, 1440×1080, 30 fps, H.264 High, no audio. Devices are rendered in HTML around the real screens. All text sits in the centre 4:5 zone (x 288–1152), checked on every 6th frame. It ends on the exact 01-Hero.
Scripts use build-workspace paths at the top (R, F, V, BG, APP). Point them at this project before re-running.


Screen size rule: desktop screens = MacBook Pro 14" M3 (1512 pt wide; `capture_all.py` 1512x945 @2x, 08 unedited 1512x982 @2x). The app font is the macOS system font (-apple-system / SF): install `SFNS.ttf` + `Apple Symbols.ttf` from /System/Library/Fonts into ~/.fonts with fontconfig aliases (SF Pro Text, -apple-system, BlinkMacSystemFont -> System Font) before capturing on Linux, or titles wrap and arrows differ from the Mac.
