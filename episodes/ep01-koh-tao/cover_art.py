"""EP.01 cover art: present-day James (tan, hibiscus shirt) at the sunset viewpoint, waving with his coffee.
Renders cover_art.html (no subtitles/UI) -> node ../../pipeline/motion/render_shot.js cover_art.html <dir> 0 1 24 2"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clip as CP
import cast as C
import style5 as S5, style6 as S6

C.anim('sh_grin_t', 'jCov')
vista = S6.renamed(S6.vista_calm())
svg = CP.put(vista, S5.sun_island('smirk'), C.james_now('jcov', 'jCov', [(0, 'chest')], [(0, (150, 30))], holdL=CP.COFFEE))
s = dict(name='cover', t0=0, t1=1, svg=svg, faces=[], ui='', frame=(2.3, 440, 545), cam=None, past=False, zb=None, subs=False, eye=False)
html = CP.page(s, 0)
html = html.replace('<g id="L-ui">', '<g id="L-ui" display="none">')
open(os.path.join(HERE, 'cover_art.html'), 'w').write(html)
print('ok')
