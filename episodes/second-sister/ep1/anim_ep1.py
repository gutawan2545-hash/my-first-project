#!/usr/bin/env python3
"""EP1 full-episode animation (subtitle version, no voice yet).

Builds anim_ep1.html + ep1_timeline.json from the approved storyboard:
  * every shot of script.md gets a time slot (length from its line, ~14 Thai chars / s)
  * each shot is shown on the most specific storyboard panel that covers it (stage + framing + camera move)
  * characters breathe, blink and (when their line is on screen) move their lips  -> SMIL inside the pose defs
  * candles flicker, haze drifts, dust floats, camera moves per panel
  * shots 17-19 reuse the hand-animated Rosa clip (rosa_tears.mp4)
Render: node anim_render_ep1.js (4 parallel workers)  ->  segments/ ; then bash assemble_ep1.sh
"""
import os, re, io, json, random, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
NS = {"__file__": os.path.join(HERE, "storyboard.py"), "__name__": "sb"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "storyboard.py")).read(), NS)
PANELS, ROWS, TITLES, CHIPS = NS["PANELS"], NS["ROWS"], NS["TITLES"], NS["CHIPS"]
ST, INS, INS_EXACT, DEFS, V2 = NS["ST"], NS["INS"], NS["INS_EXACT"], NS["DEFS"], NS["v2"]
R = random.Random(42)

# ---------------- 1. living poses: breathing, blinking, talking ----------------
SKIN = {"mek": "#eec4a2", "daeng": "#e3b088", "cat": "#f1d3bd", "luc": "#efd6c6", "rosa": "#f5d3b4", "jos": "#ebc6a6", "thana": "#d9a37c",
        "mariam": "#f6dcc4", "agnes": "#efe2da", "james": "#fbe7d8", "mkid": "#efc6a3", "jan": "#f2cdab", "twinM": "#f6dcc4", "twinA": "#f6dcc4"}
KIDS = {"mkid", "jan", "twinM", "twinA"}
POSE_CID = {}

def face_fx(cid, talk):
    if cid not in SKIN: return ""
    tr = "" if cid in KIDS else ' transform="translate(0,9) scale(.82)"'
    ey = 3 if cid in KIDS else -0.5
    per, off = R.uniform(3.6, 5.2), R.uniform(0, 4)
    kt = 'keyTimes="0;.9;.935;.965;1"'
    o = f'<g{tr}>'
    for x in (-13, 13):   # eyelids close briefly: skin ellipse grows over the eye, lash line appears
        o += (f'<ellipse cx="{x}" cy="{ey}" rx="10.5" ry="0" fill="{SKIN[cid]}"><animate attributeName="ry" values="0;0;6.8;0;0" {kt} dur="{per:.2f}s" begin="-{off:.2f}s" repeatCount="indefinite"/></ellipse>'
              f'<path d="M {x - 10},{ey} Q {x},{ey + 4} {x + 10},{ey}" stroke="#1b1316" stroke-width="1.6" fill="none" opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" {kt} dur="{per:.2f}s" begin="-{off:.2f}s" repeatCount="indefinite"/></path>')
    if talk:              # lips part and close in an irregular rhythm
        o += (f'<ellipse cx="0" cy="24.6" rx="3.4" ry=".4" fill="#5a2a2e"><animate attributeName="ry" values=".4;2.6;.8;3;.5;2;1.2;2.8;.4" dur="1.1s" repeatCount="indefinite"/>'
              f'<animate attributeName="rx" values="3.4;4.2;3.6;4.4;3.4" dur=".8s" repeatCount="indefinite"/></ellipse>')
    return o + '</g>'

def living(pose_str, talk=False):
    m = re.match(r'<g id="(sb_[a-zA-Z0-9_]+)">', pose_str)
    name = m.group(1)
    cm = re.search(r'id="([a-zA-Z_]+)-legL"', pose_str)
    cid = cm.group(1) if cm else ""
    POSE_CID[name] = cid
    new_id = name + ("_talk" if talk else "")
    body = pose_str[m.end():pose_str.rstrip().rfind("</g>")]
    breath = f'<animateTransform attributeName="transform" type="translate" values="0,0;0,-1.3;0,0" dur="{R.uniform(3.4, 4.2):.2f}s" begin="-{R.uniform(0, 4):.2f}s" repeatCount="indefinite"/>'
    fx = "" if cid == "mek_back" else face_fx(cid, talk)
    return f'<g id="{new_id}"><g>{breath}{body}{fx}</g></g>'

