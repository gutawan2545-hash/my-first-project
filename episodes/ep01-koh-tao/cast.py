"""EP.01 cast with articulated arms (shoulder -> elbow -> hand) for the full clip.
Bodies are the approved ones (sun_gen / islanders_gen / style5); only the arms are swapped for pipeline/motion/rig.py
arms and the static sleeves trimmed to a shoulder cap so the sleeve can travel with the upper arm."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'motion'))
import rig as RG
import omkit as M
import sunrig as R
import style5 as S5
import kt_scenes as K

ISL = K.ISL
SK, SKS, SKH = R.SK, R.SKS, R.SKH                    # pale (Bangkok, past)
TSK, TSKS, TSKH = '#e9b993', '#d29e78', '#f5d2b2'    # tan (islander, present)


def _arms(uid, sk, sks, skh, seqL, seqR, holdL='', holdR='', **kw):
    kwL = {k[:-2] if k.endswith('_L') else k: v for k, v in kw.items() if not k.endswith('_R')}
    kwR = {k[:-2] if k.endswith('_R') else k: v for k, v in kw.items() if not k.endswith('_L')}
    return (RG.arm(uid, 'L', sk, sks, skh, seq=seqL, hold=holdL, **kwL)
            + RG.arm(uid, 'R', sk, sks, skh, seq=seqR, hold=holdR, **kwR))


# ---------------------------------------------------------------- James, islander (present, tan)
_ISL_ARMS = ISL['arms'](SK, SKS, SKH)
_BRACELET = '<path d="M -56,226 L -41,226" stroke="#a07a58" stroke-width="5"/>'
_SLEEVE_HEM = '<path d="M -58,112 L -40,118 L -40,124 L -58,118 Z M 58,112 L 40,118 L 40,124 L 58,118 Z" fill="#163b5e"/>'


def _island_torso():
    t = S5.SUN_ISLAND2.replace(_ISL_ARMS, '').replace(_BRACELET, '').replace(_SLEEVE_HEM, '')
    t = t.replace('L -58,118 L -40,124', 'L -49,90 L -41,100').replace('L 58,118 L 40,124', 'L 49,90 L 41,100').replace('L -40,124 L -58,118', 'L -41,100 L -49,90')
    return t


ISLAND_TORSO = _island_torso()


def james_now(uid, head, seqL=None, seqR=None, holdL='', holdR='', mid=''):
    """head: an animated head id (e.g. from anim()). Tan skin."""
    arms = _arms(uid, SK, SKS, SKH, seqL, seqR, holdL, holdR, sh=(48, 74), el_y=168, hand_y=234,
                 sleeve_L=('url(#hawaii)', None, 118, '#163b5e', 10.5), sleeve_R=('url(#hawaii)', '#0b1a2c', 118, '#163b5e', 10.5),
                 wrist_L='<path d="M -55.5,226 L -40.5,226" stroke="#a07a58" stroke-width="5"/>')
    return R.tanify(ISLAND_TORSO) + mid + R.tanify(arms) + f'<use href="#{head}"/>' + S5.NECK


def james_now_static(head='smirk'):
    return S5.sun_island(head)


# ---------------------------------------------------------------- James, Bangkok outfit (past, pale)
P = R.PARTS


def _bkk_shirt():
    s = P['shirt']
    s = s.replace('<path d="M -64,132 L -46,138 L -46,146 L -66,140 Z" fill="#e9e1d0"/>', '').replace('<path d="M 64,132 L 46,138 L 46,146 L 66,140 Z" fill="#d2c9b6"/>', '')
    s = s.replace('L -66,140 L -46,146', 'L -55,94 L -46,104').replace('L 66,140 L 46,146', 'L 55,94 L 46,104')
    s = s.replace('L -46,146 L -66,140', 'L -46,104 L -55,94')
    s = s.replace('L -64,132 L -46,138', 'L -55,94 L -46,104').replace('L 64,132 L 46,138', 'L 55,94 L 46,104')
    return s


BKK_SHIRT = _bkk_shirt()


def james_then(uid, head, seqL=None, seqR=None, holdL='', holdR='', tote=True, camera=False, legs=True, mid=''):
    out = (P['trousers'] + P['ankles'] + P['shoes']) if legs else ''
    out += P['tee'] + BKK_SHIRT + P['collar'] + P['pocket'] + (P['tote'] if tote else '') + mid
    out += _arms(uid, SK, SKS, SKH, seqL, seqR, holdL, holdR, sh=(52, 74), el_y=172, hand_y=236,
                 sleeve_L=(['#3e7074', 'url(#print)'], None, 140, '#e9e1d0', 12.5), sleeve_R=(['#26494d', 'url(#print)'], '#0b1a2c', 140, '#d2c9b6', 12.5))
    if camera:
        out += P['camera']
    out += f'<use href="#{head}"/>' + R.NECK_AFTER + (R.STRAP if camera else '')
    return out


# ---------------------------------------------------------------- James, chef whites (past, pale)
CHEF_HAT = ('<g><path d="M -30,-40 C -30,-52 30,-52 30,-40 L 28,-30 L -28,-30 Z" fill="#ece8e0"/>'
            '<path d="M -34,-44 C -50,-60 -40,-92 -16,-88 C -10,-108 18,-108 22,-88 C 44,-94 52,-62 34,-44 Z" fill="#f8f6f0"/>'
            '<path d="M 22,-88 C 44,-94 52,-62 34,-44 L 20,-44 C 30,-60 30,-76 22,-88 Z" fill="#dcd6cc"/>'
            '<path d="M -30,-40 L 30,-40" stroke="#dcd6cc" stroke-width="2"/></g>')


def chef_torso():
    return ('<path d="M -42,226 L 42,226 L 45,300 L 39,456 L 9,456 L 3,296 L -3,296 L -9,456 L -39,456 L -45,300 Z" fill="#2c2f38"/>'
            '<path d="M -42,226 L -26,226 L -30,300 L -28,456 L -39,456 L -45,300 Z" fill="#3a3d48"/>'
            '<path d="M -42,454 L -6,454 C -4,466 -6,474 -10,476 L -44,476 C -48,472 -47,460 -42,454 Z M 42,454 L 6,454 C 4,466 6,474 10,476 L 44,476 C 48,472 47,460 42,454 Z" fill="#1d1f26"/>'
            # double-breasted chef jacket
            '<path d="M -12,48 C -28,50 -42,56 -48,66 L -50,96 L -44,104 L -44,240 L 44,240 L 44,104 L 50,96 L 48,66 C 42,56 28,50 12,48 Z" fill="#f4f1ea"/>'
            '<path d="M -48,66 C -42,56 -32,52 -22,50 C -28,80 -32,140 -30,240 L -44,240 L -44,104 L -50,96 Z" fill="#ffffff"/>'
            '<path d="M 22,50 C 34,53 44,58 48,66 L 50,96 L 44,104 L 44,240 L 30,240 C 32,160 30,90 22,50 Z" fill="#d9d3c8"/>'
            '<path d="M -14,50 L 24,60 L 24,240" stroke="#d9d3c8" stroke-width="2" fill="none"/>'
            + ''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#2c2f38"/>' for x in (-8, 14) for y in (84, 118, 152, 186))
            + '<path d="M -14,46 L 14,46 L 14,56 L -14,56 Z" fill="#f4f1ea"/><path d="M -14,46 L 14,46" stroke="#d9d3c8" stroke-width="2"/>'
            # apron + towel
            '<path d="M -40,176 L 40,176 L 42,330 L -42,330 Z" fill="#3a3d48"/><path d="M -40,176 L -26,176 L -28,330 L -42,330 Z" fill="#4a4e5a"/>'
            '<path d="M -40,176 L 40,176" stroke="#2c2f38" stroke-width="4"/>'
            '<path d="M 18,180 L 32,180 L 30,236 L 20,236 Z" fill="#c9d4dc"/><path d="M 18,196 L 32,196 M 19,214 L 31,214" stroke="#8aa0b4" stroke-width="2"/>')


def james_chef(uid, head, seqL=None, seqR=None, holdL='', holdR='', hat=True, hat_io=''):
    out = chef_torso()
    out += _arms(uid, SK, SKS, SKH, seqL, seqR, holdL, holdR, sh=(48, 74), el_y=170, hand_y=236,
                 sleeve_L=('#ffffff', None, 172, None, 11), sleeve_R=('#d9d3c8', None, 172, None, 11),
                 fore_sleeve_L=('#ffffff', None, 214, '#e8e2d6'), fore_sleeve_R=('#d9d3c8', None, 214, '#cfc8bb'))
    out += f'<use href="#{head}"/>'
    if hat:
        out += f'<g {hat_io}>{CHEF_HAT}</g>' if hat_io else CHEF_HAT
    return out


# ---------------------------------------------------------------- islanders: swap their static arms for rigged ones
def _swap(body, static_arms, uid, sk, sks, skh, seqL, seqR, holdL='', holdR='', sleeve=None, tee=None, **kw):
    b = body.replace(static_arms, '')
    if tee:                                   # trim tee sleeves to a shoulder cap
        old, new = tee
        b = b.replace(old, new)
    slL = slR = None
    if sleeve:
        f, fl, fd, hem = sleeve
        slL, slR = (fl, None, hem, None, 10.5), (fd, None, hem, None, 10.5)
    return b + _arms(uid, sk, sks, skh, seqL, seqR, holdL, holdR, sleeve_L=slL, sleeve_R=slR, **kw)


def _tee_trim(c, cl, cd, hem=234, sleeve_len=116):
    old = ISL['tee'](c, cl, cd, hem, sleeve_len)
    new = old.replace(f'L 57,{sleeve_len} L 40,{sleeve_len + 6}', 'L 49,90 L 41,100').replace(f'L -40,{sleeve_len + 6} L -57,{sleeve_len}', 'L -41,100 L -49,90')
    return old, new


BANANA_BAG = ISL['AUNT_BODY'][ISL['AUNT_BODY'].index('<g transform="translate(-62,262)">'):]


def aunt(uid, seqL=None, seqR=None, head='h_aunt', holdL='', holdR=''):
    sk = ('#e4ae86', '#cc9670', '#f2cba8')
    body = ISL['AUNT_BODY'].replace(BANANA_BAG, '')
    return _swap(body, ISL['arms'](*sk), uid, *sk, seqL, seqR, holdL, holdR, sleeve=('#c8a2c8', '#dcbcdc', '#a983ad', 150),
                 tee=_tee_trim('#c8a2c8', '#dcbcdc', '#a983ad', 214, 150), sh=(48, 74), el_y=168, hand_y=234) + f'<use href="#{head}"/>'


def agent(uid, seqL=None, seqR=None, head='h_agent'):
    sk = ('#e9b993', '#d29e78', '#f5d2b2')
    body = ISL['AGENT_BODY']
    clip = body[body.index('<g transform="translate(46,214) rotate(-8)">'):]
    clip = clip[:clip.index('</g>') + 4]
    body = body.replace(clip, '')
    return _swap(body, ISL['arms'](*sk), uid, *sk, seqL, seqR, '', '', sleeve=('#efe6d6', '#faf4ea', '#d6ccba', 116),
                 tee=_tee_trim('#efe6d6', '#faf4ea', '#d6ccba', 232), sh=(48, 74), el_y=168, hand_y=234) + f'<use href="#{head}"/>'


def uncle(uid, seqL=None, seqR=None, head='h_uncle'):
    sk = ('#d9a07a', '#c08860', '#e8bc98')
    return _swap(ISL['UNCLE_BODY'], ISL['arms'](*sk, tank=True), uid, *sk, seqL, seqR, sh=(46, 72), el_y=166, hand_y=234) + f'<use href="#{head}"/>'


def electrician(uid, seqL=None, seqR=None, head='h_elec', holdL=''):
    sk = ('#e9b993', '#d29e78', '#f5d2b2')
    body = ISL['ELEC_BODY']
    torch = '<g transform="translate(-60,266)">'
    body = body[:body.index(torch)] if torch in body else body
    return _swap(body, ISL['arms'](*sk), uid, *sk, seqL, seqR, holdL, '', sleeve=('#2c3a54', '#3d4f6e', '#1f2a40', 116),
                 tee=_tee_trim('#2c3a54', '#3d4f6e', '#1f2a40', 232), sh=(48, 74), el_y=168, hand_y=234) + f'<use href="#{head}"/>'


def neighbour(uid, seqL=None, seqR=None, head='h_nb'):
    sk = ('#f8d8c6', '#ebbca6', '#fff0e8')
    body = ISL['NB_BODY']
    mask = body[body.index('<g transform="translate(-60,272)">'):]
    body = body.replace(mask, '')
    return _swap(body, ISL['arms'](*sk), uid, *sk, seqL, seqR, sleeve=('#2c3a54', '#3d4f6e', '#1f2a40', 116),
                 tee=_tee_trim('#2c3a54', '#3d4f6e', '#1f2a40'), sh=(48, 74), el_y=168, hand_y=234) + f'<use href="#{head}"/>'


# ---------------------------------------------------------------- animated heads
ALL_DEFS = R.HEAD_DEFS + ISL['CLIPS'] + ISL['AUNT_HEAD'] + ISL['AGENT_HEAD'] + ISL['UNCLE_HEAD'] + ISL['ELEC_HEAD'] + ISL['NB_HEAD'] + ISL['LAE_BACK'] + ISL['LAE_HEAD']
_made = {}


def anim(src, new_id):
    """Animated copy of a head: blink, glance, lip sync. src: sunrig head id ('sh_dead', 'shead_t'...) or islander head id."""
    if new_id in _made:
        return new_id
    skin = {'h_aunt': '#cc9670', 'h_agent': '#d29e78', 'h_uncle': '#c08860', 'h_elec': '#d29e78', 'h_nb': '#ebbca6'}
    if src in skin:
        kind, clips, sk = ('tawan', ('teyeL', 'teyeR'), skin[src]) if src == 'h_aunt' else ('james', ('jeyeL', 'jeyeR'), skin[src])
        _made[new_id] = M.anim_head(ALL_DEFS, src, new_id, sk, kind, clips)
    else:
        sk = '#d29e78' if src.endswith('_t') else '#efc7b0'
        _made[new_id] = M.anim_head(R.HEAD_DEFS, src, new_id, sk)
    return new_id


def anim_defs():
    return ''.join(_made.values())
