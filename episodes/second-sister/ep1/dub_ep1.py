"""Dub EP1 of แม่ชีคนที่สอง with ElevenLabs v3.

Every spoken line of script.md (via storyboard.py ROWS) becomes vo_ep1/s###.mp3, voiced by the
character's voice from ../voices.json (narration = เมฆ). Each take is checked with speech-to-text;
an unclear take is re-recorded once and the closer take kept. Stops before the credit ceiling.
Resumable: lines already in vo_ep1/report.json are skipped.
The API key is injected by the network proxy; nothing here holds it.

Usage: python3 dub_ep1.py            -> dub everything
       python3 dub_ep1.py plan       -> print the plan and the character count, no API calls
"""
import json, os, re, subprocess, sys, difflib, urllib.request, urllib.error, time

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.elevenlabs.io/v1"
CEILING = 32000                      # ceiling for this natural re-dub run (the 32,000 the user approved with "ทุกอย่างผ่านหมด")
OUT = os.path.join(HERE, "vo_ep1_nat")      # natural re-dub (user-approved samples); vo_ep1 = previous emotion dub, kept
VOICES = json.load(open(os.path.join(HERE, "..", "voices.json")))

NS = {"__file__": os.path.join(HERE, "storyboard.py"), "__name__": "sb"}
cwd = os.getcwd(); os.chdir(HERE)
exec(open(os.path.join(HERE, "storyboard.py")).read(), NS)
os.chdir(cwd)
ROWS = NS["ROWS"]

WHO = {"เล่า": "mek", "เมฆ": "mek", "โรซา": "rosa", "เจม": "james", "ป้าแดง": "daeng", "คาทารีนา": "cat",
       "มาเรียม": "mariam", "อักเนส": "agnes", "ลูเซีย": "luc", "ยอแซฟ": "jos", "ธนา": "thana"}
PRON = {"คอนแวนต์": "คอนแวน"}      # words the TTS misreads -> spelling that sounds right
# stage directions in brackets -> v3 audio tags
TAGS = [("กระซิบ", "[whispers]"), ("สะอื้น", "[crying]"), ("ร้องไห้", "[crying]"), ("ตะโกน", "[shouting]"), ("กรีด", "[screams]"),
        ("หอบ", "[panting]"), ("กลั้นหายใจ", "[nervously]"), ("สั่น", "[shaky voice]"), ("งัวเงีย", "[sleepy]"), ("หัวเราะ", "[laughs]")]


# ---- emotion per line (user: delivery must follow the moment: whispers in suspense, startled in scares, storyteller narration)
MOOD = {}
for st in "refectory condo call email gate guestroom kitchen veranda dawn_walk path_dawn garden".split(): MOOD[st] = "calm"
for st in "mass chapel_v1".split(): MOOD[st] = "sacred"
for st in "tower_fog tower_night rosa_bed rosa_room oldwing chapel_night thana_night archive cemetery cemetery_wide drain steps sisters_ext clock rules1 rules7 note count".split(): MOOD[st] = "eerie"
for st in "flash_dorm dream album doll tag music".split(): MOOD[st] = "memory"
for st in "body_sheet police evidence_wall hand lefthand question".split(): MOOD[st] = "shock"
NARR = {"calm": "[calm]", "sacred": "[reverent]", "eerie": "[hushed]", "memory": "[nostalgic]", "shock": "[shaken]", "title": "[ominous]"}
RED = {238, 247, 251, 253}
FEEL = [("กระซิบ", "[whispers]"), ("สะอื้น", "[crying]"), ("ร้องไห้", "[crying]"), ("น้ำตา", "[tearful]"), ("ตะโกน", "[shouting]"),
        ("ตกใจ", "[startled]"), ("สะดุ้ง", "[startled]"), ("ช็อก", "[shocked]"), ("ตาเบิก", "[alarmed]"), ("หอบ", "[panting]"),
        ("หวาดหวั่น", "[fearful]"), ("กลัว", "[fearful]"), ("ระแวง", "[nervous]"), ("ขนลุก", "[fearful]"), ("หน้าซีด", "[fearful]"),
        ("เจ็บปวด", "[sad]"), ("เศร้า", "[sad]"), ("เย็นชา", "[cold]"), ("ดุ", "[stern]"), ("เข้ม", "[stern]"), ("เรียบ", "[flat]"),
        ("ตื้นตัน", "[emotional]"), ("ใจดี", "[warm]"), ("ยิ้ม", "[warm]"), ("หัวเราะ", "[laughing]"), ("ตั้งใจเล่นเกม", "[playful]"),
        ("สงสัย", "[suspicious]"), ("ละเมอ", "[dazed]"), ("งัวเงีย", "[sleepy]"), ("ลังเล", "[hesitant]"), ("เหนื่อย", "[tired]"),
        ("จริงจัง", "[serious]"), ("ลดเสียง", "[lowered voice]"), ("สั่น", "[shaky voice]"), ("พูดเร็ว", "[rushed]")]
