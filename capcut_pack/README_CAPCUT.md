# Beyond the Pages: CapCut pack

Every element of the teaser (35.4 s, 1920×1080, 30 fps) is split out so you can rebuild it or keep
editing in CapCut. Timing for every element is in **`TIMELINE.csv`**.

## Downloading the pack in parts

The pack is split into several `partNN_of_NN.zip` files so the downloads don't get cut off.
Download **every part**, then for each zip: right-click → **Extract All…** → pick the same
folder (for example `Downloads`). They all extract into **one** folder, `capcut_pack`. If
Windows asks to replace `README_CAPCUT.md` / `TIMELINE.csv`, click **Replace**, since the copies
are identical.

## Folders

| Folder | Contents | Use for |
|---|---|---|
| `00_REFERENCE/` | `reference_preview_720p.mp4`, the finished teaser | Check that your CapCut version matches |
| `01_FOOTAGE_CLIPS/` | 12 clips, already trimmed, upright, numbered in order (01–12). No zoom, no text | **Route B**: main track you can edit yourself |
| `02_BASE_FOOTAGE_WITH_MOTION/` | `base_footage_full.mp4`: all footage joined, with zoom/push-in, vignette, shading and the title/end card backgrounds already in, but **no text** | **Route A**: fastest |
| `03_GRAPHICS_OVERLAY_ALPHA/` | 10 **transparent** `.mov` files plus 2 full-screen `.mp4` cards (05, 12) (ProRes 4444 + alpha): all text, animation, title, sparkles, page-turn wipe, flash, info cards, end card | Overlay track (CapCut **desktop / PC / Mac**) |
| `03b_GRAPHICS_GREENSCREEN/` | The same 12 overlays on a green background | Overlay track in CapCut **mobile** (use Chroma Key) |
| `07_ELEMENTS_SEPARATE/` | **Every graphic element as its own file** (45 elements: each caption, word, card, icon, sparkle, wipe, shade, background) | Build the teaser over **your own footage** and edit each element separately |
| `04_AUDIO/` | `A1_music_bed.wav` (music), `A2_sfx_all_placed.wav` (**all SFX already at the right times**, 35.4 s), `sfx_individual/` (single SFX files) | Audio tracks |
| `05_CAPTIONS/` | `captions.srt`, every on-screen line | If you want to retype the text in CapCut's own fonts |

---

## 07_ELEMENTS_SEPARATE: every element in its own file

Use this when you want to put the graphics over **your own footage** and edit each one on its own
(move, resize, retime, delete, swap).

- One folder per scene (`01_hook` … `12_end_card`). Files are numbered in the order they appear.
- **`.mov`** = transparent video with the animation built in (CapCut PC/Mac).
  **`green/…_green.mp4`** = the same element on green, for **Chroma Key** in CapCut mobile.
- **`.png`** = static shading layers (vignette, bottom shade, dark shade, left shade). Stretch them
  in CapCut to the scene length.
- **`01_background_navy.mp4`** (title and end card) = ordinary full-screen background.
- Every file is 1920×1080 with the element **in its original position**, so stacked together at
  the times in **`ELEMENTS_TIMELINE.csv`** they rebuild the teaser exactly.

### Track order in CapCut (important)

In CapCut, a **higher** track covers the ones **below** it. So your footage stays on the **main
track (bottom)** and the elements go on the overlay tracks **above** it. For each scene, from
bottom to top:

1. Your footage (main track)
2. Shade / vignette `.png`. This darkens the footage so the text is easier to read
3. Background graphics: dust, glow waves, border frame, sparkles, white flash
4. Text and cards: captions, EXPLORE / DISCOVER…, Psst bubble, location and time cards, button
5. `06_stairs/01_page_turn_wipe_transition` at the very top, so the wipe covers everything

If you put an element **under** the footage, it won't be visible because the footage covers it.

### Start times by scene

