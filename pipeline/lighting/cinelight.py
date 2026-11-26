"""Odd Hours cinematic 2D lighting kit.

Reusable across every episode. Works on the existing SVG scenes (540x960 frame
units) without touching character shapes: lighting is added around them in
separate layers.

Layer order produced by compose():
    L-bg      background art (as drawn)
    L-shadow  contact shadows + ambient occlusion (multiply)
    L-char    characters, each wrapped in a static group carrying its rim/form filter
    L-light   localized glows + light shafts (screen)
    L-atmos   dust inside shafts, haze
    -- everything above is inside the colour grade group --
    L-post    vignette + film grain
    L-ui      subtitles / info cards (never graded, never vignetted)

Rule for animation: the filter sits on an UNTRANSFORMED wrapper; the character's
own motion transform goes on the inner group. The rim is therefore computed in
frame space every frame and always hugs the silhouette. For characters that
travel across the frame, cinelight.js re-aims the rim toward the light source.
"""
import math, random

# ---------------------------------------------------------------- rigs
# key = where the warm key/rim light sits (frame coords); amb = cool ambient
# shadow colour. Values were tuned on storyboard2 shots 2, 4 and 7.
RIGS = {
    'night': dict(rim='#ffbf7a', rim_op=.95, rim_soft_op=.26, rim_w=2.4, bloom=.32,
                  amb='#3d4c72', shade_op=.62, shade_k=16, shade_blur=11,
                  face_shade=.26, chin_ao=.55,
                  sat=.9, lift=(.004, .008, .028), gamma=(1.16, 1.13, 1.06), gain=(1.0, .98, .97),
                  vig=.62, grain=.07),
    'interior': dict(rim='#ffc88a', rim_op=.9, rim_soft_op=.26, rim_w=2.4, bloom=.32,
                     amb='#4a5878', shade_op=.40, shade_k=15, shade_blur=11,
                     face_shade=.18, chin_ao=.48,
                     sat=.92, lift=(.004, .008, .024), gamma=(1.12, 1.10, 1.05), gain=(1.0, .985, .97),
                     vig=.5, grain=.06),
    'closeup': dict(rim='#ffc27e', rim_op=1.0, rim_soft_op=.26, rim_w=2.6, bloom=.32,
                    amb='#3f4e74', shade_op=.55, shade_k=22, shade_blur=15,
                    face_shade=.26, chin_ao=.6,
                    sat=.9, lift=(.004, .008, .026), gamma=(1.14, 1.11, 1.05), gain=(1.0, .98, .97),
                    vig=.58, grain=.065),
    # daylight exteriors (EP Koh Tao): rim still warm, shadows cool but lighter, no low-key
    'day': dict(rim='#ffd9a8', rim_op=.75, rim_soft_op=.26, rim_w=2.2, bloom=.32,
                amb='#5a6f96', shade_op=.32, shade_k=14, shade_blur=10,
                face_shade=.2, chin_ao=.38,
                sat=.92, lift=(.012, .016, .03), gamma=(1.0, 1.0, .99), gain=(1.0, .99, .98),
                vig=.32, grain=.05),
}

# face outlines in head space (head origin = 0,0, same as the character sheets)
FACES = {
    'james': 'M -32,-14 C -32,-46 32,-46 32,-14 L 31,6 C 29,22 13,37 0,40 C -13,37 -29,22 -31,6 Z',
    'tawan': 'M -31,-14 C -31,-45 31,-45 31,-14 L 30,6 C 28,22 13,36 0,39 C -13,36 -28,22 -30,6 Z',
    'sun':   'M -31,-14 C -31,-46 31,-46 31,-14 L 30,1 C 28,17 14,34 0,41.5 C -14,34 -28,17 -30,1 Z',
}


SKIN_SHADE = '#8e6f93'   # cool-leaning shadow tint for skin (multiply); keeps faces alive, never grey


def _unit(dx, dy):
    m = math.hypot(dx, dy) or 1
    return dx / m, dy / m


def aim(char_xy, light_xy):
    """Unit vector from a character toward its light source (frame space)."""
    return _unit(light_xy[0] - char_xy[0], light_xy[1] - char_xy[1])


