"""Build the CapCut transfer pack from the HyperFrames project.

    python3 teaser/tools/build_capcut_pack.py

Reads teaser/index.html (the single source of truth for timing) and writes
capcut_pack/ next to the teaser folder:

  01_FOOTAGE_CLIPS/   each shot trimmed to its exact in/out, upright, 1920x1080, numbered in order
  04_AUDIO/           music bed, all SFX pre-placed on one 35.4 s track, and the single SFX files
  05_CAPTIONS/        captions.srt with every on-screen line, for retyping or editing in CapCut
  TIMELINE.csv        every element with its start, end and track

The rendered layers (02 base footage with motion, 03 graphics overlay with alpha, 00 reference)
come from `npx hyperframes render` and are encoded by encode_overlays.sh.
"""
import csv
import pathlib
import re
import subprocess
import wave

import numpy as np

TEASER = pathlib.Path(__file__).resolve().parent.parent
PACK = TEASER.parent / "capcut_pack"
SR = 48000
TOTAL = 35.4

SHOTS = [  # (id, label, video element id) — order on the timeline
    ("01", "hook_manuscript", "v-hook"),
    ("02", "peek_bookshelf", "v-peek"),
    ("03", "notice_poster", "v-notice"),
    ("04", "poster_zoom", "v-poster"),
    ("06", "stairs", "v-stairs"),
    ("07", "explore_aisle", "v-aisle"),
    ("08", "discover_pick_book", "v-pick"),
    ("09", "getlost_page_flip", "v-flip"),
    ("10", "uncover_manuscript", "v-history"),
    ("11", "where_when_walk", "v-walk"),
]

CAPTIONS = [  # (start, end, text) — mirrors the on-screen text in index.html
    (0.30, 2.70, "Every page hides a story…"),
    (3.30, 5.15, "Psst…"),
    (3.55, 5.10, "The library has a secret."),
    (5.55, 7.50, "Have you seen it yet?"),
    (10.40, 13.60, "LIBRARY WEEK — Beyond the Pages:"),
    (14.15, 15.90, "Step inside the story."),
    (16.25, 18.35, "EXPLORE — every shelf"),
    (18.65, 20.75, "DISCOVER — your next favourite read"),
    (21.05, 23.15, "GET LOST — in a good story"),
    (23.45, 25.55, "UNCOVER — centuries of history"),
    (26.00, 30.15, "WHERE & WHEN"),
    (26.20, 30.15, "Perpustakaan Tun Abdul Razak, Kampus Samarahan 2"),
    (26.70, 30.15, "2 – 5 PM · Library Week"),
    (30.70, 34.60, "Turn the page with us."),
    (31.00, 34.60, "Beyond the Pages · LIBRARY WEEK"),
    (31.90, 34.60, "SEE YOU THERE"),
]


def attrs(tag):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))


def ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def read_wav(path):
    with wave.open(str(path)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels())


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    html = (TEASER / "index.html").read_text()
    videos = {attrs(t)["id"]: attrs(t) for t in re.findall(r"<video\b[^>]*>", html)}
    audios = [attrs(t) for t in re.findall(r"<audio\b[^>]*>", html)]

    for d in ["01_FOOTAGE_CLIPS", "04_AUDIO/sfx_individual", "05_CAPTIONS"]:
        (PACK / d).mkdir(parents=True, exist_ok=True)

    rows = []
    # ---- footage clips: exact trims, upright, 1920x1080 30 fps, no audio (source audio is only hiss)
    for num, label, vid in SHOTS:
        v = videos[vid]
        start, dur, mstart = float(v["data-start"]), float(v["data-duration"]), float(v["data-media-start"])
        out = PACK / "01_FOOTAGE_CLIPS" / f"{num}_{label}.mp4"
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-ss", f"{mstart}", "-i", str(TEASER / v["src"]), "-t", f"{dur}",
            "-vf", "scale=1920:1080:flags=lanczos,fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "16",
            "-preset", "medium", "-an", "-movflags", "+faststart", str(out)], check=True)
        rows.append([f"{start:.2f}", f"{start + dur:.2f}", f"{dur:.2f}", "Video 1 (main)", f"01_FOOTAGE_CLIPS/{out.name}",
                     f"source {pathlib.Path(v['src']).name} {mstart:.2f}-{mstart + dur:.2f}s"])
        print("clip", out.name)
    rows.append(["10.20", "13.80", "3.60", "Video 1 (main)", "01_FOOTAGE_CLIPS/05_title_card_background.mp4", "title card background (text is on overlay 05)"])
    rows.append(["30.60", "35.40", "4.80", "Video 1 (main)", "01_FOOTAGE_CLIPS/12_end_card_background.mp4", "end card background (text is on overlay 12)"])

    # ---- audio: music + every SFX mixed onto one full-length track at its exact time and volume
    sfx_mix = np.zeros((int(TOTAL * SR), 2), dtype=np.float32)
    for a in audios:
        src = TEASER / a["src"]
        start, vol = float(a["data-start"]), float(a.get("data-volume", 1))
        name = pathlib.Path(a["src"]).name
        if name == "music_bed.wav":
            subprocess.run(["cp", str(src), str(PACK / "04_AUDIO" / "A1_music_bed.wav")], check=True)
            rows.append(["0.00", f"{TOTAL:.2f}", f"{TOTAL:.2f}", "Audio 1 (music)", "04_AUDIO/A1_music_bed.wav", f"volume {vol}"])
            continue
        x = read_wav(src) * vol
        i = int(start * SR)
        j = min(len(sfx_mix), i + len(x))
        sfx_mix[i:j] += x[: j - i]
        subprocess.run(["cp", str(src), str(PACK / "04_AUDIO" / "sfx_individual" / name)], check=True)
        rows.append([f"{start:.2f}", f"{start + len(x) / SR:.2f}", f"{len(x) / SR:.2f}", "Audio 2 (sfx)",
                     f"04_AUDIO/sfx_individual/{name}", f"volume {vol}"])
    write_wav(PACK / "04_AUDIO" / "A2_sfx_all_placed.wav", sfx_mix)

    # ---- captions
    with open(PACK / "05_CAPTIONS" / "captions.srt", "w") as f:
        for k, (s, e, t) in enumerate(CAPTIONS, 1):
            f.write(f"{k}\n{ts(s)} --> {ts(e)}\n{t}\n\n")
            rows.append([f"{s:.2f}", f"{e:.2f}", f"{e - s:.2f}", "Text (optional)", "05_CAPTIONS/captions.srt", t])

    for n, label, s0, d in [("01","hook",0,3.0),("02","peek",3.0,2.4),("03","notice",5.4,2.4),("04","poster_flash",7.8,2.4),
                            ("05","title_card",10.2,3.6),("06","page_wipe_stairs",13.8,2.4),("07","explore",16.2,2.4),
                            ("08","discover",18.6,2.4),("09","get_lost",21.0,2.4),("10","uncover",23.4,2.4),
                            ("11","where_when",25.8,4.8),("12","end_card",30.6,4.8)]:
        rows.append([f"{s0:.2f}", f"{s0 + d:.2f}", f"{d:.2f}", "Video 2 (overlay)",
                     f"03_GRAPHICS_OVERLAY_ALPHA/{n}_{label}.mov", "transparent graphics; mobile: 03b green + Chroma Key"])
    rows.sort(key=lambda r: (float(r[0]), r[3]))
    with open(PACK / "TIMELINE.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start_s", "end_s", "duration_s", "track", "file", "notes"])
        w.writerows(rows)
    print("done:", PACK)


if __name__ == "__main__":
    main()
