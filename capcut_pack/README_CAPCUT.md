# Beyond the Pages: CapCut pack

Every element of the teaser (35.4 s, 1920×1080, 30 fps) is split out so you can rebuild it or keep
editing in CapCut. Timing for every element is in **`TIMELINE.csv`**.

## Folders

| Folder | Contents | Use for |
|---|---|---|
| `00_REFERENCE/` | `reference_preview_720p.mp4`, the finished teaser | Check that your CapCut version matches |
| `01_FOOTAGE_CLIPS/` | 12 clips, already trimmed, upright, numbered in order (01–12). No zoom, no text | **Route B**: main track you can edit yourself |
| `02_BASE_FOOTAGE_WITH_MOTION/` | `base_footage_full.mp4`: all footage joined, with zoom/push-in, vignette, shading and the title/end card backgrounds already in, but **no text** | **Route A**: fastest |
| `03_GRAPHICS_OVERLAY_ALPHA/` | 12 **transparent** `.mov` files (ProRes 4444 + alpha): all text, animation, title, sparkles, page-turn wipe, flash, info cards, end card | Overlay track (CapCut **desktop / PC / Mac**) |
| `03b_GRAPHICS_GREENSCREEN/` | The same 12 overlays on a green background | Overlay track in CapCut **mobile** (use Chroma Key) |
| `04_AUDIO/` | `A1_music_bed.wav` (music), `A2_sfx_all_placed.wav` (**all SFX already at the right times**, 35.4 s), `sfx_individual/` (single SFX files) | Audio tracks |
| `05_CAPTIONS/` | `captions.srt`, every on-screen line | If you want to retype the text in CapCut's own fonts |

---

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
   | `05_title_card` | 00:10.2 |
   | `06_page_wipe_stairs` | 00:13.8 |
   | `07_explore` | 00:16.2 |
   | `08_discover` | 00:18.6 |
   | `09_get_lost` | 00:21.0 |
   | `10_uncover` | 00:23.4 |
   | `11_where_when` | 00:25.8 |
   | `12_end_card` | 00:30.6 |

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