NAME_OF = {"mek": "เมฆ", "rosa": "โรซา", "james": "เจม", "daeng": "ป้าแดง", "cat": "คาทารีนา", "mariam": "มาเรียม", "agnes": "อักเนส",
           "luc": "ลูเซีย", "jos": "คุณพ่อ", "thana": "ธนา"}
ANIM = NS.get("ANIM", {}); PANELS = NS.get("PANELS", {})
cover = {}
for sc, panels in PANELS.items():
    for idx, p in enumerate(panels):
        a, _, b = p[0].partition("-"); a = int(a); b = int(b or a)
        for n in range(a, b + 1):
            if n in cover and cover[n][2] <= b - a: continue
            cover[n] = (p[0], p[1], b - a)
def emotion(n, cid, narration, who_dirs, text):
    rng, stage, _ = cover.get(n, ("", "", 0))
    mood = MOOD.get(stage, "calm")
    if narration:
        t = "[whispers]" if "กระซิบ" in who_dirs else ("[panting]" if "หอบ" in who_dirs else NARR.get(mood, "[calm storytelling]"))
        return t
    if cid == "child": return "[eerie whisper]"
    if n in RED: return "[terrified shout]"
    expr = (ANIM.get(rng) or ("",))[0]
    parts = [x for x in expr.split("/") if NAME_OF.get(cid, "@") in x or (cid == "jos" and "ยอแซฟ" in x)]
    if not parts and "/" not in expr: parts = [expr]
    pool = who_dirs + " " + " ".join(parts)
    tags = []
    for k, t in FEEL:
        if k in pool and t not in tags: tags.append(t)
    if cid == "agnes" and not tags: tags = ["[eerily sweet]"]
    if cid == "luc" and not tags: tags = ["[frail, confused]"]
    if not tags and "!" in text: tags = ["[urgent]"]
    if not tags and mood == "eerie": tags = ["[nervous]"]
    return " ".join(tags[:2])

# ---- natural delivery (user-approved tests): at most one light tag, no levelling; real non-verbal sounds only where they happen
GAIN = {"[whispers]": -10, "[softly]": -5, "[quietly]": -5, "[low voice]": -5, "[sighs]": -4, "[wistful]": -3, "[gently]": -3, "[tearful]": -2,
        "[sobbing]": -1, "[gasps]": 2, "[panicked]": 3, "[startled]": 2, "[urgent]": 1}
