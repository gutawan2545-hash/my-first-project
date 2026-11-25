"""สร้าง anim_full.py (คลิปเต็ม 27 ช็อต) จาก anim_v2.py (ช่วงทดลองที่ผ่านแล้ว) แล้วต่อช็อต 2 และ 10-27
รัน: python3 make_full.py && python3 anim_full.py && PAGE=bg_full.html node render_bg.js && PAGE=anim_full.html OUT=... node render_anim.js"""
import re
s = open('anim_v2.py').read()
def rep(a, b, n=1):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, n)

# ---------------------------------------------------------------- ชื่อไฟล์ผลลัพธ์
rep("open('anim_v2.html', 'w').write(html)", "open('anim_full.html', 'w').write(html)")
rep("open('out/test_audio.wav', 'wb')", "open('out/full_audio.wav', 'wb')")
rep("open('out/test_timeline.json', 'w')", "open('out/full_timeline.json', 'w')")
rep("\npass\n", "\nopen('bg_full.html', 'w').write(bg_html)\n")
rep("def clean(t): return re.sub(r'\\[[^\\]]*\\]\\s*', '', re.sub(r'^\\(.*?\\)\\s*', '', t)).replace('\"', '').strip()",
    "def clean(t): return re.sub(r'\\s*\\([^)]*\\)\\s*', ' ', re.sub(r'\\[[^\\]]*\\]\\s*', '', t)).replace('\"', '').strip()")

# ---------------------------------------------------------------- เสียงพากย์ช็อตใหม่
rep("for k in ('01c', '03c', '04c', '05c', '06e', '07g', '08c', '09e')}",
    "for k in ('01c', '03c', '04c', '05c', '06e', '07g', '08c', '09e') + tuple(f'{n}f' for n in range(10, 26))}\n"
    "VO['02a'] = A.load_voice(os.path.join(HERE, 'vo', '02a_t1.mp3'))")
rep("    ('s1', .5 + D['01c'] + .9), ('s3',", "    ('s1', .5 + D['01c'] + .9), ('s2', .4 + D['02a'] + .5), ('s3',")
rep("('s9r', 2.6)]", """('s9r', 2.6),
    ('s10', .5 + D['10f'] + .5), ('s11', .4 + D['11f'] + .5), ('s12', .4 + D['12f'] + .5), ('s13', .4 + D['13f'] + .6), ('s14', .4 + D['14f'] + .6),
    ('s15', .6 + D['15f'] + .4), ('s16', .4 + D['16f'] + .5), ('s17', .4 + D['17f'] + .9), ('s18', .4 + D['18f'] + .4), ('s19', .4 + D['19f'] + 1.0),
    ('s20', .7 + D['20f'] + 1.6), ('s21', .4 + D['21f'] + .8), ('s22', .4 + D['22f'] + .5), ('s23', .4 + D['23f'] + .7),
    ('s24', .5 + D['24f'] + 2.4), ('s25', .3 + D['25f'] + .9), ('s26', 3.6), ('s27', 9.0)]""")
rep("VOICE_AT = {'01c': T0['s1'] + .5,", "VOICE_AT = {'01c': T0['s1'] + .5, '02a': T0['s2'] + .4, "
    "**{f'{n}f': T0[f's{n}'] + (.5 if n in (10, 24) else .6 if n == 15 else .7 if n == 20 else .3 if n == 25 else .4) for n in range(10, 26)},")
rep("SPEAKER = {'06e': 'w6', '09e': 'w9', '07g': 'g7'}", "SPEAKER = {'06e': 'w6', '09e': 'w9', '07g': 'g7', '22f': 'w22', '23f': 'w23', '25f': 'g25'}")
rep("SUB_TXT = {'01c': 1,", "SUB_TXT = {**{f'{n}f': n for n in range(10, 26)}, '02a': 2, '01c': 1,")
rep("        9: [('อย่าให้เขาถอดแหวน', 'r'), ('เด็ดขาด', 'r')]}", """        9: [('อย่าให้เขาถอดแหวน', 'r'), ('เด็ดขาด', 'r')], 2: [('โรงแรมหรู', 'p')], 10: [('ความผิดปกติ', 'p')],
        11: [('ไม่มีใครถ่ายรูป', 'p')], 12: [('ผิดชื่อ', 'r')], 13: [('ครั้งที่แล้ว', 'r')], 14: [('สายตาสงสาร', 'p')], 15: [('โทรศัพท์ของเจ้าบ่าว', 'p')],
        16: [('โรงแรมเดียวกัน', 'p'), ('เจ้าบ่าวคนเดียวกัน', 'p'), ('ไม่เคยซ้ำหน้า', 'r')], 17: [('เจ้าสาวของปีที่แล้ว', 'r')], 18: [('ชื่อเจ้าสาว', 'p')],
        19: [('ประกาศตามหาคนหาย', 'r'), ('หนึ่งวัน', 'r')], 20: [('ชั้นเดิม', 'p'), ('ซ้ำแล้วซ้ำเล่า', 'r')], 21: [('ผู้หญิงชุดดำ', 'p')],
        22: [('ไม่ใช่สามี', 'r'), ('เจ้าสาว', 'p')], 23: [('อยากรอด', 'p'), ('ผู้หญิงคนต่อไป', 'r')], 24: [('สามครั้ง', 'p')], 25: [('ถอดแหวน', 'r')]}""")

