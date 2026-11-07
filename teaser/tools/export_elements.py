"""Export every graphic element of the teaser as its own video for CapCut.

    cd teaser
    python3 tools/make_layer_files.py        # writes capcut-graphics.html (no footage/audio)
    python3 tools/export_elements.py         # renders + encodes into ../capcut_pack/07_ELEMENTS_SEPARATE

Each element is rendered with a transparent background, in its original position on the
1920x1080 frame, trimmed to its own time window, with its animation built in:
  <scene>/<NN>_<slug>.mov          ProRes 4444 + alpha  (CapCut PC/Mac)
  <scene>/green/<NN>_<slug>.mp4    on pure green        (CapCut mobile, Chroma Key)
Opaque full-screen backgrounds are written as plain .mp4.

Elements whose time windows don't overlap share one render ("batch"), so the whole set
takes about 9 renders instead of 45.
"""
import csv
import pathlib
import subprocess
import sys

TEASER = pathlib.Path(__file__).resolve().parent.parent
OUT = TEASER.parent / "capcut_pack" / "07_ELEMENTS_SEPARATE"
FPS = 30

# (scene folder, file slug, CSS selectors shown, start s, end s, kind)
#   kind: "alpha" = transparent graphic, "shade" = static semi-transparent darkening layer (PNG still),
#         "opaque" = full-screen background
E = [
    ("01_hook", "01_caption_every_page_hides_a_story", "#cap-hook", 0.2, 3.0, "alpha"),
    ("01_hook", "02_dust_particles", "#motes", 0.0, 3.0, "alpha"),
    ("01_hook", "03_vignette_dark_edges", '.grade-vignette[data-start="0"]', 0.0, 3.0, "shade"),
    ("02_peek", "01_psst_speech_bubble", "#psst", 3.3, 5.4, "alpha"),
    ("02_peek", "02_caption_the_library_has_a_secret", "#cap-peek", 3.0, 5.4, "alpha"),
    ("02_peek", "03_bottom_shade", '.shade-bottom[data-start="3.0"]', 3.0, 5.4, "shade"),
    ("03_notice", "01_caption_have_you_seen_it_yet", "#cap-notice", 5.4, 7.8, "alpha"),
    ("03_notice", "02_bottom_shade", '.shade-bottom[data-start="5.4"]', 5.4, 7.8, "shade"),
    ("04_poster", "01_vignette_dark_edges", '.grade-vignette[data-start="7.8"]', 7.8, 10.2, "shade"),
    ("04_poster", "02_white_flash", "#flash", 9.9, 10.6, "alpha"),
    ("05_title", "01_background_navy", '.title-bg[data-start="10.2"]', 10.2, 13.8, "opaque"),
    ("05_title", "02_glow_waves", "#wave1, #wave2", 10.2, 13.8, "alpha"),
    ("05_title", "03_border_frame", "#frame1, #frame2", 10.2, 13.8, "alpha"),
    ("05_title", "04_book_icon", "#title .book-icon", 10.2, 13.8, "alpha"),
    ("05_title", "05_library_week_label", "#title .kicker-row", 10.2, 13.8, "alpha"),
    ("05_title", "06_headline_beyond_the_pages", "#hl1, #hl2", 10.2, 13.8, "alpha"),
    ("05_title", "07_underline_swoosh", "#title .swoosh", 10.2, 13.8, "alpha"),
    ("05_title", "08_sparkles", "#sp1, #sp2, #sp3, #sp4", 10.2, 13.8, "alpha"),
    ("06_stairs", "01_page_turn_wipe_transition", "#wipe", 13.4, 14.25, "alpha"),
    ("06_stairs", "02_caption_step_inside_the_story", "#cap-stairs", 13.8, 16.2, "alpha"),
    ("06_stairs", "03_bottom_shade", '.shade-bottom[data-start="13.8"]', 13.8, 16.2, "shade"),
    ("07_explore", "01_word_EXPLORE", "#k-explore .big", 16.2, 18.6, "alpha"),
    ("07_explore", "02_line_and_subtitle_every_shelf", "#k-explore .rule, #k-explore .sub", 16.2, 18.6, "alpha"),
    ("07_explore", "03_dark_shade", '.shade-full[data-start="16.2"]', 16.2, 18.6, "shade"),
    ("08_discover", "01_word_DISCOVER", "#k-discover .big", 18.6, 21.0, "alpha"),
    ("08_discover", "02_line_and_subtitle_your_next_favourite_read", "#k-discover .rule, #k-discover .sub", 18.6, 21.0, "alpha"),
    ("08_discover", "03_dark_shade", '.shade-full[data-start="18.6"]', 18.6, 21.0, "shade"),
    ("09_get_lost", "01_word_GET_LOST", "#k-lost .big", 21.0, 23.4, "alpha"),
    ("09_get_lost", "02_line_and_subtitle_in_a_good_story", "#k-lost .rule, #k-lost .sub", 21.0, 23.4, "alpha"),
    ("09_get_lost", "03_dark_shade", '.shade-full[data-start="21.0"]', 21.0, 23.4, "shade"),
    ("10_uncover", "01_word_UNCOVER", "#k-uncover .big", 23.4, 25.8, "alpha"),
    ("10_uncover", "02_line_and_subtitle_centuries_of_history", "#k-uncover .rule, #k-uncover .sub", 23.4, 25.8, "alpha"),
    ("10_uncover", "03_dark_shade", '.shade-full[data-start="23.4"]', 23.4, 25.8, "shade"),
    ("11_where_when", "01_title_WHERE_AND_WHEN", "#info-head", 26.0, 30.6, "alpha"),
    ("11_where_when", "02_location_card", "#info-loc", 26.2, 30.6, "alpha"),
    ("11_where_when", "03_time_card", "#info-time", 26.7, 30.6, "alpha"),
    ("11_where_when", "04_left_side_shade", '.shade-bottom[data-start="25.8"]', 25.8, 30.6, "shade"),
    ("12_end_card", "01_background_navy", '.title-bg[data-start="30.6"]', 30.6, 35.4, "opaque"),
    ("12_end_card", "02_border_frame", "#frame3", 30.6, 35.4, "alpha"),
    ("12_end_card", "03_tagline_turn_the_page_with_us", "#end-pre", 30.6, 35.4, "alpha"),
    ("12_end_card", "04_logo_beyond_the_pages", "#end-logo", 30.6, 35.4, "alpha"),
    ("12_end_card", "05_library_week_label", "#end-lw", 30.6, 35.4, "alpha"),
    ("12_end_card", "06_button_SEE_YOU_THERE", "#end-cta", 30.6, 35.4, "alpha"),
    ("12_end_card", "07_venue_and_time_line", "#end-meta", 30.6, 35.4, "alpha"),
    ("12_end_card", "08_sparkles", "#sp5, #sp6", 30.6, 35.4, "alpha"),
]