# ---------------------------------------------------------------- defs
def defs(rig_name, prefix='cl'):
    r = RIGS[rig_name]
    lr, lg, lb = r['lift']; gr, gg, gb = r['gamma']; ar, ag, ab = r['gain']
    return f'''<filter id="{prefix}-grade" x="0" y="0" width="540" height="960" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
  <feColorMatrix type="saturate" values="{r['sat']}"/>
  <feComponentTransfer>
    <feFuncR type="gamma" amplitude="{ar}" exponent="{gr}" offset="{lr}"/>
    <feFuncG type="gamma" amplitude="{ag}" exponent="{gg}" offset="{lg}"/>
    <feFuncB type="gamma" amplitude="{ab}" exponent="{gb}" offset="{lb}"/>
  </feComponentTransfer>
</filter>
<radialGradient id="{prefix}-vig" cx="50%" cy="46%" r="72%">
  <stop offset=".55" stop-color="#0a0d18" stop-opacity="0"/>
  <stop offset=".82" stop-color="#0a0d18" stop-opacity="{r['vig'] * .55:.3f}"/>
  <stop offset="1" stop-color="#05060c" stop-opacity="{r['vig']}"/>
</radialGradient>
<filter id="{prefix}-grain" x="0" y="0" width="540" height="960" filterUnits="userSpaceOnUse">
  <feTurbulence type="fractalNoise" baseFrequency="1.35" numOctaves="2" seed="11" stitchTiles="stitch"/>
  <feColorMatrix type="saturate" values="0"/>
</filter>
<filter id="cl-soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="cl-soft2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="cl-moteSharp" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation=".45" result="b"/><feGaussianBlur stdDeviation="1.8" in="SourceGraphic" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="b"/></feMerge></filter>
<filter id="cl-moteFar" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.3"/></filter>
<radialGradient id="cl-contact"><stop offset="0" stop-color="#090b14" stop-opacity=".85"/><stop offset=".55" stop-color="#0d1020" stop-opacity=".35"/><stop offset="1" stop-color="#0d1020" stop-opacity="0"/></radialGradient>
<radialGradient id="{prefix}-chinAO" cx="50%" cy="30%" r="60%"><stop offset="0" stop-color="#1c2236" stop-opacity="{r['chin_ao']}"/><stop offset="1" stop-color="#1c2236" stop-opacity="0"/></radialGradient>'''


def char_filter(fid, direction, rig_name, scale=1.0):
    """Rim + form-shade filter for one character. direction: unit vector toward light."""
    r = RIGS[rig_name]
    dx, dy = direction
    w, W = r['rim_w'] * scale, r['rim_w'] * 2.8 * scale
    k, b = r['shade_k'] * scale, r['shade_blur'] * scale
    return f'''<filter id="{fid}" x="-20%" y="-12%" width="140%" height="124%" color-interpolation-filters="sRGB">
  <feGaussianBlur in="SourceAlpha" stdDeviation="{b:.2f}" result="ab"/>
  <feOffset in="ab" dx="{dx * k:.2f}" dy="{dy * k:.2f}" result="abo"/>
  <feComposite in="SourceAlpha" in2="abo" operator="out" result="far"/>
  <feFlood flood-color="{r['amb']}" flood-opacity="{r['shade_op']}"/>
  <feComposite in2="far" operator="in" result="shade"/>
  <feBlend in="shade" in2="SourceGraphic" mode="multiply" result="shaded"/>
  <feOffset class="cl-o1" in="SourceAlpha" dx="{-dx * w:.2f}" dy="{-dy * w:.2f}" result="o1"/>
  <feComposite in="SourceAlpha" in2="o1" operator="out" result="r1"/>
  <feGaussianBlur in="r1" stdDeviation="{.45 * scale:.2f}" result="r1b"/>
  <feOffset class="cl-o2" in="SourceAlpha" dx="{-dx * W:.2f}" dy="{-dy * W:.2f}" result="o2"/>
  <feComposite in="SourceAlpha" in2="o2" operator="out" result="r2"/>
  <feGaussianBlur in="r2" stdDeviation="{2.2 * scale:.2f}" result="r2b"/>
  <feFlood flood-color="{r['rim']}" flood-opacity="{r['rim_op']}"/><feComposite in2="r1b" operator="in" result="rimA"/>
  <feFlood flood-color="{r['rim']}" flood-opacity="{r['rim_soft_op']}"/><feComposite in2="r2b" operator="in" result="rimB"/>
  <feMerge result="rim"><feMergeNode in="rimB"/><feMergeNode in="rimA"/></feMerge>
  <feComposite in="rim" in2="SourceAlpha" operator="in" result="rimIn"/>
  <feBlend in="rimIn" in2="shaded" mode="screen" result="lit"/>
  <feGaussianBlur in="rimA" stdDeviation="{2.6 * scale:.2f}" result="bl"/>
  <feComponentTransfer in="bl" result="bloom"><feFuncA type="linear" slope="{r['bloom']}"/></feComponentTransfer>
  <feMerge><feMergeNode in="lit"/><feMergeNode in="bloom"/></feMerge>
</filter>'''