# ---------------------------------------------------------------- ฉากหลังนิ่งของช็อตใหม่ + ตัวละครรองแบบมีริก
rep("def img(name):", """P2 = SB.P2
BG.update({'hall_all': SB.hall(), 'hall_cool': SB.hall(cool=.12), 'hall_nmom': SB.hall(CAST_NO('mom'), cool=.12), 'hall_nph': SB.hall(CAST_NO('ph'), cool=.12),
           'hall_nstaff': SB.hall(CAST_NO('staff'), cool=.12), 'hall_nb_cool2': SB.hall(CAST_NO('bride'), cool=.12),
           'ph15': P2.phone_hand(SB.scr_search().replace('ชื่อเจ้าสาว 2025', 'รหัสผ่าน ••••'), P2.bridal_room_bg()), 'ph16': P2.phone_hand(SB.scr_album(), P2.bridal_room_bg()),
           'ph17': P2.phone_hand(SB.scr_lastyear(), P2.bridal_room_bg()), 'ph18': P2.phone_hand(SB.scr_search(), P2.bridal_room_bg()),
           'ph19': P2.phone_hand(SB.scr_missing(), P2.bridal_room_bg()), 'ph21': P2.phone_hand(SB.scr_call(), '<g filter="url(#blurBG)">' + P2.suite_room() + '</g>'),
           'elev': P2.elevator_lux(''), 'sdoor': P2.suite_door_lux(True), 'suite': P2.suite_room(''),
           'darkbg': '<rect width="540" height="960" fill="#0e0d16"/><ellipse cx="270" cy="360" rx="200" ry="260" fill="#3a3a5a" opacity=".35" filter="url(#bl4)"/>',
           'corr': SB.corridor_groom().split(SB.put('groom_sin', 270, 330 + 492 * 1.7, 1.7, shadow=False))[0]})
def sup_rig(p, f):
    n, nt, kind, back, head, body = f()
    return (f'<g id="{p}">{back}<g id="{p}Body">{body}</g><g id="{p}H">{head}</g></g>', 460 if kind == 'f' else 488)
def fxy(key):
    x, feet, sc = SB.CAST[key]; return x, feet - (sup_rig('_', {'mom': SP.c_mother, 'ph': SP.c_photographer, 'staff': SP.c_staff}[key])[1] + 4) * sc
MX, MY = fxy('mom'); PX, PY = fxy('ph'); SX, SY = fxy('staff')
DARK_TOP = '<rect width="540" height="960" fill="#1a1a30" opacity=".35" style="mix-blend-mode:multiply"/><rect width="540" height="960" fill="url(#vigD)"/>'
PHONE = '<g transform="translate(38,4) rotate(8)"><rect x="-6" y="-18" width="13" height="30" rx="3" fill="#15131c"/><rect x="-4.6" y="-16" width="10" height="25" rx="2" fill="#6f7cff" opacity=".35"/></g>'
CARD_Q = ('คุณคิดว่าผู้หญิงคนนั้นเข้ามาเพื่อ', 'ช่วยคุณ หรือกำลังหาคน', 'มาตายแทนตัวเอง?')
def card_svg():
    q = (f'<text x="270" y="300" text-anchor="middle" {FT0} font-size="26" font-weight="700" fill="#fff">{CARD_Q[0]}</text>'
         f'<text x="270" y="338" text-anchor="middle" {FT0} font-size="26" font-weight="700" fill="#fff"><tspan fill="#c04dff">ช่วยคุณ</tspan> หรือกำลังหาคน</text>'
         f'<text x="270" y="376" text-anchor="middle" {FT0} font-size="26" font-weight="700" fill="#ff3b4e">มาตายแทนตัวเอง?</text>')
    opt = lambda k, y, txt: (f'<g id="opt{k}" transform="translate(270,{y})"><rect id="opt{k}R" x="-190" y="-34" width="380" height="68" rx="34" fill="#120e1c" stroke="#9a86ff" stroke-width="2"/>'
                             f'<circle cx="-150" cy="0" r="20" fill="#7a1fff"/><text x="-150" y="8" text-anchor="middle" {FT0} font-size="22" font-weight="700" fill="#fff">{k}</text>'
                             f'<text x="-116" y="9" {FT0} font-size="22" font-weight="600" fill="#f2eefa">{txt}</text></g>')
    return ('<rect width="540" height="960" fill="#0b0912"/><rect width="540" height="960" fill="url(#vigD)"/>' + q + opt('A', 470, 'เข้ามาช่วยคุณ') + opt('B', 560, 'หาคนมาตายแทนตัวเอง')
            + f'<text x="270" y="660" text-anchor="middle" {FT0} font-size="16" fill="#a79fc0">ตอบในคอมเมนต์ A หรือ B</text>')
FT0 = 'font-family="IBM Plex Sans Thai, sans-serif"'
def img(name):""")
rep("    shot_svg('s3',", """    shot_svg('s2', img('hall_all')),
    shot_svg('s3',""")
rep("    shot_svg('s9r', img('hall_nb_cool') + placed(bride_rig('b9'), *SB.CAST['bride'])),", """    shot_svg('s9r', img('hall_nb_cool') + placed(bride_rig('b9'), *SB.CAST['bride'])),
    shot_svg('s10', img('hall_nb_cool2') + placed(bride_rig('b10'), *SB.CAST['bride'])),
    shot_svg('s11', img('hall_cool')),
    shot_svg('s12', img('hall_nmom') + placed(sup_rig('m12', SP.c_mother), *SB.CAST['mom'])),
    shot_svg('s13', img('hall_nph') + placed(sup_rig('p13', SP.c_photographer), *SB.CAST['ph'])),
    shot_svg('s14', img('hall_nstaff') + placed(sup_rig('t14', SP.c_staff), *SB.CAST['staff'])),
    *[shot_svg(f's{n}', img(f'ph{n}')) for n in (15, 16, 17, 18, 19)],
    shot_svg('s20', img('elev') + placed(bride_rig('b20'), 270, 905, .64)),
    shot_svg('s21', img('ph21')),
    shot_svg('s22', img('darkbg') + placed(woman_rig('w22'), 270, 330 + 464 * 1.7, 1.7) + DARK_TOP),
    shot_svg('s23', img('darkbg') + placed(woman_rig('w23'), 270, 330 + 464 * 1.7, 1.7) + DARK_TOP),
    shot_svg('s24', img('sdoor')),
    shot_svg('s25', img('corr') + placed(groom_rig('g25'), 270, 330 + 492 * 1.7, 1.7) + '<rect width="540" height="960" fill="url(#vigD)"/>'),
    shot_svg('s26', img('suite') + placed(bride_rig('b26'), 300, 330 + 466 * 1.8, 1.8)),
    shot_svg('s27', card_svg()),""")
# โทรศัพท์แนบหูผู้หญิงชุดดำ (ช็อต 22-23)
rep("from rigs import bride_rig, woman_rig, groom_rig, guard_rig", "from rigs import bride_rig, woman_rig as _woman_rig, groom_rig, guard_rig\n"
    "def woman_rig(p):\n    body, lf = _woman_rig(p)\n    if p in ('w22', 'w23'): body = body.replace(f'<g id=\"{p}H\">', f'<g id=\"{p}H\">' + PHONE_EAR, 1)\n    return body, lf\n"
    "PHONE_EAR = '<g transform=\"translate(30,6) rotate(10)\"><rect x=\"-6\" y=\"-20\" width=\"14\" height=\"34\" rx=\"3\" fill=\"#15131c\"/><rect x=\"-4.4\" y=\"-18\" width=\"10.8\" height=\"28\" rx=\"2\" fill=\"#6f7cff\" opacity=\".4\"/></g>'")

