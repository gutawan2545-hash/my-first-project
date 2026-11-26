"""EP.01 voice test: three narrator candidates read the same line, then the best reads the rest of the test set.
Hard ceiling of 600 credits (owner-approved). API key is injected by the network proxy."""
import json, os, sys, subprocess, urllib.request

API = 'https://api.elevenlabs.io/v1'
CEILING = 600
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vo_test')
os.makedirs(OUT, exist_ok=True)
PLAN = {k: (who, tone, text) for k, who, tone, text in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vo_plan.json')))}
CANDIDATES = {'tonce': 'yq05eeRaHPMGuWTVpqeP', 'thanid': '3SQTl9c6zS9vh1r8maCI', 'kirin': 'uI1epevl1X6hqrxEciKt'}
JAMES = 'S2oNPNuiP27Jy2lVX5uZ'
used_file = os.path.join(OUT, 'used.json')
used = json.load(open(used_file))['used'] if os.path.exists(used_file) else 0


def tts(voice, text, name, stability=0.5):
    global used
    if used + len(text) > CEILING:
        raise SystemExit(f'STOP: would pass the {CEILING}-credit ceiling (used {used})')
    body = json.dumps({'text': text, 'model_id': 'eleven_v3', 'voice_settings': {'stability': stability}}).encode()
    req = urllib.request.Request(f'{API}/text-to-speech/{voice}?output_format=mp3_44100_128', data=body, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            audio = r.read()
    except urllib.error.HTTPError as e:
        print(name, 'HTTP', e.code, e.read()[:300]); return None
    used += len(text)
    json.dump({'used': used}, open(used_file, 'w'))
    path = os.path.join(OUT, name + '.mp3')
    open(path, 'wb').write(audio)
    dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    print(f'{name}: {dur}s  (credits used {used})', flush=True)
    return path


if __name__ == '__main__':
    step = sys.argv[1] if len(sys.argv) > 1 else 'compare'
    if step == 'compare':
        for n, v in CANDIDATES.items():
            tts(v, PLAN['N02'][2], f'N02_{n}')
    else:                                      # step = chosen candidate name
        v = CANDIDATES[step]
        for k in ('N04', 'N10'):
            tts(v, PLAN[k][2], f'{k}_{step}')
        tts(JAMES, PLAN['J08'][2], 'J08_james')
