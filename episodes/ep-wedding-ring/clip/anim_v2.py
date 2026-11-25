"""ช่วงทดลองแอนิเมชัน (ช็อต 3-9 ฉากผู้หญิงชุดดำเปิดประตูเข้ามา)
ตัวละครมีชีวิต: กะพริบตา ขยับปากตามเสียงคนพูด หัวขยับ เดินเข้าฉาก ชี้มือ เปลี่ยนสีหน้า ตัวสั่น
เพิ่มช็อตปฏิกิริยานางเอก (คนฟังต้องมีปฏิกิริยา) · เสียงพากย์ใส่อารมณ์ · ดนตรีและเสียงประกอบสังเคราะห์
รัน: python3 anim_test.py -> anim_test.html + out/test_audio.wav แล้ว node render_anim.js แล้ว ffmpeg รวม"""
import os, sys, re, json, math, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'storyboard'))
import storyboard as SB                      # ฉาก ตัวละคร และ defs ที่ทำไว้แล้ว
import audiolib as A
import supporting as SP
import wedding_chars as WC
sys.path.insert(0, HERE)
from subs import thai_lines, EN
os.chdir(HERE)
FPS = 24

# ---------------------------------------------------------------- หัวเจ้าบ่าวตอนโกรธ + ตัวที่แยกแขนขวาออกมาขยับได้
gh = re.search(r'<g id="ghead">.*?\n  </g>', WC.GROOM_HEAD, re.S).group(0).replace('<g id="ghead">', '<g id="ghead_angry">')
gh = gh.replace('<path d="M -23,-14.5 L -7,-11.6 L -7.4,-8.8 L -22,-11.2 Z" fill="#141218"/>', '<path d="M -23,-16.5 L -6.6,-9.4 L -7.4,-6.4 L -22,-13 Z" fill="#141218"/>')
gh = gh.replace('<path d="M 23,-14.5 L 7,-11.6 L 7.4,-8.8 L 22,-11.2 Z" fill="#141218"/>', '<path d="M 23,-16.5 L 6.6,-9.4 L 7.4,-6.4 L 22,-13 Z" fill="#141218"/>')
i = gh.index('    <!-- thin closed-mouth smirk'); j = gh.index('    <!-- neat comma hair')
gh = gh[:i] + ('    <path d="M -8,21 Q 0,19 8,21 Q 7,30 0,30 Q -7,30 -8,21 Z" fill="#5a1a22"/><path d="M -7,21.4 Q 0,19.8 7,21.4 L 6.4,23.6 Q 0,22.4 -6.4,23.6 Z" fill="#fff"/>'
               '<path d="M -8,21 Q 0,19 8,21" fill="none" stroke="#8a4a46" stroke-width="1.4"/>\n') + gh[j:]
gb = WC.groom_body()
ARM_PARTS = [p for p in re.findall(r'<[^>]+/>', gb) if any(k in p for k in ('-58,226', '-59,229', 'x="-59"', 'cx="-51.5"', '-58,96'))]
for p in ARM_PARTS: gb = gb.replace(p, '', 1)
GROOM_ARM = ''.join(ARM_PARTS)

# ---------------------------------------------------------------- ชิ้นส่วนขยับได้
def blink(p, skin, ex=13, ey=-1.6, rx=10, ry=7, scale=None):
    g = (f'<g id="{p}B" display="none">' + ''.join(
        f'<ellipse cx="{s * ex}" cy="{ey}" rx="{rx}" ry="{ry}" fill="{skin}"/><path d="M {s * (ex + 9)},{ey + .5} Q {s * ex},{ey + 4} {s * (ex - 9)},{ey + .5}" fill="none" stroke="#1c1214" stroke-width="1.6" stroke-linecap="round"/>'
        for s in (-1, 1)) + '</g>')
    return f'<g transform="{scale}">{g}</g>' if scale else g
def mouth(p, skin, lip, scale=None):
    g = (f'<g id="{p}M" display="none"><ellipse cx="0" cy="24.2" rx="8.8" ry="5" fill="{skin}"/>'
         f'<ellipse id="{p}Mo" cx="0" cy="24.4" rx="4.6" ry="2" fill="#4a1420" stroke="{lip}" stroke-width="1.8"/>'
         f'<rect id="{p}Mt" x="-3" y="22.6" width="6" height="1.4" rx=".6" fill="#ffffff"/></g>')
    return f'<g transform="{scale}">{g}</g>' if scale else g
TEARS = lambda p: (f'<g id="{p}T" display="none"><path d="M -14,4 C -15,12 -13,20 -15,30" stroke="#cfe0ff" stroke-width="2" fill="none" opacity=".85"/>'
                   f'<path d="M 14,4 C 15,12 13,20 15,30" stroke="#cfe0ff" stroke-width="2" fill="none" opacity=".85"/><circle cx="-15" cy="31" r="1.8" fill="#e6f0ff"/></g>')

