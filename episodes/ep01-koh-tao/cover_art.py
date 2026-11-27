"""EP.01 cover art (bright daytime): present-day James on the ferry deck arriving at Koh Tao, waving with his coffee.
Renders cover_art.html (no subtitles/UI) -> node ../../pipeline/motion/render_shot.js cover_art.html <dir> 0 1 24 2"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clip as CP
import cast as C
import clip_scenes as CS

C.anim('sh_grin_t', 'jCov')
svg, _ = CS.island_view(-10, -9)                      # graphics timed in the past -> none visible
james = C.james_now('jcov', 'jCov', [(0, 'chest')], [(0, (150, 30))], holdL=CP.COFFEE)
cdefs, cg = CS.char('CV', james, 'translate(330,522) scale(.9)', (500, 60), (330, 960), 'day', 'sun')
# James stands on the deck in front of the railing; head kept below the title block (template: text in the top half)
svg = svg.replace('</g><g id="L-light">', f'{cg}</g><defs>{cdefs}</defs><g id="L-light">', 1)
s = dict(name='cover', t0=0, t1=1, svg=svg, faces=[], ui='', frame=None, cam=None, past=False, zb=None, subs=False, eye=False)
html = CP.page(s, 0).replace('<g id="L-ui">', '<g id="L-ui" display="none">')
open(os.path.join(HERE, 'cover_art.html'), 'w').write(html)
print('ok')
