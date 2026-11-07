"""Generate single-element compositions (one graphic visible, transparent background).

    python3 tools/make_element_files.py info-head info-loc info-time

Writes capcut-el-<id>.html for each element id, based on capcut-graphics.html
(run make_layer_files.py first). Everything except the chosen element is hidden.
"""
import pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "capcut-graphics.html").read_text()
for el in sys.argv[1:]:
    css = f"""
      /* single-element export: only #{el} is visible */
      #root > *:not(#{el}) {{ visibility: hidden !important; }}
      #root > #{el}, #root > #{el} * {{ visibility: visible; }}
    </style>"""
    out = root / f"capcut-el-{el}.html"
    out.write_text(src.replace("    </style>", css, 1))
    print("wrote", out.name)
