"""Voice test for the 'natural, conversational' re-dub (user: not stiff, not over-acted, smooth, like people telling
a story to each other, with light and heavy). Two candidates per line, so the user can pick by ear:
  A = eleven_v3, one soft tag at most, stability 0.5
  B = eleven_multilingual_v2, no tags, previous/next line given for natural flow, stability 0.45, style 0.15
Writes vo_nattest/{key}_A.mp3 / _B.mp3 and voice_natural_test.m4a (A then B per line). Key comes from the proxy."""
import json, os, re, subprocess, urllib.request, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "vo_nattest"); os.makedirs(OUT, exist_ok=True)
V = json.load(open(os.path.join(HERE, "..", "voices.json")))
sys.argv = [sys.argv[0], "plan"]
import importlib.util
spec = importlib.util.spec_from_file_location("dub", os.path.join(HERE, "dub_ep1.py")); dub = importlib.util.module_from_spec(spec)
so = sys.stdout; sys.stdout = open(os.devnull, "w"); spec.loader.exec_module(dub); sys.stdout = so
P = {x["key"]: x for x in dub.plan()}; keys = sorted(P)
TEST = {"s006": "[softly]", "s041": "[casual]", "s065": "[tearful]", "s186": "[gently]", "s227": "[thoughtful]", "s238": "[startled]"}
used = 0
def tts(voice, body):
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=180).read()
for k, tag in TEST.items():
    if os.path.exists(f"{OUT}/{k}_B.mp3"): continue
    x = P[k]; voice = V[x["cid"]]["voice_id"]; i = keys.index(k)
    prev = P[keys[i - 1]]["plain"] if i else ""; nxt = P[keys[i + 1]]["plain"] if i + 1 < len(keys) else ""
    a = open(f"{OUT}/{k}_A.mp3","rb").read() if os.path.exists(f"{OUT}/{k}_A.mp3") else tts(voice, {"text": f"{tag} {x['plain']}", "model_id": "eleven_v3", "language_code": "th", "voice_settings": {"stability": 0.5}})
    open(f"{OUT}/{k}_A.mp3", "wb").write(a); used += len(tag) + 1 + len(x["plain"])
    b = tts(voice, {"text": x["plain"], "model_id": "eleven_multilingual_v2", "previous_text": prev, "next_text": nxt,
                    "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True}})
    open(f"{OUT}/{k}_B.mp3", "wb").write(b); used += len(x["plain"])
    print(k, x["cid"], "ok", flush=True)
print("credits used", used)
