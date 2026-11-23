"""Scene test for the natural re-dub: eight lines of the condo conversation (shots 41-52) voiced as one exchange.
eleven_v3, stability 0.5, ONE light tag per line chosen for how people actually talk (teasing, tired, quiet, gentle, whisper),
then mixed like a scene: each line keeps its own loudness from the tag (whispers well under normal speech, nothing
levelled to the same volume), gaps that follow the talk (quick replies, a longer pause before the heavy line), almost no echo."""
import json, os, sys, subprocess, urllib.request, importlib.util
V = json.load(open("../voices.json"))
sys.argv = [sys.argv[0], "plan"]
spec = importlib.util.spec_from_file_location("dub", "dub_ep1.py"); dub = importlib.util.module_from_spec(spec)
so = sys.stdout; sys.stdout = open(os.devnull, "w"); spec.loader.exec_module(dub); sys.stdout = so
P = {x["key"]: x for x in dub.plan()}
LINES = [("s041", "[teasing]", 0, .35), ("s042", "[tired]", -2, .3), ("s043", "[casual]", 0, .25), ("s044", "[quietly]", -6, .9),
         ("s045", "[gently]", -3, 1.1), ("s047", "[sadly]", -4, .7), ("s048", "[whispers]", -10, .6), ("s052", "[softly]", -5, .5)]
os.makedirs("vo_scenetest", exist_ok=True); used = 0
for k, tag, _, _ in LINES:
    f = f"vo_scenetest/{k}.mp3"
    if os.path.exists(f): continue
    x = P[k]; body = {"text": f"{tag} {x['plain']}", "model_id": "eleven_v3", "language_code": "th", "voice_settings": {"stability": 0.5}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V[x['cid']]['voice_id']}?output_format=mp3_44100_128", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    open(f, "wb").write(urllib.request.urlopen(req, timeout=180).read()); used += len(body["text"]); print(k, "ok", flush=True)
print("credits", used)
# mix: per-line loudness normalised to one speech level, THEN the tag's offset (so dynamics are intentional), gaps from the talk
parts, inputs = [], []
for i, (k, tag, db, gap) in enumerate(LINES):
    inputs += ["-i", f"vo_scenetest/{k}.mp3"]
    parts.append(f"[{i}]atempo=0.95,aresample=44100,aformat=channel_layouts=mono,loudnorm=I=-18:TP=-2:LRA=11,volume={db}dB,apad=pad_dur={gap}[a{i}]")
fc = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(len(LINES))) + f"concat=n={len(LINES)}:v=0:a=1,aecho=0.8:0.5:22:0.08,highpass=f=70[out]"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]", "-c:a", "aac", "-b:a", "160k", "voice_scene_test.m4a"], check=True)
print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "voice_scene_test.m4a"], capture_output=True, text=True).stdout)
