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

def placed(rig, x, feet, s):
    body, lf = rig
    return f'<g data-lf="{lf}" data-x="{x}" data-feet="{feet}" data-s="{s}" class="place">{body}</g>'

CAST_NO = lambda *ks: {k: v for k, v in SB.CAST.items() if k not in ks}
BX, BY = SB.bx, SB.by; GX, GY = SB.gx, SB.gy
WF = SB.WB_FACE

# ---------------------------------------------------------------- เสียงพากย์และไทม์ไลน์
VO = {k: A.load_voice(os.path.join(HERE, 'vo', f'{k}.mp3')) for k in ('03e', '04e', '05e', '06e', '08e', '09e')}
VO['07'] = A.load_voice(os.path.join(HERE, 'vo', json.load(open('vo/report.json'))['lines']['07a']['best']['path']))
VO['07'] *= 1.0
D = {k: len(v) / A.SR for k, v in VO.items()}
TB = .3 + D['04e'] - .35                  # เสียงปังตรงคำว่า "เปิดออก"
S7_SPLIT = .3 + D['07'] * .55
SHOTS = [
    ('s3', .4 + D['03e'] + .5), ('s4', TB + 2.3), ('s4r', 1.8), ('s5', .4 + D['05e'] + .6), ('s6', .4 + D['06e'] + .5),
    ('s6r', 2.3), ('s7a', S7_SPLIT), ('s7b', D['07'] - S7_SPLIT + .3 + .7), ('s8', .4 + D['08e'] + .4), ('s9', .4 + D['09e'] + .6), ('s9r', 2.6)]