def batches():
    """Greedy interval colouring: elements in one batch never overlap in time."""
    out = []
    for e in sorted(E, key=lambda e: (e[3], e[4])):
        for b in out:
            if b[-1][4] <= e[3] + 1e-6:
                b.append(e)
                break
        else:
            out.append([e])
    return out


CHILD_OF = {"#hl1": "#title", "#hl2": "#title", "#end-pre": "#end", "#end-logo": "#end",
            "#end-lw": "#end", "#end-cta": "#end", "#end-meta": "#end"}


def split_target(sel):
    """Return (root-level clip selector, child selector or None)."""
    sel = sel.strip()
    if " " in sel:
        clip, child = sel.split(" ", 1)
        return clip, child
    if sel in CHILD_OF:
        return CHILD_OF[sel], sel
    return sel, None


def batch_html(src, group):
    """Show only this batch's elements.

    The runtime hides inactive clips with an inline !important visibility, so we never force
    `visible` on anything: we only hide (a) every root-level clip that holds no target and
    (b) the non-target children inside clips whose target is a child. Targets inherit the
    clip's own visibility, so they still appear only inside their time window.
    """
    clips, children = [], {}
    for e in group:
        for s in e[2].split(", "):
            clip, child = split_target(s)
            if clip not in clips:
                clips.append(clip)
            if child:
                children.setdefault(clip, []).append(child)
    rules = ["#root > *" + "".join(f":not({c})" for c in clips) + " { visibility: hidden !important; }"]
    for clip, kids in children.items():
        rules.append(f"#root > {clip} > *" + "".join(f":not({k})" for k in kids) + " { visibility: hidden !important; }")
    css = "\n      /* show only this batch's elements */\n      " + "\n      ".join(rules) + \
          "\n      html, body, #root { background: transparent !important; }\n    </style>"
    html = src.replace('class="layer-graphics"', 'class="layer-elements"', 1)
    return html.replace("    </style>", css, 1)


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    only_encode = "--encode-only" in sys.argv
    src = (TEASER / "capcut-graphics.html").read_text()
    bs = batches()
    print(f"{len(E)} elements in {len(bs)} renders")
    rows = []
    for i, group in enumerate(bs, 1):
        html = TEASER / f"capcut-batch-{i:02d}.html"
        html.write_text(batch_html(src, group))
        frames = TEASER / "renders" / f"batch_{i:02d}"
        if not only_encode:
            run(["npx", "hyperframes", "render", "-c", html.name, "--format", "png-sequence",
                 "-q", "delivery", "-o", str(frames.relative_to(TEASER))])
        for scene, slug, sels, t0, t1, kind in group:
            d = round(t1 - t0, 3)
            folder = OUT / scene
            (folder / "green").mkdir(parents=True, exist_ok=True)
            inp = ["-framerate", str(FPS), "-start_number", "1", "-i", str(frames / "frame_%06d.png")]
            if kind == "shade":
                # static darkening layer: one transparent PNG still is enough (stretch it in CapCut)
                out = folder / f"{slug}.png"
                mid = int(round((t0 + d / 2) * FPS)) + 1
                run(["cp", str(frames / f"frame_{mid:06d}.png"), str(out)])
                files = [out.name]
            elif kind == "opaque":
                out = folder / f"{slug}.mp4"
                run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inp, "-ss", f"{t0}", "-t", f"{d}",
                     "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "14", "-an", "-movflags", "+faststart", str(out)])
                files = [out.name]
            else:
                out = folder / f"{slug}.mov"
                run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inp, "-ss", f"{t0}", "-t", f"{d}",
                     "-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le", "-alpha_bits", "8",
                     "-qscale:v", "18" if "glow" in slug else "9", "-vendor", "apl0", str(out)])
                files = [out.name]
                if True:
                    g = folder / "green" / f"{slug}_green.mp4"
                    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i",
                         f"color=c=0x00FF00:s=1920x1080:r={FPS}", *inp, "-t", f"{d}", "-filter_complex",
                         f"[1:v]trim=start={t0}:duration={d},setpts=PTS-STARTPTS[g];"
                         "[0:v][g]overlay=format=auto:shortest=1,format=yuv420p",
                         "-c:v", "libx264", "-crf", "14", "-an", "-movflags", "+faststart", str(g)])
                    files.append(f"green/{g.name}")
            rows.append([f"{t0:.2f}", f"{t1:.2f}", f"{d:.2f}", scene, " | ".join(f"{scene}/{f}" for f in files), kind])
            print(f"  {scene}/{slug}  {t0:.2f}-{t1:.2f}s  [{kind}]")
        html.unlink()
    rows.sort(key=lambda r: (float(r[0]), r[3]))
    with open(OUT / "ELEMENTS_TIMELINE.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start_s", "end_s", "duration_s", "scene", "files", "type"])
        w.writerows(rows)
    print("done:", OUT)


if __name__ == "__main__":
    main()
