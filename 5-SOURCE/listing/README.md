# Listing image + video source
Real app screens are captured fresh with Playwright at true device sizes (iPhone 15 Pro 393×852 pt @3x, iPad Air 11" 1180×820 pt @2x, MacBook Pro 14" 1512×982 pt @2x), then perspective-warped into the green-screen photos in `5-SOURCE/_Canva-BG/`. The warp does the foreshortening, so nothing is stretched.
- `capture.py`: screenshots of `1-SELL-THIS/Brief-to-Approved.html` per route/theme/size.
- `comp.py`: chroma key, edge-fitted screen corners, iOS/iPadOS status bars (9:41, signal, Wi-Fi, battery) + home indicator, notch band on MacBook, glass reflection, film grain on background only.
- `specs.py` + `build.py`: which photo, scale, offset and screens per image (`python3 build.py 06-Phone`).
- `overlay.py`: headline/bullets layer for 03, 05, 06, 10. `hero.html` + `render.py`: 01-Hero.
- `video.py`: Listing-Video.mp4.
Scripts use build-workspace paths at the top (R, F, V, BG, APP); point them at this project before re-running.
