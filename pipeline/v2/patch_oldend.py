"""Ending as in the old draft: ringtone-of-the-old-phone shot, then the A/B choice card with the cat and
James's hand, then (in assembly) the reusable logo outro."""


def rep(s, o, n):
    assert o in s, o[:110]
    return s.replace(o, n, 1)


# ---------------- timeline ----------------
p = 'timeline.py'; s = open(p).read()
s = rep(s, "'J4', 'J5a', 'J5b']}", "'J4', 'J5a', 'J5b', 'J5', 'J6']}")
s = rep(s, """a = 0.2; b = a + L['J5a'] + 0.2
shot('endcard', 3.4, [('J5a', a), ('J5b', b)], card_in=0.3)""",
"""shot('oldtone', 0.25 + L['J6'] + 0.4, [('J6', 0.25)])
shot('choice', 0.3 + L['J5'] + 1.6, [('J5', 0.3)], hand_stop=1.0)""")
s = s.replace("e0 = S['endcard']['start']", "e0 = S['choice']['start']")
s = s.replace("seg[int((S['endcard']['start'] - c0) * SR):] *= 0.55", "seg[int((S['choice']['start'] - c0) * SR):] *= 0.5")
open(p, 'w').write(s)

# ---------------- builder ----------------
p = 'v2.py'; s = open(p).read()
s = rep(s, "    'J5_unused': (['ถ้าเป็นคุณ จะเปิดประตูไปดูว่าใครอยู่ข้างใน'", "    'J5': (['ถ้าเป็นคุณ จะเปิดประตูไปดูว่าใครอยู่ข้างใน'")
s = rep(s, "    'J4': (['ลองโทรอีกทีดิ'], ['Call it again.']),",
           "    'J4': (['ลองโทรอีกทีดิ'], ['Call it again.']),\n"
           "    'J6': (['และเสียงเรียกเข้านั้น', 'เป็นเพลงเดียวกับมือถือเครื่องเก่าของผม', 'ที่หายไปตั้งแต่ปีก่อน'], ['And that ringtone was the same song', 'as my old phone, the one I lost last year.']),")
s = rep(s, "# ---------------- subtitles (time windows) ----------------",
"""# ---- old-draft ending: ringtone of the lost phone, then the A/B choice ----
sD = A['sD'].replace(VIG + TEX, '')
sD = rep(sD, '<g filter="url(#tintNight)"><use href="#jbodyS" transform="translate(230,300) scale(2.3)"/></g>',
         '<g filter="url(#tintDim)"><use href="#jbodySNH" transform="translate(230,300) scale(2.3)"/></g>')
sD = sD.replace('fill="#e2ecff" opacity="', 'class="note" fill="#e2ecff" opacity="')
SV['oldtone'] = sD
s8 = A8['s8'].replace(VIG + TEX, '')
s8 = rep(s8, '<g filter="url(#tintNight)"><path d="M0,520', '<g filter="url(#tintDim)" class="reach"><path d="M0,520')
SV['choice'] = s8
INFO_OLD = {'oldtone': A['NEW']['D'][5], 'choice': '<g class="choicecard">' + A8['INFO'][7] + '</g>'}

# ---------------- subtitles (time windows) ----------------""")
s = rep(s, "INFO = {'hook': tag(20, 20, '04:00'), 'write': ''}", "INFO = {'hook': tag(20, 20, '04:00'), 'write': '', **INFO_OLD}")
open(p, 'w').write(s)

# ---------------- JS ----------------
p = 'v2.js'; j = open(p).read()
j = rep(j, "  if (c.key === 'endcard') {",
"""  if (c.key === 'oldtone') {
    [...svg.querySelectorAll('.note')].forEach((n, k) => { if (!n.dataset.base) n.dataset.base = n.getAttribute('transform') || '';
      const y = -((t * 14 + k * 20) % 60); n.setAttribute('transform', `translate(0 ${y.toFixed(1)}) ${n.dataset.base}`); });
  }
  if (c.key === 'choice') {
    const k = ease(t / c.hand_stop), x = -40 * (1 - k);
    el('.reach').setAttribute('transform', `translate(${x.toFixed(1)} 0)`);
  }
  if (c.key === 'endcard') {""")
open(p, 'w').write(j)

# ---------------- assembly: episode + reusable outro ----------------
p = 'assemble.sh'; a = open(p).read()
a = rep(a, 'cp body.mp4 ep01_v2_preview.mp4\n',
        'ffmpeg -y -loglevel error -i body.mp4 -i outro.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \\\n'
        '  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 19 -r 24 -c:a aac -b:a 160k -movflags +faststart ep01_v2_preview.mp4\n')
open(p, 'w').write(a)
print('patched old ending')