T0 = {}; t = 0
for k, d in SHOTS: T0[k] = t; t += d
TOTAL = t
VOICE_AT = {'03e': T0['s3'] + .4, '04e': T0['s4'] + .3, '05e': T0['s5'] + .4, '06e': T0['s6'] + .4, '07': T0['s7a'] + .3, '08e': T0['s8'] + .4, '09e': T0['s9'] + .4}
SPEAKER = {'06e': 'w6', '09e': 'w9'}
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
SUB_TXT = {'03e': 3, '04e': 4, '05e': 5, '06e': 6, '07': 7, '08e': 8, '09e': 9}
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
const R = { // ฟังก์ชันของแต่ละช็อต: t = เวลาในช็อต, gt = เวลารวม
  s3(t, gt) { cam('s3', lerp(2.0, 2.25, t / SH.s3), %(cx3)s, %(cy3)s, 360); blinkAt('b3', t, 3.1, .4); blinkAt('g3', t, 3.7, 1.6);
    head('b3', 1.6 * Math.sin(t * 1.2), 0); head('g3', -1.2 * Math.sin(t * .9 + 1), 0); place(P('b3'), 0, 0, 1 + .004 * Math.sin(t * 2.4)); },
  s4(t, gt) { const tb = %(tb)s; $('d4c').setAttribute('display', t < tb ? 'inline' : 'none'); $('d4h').setAttribute('display', t >= tb && t < tb + .12 ? 'inline' : 'none'); $('d4o').setAttribute('display', t >= tb + .12 ? 'inline' : 'none');
    const [sx, sy] = shake(t, tb, .7, 26); cam('s4', lerp(1.0, 1.08, t / SH.s4), 270, 480, 480, sx, sy); flash('s4', t, [[tb + .75, .2], [tb + 1.05, .14]]); },
  s4r(t, gt) { cam('s4r', lerp(3.0, 3.3, t / SH.s4r), %(bx)s, %(by)s, 380); face('b4', 2, 3); $('b4B').setAttribute('display', 'none');
    head('b4', (Math.random() - .5) * 1.4, -2 * ease(t / .3)); place(P('b4'), (Math.random() - .5) * .6, 0, 1); },
  s5(t, gt) { const p = ease(t / 3.6), step = Math.abs(Math.sin(t * Math.PI * 1.7)) * (1 - ease((t - 3.4) / .3));
    const el = P('w5'); el.dataset.feet = lerp(610, %(df)s, p); el.dataset.s = lerp(.30, %(ds)s, p); place(el, 0, -6 * step, 1, 1.3 * Math.sin(t * Math.PI * 1.7) * (1 - p * .7));
    blinkAt('w5', t, 3.3, 1.2); head('w5', 0, 0); $('w5M').setAttribute('display', 'none');
    $('ring5').setAttribute('display', t > %(ringt)s ? 'inline' : 'none'); cam('s5', lerp(1.0, 1.12, t / SH.s5), 270, 560, 560); },
  s6(t, gt) { cam('s6', lerp(3.1, 3.4, t / SH.s6), %(wfx)s, %(wfy)s + 40, 380); blinkAt('w6', t, 3.4, .9); head('w6', 1.4 * Math.sin(t * .8), 0); talk('w6', '06e', gt); },
  s6r(t, gt) { cam('s6r', lerp(3.2, 3.6, t / SH.s6r), %(bx)s, %(by)s, 380); face('b6', t < .9 ? 2 : 1, 3); blinkAt('b6', t, 2.1, 1.5);
    head('b6', (Math.random() - .5) * (t < .9 ? 1.6 : .6), 0); },
  s7a(t, gt) { cam('s7a', lerp(2.4, 2.6, t / SH.s7a), %(gx)s, %(gy)s + 90, 400); face('g7', t < .35 ? 0 : 1, 2); blinkAt('g7', t, 3.9, 2.2);
    const a = 72 * ease((t - .5) / .45); $('g7A').setAttribute('transform', `rotate(${a + (t > .95 ? 2 * Math.sin(t * 14) : 0)} -50 72)`);
    head('g7', t > .5 && t < 1.6 ? 3 * Math.sin(t * 10) : 0, 0); },
  s7b(t, gt) { cam('s7b', lerp(1.35, 1.45, t / SH.s7b), 270, 590, 480); const p = ease(t / 2.2), step = Math.abs(Math.sin(t * Math.PI * 2)) * (1 - p);
    const el = P('k7'); el.dataset.x = lerp(600, 316, p); place(el, 0, -5 * step, 1); blinkAt('w7', t, 3.1, .3); blinkAt('k7', t, 4.2, 1.1);
    head('w7', -3 * ease(t / 2.4), 0); $('w7M').setAttribute('display', 'none'); },
  s8(t, gt) { cam('s8', lerp(1.7, 1.95, t / SH.s8), 270, 600, 430); head('w8', lerp(-4, 0, ease((t - 1.2) / 1.5)), 0); blinkAt('w8', t, 3.6, 2.4); blinkAt('k8', t, 4.0, .6); $('w8M').setAttribute('display', 'none'); },
  s9(t, gt) { cam('s9', lerp(4.8, 5.3, t / SH.s9), %(wfx)s, %(wfy)s + 4, 380); blinkAt('w9', t, 3.9, 2.8); head('w9', .8 * Math.sin(t * .7), 0); talk('w9', '09e', gt);
    flash('s9', t, [[2.1, .18]]); },
  s9r(t, gt) { cam('s9r', lerp(3.2, 3.8, t / SH.s9r), %(bx)s, %(by)s, 380); face('b9', 1, 3); blinkAt('b9', t, 2.6, 1.9); head('b9', (Math.random() - .5) * .8, 0);
    $('b9T').setAttribute('display', t > .8 ? 'inline' : 'none'); $('s9rk').setAttribute('opacity', Math.max(0, (t - (SH.s9r - .7)) / .7).toFixed(3)); },
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
               cx3=(BX + GX) / 2, cy3=BY + 60, tb=TB, bx=BX, by=BY + 40, gx=GX, gy=GY, df=SB.DOOR_FEET, ds=SB.DOOR_S, ringt=.4 + D['05e'] * .55,
               wfx=WF[0], wfy=WF[1])

base = SB.N9.H8.S.DEFS
for gid in ('drapeShadeL', 'drapeShadeR', 'glass4', 'vig4'):
    base = re.sub(rf'<(linear|radial)Gradient id="{gid}".*?</\1Gradient>', '', base, flags=re.S)
DEFS = (base + SB.H8.DEFS_EXTRA + SB.N9.EXTRA_DEFS + WC.DEFS + SB.B2.DEFS + SP.DEFS + SB.P2.DEFS2 + SB.EXTRA_DEFS + SB.CHAR_DEFS
        + f'<svg width="0" height="0" style="position:absolute"><defs>{gh}</defs></svg>')
