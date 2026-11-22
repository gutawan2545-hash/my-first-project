"""Builds anim.html: the 12 shots with animation hooks (blink, talk, breathe, arms, dust, flicker)
driven by window.setT(shot, t). Also writes anim.json with per-shot durations."""
import runpy, json, re
A = runpy.run_path('all12.py')
ORDER = A['ORDER']; G = A['G']; sub = A['sub']; EN = A['EN']; wlen = A['wlen']


def rep(s, o, n, count=1):
    assert o in s, o[:90]
    return s.replace(o, n, count)


rows = [list(r) for r in ORDER]
# ---- tag moving parts in each shot ----
arm3 = G['arm'] + '<rect x="-36" y="54" width="18" height="34" rx="3" fill="#0c0d14"/><rect x="-34" y="57" width="14" height="27" rx="2" fill="#3a4a8a"/>'
rows[2][4] = rep(rows[2][4], arm3, f'<g class="arm" data-pivot="-57 70" data-amp="7" data-per="1.6">{arm3}</g>')
armJ = A['armJ']; armT = A['armT']
rows[7][4] = rep(rows[7][4], armJ, f'<g class="arm" data-pivot="50 70" data-amp="13" data-per="0.9">{armJ}</g>')
rows[7][4] = rep(rows[7][4], armT, f'<g class="arm" data-pivot="50 70" data-amp="5" data-per="2.2">{armT}</g>')
rows[6][4] = rep(rows[6][4], A['thumb'], f'<g class="press">{A["thumb"]}</g>')
rows[11][4] = rep(rows[11][4], '<g filter="url(#tintNight)"><path d="M0,520', '<g filter="url(#tintNight)" class="reach"><path d="M0,520')
rows[9][4] = rep(rows[9][4], '<g fill="none" stroke="#e2ecff" stroke-width="3" stroke-linecap="round" opacity=".8">', '<g class="pulse" fill="none" stroke="#e2ecff" stroke-width="3" stroke-linecap="round" opacity=".8">')
rows[10][4] = rows[10][4].replace('fill="#e2ecff" opacity="', 'class="note" fill="#e2ecff" opacity="')

# per-shot settings: talk = which character's mouth moves
CFG = [dict(talk='') for _ in rows]
CFG[2]['talk'] = 'J'      # James talks to the bank
CFG[5]['talk'] = 'T'      # Tawan explains the digits
CFG[7]['talk'] = 'J'      # James: "don't!"
durs = []
for i, r in enumerate(rows):
    d = max(3.4, wlen(r[1]) / 11.0 + 1.4) + (1.5 if i == len(rows) - 1 else 0)
    durs.append(round(d, 2))

cards = ''
for i, (t, line, ls, note, svg, info) in enumerate(rows, 1):
    cards += (f'<figure data-i="{i-1}"><svg viewBox="0 0 540 960" role="img" aria-label="ช็อต {i}: {t}"><g class="cam">{svg}</g>'
              f'<g class="info">{info}</g>{sub(ls, EN[i-1])}</svg><figcaption><span class="n">ช็อต {i}</span><b>{t}</b></figcaption></figure>\n')

page = open('storyboard3.html').read()
start = page.index('<div class="grid">') + len('<div class="grid">')
end = page.index('</div></div>\n<script>')
page = page[:start] + cards + page[end:]

# ---- closed-eye lids and talking mouths inside the shared head definitions ----
lidJ = ('<g class="blinkJ"><path d="M -22,-3 C -18,-8.5 -8,-8.5 -4,-2 C -8,1.5 -18,1.5 -22,-3 Z" fill="#fbe7d8"/>'
        '<path d="M 22,-3 C 18,-8.5 8,-8.5 4,-2 C 8,1.5 18,1.5 22,-3 Z" fill="#f6dccb"/>'
        '<path d="M -21,-1.5 C -17,1.2 -9,1.2 -5,-1.2 M 21,-1.5 C 17,1.2 9,1.2 5,-1.2" stroke="#17151d" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>\n')
page = page.replace('    <!-- glasses: round, thin silver wire -->', lidJ + '    <!-- glasses: round, thin silver wire -->')
mouthJ = '<g class="mouthJ"><ellipse cx="1" cy="24.2" rx="4.6" ry="3.4" fill="#6b3a3a"/><ellipse cx="1" cy="25.6" rx="2.6" ry="1.3" fill="#b0605a"/></g>\n'
hp = page.split('    <!-- hair: short, chunky spikes -->')
mouthJS = '<g class="mouthJ"><ellipse cx="0" cy="25.5" rx="6" ry="6.4" fill="#fbe7d8"/><ellipse cx="0" cy="25.6" rx="4.4" ry="2.4" fill="#6b3a3a"/></g>\n'
out = hp[0]
for k, part in enumerate(hp[1:]):
    out += (mouthJ if k == 0 else mouthJS) + '    <!-- hair: short, chunky spikes -->' + part