def head_light(uid, face, direction, rig_name, key_on_face=True, prefix='cl'):
    """Soft gradient shading on face + neck AO + thin face rim, in head space.
    Put it inside the same transform as the head (head origin 0,0)."""
    r = RIGS[rig_name]
    dx, dy = direction
    fp = FACES[face]
    # gradient runs from the lit side (clear) to the far side (cool shade)
    x1, y1 = .5 + dx * .5, .5 + dy * .5
    x2, y2 = .5 - dx * .5, .5 - dy * .5
    rim = (f'<g clip-path="url(#{uid}-low)"><path d="{fp}" fill="none" stroke="{r["rim"]}" stroke-width="3.2" '
           f'clip-path="url(#{uid}-fc)" mask="url(#{uid}-lm)" opacity="{.85 if key_on_face else .5}"/></g>')
    return f'''<defs>
  <clipPath id="{uid}-fc"><path d="{fp}"/></clipPath>
  <linearGradient id="{uid}-fg" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}">
    <stop offset=".25" stop-color="{SKIN_SHADE}" stop-opacity="0"/>
    <stop offset="1" stop-color="{SKIN_SHADE}" stop-opacity="{r['face_shade'] * 1.5:.2f}"/>
  </linearGradient>
  <linearGradient id="{uid}-lg" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}">
    <stop offset="0" stop-color="#fff"/><stop offset=".32" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="{uid}-nf" maskContentUnits="userSpaceOnUse"><rect x="-50" y="-60" width="100" height="130" fill="#fff"/><path d="{fp}" fill="#000"/></mask>
  <clipPath id="{uid}-low"><rect x="-50" y="-12" width="100" height="60"/></clipPath>
  <mask id="{uid}-lm" maskContentUnits="userSpaceOnUse"><rect x="-50" y="-60" width="100" height="110" fill="url(#{uid}-lg)"/></mask>
  <radialGradient id="{uid}-wg" cx="{x1:.2f}" cy="{.42 + dy * .2:.2f}" r=".55">
    <stop offset="0" stop-color="{r['rim']}" stop-opacity=".12"/><stop offset="1" stop-color="{r['rim']}" stop-opacity="0"/>
  </radialGradient>
</defs>
<g class="cl-head" pointer-events="none">
  <rect x="-40" y="-50" width="80" height="95" fill="url(#{uid}-fg)" clip-path="url(#{uid}-fc)" style="mix-blend-mode:multiply"/>
  <rect x="-40" y="-50" width="80" height="95" fill="url(#{uid}-wg)" clip-path="url(#{uid}-fc)" style="mix-blend-mode:screen"/>
  <ellipse cx="0" cy="38" rx="15" ry="13" fill="url(#{prefix}-chinAO)" mask="url(#{uid}-nf)" style="mix-blend-mode:multiply"/>
  {rim}
</g>'''


def character(uid, inner, direction, rig_name, transform='', heads=(), scale=1.0, prefix='cl'):
    """inner: character markup (e.g. a <use>), drawn as-is.
    heads: list of (face_name, head_transform_inside_char) for gradient face shading.
    Returns (filter_def, markup). The filter goes into <defs>."""
    f = char_filter(f'{uid}-f', direction, rig_name, scale)
    hl = ''.join(f'<g transform="{transform} {ht}">{head_light(f"{uid}-h{i}", face, direction, rig_name, prefix=prefix)}</g>'
                 for i, (face, ht) in enumerate(heads))
    body = inner if not transform else f'<g transform="{transform}">{inner}</g>'
    return f, f'<g class="cl-char" id="{uid}" filter="url(#{uid}-f)" data-dir="{direction[0]:.3f},{direction[1]:.3f}">{body}{hl}</g>'


