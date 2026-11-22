"""Ending rework: same storage door everywhere (85:200), Dean reacts on the first ring, Tawan's look,
over-the-shoulder second call with a slow reach, single-question end card with logo + blink."""


def rep(s, o, n):
    assert o in s, o[:110]
    return s.replace(o, n, 1)


p = 'v2.py'
s = open(p).read()

# ---------- Tawan face variants: looking down at the phone / serious / looking at James ----------
s = rep(s, "assert jbNHnoL.count('M -55,114') == 0",
"""th = group_by_id(head, 'thead')
def iris_shift(g, dx, dy):
    for (x, y, r) in [(-13, -0.5, 4.9), (-13, -0.5, 2.3), (13, -0.5, 4.9), (13, -0.5, 2.3), (-14.8, -2.3, 1.5), (-11.4, 1.4, .7), (11.2, -2.3, 1.5), (14.6, 1.4, .7)]:
        rs = ('.7' if r == .7 else str(r))
        g = g.replace(f'<circle cx="{x:g}" cy="{y:g}" r="{rs}"', f'<circle cx="{x+dx:g}" cy="{y+dy:g}" r="{rs}"')
    return g
SMILE = '<path d="M -6.5,22 Q 0,25.6 6.5,21.6" fill="none" stroke="#a24a46" stroke-width="2" stroke-linecap="round"/>'
LIP = '<path d="M -3.5,25.4 Q 0,27.4 3.5,25.2" fill="none" stroke="#e79a8a" stroke-width="1.6" stroke-linecap="round"/>'
assert SMILE in th and LIP in th, 'tawan smile'
FLAT = '<path d="M -5.5,23.2 Q 0,23.8 5.5,23.2" fill="none" stroke="#a24a46" stroke-width="2" stroke-linecap="round"/>'
thDown = iris_shift(th, 0, 2.0).replace('id="thead"', 'id="theadDown"', 1)
thDownS = thDown.replace('id="theadDown"', 'id="theadDownS"', 1).replace(SMILE, FLAT).replace(LIP, '')
thLookS = iris_shift(th, -3.2, 0).replace('id="thead"', 'id="theadLookS"', 1).replace(SMILE, FLAT).replace(LIP, '')
assert thDown.count('cy="1.5" r="4.9"') == 2 and thLookS.count('cx="-16.2"') == 2, 'iris variants'
tbV = ''.join(tbNoR.replace('id="tbodyNoR"', f'id="tb_{v}"', 1).replace('<use href="#thead"/>', f'<use href="#{v}"/>') for v in ('theadDown', 'theadDownS', 'theadLookS'))
assert jbNHnoL.count('M -55,114') == 0""")
s = rep(s, "extra = ('<svg width=\"0\" height=\"0\" style=\"position:absolute\" aria-hidden=\"true\"><defs>' + jbNHnoL + tbNoR + tbSNoArms + jhNH",
           "extra = ('<svg width=\"0\" height=\"0\" style=\"position:absolute\" aria-hidden=\"true\"><defs>' + thDown + thDownS + thLookS + tbV + jbNHnoL + tbNoR + tbSNoArms + jhNH")

# ---------- the one storage door: 85:200, same colours / panels / knob ----------
s = rep(s, "SV['dean'] = (hall(560, (30, 170, 190, 560)) + '<rect x=\"30\" y=\"552\" width=\"160\" height=\"8\" fill=\"#08060c\"/>'",
           "SV['dean'] = (hall(560, (30, 170, 196, 560)) + '<rect x=\"30\" y=\"552\" width=\"166\" height=\"8\" fill=\"#08060c\"/>'")
a = s.index("s7 = A8['s7'].replace(VIG + TEX, '')"); b = s.index("SV['door'] = s7") + len("SV['door'] = s7")
waves = ('<g class="pulse" fill="none" stroke="#e2ecff" stroke-width="3" stroke-linecap="round" opacity=".8">'
         '<path d="M{x1},{y} q14,20 0,40"/><path d="M{x2},{y2} q22,32 0,64"/><path d="M{x3},{y} q-14,20 0,40"/><path d="M{x4},{y2} q-22,32 0,64"/></g>')