def bride_rig(p, heads=('b2head', 'b2head_worry', 'b2head_scared')):
    hs = ''.join(f'<use id="{p}H{k}" href="#{h}" display="{"inline" if k == 0 else "none"}"/>' for k, h in enumerate(heads))
    return (f'<g id="{p}"><use href="#b2back"/>{WC.bride_body()}<g id="{p}H">{hs}{blink(p, "#fbe2cf")}{TEARS(p)}</g></g>', 462)
def woman_rig(p):
    n, nt, kind, back, head, body = SP.c_woman_black()
    sc = 'scale(.87 1.03)'
    return (f'<g id="{p}">{back}{body}<g id="{p}H">{head}{blink(p, "#f1d8cc", scale=sc)}{mouth(p, "#f1d8cc", "#8e2236", scale=sc)}</g></g>', 460)
def groom_rig(p, heads=('ghead', 'ghead_angry')):
    hs = ''.join(f'<use id="{p}H{k}" href="#{h}" display="{"inline" if k == 0 else "none"}"/>' for k, h in enumerate(heads))
    return (f'<g id="{p}">{gb}<g id="{p}A">{GROOM_ARM}</g><g id="{p}H">{hs}{blink(p, "#f6dcc8", 12, -1.6, 9.6, 5.4)}'
            f'<path d="M -12,49 C -8,59 8,59 12,49" fill="none" stroke="#d8d4ce" stroke-width="2"/></g></g>', 488)
def guard_rig(p):
    n, nt, kind, back, head, body = SP.c_guard()
    return (f'<g id="{p}">{back}{body}<g id="{p}H">{head}{blink(p, "#ecc4a2", 12, -1.6, 9.6, 5.4, scale="scale(.88 1.03)")}</g></g>', 488)

from rigs import bride_rig, woman_rig, groom_rig, guard_rig

def placed(rig, x, feet, s):
    body, lf = rig
    return f'<g data-lf="{lf}" data-x="{x}" data-feet="{feet}" data-s="{s}" class="place">{body}</g>'

CAST_NO = lambda *ks: {k: v for k, v in SB.CAST.items() if k not in ks}
BX, BY = SB.bx, SB.by; GX, GY = SB.gx, SB.gy
WF = SB.WB_FACE

# ---------------------------------------------------------------- เสียงพากย์และไทม์ไลน์
VO = {k: A.load_voice(os.path.join(HERE, 'vo', f'{k}.mp3')) for k in ('01c', '03c', '04c', '05c', '06e', '07g', '08c', '09e')}
D = {k: len(v) / A.SR for k, v in VO.items()}
TB = .3 + D['04c'] - .35                  # เสียงปังตรงคำว่า "เปิดออก"
S7_SPLIT = .3 + D['07g'] + .35          # เจ้าบ่าวพูดจบในช็อตตัวเองก่อน แล้วค่อยตัดไป รปภ. เดินเข้ามา
G7_POINT = .3 + D['07g'] * .66            # ชี้ตอนพูดว่า "เจ้าหน้าที่ครับ"
SHOTS = [
    ('s1', .5 + D['01c'] + .9), ('s3', .4 + D['03c'] + .5), ('s4', TB + 2.3), ('s4r', 1.8), ('s5', .4 + D['05c'] + .6), ('s6', .4 + D['06e'] + .5),
    ('s6r', 2.3), ('s7a', S7_SPLIT), ('s7b', 3.0), ('s8', .4 + D['08c'] + .4), ('s9', .4 + D['09e'] + .6), ('s9r', 2.6)]
T0 = {}; t = 0
for k, d in SHOTS: T0[k] = t; t += d
TOTAL = t
VOICE_AT = {'01c': T0['s1'] + .5, '03c': T0['s3'] + .4, '04c': T0['s4'] + .3, '05c': T0['s5'] + .4, '06e': T0['s6'] + .4, '07g': T0['s7a'] + .3, '08c': T0['s8'] + .4, '09e': T0['s9'] + .4}
SPEAKER = {'06e': 'w6', '09e': 'w9', '07g': 'g7'}
ENV = {k: A.envelope_fps(VO[k], FPS) for k in SPEAKER}

# ---------------------------------------------------------------- ฉากแต่ละช็อต
def shot_svg(sid, content):
    return f'<svg id="{sid}" class="shot" viewBox="0 0 540 960" display="none"><g id="{sid}c">{content}</g><rect id="{sid}f" width="540" height="960" fill="#ffffff" opacity="0"/><rect id="{sid}k" width="540" height="960" fill="#000" opacity="0"/></svg>'
# ฉากหลังที่ไม่ขยับ เรนเดอร์เป็นภาพครั้งเดียว (render_bg.js) แล้วใช้เป็น <image> ทำให้เรนเดอร์ทีละเฟรมเร็วขึ้นมาก
BG = {'hall_nbg': SB.hall(CAST_NO('bride', 'groom')), 'hall_nb': SB.hall(CAST_NO('bride')), 'hall_ng': SB.hall(CAST_NO('groom')),
      'hall_nb_cool': SB.hall(CAST_NO('bride'), cool=.15), 'door_closed': SB.doors('closed'), 'door_half': SB.doors('half'), 'door_open': SB.doors('open')}
