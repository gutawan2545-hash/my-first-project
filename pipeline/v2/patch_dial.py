"""(1) new dial-pad close-up: Tawan types the ten digits, then presses call; (2) softer lips: James no red,
Tawan dusty pink; (3) warmer, consistent skin in the late shots (no cold, washed-out tint)."""


def rep(s, o, n):
    assert o in s, o[:110]
    return s.replace(o, n, 1)


# ---------------- timeline ----------------
p = 'timeline.py'; s = open(p).read()
s = rep(s, "shot('dial', 1.6)", "shot('dialpad', 2.7, [], taps=[round(0.25 + k * 0.17, 2) for k in range(10)], call=2.2)\nshot('dial', 1.6)")
s = rep(s, "# soft phone buzz when the screen lights up in the headphones shot",
"""# key taps (short two-tone beeps) and the call press on the dial pad
for k, tp in enumerate(S['dialpad']['taps'] + [S['dialpad']['call']]):
    i = int((S['dialpad']['start'] + tp) * SR); n = int(0.07 * SR); x = np.arange(n) / SR
    f1, f2 = [(941, 1336), (852, 1336), (697, 1209), (770, 1336), (770, 1209), (852, 1477), (697, 1336), (852, 1209), (770, 1477), (770, 1336), (600, 900)][k]
    sfx[i:i + n] += ((np.sin(2 * np.pi * f1 * x) + np.sin(2 * np.pi * f2 * x)) * np.hanning(n) * 0.05).astype(np.float32)
# soft phone buzz when the screen lights up in the headphones shot""")
open(p, 'w').write(s)

# ---------------- builder ----------------
p = 'v2.py'; s = open(p).read()
# dial-pad shot, built from the hand-held phone shot
s = rep(s, "SV['scroll'] = s5",
"""SV['scroll'] = s5
dp = A['s5'].replace(VIG + TEX, '')
a = dp.index('<g font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"><text x="270" y="180"'); b = dp.index('</g>', a) + 4
KEYS = [('1', 210, 250), ('2', 270, 250), ('3', 330, 250), ('4', 210, 306), ('5', 270, 306), ('6', 330, 306),
        ('7', 210, 362), ('8', 270, 362), ('9', 330, 362), ('*', 210, 418), ('0', 270, 418), ('#', 330, 418)]
pad = ''.join(f'<g class="key" data-d="{d}"><circle cx="{x}" cy="{y}" r="23" fill="#2c3264"/><circle class="flash" cx="{x}" cy="{y}" r="23" fill="#c9a8ff" opacity="0"/>'
              f'<text x="{x}" y="{y+8}" text-anchor="middle" font-size="22" font-weight="500" fill="#eef0ff">{d}</text></g>' for d, x, y in KEYS)
dial_screen = (f'<g {FONT}><text x="270" y="150" text-anchor="middle" font-size="11" fill="#9aa3c8">โทรศัพท์</text>'
               '<text class="num" x="270" y="200" text-anchor="middle" font-size="27" font-weight="500" fill="#ffffff" letter-spacing="1"></text>'
               '<rect class="caret" x="356" y="180" width="2" height="26" fill="#c9a8ff"/>' + pad +
               '<circle class="callbtn" cx="270" cy="482" r="23" fill="#3cb46e"/><path d="M262,478 q2,-6 6,-4 l2,3 q-3,3 -1,6 q3,4 7,5 q2,-2 5,0 l2,3 q-2,5 -6,4 q-12,-3 -15,-17 Z" fill="#ffffff"/></g>')
dp = dp[:a] + dial_screen + dp[b:]
dp = rep(dp, A['thumb'], f'<g class="tap">{A["thumb"]}</g>')
SV['dialpad'] = dp + dust(311, (330, 10, 540, 260), 12)""")

# warm, consistent skin in the late shots
s = s.replace("SKB = '#d9bfb8'", "SKB = '#f2d6c6'")
s = s.replace("fill=\"#c4a8a2\"", "fill=\"#e2bba6\"")
s = s.replace("'<g filter=\"url(#tintNight)\"><g transform=\"translate(400,500) scale(1.55)\">' + TBACK", "'<g filter=\"url(#tintDim)\"><g transform=\"translate(400,500) scale(1.55)\">' + TBACK")
s = s.replace('<path d="M 60,106 L 48,112 L 40,30 L 52,24 Z" fill="#d9a48c"/>', '<path d="M 60,106 L 48,112 L 40,30 L 52,24 Z" fill="#e8b08a"/>')
s = s.replace('<ellipse cx="46" cy="18" rx="9" ry="10" fill="#d9a48c"/>', '<ellipse cx="46" cy="18" rx="9" ry="10" fill="#e8b08a"/>')
s = s.replace('<path d="M -40,64 C -46,68 -50,86 -50,104 L -51,212 L -40,212 L -38,110 Z" fill="#e2b29c"/>', '<path d="M -40,64 C -46,68 -50,86 -50,104 L -51,212 L -40,212 L -38,110 Z" fill="#f8d2ab"/>')
s = rep(s, "'<g class=\"reach\" filter=\"url(#tintNight)\"><g transform=\"translate(250 690)\">'", "'<g class=\"reach\" filter=\"url(#tintDim)\"><g transform=\"translate(250 690)\">'")
for o, n in [('#e2c4bc', '#efc7b0'), ('#f2d9d2', '#fbe7d8'), ('#e9cdc6', '#f6dccb'), ('#dcbab2', '#e6b9a2'), ('#c9a69e', '#d29d86')]:
    s = s.replace(o, n)