for ps in V2.POSES:
    if not ps.startswith('<g id="sb_'): continue
    DEFS = DEFS.replace(ps, living(ps) + living(ps, talk=True), 1)

# ---------------- 2. environment motion in the stages ----------------
def flicker(m):
    tag, op = m.group(1), float(m.group(3) or 1)
    return f'{tag}><animate attributeName="opacity" values="{op:.2f};{op * .78:.2f};{op:.2f};{op * .9:.2f};{op:.2f}" dur="{R.uniform(.6, 1.4):.2f}s" repeatCount="indefinite"/></circle>'
DEFS = re.sub(r'(<circle [^>]*fill="url\(#lg_(ffe6c4|fff0dc)\)"[^>]*?opacity="([\d.]+)"[^>]*?)/>', flicker, DEFS)
def drift(m):
    return f'<rect {m.group(1)}><animateTransform attributeName="transform" type="translate" values="0,0;{R.uniform(12, 26):.0f},0;0,0" dur="{R.uniform(12, 20):.1f}s" repeatCount="indefinite"/></rect>'
DEFS = re.sub(r'<rect ([^>]*filter="url\(#lhaze\)"[^>]*?)/>', drift, DEFS)

COOL_LIGHT = {"#fff0dc": "#f2e8f8", "#ffe6c4": "#f6e0e6", "#fff4e0": "#eee9fb", "#fff4dc": "#f1ebfa", "#f4dca0": "#ecd8ea",
              "#ffe9b0": "#efdcec", "#ffd27a": "#e9cfe6", "#fff1c8": "#f1e6f6", "#ffe8a8": "#eedaea"}
def cool(svg):
    for a, b in COOL_LIGHT.items(): svg = svg.replace(a, b).replace(a.upper(), b)
    return svg
DEFS = cool(DEFS)
INS = {k: cool(v) for k, v in INS.items()}
LIGHTS = NS["LIGHTS"]
INS_DEFS = "".join(f'<g id="ins_{k}">{v}</g>' for k, v in INS.items())
EXACT_DEFS = "".join(f'<g id="exact_{k}">{v}</g>' for k, v in INS_EXACT.items())
# the approved frame stays pixel-identical; only its baked subtitle text is switched off so each shot shows its own line
EXACT_DEFS = EXACT_DEFS.replace('<g id="v1_subs"', '<g id="v1_subs" display="none"')
_o = EXACT_DEFS.find("OVERLAY: time chip"); _e = EXACT_DEFS.find('<g id="v1_subs"', _o)
if _o > 0: EXACT_DEFS = EXACT_DEFS[:_o] + "-->" + EXACT_DEFS[_o:_e].replace("-->", "", 1).replace("<g", '<g display="none"', 1).replace('<g transform="translate(500,44)"', '<g display="none" transform="translate(500,44)"') + EXACT_DEFS[_e:]

# ---------------- 3. timeline ----------------
SPEAKERS = {"โรซา": "rosa", "เมฆ": "mek", "เจมส์": "james", "ป้าแดง": "daeng", "คาทารีนา": "cat", "มาเรียม": "mariam", "อักเนส": "agnes", "ลูเซีย": "luc", "ยอแซฟ": "jos", "ธนา": "thana", "โรซา ": "rosa"}
COMBINING = re.compile(r"[ัิ-ฺ็-๎]")
def vis_len(s): return len(COMBINING.sub("", s))
def wrap_th(text, limit=24):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        if not w: continue
        cand = (cur + " " + w).strip()
        if vis_len(cand) > limit and cur:
            lines.append(cur); cur = w
        else:
            cur = cand
    if cur: lines.append(cur)
    return lines