def img(name): return f'<image href="bg/{name}.jpg" width="540" height="960" preserveAspectRatio="none"/>'
door_open = img('door_open')
SVGS = [
    shot_svg('s1', img('hall_nbg') + placed(bride_rig('b1'), *SB.CAST['bride']) + placed(groom_rig('g1'), *SB.CAST['groom'])),
    shot_svg('s3', img('hall_nbg') + placed(bride_rig('b3'), *SB.CAST['bride']) + placed(groom_rig('g3'), *SB.CAST['groom'])),
    shot_svg('s4', f'<g id="d4c">{img("door_closed")}</g><g id="d4h" display="none">{img("door_half")}</g><g id="d4o" display="none">{door_open}</g>'),
    shot_svg('s4r', img('hall_nb') + placed(bride_rig('b4'), *SB.CAST['bride'])),
    shot_svg('s5', door_open + placed(woman_rig('w5'), 270, SB.DOOR_FEET, SB.DOOR_S) + f'<g id="ring5" display="none">{SB.inset_ring()}</g>'),
    shot_svg('s6', door_open + placed(woman_rig('w6'), 270, SB.DOOR_FEET, SB.DOOR_S)),
    shot_svg('s6r', img('hall_nb') + placed(bride_rig('b6'), *SB.CAST['bride'])),
    shot_svg('s7a', img('hall_ng') + placed(groom_rig('g7'), *SB.CAST['groom'])),
    shot_svg('s7b', door_open + placed(woman_rig('w7'), 246, SB.DOOR_FEET, SB.DOOR_S) + placed(guard_rig('k7'), 600, SB.DOOR_FEET + 4, SB.DOOR_S)),
    shot_svg('s8', door_open + placed(woman_rig('w8'), 246, SB.DOOR_FEET, SB.DOOR_S) + placed(guard_rig('k8'), 312, SB.DOOR_FEET + 4, SB.DOOR_S)),
    shot_svg('s9', door_open + placed(woman_rig('w9'), 270, SB.DOOR_FEET, SB.DOOR_S)),
    shot_svg('s9r', img('hall_nb_cool') + placed(bride_rig('b9'), *SB.CAST['bride'])),
]

# ---------------------------------------------------------------- ซับแบบตั้งเวลา (ไทย + อังกฤษ)
SUB_TXT = {'01c': 1, '03c': 3, '04c': 4, '05c': 5, '06e': 6, '07g': 7, '08c': 8, '09e': 9}
subs = []; sub_svg = []
script = {int(m.group(1)): m.group(2) for m in (re.match(r'^(\d+)\. (.*)$', l.strip()) for l in open('../script.md')) if m}
def clean(t): return re.sub(r'\[[^\]]*\]\s*', '', re.sub(r'^\(.*?\)\s*', '', t)).replace('"', '').strip()
for key, n in SUB_TXT.items():
    ls = thai_lines(clean(script[n])); groups = [ls[i:i + 2] for i in range(0, len(ls), 2)]
    words = EN[n].split(' '); tot = sum(len(''.join(g)) for g in groups); acc = 0; wi = 0
    for gi, g in enumerate(groups):
        a0 = VOICE_AT[key] + D[key] * acc / tot - .1; acc += len(''.join(g)); a1 = VOICE_AT[key] + D[key] * acc / tot + (.4 if gi == len(groups) - 1 else 0)
        upto = len(words) if gi == len(groups) - 1 else round(len(words) * acc / tot); en = ' '.join(words[wi:upto]); wi = upto
        el = []; cur = ''
        for w in en.split(' '):
            if len(cur) + len(w) > 44 and cur: el.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        if cur: el.append(cur)
        block = len(g) * 27 + 6 + len(el) * 17; y0 = 712 - block / 2 + 20
        th = ''.join(f'<text x="270" y="{y0 + i * 27:.0f}" class="th">{l}</text>' for i, l in enumerate(g))
        ye = y0 + (len(g) - 1) * 27 + 23
        enx = ''.join(f'<text x="270" y="{ye + i * 17:.0f}" class="en">{l}</text>' for i, l in enumerate(el[:3]))
        sid = f'sub{len(subs)}'; subs.append((round(a0, 3), round(a1, 3), sid)); sub_svg.append(f'<g id="{sid}" display="none">{th}{enx}</g>')