# ---------------------------------------------------------------- shadows
def contact_shadow(cx, cy, rx, ry=None, strength=1.0):
    ry = ry or rx * .14
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * 1.35:.1f}" ry="{ry * 1.8:.1f}" fill="url(#cl-contact)" opacity="{.55 * strength:.2f}" style="mix-blend-mode:multiply"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * .7:.1f}" ry="{ry * .7:.1f}" fill="url(#cl-contact)" opacity="{.9 * strength:.2f}" style="mix-blend-mode:multiply"/>')


def ao_line(x1, y1, x2, y2, width=18, strength=.5, color='#0b0e1a'):
    """Ambient occlusion along a crease (wall/floor, under furniture, corners)."""
    return (f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
            f'opacity="{strength}" filter="url(#cl-soft2)" style="mix-blend-mode:multiply"/>')


def ao_corner(path_d, strength=.45, color='#0b0e1a'):
    return f'<path d="{path_d}" fill="{color}" opacity="{strength}" filter="url(#cl-soft)" style="mix-blend-mode:multiply"/>'


# ---------------------------------------------------------------- light
_gid = [0]


def glow(cx, cy, r, color, strength=.5, core=True):
    _gid[0] += 1
    g = f'clg{_gid[0]}'
    out = (f'<radialGradient id="{g}"><stop offset="0" stop-color="{color}" stop-opacity="{strength}"/>'
           f'<stop offset=".35" stop-color="{color}" stop-opacity="{strength * .38:.3f}"/>'
           f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{g})" style="mix-blend-mode:screen"/>')
    if core:
        out += f'<circle cx="{cx}" cy="{cy}" r="{r * .12:.1f}" fill="#fff8ef" opacity=".55" filter="url(#cl-soft2)" style="mix-blend-mode:screen"/>'
    return out


def shaft(points, color, strength=.35, src=None, end=None, dust_n=0, seed=1):
    """Soft beam polygon with gradient falloff from src to end; optional dust clipped inside."""
    _gid[0] += 1
    g = f'cls{_gid[0]}'
    pts = ' '.join(f'{x},{y}' for x, y in points)
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    src = src or points[0]
    end = end or (sum(xs) / len(xs) * 2 - src[0], sum(ys) / len(ys) * 2 - src[1])
    out = (f'<linearGradient id="{g}" gradientUnits="userSpaceOnUse" x1="{src[0]}" y1="{src[1]}" x2="{end[0]:.0f}" y2="{end[1]:.0f}">'
           f'<stop offset="0" stop-color="{color}" stop-opacity="{strength}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>'
           f'<clipPath id="{g}c"><polygon points="{pts}"/></clipPath>'
           f'<polygon points="{pts}" fill="url(#{g})" filter="url(#cl-soft)" style="mix-blend-mode:screen"/>')
    if dust_n:
        out += f'<g clip-path="url(#{g}c)">{dust((min(xs), min(ys), max(xs), max(ys)), dust_n, seed)}</g>'
    return out


def falloff(cx, cy, r, strength=.55, color='#0a0e1c', inner=.35):
    """Low-key light falloff: frame darkens with distance from the motivating light (multiply)."""
    _gid[0] += 1
    g = f'clf{_gid[0]}'
    return (f'<radialGradient id="{g}" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{r}">'
            f'<stop offset="{inner}" stop-color="{color}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="{strength}"/></radialGradient>'
            f'<rect x="-600" y="-600" width="1740" height="2160" fill="url(#{g})" style="mix-blend-mode:multiply"/>')


def dust(box, n, seed=1, color='#fff4e6'):
    """Motes: a few sharp ones with a faint bloom, more blurred far ones. No sparkles."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    near = far = ''
    for i in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if i % 3 == 0:
            near += f'<circle class="cl-mote" cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.6, 1.2):.2f}" opacity="{rnd.uniform(.55, .9):.2f}"/>'
        else:
            far += f'<circle class="cl-mote" cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1.2, 2.4):.2f}" opacity="{rnd.uniform(.18, .38):.2f}"/>'
    return f'<g fill="{color}"><g filter="url(#cl-moteFar)">{far}</g><g filter="url(#cl-moteSharp)">{near}</g></g>'


# ---------------------------------------------------------------- compose
def compose(rig_name, bg='', shadow='', chars='', light='', atmos='', ui='', extra_defs='', view='0 0 540 960',
            frame_transform='', label='', prefix='cl'):
    r = RIGS[rig_name]
    inner = (f'<g id="L-bg">{bg}</g><g id="L-shadow">{shadow}</g><g id="L-char">{chars}</g>'
             f'<g id="L-light">{light}</g><g id="L-atmos">{atmos}</g>')
    if frame_transform:
        inner = f'<g transform="{frame_transform}">{inner}</g>'
    return (f'<svg viewBox="{view}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">'
            f'<defs>{defs(rig_name, prefix)}{extra_defs}</defs>'
            f'<g id="L-graded" filter="url(#{prefix}-grade)">{inner}</g>'
            f'<g id="L-post" pointer-events="none"><rect width="540" height="960" fill="url(#{prefix}-vig)" style="mix-blend-mode:multiply"/>'
            f'<rect width="540" height="960" filter="url(#{prefix}-grain)" opacity="{r["grain"]}" style="mix-blend-mode:overlay"/>'
            f'<rect width="540" height="960" filter="url(#{prefix}-grain)" opacity="{r["grain"] * .5:.3f}" style="mix-blend-mode:screen"/></g>'
            f'<g id="L-ui">{ui}</g></svg>')