# words that get the purple highlight (at most two per card, longest match first)
EMPH = ["มาร์ธา", "มาเรียม", "อักเนส", "โรซา", "ป้าแดง", "จันทร์เจ้า", "ลูเซีย", "คาทารีนา", "ยอแซฟ", "ธนา", "เจมส์", "นภา",
        "หอระฆัง", "ระฆัง", "ตีสาม", "ฝาแฝด", "แฝด", "กองเพลิง", "ไฟไหม้", "ศพ", "ห้าม", "กฎ", "ปีกเก่า", "หลุมศพ", "หลุม",
        "มือซ้าย", "ถนัดซ้าย", "ยี่สิบปี", "20 ปี", "สิบปี", "ลูกนกน้อย", "ผ้าเช็ดหน้า", "ตุ๊กตา", "เซนต์เวโรนิกา", "ผี", "เลือด", "หายไป"]
def emph_line(line, budget):
    spans, i = [], 0
    while i < len(line):
        hit = None
        if budget[0] > 0:
            for w in sorted(EMPH, key=len, reverse=True):
                if line.startswith(w, i): hit = w; break
        if hit:
            spans.append([hit, 1]); i += len(hit); budget[0] -= 1
        else:
            if spans and spans[-1][1] == 0: spans[-1][0] += line[i]
            else: spans.append([line[i], 0])
            i += 1
    return spans
def make_cards(text, dur):
    if not text: return []
    lines = wrap_th(text, 22)
    groups, k = [], 0
    while k < len(lines):
        left = len(lines) - k
        take = left if left <= 3 else 2      # 4 lines -> 2+2, 5 -> 2+3 ...
        groups.append(lines[k:k + take]); k += take
    total = sum(vis_len("".join(g)) for g in groups)
    cards, t = [], 0.0
    for g in groups:
        d = dur * vis_len("".join(g)) / total
        budget = [2]
        cards.append({"t0": round(t, 2), "dur": round(d, 2), "lines": [emph_line(L, budget) for L in g]})
        t += d
    return cards

def parse_audio(a):
    sfx = " ".join(re.findall(r"(?<!\*)\*([^*]+)\*(?!\*)", a))
    m = re.match(r"\s*\*\*([^*]+):\*\*\s*(.*)", a)
    speaker, text = None, ""
    if m:
        who, text = m.group(1).strip(), m.group(2)
        base = re.sub(r"\s*\(.*?\)", "", who).strip()
        speaker = SPEAKERS.get(base) if base != "เล่า" else None
        if base.startswith("เสียงเด็ก") or base.startswith("เด็ก"): speaker = None
    text = re.sub(r"\([^)]*\)", "", text).replace("**", "").strip()
    text = re.sub(r"\s+", " ", text)
    return speaker, text, sfx

def shot_dur(text, sfx):
    c = vis_len(re.sub(r"\s", "", text))
    return max(2.0, c / 13.5 + 1.0) if c else (2.6 if sfx else 2.2)

# most specific panel for each shot
cover = {}
for sc, panels in PANELS.items():
    for idx, p in enumerate(panels):
        a, _, b = p[0].partition("-"); a = int(a); b = int(b or a)
        for n in range(a, b + 1):
            if n in cover and (cover[n][2] <= b - a): continue
            cover[n] = (sc, idx, b - a)

segments, T = [], 0.0
silence_left = 0
RED_SHOTS = {238, 247, 251, 253, 284}       # the big scares: subtitle turns red
STINGER_SHOTS = {237, 247, 284}             # sharp scare hit in the sound
ROSA_SHOTS = (17, 18, 19)
n = 1
while n <= 287:
    sc, idx, _ = cover[n]
    if n in ROSA_SHOTS:
        segments.append({"type": "video", "file": "rosa_tears.mp4", "t0": T, "dur": 17.0, "scene": sc, "shots": list(ROSA_SHOTS), "bells": []})
        T += 17.0; n = 20; continue
    rng, stage, crop, size, mv, desc = PANELS[sc][idx]
    seg = {"type": "html", "scene": sc, "stage": stage, "crop": list(crop) if crop else None, "move": mv,
           "kind": "exact" if stage in INS_EXACT else ("ins" if stage in INS else "stage"),
           "chip": CHIPS.get(sc, ""), "t0": T, "shots": [], "bells": [], "lights": LIGHTS.get(stage, [])}
    while n <= 287 and cover.get(n) == (sc, idx, cover[n][2]) and n not in ROSA_SHOTS:
        _, vis, aud = ROWS[n]
        speaker, text, sfx = parse_audio(aud)
        d = shot_dur(text, sfx)
        if "ระฆัง" in sfx or "ตั๊ง" in sfx:
            cnt = 6 if "หกครั้ง" in sfx else (1 if ("หนึ่งครั้ง" in sfx or "ตั๊ง" in sfx) else 3)
            vol = 1.35 if "สนั่น" in sfx else (.55 if ("เบาลง" in vis or "ไกล" in sfx) else 1.0)
            seg["bells"].append([round(T - seg["t0"], 2), cnt, vol])
        if n in STINGER_SHOTS: seg.setdefault("stingers", []).append(round(T - seg["t0"], 2))
        if "เงียบสนิท" in aud or "ดนตรีตัด" in sfx: silence_left = 3 if "ดนตรีตัด" in sfx else 1
        if silence_left > 0: seg.setdefault("hush", []).append([round(T - seg["t0"], 2), round(d, 2)]); silence_left -= 1
        seg["shots"].append({"n": n, "t0": round(T - seg["t0"], 2), "dur": round(d, 2), "speaker": speaker, "cards": make_cards(text, d), "red": n in RED_SHOTS})
        T += d; n += 1
    seg["dur"] = round(T - seg["t0"], 2)
    segments.append(seg)