# ---------------------------------------------------------------- การแสดงของช็อตใหม่
rep("    $('s9rk').setAttribute('opacity', Math.max(0, (t - (SH.s9r - .7)) / .7).toFixed(3)); },", r"""  },
  s2(t, gt) { const k = ease(t / SH.s2); cam('s2', lerp(1.55, 1.08, k), 270, lerp(230, 560, k), lerp(330, 470, k)); },
  s10(t, gt) { cam('s10', lerp(2.2, 2.7, ease(t / SH.s10)), %(bx)s, %(by)s + 40, 380); face('b10', 1, 3); blinkAt('b10', t, 2.8, .6);
    pose('b10', CLASP, CLASP, 1); arm('b10', 'L', -12 + 1.5 * Math.sin(t * 2), -18 - 4 * Math.sin(t * 2)); arm('b10', 'R', 12 - 1.5 * Math.sin(t * 2), 18 + 4 * Math.sin(t * 2));
    head('b10', t < 2 ? 4 * ease(t / .6) : t < 4 ? lerp(4, -5, ease((t - 2) / .5)) : lerp(-5, 1, ease((t - 4) / .6)), 0); breathe('b10', t, .008, 4, 0); },
  s11(t, gt) { cam('s11', lerp(1.9, 2.05, t / SH.s11), lerp(400, 450, ease(t / SH.s11)), 640, 420); },
  s12(t, gt) { cam('s12', lerp(3.0, 3.4, t / SH.s12), %(mx)s, %(my)s + 20, 380); head('m12', 2 * Math.sin(t * 1.4) + (t > 1 && t < 2.4 ? 3 * Math.sin((t - 1) * 9) : 0), 0); breathe('m12', t, .004, 1.6, .4); },
  s13(t, gt) { cam('s13', lerp(1.85, 2.05, t / SH.s13), %(px)s, %(py)s + 70, 380); head('p13', t < 1.6 ? 2 * Math.sin(t * 2) : lerp(0, -7, ease((t - 1.6) / .4)) + 1.5 * Math.sin(t * 7), t > 1.6 ? -2 : 0);
    breathe('p13', t, .006, 3, -.6); },
  s14(t, gt) { cam('s14', lerp(3.2, 3.6, t / SH.s14), %(sx)s, %(sy)s + 20, 380); head('t14', t < SH.s14 * .55 ? -2 + Math.sin(t * 1.2) : lerp(-2, 8, ease((t - SH.s14 * .55) / .6)), t > SH.s14 * .55 ? 1.5 : 0);
    breathe('t14', t, .004, 1.5, .3); },
  s15(t, gt) { cam('s15', lerp(1.0, 1.06, t / SH.s15), 270 + 3 * Math.sin(t * .9), 470 + 4 * Math.sin(t * 1.3), 470); },
  s16(t, gt) { cam('s16', lerp(1.02, 1.16, ease(t / SH.s16)), 270 + 2 * Math.sin(t * .8), lerp(470, 430, ease(t / SH.s16)) + 3 * Math.sin(t * 1.1), 470); },
  s17(t, gt) { const tp = .4 + VD['17f'] * .55, [sx, sy] = shake(t, tp, .4, 9); cam('s17', 1.04 + (t > tp ? .14 * backOut((t - tp) / .3) : 0), 270, 420, 470, sx, sy); flash('s17', t, [[tp, .12]]); },
  s18(t, gt) { cam('s18', lerp(1.0, 1.05, t / SH.s18), 270 + 3 * Math.sin(t), 470 + 3 * Math.sin(t * 1.4), 470); },
  s19(t, gt) { const tp = .4 + VD['19f'] * .25, [sx, sy] = shake(t, tp, .45, 10); cam('s19', 1.03 + (t > tp ? .16 * backOut((t - tp) / .3) : 0), 270, 420, 470, sx, sy);
    $('s19k').setAttribute('opacity', Math.max(0, (t - SH.s19 + .5) / .5).toFixed(2)); },
  s20(t, gt) { const dings = [.5, .5 + (SH.s20 - 1.2) / 2.4, .5 + (SH.s20 - 1.2) / 1.2]; let bump = 0, look = 0;
    for (const d of dings) { if (t > d && t < d + .5) { bump = 4 * Math.sin((t - d) * 20) * (1 - (t - d) / .5); } if (t > d) look = Math.max(look, 1 - Math.min(1, (t - d) / 1.4)); }
    cam('s20', lerp(1.0, 1.12, ease(t / SH.s20)), 270, 640, 520, 0, bump); face('b20', 1, 3); blinkAt('b20', t, 2.4, .3);
    pose('b20', CLASP, CLASP, 1); arm('b20', 'L', -12 + 2 * Math.sin(t * 3), -18 - 4 * Math.sin(t * 3)); arm('b20', 'R', 12, 18 + 4 * Math.sin(t * 3));
    head('b20', 3 * Math.sin(t * 1.7), -4 * look); breathe('b20', t, .01, 6, 0); },
  s21(t, gt) { const vib = t > .2 && t < SH.s21 - .3 && (t * 1.25) %% 1 < .45; cam('s21', 1.02, 270 + (vib ? 2.5 * Math.sin(t * 90) : 0), 470, 470); },
  s22(t, gt) { cam('s22', lerp(1.0, 1.12, t / SH.s22), 270, 470, 480); blinkAt('w22', t, 3.6, 1.0); const e = env('22f', gt); talk('w22', '22f', gt);
    head('w22', -3 + 1.2 * Math.sin(t * .7) + 2 * e, -1.2 * e); arm('w22', 'L', 1.5 * Math.sin(t), -5); arm('w22', 'R', -100, 219); breathe('w22', t, .004, 1.5, .3); },
  s23(t, gt) { cam('s23', lerp(1.55, 1.75, t / SH.s23), 270, 400, 440); blinkAt('w23', t, 4.1, 2.2); const e = env('23f', gt); talk('w23', '23f', gt);
    head('w23', -2 + .8 * Math.sin(t * .6) + 1.5 * e, -1 * e); arm('w23', 'L', 1.5 * Math.sin(t), -5); arm('w23', 'R', -100, 219); breathe('w23', t, .003, 1.4, .2); },
  s24(t, gt) { let j = 0; for (const k of KNOCKS) if (t > k && t < k + .12) j = 3 * (1 - (t - k) / .12); cam('s24', 1.0, 270, 480, 480, 0, j); },
  s25(t, gt) { cam('s25', lerp(1.0, 1.18, ease(t / SH.s25)), 270, 420, 440); face('g25', 2, 3); blinkAt('g25', t, 4.4, 1.6); const e = env('25f', gt); talk('g25', '25f', gt);
    head('g25', 3 + 2 * e + .8 * Math.sin(t * .6), -1.2 * e); arm('g25', 'L', 0, -5); arm('g25', 'R', 0, 5); place(P('g25'), 0, 0, 1, .8 * Math.sin(t * .5));
    flash('s25', t, [[SH.s25 - .35, .3]]); },
  s26(t, gt) { cam('s26', lerp(1.0, 1.15, ease(t / SH.s26)), 300, 440, 440); face('b26', 2, 3); blinkAt('b26', t, 9, .2); flash('s26', t, [[.02, .25], [.42, .14]]);
    pose('b26', CLASP, CHEST, t / .4); head('b26', -2 + (Math.random() - .5) * .8, Math.sin(t * 9) * .8); breathe('b26', t, .012, 9, 0);
    place(P('b26'), 0, -14 * ease(t / 1.2), 1 - .04 * ease(t / 1.2), 0); $('s26k').setAttribute('opacity', Math.max(0, (t - SH.s26 + .6) / .6).toFixed(2)); },
  s27(t, gt) { const k = Math.floor(Math.max(0, t - 1.0) / 1.4), a = t < 1.0 ? -1 : k %% 2;
    for (const [i, id] of [[0, 'optA'], [1, 'optB']]) { const on = a === i; $(id).setAttribute('transform', `translate(270,${i ? 560 : 470}) scale(${on ? 1.04 : 1})`);
      $(id + 'R').setAttribute('fill', on ? '#2a1f44' : '#120e1c'); $(id + 'R').setAttribute('stroke', on ? '#e2d2ff' : '#6a5aaa'); $(id + 'R').setAttribute('stroke-width', on ? 3 : 1.5); }
    $('s27in').setAttribute('opacity', Math.min(1, t / .6).toFixed(2)); },""")