html = ('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=Inter:wght@600&family=IBM+Plex+Mono:wght@500&display=swap">'
        '<style>html,body{margin:0;background:#000}#stage{position:relative;width:540px;height:960px;overflow:hidden}#stage svg{position:absolute;inset:0;width:540px;height:960px}'
        '.th{font-family:"IBM Plex Sans Thai";font-weight:700;font-size:20px;fill:#ffd84a;stroke:#1a1410;stroke-width:5px;paint-order:stroke;stroke-linejoin:round;text-anchor:middle}'
        '.en{font-family:Inter,sans-serif;font-weight:600;font-size:13px;fill:#fff;stroke:#14121a;stroke-width:3.4px;paint-order:stroke;stroke-linejoin:round;text-anchor:middle}</style>'
        + DEFS + '<div id="stage">' + ''.join(SVGS) + f'<svg viewBox="0 0 540 960">{"".join(sub_svg)}</svg></div><script>{js}</script>')
open('anim_test.html', 'w').write(html)
os.makedirs('bg', exist_ok=True)
bg_html = ('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap"><style>html,body{margin:0}svg{display:block}</style>'
           + DEFS + ''.join(f'<svg id="{k}" viewBox="0 0 540 960" width="540" height="960">{v}</svg>' for k, v in BG.items()))
open('bg.html', 'w').write(bg_html)

# ---------------------------------------------------------------- เสียง
N = int((TOTAL + 1) * A.SR)
voice = np.zeros(N, np.float32)
for k, at in VOICE_AT.items(): A.add(voice, at, VO[k])
bang_t = T0['s4'] + TB
music_w = A.bridal_chorus(N, 0.0, bang_t)
cl = A.claps(N, 0.1, 2.6)
sfx = np.zeros(N, np.float32)
A.add(sfx, bang_t, A.door_bang()); A.add(sfx, bang_t + .75, A.thunder(5.0, 1.0)); A.add(sfx, T0['s9'] + 2.1, A.thunder(4.0, 1.4), .8)
A.add(sfx, T0['s6r'] + .05, A.sting(), .8); A.add(sfx, T0['s9r'] + .2, A.boom(2.6, 46), .5)
steps = A.footsteps(N, T0['s5'] + .1, T0['s5'] + 3.5, 1.7, .55) + A.footsteps(N, T0['s7b'] + .05, T0['s7b'] + 2.2, 2.0, .45)
rn = A.rain(N, bang_t + .9)
thr = A.thriller(N, T0['s5'], TOTAL)
def rms(x): return float(np.sqrt(np.mean(x ** 2)) + 1e-9)
v = rms(voice[np.abs(voice) > 1e-4])
def lvl(x, a, b, db): i0, i1 = int(a * A.SR), int(b * A.SR); return x * (v * 10 ** (-db / 20) / rms(x[i0:i1]))
music_w = lvl(music_w, .3, bang_t - .1, 5.5); thr = lvl(thr, T0['s6'], TOTAL - 1, 6.5); rn = lvl(rn, bang_t + 2, TOTAL - 1, 22); cl = lvl(cl, .4, 2.3, 14)
steps = lvl(steps, T0['s5'] + .2, T0['s5'] + 3.3, 10)
venv = A.lp(np.abs(voice), 4); duck = 1 - .45 * np.clip(venv / (venv.max() * .25 + 1e-6), 0, 1)
mix = voice + (music_w + thr) * duck + cl + rn + steps + sfx * .35
fade = int(.7 * A.SR); end = int(TOTAL * A.SR); mix[end - fade:end] *= np.linspace(1, 0, fade); mix[end:] = 0
mix = np.tanh(mix * 1.3) / 1.3; mix = mix / (np.abs(mix).max() + 1e-6) * .9
os.makedirs('out', exist_ok=True)
with wave.open('out/test_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(A.SR)
    w.writeframes(np.repeat((mix[:end] * 32767).astype(np.int16)[:, None], 2, axis=1).tobytes())
json.dump(dict(total=TOTAL, fps=FPS, shots=SHOTS), open('out/test_timeline.json', 'w'))
print(f'total {TOTAL:.1f}s · frames {int(TOTAL * FPS)} · arm parts {len(ARM_PARTS)}')
