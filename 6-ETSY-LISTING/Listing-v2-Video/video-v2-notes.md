# Social Media Client Studio: listing video v2 (open loops → closed)
Built 2026-10-29 with MASTER-ETSY-VIDEO-PROMPT-v5.
File: `11-Video-Open-Loops-v2.mp4`. The old `Listing-v1/Listing-Video-14s.mp4` is untouched.

## Auto-decide
| Item | Decision | Label |
|---|---|---|
| Product name | Social Media Client Studio (same as hero headline) | VERIFIED from 01-Hero.jpg |
| Buyer | Freelance social media managers | VERIFIED from hero kicker / README |
| Archetype | Pro workflow | INFERENCE |
| Pain | "Approvals lost in DMs?" | INFERENCE (buyer-voice copy, not a claim) |
| Steps | Client brief → Review checks → Approvals → Reports | VERIFIED: the app's own pipeline and nav |
| Hero moment | Approvals donut 33% → 67%, then Reports KPIs | VERIFIED (real states in the capture) |
| Proof+ | Real theme switch (avatar menu → "Switch theme") on desktop, then on phone | VERIFIED: the `#theme` button exists; real toast "Theme: dark" |
| Payoff | Cross-fade to listing photo 1. Its 3 chips pulse (Instant download · No subscription · Light & dark mode) | VERIFIED: the chips are already on the hero |

## Chips (12) → steps
- Step 1 (Brief): brief in emails · brand voice? · the offer?
- Step 2 (Checks): facts checked? · photo rights? · caption v3?
- Step 3 (Approvals): Avery's yes? · approved in DMs? · which version?
- Step 4 (Reports): report due Fri · what got saves? · reach numbers?

"Avery" is the app's own fictional demo approver. Counter: 12 → 9 → 6 → 3 → 0, one step per chip landing. 12 − 3×4 = 0. VERIFIED.

## Real screens (from `1-SELL-THIS/Brief-to-Approved.html`, fictional demo data, Playwright 1440×936 @2x and 393×852 @3x)
| Time (s) | Laptop screen file | Real action |
|---|---|---|
| 0.0 | d-ov0 | Overview, demo start ("Check facts and rights…", Approved 1/3) |
| 2.0 | d-brief | Client brief, 10/10 |
| 3.85 | d-edit0 | Editor for P001 opened via "Run checks" |
| 4.5 | d-edit1 | "Facts checked" toggled on |
| 5.15 | d-ov1 | Saved. Real toast "Saved." |
| 6.0–6.6 | d-appr0, d-apprt1–6 | Record decision dialog, evidence typed: "Email from Avery · v1 approved" |
| 7.1 | d-ov2 | Real toast "Approved · version 1", donut 67%, Approved now 2/3 |
| 8.05 | d-rep | Reports (fictional practice figures, labelled in the app) |
| 10.05–11.25 | d-ov2clean → d-menu → d-dark → d-darkclean | Avatar menu → Switch theme → dark. Real toast "Theme: dark" |

The phone shows p-ov0 until 10.85 s, then switches to dark (p-dark, p-darkclean) through its own menu. The phone never mirrors laptop actions, so the video does not suggest cross-device sync (the app stores data per browser).

Device photo: `5-SOURCE/_Canva-BG/7.jpg` (green screen), chroma-keyed. Screens are perspective-warped into the green area. Film grain sits on the photo only, not on the screens.

## QA (results from checks actually run)
- ffprobe: 14.500 s, 1440×1080, 30/1 fps, 435 frames, H.264 High, yuv420p, 0 audio streams, 10.66 MB. moov before mdat (faststart). VERIFIED.
- 16-frame contact sheet and 4:5 centre crop checked. Headlines and counter stay inside x 288–1152 after an auto-fit to 770 px. Chips and the phone sit partly outside the crop on purpose (they are atmosphere). VERIFIED by viewing.
- Bottom-right 15%: empty on the hook and the steps. The hero's phone stays above y 918. VERIFIED by viewing.
- Frame 0 at 300 px wide: product name, "Approvals lost in DMs?" and "12 open" are readable. The chips read as clutter. VERIFIED by viewing.
- Caption times on screen (in → out, s): c0 0–1.92 · c1 1.85–3.97 · c2 3.85–5.97 · c3 5.85–7.97 · c4 7.85–10.12 · c5 10.0–11.92.
  Fully opaque time is 1.5–1.85 s. c5 is fully opaque for about 1.5 s, under the 1.6 s target.
- Frames at 0 / 3 / 6 / 10 s:
  - 0 s: messy laptop and phone with 12 worry chips. "Approvals lost in DMs?"
  - 3 s: push-in on the real client brief, a tick lands, 9 open.
  - 6 s: approval step starts, 6 open.
  - 10 s: Reports shown, 0 open, warm light.
  Together these give what it is, who it's for, and what changed. INFERENCE (my reading).

## Deviations from the prompt (be aware)
- Chip text is 36 px, not 44. Twelve chips at 44 px would cover the laptop. INFERENCE trade-off.
- The step kicker is 30 px (small caps label). Headlines are 76–84 px and sub-lines 40 px, under the 44 px rule.
- No separate payoff line. Photo 1 already carries the product name, the tagline and the 3 chips, so nothing was added on top of it.
- Plate 7 is upscaled 1.14× (and up to about 1.5× during push-ins). The device photo is slightly soft when zoomed in. The screens stay sharp.

## Not verified
- Etsy may crop or trim the video in some views. UNKNOWN.
- Conversion impact. UNKNOWN until Etsy stats arrive. Compare against Listing-Video-14s.mp4 over the same period.

## Rebuild
Unzip video-v2-source.zip, copy `Brief-to-Approved.html` → `app.html` and `01-Hero.jpg` → resized `hero1440.jpg` (1440×1080).
Then: `node cap2.js` (screens) → `node rend.js` (MP4).