rep("const TRUST = %(trust)s,", "const VD = %(vd)s, KNOCKS = %(knocks)s, EVT = %(evt)s;\nconst TRUST = %(trust)s,")
rep("gpt=G7_POINT,", "gpt=G7_POINT, mx=MX, my=MY, px=PX, py=PY, sx=SX, sy=SY, vd=json.dumps(D), knocks=json.dumps(KNOCKS), evt=json.dumps(EVT, ensure_ascii=False),")
rep("TRUST = [(T0['s6'] + .4 + D['06e'] * .85, 100, 70), (T0['s7a'] + G7_POINT - 3.2, 70, 45), (T0['s9'] + .4 + D['09e'] * .7, 45, 20)]",
    "TRUST = [(T0['s6'] + .4 + D['06e'] * .85, 100, 70), (T0['s7a'] + G7_POINT - 3.2, 70, 45), (T0['s9'] + .4 + D['09e'] * .7, 45, 20),\n"
    "         (T0['s12'] + .4 + D['12f'] * .7, 20, 12), (T0['s13'] + .4 + D['13f'] * .8, 12, 5), (T0['s17'] + .4 + D['17f'] * .6, 5, 0)]\n"
    "KNOCKS = [.5 + D['24f'] + .45 + k * .55 for k in range(3)]\n"
    "EVT = [(T0['s4'] + TB + .6, 'มีคนบุกงานแต่ง'), (T0['s10'], 'มีบางอย่างผิดปกติ'), (T0['s15'], 'แอบค้นมือถือเจ้าบ่าว'), (T0['s17'], 'เจ้าสาวปีที่แล้ว'),\n"
    "       (T0['s19'], 'เจ้าสาวทุกคนหายตัว'), (T0['s20'], 'หนีออกไปไม่ได้'), (T0['s21'], 'สายเข้า · ผู้หญิงชุดดำ'), (T0['s24'], 'มีคนเคาะประตู')]")
# ป้ายเหตุการณ์ข้อความเปลี่ยนได้ ความกว้างตามข้อความ · นาฬิกาตามช่วงเวลาในเรื่อง · ซ่อนป้ายและจางลายน้ำตอนการ์ดคำถาม
rep('<text x="52" y="88" font-size="13" font-weight="600" fill="#ffd2d7">มีคนบุกงานแต่ง</text>', '<text id="evtTxt" x="52" y="88" font-size="13" font-weight="600" fill="#ffd2d7">มีคนบุกงานแต่ง</text>')
rep('<g id="evt" opacity="0"><rect x="20" y="68" width="150"', '<g id="evt" opacity="0"><rect id="evtR" x="20" y="68" width="150"')
rep("""  const mins = Math.floor(gt / 3.2), hh = 19 + Math.floor(mins / 60), mm = mins %% 60;
  $('hudTxt').textContent = hh + ':' + String(mm).padStart(2, '0');""", """  let mins = gt < T0.s15 ? Math.floor(gt / 3.2) : gt < T0.s20 ? 160 + Math.floor((gt - T0.s15) / 3) : gt < T0.s24 ? 281 + Math.min(17, Math.floor((gt - T0.s20) / 2.5)) : 299;
  const hh = 19 + Math.floor(mins / 60), mm = mins %% 60;
  $('hudTxt').textContent = hh + ':' + String(mm).padStart(2, '0');
  const card = cur === 's27'; $('hud').setAttribute('display', card ? 'none' : 'inline'); $('wm').setAttribute('opacity', card ? Math.max(0, .85 - (gt - T0.s27) / .5).toFixed(2) : .85);
  let et = null; for (const E of EVT) if (gt >= E[0]) et = E;
  if (et) { if ($('evtTxt').textContent !== et[1]) { $('evtTxt').textContent = et[1]; $('evtR').setAttribute('width', ($('evtTxt').getComputedTextLength() + 44).toFixed(0)); } }""")