s = s[:a] + '''DOOR_F = (155, 150, 385, 691)          # front-on: 230 x 541 = 85:200, both jambs + a strip of floor
x0, y0, x1, y1 = DOOR_F
SV['door'] = (hall(y1, DOOR_F) + f'<rect class="underlight" x="{x0}" y="{y1-8}" width="{x1-x0}" height="8" fill="#e2ecff"/>'
              '<rect width="540" height="960" fill="url(#coolPool)" style="mix-blend-mode:screen"/>'
              + ''' + repr(waves) + '''.format(x1=300, x2=314, x3=240, x4=226, y=400, y2=388) + dust(281, (150, 600, 400, 760), 14, '#eef4ff'))
DOOR_O = (252, 250, 392, 580)          # same door, further away, for the over-the-shoulder shot
x0, y0, x1, y1 = DOOR_O
knob = (x1 - 18, (y0 + y1) / 2 + 20)
ots_reach = (f'<g class="otsreach"><path d="M 250,980 C 270,800 300,600 {knob[0]-34},{knob[1]+18} L {knob[0]-20},{knob[1]+30} C 330,640 320,820 330,980 Z" fill="#1f2852"/>'
             f'<path d="M 250,980 C 270,800 300,600 {knob[0]-34},{knob[1]+18}" fill="none" stroke="#7f8ec4" stroke-width="2.5"/>'
             f'<ellipse cx="{knob[0]-24}" cy="{knob[1]+12}" rx="12" ry="10" fill="#c9b0b4"/><path d="M {knob[0]-20},{knob[1]+8} L {knob[0]-9},{knob[1]+2}" stroke="#c9b0b4" stroke-width="6" stroke-linecap="round"/></g>')
SV['ots'] = (hall(y1, DOOR_O) + f'<rect class="underlight" x="{x0}" y="{y1-6}" width="{x1-x0}" height="6" fill="#e2ecff"/>'
             f'<circle cx="{(x0+x1)/2}" cy="{y1+30}" r="150" fill="#cfe0ff" opacity=".28" filter="url(#haze)" style="mix-blend-mode:screen"/>'
             + ''' + repr(waves) + '''.format(x1=344, x2=356, x3=300, x4=288, y=370, y2=360)
             + dust(291, (230, 480, 420, 620), 12, '#eef4ff') +
             '<g filter="url(#tintNight)">' + ots_reach +
             '<path d="M -60,960 C -50,800 20,720 140,705 C 230,696 300,735 330,820 L 350,960 Z" fill="#1f2852"/>'
             '<path d="M 20,760 C 70,724 130,712 190,714" fill="none" stroke="#7f8ec4" stroke-width="3"/>'
             '<ellipse cx="150" cy="610" rx="92" ry="104" fill="#14111c"/>'
             '<path d="M 62,580 L 54,540 L 80,556 L 84,512 L 108,540 L 122,500 L 140,532 L 162,498 L 172,534 L 198,506 L 200,546 L 230,530 L 238,590 Z" fill="#14111c"/>'
             '<ellipse cx="62" cy="630" rx="12" ry="20" fill="#b89a98"/><path d="M 236,600 L 300,606" stroke="#9aa0b8" stroke-width="2.4"/></g>'
             '<g><path d="M 486,560 L 552,540 L 560,690 L 500,700 Z" fill="#c99486"/>'
             '<g transform="rotate(-10 505 590)"><rect x="470" y="520" width="56" height="104" rx="9" fill="#0c0d14"/><rect x="474" y="524" width="48" height="96" rx="7" fill="#9fb4ff"/>'
             '<rect x="480" y="540" width="36" height="12" rx="3" fill="#e2ecff"/><circle cx="498" cy="600" r="7" fill="#e0574a"/></g>'
             '<circle cx="500" cy="580" r="70" fill="#9fb4ff" opacity=".3" filter="url(#haze)" style="mix-blend-mode:screen"/></g>')''' + s[b:]

