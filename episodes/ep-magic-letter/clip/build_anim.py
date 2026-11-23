"""คลิปแบบมีการเคลื่อนไหว (ต่อจาก build_clip.py ที่สร้างเสียงและ timeline ไว้แล้ว)
1) สร้าง anim/anim.html: ช็อตทั้งหมดจาก storyboard.html + ข้อมูลเวลา + JS ขยับตัวละคร
   - กะพริบตาทุกตัว · ขยับปากเฉพาะคนที่พูดจริงตามความดังของเสียง (เสียงบรรยายไม่ขยับปาก)
   - หายใจ ตัวขยับเบา ๆ · เดินเข้าเฟรมแบบขาก้าวสลับ (ตัดตัวเป็นช่วงบน ขาซ้าย ขาขวา หมุนที่สะโพก)
   - กล้องซูมช้า ๆ · กล้องสั่นตอนไก่ขัน · ซิ่งล้มตอนไก่ขัน · หัวตุ๊กตุ๊กโยก · หมวกโยก · คนถูกดูดหมุนเข้าศาล
2) node render_anim.js เรนเดอร์ทีละเฟรม 24fps
3) ต่อเป็น out/clip_anim.mp4 พร้อมเสียง out/mix.wav และโลโก้ปิดท้าย"""
import json, re, os, subprocess, pathlib, wave
import numpy as np

HERE = pathlib.Path(__file__).parent; EP = HERE.parent
OUTRO = EP.parent.parent / "pipeline" / "v2" / "outro.mp4"
FPS, XF, SR = 24, 0.3, 48000
os.chdir(HERE)
os.makedirs("anim", exist_ok=True); os.makedirs("seg24", exist_ok=True)

TL = json.load(open("out/timeline.json"))
KEY = {"ซิ่ง": "sing", "อาม้า": "ama", "ลุงเปี๊ยก": "tukdriver", "ลุงโต": "giant", "ป้าแต๋ว": "vendor", "ต้น": "ton", "เดรโก": "draco", "หมวก": "hat"}

# ช็อตไหนเป็นเสียงบรรยาย (ซิ่ง VO) ดูจากคอลัมน์ผู้พูดใน script.md
vo_shots = {}
for line in (EP / "script.md").read_text().splitlines():
    if re.match(r"^\| \d+ \|", line):
        c = [x.strip() for x in line.strip("|").split("|")]
        vo_shots[int(c[0])] = "(VO)" in c[2]

def read_wav(path):
    with wave.open(str(path)) as w:
        sr, ch, raw = w.getframerate(), w.getnchannels(), w.readframes(w.getnframes())
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    return (x.reshape(-1, ch).mean(1) if ch > 1 else x), sr

shots = []
for sh in TL:
    n, d = sh["n"], sh["dur"]
    talk = []
    for i, (who, text, at, ln) in enumerate(sh["lines"]):
        if who == "ซิ่ง" and vo_shots.get(n) and i == 0:
            continue                                         # เสียงบรรยาย ไม่ขยับปาก
        el = HERE / "vo_fast" / f"s{n:02d}_{i}.wav"
        x, sr = read_wav(el if el.exists() else HERE / "vo" / f"s{n:02d}_{i}.wav")
        nz = np.where(np.abs(x) > (0.012 if el.exists() else 0.01))[0]; x = x[max(0, nz[0] - (800 if el.exists() else 0)):nz[-1] + 1] if len(nz) else x
        hop = sr // FPS; fr = []
        for k in range(0, len(x), hop):
            fr.append(float(np.sqrt(np.mean(x[k:k + hop] ** 2))))
        mx = max(fr) if fr else 1
        flags = [1 if v > mx * 0.28 else 0 for v in fr]
        for k in range(1, len(flags) - 1):                     # ไม่ให้ปากกระพริบถี่เกิน
            if flags[k - 1] == flags[k + 1] != flags[k]:
                flags[k] = flags[k - 1]
        talk.append(dict(key=KEY[who], start=int(at * FPS), flags=flags))
    shots.append(dict(n=n, dur=d, frames=int(round(d * FPS)), talk=talk))

# เวลาไก่ขัน (หลังประโยคแรกของช็อต 2)
s2 = TL[1]["lines"][0]; CROW = s2[2] + s2[3] + 0.05