# ---------------------------------------------------------------- JS ขับการเคลื่อนไหวทุกเฟรม
JS = r'''
const SH = %(shots)s, T0 = %(t0)s, ENV = %(env)s, VAT = %(vat)s, SUBS = %(subs)s, FPS = %(fps)s;
const $ = id => document.getElementById(id);
function place(el, dx, dfeet, ds, rot) {
  const lf = +el.dataset.lf, x = +el.dataset.x + (dx||0), feet = +el.dataset.feet + (dfeet||0), s = +el.dataset.s * (ds||1);
  el.setAttribute('transform', `translate(${x},${feet - lf * s}) scale(${s}) rotate(${rot||0} 0 ${lf})`);
}
function P(rig) { return $(rig).parentNode; }
function head(rig, ang, dy) { $(rig + 'H').setAttribute('transform', `translate(0,${dy||0}) rotate(${ang||0} 0 40)`); }
function blinkAt(rig, t, per, off, force) { const c = force || ((t + off) %% per) < .13; $(rig + 'B').setAttribute('display', c ? 'inline' : 'none'); }
function face(rig, k, n) { for (let i = 0; i < n; i++) { const u = $(rig + 'H' + i); if (u) u.setAttribute('display', i === k ? 'inline' : 'none'); } }
function talk(rig, key, gt) {
  const e = ENV[key], i = Math.floor((gt - VAT[key]) * FPS), m = $(rig + 'M');
  if (!e || i < 0 || i >= e.length) { m.setAttribute('display', 'none'); return; }
  const a = e[i];
  if (a < .1) { m.setAttribute('display', 'none'); return; }
  m.setAttribute('display', 'inline'); $(rig + 'Mo').setAttribute('ry', (1.1 + a * 4.4).toFixed(2)); $(rig + 'Mo').setAttribute('rx', (4 + a * 1.4).toFixed(2));
  $(rig + 'Mt').setAttribute('display', a > .35 ? 'inline' : 'none');
}
function cam(sid, z, cx, cy, ty, sx, sy) { $(sid + 'c').setAttribute('transform', `translate(${270 - cx * z + (sx||0)},${(ty||400) - cy * z + (sy||0)}) scale(${z})`); }
const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
const lerp = (a, b, x) => a + (b - a) * x;
function shake(t, t0, d, amp) { if (t < t0 || t > t0 + d) return [0, 0]; const q = 1 - (t - t0) / d; return [Math.sin(t * 90) * amp * q, Math.cos(t * 77) * amp * q]; }
function flash(sid, t, list) { let o = 0; for (const [a, d] of list) if (t >= a && t < a + d) o = Math.max(o, .85 * (1 - (t - a) / d)); $(sid + 'f').setAttribute('opacity', o.toFixed(3)); }
function arm(p, side, a, b) { const u = $(p + side + 'U'); if (!u) return; u.setAttribute('transform', `rotate(${a} ${u.dataset.sx} ${u.dataset.sy})`);
  const f = $(p + side + 'F'); f.setAttribute('transform', `rotate(${b} ${f.dataset.ex} ${f.dataset.ey})`); }
const backOut = x => { x = Math.min(1, Math.max(0, x)); const c = 1.6; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
function pose(p, from, to, k) { const e = backOut(k); arm(p, 'L', lerp(from[0], to[0], e), lerp(from[1], to[1], e)); arm(p, 'R', lerp(from[2], to[2], e), lerp(from[3], to[3], e)); }
function idleArms(p, t, ph) { arm(p, 'L', 1.6 * Math.sin(t * .9 + ph), -5 - 2.5 * Math.sin(t * 1.1 + ph)); arm(p, 'R', -1.6 * Math.sin(t * .8 + ph), 5 + 2.5 * Math.sin(t * 1.2 + ph)); }
function env(key, gt) { const e = ENV[key]; if (!e) return 0; const i = Math.floor((gt - VAT[key]) * FPS); return (i >= 0 && i < e.length) ? e[i] : 0; }
function breathe(p, t, amp, rate, sway) { place(P(p), 0, 0, 1 + amp * Math.sin(t * rate), sway * Math.sin(t * .45)); }
const CLASP = [-12, -18, 12, 18], SHOCK = [-28, -138, 10, 140], RELAX = [0, -5, 0, 5], RINGUP = [0, -5, 15, 122], CHEST = [0, -5, 12, 128];
const R = { // การแสดงของแต่ละช็อต: t = เวลาในช็อต, gt = เวลารวม
  s1(t, gt) { cam('s1', lerp(1.0, 1.75, ease(t / SH.s1)), lerp(270, %(cx3)s, ease(t / SH.s1)), lerp(520, %(cy3)s, ease(t / SH.s1)), lerp(480, 380, ease(t / SH.s1)));
    blinkAt('b1', t, 3.4, .7); blinkAt('g1', t, 3.9, 2.1); breathe('b1', t, .005, 2.0, .6); breathe('g1', t, .004, 1.8, -.4);
    const k = (t - 2.0) / .9; if (t < 2.0) pose('b1', CLASP, CLASP, 1); else pose('b1', CLASP, [-12, -18, 26, 96], k);
    head('b1', 3 + 1.5 * Math.sin(t * 1.0), 0); idleArms('g1', t, .5); head('g1', -2 - Math.sin(t * .8), 0);
    if (t > SH.s1 - 3) { face('b1', 1, 3); head('b1', lerp(3, -5, ease((t - SH.s1 + 3) / .8)), 0); } else face('b1', 0, 3); },
  s3(t, gt) { cam('s3', lerp(2.0, 2.25, t / SH.s3), %(cx3)s, %(cy3)s, 360); blinkAt('b3', t, 3.1, .4); blinkAt('g3', t, 3.7, 1.6);
    breathe('b3', t, .005, 2.2, .7); breathe('g3', t, .004, 1.9, -.5);
    pose('b3', CLASP, CLASP, 1); arm('b3', 'L', -12 + 1.5 * Math.sin(t * 1.3), -18 - 3 * Math.sin(t * 1.3)); arm('b3', 'R', 12 - 1.5 * Math.sin(t * 1.3), 18 + 3 * Math.sin(t * 1.3));
    head('b3', 3.5 + 1.8 * Math.sin(t * 1.1), 0); idleArms('g3', t, 1); head('g3', -2.5 - 1.2 * Math.sin(t * .9 + 1), 0);
    face('g3', t > SH.s3 - 2 ? 2 : 0, 3); },
  s4(t, gt) { const tb = %(tb)s; $('d4c').setAttribute('display', t < tb ? 'inline' : 'none'); $('d4h').setAttribute('display', t >= tb && t < tb + .12 ? 'inline' : 'none'); $('d4o').setAttribute('display', t >= tb + .12 ? 'inline' : 'none');
    const [sx, sy] = shake(t, tb, .7, 26); cam('s4', lerp(1.0, 1.08, t / SH.s4), 270, 480, 480, sx, sy); flash('s4', t, [[tb + .75, .2], [tb + 1.05, .14]]); },
  s4r(t, gt) { cam('s4r', lerp(2.6, 2.9, t / SH.s4r), %(bx)s, %(by)s + 40, 400); face('b4', t < .12 ? 0 : 2, 3); $('b4B').setAttribute('display', t < .1 ? 'inline' : 'none');
    pose('b4', CLASP, SHOCK, (t - .05) / .28); head('b4', -1.5 + (Math.random() - .5) * 1.2, -3.5 * ease(t / .2)); breathe('b4', t, .012, 10, 0); },
  s5(t, gt) { const p = ease(t / 3.6), ph = t * Math.PI * 1.7, walking = 1 - ease((t - 3.4) / .3), step = Math.abs(Math.sin(ph)) * walking;
    const el = P('w5'); el.dataset.feet = lerp(610, %(df)s, p); el.dataset.s = lerp(.30, %(ds)s, p);
    place(el, 1.5 * Math.sin(ph) * walking, -6 * step, 1, 1.6 * Math.sin(ph) * walking);
    $('w5Body').setAttribute('transform', `skewX(${1.8 * Math.sin(ph + .6) * walking})`);
    head('w5', -1.4 * Math.sin(ph) * walking, 0); blinkAt('w5', t, 3.3, 1.2); $('w5M').setAttribute('display', 'none');
    const rt = %(ringt)s;
    if (t < rt - .3) { arm('w5', 'L', 7 * Math.sin(ph) * walking, -8); arm('w5', 'R', 7 * Math.sin(ph) * walking, 8); }
    else if (t < rt + 1.9) pose('w5', RELAX, RINGUP, (t - rt + .3) / .45);
    else pose('w5', RINGUP, RELAX, (t - rt - 1.9) / .6);
    $('ring5').setAttribute('display', t > rt && t < rt + 2.2 ? 'inline' : 'none'); cam('s5', lerp(1.0, 1.12, t / SH.s5), 270, 560, 560); },
  s6(t, gt) { cam('s6', lerp(2.6, 2.95, t / SH.s6), %(wfx)s, %(wfy)s + 70, 400); blinkAt('w6', t, 3.4, .9); const e = env('06e', gt);
    head('w6', 1.2 * Math.sin(t * .8) + 3 * e, -1.6 * e); talk('w6', '06e', gt); breathe('w6', t, .004, 1.7, .5);
    const k0 = SH.s6 * .58; if (t < k0) idleArms('w6', t, 0); else pose('w6', RELAX, CHEST, (t - k0) / .4); },
  s6r(t, gt) { cam('s6r', lerp(2.8, 3.2, t / SH.s6r), %(bx)s, %(by)s + 40, 400); face('b6', t < .9 ? 2 : 1, 3); blinkAt('b6', t, .9, .5, t > 1.0 && t < 1.25);
    if (t < 1.1) pose('b6', SHOCK, SHOCK, 1); else pose('b6', SHOCK, CLASP, (t - 1.1) / .7);
    head('b6', (Math.random() - .5) * (t < .9 ? 1.6 : .5) + (t > .9 ? -3 * ease((t - .9) / .6) : 0), 0); breathe('b6', t, t < 1 ? .012 : .007, t < 1 ? 9 : 4, 0); },
  s7a(t, gt) { const tp = %(gpt)s; cam('s7a', lerp(2.1, 2.35, t / SH.s7a), %(gx)s, %(gy)s + 110, 420); blinkAt('g7', t, 3.9, 2.2);
    const e = env('07g', gt); talk('g7', '07g', gt); face('g7', t < tp - .1 ? 0 : 1, 3);
    if (t < tp - .35) { const c = backOut((t - .3) / .5), w = 4 * Math.sin(t * 2.4);   // มือสองข้างกางออกตรงหน้า ท่าบอกให้ใจเย็น
      arm('g7', 'L', lerp(0, 12, c) + w, lerp(0, -38, c)); arm('g7', 'R', lerp(-6, -12, c) - w, lerp(22, 38, c)); }
    else { const wind = -14 * Math.sin(Math.PI * Math.min(1, Math.max(0, (t - tp + .35) / .25)));
      const a = t < tp ? wind : lerp(0, 74, backOut((t - tp) / .35)) + (t > tp + .4 ? 2.5 * Math.sin(t * 13) : 0);
      arm('g7', 'L', a, t < tp ? -38 : -6); arm('g7', 'R', lerp(-12, -6, ease((t - tp + .35) / .4)), lerp(38, 22, ease((t - tp + .35) / .4))); }
    head('g7', (t < tp ? 1.5 * Math.sin(t * 1.3) : 3 * Math.sin(t * 9) * Math.max(0, 1 - (t - tp) / 1.2)) + 2.5 * e, -1.2 * e); place(P('g7'), 0, 0, 1, t > tp ? -1.8 : 0); },
  s7b(t, gt) { cam('s7b', lerp(1.35, 1.45, t / SH.s7b), 270, 590, 480); const p = ease(t / 2.2), ph = t * Math.PI * 2, step = Math.abs(Math.sin(ph)) * (1 - p);
    const el = P('k7'); el.dataset.x = lerp(600, 316, p); place(el, 0, -5 * step, 1, 1.2 * Math.sin(ph) * (1 - p));
    if (t < 2.2) { arm('k7', 'L', 8 * Math.sin(ph) * (1 - p), -6); arm('k7', 'R', -8 * Math.sin(ph) * (1 - p), 6); } else pose('k7', RELAX, [38, -24, 0, 5], (t - 2.2) / .4);
    blinkAt('w7', t, 3.1, .3); blinkAt('k7', t, 4.2, 1.1); head('w7', -4 * ease((t - 1.8) / .5), 0); $('w7M').setAttribute('display', 'none');
    if (t < 2.3) idleArms('w7', t, 2); else pose('w7', RELAX, [-6, -40, 4, 20], (t - 2.3) / .35); place(P('w7'), 0, 0, 1, t > 2.3 ? -1.2 : 0); },
  s8(t, gt) { cam('s8', lerp(1.7, 1.95, t / SH.s8), 270, 600, 430); head('w8', lerp(-5, 1, ease((t - 1.2) / 1.6)), 0); blinkAt('w8', t, 3.6, 2.4); blinkAt('k8', t, 4.0, .6);
    $('w8M').setAttribute('display', 'none'); pose('k8', [38, -24, 0, 5], [38, -24, 0, 5], 1); pose('w8', [-6, -40, 4, 20], [-6, -40, 4, 20], 1); breathe('w8', t, .004, 1.6, .4); },
  s9(t, gt) { cam('s9', lerp(4.6, 5.1, t / SH.s9), %(wfx)s, %(wfy)s + 6, 380); blinkAt('w9', t, 3.9, 2.8); const e = env('09e', gt);
    head('w9', .8 * Math.sin(t * .7) + 2.5 * e, -1.4 * e); talk('w9', '09e', gt); flash('s9', t, [[2.1, .18]]); },
  s9r(t, gt) { cam('s9r', lerp(3.0, 3.6, t / SH.s9r), %(bx)s, %(by)s + 40, 400); face('b9', 1, 3); blinkAt('b9', t, 1.3, .9);
    pose('b9', CLASP, [-26, -132, 10, 140], (t - .4) / .5); head('b9', -2 + (Math.random() - .5) * .8, Math.sin(t * 7) * .8);
    breathe('b9', t, .01, 7, 0); $('b9T').setAttribute('display', t > .8 ? 'inline' : 'none');
    $('s9rk').setAttribute('opacity', Math.max(0, (t - (SH.s9r - .7)) / .7).toFixed(3)); },
};
window.renderAt = function (gt) {
  let cur = null;
  for (const k of Object.keys(SH)) { if (gt >= T0[k] && gt < T0[k] + SH[k]) cur = k; }
  if (!cur) cur = Object.keys(SH).pop();
  document.querySelectorAll('svg.shot').forEach(s => s.setAttribute('display', s.id === cur ? 'inline' : 'none'));
  document.querySelectorAll('.place').forEach(el => { if (!el.dataset.init) { el.dataset.init = 1; place(el); } });
  R[cur](gt - T0[cur], gt);
  for (const [a, b, id] of SUBS) $(id).setAttribute('display', gt >= a && gt < b ? 'inline' : 'none');
};
'''
js = JS % dict(shots=json.dumps(dict(SHOTS)), t0=json.dumps(T0), env=json.dumps(ENV), vat=json.dumps(VOICE_AT), subs=json.dumps(subs), fps=FPS,
               cx3=(BX + GX) / 2, cy3=BY + 60, tb=TB, bx=BX, by=BY + 40, gx=GX, gy=GY, df=SB.DOOR_FEET, ds=SB.DOOR_S, ringt=.4 + D['05c'] * .55,
               wfx=WF[0], wfy=WF[1], gpt=G7_POINT)

