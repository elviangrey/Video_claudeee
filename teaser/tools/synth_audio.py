"""Synthesize the original music bed and sound effects for the teaser.

Everything is generated from scratch with numpy (no samples), so the audio is
100% original and deterministic. Run:

    python3 teaser/tools/synth_audio.py teaser/assets/audio

Music: 100 BPM (one beat = 0.6 s, one bar = 2.4 s), A minor, laid out to the
scene grid in index.html (intro -> riser -> drop at 10.2 s -> outro at 30.6 s).
"""

import os
import sys
import wave

import numpy as np

SR = 48000
BPM = 100
BEAT = 60 / BPM          # 0.6 s
BAR = BEAT * 4           # 2.4 s
rng = np.random.default_rng(7)


# ----------------------------------------------------------------- helpers
def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def env_adsr(n, a=0.01, d=0.1, s=0.7, r=0.2):
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    s_n = max(n - a_n - d_n - r_n, 0)
    e = np.concatenate([
        np.linspace(0, 1, a_n, endpoint=False),
        np.linspace(1, s, d_n, endpoint=False),
        np.full(s_n, s),
        np.linspace(s, 0, r_n),
    ])
    return np.pad(e, (0, max(0, n - len(e))))[:n]


def lowpass(x, cutoff):
    """One-pole low-pass; cutoff may be a scalar or per-sample array."""
    cutoff = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def lp_fast(x, cutoff, passes=2):
    """Static-cutoff low-pass via FFT brick-ish rolloff (fast)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** (2 * passes))
    return np.fft.irfft(X, len(x))


def hp_fast(x, cutoff, passes=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    f[0] = 1e-9
    X *= 1 / (1 + (cutoff / f) ** (2 * passes))
    return np.fft.irfft(X, len(x))


def bp_fast(x, lo, hi):
    return hp_fast(lp_fast(x, hi), lo)


def note_hz(name):
    names = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3,
             "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    pitch, octave = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[pitch] + (octave - 4) * 12) / 12)


def saw(freq, t):
    # band-limited-ish saw from additive partials
    out = np.zeros_like(t)
    k = 1
    while k * freq < 9000 and k < 40:
        out += ((-1) ** (k + 1)) * np.sin(2 * np.pi * k * freq * t) / k
        k += 1
    return out * (2 / np.pi)


def add(buf, sig, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


def write_wav(path, x, stereo_width=0.0):
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        if stereo_width:
            d = int(0.011 * SR)
            l = x
            r = np.concatenate([np.zeros(d), x[:-d]]) * (1 - stereo_width) + x * stereo_width
            x = np.stack([l, r], axis=1)
        else:
            x = np.stack([x, x], axis=1)
    peak = np.max(np.abs(x)) or 1
    x = x / peak * 0.89
    pcm = (x * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wrote", path, f"{len(pcm) / SR:.2f}s")


# ------------------------------------------------------------- instruments
def kick(dur=0.45):
    t = t_axis(dur)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7)
    click = rng.standard_normal(len(t)) * np.exp(-t * 300) * 0.25
    return np.tanh((body + click) * 1.6)


def clap(dur=0.3):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    e = np.zeros_like(t)
    for off in (0, 0.011, 0.022):
        e += np.where(t >= off, np.exp(-(t - off) * 60), 0)
    e += np.exp(-t * 14) * 0.5
    return bp_fast(n * e, 900, 5000)


def hat(dur=0.08, open_=False):
    t = t_axis(0.35 if open_ else dur)
    n = rng.standard_normal(len(t))
    return hp_fast(n, 7000) * np.exp(-t * (12 if open_ else 70)) * 0.6


def pluck(freq, dur=0.5, bright=0.5):
    """Karplus-Strong pluck."""
    n = int(dur * SR)
    period = int(SR / freq)
    buf = rng.uniform(-1, 1, period)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % period]
        nxt = buf[(i + 1) % period]
        buf[i % period] = 0.996 * (bright * out[i] + (1 - bright) * 0.5 * (out[i] + nxt))
    return out * env_adsr(n, 0.002, 0.05, 0.8, 0.12)


def pad_chord(notes, dur, cutoff=1800):
    t = t_axis(dur)
    x = np.zeros_like(t)
    for nme in notes:
        f = note_hz(nme)
        for det in (-0.12, 0.0, 0.11):
            x += saw(f * 2 ** (det / 12), t + rng.uniform(0, 0.01))
    x /= len(notes) * 3
    x = lp_fast(x, cutoff)
    return x * env_adsr(len(t), 0.5, 0.3, 0.85, 0.6)


def bell(freq, dur=1.6):
    t = t_axis(dur)
    x = (np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t * 3)
         + 0.25 * np.sin(2 * np.pi * freq * 5.4 * t) * np.exp(-t * 6))
    return x * np.exp(-t * 2.2) * env_adsr(len(t), 0.003, 0.0, 1.0, 0.05)


def sub_bass(freq, dur):
    t = t_axis(dur)
    x = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)
    return np.tanh(x * 1.3) * env_adsr(len(t), 0.01, 0.1, 0.8, 0.08)


# ------------------------------------------------------------------- music
PROG = [  # one chord per bar
    ("A2", ["A3", "C4", "E4", "B4"]),   # Am(add9)
    ("F2", ["F3", "A3", "C4", "E4"]),   # Fmaj7
    ("C3", ["C4", "E4", "G4", "B4"]),   # Cmaj7
    ("G2", ["G3", "B3", "D4", "A4"]),   # G(add9)
]
TOTAL = 35.4
DROP = 10.2
OUTRO = 30.6


def music():
    n = int((TOTAL + 2.5) * SR)
    pads = np.zeros(n)
    drums = np.zeros(n)
    bass = np.zeros(n)
    arp = np.zeros(n)
    fx = np.zeros(n)

    # Pads across the whole piece (one chord per bar, aligned so a bar starts at the drop)
    first_bar = DROP - BAR * 5   # = -1.8 -> start the progression slightly before 0
    bar_t = first_bar
    k = 0
    while bar_t < OUTRO:
        root, chord = PROG[k % 4]
        cutoff = 900 if bar_t < DROP - 2.4 else 2400
        sig = pad_chord(chord, BAR + 0.6, cutoff)
        if bar_t < 0:
            sig = sig[int(-bar_t * SR):]
            add(pads, sig, 0)
        else:
            add(pads, sig, bar_t)
        # bass in main section
        if DROP <= bar_t < OUTRO:
            f = note_hz(root)
            for b in range(4):
                for half in (0, 0.5):
                    add(bass, sub_bass(f, BEAT * 0.45), bar_t + (b + half) * BEAT)
        # music-box arpeggio: soft in intro, brighter after the drop
        pattern = [0, 2, 1, 3, 2, 1, 3, 2]
        for s in range(8):
            at = bar_t + s * BEAT / 2
            if at < 0.6 or at >= OUTRO:
                continue
            nme = chord[pattern[s] % len(chord)]
            f = note_hz(nme) * 2
            if at < DROP:
                add(arp, pluck(f, 0.7, 0.3) * 0.55, at)
            else:
                add(arp, pluck(f, 0.5, 0.6), at)
        bar_t += BAR
        k += 1

    # Intro heartbeat on the beat (soft kicks) until the riser
    b = 0.0
    while b < 7.8:
        add(drums, kick(0.35) * 0.35, b)
        add(drums, kick(0.3) * 0.18, b + 0.2)
        b += BAR / 2
    # Snare/clap roll build 7.8 -> 10.2
    t0, t1 = 7.8, DROP
    steps = [t0 + i * BEAT / 2 for i in range(4)] + [t0 + 1.2 + i * BEAT / 4 for i in range(4)] + \
            [t0 + 1.8 + i * BEAT / 8 for i in range(8)]
    for i, at in enumerate(steps):
        add(drums, clap(0.2) * (0.25 + 0.6 * i / len(steps)), at)

    # Main groove from the drop to the outro
    beat_t = DROP
    i = 0
    while beat_t < OUTRO - 1e-6:
        add(drums, kick(), beat_t)
        if i % 2 == 1:
            add(drums, clap() * 0.7, beat_t)
        add(drums, hat() * 0.5, beat_t + BEAT / 2)
        if i % 4 == 3:
            add(drums, hat(open_=True) * 0.35, beat_t + BEAT * 0.75)
        beat_t += BEAT
        i += 1

    # Outro: final chord + bell, long tail
    add(pads, pad_chord(["A3", "C4", "E4", "G4", "B4"], 4.6, 2000) * 1.2, OUTRO)
    add(bass, sub_bass(note_hz("A1"), 2.8) * 0.9, OUTRO)
    add(drums, kick(0.9) * 1.1, OUTRO)
    for j, nme in enumerate(["E5", "A5", "B5", "C6", "E6"]):
        add(fx, bell(note_hz(nme), 2.5) * 0.35, OUTRO + 0.3 + j * 0.3)

    mix = 0.55 * pads + 0.9 * drums + 0.55 * bass + 0.35 * arp + 0.5 * fx
    # gentle fade at the end
    fade_start = int((TOTAL - 1.4) * SR)
    mix[fade_start:] *= np.linspace(1, 0, len(mix) - fade_start) ** 2
    mix = mix[: int(TOTAL * SR)]
    return np.tanh(mix * 1.1)


# --------------------------------------------------------------------- sfx
def whoosh(dur=0.7, up=True):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    sweep = (300 + 5000 * (t / dur) ** 2) if up else (5000 - 4600 * (t / dur) ** 0.5)
    x = lowpass(n, sweep)
    x = x - lowpass(x, 150)
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return x * e


def riser(dur=2.4):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    x = lowpass(n, 200 + 7000 * (t / dur) ** 2.2)
    tone_f = 110 * 2 ** (2.5 * t / dur)
    tone = np.sin(2 * np.pi * np.cumsum(tone_f) / SR) * 0.4
    e = (t / dur) ** 2
    out = (x * 0.8 + tone) * e
    out[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return out


def impact(dur=2.2):
    t = t_axis(dur)
    f = 38 + 90 * np.exp(-t * 18)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    n = rng.standard_normal(len(t))
    crack = lp_fast(n, 3500) * np.exp(-t * 18) * 0.6
    tail = lp_fast(n, 900) * np.exp(-t * 3) * 0.25
    return np.tanh((boom * 1.4 + crack + tail) * 1.4)


def deep_boom(dur=2.5):
    t = t_axis(dur)
    f = 30 + 50 * np.exp(-t * 6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6) + \
        lp_fast(rng.standard_normal(len(t)), 400) * np.exp(-t * 4) * 0.3


def pop(dur=0.18):
    t = t_axis(dur)
    f = 300 + 900 * np.exp(-t * 40)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)


def tick(dur=0.12):
    t = t_axis(dur)
    return (np.sin(2 * np.pi * 1800 * t) * 0.6 + bp_fast(rng.standard_normal(len(t)), 2000, 8000) * 0.5) \
        * np.exp(-t * 60)


def shimmer(dur=1.8):
    t = t_axis(dur)
    x = np.zeros_like(t)
    notes = ["E6", "A6", "B6", "E7", "C7", "A6", "E7"]
    for i, nme in enumerate(notes):
        add(x, bell(note_hz(nme), dur - i * 0.08) * (0.9 - i * 0.08), i * 0.07)
    return x


def page_flip(dur=0.55):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    flutter = 0.55 + 0.45 * np.sin(2 * np.pi * (18 + 12 * t / dur) * t) ** 2
    e = np.exp(-((t - 0.18) / 0.12) ** 2) + 0.5 * np.exp(-((t - 0.36) / 0.08) ** 2)
    return bp_fast(n, 1200, 7500) * flutter * e


def paper_rustle(dur=1.2):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    grains = np.zeros_like(t)
    for c in rng.uniform(0.05, dur - 0.1, 22):
        grains += np.exp(-((t - c) / rng.uniform(0.01, 0.04)) ** 2) * rng.uniform(0.3, 1)
    return bp_fast(n, 1500, 9000) * grains


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    write_wav(os.path.join(out_dir, "music_bed.wav"), music(), stereo_width=0.6)
    write_wav(os.path.join(out_dir, "sfx_whoosh.wav"), whoosh(0.7), 0.5)
    write_wav(os.path.join(out_dir, "sfx_whoosh_short.wav"), whoosh(0.4), 0.5)
    write_wav(os.path.join(out_dir, "sfx_riser.wav"), riser(2.4), 0.5)
    write_wav(os.path.join(out_dir, "sfx_impact.wav"), impact(), 0.3)
    write_wav(os.path.join(out_dir, "sfx_deep_boom.wav"), deep_boom(), 0.2)
    write_wav(os.path.join(out_dir, "sfx_pop.wav"), pop())
    write_wav(os.path.join(out_dir, "sfx_tick.wav"), tick())
    write_wav(os.path.join(out_dir, "sfx_shimmer.wav"), shimmer(), 0.7)
    write_wav(os.path.join(out_dir, "sfx_page_flip.wav"), page_flip(), 0.4)
    write_wav(os.path.join(out_dir, "sfx_paper_rustle.wav"), paper_rustle(), 0.5)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/audio")