rep("const ev = ease((gt - BANG - .6) / .4);", "const ev = et ? ease((gt - et[0]) / .4) : 0;")
# ช็อตที่ต้องตัดดำตอนท้าย
rep("<rect id=\"{sid}k\" width=\"540\" height=\"960\" fill=\"#000\" opacity=\"0\"/>", "<rect id=\"{sid}k\" width=\"540\" height=\"960\" fill=\"#000\" opacity=\"0\"/>")
rep("    shot_svg('s27', card_svg()),", "    shot_svg('s27', f'<g id=\"s27in\" opacity=\"0\">{card_svg()}</g>'),")

# ---------------------------------------------------------------- เสียง: เพลงช่วงหลัง + เสียงประกอบช็อตใหม่
rep("venv = A.lp(np.abs(voice), 4);", """SR = A.SR
def knock():
    n = int(.25 * SR); x = np.arange(n) / SR
    s_ = np.sin(2 * np.pi * 150 * x) * np.exp(-x * 38) + .5 * np.sin(2 * np.pi * 360 * x) * np.exp(-x * 55)
    s_ = s_ + A.bp(A.rng.standard_normal(n).astype(np.float32), 300, 2500) * np.exp(-x * 70) * .7
    return A.reverb(s_.astype(np.float32), .5, .2)
def ding(f=1318.5):
    n = int(1.6 * SR); x = np.arange(n) / SR
    return ((np.sin(2 * np.pi * f * x) + .4 * np.sin(2 * np.pi * f * 2.76 * x) * np.exp(-x * 4)) * np.exp(-x * 2.5) * .22).astype(np.float32)
def buzz(dur=.45):
    n = int(dur * SR); x = np.arange(n) / SR
    s_ = (np.sign(np.sin(2 * np.pi * 150 * x)) * .5 + np.sin(2 * np.pi * 300 * x)).astype(np.float32)
    return (A.bp(s_, 120, 1500) * A.env_adsr(n, .02, .05) * .12).astype(np.float32)
def click():
    n = int(.04 * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2200 * x) * np.exp(-x * 160) * .35).astype(np.float32)
def whoosh(dur=.6):
    n = int(dur * SR); x = np.arange(n) / SR
    return (A.bp(A.rng.standard_normal(n).astype(np.float32), 300, 2500) * np.sin(np.pi * x / dur) ** 2 * .5).astype(np.float32)
sfx2 = np.zeros(N, np.float32)
for st in ('s15', 's20'): A.add(sfx2, T0[st] - .3, whoosh(), .8)
A.add(sfx2, T0['s17'] + .4 + D['17f'] * .55, A.boom(2.6, 48), .9); A.add(sfx2, T0['s19'] + .4 + D['19f'] * .25, A.boom(2.8, 44), 1.0)
for k in range(3): A.add(sfx2, T0['s20'] + .5 + k * (SH_D['s20'] - 1.2) / 2.4, ding(), 1.0)
for k in range(4): A.add(sfx2, T0['s21'] + .2 + k * .8, buzz(), 1.0)
for kt in KNOCKS: A.add(sfx2, T0['s24'] + kt, knock(), 1.3)
th2 = R_['thunder'] * 3 if R_['thunder'] is not None else A.thunder(5.0, .9)
A.add(sfx2, T0['s25'] + SH_D['s25'] - .35, th2, 1.0)                      # ผู้ใช้สั่ง: ฟ้าผ่าอีกครั้งหลังสามีเรียกจบประโยค
A.add(sfx2, T0['s26'] + .3, A.boom(3.0, 42), .5)
for k in range(5): A.add(sfx2, T0['s27'] + 1.0 + k * 1.4, click(), 1.0)
if os.path.exists('music/C_night.mp3'):
    c_ = load_raw('music/C_night.mp3'); mc = np.zeros(N, np.float32); A.add(mc, T0['s10'], c_)
    mc = lvl(mc, T0['s10'] + 1, T0['s26'], 9); thr = thr + mc
venv = A.lp(np.abs(voice), 4);""")
rep("mix = voice + (music_w + thr) * duck + cl + rn + steps + sfx * .35", "mix = voice + (music_w + thr) * duck + cl + rn + steps + sfx * .35 + sfx2 * .35")
rep("bang_t = T0['s4'] + TB\nmusic_w", "bang_t = T0['s4'] + TB\nSH_D = dict(SHOTS)\nmusic_w")
# เพลง B เดิมจบท้ายช็อต 9r ให้เฟดออกนุ่ม ๆ ก่อนเพลงช่วงหลัง
rep("    b = load_raw('music/B_thriller.mp3'); thr = np.zeros(N, np.float32); A.add(thr, bang_t + 1.4, b)",
    "    b = load_raw('music/B_thriller.mp3'); thr = np.zeros(N, np.float32); A.add(thr, bang_t + 1.4, b)\n"
    "    i1 = int(T0['s10'] * A.SR); k = int(1.2 * A.SR); thr[i1 - k // 2:i1 + k // 2] *= np.linspace(1, 0, k); thr[i1 + k // 2:] = 0")
rep("thr = lvl(thr, bang_t + 2, TOTAL - 1, 8);", "thr = lvl(thr, bang_t + 2, T0['s10'] - 1, 8);")
rep("rn = lvl(rn, bang_t + 2, TOTAL - 1, 22);", "rn = lvl(rn, bang_t + 2, T0['s10'] - 1, 22);")

# ================================================================ รอบแก้ 1 (ผู้ใช้สั่ง)
# 1) กล้องห้ามเลยขอบภาพจนเห็นขอบดำ: บีบตำแหน่งกล้องให้อยู่ในภาพเสมอ
rep("function cam(sid, z, cx, cy, ty, sx, sy) { $(sid + 'c').setAttribute('transform', `translate(${270 - cx * z + (sx||0)},${(ty||400) - cy * z + (sy||0)}) scale(${z})`); }",
    "function cam(sid, z, cx, cy, ty, sx, sy) { let X = 270 - cx * z + (sx||0), Y = (ty||400) - cy * z + (sy||0);\n"
    "  if (z >= 1) { X = Math.min(0, Math.max(540 - 540 * z, X)); Y = Math.min(0, Math.max(960 - 960 * z, Y)); }\n"
    "  $(sid + 'c').setAttribute('transform', `translate(${X},${Y}) scale(${z})`); }")