OUTRO = 2.6
timeline = {"fps": 24, "total": round(T, 2), "outro": OUTRO, "segments": segments}
json.dump(timeline, open(os.path.join(HERE, "ep1_timeline.json"), "w"), ensure_ascii=False, indent=1)

# ---------------- 4. player page ----------------
JS = r'''
const TL = %TL%, POSE_CID = %PC%;
const $ = id => document.getElementById(id);
const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
const stage = $('stage'); stage.pauseAnimations();
let curSeg = -1, curShot = -1, curCard = -2, curStageKey = null;
const SUB_Y = 770;
const NS = 'http://www.w3.org/2000/svg';
const MR = (i, k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
const motes = [...Array(12)].map((_, i) => ({ x: MR(i, 1) * 540, y: MR(i, 2) * 960, vy: 3 + MR(i, 3) * 5, vx: (MR(i, 4) - .5) * 3, r: .6 + MR(i, 5) * 1.1, far: MR(i, 6) < .35, ph: MR(i, 7) * 6.28 }));
motes.forEach((m, i) => {
  const g = document.createElementNS(NS, 'g'); g.setAttribute('id', 'mote' + i);
  const halo = document.createElementNS(NS, 'circle'); halo.setAttribute('r', m.r * 4.5); halo.setAttribute('fill', '#f3eeff'); halo.setAttribute('filter', 'url(#moteHalo)'); halo.setAttribute('class', 'h');
  const dot = document.createElementNS(NS, 'circle'); dot.setAttribute('r', m.far ? m.r * 1.6 : m.r); dot.setAttribute('fill', '#f7f4ff'); if (m.far) dot.setAttribute('filter', 'url(#moteBlur2)');
  g.appendChild(halo); g.appendChild(dot); $('motes').appendChild(g);
});
document.querySelectorAll('.lmotes').forEach(e => e.setAttribute('display', 'none'));
function setTalk(seg, shot) {
  const g = seg.kind === 'stage' ? $('st_' + seg.stage) : null; if (!g) return;
  g.querySelectorAll('use').forEach(u => {
    const h = (u.getAttribute('href') || '').slice(1); if (!h.startsWith('sb_')) return;
    const base = h.replace(/_talk$/, ''), cid = POSE_CID[base];
    const want = (shot.speaker && cid === shot.speaker) ? base + '_talk' : base;
    if (want !== h) u.setAttribute('href', '#' + want);
  });
}
window.render = function (si, t) {          // segment index, seconds into the segment
  const seg = TL.segments[si];
  if (si !== curSeg) {
    curSeg = si; curShot = -1; curCard = -2;
    const src = seg.kind === 'stage' ? '#st_' + seg.stage : seg.kind === 'ins' ? '#ins_' + seg.stage : '#exact_' + seg.stage;
    $('viewUse').setAttribute('href', src);
    const [cx, cy, h] = seg.crop || [270, 480, 960], w = h * 9 / 16;
    $('view').setAttribute('viewBox', `${cx - w / 2} ${cy - h / 2} ${w} ${h}`);
    $('viewWrap').style.filter = seg.kind === 'exact' ? 'none' : 'saturate(1.12) brightness(1.05) contrast(1.05)';
    $('grade').style.display = seg.kind === 'exact' ? 'none' : ''; $('grain').style.display = seg.kind === 'exact' ? 'none' : '';
    $('chipText').textContent = seg.chip; $('chip').style.display = seg.chip ? '' : 'none';
    if (seg.chip) $('chipBox').setAttribute('width', 14 + seg.chip.length * 7.4);
  }
  const si2 = seg.shots.findIndex(s => t >= s.t0 && t < s.t0 + s.dur);
  const shotIdx = si2 < 0 ? seg.shots.length - 1 : si2, shot = seg.shots[shotIdx];
  if (shotIdx !== curShot) { curShot = shotIdx; curCard = -2; setTalk(seg, shot); }
  const lt = t - shot.t0;
  let ci = shot.cards.findIndex(c => lt >= c.t0 && lt < c.t0 + c.dur); if (ci < 0 && shot.cards.length) ci = shot.cards.length - 1;
  if (ci !== curCard) {
    curCard = ci;
    const sub = $('sub'); sub.innerHTML = '';
    if (ci >= 0) {
      const lines = shot.cards[ci].lines, n = lines.length, LH = 30;
      let y = SUB_Y - ((n - 1) * LH) / 2 + 8;
      for (const L of lines) {
        const tx = document.createElementNS(NS, 'text'); tx.setAttribute('x', 270); tx.setAttribute('y', y);
        for (const [str, em] of L) { const sp = document.createElementNS(NS, 'tspan'); sp.textContent = str; if (em && !shot.red) sp.setAttribute('class', 'em'); tx.appendChild(sp); }
        if (shot.red) tx.setAttribute('class', 'red');
        sub.appendChild(tx); y += LH;
      }
    }
  }
  const card = shot.cards[ci];
  let a = 0;
  if (card) { const ct = lt - card.t0; a = Math.min(1, ct / .15, (card.dur - ct) / .15); }
  $('sub').setAttribute('opacity', Math.max(0, a).toFixed(3));
  // camera
  const p = Math.min(1, t / Math.max(seg.dur, .1)), e = ease(p);
  let s = 1 + .02 * e, tx = 0, ty = 0;
  if (seg.move === 'in') s = 1 + .08 * e;
  else if (seg.move === 'out') s = 1.08 - .08 * e;
  else if (seg.move === 'pan-l') { s = 1.08; tx = 22 - 44 * e; }
  else if (seg.move === 'pan-r') { s = 1.08; tx = -22 + 44 * e; }
  else if (seg.move === 'tilt-u') { s = 1.08; ty = -34 + 68 * e; }
  else if (seg.move === 'tilt-d') { s = 1.08; ty = 34 - 68 * e; }
  else if (seg.move === 'shake') { s = 1.04; const k = Math.max(0, 1 - t / .8); tx = Math.sin(t * 61) * 5 * k; ty = Math.cos(t * 47) * 4 * k; }
  $('cam').setAttribute('transform', `translate(${270 + tx},${480 + ty}) scale(${s.toFixed(4)}) translate(-270,-480)`);
  // dust
  const gt = seg.t0 + t;
  const [vcx, vcy, vh] = seg.crop || [270, 480, 960], vk = 960 / vh, vx0 = vcx - vh * 9 / 32, vy0 = vcy - vh / 2;
  const L = (seg.lights || []).map(([x, y, r]) => [(x - vx0) * vk, (y - vy0) * vk, r * vk]);
  motes.forEach((m, i) => {
    const x = (((m.x + gt * m.vx + Math.sin(gt * .23 + m.ph) * 14) % 540) + 540) % 540;
    const y = (((m.y - gt * m.vy + Math.sin(gt * .31 + m.ph) * 8) % 960) + 960) % 960;
    let lit = 0; for (const [lx, ly, lr] of L) { const d2 = ((x - lx) ** 2 + (y - ly) ** 2) / (lr * lr); lit = Math.max(lit, Math.exp(-d2 * 1.6)); }
    const tw = .75 + .25 * Math.sin(gt * 1.7 + m.ph * 3);
    const g = $('mote' + i); g.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)})`);
    g.firstChild.setAttribute('opacity', (lit * .55 * tw).toFixed(3));
    g.lastChild.setAttribute('opacity', ((m.far ? .12 : .16) + lit * (m.far ? .35 : .75) * tw).toFixed(3));
  });
  $('motes').style.display = (seg.kind === 'stage' && L.length) ? '' : 'none';
  $('grainT').setAttribute('seed', Math.floor(gt * 24) % 997);
  // dip to black at scene changes
  const prev = TL.segments[si - 1], next = TL.segments[si + 1];
  let fade = 0;
  if (prev && prev.scene !== seg.scene) fade = Math.max(fade, 1 - t / .35);
  if (next && next.scene !== seg.scene) fade = Math.max(fade, 1 - (seg.dur - t) / .35);
  $('fade').setAttribute('opacity', Math.max(0, Math.min(1, fade)).toFixed(3));
  stage.setCurrentTime(gt);
};
window.TL = TL;
'''
JS = JS.replace("%TL%", json.dumps(timeline, ensure_ascii=False)).replace("%PC%", json.dumps(POSE_CID))

