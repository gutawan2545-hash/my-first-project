"""บ้านตรงข้าม · คลิปทดลอง (ยังไม่มีเสียงพากย์): เตรียมช็อต เวลา และการเคลื่อนไหว -> clip/shots.json + clip/page.html"""
import os, runpy, json
HERE = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(HERE)
os.chdir(EP); G = runpy.run_path('storyboard.py'); os.chdir(HERE)
SHOTS, FRAMES = G['SHOTS'], G['FRAMES']
MOVE = {   # per shot: camera push (z0,z1,cx,cy), character moves, shake, special
    1: dict(push=(1.0, 1.07, 270, 380)),
    2: dict(push=(1.0, 1.05, 270, 470), walk=[(0, 0, -36, .78)]),
    10: dict(push=(1.0, 1.08, 270, 400), shake=(1.6, 4)),
    12: dict(push=(1.0, 1.06, 300, 480)),
    14: dict(push=(1.0, 1.14, 350, 520), shake=(2.6, 5)),
    17: dict(push=(1.0, 1.06, 270, 360), shake=(1.0, 7)),
    20: dict(push=(1.0, 1.03, 270, 520), walk=[(0, 0, -70, .7)]),
    21: dict(push=(1.0, 1.06, 270, 400), shake=(2.0, 4)),
    22: dict(push=(1.0, 1.04, 270, 500), walk=[(0, 0, 26, 1.06)]),
    23: dict(push=(1.0, 1.08, 300, 470)),
    24: dict(push=(1.04, 1.0, 280, 520), lights_on=True, shake=(.35, 3)),
    29: dict(push=(1.0, 1.1, 270, 480), cut_black=True),
    30: dict(ab=True),
}
shots = []
for n, (sid, tg, chars, th, en, note) in enumerate(SHOTS, 1):
    n_chars = len(th.replace('\n', ''))
    dur = 5.0 if sid == 'AB' else (3.4 if not th else min(5.6, max(3.0, n_chars / 11 + 1.7)))
    shots.append(dict(n=n, sid=sid, dur=round(dur, 2), move=MOVE.get(n, dict(push=(1.0, 1.05, 270, 460))), svg=FRAMES[n - 1]))
json.dump(shots, open('shots.json', 'w', encoding='utf-8'), ensure_ascii=False)
page = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&family=Inter:wght@400;700&display=swap">
<style>html,body{{margin:0;background:#000}} #f svg{{display:block;width:540px;height:960px}}
.th{{font-family:"IBM Plex Sans Thai",sans-serif;font-weight:700;font-size:20px;fill:#ffd84a;stroke:#1a1020;stroke-width:4.5px;paint-order:stroke;text-anchor:middle}}
.en{{font-family:Inter,sans-serif;font-size:13px;fill:#fff;stroke:#1a1020;stroke-width:3px;paint-order:stroke;text-anchor:middle}}
.tag{{font-family:"IBM Plex Sans Thai",sans-serif;font-size:14px;fill:#efe6ff;text-anchor:middle}}
.q{{font-family:"IBM Plex Sans Thai",sans-serif;font-weight:700;font-size:30px;fill:#fff;text-anchor:middle}}
.qe{{font-family:Inter,sans-serif;font-size:14px;fill:#b8acd8;text-anchor:middle}}
.abl{{font-family:Inter,sans-serif;font-weight:700;font-size:26px;fill:#140f22;text-anchor:middle}}
.abt{{font-family:"IBM Plex Sans Thai",sans-serif;font-weight:700;font-size:24px;fill:#fff}}
.abe{{font-family:Inter,sans-serif;font-size:13px;fill:#b8acd8}}</style></head><body>
{G['SG']['DEFS']}
<svg width="0" height="0" style="position:absolute"><defs><filter id="sbBlur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
{G['TG']['HEAD_DEFS']}{G['OG']['DEFS']}{G['EXTRA_DEFS']}</defs></svg>
<div id="f"></div>
<script>
let S=null, BR=[];
function load(svg, spec){{ document.getElementById('f').innerHTML = svg; S = spec;
  BR = [...document.querySelectorAll('#f .br')].map(e => ({{e, x:+e.dataset.x, fy:+e.dataset.fy}}));
  S.fl = [...document.querySelectorAll('#f .fl')]; }}
function rnd(i){{ const x = Math.sin(i*12.9898)*43758.5453; return x - Math.floor(x); }}
function setT(t, dur){{
  const m = S.move || {{}}; const u = Math.min(1, t/dur); const e = u*u*(3-2*u);
  const cam = document.getElementById('cam');
  if (cam && m.push) {{ const [z0,z1,cx,cy] = m.push; const z = z0 + (z1-z0)*e;
    let sx = 0, sy = 0;
    if (m.shake && t > m.shake[0]) {{ const k = Math.max(0, 1 - (t - m.shake[0]) / .6); const a = m.shake[1]*k;
      sx = (rnd(Math.floor(t*30))-.5)*2*a; sy = (rnd(Math.floor(t*30)+7)-.5)*2*a; }}
    cam.setAttribute('transform', `translate(${{cx+sx}},${{cy+sy}}) scale(${{z}}) translate(${{-cx}},${{-cy}})`); }}
  BR.forEach((b, i) => {{ let dx = 0, dy = 0, s = 1;
    (m.walk||[]).forEach(w => {{ if (w[0] === i) {{ dx = w[1]*e; dy = w[2]*e; s = 1 + (w[3]-1)*e; }} }});
    const br = 1 + .007*Math.sin(t*2*Math.PI/3.4 + i*1.7); const bob = (m.walk||[]).some(w => w[0] === i) ? Math.abs(Math.sin(t*Math.PI*2.2))*3 : 0;
    b.e.setAttribute('transform', `translate(${{b.x+dx}},${{b.fy+dy-bob}}) scale(${{s}},${{s*br}}) translate(${{-b.x}},${{-b.fy}})`); }});
  S.fl.forEach((g, i) => g.setAttribute('opacity', (.9 + .1*Math.sin(t*7.3 + i*2) * Math.sin(t*2.1 + i)).toFixed(3)));
  const d = document.getElementById('dust'); if (d) d.setAttribute('transform', `translate(${{Math.sin(t*.7)*4}},${{-t*7}})`);
  const ov = document.getElementById('ov'); if (ov) ov.setAttribute('opacity', Math.min(1, Math.max(0, (t - .25)/.35)).toFixed(3));
  const dk = document.getElementById('dark');
  if (dk) {{ let o = 0; if (m.lights_on) o = t < .3 ? 1 : Math.max(0, 1 - (t - .3)/.25);
    if (m.cut_black && t > dur - .35) o = 1; dk.setAttribute('opacity', o); }}
  if (m.ab) {{ const on = Math.floor(t/0.9) % 2; document.querySelectorAll('#f .abopt').forEach((g, i) => {{
      g.querySelector('.abbox').setAttribute('fill', i === on ? '#3a2a5e' : '#221a36'); g.querySelector('.abbox').setAttribute('stroke', i === on ? '#c9a8ff' : '#5a4a7a');
      g.querySelector('.abbox').setAttribute('stroke-width', i === on ? 3 : 1.5); g.querySelector('.abdot').setAttribute('fill', i === on ? '#c9a8ff' : '#4a3a6a');
      g.setAttribute('opacity', i === on ? 1 : .8); }}); }}
}}
</script></body></html>"""
open('page.html', 'w', encoding='utf-8').write(page)
print('shots', len(shots), 'total', round(sum(s['dur'] for s in shots), 1), 's')