# 2) ช็อตพนักงานโรงแรม: เอาช่างภาพที่ยืนแถวหน้าออก จะได้ไม่มีคนตัวใหญ่บังฉากหลัง
rep("'hall_nstaff': SB.hall(CAST_NO('staff'), cool=.12)", "'hall_nstaff': SB.hall(CAST_NO('staff', 'ph'), cool=.12)")
# 3) ช็อตมือถือ: นิ้วโป้งแยกเป็นชิ้นขยับได้ กดปุ่ม เลื่อนจอ พิมพ์ จอเปลี่ยนตามการกด
rep("P2 = SB.P2\nBG.update(", r'''P2 = SB.P2
THUMB_OLD = '<path d="M 300,630 C 320,580 340,540 352,510 C 362,496 382,500 380,520 C 372,560 360,610 340,660 Z" fill="#fbe2cf"/><ellipse cx="366" cy="512" rx="12" ry="9" fill="#ffffff" opacity=".5"/>'
THUMB = ('<path d="M 286,880 C 296,760 322,590 352,510 C 362,496 382,500 380,520 C 374,580 362,700 350,880 Z" fill="#fbe2cf"/>'
         '<path d="M 352,520 C 356,560 352,620 344,700" stroke="#efc3a8" stroke-width="3" fill="none" opacity=".6"/><ellipse cx="366" cy="512" rx="12" ry="9" fill="#ffffff" opacity=".5"/>')
def phone_bg(bg):
    o = P2.phone_hand('', bg); assert THUMB_OLD in o; return o.replace(THUMB_OLD, '')
FTP = 'font-family="IBM Plex Sans Thai, sans-serif"'
def scr_lock():
    keys = ''.join(f'<g id="k15_{d}"><circle cx="{200 + (i % 3) * 70}" cy="{420 + (i // 3) * 52}" r="20" fill="#2a2e44"/><text x="{200 + (i % 3) * 70}" y="{427 + (i // 3) * 52}" text-anchor="middle" {FTP} font-size="18" fill="#eef0f6">{d}</text></g>'
                   for i, d in enumerate('123456789') ) + f'<circle cx="270" cy="576" r="20" fill="#2a2e44"/><text x="270" y="583" text-anchor="middle" {FTP} font-size="18" fill="#eef0f6">0</text>'
    dots = ''.join(f'<circle id="pd15_{i}" cx="{240 + i * 20}" cy="350" r="6" fill="none" stroke="#c9a8ff" stroke-width="2"/>' for i in range(4))
    return (f'<rect x="156" y="156" width="228" height="488" fill="#141826"/><text x="270" y="250" text-anchor="middle" {FTP} font-size="44" font-weight="300" fill="#eef0f6">21:41</text>'
            f'<text x="270" y="275" text-anchor="middle" {FTP} font-size="11" fill="#9aa2b8">มือถือของเขา · ใส่รหัสผ่าน</text>{dots}{keys}')
def scr_album_long(n=15, scroll_id='al'):
    hairs = ['#3a2620', '#141017', '#6a4a3c', '#2a1c18', '#141017', '#5a3a2a', '#0e0b10', '#3a2a24', '#7a5848', '#2c1e1a', '#4a3028', '#141017', '#6a4a3c', '#3a2620', '#141017']
    cells = ''
    for i in range(n):
        x = 162 + (i % 3) * 74; y = 206 + (i // 3) * 132
        cells += SB.mini_couple(x, y, 68, 104, hairs[i], i + 3) + f'<text x="{x + 34}" y="{y + 120}" text-anchor="middle" font-size="10" fill="#9aa2b8" {FTP}>{2011 + i}</text>'
    hl = f'<rect id="{scroll_id}HL" x="{162 + 2 * 74}" y="{206 + 4 * 132}" width="68" height="104" fill="none" stroke="#c9a8ff" stroke-width="3" opacity="0"/>'
    return (f'<rect x="156" y="156" width="228" height="488" fill="#1a1c28"/><g id="{scroll_id}">{cells}{hl}</g>'
            f'<rect x="156" y="156" width="228" height="40" fill="#2a2c3c"/><text x="170" y="182" font-size="13" font-weight="600" fill="#e8ecf4" {FTP}>อัลบั้ม · งานแต่ง</text>')
def scr_type():
    rows = ''.join(f'<g id="r18_{i}" opacity="0"><rect x="166" y="{254 + i * 72}" width="208" height="60" rx="8" fill="#22263a"/><rect x="176" y="{264 + i * 72}" width="40" height="40" rx="4" fill="#3a3f58"/>'
                   f'<rect x="226" y="{268 + i * 72}" width="{120 - i * 8}" height="8" rx="4" fill="#8a94b4"/><rect x="226" y="{286 + i * 72}" width="{90 + i * 6}" height="6" rx="3" fill="#4e5674"/></g>' for i in range(5))
    kb = ('<g id="kb18"><rect x="156" y="470" width="228" height="174" fill="#262a3a"/>' +
          ''.join(f'<rect x="{162 + c * 22.4}" y="{480 + r * 40}" width="19" height="32" rx="4" fill="#3c4258"/>' for r in range(3) for c in range(10)) +
          '<rect x="200" y="600" width="140" height="30" rx="5" fill="#3c4258"/></g>')
    return (f'<rect x="156" y="156" width="228" height="488" fill="#1a1c28"/><rect x="156" y="156" width="228" height="40" fill="#2a2c3c"/>'
            f'<rect x="166" y="206" width="208" height="30" rx="15" fill="#2c3044"/><text id="q18" x="182" y="226" font-size="12" fill="#e8ecf4" {FTP}></text>'
            f'<rect id="cur18" x="182" y="214" width="1.6" height="15" fill="#c9a8ff"/>{rows}{kb}')
def scr_missing_live():
    s = SB.scr_missing(); parts = s.split('<rect x="')
    return s
def phone_live(n, screen):
    return (f'<g transform="rotate(-4 270 420)"><clipPath id="sc{n}"><rect x="152" y="140" width="236" height="520" rx="24"/></clipPath>'
            f'<g clip-path="url(#sc{n})"><g transform="translate(152,140) scale({236 / 228:.4f},{520 / 488:.4f}) translate(-156,-156)">{screen}'
            f'<circle id="rp{n}" r="10" fill="none" stroke="#ffffff" stroke-width="3" opacity="0"/></g></g></g><g id="th{n}">{THUMB}</g>')
LAST = f'<g id="ly17" opacity="0">{SB.scr_lastyear()}</g>'
MISS = SB.scr_missing()
# แยกโปสเตอร์ตามหาคนหายเป็นชิ้น ให้ขึ้นทีละใบ
_m = re.split(r'(?=<rect x="\d+" y="\d+" width="102" height="136")', MISS)
MISS_LIVE = _m[0] + '<g id="ms19">' + ''.join(f'<g id="ms19_{i}" opacity="0">{p}</g>' for i, p in enumerate(_m[1:])) + '</g>'
BG.update(''')
rep("           'ph15': P2.phone_hand(SB.scr_search().replace('ชื่อเจ้าสาว 2025', 'รหัสผ่าน ••••'), P2.bridal_room_bg()), 'ph16': P2.phone_hand(SB.scr_album(), P2.bridal_room_bg()),",
    "           'phb_bridal': phone_bg(P2.bridal_room_bg()), 'phb_suite': phone_bg('<g filter=\"url(#blurBG)\">' + P2.suite_room() + '</g>'),")
