"""พากย์ตอนฮอกวอตส์สาขาไทยด้วย ElevenLabs (eleven_v3) · คีย์ถูกใส่โดย network proxy ไม่มีในไฟล์นี้
ใช้: python3 dub_el.py test   -> ลองเสียงละหนึ่งประโยคสั้น
     python3 dub_el.py full   -> พากย์ทุกประโยค (อัดซ้ำเมื่อฟังไม่ชัด ถ้าตรวจด้วย speech-to-text ได้)
หยุดทันทีถ้าจะเกินเพดานเครดิต · บันทึก el/report.json · ไฟล์ที่ใช้จริง vo_el/sNN_i.wav"""
import json, os, re, sys, subprocess, difflib, urllib.request, urllib.error, pathlib
HERE = pathlib.Path(__file__).parent; EP = HERE.parent; os.chdir(HERE)
API = "https://api.elevenlabs.io/v1"
CEILING = 1800
os.makedirs("el", exist_ok=True); os.makedirs("vo_el", exist_ok=True)
VOICE = {   # เสียงสำเร็จรูปของ ElevenLabs + เสียงประจำช่อง (เจม/ตะวัน) เป็นตัวสำรอง
    "ซิ่ง": "TX3LPaxmHKxFdv7VOQHJ", "อาม้า": "XrExE9yKIg1WjnnlVkGX", "ลุงเปี๊ยก": "pqHfZKP75CVOlQylNhV4",
    "ลุงโต": "nPczCjzI2devNBz1zQrb", "ป้าแต๋ว": "FGY2WhTYpPnrIDTdsKH5", "ต้น": "IKne3meq5aSn9XLyUdCD",
    "เดรโก": "N2lVS1w4EtoT3dr4eOWO", "หมวก": "JBFqnCBsd6RMkjVDRZzb", "ไก่": "N2lVS1w4EtoT3dr4eOWO",
}
FALLBACK = {"ซิ่ง": "S2oNPNuiP27Jy2lVX5uZ", "อาม้า": "IM6pYHlwZQDuZqGBrSYI", "ป้าแต๋ว": "IM6pYHlwZQDuZqGBrSYI"}
TAG = {"ซิ่ง": "", "อาม้า": "[excited] ", "ลุงเปี๊ยก": "[cheerful] ", "ลุงโต": "", "ป้าแต๋ว": "[shouting] ", "ต้น": "[cheerful] ", "เดรโก": "[smug] ", "หมวก": "", "ไก่": "[shouting] "}
used_path = pathlib.Path("el/used.json")
used = json.loads(used_path.read_text())["used"] if used_path.exists() else 0

def who_of(s):
    s = s.replace("หมวกคัดสรร", "หมวก")
    return next((k for k in VOICE if k in s), None)

def lines():
    out = []
    for line in (EP / "script.md").read_text().splitlines():
        if not re.match(r"^\| \d+ \|", line):
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        n, spk = int(c[0]), c[2]
        for i, p in enumerate([q.strip() for q in c[3].split("·")]):
            m = re.match(r"^\(([^)]+)\)\s*(.+)$", p)
            if m and who_of(m.group(1)):
                out.append((n, len([o for o in out if o[0] == n]), who_of(m.group(1)), m.group(2)))
            else:
                t = re.sub(r"\([^)]*\)", "", p).strip()
                if t:
                    out.append((n, len([o for o in out if o[0] == n]), who_of(spk.split("→")[0]) or "ซิ่ง", t))
    return out

