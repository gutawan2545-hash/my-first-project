"""EP.01 full clip: every shot as a page on the global clock (clip_timeline.T), rendered frame by frame.
Run: python3 clip.py  -> clip_pages/<nn>_<name>.html + clip_pages/shots.json
Speaker rule: the camera is on whoever talks; only that character's mouth moves (loudness of their own voice file)."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, HERE)
for p in ('pipeline/lighting', 'pipeline/motion'):
    sys.path.insert(0, os.path.join(ROOT, p))
import omkit as M
import rig as RG
import cast as C
import sunrig as R
import kt_scenes as K
import style4 as S4
import style5 as S5
import style6 as S6
import clip_scenes as CS
import motion_preview as MP
from clip_timeline import T, at, SUB, TOTAL, FPS

OUT = os.path.join(HERE, 'clip_pages')
ENGINE = open(os.path.join(ROOT, 'pipeline', 'motion', 'oddmotion.js')).read()
ENV = json.load(open(os.path.join(HERE, 'vo', 'env.json')))
EYE = S4.EYE
ISL = K.ISL
SHOTS = []


# ---------------------------------------------------------------- helpers
def put(svg, old, new):
    assert old in svg, 'missing: ' + old[:80]
    return svg.replace(old, new, 1)


def talk(key):
    a, b = T[key]
    return [a, b, key]


def ui_for(t0, t1, extra='', subs=True, eye=True):
    out = extra
    if subs:
        keys = sorted(T, key=lambda k: T[k][0])
        for i, k in enumerate(keys):
            a, b = T[k]
            if b > t0 + .02 and a < t1 - .02:
                nxt = T[keys[i + 1]][0] if i + 1 < len(keys) else TOTAL
                th, en = SUB[k]
                n = th.count('/') + 1
                gap = max(.3, min(1.5, (b - a) / (n + .3)))
                out += M.subs(th, en, a, min(b + .35, nxt - .22), line_gap=gap)
    return out + (EYE if eye else '')


def set_ui(svg, ui):
    a = svg.rindex('<g id="L-ui">')
    return svg[:a] + f'<g id="L-ui">{ui}</g></svg>'


def breath(svg):
    return re.sub(r'(<g class="cl-char"[^>]*>)<g transform="', r'\1<g data-breath="1.1,3.8" transform="', svg)


def shot(name, t0, t1, svg, faces=(), ui='', frame=None, cam='1,1.04,0,0', past=False, zb=None, subs=True, eye=True):
    SHOTS.append(dict(name=name, t0=round(t0, 3), t1=round(t1, 3), svg=svg, faces=list(faces), ui=ui, frame=frame, cam=cam, past=past, zb=zb, subs=subs, eye=eye))


def face(fid, key=None, glance=(), seed=3, blinkAt=(), extra_talk=()):
    f = {'id': fid, 'glance': [list(g) for g in glance], 'seed': seed, 'blinkAt': list(blinkAt)}
    f['talk'] = ([talk(key)] if key else []) + [list(x) for x in extra_talk]
    return f


A = C.anim
COFFEE = ('<g><path d="M -61,232 L -35,232 L -37.5,264 L -58.5,264 Z" fill="#f4efe6"/><rect x="-62.5" y="227" width="29" height="6" rx="2" fill="#4a3a34"/>'
          '<path d="M -60,244 L -36,244 L -36.8,254 L -59.2,254 Z" fill="#b98c6a"/></g>')
PHONE_L = '<g><rect x="-60" y="226" width="22" height="40" rx="4" fill="#15151c"/><rect x="-57.5" y="229.5" width="17" height="33" rx="2.5" fill="#9fb8ff" opacity=".85"/></g>'


def bag(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M -6,-30 C -6,-48 14,-48 14,-30" stroke="#b49a78" stroke-width="4" fill="none"/>'
            '<path d="M -22,-30 L 30,-30 L 26,30 L -18,30 Z" fill="#e6dcc6"/><path d="M 14,-30 L 30,-30 L 26,30 L 12,30 Z" fill="#cfc3aa"/>'
            '<path d="M -10,-30 C -14,-50 -4,-60 6,-58 C 0,-52 -2,-42 0,-30 Z M 2,-30 C 2,-52 14,-60 22,-54 C 14,-50 10,-42 10,-30 Z" fill="#e8c35e"/></g>')


# ================================================================ 1. present: James on the street (narration)
J_ISL_STATIC = S5.sun_island('smirk')
A('shead_t', 'jT1')
t1a, t1b = 0, at('N01', .52)
seqL = [(0, 'rest'), (2.4, 'rest'), (2.9, 'chest'), (3.5, 'chest'), (3.9, 'relax'), (5.6, 'relax'), (6.0, 'chest'), (6.5, 'relax')]
seqR = [(0, 'rest'), (.7, 'rest'), (1.1, 'wave'), (1.35, 'wave2'), (1.6, 'wave'), (1.85, 'wave2'), (2.1, 'wave'), (2.6, 'hip'), (8, 'hip')]
street_now = S6.renamed(S6.street())
svg = put(street_now, J_ISL_STATIC, C.james_now('j1', 'jT1', seqL, seqR, holdL=COFFEE))
f1 = face('jT1', glance=[[.2, 1.6, .4], [3.0, 0, 0], [5.4, -1.8, .3]], seed=4)
shot('street_wide', t1a, t1b, breath(svg), [f1], M.tag('ปัจจุบัน · เกาะเต่า', .2, t1b - .1), cam='1,1.05,0,-10,0,4')
shot('street_close', t1b, at('J01') - .28, breath(svg), [f1], M.tag('ครูสอนดำน้ำ · JAMES', t1b + .2, at('N01', 1) - .1), frame=(1.75, 238, 470), cam='1,1.04,-6,0,3.6,7.4')

# ================================================================ 2. auntie tosses bananas, James: "ขอบคุณครับป้า!"
A('sh_grin_t', 'jG1')
shop_now = S4.shop()
J_BKK_SHOP = R.body(head='annoy', tote=True, camera=False)
AUNT_STATIC = ISL['AUNT_BODY'] + '<use href="#h_aunt"/>'
ta = at('J01')
toss = ta - .25
bag_in_aunt = f'<g data-in="fade" data-at="0" data-dur=".01" data-out="fade" data-out-at="{toss:.2f}" data-out-dur=".06">{bag(48, 280, .9)}</g>'
bag_in_james = f'<g data-in="pop" data-at="{toss + .05:.2f}" data-dur=".3">{bag(-48, 280, .9)}</g>'
aunt_seq_R = [(0, 'relax'), (toss - .5, 'relax'), (toss - .15, 'reach'), (toss + .25, 'wave'), (toss + .55, 'wave2'), (toss + .85, 'wave'), (toss + 1.3, 'relax')]
svg = put(shop_now, J_BKK_SHOP, C.james_now('j2', 'jG1', [(0, 'rest'), (toss - .2, 'rest'), (toss + .05, 'catch'), (ta + .9, 'catch'), (ta + 1.4, 'talk')],
                                              RG.talk_seq([T['J01'][:2]], seed=2), holdL=bag_in_james))
svg = put(svg, 'href="#sh_annoy"', 'href="#jG1"') if 'href="#sh_annoy"' in svg else svg
svg = put(svg, AUNT_STATIC, C.aunt('au1', [(0, 'relax')], aunt_seq_R, holdR=bag_in_aunt))
shot('shop_thanks', at('J01') - .28, at('N02') - .3, breath(svg), [face('jG1', 'J01', glance=[[toss - .3, -2.4, 0]], seed=6)],
     cam=f'1,1.05,20,0,{at("J01") - .28},{at("N02") - .3}')

# ================================================================ 3. flashback: Bangkok kitchen (warm faded)
A('sh_dead', 'jC1'); A('sh_annoy', 'jC2')
stir = [(0, 'stir')] + [(i * .32, 'stir' if i % 2 else 'stir2') for i in range(1, 60)]
kit = CS.kitchen(C.james_chef('jc1', 'jC1', [(0, 'table')], [(0, (40, 30))] + [(i * .3, (36, 22) if i % 2 else (46, 40)) for i in range(1, 80)]), 'jC1')
t3 = at('N02') - .3
shot('kitchen', t3, at('N02', .55), breath(kit), [face('jC1', glance=[[.0, 1.6, 1.4]], seed=7)],
     M.tag('สองปีก่อน · กรุงเทพ', t3 + .5, at('N02', .55) - .1), cam=f'1.02,1.06,0,-10,{t3},{at("N02", .55)}', past=True, zb=(t3, .42, 'in'))
shot('kitchen_close', at('N02', .55), at('N03', .56), breath(kit), [face('jC1', glance=[[.0, 1.6, 1.4], [at('N03', .1), 0, 0]], seed=7)],
     M.callout(318, 150, 196, ['กรุงเทพเนทีฟ', 'เกิดและโตที่นี่'], 330, 470, at('N03') + .1, at('N03', .56) - .2, '#7a5ab8'),
     frame=(1.55, 220, 470), cam=f'1,1.05,0,0,{at("N02", .55)},{at("N03", .56)}', past=True)

# ================================================================ 4. flashback: taxi in traffic
A('sh_dead', 'jC3')
tx = CS.taxi(C.james_then('jt1', 'jC3', [(0, 'phone')], [(0, 'relax')], holdL=PHONE_L, tote=False, legs=False), at('N03', .58), at('N03', 1) + .1)
shot('taxi', at('N03', .56), at('N03', 1) + .2, breath(tx), [face('jC3', glance=[[.0, 0, 2.2]], seed=8)], cam=f'1.02,1.07,0,0,{at("N03", .56)},{at("N03", 1)}', past=True)

# ================================================================ 5. "พอกันที" + title
tq0, tq1 = at('N03', 1) + .2, at('N04') - .08
swap = at('J02') + .35
hat_io = f'data-in="fade" data-at="0" data-dur=".01" data-out="fade" data-out-at="{swap:.2f}" data-out-dur=".05"'
hat_hand = f'<g data-in="fade" data-at="{swap:.2f}" data-dur=".05"><g transform="translate(48,292) scale(.9)">{C.CHEF_HAT}</g></g>'
seqR = [(0, 'relax'), (at('J02') - .35, 'relax'), (at('J02') + .2, 'hat'), (swap + .1, 'hat'), (swap + .8, 'table'), (tq1, 'table')]
kq = CS.kitchen(C.james_chef('jc2', 'jC2', [(0, 'relax')], seqR, holdR=hat_hand, hat_io=hat_io), 'jC2')
title = (f'<g data-in="mask-right" data-at="{at("J02", 1) + .1:.2f}" data-dur=".6" data-out="fade" data-out-at="{tq1 - .25:.2f}" data-out-dur=".25" {M.TH}>'
         f'<rect x="30" y="168" width="480" height="150" rx="18" fill="#120e1c" fill-opacity=".86" stroke="#9a86ff"/>'
         f'<text x="270" y="206" font-size="15" font-weight="700" fill="#c9b8f2" text-anchor="middle">EP.01</text>'
         f'<text x="270" y="250" font-size="30" font-weight="800" fill="#fff" text-anchor="middle">เมื่อ<tspan fill="#c9a8ff">กรุงเทพเนทีฟ</tspan></text>'
         f'<text x="270" y="294" font-size="30" font-weight="800" fill="#fff" text-anchor="middle">ย้ายไปอยู่เกาะเต่า</text></g>')
shot('quit', tq0, tq1, breath(kq), [face('jC2', 'J02', glance=[[tq0, 0, 1.0], [at('J02') + .1, 0, 0]], seed=9)], title,
     frame=(1.35, 220, 470), cam=f'1,1.06,0,0,{tq0},{tq1}', past=True)

# ================================================================ 6. no airport: the map on the table
tm0, tm1 = at('N04') - .08, at('N04', .5)
gm = S5.g_map()
ui = (M.step(1, 'เกาะเต่าไม่มีสนามบิน', 'NO AIRPORT · BY BOAT ONLY', tm0 + .2, tm1 - .3)
      + M.arrow('M 168,452 C 228,404 300,388 344,404', tm0 + .9, tm1 - .2, '#c4463d', 5))
shot('map', tm0, tm1, gm, [], ui, cam=f'1.02,1.08,0,-20,{tm0},{tm1}', past=True)

# ================================================================ 7. the pier: boxes + uncle
A('sh_dead', 'jP3'); A('h_uncle', 'unA')
pier = S4.pier()
J_PIER = R.body(head='dead', tote=True, camera=True)
UNCLE_STATIC = ISL['UNCLE_BODY'] + '<use href="#h_uncle"/>'
tp0, tp1 = at('N04', .5), at('U01') - .1
pier_j = C.james_then('jp1', 'jP3', [(0, 'rest'), (tp1 + 1, 'rest'), (at('U01', .7), 'hip')], [(0, 'relax')], tote=True, camera=True)
uncle_seqR = [(0, 'relax'), (tp1 - .5, 'relax')] + RG.talk_seq([T['U01'][:2]], 'relax', 'explain', 'point_up', seed=5)[1:]
pier_un = C.uncle('un1', [(0, 'relax')], uncle_seqR, head='unA')
pier_svg = CS.pier2([(pier_un, 'translate(66,420) scale(.8)', (66, 804), None), (pier_j, 'translate(176,425) scale(1.0)', (176, 905), 'sun')])
labels = ''
for i, (txt, x, y, fr) in enumerate((('พัดลม', 300, 668, .64), ('หม้อหุงข้าว', 452, 470, .76), ('กระทะ', 436, 392, .88))):
    a = at('N04', fr)
    labels += M.pop(f'<g transform="translate({x},{y})"><rect x="{-12 - len(txt) * 6.5:.0f}" y="-15" width="{24 + len(txt) * 13:.0f}" height="30" rx="15" fill="#120e1c" fill-opacity=".86" stroke="#9a86ff"/>'
                    f'<text x="0" y="5" {M.TH} font-size="14" font-weight="800" fill="#f2eefa" text-anchor="middle">{txt}</text></g>', a, tp1 - .1, .45)
shot('pier', tp0, tp1, breath(pier_svg), [face('jP3', glance=[[tp0, 2.2, -1.2]], seed=10)], M.tag('วันย้ายบ้าน · ท่าเรือแม่หาด', tp0 + .2, tp1 - .1) + labels,
     cam=f'1,1.05,10,0,{tp0},{tp1}', past=True)
pier_u = pier_svg
shot('pier_uncle', tp1, at('G01') - .1, breath(pier_u), [face('unA', 'U01', seed=11), face('jP3', glance=[[tp1, -2.4, 0]], seed=10)],
     frame=(1.45, 120, 600), cam=f'1,1.04,0,0,{tp1},{at("G01")}', past=True)

# ================================================================ 8. the stairs: agent at the foot, James climbing
A('h_agent', 'agA'); A('sh_annoy', 'jP4'); A('sh_pant', 'jP5')
BOX = ('<g><path d="M -46,150 L 46,150 L 46,226 L -46,226 Z" fill="#c49a6c"/><path d="M -46,150 L 46,150 L 46,160 L -46,160 Z" fill="#a97f55"/>'
       '<rect x="-10" y="150" width="20" height="76" fill="#e6d2b0" opacity=".8"/>' f'<text x="-26" y="200" {M.TH} font-size="13" font-weight="800" fill="#6a4a2e">ครัว</text></g>')
ts0, ts1 = at('G01') - .1, at('J03') - .12
ag_seqR = [(0, 'relax'), (ts0 + .1, 'relax'), (at('G01', .1), 'point_up'), (at('G01', .55), (170, 10)), (at('G01', .8), 'point_up'), (ts1, 'point_up')]
ag = C.agent('ag1', [(0, 'rest')], ag_seqR, head='agA')
jb = C.james_then('jb1', 'jP4', [(0, 'carry')], [(0, 'carry')], tote=False, mid=BOX)
st1 = CS.stairs([(ag, 'translate(112,370) scale(1.3)', (112, 990), None), (jb, 'translate(372,400) scale(1.36)', (372, 1040), 'sun')])
shot('stairs_agent', ts0, ts1, breath(st1), [face('agA', 'G01', glance=[[ts0, 2.2, -1.6]], seed=12), face('jP4', glance=[[ts0, -2.4, -.6], [at('G01', .6), -1, -2.2]], seed=13)],
     M.tag('บ้านเช่า "ใกล้ท่าเรือ"', ts0 + .2, ts1 - .1), frame=(1.3, 200, 560), cam=f'1,1.04,0,0,{ts0},{ts1}', past=True)
tc0, tc1 = ts1, at('N05') - .08
jc = C.james_then('jb2', 'jP5', [(0, 'carry')] + [(tc0 + i * .5, (16, 100 + (6 if i % 2 else -4))) for i in range(10)], [(0, 'carry')], tote=False, mid=BOX)
st2 = CS.stairs([(jc, 'translate(330,236) scale(1.08)', (330, 760), 'sun')], sign=True)
shot('stairs_climb', tc0, tc1, breath(st2), [face('jP5', 'J03', glance=[[tc0, 0, -2.2]], seed=14)], frame=(1.7, 320, 400), cam=f'1,1.06,0,8,{tc0},{tc1}', past=True)

# ================================================================ 9. island seen from the ferry (21 km2)
ti0, ti1 = tc1, at('N06') - .08
iv_svg, iv_ui = CS.island_view(ti0, ti1)
shot('island', ti0, ti1, iv_svg, [], iv_ui, cam=f'1.0,1.07,0,10,{ti0},{ti1}', past=True)

# ================================================================ 10. first night: the gecko roommate
A('sh_dead', 'jP6')
bed = S5.bedroom()
J_BED = R.body(head='dead', tote=False, camera=False)
tb0, tb1 = ti1, at('N07') - .08
bed1 = put(bed, J_BED, C.james_then('jd1', 'jP6', [(0, 'rest')], [(0, 'relax'), (at('N06', .5), 'relax'), (at('N06', .7), 'chest'), (tb1, 'chest')], tote=False))
shot('gecko', tb0, tb1, breath(bed1), [face('jP6', glance=[[tb0, 0, 0], [at('N06', .35), 1.8, -2.4]], seed=15)],
     M.tag('คืนแรกในบ้านเช่า', tb0 + .2, tb1 - .1) + M.callout(260, 66, 150, ['รูมเมทคนแรก'], 226, 168, at('N06', .5), tb1 - .1, '#7a5ab8'),
     cam=f'1,1.06,0,-6,{tb0},{tb1}', past=True)

# ================================================================ 11. scooter lessons (+ auntie overtakes)
A('sh_annoy', 'jP7')
HELMET = ('<g transform="translate(48,268)"><path d="M -24,0 C -24,-26 24,-26 24,0 Z" fill="#f2eee6"/><path d="M -24,0 C -24,-26 0,-26 6,-25 C -8,-20 -14,-10 -16,0 Z" fill="#ffffff"/>'
          '<rect x="-26" y="-2" width="52" height="5" rx="2" fill="#2fb3b8"/><path d="M -14,3 C -10,14 10,14 14,3" stroke="#2c3a54" stroke-width="2.5" fill="none"/></g>')
tn0, tn1, tn2 = tb1, at('N07', .5), at('J04') - 1.3
st_now = S6.renamed(S6.street())
jn_seqR = [(0, 'hold'), (tn1 + .2, 'hold'), (at('N07', .72), (40, 70)), (at('N07', 1), 'hold')]
st_bkk = put(st_now, J_ISL_STATIC, C.james_then('js1', 'jP7', [(0, 'rest')], jn_seqR, holdR=HELMET, tote=False))
ui1 = M.callout(300, 420, 210, ['มอไซค์ = BTS', 'ของชาวเกาะ'], 450, 760, tn0 + .5, tn1 - .1, '#2a7f86')
shot('scooter_wide', tn0, tn1, breath(st_bkk), [face('jP7', glance=[[tn0, 2.4, 1.6]], seed=16)], M.tag('ปีแรก · หัดขี่มอไซค์', tn0 + .2, tn2 - .1) + ui1, cam=f'1,1.04,0,0,{tn0},{tn1}', past=True)
shot('scooter_close', tn1, tn2, breath(st_bkk), [face('jP7', glance=[[tn0, 2.4, 1.6], [tn1 + .4, 0, 2]], seed=16)],
     M.step(2, 'ใส่หมวกกันน็อกทุกครั้ง', 'HELMET ON, LEARN SLOWLY', tn1 + .3, tn2 - .1, 70), frame=(1.6, 240, 470), cam=f'1,1.05,0,0,{tn1},{tn2}', past=True)

A('sh_annoy', 'jP8')
tj0, tj1 = tn2, at('N08') - .08
pass0, pass1 = tj0 + .1, at('J04') - .05
SC, AS, Y = 5.9, .95, 790                      # scooter ~1.8 m against the auntie (same depth, behind James)
AX = 18
aunt_ride = C.aunt('au2', [(0, (-60, 10))], [(0, (82, 4))], head='h_aunt')
aunt_ride = re.sub(r'<path d="M -42,206 L 42,206 L 48,452 L -48,452 Z"[^>]*/>', '', aunt_ride)
lap = ('<path d="M -42,200 L 42,200 L 110,232 L 116,356 L 88,360 L 82,262 L -40,250 Z" fill="#2f6d72"/><path d="M -42,200 L -26,200 L -24,252 L -40,250 Z" fill="#3c8186"/>'
       '<path d="M 86,352 L 118,352 L 122,364 L 84,366 Z" fill="#e4ae86"/><rect x="82" y="364" width="44" height="6" rx="3" fill="#c4463d"/>')
legs_cut = '<clipPath id="auntTop"><rect x="-200" y="-200" width="400" height="406"/></clipPath>'
sy = Y - 34 * SC - 226 * AS
rider = (f'<g data-mv="{pass0:.2f},-640,0;{pass1:.2f},760,0" data-bob="1.2">'
         f'<g transform="translate({AX},{sy:.0f}) scale({AS})"><g clip-path="url(#auntTop)">{aunt_ride}</g>{lap}</g>'
         f'<g transform="translate(0,{Y}) scale({SC})">{K.scooter(0, -15, 1, "#e8735f")}</g>'
         f'<g transform="translate(205,{Y - 300})">{bag(0, 0, 1.0)}</g><g transform="translate(232,{Y - 292})">{bag(0, 0, .9)}</g></g>')
st_pass = put(st_now, J_ISL_STATIC, C.james_then('js2', 'jP8', [(0, 'rest')], [(0, 'hold'), (at('J04') + .2, 'hold'), (at('J04', .45), 'open'), (at('J04', 1) + .2, 'open')], holdR=HELMET, tote=False))
st_pass = st_pass.replace('<g id="L-char">', f'<g id="L-char"><defs>{legs_cut}</defs><g id="rider">{rider}</g>', 1)
shot('aunt_pass', tj0, tj1, breath(st_pass), [face('jP8', 'J04', glance=[[tj0, -2.6, 0], [pass0 + .5, 0, 0], [pass1 - .2, 2.6, 0], [at('J04') + .3, 2.6, -.4]], seed=17)],
     frame=(1.32, 250, 520), cam=f'1,1.04,0,0,{tj0},{tj1}', past=True)

# ================================================================ 12. parcels come by boat (retimed preview graphic) + calendar
def retime(svg, t0, k):
    def f(m):
        name, v = m.group(1), float(m.group(2))
        nv = t0 + v * k if name in ('at', 'out-at') else v * k
        return f'data-{name}="{nv:.2f}"'
    return re.sub(r'data-(at|out-at|dur|out-dur|stagger)="([-\d.]+)"', f, svg)


tq0, tq1 = tj1, at('N08', .5)
pc_svg, _ = MP.parcel()
pc_svg = retime(pc_svg, tq0 - .4, (tq1 - tq0 + .4) / 7.4)
pc_svg = pc_svg.replace('data-cam="1.02,1.06,0,6"', f'data-cam="1.02,1.06,0,6,{tq0},{tq1}"')
pc_svg = S6.renamed(pc_svg)
shot('parcel', tq0, tq1, pc_svg, [], M.step(3, 'พัสดุก็ต้องนั่งเรือ', 'PARCELS RIDE THE BOAT TOO', tq0 + .1, tq1 - .2, 852), cam=None, past=True)
tk0, tk1 = tq1, at('J05') - .1
cal = S5.g_calendar()
shot('calendar', tk0, tk1, cal, [], M.callout(40, 600, 200, ['คลื่นแรง', 'เรืองด = ของรอ'], 300, 520, tk0 + .3, tk1 - .1, '#3d6fb0'), cam=f'1,1.07,0,-10,{tk0},{tk1}', past=True)

# ================================================================ 13. the phone call
A('shead', 'jP9'); A('sh_dead', 'jP10')
bung = K.bungalow()
J_BUNG = R.body(head='dead', tote=False, camera=False)
rain = ('<g clip-path="url(#winclip)"><g class="om-rain">' + ''.join(f'<path d="M {300 + (i * 37) % 210},{120 + (i * 53) % 250} l -4,20" stroke="#cfe0ff" stroke-opacity=".5" stroke-width="1.4"/>' for i in range(70)) + '</g></g>'
        '<clipPath id="winclip"><rect x="300" y="120" width="210" height="250"/></clipPath>')
tc_0, tc_1 = tk1, at('S01') - .06
call1 = put(bung, J_BUNG, C.james_then('jh1', 'jP9', [(0, 'phone')], RG.talk_seq([T['J05'][:2]], 'relax', 'talk', 'open', seed=8), holdL=PHONE_L, tote=False))
call1 = call1.replace('<g id="L-light">', f'<g id="L-rain">{rain}</g><g id="L-light">', 1)
shot('call', tc_0, tc_1, breath(call1), [face('jP9', 'J05', glance=[[tc_0, -1.6, 2.2]], seed=18)], M.tag('ฝนตก · เรืองด', tc_0 + .1, tc_1 - .05),
     frame=(1.55, 190, 520), cam=f'1,1.04,0,0,{tc_0},{tc_1}', past=True)
tps0, tps1 = tc_1, at('J06') - .06
shot('phone', tps0, tps1, CS.phone_screen('S01', at('S01'), tps1), [], cam=f'1,1.05,0,0,{tps0},{tps1}', past=True)
call2 = put(bung, J_BUNG, C.james_then('jh2', 'jP10', [(0, 'phone')], [(0, 'relax')], holdL=PHONE_L, tote=False))
call2 = call2.replace('<g id="L-light">', f'<g id="L-rain">{rain}</g><g id="L-light">', 1)
tdd0, tdd1 = tps1, at('N09') - .08
shot('deadpan', tdd0, tdd1, breath(call2), [face('jP10', 'J06', seed=19)], frame=(1.9, 182, 490), cam=f'1,1.05,0,0,{tdd0},{tdd1}', past=True)

# ================================================================ 14. power cut: torch, gecko, the electrician
A('sh_dead', 'jP11'); A('h_elec', 'elA')
TORCH = ('<g><rect x="-56" y="236" width="16" height="34" rx="4" fill="#2c3040"/><rect x="-58" y="266" width="20" height="10" rx="2" fill="#3a3d48"/>'
         '<path d="M -58,276 L -38,276 L 40,520 L -150,520 Z" fill="#fff4d6" opacity=".18" style="mix-blend-mode:screen"/><circle cx="-48" cy="276" r="7" fill="#fff6dc"/></g>')
to0, to1 = tdd1, at('N10') - .08
el_in0, el_in1 = at('N09', .78), at('E01') - .05
elec = C.electrician('el1', [(0, 'relax')], [(0, 'relax'), (at('E01'), 'relax'), (at('E01') + .1, 'wave'), (at('E01', 1) + .1, 'wave2'), (to1, 'relax')], head='elA')
elec_g = (f'<g data-mv="{el_in0:.2f},260,0;{el_in1:.2f},0,0" data-bob="2">'
          f'<g transform="translate(440,420) scale(.86)">{elec}<g transform="translate(0,0)">{ISL["LAMP_GLOW"]}</g></g></g>')
out1 = put(bung, J_BUNG, C.james_then('jo1', 'jP11', [(0, 'chest')], [(0, 'relax')], holdL=TORCH, tote=False))
dark = '<rect width="540" height="960" fill="#0b0f1e" opacity=".42" style="mix-blend-mode:multiply"/>'
out1 = out1.replace('<g id="L-light">', f'<g id="L-dark">{dark}</g><g id="L-elec">{elec_g}</g><g id="L-light">', 1)
out1 = out1.replace(f'<g id="L-dark">', '<g id="L-dark">' + CS.CL.glow(440, 380, 160, '#fff4d6', .25, core=False), 1)
shot('outage', to0, to1, breath(out1), [face('jP11', glance=[[to0, 0, 0], [at('N09', .4), -2.2, -2.2], [el_in1, 2.4, 0]], seed=20), face('elA', 'E01', seed=21)],
     M.tag('พายุเข้า · ไฟดับ', to0 + .2, to1 - .1), cam=f'1.05,1.12,30,0,{to0},{to1}', past=True)

# ================================================================ 15. prices at the wooden shop
A('sh_annoy', 'jP12')
tsh0, tsh1 = to1, at('N11') - .08
shop2 = put(S4.shop(), J_BKK_SHOP, C.james_then('jm1', 'jP12', [(0, 'rest')], [(0, 'relax'), (at('N10', .3), 'reach'), (tsh1, 'reach')], tote=True))
shop2 = put(shop2, AUNT_STATIC, C.aunt('au3', [(0, 'relax')], [(0, 'relax')]))
ui = M.callout(34, 540, 220, ['ค่าเรือ', 'รวมอยู่ในราคา'], 120, 618, at('N10', .45), tsh1 - .1, '#c4463d')
shot('prices', tsh0, tsh1, breath(shop2), [face('jP12', glance=[[tsh0, -2.6, .6]], seed=22)], M.step(4, 'ของบนเกาะแพงกว่าฝั่ง', 'EVERYTHING ARRIVES BY BOAT', tsh0 + .1, tsh1 - .1) + ui,
     cam=f'1,1.05,10,-10,{tsh0},{tsh1}', past=True)

# ================================================================ 16. neighbours from all over the world
tw0, tw1 = tsh1, at('J07') - .1
shot('pinboard', tw0, tw1, CS.pinboard(tw0, tw1), [], M.step(5, 'เพื่อนบ้านมาจากทั่วโลก', 'KOH TAO: A DIVING TOWN', tw0 + .1, tw1 - .1, 40), cam=f'1,1.06,0,0,{tw0},{tw1}', past=True)

A('shead', 'jP13'); A('h_nb', 'nbA')
tn_0, tn_1 = tw1, at('F01') - .08
nb_seqR = [(0, 'rest'), (at('F01') - .1, 'rest'), (at('F01') + .05, 'wave'), (at('F01', 1) + .2, 'wave2'), (at('F01', 1) + .7, 'relax')]
nb = C.neighbour('nb1', [(0, 'rest')], nb_seqR, head='nbA')
nb_g = f'<g data-mv="{tn_0 - .6:.2f},-200,0;{tn_0 + .7:.2f},0,0" data-bob="2"><g transform="translate(70,350) scale(1.3)">{nb}</g></g>'
jw_seqR = [(0, 'relax'), (at('J07') - .1, 'relax'), (at('J07') + .15, 'wave'), (at('J07', .25), 'wave2'), (at('J07', .4), 'wave'), (at('J07', .55), 'talk'), (at('J07', .8), 'open'), (at('J07', 1) + .3, 'relax')]
st_nb = put(st_now, J_ISL_STATIC, C.james_then('jw1', 'jP13', [(0, 'rest')], jw_seqR, tote=False))
st_nb = st_nb.replace('<g id="L-light">', f'<g id="L-nb">{CS.char("NB", nb_g, "", (560, -40), (70, 900), "warm", None)[1]}</g><g id="L-light">', 1)
st_nb = st_nb.replace('<g id="L-light">', '<defs>' + CS.char("NB", '', '', (560, -40), (70, 900), "warm", None)[0] + '</defs><g id="L-light">', 1)
shot('hello', tn_0, tn_1, breath(st_nb), [face('jP13', 'J07', glance=[[tn_0, -2.6, 0]], seed=23), face('nbA', glance=[[tn_0, 2.4, 0]], seed=24)],
     frame=(1.35, 280, 520), cam=f'1,1.04,0,0,{tn_0},{tn_1}', past=True)
tf1 = at('F01', 1) + .2
shot('reply', tn_1, tf1, breath(st_nb), [face('nbA', 'F01', glance=[[tn_0, 2.4, 0]], seed=24), face('jP13', glance=[[tn_0, -2.6, 0]], seed=23)],
     frame=(1.6, 160, 500), cam=f'1,1.03,0,0,{tn_1},{tf1}', past=True)
tr1 = at('N12') - .08
shot('blink', tf1, tr1, breath(st_nb), [face('jP13', glance=[[tn_0, -2.6, 0]], seed=23, blinkAt=[tf1 + .25, tf1 + .58])],
     frame=(2.1, 236, 440), cam=f'1,1.08,0,0,{tf1},{tr1}', past=True)

# ================================================================ 17. montage: dive shop with Lae, instructor card
A('shead_t', 'jT2'); A('sh_grin_t', 'jT3')
J_DIVE = S4.sun_now('smirktalk')
dv = S4.dive()
CARD = ('<g transform="translate(48,262) rotate(-14) scale(1.5)"><rect x="-40" y="-26" width="80" height="52" rx="6" fill="#f8f4ea"/><rect x="-40" y="-26" width="80" height="16" rx="6" fill="#2a7f86"/>'
        f'<text x="0" y="-14" {M.EN} font-size="8" font-weight="800" fill="#fff" text-anchor="middle">DIVE INSTRUCTOR</text><circle cx="-22" cy="6" r="9" fill="#d29e78"/>'
        f'<text x="8" y="4" {M.EN} font-size="9" font-weight="800" fill="#1a1626" text-anchor="middle">JAMES</text><rect x="-4" y="10" width="30" height="3" fill="#8a8494"/></g>')
tm_0, tm_1, tm_2 = tr1, at('N12', .5), at('N13') - .36
dv1 = put(dv, J_DIVE, C.james_now('jv1', 'jT2', [(0, 'rest')], [(0, 'relax'), (at('N12', .2), 'point_out'), (tm_1, 'point_out')]))
shot('dive', tm_0, tm_1, breath(dv1), [face('jT2', glance=[[tm_0, -2.4, 0]], seed=25)], M.step(6, 'จากเชฟ สู่ครูสอนดำน้ำ', 'FROM THE KITCHEN TO THE REEF', tm_0 + .1, tm_2 - .1, 40),
     cam=f'1,1.05,0,0,{tm_0},{tm_1}', past=True)
dv2 = put(dv, J_DIVE, C.james_now('jv2', 'jT3', [(0, 'rest')], [(0, 'relax'), (tm_1 + .2, 'relax'), (tm_1 + .7, (12, 130)), (tm_2, (12, 130))], holdR=f'<g data-in="pop" data-at="{tm_1 + .6:.2f}" data-dur=".4">{CARD}</g>'))
shot('instructor', tm_1, tm_2, breath(dv2), [face('jT3', glance=[[tm_1, 0, 0]], seed=26)], frame=(1.3, 380, 520), cam=f'1,1.05,0,0,{tm_1},{tm_2}', past=True, zb=(tm_2 - .36, .36, 'out'))

# ================================================================ 18. back to now: the vista, rough sea, the question
A('shead_t', 'jT4'); A('sh_dead_t', 'jT5')
vista = S6.renamed(S6.vista_calm())
J_VISTA = S5.sun_island('smirk')
tv0, tv1 = tm_2, at('J08') - .1
vs = put(vista, J_VISTA, C.james_now('jx1', 'jT4', [(0, 'rest')], [(0, 'hip')]))
shot('vista', tv0, tv1, breath(vs), [face('jT4', seed=27)], M.tag('สองปีต่อมา · ปัจจุบัน', tv0 + .4, tv1 - .1), cam=f'1.0,1.08,0,-20,{tv0},{tv1}', zb=(tv0, .42, 'in'))
rough = S6.rough_sea()
J_ROUGH = S5.sun_island('dead')
trr0, trr1 = tv1, at('N14') - .1
rs = put(rough, J_ROUGH, C.james_now('jr1', 'jT5', [(0, 'rest')], RG.talk_seq([T['J08'][:2]], 'relax', 'hip', 'explain', seed=9)))
shot('rough', trr0, trr1, breath(rs), [face('jT5', 'J08', glance=[[trr0, -2.4, .8], [at('J08', .35), 0, 0], [at('J08', .8), -2.4, .8]], seed=28)],
     M.callout(40, 470, 190, ['คลื่นแรง', 'เรืองดวิ่ง'], 200, 690, at('J08', .5), trr1 - .1, '#3d6fb0'), frame=(1.35, 400, 560), cam=f'1,1.06,-20,-20,{trr0},{trr1}')
tz0, tz1 = trr1, at('N15') - .1
shot('vista_wide', tz0, tz1, breath(vs), [face('jT4', seed=27)], cam=f'1.12,1.0,0,10,{tz0},{tz1}')
tab0 = tz1
toggles, t = [], at('N15', 1) + .1
while t < TOTAL - .4:
    toggles.append((t, t + .82)); t += .9
shot('ab_card', tab0, TOTAL, CS.ab_card(tab0, TOTAL, toggles), [], cam=None, eye=False)


# ================================================================ pages
def wrap_graded(svg, s):
    g = M.group(svg, 'L-graded')
    inner = g
    if s['cam']:
        inner = inner.replace('<g id="L-graded"', f'<g id="L-graded" data-cam="{s["cam"]}"', 1)
    if s['past']:
        inner = f'<g filter="url(#pastGrade)">{inner}</g>'
    if s['frame']:
        z, cx, cy = s['frame']
        cx = min(max(cx, 270 / z), 540 - 270 / z)
        cy = min(max(cy, 480 / z), 960 - 480 / z)
        inner = f'<g transform="translate(270,480) scale({z}) translate({-cx},{-cy})">{inner}</g>'
    if s['zb']:
        z0, zd, d = s['zb']
        inner = f'<g data-zb="{z0},{zd},{d},zbBlur" filter="url(#zbF)">{inner}</g>'
    return svg.replace(g, inner, 1)


GLOBAL_DEFS = (S5.HAWAII + '<filter id="pastGrade" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="'
               '.78 .16 .06 0 .035  .10 .76 .10 0 .02  .08 .12 .66 0 .02  0 0 0 1 0"/></filter>'
               '<filter id="zbF" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur id="zbBlur" stdDeviation="0"/></filter>'
               '<pattern id="print" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.1" fill="#e9e1d0" opacity=".55"/><circle cx="9" cy="9" r="1.1" fill="#e9e1d0" opacity=".35"/></pattern>')


def page(s, idx):
    svg = wrap_graded(s['svg'], s)
    svg = set_ui(svg, ui_for(s['t0'], s['t1'], s['ui'], s['subs'], s['eye']))
    svg = svg.replace('<svg ', '<svg data-scene="0" width="540" height="960" ', 1)
    keys = {f['talk'][0][2] for f in s['faces'] if f['talk']} | set(re.findall(r'data-key="(\w+)"', svg))
    env = {k: ENV[k] for k in keys if k in ENV}
    conf = {'dur': TOTAL, 'faces': s['faces']}
    return (f'<!doctype html><meta charset="utf-8"><title>{s["name"]}</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700;800&family=Inter:wght@500;600;700;800&display=swap">'
            '<style>html,body{margin:0;background:#000}</style>'
            f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{GLOBAL_DEFS}{C.ALL_DEFS}{C.anim_defs()}</defs></svg>'
            f'<div style="width:540px;height:960px">{svg}</div>'
            f'<script>window.OM_ENV={json.dumps(env, separators=(",", ":"))};</script><script>{ENGINE}</script>'
            f'<script>window.addEventListener("load",()=>{{window.S=OM.mount(document.querySelector("svg[data-scene]"),{json.dumps(conf)});'
            f'document.fonts.ready.then(()=>{{window.READY=true;}});}});</script>')


def build():
    os.makedirs(OUT, exist_ok=True)
    meta = []
    SHOTS.sort(key=lambda s: s['t0'])
    for i, s in enumerate(SHOTS):
        fn = f'{i:02d}_{s["name"]}.html'
        open(os.path.join(OUT, fn), 'w').write(page(s, i))
        f0, f1 = round(s['t0'] * FPS), round(s['t1'] * FPS)
        meta.append({'file': fn, 't0': s['t0'], 't1': s['t1'], 'f0': f0, 'f1': f1})
    # sanity: shots tile the timeline
    for a, b in zip(meta, meta[1:]):
        assert a['f1'] == b['f0'], (a, b)
    json.dump({'fps': FPS, 'total': TOTAL, 'shots': meta}, open(os.path.join(OUT, 'shots.json'), 'w'), indent=1)
    print(len(meta), 'shots, frames', meta[-1]['f1'], 'total', TOTAL)


if __name__ == '__main__':
    build()
