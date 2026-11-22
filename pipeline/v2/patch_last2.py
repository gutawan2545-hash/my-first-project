"""Last two shots: (1) over James's shoulder down the hallway to the door at the far end; James, arms at
his sides, turns toward the ring and takes one step; Tawan beside him with her phone.
(2) close on the knob: only James's wrist + hand from bottom-left, palm toward the knob, fingers curled,
stopping short with a clear gap; question + logo (logo one line lower, centred, above hand and knob)."""


def rep(s, o, n):
    assert o in s, o[:110]
    return s.replace(o, n, 1)


p = 'v2.py'
s = open(p).read()

a = s.index("DOOR_O = (252, 250, 392, 580)"); b0 = s.index("SV['ots'] = (hall(y1, DOOR_O)", a)
b = s.index("')\n", s.index('opacity=".3" filter="url(#haze)" style="mix-blend-mode:screen"/></g>', b0)) + 3
new_ots = r'''# ---- hallway in perspective, the same storage door at the far end (85:200) ----
DX0, DY0, DX1, DY1 = 232, 300, 308, 479          # 76 x 179 = 85:200
hallp = ('<rect width="540" height="960" fill="#120e18"/>'
         '<path d="M0,0 L190,250 L350,250 L540,0 Z" fill="#17121e"/>'                      # ceiling
         '<path d="M0,0 L190,250 L190,500 L0,960 Z" fill="#221a2a"/>'                      # left wall
         '<path d="M540,0 L350,250 L350,500 L540,960 Z" fill="#1d1724"/>'                  # right wall
         '<rect x="190" y="250" width="160" height="250" fill="url(#hallWall)"/>'          # end wall
         '<path d="M0,960 L190,500 L350,500 L540,960 Z" fill="#231a26"/>'                  # floor
         + ''.join(f'<line x1="{190+k*20}" y1="500" x2="{-140+k*82}" y2="960" stroke="#0e0a14" stroke-opacity=".5" stroke-width="1.5"/>' for k in range(9))
         + '<path d="M0,940 L190,496 L190,500 L0,960 Z" fill="#120e18"/><path d="M540,940 L350,496 L350,500 L540,960 Z" fill="#120e18"/>'
         f'<rect x="{DX0-6}" y="{DY0-6}" width="{DX1-DX0+12}" height="{DY1-DY0+6}" fill="#2e2228"/><rect x="{DX0}" y="{DY0}" width="{DX1-DX0}" height="{DY1-DY0}" fill="#3a2c32"/>'
         f'<rect x="{DX0+8}" y="{DY0+10}" width="{DX1-DX0-16}" height="64" fill="none" stroke="#2a1e24" stroke-width="2"/><rect x="{DX0+8}" y="{DY0+94}" width="{DX1-DX0-16}" height="72" fill="none" stroke="#2a1e24" stroke-width="2"/>'
         f'<circle cx="{DX1-9}" cy="{(DY0+DY1)/2+9}" r="3" fill="#9a96a0"/>'
         f'<rect class="underlight" x="{DX0}" y="{DY1-3}" width="{DX1-DX0}" height="3" fill="#e2ecff"/>'
         f'<path d="M{DX0-30},{DY1} L{DX1+30},{DY1} L{DX1+90},{DY1+90} L{DX0-90},{DY1+90} Z" fill="#cfe0ff" opacity=".22" filter="url(#haze)" style="mix-blend-mode:screen"/>'
         '<g class="pulse" fill="none" stroke="#e2ecff" stroke-width="2" stroke-linecap="round" opacity=".8"><path d="M286,368 q8,12 0,24"/><path d="M294,360 q14,20 0,40"/><path d="M254,368 q-8,12 0,24"/><path d="M246,360 q-14,20 0,40"/></g>')
# ---- James from behind (head units), head can face Tawan (A) or the door (B) ----
SKB = '#d9bfb8'
jback_body = ('<rect x="-9" y="22" width="18" height="36" fill="' + SKB + '"/>'
              '<path d="M -55,114 L -41,118 L -40,170 L -42,236 L -54,236 L -57,170 Z" fill="' + SKB + '"/><path d="M 55,114 L 41,118 L 40,170 L 42,236 L 54,236 L 57,170 Z" fill="#c4a8a2"/>'
              '<path d="M -55,234 L -41,234 C -40,248 -42,262 -48,264 C -54,264 -57,250 -55,234 Z" fill="' + SKB + '"/><path d="M 55,234 L 41,234 C 40,248 42,262 48,264 C 54,264 57,250 55,234 Z" fill="#c4a8a2"/>'
              '<path d="M -41,228 L 41,228 L 44,300 L 37,462 L 9,462 L 2,292 L -2,292 L -9,462 L -37,462 L -44,300 Z" fill="#33406e"/>'
              '<path d="M -12,49 L 12,49 C 28,51 42,56 47,66 L 57,116 L 40,122 L 42,234 L -42,234 L -40,122 L -57,116 L -47,66 C -42,56 -28,51 -12,49 Z" fill="#2b3768"/>'
              '<path d="M 20,50 C 32,53 43,58 47,66 L 57,116 L 40,122 L 42,234 L 26,234 C 28,180 28,100 20,50 Z" fill="#1c2448"/>'
              '<path d="M -14,50 C -6,56 6,56 14,50" fill="none" stroke="#a9b8e8" stroke-width="2.5"/><path d="M 0,58 L 0,232" stroke="#1c2448" stroke-width="1.5"/>'
              '<path d="M -57,116 L -40,122 M 57,116 L 40,122 M -42,232 L 42,232" stroke="#a9b8e8" stroke-width="2"/>')
hairB = ('M -34,-6 C -40,-50 -14,-64 2,-64 C 26,-64 40,-50 34,-6 C 34,14 26,30 12,34 L -12,34 C -26,30 -34,14 -34,-6 Z '
         'M -26,-46 L -30,-66 L -14,-56 L -8,-72 L 2,-58 L 12,-70 L 16,-56 L 30,-64 L 26,-44 Z')
headA = ('<g class="hA"><ellipse cx="-33" cy="4" rx="7" ry="11" fill="' + SKB + '"/>'
         '<path d="M 22,-6 C 34,-6 40,8 36,22 C 32,32 22,36 14,34 Z" fill="' + SKB + '"/>'
         '<g transform="translate(-6 0)"><path d="' + hairB + '" fill="#14111c"/></g></g>')
headB = ('<g class="hB" display="none"><ellipse cx="-33" cy="4" rx="7" ry="11" fill="' + SKB + '"/><ellipse cx="33" cy="4" rx="7" ry="11" fill="#c4a8a2"/>'
         '<path d="' + hairB + '" fill="#14111c"/></g>')
JBACK = f'<g class="jback">{jback_body}{headA}{headB}</g>'
# ---- Tawan from behind, phone at her ear (head units) ----
TBACK = ('<g><path d="M -40,64 C -46,68 -50,86 -50,104 L -51,212 L -40,212 L -38,110 Z" fill="#e2b29c"/>'
         '<path d="M -42,158 L 42,158 L 46,200 L 50,442 L 8,442 L 3,252 L -3,252 L -8,442 L -50,442 Z" fill="#e6d6bc"/>'
         '<path d="M -14,50 L 14,50 C 26,52 36,56 40,64 L 50,98 L 38,102 L 41,204 L -41,204 L -38,102 L -50,98 L -40,64 C -36,56 -26,52 -14,50 Z" fill="#efe2c8"/>'
         '<path d="M 18,51 C 28,53 37,57 40,64 L 50,98 L 38,102 L 41,204 L 26,204 C 27,140 24,80 18,51 Z" fill="#cdb593"/>'
         '<path d="M -38,-4 C -40,-44 -22,-62 0,-62 C 22,-62 40,-44 38,-4 L 45,130 L 37,138 L 29,131 L 20,136 L 0,140 L -20,136 L -29,131 L -37,138 L -45,130 Z" fill="#17121a"/>'
         '<path d="M -38,-4 L -45,130 L -40,135 L -34,0 Z" fill="#372a32"/>'
         '<path d="M 50,64 C 58,72 62,92 62,110 L 48,112 L 40,74 Z" fill="#efe2c8"/><path d="M 60,106 L 48,112 L 40,30 L 52,24 Z" fill="#d9a48c"/>'
         '<ellipse cx="46" cy="18" rx="9" ry="10" fill="#d9a48c"/><rect x="38" y="-10" width="12" height="32" rx="3" fill="#0c0d14"/></g>')
SV['ots'] = (hallp + dust(291, (190, 380, 360, 560), 12, '#eef4ff')
             + '<circle cx="455" cy="485" r="80" fill="#9fb4ff" opacity=".3" filter="url(#haze)" style="mix-blend-mode:screen"/>'
             '<g filter="url(#tintNight)"><g transform="translate(400,500) scale(1.55)">' + TBACK + '</g>'
             '<g class="jstep" transform="translate(185,470) scale(2.0)">' + JBACK + '</g></g>')
'''
s = s[:a] + new_ots + s[b:]