page = out
lidT = ('<g class="blinkT"><path d="M -23.5,-1.5 C -19,-10 -7,-10 -3,-2 C -8,3.6 -18,3.6 -23.5,-1.5 Z" fill="#f8d2ab"/>'
        '<path d="M 23.5,-1.5 C 19,-10 7,-10 3,-2 C 8,3.6 18,3.6 23.5,-1.5 Z" fill="#f4caa2"/>'
        '<path d="M -22,0 C -17,3.2 -9,3.2 -4,0.2 M -21.5,0.4 L -26,-1.8 M 22,0 C 17,3.2 9,3.2 4,0.2 M 21.5,0.4 L 26,-1.8" stroke="#1a1118" stroke-width="2" fill="none" stroke-linecap="round"/></g>\n')
mouthT = '<g class="mouthT"><ellipse cx="0" cy="23.4" rx="4.6" ry="3.6" fill="#8a3436"/><path d="M -3.6,21.4 Q 0,20.6 3.6,21.4 L 3.2,22.6 Q 0,22 -3.2,22.6 Z" fill="#fff8f0"/></g>\n'
anchor = '    <!-- crown: same outline as the back hair'
parts = page.split(anchor)
assert len(parts) >= 3, len(parts)
# rebuild explicitly: first head (thead) gets mouth+lids, later heads get lids
out = parts[0]
for k, p in enumerate(parts[1:]):
    out += (mouthT + lidT if k == 0 else lidT) + anchor + p
page = out
lidC = ('<g class="blinkC"><path d="M -41,-7 C -36,-21 -14,-21 -9,-6 C -14,4 -36,4 -41,-7 Z" fill="#e79a4a"/>'
        '<path d="M 41,-7 C 36,-21 14,-21 9,-6 C 14,4 36,4 41,-7 Z" fill="#e79a4a"/>'
        '<path d="M -39,-5 C -32,0 -18,0 -11,-4 M 39,-5 C 32,0 18,0 11,-4" stroke="#5a3420" stroke-width="2" fill="none" stroke-linecap="round"/></g>')
for gid in ('eyesSleepy', 'eyesAlert'):
    a = page.index(f'<g id="{gid}">'); b = page.index('\n  </g>', a)
    page = page[:b] + lidC + page[b:]