| Scene | Start | Contents |
|---|---|---|
| `01_hook` | 00:00.0 | caption, dust, vignette |
| `02_peek` | 00:03.0 | Psst bubble (00:03.3), caption, bottom shade |
| `03_notice` | 00:05.4 | caption, bottom shade |
| `04_poster` | 00:07.8 | vignette, white flash (00:09.9) |
| `05_title` | 00:10.2 | navy bg, glow waves, frame, book icon, LIBRARY WEEK, headline, swoosh, sparkles |
| `06_stairs` | 00:13.4 wipe / 00:13.8 | page-turn wipe, caption, bottom shade |
| `07_explore` | 00:16.2 | EXPLORE, line + subtitle, dark shade |
| `08_discover` | 00:18.6 | DISCOVER, line + subtitle, dark shade |
| `09_get_lost` | 00:21.0 | GET LOST, line + subtitle, dark shade |
| `10_uncover` | 00:23.4 | UNCOVER, line + subtitle, dark shade |
| `11_where_when` | 00:25.8 | left shade, WHERE & WHEN (26.0), location card (26.2), time card (26.7) |
| `12_end_card` | 00:30.6 | navy bg, frame, tagline, logo, LIBRARY WEEK, SEE YOU THERE button, venue line, sparkles |

Exact start and end times for all 45 files are in `ELEMENTS_TIMELINE.csv` (open it in Excel).
Don't use these files together with `03_GRAPHICS_OVERLAY_ALPHA`, or everything will appear twice.

## Route A: fastest, matches the preview exactly (about 5 minutes)

1. CapCut, **New project**, set the ratio to **16:9** and **30 fps**.
2. **Import** everything in `02_`, `03_` (or `03b_` on phone) and `04_`.
3. **Main track (Video 1):** drag `base_footage_full.mp4` to **0:00**.
4. **Overlay track (Video 2):** put the 12 overlay files on the overlay track in number order. Each
   one starts where the previous one ends:

   | File | Start at |
   |---|---|
   | `01_hook` | 00:00.0 |
   | `02_peek` | 00:03.0 |
   | `03_notice` | 00:05.4 |
   | `04_poster_flash` | 00:07.8 |
   | `05_title_card_FULLSCREEN.mp4` | 00:10.2 |
   | `06_page_wipe_stairs` | 00:13.8 |
   | `07_explore` | 00:16.2 |
   | `08_discover` | 00:18.6 |
   | `09_get_lost` | 00:21.0 |
   | `10_uncover` | 00:23.4 |
   | `11_where_when` | 00:25.8 |
   | `12_end_card_FULLSCREEN.mp4` | 00:30.6 |

   Overlays `05` and `12` are **ordinary MP4s that cover the whole screen** (title card and end
   card). They have no transparency and need no Chroma Key.

   Tip: if you drop them in a row with no gaps starting at 0:00, they line up on their own
   because the lengths are already right.
5. **Audio:** drag `A1_music_bed.wav` and `A2_sfx_all_placed.wav` to **0:00** on two audio tracks.
6. Export at 1080p, 30 fps.

## Route B: editable (change shots, add CapCut effects)

1. Main track: drag `01_FOOTAGE_CLIPS/01…12` in order with no gaps. They're already the right
   length, so the total comes to 35.4 s.
2. Overlay track: same as Route A step 4.
3. Audio: same as Route A step 5. If you want to adjust each SFX, use the files in
   `sfx_individual/` and the `Audio 2 (sfx)` times in `TIMELINE.csv` instead of
   `A2_sfx_all_placed.wav`.
4. Optional: add **Keyframe** zooms to each clip, about 100% to 112% across the clip, to get the
   same push-in as the preview. Or use CapCut's Zoom In effect.

## Using the green-screen overlays (CapCut mobile)

Put the `03b_…_green.mp4` file on the overlay track, then tap it and go to **Remove BG →
Chroma Key**. Pick the green colour and set **Intensity about 15–25** and **Shadow about 0–10**.
Thin shadows and blur may look slightly less smooth than the `.mov` version, which is why the
desktop route is the better option.

## Rough music grid

100 BPM, 1 beat = 0.6 s. Scene changes are on the bar (every 2.4 s). The **title drop** lands at
**00:10.2** and the **end card** at **00:30.6**. If you move scenes around, keep the cuts on
multiples of 0.6 s so they stay on the beat.

## Fonts (if you retype the text)

- **Playfair Display** (italic captions, headline), **Cinzel** (EXPLORE / DISCOVER / LIBRARY WEEK),
  **Montserrat** (small info text). All are free Google Fonts and are included in
  `teaser/assets/fonts/` in the repo.
- Colours: navy `#0F1F3D`, poster blue `#2B4F8E`, cream `#F4ECDC`, gold `#E6B85C`.

## Audio levels (as mixed in the preview)

Music 85%. SFX are already balanced inside `A2_sfx_all_placed.wav`, so leave it at 100%. The
original footage audio is muted, since it's only room hiss.
