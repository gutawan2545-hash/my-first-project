"""Dubs episode 1 with the channel voices (ElevenLabs v3), checks every take with speech-to-text,
re-records unclear lines and keeps the closest take. Stops before going over the credit ceiling.
The API key is injected by the network proxy; nothing here holds it."""
import json, os, re, subprocess, difflib, sys, time
import urllib.request

API = 'https://api.elevenlabs.io/v1'
VOICE = {'J': 'S2oNPNuiP27Jy2lVX5uZ', 'T': 'IM6pYHlwZQDuZqGBrSYI'}
CEILING = 1200 - 593
PLAN = json.load(open('vo_redo.json'))          # [key, who, tone, text]
os.makedirs('el', exist_ok=True)
used = 0; log = []


def post_json(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def tts(key, text, take, stability):
    global used
    if used + len(text) > CEILING:
        raise SystemExit(f'STOP: next take would pass the {CEILING}-credit ceiling (used {used})')
    v = VOICE['T' if key.startswith('T') else 'J']
    audio = post_json(f'{API}/text-to-speech/{v}?output_format=mp3_44100_128',
                      {'text': text, 'model_id': 'eleven_v3', 'voice_settings': {'stability': stability}})
    used += len(text)
    path = f'el/{key}_v2_t{take}.mp3'
    open(path, 'wb').write(audio)
    return path


def stt(path):
    out = subprocess.run(['curl', '-s', '-X', 'POST', f'{API}/speech-to-text', 
                          '-F', 'model_id=scribe_v1', '-F', 'language_code=tha', '-F', f'file=@{path}'],
                         capture_output=True, text=True, timeout=180).stdout
    try:
        d = json.loads(out)
    except Exception:
        return None, out[:200]
    if 'text' not in d:
        return None, json.dumps(d)[:300]
    return d['text'], None


norm = lambda s: re.sub(r'[\s\.\?\!…,"\'“”]|\[[^\]]*\]', '', s)
stt_ok = True
results = {}
for key, who, tone, text in PLAN:
    target = norm(text)
    takes = []
    for take, stab in enumerate([0.5, 0.5, 1.0], start=1):
        path = tts(key, text, take, stab)
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout or 0)
        heard, err = (stt(path) if stt_ok else (None, 'skipped'))
        if heard is None and err and err != 'skipped':
            print('  speech-to-text unavailable:', err); stt_ok = False
        score = difflib.SequenceMatcher(None, target, norm(heard)).ratio() if heard is not None else None
        takes.append(dict(path=path, take=take, dur=round(dur, 2), heard=heard, score=score))
        print(f'{key} take{take} dur={dur:.2f}s score={score} heard={heard!r}  (credits used {used})', flush=True)
        if score is None or score >= 0.9:
            break
    best = max(takes, key=lambda x: (x['score'] or 0, -x['take']))
    results[key] = dict(best=best, takes=takes, text=text, tone=tone, who=who)
    json.dump(dict(used=used, results=results), open('el/report_redo.json', 'w'), ensure_ascii=False, indent=1)
print('DONE credits used', used)
