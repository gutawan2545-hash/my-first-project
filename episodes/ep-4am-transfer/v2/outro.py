"""Builds the reusable Odd Hours logo outro (2.6 s): outro.html (+ setT) and outro.wav.
The eye in the logo is redrawn in SVG so it can open, look around and blink."""
import base64, wave
import numpy as np

W, H = 540, 960
LW = 380; S = LW / 1595; LH = 260 * S
LX = (W - LW) / 2; LY = 560 - LH / 2              # logo sits a little below the middle
EX, EY = LX + 145 * S, LY + 151 * S               # eye centre (logo.png crop coords 145,151)
RX, RY = 134 * S, 101 * S
AW, AH = 103 * S, 46 * S                          # almond half width / height
PR = 26 * S
logo64 = base64.b64encode(open('logo.png', 'rb').read()).decode()

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
<radialGradient id="bg" cx="50%" cy="58%" r="75%"><stop offset="0" stop-color="#1c1430"/><stop offset=".55" stop-color="#0d0a16"/><stop offset="1" stop-color="#050408"/></radialGradient>
<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#8a3dff" stop-opacity=".55"/><stop offset="1" stop-color="#8a3dff" stop-opacity="0"/></radialGradient>
<clipPath id="almond"><path d="M {EX-AW:.1f},{EY:.1f} C {EX-AW*0.45:.1f},{EY-AH*1.25:.1f} {EX+AW*0.45:.1f},{EY-AH*1.25:.1f} {EX+AW:.1f},{EY:.1f} C {EX+AW*0.45:.1f},{EY+AH*1.25:.1f} {EX-AW*0.45:.1f},{EY+AH*1.25:.1f} {EX-AW:.1f},{EY:.1f} Z"/></clipPath>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter>
<filter id="grain" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="9"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle id="glowc" cx="{EX:.1f}" cy="{EY:.1f}" r="120" fill="url(#glow)" opacity="0"/>
<g id="motes" fill="#e6d6ff"></g>
<g id="logo" opacity="0">
  <image href="data:image/png;base64,{logo64}" x="{LX:.1f}" y="{LY:.1f}" width="{LW}" height="{LH:.1f}"/>
  <ellipse cx="{EX:.1f}" cy="{EY:.1f}" rx="{RX:.1f}" ry="{RY:.1f}" fill="#7a1fff"/>
  <g id="eye" transform="translate({EX:.1f} {EY:.1f}) scale(1 0.06) translate({-EX:.1f} {-EY:.1f})">
    <path d="M {EX-AW:.1f},{EY:.1f} C {EX-AW*0.45:.1f},{EY-AH*1.25:.1f} {EX+AW*0.45:.1f},{EY-AH*1.25:.1f} {EX+AW:.1f},{EY:.1f} C {EX+AW*0.45:.1f},{EY+AH*1.25:.1f} {EX-AW*0.45:.1f},{EY+AH*1.25:.1f} {EX-AW:.1f},{EY:.1f} Z" fill="#05040a"/>
    <g clip-path="url(#almond)"><circle id="pupil" cx="{EX:.1f}" cy="{EY:.1f}" r="{PR:.1f}" fill="#d6b0ff"/></g>
  </g>
</g>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".05" style="mix-blend-mode:screen"/>
</svg>'''

js = f'''<script>
const EX={EX:.2f}, EY={EY:.2f}, AW={AW:.2f};
const ease=x=>x<=0?0:x>=1?1:x*x*(3-2*x), clamp=x=>Math.max(0,Math.min(1,x));
const motes=document.getElementById('motes');
const M=[...Array(18)].map((_,k)=>{{const c=document.createElementNS('http://www.w3.org/2000/svg','circle');
  const r=Math.sin(k*12.9898)*43758.5453; const fr=r-Math.floor(r);
  c.setAttribute('r',(0.7+1.6*((k*7)%5)/5).toFixed(1)); if(k%3==0)c.setAttribute('filter','url(#soft)'); motes.appendChild(c);
  return {{c,k,x:120+300*fr,y:380+300*((k*0.37)%1),o:0.3+0.5*((k*0.53)%1)}};}});
window.setT=function(t){{
  const fade=clamp(t/0.35);
  document.getElementById('logo').setAttribute('opacity',fade.toFixed(2));
  document.getElementById('glowc').setAttribute('opacity',(fade*(0.55+0.15*Math.sin(t*3))).toFixed(2));
  // eye: opens 0.45-0.7, blinks at 1.85, otherwise open
  let open = t<0.45?0.06 : t<0.7? 0.06+0.94*ease((t-0.45)/0.25) : 1;
  if(t>1.85&&t<2.0) open = 0.06 + 0.94*Math.abs((t-1.925)/0.075);
  document.getElementById('eye').setAttribute('transform',`translate(${{EX}} ${{EY}}) scale(1 ${{open.toFixed(3)}}) translate(${{-EX}} ${{-EY}})`);
  // pupil glances left, then right, then back to centre
  let px=0; if(t>0.8&&t<1.75){{const u=(t-0.8)/0.95; px = u<0.4? -0.42*AW*ease(u/0.4) : u<0.8? -0.42*AW+0.84*AW*ease((u-0.4)/0.4) : 0.42*AW*(1-ease((u-0.8)/0.2));}}
  document.getElementById('pupil').setAttribute('cx',(EX+px).toFixed(2));
  for(const p of M){{const dx=6*Math.sin(t*0.8+p.k), dy=-(6+(p.k%4)*2)*t;
    p.c.setAttribute('cx',(p.x+dx).toFixed(1)); p.c.setAttribute('cy',(p.y+dy).toFixed(1));
    p.c.setAttribute('opacity',(fade*p.o*(0.6+0.4*Math.sin(t*2.4+p.k*2))).toFixed(2));}}
}};
setT(1.0);
</script>'''
open('outro.html', 'w').write(f'<!doctype html><meta charset="utf-8"><title>Odd Hours outro</title><style>html,body{{margin:0;background:#000}}svg{{display:block;width:540px;height:960px}}</style>{svg}{js}')

# ---- outro sound: soft whoosh in, low swell, tiny tick on the blink ----
SR = 48000; D = 2.6; N = int(SR * D); t = np.arange(N) / SR
rng = np.random.default_rng(2)
noise = rng.standard_normal(N)
k = np.ones(200) / 200
air = np.convolve(noise, k, mode='same') * 4
env = np.clip(t / 0.35, 0, 1) * np.exp(-np.clip(t - 0.35, 0, None) * 3)
swell = (np.sin(2 * np.pi * 73.4 * t) + 0.5 * np.sin(2 * np.pi * 110 * t)) * np.clip(t / 0.6, 0, 1) * np.exp(-np.clip(t - 0.8, 0, None) * 1.3)
tick = np.zeros(N); i = int(1.86 * SR); n = int(0.05 * SR)
tick[i:i + n] = np.sin(2 * np.pi * 1800 * np.arange(n) / SR) * np.exp(-np.arange(n) / SR * 90)
mix = air * env * 0.12 + swell * 0.14 + tick * 0.18
mix[-int(0.25 * SR):] *= np.linspace(1, 0, int(0.25 * SR))
pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
with wave.open('outro.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('outro built')
