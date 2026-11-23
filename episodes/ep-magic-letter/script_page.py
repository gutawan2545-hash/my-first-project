# สร้าง script.html จาก script.md (อ่านบทแบบบทภาพยนตร์ ดูง่ายบนมือถือ)
import re, html, pathlib
here = pathlib.Path(__file__).parent
md = (here / "script.md").read_text()
rows = []
for line in md.splitlines():
    if re.match(r"^\| \d+ \|", line):
        c = [x.strip() for x in line.strip("|").split("|")]
        rows.append(dict(n=c[0], sec=c[1], who=c[2], th=c[3], en=c[4], cam=c[5]))
notes = [l[2:] for l in md.split("หมายเหตุ", 1)[1].splitlines() if l.startswith("- ")]
COL = {"เจม": "#9fb4ff", "ตะวัน": "#f2a7b8", "ต้น": "#8fd19e", "เดรโก": "#c4c8d4", "หมวก": "#e0c27a"}
def col(w):
    for k, v in COL.items():
        if w.startswith(k): return v
    return "#d4d6e0"
t = 0.0; shots = ""
for r in rows:
    start = t; t += float(r["sec"])
    vo = "(VO)" in r["who"]
    th = html.escape(r["th"]).replace(" · ", "<br>")
    shots += f'''<article class="shot">
  <div class="meta"><span class="num">{r["n"]}</span><span class="tc">{int(start//60)}:{start%60:04.1f} – {int(t//60)}:{t%60:04.1f}</span></div>
  <p class="cam">{html.escape(r["cam"])}</p>
  <p class="who" style="color:{col(r["who"])}">{html.escape(r["who"].replace(" (VO)", ""))}{' <em>เสียงบรรยาย</em>' if vo else ''}</p>
  <p class="th">{th}</p>
  <p class="en">{html.escape(r["en"])}</p>
</article>'''
title = md.splitlines()[0].lstrip("# ").split(" (")[0]
page = f'''<title>บท ฮอกวอตส์สาขาไทย</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=Inter:wght@400;500&display=swap">
<style>
/* Layout: บทเรียงช็อตแบบบทภาพยนตร์ คอลัมน์เดียว อ่านบนมือถือ · โทนมืดของช่อง */
:root {{ --bg:#0d0f14; --panel:#1b1f2b; --ink:#e6e7ee; --muted:#80849a; --line:#2a2e3a; --sub:#ffd84a; --accent:#c9a8ff;
  --th:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; --en:Inter,system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--bg); color:var(--ink); }}
body {{ font-family:var(--th); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:28px 48px; }}
.wrap {{ max-width:680px; margin:0 auto; display:grid; gap:14px; }}
h1 {{ font-size:22px; line-height:1.4; margin:0; text-wrap:balance; }}
.sub {{ color:var(--muted); font-size:14px; margin:0 0 8px; }}
.shot {{ background:var(--panel); border-radius:8px; padding:14px 16px; display:grid; gap:6px; }}
.meta {{ display:flex; gap:10px; align-items:center; font-size:12px; color:var(--muted); font-variant-numeric:tabular-nums; }}
.num {{ background:#2a2440; color:var(--accent); border:1px solid #4a3f72; border-radius:99px; padding:1px 9px; font-weight:600; }}
.cam {{ margin:0; font-size:13px; color:var(--muted); line-height:1.6; }}
.who {{ margin:4px 0 0; font-weight:600; font-size:14px; letter-spacing:.02em; }}
.who em {{ font-style:normal; font-weight:400; color:var(--muted); font-size:12px; margin-left:6px; }}
.th {{ margin:0; font-size:19px; font-weight:700; line-height:1.55; color:var(--sub); }}
.en {{ margin:0; font-family:var(--en); font-size:13px; color:#cfd2dc; line-height:1.5; }}
.notes {{ font-size:13px; color:var(--muted); line-height:1.7; padding-left:18px; margin:8px 0 0; }}
h2 {{ font-size:15px; color:var(--accent); margin:12px 0 0; font-weight:600; }}
</style>
<div class="wrap">
  <h1>{html.escape(title)}</h1>
  <p class="sub">{len(rows)} ช็อต · ยาว {t:.1f} วิ + โลโก้ปิดท้าย 2.6 วิ · ซับเหลือง = ที่พูด/ซับไทย · ซับขาว = ซับอังกฤษ</p>
  {shots}
  <h2>หมายเหตุ</h2>
  <ul class="notes">{''.join(f"<li>{html.escape(n)}</li>" for n in notes)}</ul>
</div>'''
(here / "script.html").write_text(page)
print(len(rows), "shots", t, "sec")
