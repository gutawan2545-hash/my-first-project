"""Odd Hours articulated arms (reusable for every episode).

Each arm is a shoulder group (rotates about the shoulder) holding the upper arm + sleeve and a nested elbow group
(rotates about the elbow) holding the forearm, hand and anything the hand carries. oddmotion.js drives the angles
from keyframes (data-k) plus a small idle sway (data-sway), so the forearm always follows the upper arm.

Angles are written side-normalised:  abd = shoulder abduction (arm swings out to the side, + = away from the body)
                                      flex = elbow flex (forearm folds up toward the chest, + = toward the midline)
"""
import random

POSES = {                      # (abd, flex)
    'rest': (3, 4), 'relax': (6, 14),
    'talk': (12, 72), 'talk2': (20, 98), 'open': (34, 44), 'explain': (26, 86),
    'hip': (40, 86), 'shrug': (46, 112), 'chest': (8, 128),
    'wave': (150, 10), 'wave2': (150, 40), 'point_up': (166, 4), 'point_out': (84, 2), 'reach': (62, 30),
    'catch': (128, 26), 'hat': (162, 46), 'table': (18, 70), 'phone': (14, 132), 'carry': (16, 100),
    'stir': (24, 82), 'stir2': (28, 64), 'hold': (10, 92),
}


def _ang(side, abd, flex):
    s = -1 if side == 'L' else 1
    return -s * abd, s * flex


def keys(side, seq):
    """seq: [(t, pose or (abd, flex)), ...] -> (shoulder data-k, elbow data-k) strings."""
    sh, el = [], []
    for t, p in sorted(seq, key=lambda x: x[0]):
        abd, flex = POSES[p] if isinstance(p, str) else p
        a, f = _ang(side, abd, flex)
        sh.append(f'{t:.2f},{a:.1f}')
        el.append(f'{t:.2f},{f:.1f}')
    return ';'.join(sh), ';'.join(el)


def talk_seq(intervals, rest='rest', pose='talk', alt='explain', seed=1, beat=.52, amp=(6, 16)):
    """Gestures that follow speech: arm comes up as the line starts, beats on the phrasing, settles after."""
    r = random.Random(seed)
    seq = [(0, rest)]
    for a, b in intervals:
        seq.append((max(0, a - .28), rest))
        base = POSES[pose]
        seq.append((a + .12, base))
        t, k = a + .12 + beat, 0
        while t < b - .15:
            p = POSES[alt] if k % 3 == 2 else base
            seq.append((t, (p[0] + r.uniform(-amp[0], amp[0]), p[1] + (amp[1] if k % 2 else -amp[1] * .6) + r.uniform(-4, 4))))
            t += beat * r.uniform(.8, 1.25); k += 1
        seq.append((b + .05, base))
        seq.append((b + .45, rest))
    return seq


