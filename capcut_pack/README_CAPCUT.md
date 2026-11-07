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
| `06_ELEMENTS_WHERE_WHEN/` | The three *Where & When* elements (heading, location card, time card), one transparent video each | Edit or move each element separately |
| `04_AUDIO/` | `A1_music_bed.wav` (music), `A2_sfx_all_placed.wav` (**all SFX already at the right times**, 35.4 s), `sfx_individual/` (single SFX files) | Audio tracks |
| `05_CAPTIONS/` | `captions.srt`, every on-screen line | If you want to retype the text in CapCut's own fonts |

---

## 06_ELEMENTS_WHERE_WHEN: info elements as separate videos

The three graphics from the *Where & When* scene are also exported **one per file**, so you can
move, resize, retime or reuse each one on its own in CapCut.

| File | Element | Length | Original start |
|---|---|---|---|
| `A_where_when_title.mov` | "WHERE & WHEN" heading (gold) | 4.6 s | 00:26.0 |
| `B_location_card.mov` | Pin card: Perpustakaan Tun Abdul Razak, Kampus Samarahan 2 | 4.4 s | 00:26.2 |
| `C_time_card.mov` | Clock card: 2 – 5 PM, Library Week | 3.9 s | 00:26.7 |

- `.mov` = transparent (CapCut PC/Mac). `_green.mp4` = green background, for Chroma Key on CapCut mobile.
- Each file is 1920×1080 and the element sits **in its original position**, so placing them on
  three overlay tracks at the starts above gives exactly the original scene. Drag the element in
  the preview to move it wherever you like.
- Each one already has its slide-in animation and fade-out built in.
- If you use these three, **don't** also use `03_…/11_where_when.mov`, or the elements will show twice.

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