base = SB.N9.H8.S.DEFS
for gid in ('drapeShadeL', 'drapeShadeR', 'glass4', 'vig4'):
    base = re.sub(rf'<(linear|radial)Gradient id="{gid}".*?</\1Gradient>', '', base, flags=re.S)
DEFS = (base + SB.H8.DEFS_EXTRA + SB.N9.EXTRA_DEFS + WC.DEFS + SB.B2.DEFS + SP.DEFS + SB.P2.DEFS2 + SB.EXTRA_DEFS + SB.CHAR_DEFS
        + f'<svg width="0" height="0" style="position:absolute"><defs>{gh}</defs></svg>')
html = ('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=Inter:wght@600&family=IBM+Plex+Mono:wght@500&display=swap">'
        '<style>html,body{margin:0;background:#000}#stage{position:relative;width:540px;height:960px;overflow:hidden}#stage svg{position:absolute;inset:0;width:540px;height:960px}'
        '.th{font-family:"IBM Plex Sans Thai";font-weight:700;font-size:20px;fill:#c04dff;stroke:#12081c;stroke-width:5px;paint-order:stroke;stroke-linejoin:round;text-anchor:middle}'
        '.en{font-family:Inter,sans-serif;font-weight:600;font-size:13px;fill:#fff;stroke:#14121a;stroke-width:3.4px;paint-order:stroke;stroke-linejoin:round;text-anchor:middle}</style>'
        + DEFS + '<div id="stage">' + ''.join(SVGS) + f'<svg viewBox="0 0 540 960">{"".join(sub_svg)}</svg></div><script>{js}</script>')