# ---------- Tawan hangs up, smile drops, looks up at James ----------
s = rep(s, "SV['glance'] = duo('jbodySNH')",
"""armTphone = ('<path d="M 50,64 C 58,72 62,92 62,110 L 46,114 L 40,74 Z" fill="#f3e6cf"/>'
             '<path d="M 60,106 L 47,113 L 20,100 L 28,86 Z" fill="#e8b08a"/><ellipse cx="22" cy="93" rx="9" ry="8" fill="#e8b08a"/>'
             '<g transform="rotate(-12 14 88)"><rect x="4" y="70" width="18" height="32" rx="3" fill="#0c0d14"/><circle cx="9" cy="75" r="1.6" fill="#3a3a48"/></g>')
SV['tawanlook'] = (room_top + bg + '<g filter="url(#bright)"><g transform="translate(270,300) scale(2.1)">'
                   '<g class="fA"><use href="#tb_theadDown"/></g><g class="fB" display="none"><use href="#tb_theadDownS"/></g><g class="fC" display="none"><use href="#tb_theadLookS"/></g>'
                   + armTphone + '</g></g>' + lampglow + dust(301, (330, 120, 530, 420), 12))
SV['glance'] = duo('jbodySNH')""")

# ---------- end card: fingertip a hair from the knob, one question, logo under it ----------
a = s.index("SV['endcard'] = ("); b = s.index("'<g class=\"choice\" opacity=\"0\">' + A8['INFO'][7] + '</g>')\n") + len("'<g class=\"choice\" opacity=\"0\">' + A8['INFO'][7] + '</g>')\n")
s = s[:a] + '''lw = 300; lh = lw * 260 / 1595; lx = 120; ly = 500
ecx = lx + 145 * lw / 1595; ecy = ly + 151 * lw / 1595
KX, KY = 330, 660
SV['endcard'] = ('<rect width="540" height="960" fill="#3a2c32"/>'
                 '<rect x="40" y="40" width="460" height="330" fill="none" stroke="#2a1e24" stroke-width="5"/><rect x="40" y="420" width="460" height="520" fill="none" stroke="#2a1e24" stroke-width="5"/>'
                 '<rect width="540" height="960" fill="#0a0612" opacity=".35"/>'
                 f'<circle cx="{KX}" cy="{KY}" r="150" fill="#cfe0ff" opacity=".10" filter="url(#haze)" style="mix-blend-mode:screen"/>'
                 f'<ellipse cx="{KX}" cy="{KY}" rx="20" ry="46" fill="#2a2024"/><circle cx="{KX}" cy="{KY}" r="22" fill="#9a96a0"/><circle cx="{KX-5}" cy="{KY-5}" r="8" fill="#d9d6e0"/>'
                 f'<g class="reach" filter="url(#tintNight)"><path d="M -60,{KY+10} C 60,{KY-14} 180,{KY-22} {KX-62},{KY-16} L {KX-56},{KY+12} C 180,{KY+16} 60,{KY+40} -60,{KY+70} Z" fill="#2b3768"/>'
                 f'<path d="M -60,{KY+10} C 60,{KY-14} 180,{KY-22} {KX-62},{KY-16}" fill="none" stroke="#a9b8e8" stroke-width="3"/>'
                 f'<ellipse cx="{KX-50}" cy="{KY-2}" rx="17" ry="14" fill="#fbe7d8"/><path d="M {KX-40},{KY-6} L {KX-27},{KY-4}" stroke="#fbe7d8" stroke-width="8" stroke-linecap="round"/></g>'
                 + dust(271, (60, 520, 300, 760), 12, '#eef4ff') +
                 f'<g class="q" opacity="0" {FT} text-anchor="middle">'
                 '<text x="270" y="392" font-size="32" font-weight="500" fill="#f2eefa" stroke="#0b0812" stroke-width="6" paint-order="stroke">ถ้าเป็นคุณ…</text>'
                 '<text x="270" y="462" font-size="50" font-weight="700" fill="#ffffff" stroke="#0b0812" stroke-width="8" paint-order="stroke">จะ<tspan fill="#c9a8ff">เปิดประตู</tspan>ไหม?</text></g>'
                 f'<g class="logo" opacity="0"><image href="data:image/png;base64,{logo64}" x="{lx}" y="{ly}" width="{lw}" height="{lh:.1f}"/>'
                 f'<g class="logolid" display="none"><ellipse cx="{ecx:.1f}" cy="{ecy:.1f}" rx="21" ry="10" fill="#7a1fff"/>'
                 f'<path d="M {ecx-18:.1f},{ecy+1:.1f} C {ecx-8:.1f},{ecy+5:.1f} {ecx+8:.1f},{ecy+5:.1f} {ecx+18:.1f},{ecy+1:.1f}" stroke="#05040a" stroke-width="2" fill="none"/></g></g>')
''' + s[b:]
s = rep(s, "'hand_stop')", "'hand_stop', 'card_in')")
s = s.replace("    'J5': (['ถ้าเป็นคุณ จะเปิดประตูไปดูว่าใครอยู่ข้างใน'", "    'J5_unused': (['ถ้าเป็นคุณ จะเปิดประตูไปดูว่าใครอยู่ข้างใน'")
open(p, 'w').write(s)

