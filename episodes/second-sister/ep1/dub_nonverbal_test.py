"""Test of non-verbal sounds inside the natural delivery (user: friends laugh at a joke, breathing/panting when tense,
sighs when it's wearying, real sobbing when crying). eleven_v3, stability 0.5, tags placed where the sound happens."""
import json, os, sys, subprocess, urllib.request, importlib.util
V = json.load(open("../voices.json"))
LINES = [  # key, cid, text with tags, gain dB, gap after
    ("s057", "james", "[laughs] ไปเถอะ ถ้าเจอผีก็วิดีโอคอลมา [chuckles] กูตื่นทั้งคืนอยู่แล้ว", 0, .9),
    ("s192", "mek", "[laughs softly] ยังครับป้า… รสเดิมเลยนะป้า", -2, 1.0),
    ("s044", "mek", "[sighs] มันไม่ใช่บ้านว่ะ", -5, 1.0),
    ("s065", "daeng", "[sobbing] เมฆ… [sniffles] ใช่เมฆจริง ๆ ใช่ไหมลูก", -1, 1.1),
    ("s245", "mek", "[breathing heavily] โซ่ประตูหอระฆังถูกปลด… [gasps] มีคนขึ้นไปข้างบน", -3, .7),
    ("s238", "james", "[gasps] อะไรวะนั่น!", 2, .8),
    ("s248", "mek", "[panting] ไม่มีใคร… [panting] มีแต่รอยเท้าเปียก ๆ บนพื้น", -2, 1.0),
    ("s265", "mariam", "[sobbing] ป้าแดง… ไม่จริง… [crying] ป้าบอกว่าจะสอนหนูทำแกงจืด…", -1, .6)]
os.makedirs("vo_nvtest", exist_ok=True); used = 0
for k, cid, text, _, _ in LINES:
    f = f"vo_nvtest/{k}.mp3"
    if os.path.exists(f): continue
    body = {"text": text, "model_id": "eleven_v3", "language_code": "th", "voice_settings": {"stability": 0.5}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V[cid]['voice_id']}?output_format=mp3_44100_128", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    open(f, "wb").write(urllib.request.urlopen(req, timeout=180).read()); used += len(text); print(k, "ok", flush=True)
print("credits", used)
inputs, parts = [], []
for i, (k, _, _, db, gap) in enumerate(LINES):
    inputs += ["-i", f"vo_nvtest/{k}.mp3"]
    parts.append(f"[{i}]atempo=0.95,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,loudnorm=I=-18:TP=-2:LRA=11,volume={db}dB,aresample=44100,apad=pad_dur={gap}[a{i}]")
fc = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(len(LINES))) + f"concat=n={len(LINES)}:v=0:a=1,aecho=0.8:0.5:22:0.08,highpass=f=70[out]"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]", "-c:a", "aac", "-b:a", "160k", "voice_nonverbal_test.m4a"], check=True)
