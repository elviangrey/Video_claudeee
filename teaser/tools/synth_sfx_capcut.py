"""Extra CapCut-style SFX for compositions/capcut-vibes.html (original, numpy-generated).

    python3 teaser/tools/synth_sfx_capcut.py teaser/assets/audio
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from synth_audio import SR, bp_fast, hp_fast, lowpass, lp_fast, rng, t_axis, write_wav  # noqa: E402


def glitch(dur=0.45):
    """Digital stutter: gated square bursts + bit-crushed noise."""
    t = t_axis(dur)
    out = np.zeros_like(t)
    seg = int(0.03 * SR)
    for i in range(0, len(t), seg):
        f = rng.choice([180, 360, 720, 1440, 2880])
        tt = t[i:i + seg]
        sq = np.sign(np.sin(2 * np.pi * f * tt))
        if rng.random() < 0.35:
            sq = rng.uniform(-1, 1, len(tt))
        gate = 1.0 if rng.random() < 0.75 else 0.0
        out[i:i + seg] = sq * gate
    crushed = np.round(out * 4) / 4
    return lp_fast(crushed, 6000) * np.exp(-t * 2.5) * 0.7


def bass_hit(dur=0.9):
    t = t_axis(dur)
    f = 42 + 70 * np.exp(-t * 22)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    click = hp_fast(rng.standard_normal(len(t)), 2000) * np.exp(-t * 200) * 0.3
    return np.tanh((body + click) * 2.0)


def swipe(dur=0.35):
    """Bright fast swipe for whip transitions."""
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    sweep = 1500 + 9000 * (t / dur)
    x = lowpass(n, sweep)
    x = hp_fast(x, 900)
    return x * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5


def shutter(dur=0.18):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    e = np.exp(-t * 90) + 0.6 * np.where(t > 0.07, np.exp(-(t - 0.07) * 110), 0)
    return bp_fast(n, 1500, 9000) * e


def type_tick(dur=0.06):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    return bp_fast(n, 2500, 9000) * np.exp(-t * 140) + np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 200) * 0.3


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    write_wav(os.path.join(out_dir, "cc_glitch.wav"), glitch(), 0.4)
    write_wav(os.path.join(out_dir, "cc_bass_hit.wav"), bass_hit(), 0.1)
    write_wav(os.path.join(out_dir, "cc_swipe.wav"), swipe(), 0.6)
    write_wav(os.path.join(out_dir, "cc_shutter.wav"), shutter(), 0.3)
    write_wav(os.path.join(out_dir, "cc_type_tick.wav"), type_tick(), 0.2)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/audio")