DEFS_INNER = DEFS.replace('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>', "").replace("</defs></svg>", "")
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>EP1</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&family=Noto+Serif+Thai:wght@500;700&family=Dancing+Script:wght@600;700&family=Inter:wght@500&display=swap">
<style>html,body{{margin:0;background:#000}} svg{{display:block}} #sub text{{font-family:"IBM Plex Sans Thai",sans-serif;font-size:22px;font-weight:700;fill:#ffffff;text-anchor:middle}} #sub .em{{fill:#c27bff}} #sub .red{{fill:#ff3b3b}}</style></head><body>
<svg id="stage" width="540" height="960" viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg">
<defs>{DEFS_INNER}{INS_DEFS}{EXACT_DEFS}
<filter id="subStroke2" x="-10%" y="-30%" width="120%" height="160%"><feMorphology in="SourceAlpha" operator="dilate" radius="2.6" result="d"/><feFlood flood-color="#120e18"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="moteBlur2" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation=".9"/></filter>
<filter id="moteHalo" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.4"/></filter>
<filter id="grainF" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB"><feTurbulence id="grainT" type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="1" result="n"/><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  2.2 0 0 0 -0.9"/></filter>
</defs>
<rect width="540" height="960" fill="#0a080c"/>
<g id="cam"><g id="viewWrap"><svg id="view" x="0" y="0" width="540" height="960" viewBox="0 0 540 960" preserveAspectRatio="xMidYMid slice"><use id="viewUse" href="#st_tower_fog"/></svg></g></g>
<g id="grade"><rect width="540" height="960" fill="#e2dcfa" opacity=".42" style="mix-blend-mode:multiply"/><rect width="540" height="960" fill="#6c64b0" opacity=".14" style="mix-blend-mode:soft-light"/><rect width="540" height="960" fill="url(#pvig)"/></g>
<g id="grain" pointer-events="none"><rect width="540" height="960" filter="url(#grainF)" opacity=".2" style="mix-blend-mode:screen"/><rect width="540" height="960" filter="url(#grainF)" opacity=".12" style="mix-blend-mode:overlay"/></g>
<g id="motes"></g>
<g id="chip"><rect id="chipBox" x="24" y="28" width="134" height="30" rx="15" fill="#15121c" fill-opacity=".85" stroke="#8f74d8" stroke-width="1.4"/><text id="chipText" x="36" y="48" font-family="IBM Plex Sans Thai, sans-serif" font-size="14" font-weight="500" fill="#e6e0f4"></text></g>
<g id="wm" transform="translate(500,44)" opacity=".8"><path d="M -14,0 C -8,-8 8,-8 14,0 C 8,8 -8,8 -14,0 Z" fill="none" stroke="#b18cff" stroke-width="1.6"/><circle r="3.6" fill="#b18cff"/></g>
<g id="sub" filter="url(#subStroke2)"></g>
<rect id="fade" width="540" height="960" fill="#000" opacity="0"/>
</svg>
<script>{JS}</script></body></html>'''
open(os.path.join(HERE, "anim_ep1.html"), "w").write(html)
print(f"wrote anim_ep1.html {len(html) // 1024} KB · {len(segments)} segments · {T / 60:.1f} min + outro")