rep("    *[shot_svg(f's{n}', img(f'ph{n}')) for n in (15, 16, 17, 18, 19)],", """    shot_svg('s15', img('phb_bridal') + phone_live(15, scr_lock() + f'<g id="al15" opacity="0">{scr_album_long(15, "a15")}</g>')),
    shot_svg('s16', img('phb_bridal') + phone_live(16, scr_album_long(15, 'a16'))),
    shot_svg('s17', img('phb_bridal') + phone_live(17, scr_album_long(15, 'a17') + LAST)),
    shot_svg('s18', img('phb_bridal') + phone_live(18, scr_type())),
    shot_svg('s19', img('phb_bridal') + phone_live(19, MISS_LIVE)),""")
rep("    shot_svg('s21', img('ph21')),", "    shot_svg('s21', img('phb_suite') + phone_live(21, SB.scr_call() + '<circle id=\"ring21\" cx=\"270\" cy=\"300\" r=\"44\" fill=\"none\" stroke=\"#9aa8ff\" stroke-width=\"2\"/>')),")
PHJS = r"""
function scrXY(cx, cy) { const px = 152 + (cx - 156) * 236 / 228, py = 140 + (cy - 156) * 520 / 488, a = -4 * Math.PI / 180, dx = px - 270, dy = py - 420;
  return [270 + dx * Math.cos(a) - dy * Math.sin(a), 420 + dx * Math.sin(a) + dy * Math.cos(a)]; }
function thumb(n, kf, t) {   // kf = [[เวลา, x จอ, y จอ, กด(0/1)], ...] นิ้วโป้งเคลื่อนนุ่ม ๆ ระหว่างจุด กดแล้วจุ่มลงนิดหนึ่งพร้อมวงคลื่นบนจอ
  let i = 0; while (i < kf.length - 1 && t > kf[i + 1][0]) i++;
  const A = kf[i], B = kf[Math.min(i + 1, kf.length - 1)], k = B[0] > A[0] ? ease((t - A[0]) / (B[0] - A[0])) : 0;
  const cx = lerp(A[1], B[1], k), cy = lerp(A[2], B[2], k); let press = 0, rp = null;
  for (const K of kf) if (K[3]) { const u = t - K[0]; if (u >= 0 && u < .16) press = Math.sin(u / .16 * Math.PI); if (u >= 0 && u < .45) rp = [K[1], K[2], u]; }
  const [x, y] = scrXY(cx, cy), dx = x - 366, dy = y - 512 + press * 5;
  $('th' + n).setAttribute('transform', `translate(${dx.toFixed(1)},${dy.toFixed(1)}) rotate(${(dx * .04).toFixed(2)} 330 880)`);
  const r = $('rp' + n); if (rp) { r.setAttribute('cx', rp[0]); r.setAttribute('cy', rp[1]); r.setAttribute('r', (8 + 40 * rp[2]).toFixed(1)); r.setAttribute('opacity', (.8 * (1 - rp[2] / .45)).toFixed(2)); } else r.setAttribute('opacity', 0);
}
const KEYXY = d => [200 + ((d - 1) %% 3) * 70, 420 + Math.floor((d - 1) / 3) * 52];
"""
rep("const R = { // การแสดงของแต่ละช็อต: t = เวลาในช็อต, gt = เวลารวม\n", PHJS + "const R = { // การแสดงของแต่ละช็อต: t = เวลาในช็อต, gt = เวลารวม\n")
rep("  s15(t, gt) { cam('s15', lerp(1.0, 1.06, t / SH.s15), 270 + 3 * Math.sin(t * .9), 470 + 4 * Math.sin(t * 1.3), 470); },",
r"""  s15(t, gt) { cam('s15', lerp(1.0, 1.06, t / SH.s15), 270 + 3 * Math.sin(t * .9), 470 + 4 * Math.sin(t * 1.3), 470);
    const pin = [2, 5, 8, 0], tt = [.9, 1.45, 2.0, 2.55], KF = [[0, 330, 600, 0]];   // พิมพ์รหัสสี่ตัว แล้วปลดล็อกเข้าอัลบั้ม
    pin.forEach((d, i) => { const [x, y] = d ? KEYXY(d) : [270, 576]; KF.push([tt[i] - .25, x, y, 0], [tt[i], x, y, 1]); }); KF.push([3.2, 340, 610, 0], [SH.s15, 330, 610, 0]);
    thumb(15, KF, t); for (let i = 0; i < 4; i++) $('pd15_' + i).setAttribute('fill', t > tt[i] ? (t > 2.8 ? '#6fe0a0' : '#c9a8ff') : 'none');
    $('al15').setAttribute('opacity', Math.max(0, Math.min(1, (t - 3.0) / .35)).toFixed(2)); },""")
rep("  s16(t, gt) { cam('s16', lerp(1.02, 1.16, ease(t / SH.s16)), 270 + 2 * Math.sin(t * .8), lerp(470, 430, ease(t / SH.s16)) + 3 * Math.sin(t * 1.1), 470); },",
r"""  s16(t, gt) { cam('s16', lerp(1.02, 1.12, ease(t / SH.s16)), 270 + 2 * Math.sin(t * .8), 450 + 3 * Math.sin(t * 1.1), 470);
    const sw = [[.8, 1.3, 0, -110], [3.0, 3.5, -110, -222]];   // ปัดขึ้นสองครั้ง จอเลื่อนตามแบบมีแรงเหวี่ยง
    let sy = 0; for (const [a, b, f, to] of sw) { if (t >= a) sy = lerp(f, to, 1 - Math.pow(1 - Math.min(1, (t - a) / (b - a + .5)), 3)); }
    $('a16').setAttribute('transform', `translate(0,${sy.toFixed(1)})`);
    thumb(16, [[0, 330, 600, 0], [.6, 300, 600, 0], [.8, 300, 600, 0], [1.25, 300, 470, 0], [1.6, 330, 600, 0], [2.8, 300, 600, 0], [3.0, 300, 600, 0], [3.45, 300, 470, 0], [3.9, 335, 605, 0], [SH.s16, 335, 605, 0]], t);
    $('a16HL').setAttribute('opacity', t > SH.s16 - 2.2 ? (.6 + .4 * Math.sin(t * 6)).toFixed(2) : 0); },""")
