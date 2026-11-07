# Transcript (OpenAI Whisper `small`, word timestamps, CPU)

Each clip was transcribed on its own, plus an ffmpeg `volumedetect` + `silencedetect` pass
(threshold −35 dB, minimum 0.4 s).

| Clip | Whisper output | Confidence | Audio level (mean / peak) | Verdict |
|---|---|---|---|---|
| `Opening_1.mp4` | `[0.00–0.18] "Got it."` | logprob −2.72, no_speech 0.59 | −45.1 / −28.8 dB | ❌ hallucination (0.18 s blip of room noise) |
| `Opening_2.mp4` | — | — | −43.0 / −21.1 dB | footsteps only |
| `Opening3.mp4` | `[4.98–6.38] "see you soon."` | logprob −2.20, no_speech 0.58 | −52.5 / −28.8 dB | ❌ hallucination (two short noise bursts at 4.9 s and 5.8 s) |
| `Book transition.mp4` | — | — | −49.4 / −25.4 dB | shelf and page rustle at 7–12 s |
| `5_6300940584869700113.mp4` | (skipped: byte-identical duplicate of `Book transition.mp4`) | | | |
| `book transition_2.mp4` | — | — | −48.7 / −29.0 dB | room tone |
| `5_6300940584869700108.mp4` | — | — | −49.1 / −30.5 dB | room tone |
| `Library ambience.mp4` | — | — | −46.9 / −31.1 dB | air-con and room tone |
| `ending.mp4` | — | — | −51.3 / −32.2 dB | almost silent |

**Conclusion:** the footage has **no spoken lines**. The two outputs above have very low
log-probability and about a 60% no-speech probability, which is the typical pattern of Whisper
hallucinating on noise. So:

- the cuts are placed on **visual action and the music grid**, not on speech,
- all source audio is muted, because it is just hiss and room tone,
- the story is told through **on-screen text, motion graphics, music and SFX**, each timed to an
  on-screen action (see `EDIT_PLAN.md` §3).

If a voice-over is wanted later, record it, drop it into `assets/audio/`, and rerun
`npx hyperframes transcribe vo.wav --model small` to get word timestamps for captions.