open('anim_v2.html', 'w').write(html)
os.makedirs('bg', exist_ok=True)
bg_html = ('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap"><style>html,body{margin:0}svg{display:block}</style>'
           + DEFS + ''.join(f'<svg id="{k}" viewBox="0 0 540 960" width="540" height="960">{v}</svg>' for k, v in BG.items()))
pass

# ---------------------------------------------------------------- เสียง
N = int((TOTAL + 1) * A.SR)
voice = np.zeros(N, np.float32)
for k, at in VOICE_AT.items(): A.add(voice, at, VO[k])
bang_t = T0['s4'] + TB
music_w = A.bridal_chorus(N, 0.0, bang_t)
cl = A.claps(N, T0['s3'] + .1, T0['s3'] + 2.6)
sfx = np.zeros(N, np.float32)
A.add(sfx, bang_t, A.door_bang()); A.add(sfx, bang_t + .75, A.thunder(5.0, 1.0)); A.add(sfx, T0['s9'] + 2.1, A.thunder(4.0, 1.4), .8)
A.add(sfx, T0['s6r'] + .05, A.sting(), .8); A.add(sfx, T0['s9r'] + .2, A.boom(2.6, 46), .5)
steps = A.footsteps(N, T0['s5'] + .1, T0['s5'] + 3.5, 1.7, .55) + A.footsteps(N, T0['s7b'] + .05, T0['s7b'] + 2.2, 2.0, .45)
rn = A.rain(N, bang_t + .9)
# เสียงจริงจาก sfx/*.mp3 (gen_sfx.py) ถ้ามี ใช้แทนเสียงสังเคราะห์
def real(name): f = f'sfx/{name}.mp3'; return A.load_voice(f, .1) if os.path.exists(f) else None
def fit(x, n, fo=.4): x = x[:n].copy(); k = min(len(x), int(fo * A.SR)); x[-k:] *= np.linspace(1, 0, k); return x
R_ = {k: real(k) for k in ('applause', 'door_bang', 'thunder', 'rain', 'heels', 'guard_steps')}
if R_['applause'] is not None: cl = np.zeros(N, np.float32); A.add(cl, T0['s3'] + .1, fit(R_['applause'], int(2.6 * A.SR), .8))
if R_['door_bang'] is not None or R_['thunder'] is not None:
    sfx = np.zeros(N, np.float32)
    A.add(sfx, bang_t, R_['door_bang'] * 3 if R_['door_bang'] is not None else A.door_bang())
    th = R_['thunder'] * 3 if R_['thunder'] is not None else None
    A.add(sfx, bang_t + .75, th if th is not None else A.thunder(5.0, 1.0)); A.add(sfx, T0['s9'] + 2.1, th if th is not None else A.thunder(4.0, 1.4), .8)
    A.add(sfx, T0['s6r'] + .05, A.sting(), .8); A.add(sfx, T0['s9r'] + .2, A.boom(2.6, 46), .5)