# ---- end card: wrist + hand from bottom-left, palm toward the knob, fingers curled, clear gap ----
a = s.index("lw = 300; lh = lw * 260 / 1595; lx = 120; ly = 500"); b = s.index("SV['endcard'] = (")
s = s[:a] + "lw = 300; lh = lw * 260 / 1595; lx = 120; ly = 530\necx = lx + 145 * lw / 1595; ecy = ly + 151 * lw / 1595\nKX, KY = 330, 680\n" + s[b:]
a = s.index("                 f'<g class=\"reach\" filter=\"url(#tintNight)\">"); b = s.index("                 + dust(271,", a)
hand = r'''                 '<g class="reach" filter="url(#tintNight)"><g transform="translate(250 690)">'
                 '<path d="M -230,330 L -150,330 L 10,22 L -22,-6 Z" fill="#e2c4bc"/>'
                 '<path d="M -230,330 L -196,330 L -14,4 L -22,-6 Z" fill="#f2d9d2"/>'
                 '<ellipse cx="0" cy="0" rx="25" ry="31" transform="rotate(-32)" fill="#e9cdc6"/>'
                 '<path d="M 14,-22 q 18,-10 28,2" stroke="#e9cdc6" stroke-width="11" stroke-linecap="round" fill="none"/>'
                 '<path d="M 20,-10 q 20,-6 30,6" stroke="#e9cdc6" stroke-width="11" stroke-linecap="round" fill="none"/>'
                 '<path d="M 22,3 q 18,-2 26,9" stroke="#e2c4bc" stroke-width="10.5" stroke-linecap="round" fill="none"/>'
                 '<path d="M 18,16 q 14,0 20,9" stroke="#dcbab2" stroke-width="9.5" stroke-linecap="round" fill="none"/>'
                 '<path d="M -6,20 q 20,8 32,-2" stroke="#e2c4bc" stroke-width="11" stroke-linecap="round" fill="none"/>'
                 '<path d="M 6,-16 q 4,14 0,30" stroke="#c9a69e" stroke-width="1.6" fill="none" opacity=".7"/></g></g>'
'''
s = s[:a] + hand + s[b:]
s = s.replace("f'<circle cx=\"{KX}\" cy=\"{KY}\" r=\"150\" fill=\"#cfe0ff\" opacity=\".10\"", "f'<circle cx=\"{KX}\" cy=\"{KY}\" r=\"150\" fill=\"#cfe0ff\" opacity=\".10\"")
open(p, 'w').write(s)