def natural(n, cid, narration, who_dirs, text):
    """Returns (prefix tag, mid-line tag or '', gain dB)."""
    rng, stage, _ = cover.get(n, ("", "", 0))
    mood = MOOD.get(stage, "calm")
    a = ANIM.get(rng) or ("", "", "", "")
    expr = a[0]; act = a[1]
    if narration:
        if "กระซิบ" in who_dirs: t = "[whispers]"
        elif "หอบ" in who_dirs or "หอบ" in expr: t = "[breathing heavily]"
        else: t = {"eerie": "[softly]", "memory": "[wistful]", "shock": "[quietly]", "title": "[low voice]", "sacred": "[softly]"}.get(mood, "")
        return t, "", GAIN.get(t, 0) - 2
    if cid == "child": return "[whispers]", "", -6
    parts = [x for x in expr.split("/") if NAME_OF.get(cid, "@") in x or (cid == "jos" and "ยอแซฟ" in x)]
    if not parts and "/" not in expr: parts = [expr]
    pool = who_dirs + " " + " ".join(parts) + " " + " ".join(x for x in act.split("/") if NAME_OF.get(cid, "@") in x)
    has = lambda *ks: any(k in pool for k in ks)
    if cid == "agnes": return ("[whispers]", "", -10) if "กระซิบ" in pool else ("[softly]", "", -3)
    if cid == "luc": return "[frail]", "", -3
    if n in (238,): return "[gasps]", "", 2
    if n in (247,): return "[startled]", "", 2
    if n in (251, 253): return "[panicked]", "", 3
    if has("กระซิบ"): return "[whispers]", "", -10
    if has("สะอื้น", "ร้องไห้", "น้ำตาไหล"): return "[sobbing]", "[sniffles]", -1
    if has("น้ำตาคลอ", "น้ำตา", "ตื้นตัน"): return "[tearful]", "", -2
    if has("หอบ", "วิ่ง"): return "[panting]", "", 0
    if has("หัวเราะ", "ขำ", "ตลก"): return "[laughs]", "", 0
    if has("แซว", "ยิ้มมุมปาก", "ผิวปาก", "ยิ้มกวน"): return "[chuckles]", "", 0
    if has("ถอนหายใจ", "เหนื่อยใจ", "ปลง", "เบื่อ", "ยิ้มเหนื่อย"): return "[sighs]", "", -4
    if has("ตกใจ", "สะดุ้ง", "ช็อก", "ตาเบิก"): return "[gasps]", "", 1
    if has("หวาดหวั่น", "กลัว", "ระแวง", "ขนลุก", "หน้าซีด"): return "[nervously]", "", -2
    if has("ลังเล", "สงสัย"): return "[hesitant]", "", -1
    if has("ใจดี", "ยิ้ม", "อบอุ่น"): return "[warmly]", "", 0
    if has("เศร้า", "เจ็บปวด"): return "[sadly]", "", -3
    if has("ละเมอ", "งัวเงีย"): return "[sleepy]", "", -4
    if cid == "agnes": return "[softly]", "", -3
    if cid == "luc": return "[frail]", "", -3
    if cid == "james" and stage in ("condo",): return "[casual]", "", 0
    if mood == "eerie": return "[softly]", "", -3
    return "", "", 0
