"""Cover art for แม่ชีคนที่สอง EP1: the approved chapel frame (Mariam front, Agnes behind with the candle),
current character versions (pale Agnes), no subtitles or time chip. Writes art_ep1.svg.html for cover/cover.py."""
import os, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
EP1 = os.path.join(HERE, "..", "ep1")
NS = {"__file__": os.path.join(EP1, "storyboard.py"), "__name__": "sb"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(EP1, "storyboard.py")).read(), NS)
fr = NS["INS_EXACT"]["chapel_v1"]
fr = fr.replace('<g id="v1_subs"', '<g id="v1_subs" display="none"')
o = fr.find("OVERLAY: time chip"); e = fr.find('<g id="v1_subs"', o)
if o > 0: fr = fr[:o] + "-->" + fr[o:e].replace("-->", "", 1).replace("<g", '<g display="none"', 1).replace('<g transform="translate(500,44)"', '<g display="none" transform="translate(500,44)"') + fr[e:]
out = f'<svg width="0" height="0" style="position:absolute"><defs>{NS["V1_DEFS"]}<g id="chapelArt">{fr}</g></defs></svg>'
open(os.path.join(HERE, "art_ep1.svg.html"), "w").write(out)
print("art_ep1.svg.html", len(out) // 1024, "KB")