if R_['heels'] is not None or R_['guard_steps'] is not None:
    steps = np.zeros(N, np.float32)
    A.add(steps, T0['s5'] + .1, fit(R_['heels'], int(3.4 * A.SR)) if R_['heels'] is not None else A.footsteps(N, 0, 3.4, 1.7, .55)[:int(3.4 * A.SR)])
    A.add(steps, T0['s7b'] + .05, fit(R_['guard_steps'], int(2.2 * A.SR)) if R_['guard_steps'] is not None else A.footsteps(N, 0, 2.2, 2.0, .45)[:int(2.2 * A.SR)])
if R_['rain'] is not None:
    r = R_['rain']; x = r[int(.5 * A.SR):]; k = int(1.0 * A.SR)  # วนลูปแบบเฟดซ้อน
    loop = np.zeros(N, np.float32); t = int((bang_t + .9) * A.SR); w = np.linspace(0, 1, k)
    while t < N: seg = x.copy(); seg[:k] *= w; seg[-k:] *= w[::-1]; n = min(len(seg), N - t); loop[t:t + n] += seg[:n]; t += len(seg) - k
    rn = loop
import score
thr = score.build(N, dict(bang=bang_t, s5=T0['s5'], s6=T0['s6'], s6r=T0['s6r'], s7a=T0['s7a'], s7b=T0['s7b'], s8=T0['s8'], s9=T0['s9'], s9r=T0['s9r'], end=TOTAL))
def rms(x): return float(np.sqrt(np.mean(x ** 2)) + 1e-9)
v = rms(voice[np.abs(voice) > 1e-4])
def lvl(x, a, b, db): i0, i1 = int(a * A.SR), int(b * A.SR); return x * (v * 10 ** (-db / 20) / rms(x[i0:i1]))
music_w = lvl(music_w, .3, bang_t - .1, 5.5); thr = lvl(thr, bang_t + 1.5, TOTAL - 1, 8)
# เพลงจริงจาก ElevenLabs Music (gen_music.py) ถ้ามี ใช้แทนเพลงสังเคราะห์ ท่อนเพลงตั้งความยาวตามไทม์ไลน์ไว้แล้ว
def load_raw(f):
    import subprocess
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 's16le', '-ac', '1', '-ar', str(A.SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
if os.path.exists('music/A_wedding.mp3'):
    w = load_raw('music/A_wedding.mp3'); music_w = np.zeros(N, np.float32); A.add(music_w, 0, w)
    k = int(.06 * A.SR); i = int(bang_t * A.SR); music_w[i:i + k] *= np.linspace(1, 0, k); music_w[i + k:] = 0   # ตัดฉับตรงเสียงปัง
    music_w = lvl(music_w, .5, bang_t - .2, 8)
if os.path.exists('music/B_thriller.mp3'):
    b = load_raw('music/B_thriller.mp3'); thr = np.zeros(N, np.float32); A.add(thr, bang_t + 1.4, b)
    thr = lvl(thr, bang_t + 2, TOTAL - 1, 8); rn = lvl(rn, bang_t + 2, TOTAL - 1, 22); cl = lvl(cl, T0['s3'] + .4, T0['s3'] + 2.3, 16)
steps = lvl(steps, T0['s5'] + .2, T0['s5'] + 3.3, 10)
venv = A.lp(np.abs(voice), 4); duck = 1 - .3 * np.clip(venv / (venv.max() * .25 + 1e-6), 0, 1)
mix = voice + (music_w + thr) * duck + cl + rn + steps + sfx * .35
fade = int(.7 * A.SR); end = int(TOTAL * A.SR); mix[end - fade:end] *= np.linspace(1, 0, fade); mix[end:] = 0
mix = np.tanh(mix * 1.3) / 1.3; mix = mix / (np.abs(mix).max() + 1e-6) * .9
os.makedirs('out', exist_ok=True)
with wave.open('out/test_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(A.SR)
    w.writeframes(np.repeat((mix[:end] * 32767).astype(np.int16)[:, None], 2, axis=1).tobytes())
json.dump(dict(total=TOTAL, fps=FPS, shots=SHOTS, t0=T0, bang=bang_t), open('out/test_timeline.json', 'w'))
print(f'total {TOTAL:.1f}s · frames {int(TOTAL * FPS)} · arm parts {len(ARM_PARTS)}')