css = '''<style>
figcaption{display:none}
</style>'''
js = '''<script>
const CFG=%s, DUR=%s;
const S=[...document.querySelectorAll('figure svg')].map((svg,i)=>{
  const cam=svg.querySelector('.cam');
  const dust=[...svg.querySelectorAll('g[filter="url(#moteBlur)"] circle, g[filter="url(#moteGlow)"] circle')].map((c,k)=>({c,k,x:+c.getAttribute('cx'),y:+c.getAttribute('cy'),o:+(c.getAttribute('opacity')||1)}));
  const bodyRefs=['#jbody','#jbodyS','#tbody','#tbodyS','#catSide','#catSideAlert','#sitBody'];
  const bob=[];
  svg.querySelectorAll('use').forEach(u=>{const h=u.getAttribute('href');if(!bodyRefs.includes(h))return;
    let t=u; const p=u.parentNode; if(p.getAttribute&&p.getAttribute('transform')&&!p.classList.contains('cam'))t=p;
    if(!bob.find(b=>b.el===t))bob.push({el:t,base:t.getAttribute('transform')||'',ph:bob.length*1.3,cat:h.startsWith('#cat')||h=='#sitBody'});});
  const arms=[...svg.querySelectorAll('.arm')].map(a=>({el:a,p:a.dataset.pivot,amp:+a.dataset.amp,per:+a.dataset.per}));
  const glow=[...svg.querySelectorAll('[fill*="faceLight"],[fill*="scrGlow"],[fill*="gPhone"],[fill*="coolPool"],[fill*="gLamp"],[fill*="monBeam"]')].map(e=>({el:e,o:+(e.getAttribute('opacity')||1)}));
  const paw=svg.querySelector('g[transform="translate(540,560)"]');
  return {svg,cam,dust,bob,arms,glow,paw,press:svg.querySelector('.press'),reach:svg.querySelector('.reach'),pulse:svg.querySelector('.pulse'),
          notes:[...svg.querySelectorAll('.note')].map(n=>({el:n,base:n.getAttribute('transform')})),info:svg.querySelector('.info'),subs:svg.querySelector('.subs')};
});
const SW={};['blinkJ','blinkT','blinkC','mouthJ','mouthT'].forEach(c=>{SW[c]={els:[...document.querySelectorAll('.'+c)],on:null};SW[c].els.forEach(e=>e.setAttribute('display','none'));});
function setSw(c,on){const w=SW[c];if(w.on===on)return;w.on=on;w.els.forEach(e=>e.setAttribute('display',on?'inline':'none'));}
function blink(t,off,per){const x=(t+off)%%per;return x<0.13;}
window.setT=function(i,t){
  const s=S[i],d=DUR[i],cfg=CFG[i],root=document.body.classList;
  const z=(i%%2==0)?1+0.045*t/d:1.045-0.045*t/d;
  s.cam.setAttribute('transform',`translate(270 480) scale(${z}) translate(-270 -480)`);
  for(const p of s.dust){const k=p.k;
    const dx=7*Math.sin(t*0.7+k*1.9)+((k%%3)-1)*2.5*t, dy=-(5+(k%%5)*1.6)*t+4*Math.sin(t*0.9+k*2.7);
    p.c.setAttribute('cx',(p.x+dx).toFixed(1));p.c.setAttribute('cy',(p.y+dy).toFixed(1));
    p.c.setAttribute('opacity',(p.o*(0.55+0.45*Math.sin(t*2.2+k*2.3))).toFixed(2));}
  for(const b of s.bob){const a=b.cat?2:3.6, w=b.cat?2*Math.PI/2.4:2*Math.PI/3.4;
    const y=a*Math.sin(t*w+b.ph), sc=1+ (b.cat?0.012:0.006)*Math.sin(t*w+b.ph);
    b.el.setAttribute('transform',`translate(0 ${y.toFixed(2)}) ${b.base}`);}
  for(const a of s.arms){const ang=a.amp*Math.sin(t*2*Math.PI/a.per);a.el.setAttribute('transform',`rotate(${ang.toFixed(2)} ${a.p})`);}
  for(const g of s.glow){g.el.setAttribute('opacity',(g.o*(0.9+0.1*Math.sin(t*11)*Math.sin(t*2.7+1))).toFixed(3));}
  if(s.paw){const x=-14*Math.max(0,Math.sin(t*1.6));s.paw.setAttribute('transform',`translate(${(540+x).toFixed(1)},560)`);}
  if(s.press){const k=Math.max(0,Math.sin(t*2*Math.PI/1.3));s.press.setAttribute('transform',`translate(${(-5*k).toFixed(1)} ${(-4*k).toFixed(1)})`);}
  if(s.reach){const k=Math.sin(t*2*Math.PI/2.2);s.reach.setAttribute('transform',`translate(${(8*k).toFixed(1)} ${(-2*k).toFixed(1)})`);}
  if(s.pulse){const k=(t*1.6)%%1;s.pulse.setAttribute('transform',`translate(270 440) scale(${(1+0.25*k).toFixed(3)}) translate(-270 -440)`);s.pulse.setAttribute('opacity',(0.9*(1-k)+0.1).toFixed(2));}
  for(const [n,o] of s.notes.map((o,k)=>[o,k])){const y=-((t*14+o*20)%%60);n.el.setAttribute('transform',`translate(0 ${y.toFixed(1)}) ${n.base}`);}
  setSw('blinkJ',blink(t,0.4,3.1)); setSw('blinkT',blink(t,1.5,3.6)); setSw('blinkC',blink(t,2.2,4.2));
  const talk=(t>0.5&&t<d-0.6)&&Math.sin(t*15)*Math.sin(t*3.7+0.5)>0.05;
  setSw('mouthJ',cfg.talk=='J'&&talk); setSw('mouthT',cfg.talk=='T'&&talk);
  const f=Math.min(1,Math.max(0,(t-0.3)/0.35)); s.info.setAttribute('opacity',f); s.subs.setAttribute('opacity',f);
};
window.showOnly=function(i){document.querySelectorAll('figure').forEach((f,k)=>f.style.display=k==i?'':'none');};
</script>''' % (json.dumps(CFG), json.dumps(durs))
page = page.replace('</style>\n<link', '</style>\n' + css + '\n<link', 1)
page = page + js
open('anim.html', 'w').write(page)
json.dump(durs, open('anim.json', 'w'))
print('anim built', sum(durs))