j = open('v2.js').read()
a = j.index("  if (c.key === 'ots') {"); b = j.index("  if (c.key === 'endcard') {")
j = j[:a] + """  if (c.key === 'ots') {
    const turn = t > 0.55; el('.hA').setAttribute('display', turn ? 'none' : 'inline'); el('.hB').setAttribute('display', turn ? 'inline' : 'none');
    const k = ease((t - 1.2) / 1.1), dip = (t > 1.2 && t < 2.3) ? -6 * Math.sin(Math.PI * (t - 1.2) / 1.1) : 0;
    el('.jstep').setAttribute('transform', `translate(${(185 + 10 * k).toFixed(1)} ${(470 - 22 * k + dip).toFixed(1)}) scale(${(2.0 - 0.18 * k).toFixed(3)})`);
  }
""" + j[b:]
a = j.index("    const k = ease(t / 0.4), x = -10 * (1 - k);"); b = j.index("\n", j.index("el('.reach')", a)) + 1
j = j[:a] + "    const k = ease(t / 0.55), x = -70 * (1 - k), y = 90 * (1 - k);\n    el('.reach').setAttribute('transform', `translate(${x.toFixed(1)} ${y.toFixed(1)})`);\n" + j[b:]
open('v2.js', 'w').write(j)
print('patched last two')