rep("  s17(t, gt) { const tp = .4 + VD['17f'] * .55, [sx, sy] = shake(t, tp, .4, 9); cam('s17', 1.04 + (t > tp ? .14 * backOut((t - tp) / .3) : 0), 270, 420, 470, sx, sy); flash('s17', t, [[tp, .12]]); },",
r"""  s17(t, gt) { const tp = .4 + VD['17f'] * .55, [sx, sy] = shake(t, tp, .4, 9); cam('s17', 1.04 + (t > tp ? .14 * backOut((t - tp) / .3) : 0), 270, 420, 470, sx, sy); flash('s17', t, [[tp, .12]]);
    $('a17').setAttribute('transform', 'translate(0,-222)'); $('a17HL').setAttribute('opacity', .9);
    thumb(17, [[0, 335, 605, 0], [.35, 344, 566, 0], [.55, 344, 566, 1], [1.0, 330, 640, 0], [SH.s17, 330, 640, 0]], t);   // แตะรูปปี 2025 แล้วรูปขยายเต็มจอ
    const o = ease((t - .65) / .35); $('ly17').setAttribute('opacity', o.toFixed(2));
    $('ly17').setAttribute('transform', `translate(${lerp(344, 270, o).toFixed(1)},${lerp(566, 400, o).toFixed(1)}) scale(${lerp(.3, 1, o).toFixed(3)}) translate(-270,-400)`); },""")
rep("  s18(t, gt) { cam('s18', lerp(1.0, 1.05, t / SH.s18), 270 + 3 * Math.sin(t), 470 + 3 * Math.sin(t * 1.4), 470); },",
r"""  s18(t, gt) { cam('s18', lerp(1.0, 1.05, t / SH.s18), 270 + 3 * Math.sin(t), 470 + 3 * Math.sin(t * 1.4), 470);
    const W = ['ชื่อ', 'เจ้าสาว', ' ', '2025', ' ', 'หาย'], t0 = .35, dt = .22, nT = W.length, done = t0 + nT * dt;   // พิมพ์ค้นหาทีละคำ นิ้วกดคีย์บอร์ดตามจังหวะ
    $('q18').textContent = W.slice(0, Math.max(0, Math.min(nT, Math.floor((t - t0) / dt) + 1))).join('').trim();
    $('cur18').setAttribute('x', (183 + $('q18').getComputedTextLength()).toFixed(1)); $('cur18').setAttribute('opacity', (t * 2) %% 1 < .6 ? 1 : 0);
    const KF = [[0, 330, 610, 0]]; for (let i = 0; i < nT; i++) { const x = 175 + ((i * 97) %% 200), y = 496 + ((i * 53) %% 3) * 40; KF.push([t0 + i * dt - .14, x, y, 0], [t0 + i * dt, x, y, 1]); }
    KF.push([done + .2, 270, 615, 0], [done + .45, 270, 615, 1], [done + 1, 330, 640, 0], [SH.s18, 330, 640, 0]); thumb(18, KF, t);
    const kd = ease((t - done - .55) / .35); $('kb18').setAttribute('transform', `translate(0,${(190 * kd).toFixed(1)})`);
    for (let i = 0; i < 5; i++) $('r18_' + i).setAttribute('opacity', Math.max(0, Math.min(1, (t - done - .7 - i * .15) / .25)).toFixed(2)); },""")
rep("  s19(t, gt) { const tp = .4 + VD['19f'] * .25, [sx, sy] = shake(t, tp, .45, 10); cam('s19', 1.03 + (t > tp ? .16 * backOut((t - tp) / .3) : 0), 270, 420, 470, sx, sy);",
r"""  s19(t, gt) { const tp = .4 + VD['19f'] * .25, [sx, sy] = shake(t, tp, .45, 10); cam('s19', 1.03 + (t > tp ? .16 * backOut((t - tp) / .3) : 0), 270, 420, 470, sx, sy);
    for (let i = 0; i < 6; i++) { const u = (t - .25 - i * .28) / .3, e = Math.max(0, Math.min(1, u)); const g = $('ms19_' + i); if (!g) continue;   // โปสเตอร์คนหายขึ้นทีละใบ
      g.setAttribute('opacity', e.toFixed(2)); }
    const sy2 = -70 * ease((t - 2.6) / .8); $('ms19').setAttribute('transform', `translate(0,${sy2.toFixed(1)})`);
    thumb(19, [[0, 330, 620, 0], [2.4, 300, 610, 0], [2.6, 300, 610, 0], [3.2, 300, 520, 0], [3.7, 335, 625, 0], [SH.s19, 335, 625, 0]], t);""")
rep("  s21(t, gt) { const vib = t > .2 && t < SH.s21 - .3 && (t * 1.25) %% 1 < .45; cam('s21', 1.02, 270 + (vib ? 2.5 * Math.sin(t * 90) : 0), 470, 470); },",
r"""  s21(t, gt) { const vib = t > .2 && t < SH.s21 - .5 && (t * 1.25) %% 1 < .45; cam('s21', 1.02, 270 + (vib ? 2.5 * Math.sin(t * 90) : 0), 470, 470);
    const pr = (t * .8) %% 1; $('ring21').setAttribute('r', (44 + 26 * pr).toFixed(1)); $('ring21').setAttribute('opacity', (1 - pr).toFixed(2));
    const tr = 1.5 * Math.sin(t * 23);   // นิ้วโป้งสั่นลังเล แล้วค่อย ๆ เลื่อนไปกดรับสาย
    thumb(21, [[0, 300, 630, 0], [SH.s21 - 1.1, 310 + tr, 610, 0], [SH.s21 - .55, 330, 560, 0], [SH.s21 - .4, 330, 560, 1], [SH.s21, 330, 575, 0]], t); },""")

open('anim_full.py', 'w').write(s)
print('wrote anim_full.py')