for key in ("SV['door']", "SV['whisper']", "SV['dean']"):
    pass
s = s.replace("'<g filter=\"url(#tintWarm)\"><use href=\"#jbodySNH\" transform=\"translate(250,330) scale(2.3)\"/></g>'",
              "'<g filter=\"url(#bright)\"><use href=\"#jbodySNH\" transform=\"translate(250,330) scale(2.3)\"/></g>'")
s = s.replace("'<g filter=\"url(#tintNight)\">' + ots_reach", "'<g filter=\"url(#tintDim)\">' + ots_reach")
s = rep(s, "'<g class=\"jstep\" transform=\"translate(185,470) scale(2.0)\">' + JBACK + '</g></g>')", "'<g class=\"jstep\" transform=\"translate(185,470) scale(2.0)\">' + JBACK + '</g></g>')")
s = rep(s, "'<g filter=\"url(#tintNight)\"><g transform=\"translate(400,500) scale(1.55)\">' + TBACK", "'<g filter=\"url(#tintDim)\"><g transform=\"translate(400,500) scale(1.55)\">' + TBACK") if "'<g filter=\"url(#tintNight)\"><g transform=\"translate(400,500) scale(1.55)\">' + TBACK" in s else s
TINT = '<filter id="tintDim" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.86 0 0 0 0.02  0 0.82 0 0 0.02  0 0 0.86 0 0.04  0 0 0 1 0"/></filter>'
s = rep(s, "f'<g id=\"hp\">{hp}</g>", f"'{TINT}' + f'<g id=\"hp\">{{hp}}</g>")

# softer lips (applied to the finished page so every face variant follows)
s = rep(s, "open('v2.html', 'w').write(html)",
"""for o, n in [('#a05a50', '#b98378'), ('#6b3a3a', '#6e5052'), ('#b0605a', '#b58a84'),        # James: no red
             ('#a24a46', '#c47f86'), ('#e79a8a', '#ebb3b3'), ('#8a3436', '#a8646e'),         # Tawan: dusty pink
             ('#7a3434', '#9c5f68'), ('#d27a74', '#e0a5aa')]:
    html = html.replace(o, n)
open('v2.html', 'w').write(html)""")
open(p, 'w').write(s)

# ---------------- JS ----------------
p = 'v2.js'; j = open(p).read()
j = rep(j, "  if (c.key === 'tawanlook') {",
"""  if (c.key === 'dialpad') {
    const NUM = '0815923746', n = c.taps.filter(x => t >= x).length;
    const shown = NUM.slice(0, n).replace(/^(\\d{3})(\\d{0,3})(\\d{0,4}).*/, (m, a, b, d) => [a, b, d].filter(Boolean).join(' '));
    const num = el('.num'); num.textContent = n < 3 ? NUM.slice(0, n) : shown;
    el('.caret').setAttribute('opacity', (Math.floor(t * 3) % 2) ? 1 : 0.2);
    const keys = [...svg.querySelectorAll('.key')];
    const pos = d => { const k = keys.find(e => e.dataset.d === d); const ci = k.querySelector('circle'); return [+ci.getAttribute('cx'), +ci.getAttribute('cy')]; };
    keys.forEach(k => k.querySelector('.flash').setAttribute('opacity', 0));
    let target = [300, 520];
    for (let i = 0; i < c.taps.length; i++) {
      if (t >= c.taps[i] - 0.12) target = pos(NUM[i]);
      if (t >= c.taps[i] && t < c.taps[i] + 0.12) keys.find(e => e.dataset.d === NUM[i]).querySelector('.flash').setAttribute('opacity', 0.7);
    }
    if (t >= c.call - 0.15) target = [270, 482];
    el('.callbtn').setAttribute('fill', (t >= c.call && t < c.call + 0.2) ? '#6be09a' : '#3cb46e');
    const press = (t % 0.17) < 0.06 ? 3 : 0;
    el('.tap').setAttribute('transform', `translate(${(target[0] - 288 + 6).toFixed(1)} ${(target[1] - 487 + 6 + press).toFixed(1)})`);
  }
  if (c.key === 'tawanlook') {""")
open(p, 'w').write(j)
print('patched dial + lips + skin')