def arm(uid, side, sk, skd, skh, *, sh=(48, 74), el_y=170, hand_y=236, wu=8.5, wf=7.2,
        sleeve=None, fore_sleeve=None, hold='', wrist='', seq=None, sway=(1.6, 3.8)):
    """sleeve = (fill, shade_or_None, hem_y, hem_band_color_or_None, half_width)
    fore_sleeve = (fill, shade_or_None, cuff_y, cuff_color_or_None) for long sleeves."""
    s = -1 if side == 'L' else 1
    X = lambda v: f'{s * v:.1f}'
    sx, sy = sh
    base = sk if side == 'L' else skd
    up = (f'<path d="M {X(sx - wu)},{sy - 8} C {X(sx)},{sy - 14} {X(sx + wu + 2)},{sy - 6} {X(sx + wu + 1)},{sy + 8} '
          f'L {X(sx + wu)},{el_y} L {X(sx - wu)},{el_y} L {X(sx - wu - 1)},{sy + 6} Z" fill="{base}"/>')
    if side == 'L':
        up += f'<path d="M {X(sx + wu - 2)},{sy + 10} L {X(sx + wu)},{sy + 10} L {X(sx + wu - .5)},{el_y} L {X(sx + wu - 3)},{el_y} Z" fill="{skh}" opacity=".7"/>'
    if sleeve:
        f, shd, hem, band, hw = sleeve
        sl = (f'M {X(sx - hw + 1)},{sy - 12} C {X(sx)},{sy - 18} {X(sx + hw + 2)},{sy - 8} {X(sx + hw + 1)},{sy + 8} '
              f'L {X(sx + hw)},{hem} L {X(sx - hw)},{hem + 4} L {X(sx - hw - 1)},{sy + 4} Z')
        up += ''.join(f'<path d="{sl}" fill="{ff}"/>' for ff in (f if isinstance(f, (list, tuple)) else [f]))
        if shd:
            up += f'<path d="{sl}" fill="{shd}" opacity="{.28 if side == "R" else .0}"/>'
        if band:
            up += f'<path d="M {X(sx + hw)},{hem - 5} L {X(sx - hw)},{hem - 1} L {X(sx - hw)},{hem + 4} L {X(sx + hw)},{hem} Z" fill="{band}"/>'
    elbow = f'<circle cx="{X(sx)}" cy="{el_y}" r="{wf + .6:.1f}" fill="{base}"/>'
    fore = f'<path d="M {X(sx + wf + .6)},{el_y - 2} L {X(sx + wf)},{hand_y} L {X(sx - wf)},{hand_y} L {X(sx - wf - .6)},{el_y - 2} Z" fill="{base}"/>'
    if side == 'L':
        fore += f'<path d="M {X(sx + wf - 2)},{el_y} L {X(sx + wf)},{el_y} L {X(sx + wf - .3)},{hand_y} L {X(sx + wf - 2.6)},{hand_y} Z" fill="{skh}" opacity=".6"/>'
    hand = (f'<path d="M {X(sx + wf + .4)},{hand_y - 2} L {X(sx - wf - .4)},{hand_y - 2} C {X(sx - wf - 1.5)},{hand_y + 12} {X(sx - wf + 1)},{hand_y + 26} {X(sx)},{hand_y + 28} '
            f'C {X(sx + wf - 1)},{hand_y + 28} {X(sx + wf + 1.8)},{hand_y + 14} {X(sx + wf + .4)},{hand_y - 2} Z" fill="{base}"/>'
            f'<path d="M {X(sx - wf + 1)},{hand_y} C {X(sx - wf - 4)},{hand_y + 4} {X(sx - wf - 4)},{hand_y + 10} {X(sx - wf - 1)},{hand_y + 13} L {X(sx - wf + 1)},{hand_y + 8} Z" fill="{skd if side == "L" else base}"/>')
    if fore_sleeve:
        f, shd, cuff, cc = fore_sleeve
        fs = f'M {X(sx + wf + 3)},{el_y - 10} L {X(sx + wf + 2)},{cuff} L {X(sx - wf - 2)},{cuff} L {X(sx - wf - 3)},{el_y - 10} Z'
        fore += f'<circle cx="{X(sx)}" cy="{el_y}" r="{wf + 3:.1f}" fill="{f}"/><path d="{fs}" fill="{f}"/>'
        if shd and side == 'R':
            fore += f'<path d="{fs}" fill="{shd}" opacity=".25"/>'
        if cc:
            fore += f'<path d="M {X(sx + wf + 2)},{cuff - 7} L {X(sx - wf - 2)},{cuff - 7} L {X(sx - wf - 2)},{cuff} L {X(sx + wf + 2)},{cuff} Z" fill="{cc}"/>'
    ks, ke = keys(side, seq or [(0, 'rest')])
    ph = .0 if side == 'L' else 1.7
    return (f'<g id="{uid}-{side}s" data-rot="{X(sx)},{sy}" data-k="{ks}" data-sway="{sway[0]},{sway[1]},{ph}">{up}'
            f'<g id="{uid}-{side}e" data-rot="{X(sx)},{el_y}" data-k="{ke}" data-sway="{sway[0] * 1.4:.1f},{sway[1] * .9:.1f},{ph + .8:.1f}">{elbow}{fore}{hand}{wrist}{hold}</g></g>')