def tts(voice, text, path, stability=0.5):
    global used
    if used + len(text) > CEILING:
        raise SystemExit(f"STOP: จะเกินเพดาน {CEILING} เครดิต (ใช้ไป {used})")
    req = urllib.request.Request(f"{API}/text-to-speech/{voice}?output_format=mp3_44100_128",
                                 data=json.dumps({"text": text, "model_id": "eleven_v3", "voice_settings": {"stability": stability}}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            open(path, "wb").write(r.read())
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read()[:200]!r}"
    used += len(text); used_path.write_text(json.dumps({"used": used}))
    return None

def stt(path):
    r = subprocess.run(["curl", "-s", "-X", "POST", f"{API}/speech-to-text", "-F", "model_id=scribe_v1", "-F", "language_code=tha", "-F", f"file=@{path}"],
                       capture_output=True, text=True, timeout=180).stdout
    try:
        d = json.loads(r); return d.get("text")
    except Exception:
        return None

norm = lambda s: re.sub(r"[\s\.\?\!…,\"'“”]|\[[^\]]*\]", "", s)
def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout or 0)

mode = sys.argv[1] if len(sys.argv) > 1 else "test"
report = json.loads(pathlib.Path("el/report.json").read_text()) if pathlib.Path("el/report.json").exists() else {}
if mode == "test":
    SAMPLE = {"ซิ่ง": "เกรดผมหนึ่งจุดห้าเองนะเว้ย", "อาม้า": "แท้! ทองเก้าสิบหกจุดห้า!", "ลุงเปี๊ยก": "สามร้อย! คนตัวใหญ่คิดสองที่!",
              "ลุงโต": "ต้องถวายน้ำแดงก่อนนะไอ้หนู", "ป้าแต๋ว": "สามอันร้อยจ้า!", "ต้น": "เสี่ยว! ไม้ข้าวเหนียวปิ้ง!",
              "เดรโก": "พ่อมดใหญ่!", "หมวก": "มาเช็กเกลียวฉันเหรอ?"}
    for who, text in SAMPLE.items():
        path = f"el/test_{VOICE[who]}.mp3"
        err = tts(VOICE[who], TAG[who] + text, path)
        if err:
            print(who, "ERROR", err); report[f"test:{who}"] = dict(error=err); continue
        heard = stt(path); sc = difflib.SequenceMatcher(None, norm(text), norm(heard or "")).ratio() if heard else None
        print(f"{who}: {dur(path):.2f}s heard={heard!r} score={sc}  (ใช้ไป {used})", flush=True)
        report[f"test:{who}"] = dict(path=path, heard=heard, score=sc)
else:
    voices = json.loads(pathlib.Path("el/voices.json").read_text()) if pathlib.Path("el/voices.json").exists() else VOICE
    for n, i, who, text in lines():
        key = f"s{n:02d}_{i}"; final = f"vo_el/{key}.wav"
        if report.get(key, {}).get("text") == text and os.path.exists(final):
            continue
        prev = next((k for k, v in report.items() if isinstance(v, dict) and v.get("text") == text and v.get("who") == who and os.path.exists(f"vo_el_prev/{k}.wav")), None)
        if prev:                                             # ข้อความเดิม ใช้เสียงเดิม ไม่เสียเครดิต
            subprocess.run(["cp", f"vo_el_prev/{prev}.wav", final], check=True)
            report[key] = dict(report[prev]); print(key, "reuse", prev); continue
        takes = []
        for take, stab in enumerate([0.5, 0.5, 1.0], 1):
            path = f"el/{key}_t{take}.mp3"
            tag = "[singing] " if "โอ้ละหนอ" in text else ("[amazed] " if "ครั้งแรกของโลก" in text else TAG[who])
            err = tts(voices[who], tag + text, path, stab)
            if err:
                print(key, "ERROR", err); break
            heard = stt(path); sc = difflib.SequenceMatcher(None, norm(text), norm(heard or "")).ratio() if heard else None
            takes.append(dict(path=path, score=sc, heard=heard))
            print(f"{key} {who} take{take} score={sc} heard={heard!r} (ใช้ไป {used})", flush=True)
            if sc is None or sc >= 0.8:
                break
        if takes:
            best = max(takes, key=lambda x: x["score"] or 0)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", best["path"], "-ac", "1", "-ar", "48000", final], check=True)
            report[key] = dict(who=who, text=text, best=best, takes=takes)
            pathlib.Path("el/report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
pathlib.Path("el/report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
print("credits used", used)