# ท่าเดินเข้าเฟรม: ช็อต: [(href, ระยะเริ่ม (หน่วยในตัวละคร), วินาที)]
WALK = {4: [("#c_sing", 420, 1.0)], 11: [("#c_ton", -560, 1.1)], 12: [("#c_draco", -420, .9)]}

html = (EP / "storyboard.html").read_text()
head = html.split('<div class="wrap">')[0]
frames = re.findall(r'<div class="frame">(<svg viewBox="0 0 540 960".*?</svg>)</div>', html, re.S)
assert len(frames) == len(shots), (len(frames), len(shots))
page = head + '''<style>
html,body{margin:0;background:#000}
.shot{display:none;position:absolute;left:0;top:0;width:540px;height:960px}
.shot.on{display:block}
[data-ui]{display:none!important}
</style>''' + "".join(f'<svg class="shot" id="shot{i+1}"{f[4:]}' for i, f in enumerate(frames)) + f'''
<script>
const SHOTS = {json.dumps(shots)};
const CROW = {CROW:.3f};
const WALK = {json.dumps(WALK)};
const FPS = {FPS};
const KEYS = ["sing","ama","tukdriver","giant","vendor","ton","draco","hat","harry","ron","hermione","kidboy","kidgirl","strict","head","potion","rooster"];
const sel = c => document.querySelectorAll("." + c);
const show = (c, on) => sel(c).forEach(e => e.setAttribute("display", on ? "inline" : "none"));
const ease = p => p < 0 ? 0 : p > 1 ? 1 : (1 - Math.cos(Math.PI * p)) / 2;
const HIP = -250;
function prep(svg) {{
  if (svg.dataset.prep) return; svg.dataset.prep = 1;
  svg.querySelectorAll("use").forEach((u, i) => {{
    const h = u.getAttribute("href") || "";
    if (!h.startsWith("#c_")) return;
    u.dataset.orig = u.getAttribute("transform") || ""; u.dataset.ph = (i * 1.37) % 6.28;
  }});
  svg.querySelectorAll("[data-anim]").forEach(g => g.dataset.orig = g.getAttribute("transform"));
  const root = svg.querySelector("g[clip-path]"); root.dataset.orig = root.getAttribute("transform") || "";
}}
function legs(u, n) {{
  // สร้างชิ้นขาซ้าย/ขวาครั้งเดียว: ตัวบน (ตัดที่สะโพก) + ขาสองข้าง
  if (u.dataset.split) return [u, ...u.parentNode.querySelectorAll(`use[data-leg="${{u.dataset.uid}}"]`)];
  const id = "w" + n + Math.random().toString(36).slice(2, 7); u.dataset.uid = id; u.dataset.split = 1;
  const svg = u.ownerSVGElement, defs = svg.querySelector("defs");
  const mk = (nm, x, y, w, h) => {{ const c = document.createElementNS("http://www.w3.org/2000/svg", "clipPath"); c.id = id + nm;
    c.innerHTML = `<rect x="${{x}}" y="${{y}}" width="${{w}}" height="${{h}}"/>`; defs.appendChild(c); return `url(#${{id + nm}})`; }};
  u.setAttribute("clip-path", mk("u", -400, -900, 800, 900 + HIP + 4));
  const out = [u];
  for (const [nm, x] of [["l", -400], ["r", 0]]) {{
    const c = u.cloneNode(); c.removeAttribute("clip-path"); c.dataset.leg = id; c.dataset.side = nm;
    c.setAttribute("clip-path", mk(nm, x, HIP, 400, 400)); u.parentNode.insertBefore(c, u); out.push(c);
  }}
  return out;
}}
window.setShot = function (n, f) {{
  document.querySelectorAll(".shot").forEach(s => s.classList.toggle("on", s.id === "shot" + n));
  const svg = document.getElementById("shot" + n); prep(svg);
  const sh = SHOTS[n - 1], t = f / FPS, d = sh.dur;
  // กล้อง: ซูมช้า ๆ สลับเข้า/ออก + กล้องสั่นตอนไก่ขัน
  let z = n % 2 ? 1 + 0.05 * t / d : 1.05 - 0.05 * t / d, sx = 0, sy = 0;
  if (n === 2 && t > CROW && t < CROW + 0.5) {{ sx = 9 * Math.sin(t * 55); sy = 7 * Math.cos(t * 70); }}
  const root = svg.querySelector("g[clip-path]");
  root.setAttribute("transform", `translate(${{270 + sx}},${{480 + sy}}) scale(${{z}}) translate(-270,-480)`);
  // ตัวละคร: หายใจ + เดินเข้าเฟรม
  svg.querySelectorAll("use[data-orig]").forEach(u => {{
    if (u.dataset.leg) return;
    const h = u.getAttribute("href"), ph = +u.dataset.ph;
    let extra = ` scale(1,${{(1 + 0.007 * Math.sin(2 * Math.PI * t / 2.8 + ph)).toFixed(4)}})`;
    const w = (WALK[n] || []).find(x => x[0] === h);
    if (n === 8) extra = ` rotate(${{t * 420}},0,-260) scale(${{Math.max(0.2, 1 - 0.3 * t)}})`;
    if (h === "#c_hat") extra += ` rotate(${{3 * Math.sin(t * 5)}},0,0)`;
    if (w) {{
      const p = Math.min(1, t / w[2]), dx = w[1] * (1 - ease(p)), walking = p < 1;
      const parts = legs(u, n), sw = walking ? Math.sin(t * 2 * Math.PI * 2.2) : 0, bob = walking ? -Math.abs(Math.sin(t * 2 * Math.PI * 2.2)) * 8 : 0;
      parts.forEach(pu => {{
        let e = ` translate(${{dx.toFixed(1)}},${{bob.toFixed(1)}})` + extra;
        if (pu.dataset.side === "l") e += ` rotate(${{(14 * sw).toFixed(2)}},-15,${{HIP}})`;
        if (pu.dataset.side === "r") e += ` rotate(${{(-14 * sw).toFixed(2)}},15,${{HIP}})`;
        if (!pu.dataset.orig && pu !== u) pu.dataset.orig = u.dataset.orig;
        pu.setAttribute("transform", (u.dataset.orig + e).trim());
      }});
      return;
    }}
    u.setAttribute("transform", (u.dataset.orig + extra).trim());
  }});
  // กลุ่มท่าพิเศษ
  svg.querySelectorAll("[data-anim]").forEach(g => {{
    const a = g.dataset.anim;
    if (a === "tuk") {{
      const w = -14 + 3.5 * Math.sin(t * 2 * Math.PI * 1.6), b = 3 * Math.abs(Math.sin(t * 2 * Math.PI * 3.2));
      g.setAttribute("transform", `translate(300,${{620 - b}}) rotate(${{w}})`);
    }}
    if (a === "carry") {{
      const p = Math.min(1, t / +g.dataset.t), dx = +g.dataset.dx * (1 - ease(p));
      g.setAttribute("transform", `translate(${{dx.toFixed(1)}},0) ` + g.dataset.base);
    }}
    if (a === "rooster") {{
      const j0 = CROW + 0.4, J = 0.45; let x = 340, y = 374;
      if (t >= j0) {{ const q = Math.min(1, (t - j0) / J), p = ease(q); x = 340 + (232 - 340) * p; y = 374 + (676 - 374) * p - 130 * Math.sin(Math.PI * q);
        if (q >= 1) y -= 3 * Math.abs(Math.sin(t * 9)); }}
      else if (t > CROW) y -= 5 * Math.abs(Math.sin(t * 22));
      g.setAttribute("transform", `translate(${{x.toFixed(1)}},${{y.toFixed(1)}}) scale(.62)`);
    }}
    if (a === "fall") {{
      const p = ease((t - CROW) / 0.35), ang = -118 * p;
      g.setAttribute("transform", `translate(${{470 - 40 * p}},${{560 + 40 * (1 - p)}}) rotate(${{ang}}) scale(.72)`);
    }}
  }});
  // กะพริบตา (ทุก ~3 วินาที คนละจังหวะ)
  KEYS.forEach((k, i) => show("an-blink-" + k, ((t + i * 0.73) % 3.1) < 0.12));
  // ขยับปากตามเสียง
  KEYS.forEach(k => show("an-mouth-" + k, false));
  sh.talk.forEach(x => {{ const i = f - x.start; if (i >= 0 && i < x.flags.length && x.flags[i]) show("an-mouth-" + x.key, true); }});
  if (n === 2 && ((t > CROW && t < CROW + 0.4) || (t > CROW + 0.9 && t < CROW + 1.5))) show("an-mouth-rooster", Math.floor(t * 8) % 2 === 0);
}};
window.FRAMES = SHOTS.map(s => s.frames);
</script>'''
(HERE / "anim" / "anim.html").write_text(page)
print("anim page ok", [s["frames"] for s in shots], sum(s["frames"] for s in shots))
