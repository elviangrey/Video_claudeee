"""Generate layer-only compositions from index.html for the CapCut export pack.

  capcut-graphics.html : every <video>/<audio> tag stripped, transparent background
                         (text, motion graphics, title/end cards, wipes)
  capcut-base.html     : no <audio>, text/graphics hidden (footage + zooms + shading + card backgrounds)

The HyperFrames renderer composites <video> frames itself, so footage has to be removed
from the markup rather than hidden with CSS.
"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text()
no_audio = re.sub(r'\s*<audio\b[^>]*></audio>', '', src)

g = re.sub(r'\s*<video\b[^>]*></video>', '', no_audio)
g = g.replace('<html lang="en"', '<html lang="en" class="layer-graphics"', 1)
(root / "capcut-graphics.html").write_text(g)

b = no_audio.replace('<html lang="en"', '<html lang="en" class="layer-base"', 1)
(root / "capcut-base.html").write_text(b)
print("wrote capcut-graphics.html, capcut-base.html")
