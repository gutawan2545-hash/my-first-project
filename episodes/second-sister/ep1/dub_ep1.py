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
CEILING = 20000                      # user-approved credit ceiling for this episode
OUT = os.path.join(HERE, "vo_ep1")
VOICES = json.load(open(os.path.join(HERE, "..", "voices.json")))

NS = {"__file__": os.path.join(HERE, "storyboard.py"), "__name__": "sb"}
cwd = os.getcwd(); os.chdir(HERE)
exec(open(os.path.join(HERE, "storyboard.py")).read(), NS)
os.chdir(cwd)
ROWS = NS["ROWS"]

WHO = {"เล่า": "mek", "เมฆ": "mek", "โรซา": "rosa", "เจมส์": "james", "ป้าแดง": "daeng", "คาทารีนา": "cat",
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
NAME_OF = {"mek": "เมฆ", "rosa": "โรซา", "james": "เจมส์", "daeng": "ป้าแดง", "cat": "คาทารีนา", "mariam": "มาเรียม", "agnes": "อักเนส",
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
        tag = emotion(n, cid, base == "เล่า", dirs, text)
        clean = re.sub(r"\s+", " ", re.sub(r"\([^)]*\)", "", text).replace("**", "")).strip()
        clean = re.sub(r"(?<!\*)\*[^*]+\*(?!\*)", "", clean).strip()     # drop *sfx*
        if not clean: continue
        for w, say in PRON.items(): clean = clean.replace(w, say)   # spoken spelling only; subtitles keep the script
        out.append({"key": f"s{n:03d}", "n": n, "cid": cid, "narration": base == "เล่า", "text": (tag + " " + clean).strip(), "plain": clean})
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
        for take, stab in ((1, 0.5), (2, 1.0)):
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
        rep["lines"][x["key"]] = {"n": x["n"], "cid": x["cid"], "text": x["text"], "dur": best["dur"], "score": best["score"], "takes": len(takes)}
        json.dump(rep, open(rp, "w"), ensure_ascii=False, indent=1)
    print("DONE credits used", rep["used"], "lines", len(rep["lines"]))


if __name__ == "__main__":
    main()
