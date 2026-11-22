"""Shot 2: a monitor that reads as a monitor, and warm-violet screen light without the washed-out haze.
Bedroom two-shots: richer colour instead of the brightening filter (saturated, not brighter)."""


def rep(s, o, n):
    assert o in s, o[:110]
    return s.replace(o, n, 1)


p = 'v2.py'; s = open(p).read()
s = rep(s, "SV['headphones'] = s2", r'''# --- monitor seen from behind: casing, back panel, vents, stand, cable, light spilling round the edges ---
MON = ('<defs><linearGradient id="monCase" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3646"/><stop offset="1" stop-color="#1b1922"/></linearGradient>'
       '<radialGradient id="faceLight2" gradientUnits="userSpaceOnUse" cx="250" cy="420" r="220"><stop offset="0" stop-color="#f2b8d6" stop-opacity=".30"/>'
       '<stop offset=".55" stop-color="#b79cff" stop-opacity=".12"/><stop offset="1" stop-color="#b79cff" stop-opacity="0"/></radialGradient>'
       '<linearGradient id="monBeam2" gradientUnits="userSpaceOnUse" x1="200" y1="480" x2="250" y2="260"><stop offset="0" stop-color="#f6c6a0" stop-opacity=".22"/><stop offset="1" stop-color="#c7a8ff" stop-opacity="0"/></linearGradient>'
       '<filter id="tintLilac" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="1.0 0 0 0 0.03  0 0.88 0 0 0.0  0 0 0.98 0 0.05  0 0 0 1 0"/></filter></defs>'
       '<path d="M10,478 L340,470 L346,486 L16,494 Z" fill="#f4c49c" opacity=".55" filter="url(#bokeh)"/>'                 # warm light leaking over the top edge
       '<path d="M8,486 L8,486" />'
       '<rect x="14" y="484" width="330" height="200" rx="14" fill="url(#monCase)"/>'
       '<rect x="14" y="484" width="330" height="200" rx="14" fill="none" stroke="#c9a6e8" stroke-opacity=".55" stroke-width="2.5"/>'
       '<rect x="104" y="530" width="150" height="112" rx="16" fill="#2a2734"/><rect x="104" y="530" width="150" height="112" rx="16" fill="none" stroke="#3e3a4c" stroke-width="2"/>'
       + ''.join(f'<rect x="{122+k*12}" y="548" width="5" height="22" rx="2" fill="#1d1b25"/>' for k in range(10)) +
       '<circle cx="179" cy="604" r="9" fill="#3a3648"/><circle cx="179" cy="604" r="4" fill="#8d7ac0" opacity=".8"/>'
       '<rect x="166" y="642" width="26" height="50" fill="#24222c"/><rect x="166" y="642" width="6" height="50" fill="#33303d"/>'
       '<path d="M186,660 C200,680 220,684 236,692" stroke="#15141b" stroke-width="5" fill="none"/>'
       '<ellipse cx="179" cy="694" rx="60" ry="7" fill="#15131b"/>')
s2 = s2.replace('<path d="M-10,500 L340,466 L368,700 L-10,700 Z" fill="url(#monBack)"/>', MON)
s2 = s2.replace('<path d="M120,600 l16,-14 l16,14 l-16,14 Z" fill="#d9c6d6" opacity=".7"/>', '')
s2 = s2.replace('<path d="M340,466 L368,700 L360,700 L334,468 Z" fill="#f6d2c4"/>', '')
s2 = s2.replace('url(#faceLight)', 'url(#faceLight2)').replace('url(#monBeam)', 'url(#monBeam2)')
s2 = s2.replace('<g filter="url(#tintWarm)"><g transform="translate(262,320) scale(1.7)">', '<g filter="url(#tintLilac)"><g transform="translate(262,320) scale(1.7)">')
s2 = s2.replace('<rect x="0" y="696" width="340" height="10" fill="#f0c0b0" opacity=".5" filter="url(#bokeh)"/>', '<rect x="14" y="690" width="330" height="8" fill="#e8b8e0" opacity=".35" filter="url(#bokeh)"/>')
SV['headphones'] = s2''')

# saturated-not-brighter look for the bedroom two-shots
VIVID = ('<filter id="vivid" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values="1.3"/>'
         '<feComponentTransfer><feFuncR type="linear" slope="0.97" intercept="0.0"/><feFuncG type="linear" slope="0.94"/><feFuncB type="linear" slope="0.98" intercept="0.01"/></feComponentTransfer></filter>')
s = rep(s, "         '<filter id=\"tintDim\"", "         " + repr(VIVID) + " + '<filter id=\"tintDim\"")
s = s.replace("filter=\"url(#bright)\"", "filter=\"url(#vivid)\"")
s = rep(s, "lampglow = '<circle cx=\"480\" cy=\"230\" r=\"170\" fill=\"#ffe6da\" opacity=\".14\"", "lampglow = '<circle cx=\"480\" cy=\"230\" r=\"170\" fill=\"#f2c8e4\" opacity=\".08\"")
open(p, 'w').write(s)
print('patched look')