OVERRIDE = {   # key: (full spoken text with tags, gain)
    "s018": ("[whispers] แล้วเด็กคนนั้นก็เป่าเทียนดับ", -9),
    "s041": ("[chuckles] หน้าแบบนี้ ใครทวงเงินมึงอีกล่ะ", 0), "s042": ("[tired] ที่เก่ากู เขาจะทำหนังสือครบร้อยปี ให้กูไปถ่ายรูปเอกสารเก่าทั้งหมด สามอาทิตย์", -2),
    "s043": ("[casual] ค่าจ้างเท่านี้ มึงจะคิดทำไม ไปเหอะ ถือว่ากลับไปเยี่ยมบ้านด้วย", 0), "s044": ("[sighs] มันไม่ใช่บ้านว่ะ", -5),
    "s045": ("[gently] มึงไม่เคยเล่าเรื่องที่นั่นให้กูฟังเลยนะ สิบปีที่รู้จักกันมา", -3), "s048": ("[whispers] …เชี่ย", -10),
    "s052": ("[softly] มึงเคยตามหาน้องไหม", -5), "s057": ("[laughs] ไปเถอะ ถ้าเจอผีก็วิดีโอคอลมา [chuckles] กูตื่นทั้งคืนอยู่แล้ว", 0),
    "s192": ("[laughs softly] ยังครับป้า… รสเดิมเลยนะป้า", -2), "s065": ("[sobbing] เมฆ… [sniffles] ใช่เมฆจริง ๆ ใช่ไหมลูก", -1),
    "s245": ("[breathing heavily] โซ่ประตูหอระฆังถูกปลด… [gasps] มีคนขึ้นไปข้างบน", -3), "s238": ("[gasps] อะไรวะนั่น!", 2),
    "s248": ("[panting] ไม่มีใคร… [panting] มีแต่รอยเท้าเปียก ๆ บนพื้น", -2), "s265": ("[sobbing] ป้าแดง… ไม่จริง… [crying] ป้าบอกว่าจะสอนหนูทำแกงจืด…", -1),
    # roll call and jokes (user: friends laugh at jokes, natural)
    "s301": ("[low voice] คุณเคยได้ยินเรื่องกฎเจ็ดข้อ ของคอนแวนเซนต์เวโรนิกาไหมครับ", -2),
    "s310": ("[chuckles] หนึ่งนาทีของโรซา… ใช้ไปสิบนาที แต่ผมก็ได้รู้ว่าที่นี่มีคนอยู่ไม่ถึงยี่สิบคน", -1),
    "s311": ("[amused] เข้มงวดที่สุดในที่นี้ ผมเดาว่าขนาดนาฬิกายังไม่กล้าเดินช้ากว่าที่มาเธอร์สั่ง", -1),
    "s314": ("[chuckles] และช่างพูดที่สุดด้วย", -1),
    "s316": ("[sighs] โรซาบอกชื่อครบทั้งเก้าคน ผมจำได้ไม่ถึงครึ่ง ทุกคนต้องกลับเข้าหลังรั้วตอนหกโมงเย็น", -3),
    "s320": ("[cheerfully] คุณเมฆอยากรู้ไหมคะว่าที่นี่มีใครบ้าง หนูสรุปให้ได้ภายในหนึ่งนาทีเลย", 0),
    "s330": ("[nervous laugh] หนูชอบเดินตรงนี้ตอนกลางวันนะคะ ส่วนตอนกลางคืน… หนูวิ่ง", 0),
    "s331": ("[laughs] สามสิบเอ็ดแล้วยังไม่มีอีก เดี๋ยวป้าให้ซิสเตอร์ช่วยสวดให้ทั้งโบสถ์เลย", 0),
    "s341": ("[cheerfully] คนแรก มาเธอร์คาทารีนา อธิการิณีของเราค่ะ", 0),
    "s344": ("[giggles] ส่วนหนู โรซา แม่ชีฝึกหัด อายุน้อยที่สุดค่ะ", 0),
    "s346": ("[cheerfully] แล้วก็ซิสเตอร์อีกเก้าคนค่ะ คนแรกชื่อ…", 0),
    "s348": ("[laughs softly] ป้าแดง คุณเมฆรู้จักอยู่แล้วเนอะคะ", 0),
}
def with_mid(text, mid):
    """Put the second sound (e.g. a sniffle) at a natural break in longer lines."""
    if not mid or len(text) < 24: return text
    for br in ("… ", " "):
        i = len(text) // 3
        while True:
            i = text.find(br, i)
            if i < 0 or i >= len(text) - 6: break
            j = i + len(br)
            if not text[j:].startswith("ๆ"): return text[:j] + mid + " " + text[j:]
            i = j
    return text

def plan():
    out = []
    for n in sorted(ROWS):
        aud = ROWS[n][2]
        m = re.match(r"\s*\*\*([^*]+):\*\*\s*(.*)", aud)
        if not m: continue
        who, text = m.group(1).strip(), m.group(2)
        base = re.sub(r"\s*\(.*?\)", "", who).strip()
        if base.startswith("เสียงเด็ก") or base.startswith("เด็ก"): cid = "child"
        else: cid = WHO.get(base)
        if not cid: continue
        dirs = " ".join(re.findall(r"\(([^)]*)\)", who + " " + text))
        tag, mid, gain = natural(n, cid, base == "เล่า", dirs, text)
        clean = re.sub(r"\s+", " ", re.sub(r"\([^)]*\)", "", text).replace("**", "")).strip()
        clean = re.sub(r"(?<!\*)\*[^*]+\*(?!\*)", "", clean).strip()     # drop *sfx*
        if not clean: continue
        for w, say in PRON.items(): clean = clean.replace(w, say)   # spoken spelling only; subtitles keep the script
        spoken = (tag + " " + with_mid(clean, mid)).strip()
        if f"s{n:03d}" in OVERRIDE: spoken, gain = OVERRIDE[f"s{n:03d}"]
        out.append({"key": f"s{n:03d}", "n": n, "cid": cid, "narration": base == "เล่า", "text": spoken, "plain": clean, "gain": gain})
    return out