# ---------- JS ----------
j = open('v2.js').read()
j = rep(j, "    const k = ease((t - 0.45) / 0.35);\n    DL.head", "    const k = ease((t - 0.06) / 0.28);\n    DL.head")
j = rep(j, "const alert = t > 0.55;", "const alert = t > 0.1;")
a = j.index("  if (c.key === 'endcard') {"); b = j.index("\n};", a)
j = j[:a] + """  if (c.key === 'tawanlook') {
    const st = t < 0.3 ? 'A' : t < 0.55 ? 'B' : 'C';
    ['A', 'B', 'C'].forEach(x => el('.f' + x).setAttribute('display', x === st ? 'inline' : 'none'));
  }
  if (c.key === 'ots') {
    const k = ease((t - 0.6) / 2.8), dx = -60 * (1 - k), dy = 300 * (1 - k);
    el('.otsreach').setAttribute('transform', `translate(${dx.toFixed(1)} ${dy.toFixed(1)})`);
  }
  if (c.key === 'endcard') {
    const k = ease(t / 0.4), x = -10 * (1 - k);
    el('.reach').setAttribute('transform', `translate(${x.toFixed(1)} 0)`);
    el('.q').setAttribute('opacity', clamp((t - c.card_in) / 0.25).toFixed(2));
    el('.logo').setAttribute('opacity', clamp((t - c.card_in - 0.35) / 0.35).toFixed(2));
    el('.logolid').setAttribute('display', (t > c.dur - 0.2) ? 'inline' : 'none');
  }""" + j[b:]
j = rep(j, "const p = el('.pulse'); if (p) { const k = (t * 1.6) % 1; p.setAttribute('transform', `translate(270 440)",
           "const p = el('.pulse'); if (p) { const k = (t * 1.6) % 1; const cx = c.key === 'ots' ? 322 : 270, cy = c.key === 'ots' ? 400 : 430; p.setAttribute('transform', `translate(${cx} ${cy})")
j = rep(j, "scale(${(1 + 0.25 * k).toFixed(3)}) translate(-270 -440)`);", "scale(${(1 + 0.25 * k).toFixed(3)}) translate(${-cx} ${-cy})`);")
j = rep(j, "if (c.key === 'door' || c.key === 'behind') {", "if (c.key === 'door' || c.key === 'ots') {")
open('v2.js', 'w').write(j)
print('patched end')