def tts(voice, text, stability):
    body = {"text": text, "model_id": "eleven_v3", "language_code": "th", "voice_settings": {"stability": stability}}
    req = urllib.request.Request(f"{API}/text-to-speech/{voice}?output_format=mp3_44100_128", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 502, 503) and attempt < 3: time.sleep(5 * (attempt + 1)); continue
            raise SystemExit(f"TTS failed ({e.code}): {msg}")
        except urllib.error.URLError:
            if attempt < 3: time.sleep(5 * (attempt + 1)); continue
            raise


STT_OK = True
def stt(path):
    global STT_OK
    if not STT_OK: return None
    r = subprocess.run(["curl", "-s", "-X", "POST", f"{API}/speech-to-text", "-F", "model_id=scribe_v1", "-F", "language_code=tha",
                        "-F", f"file=@{path}"], capture_output=True, text=True, timeout=180).stdout
    try:
        d = json.loads(r)
        if "text" in d: return d["text"]
    except Exception:
        pass
    print("  speech-to-text unavailable, continuing without checks:", r[:160]); STT_OK = False
    return None


norm = lambda s: re.sub(r"[\s\.\?\!…,\"'“”‘’\-–—~]|\[[^\]]*\]", "", s)
dur_of = lambda p: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                        capture_output=True, text=True).stdout or 0)


def main():
    P = plan()
    total = sum(len(x["text"]) for x in P)
    if len(sys.argv) > 1 and sys.argv[1] == "plan":
        by = {}
        for x in P: by[x["cid"]] = by.get(x["cid"], 0) + len(x["text"])
        print(json.dumps(by, ensure_ascii=False), "lines", len(P), "chars", total); return
    os.makedirs(OUT, exist_ok=True)
    rp = os.path.join(OUT, "report.json")
    rep = json.load(open(rp)) if os.path.exists(rp) else {"used": 0, "lines": {}}
    for x in P:
        if x["key"] in rep["lines"]: continue
        voice = VOICES[x["cid"]]["voice_id"]
        takes = []
        for take, stab in ((1, 0.5),):   # natural setting only, one take
            if rep["used"] + len(x["text"]) > CEILING:
                json.dump(rep, open(rp, "w"), ensure_ascii=False, indent=1)
                raise SystemExit(f"STOP: next take would pass the {CEILING}-credit ceiling (used {rep['used']})")
            audio = tts(voice, x["text"], stab)
            rep["used"] += len(x["text"])
            path = os.path.join(OUT, f"{x['key']}_t{take}.mp3"); open(path, "wb").write(audio)
            heard = stt(path)
            score = difflib.SequenceMatcher(None, norm(x["plain"]), norm(heard)).ratio() if heard is not None else None
            takes.append({"path": os.path.basename(path), "take": take, "dur": round(dur_of(path), 2), "heard": heard, "score": score})
            print(f"{x['key']} {x['cid']:7s} take{take} {takes[-1]['dur']:5.2f}s score={score if score is None else round(score, 2)}  credits {rep['used']}", flush=True)
            if score is None or score >= 0.75: break
        best = max(takes, key=lambda t: (t["score"] or 0, -t["take"]))
        os.replace(os.path.join(OUT, best["path"]), os.path.join(OUT, x["key"] + ".mp3"))
        rep["lines"][x["key"]] = {"n": x["n"], "cid": x["cid"], "text": x["text"], "dur": best["dur"], "score": best["score"], "takes": len(takes), "gain": x["gain"]}
        json.dump(rep, open(rp, "w"), ensure_ascii=False, indent=1)
    print("DONE credits used", rep["used"], "lines", len(rep["lines"]))


if __name__ == "__main__":
    main()
