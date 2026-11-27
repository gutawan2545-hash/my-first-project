"""EP.01 dub, script v5 (owner picked take A: v3, stability 0.0 = Creative). Old v4 takes kept in vo_v4/.
Credit ceiling 2,000 (owner approved the plan). Key injected by the network proxy.
Output: vo/<key>.wav (mono 44.1k) + vo/durations.json"""
import json, os, subprocess, urllib.request

H = os.path.dirname(os.path.abspath(__file__))
API = 'https://api.elevenlabs.io/v1'
CEILING = 300
VOICE = {'narrator': 'yq05eeRaHPMGuWTVpqeP',      # Tonce (owner's pick)
         'james': 'S2oNPNuiP27Jy2lVX5uZ',         # เจมจิ (channel voice)
         'agent': 'bTU3YcWRdgcxQzaPPSNs',         # ชายแท้
         'uncle': 'gImkfeJS2sJvoWcxNPos',         # คุณพ่อ
         'staff': 'qJqi8XxeBcos4asE2nOV',         # ตำรวจ (flat, on the phone)
         'electrician': 'bTU3YcWRdgcxQzaPPSNs',
         'neighbor': 'iP95p4xoKVk53GoZ742B'}      # Chris (English voice speaking Thai = the foreign neighbour)
REUSE = {'N01': 'A_creative'}
plan = json.load(open(os.path.join(H, 'vo_plan_v5.json')))
os.makedirs(os.path.join(H, 'vo'), exist_ok=True)
used = 0
dur = {}


def tts(voice, text, path):
    global used
    if used + len(text) > CEILING:
        raise SystemExit(f'STOP: ceiling {CEILING} (used {used})')
    body = json.dumps({'text': text, 'model_id': 'eleven_v3', 'voice_settings': {'stability': 0.0}}).encode()
    req = urllib.request.Request(f'{API}/text-to-speech/{voice}?output_format=mp3_44100_128', data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=180) as r:
        open(path, 'wb').write(r.read())
    used += len(text)


for key, who, tone, text in plan:
    wav = os.path.join(H, 'vo', key + '.wav')
    if not os.path.exists(wav):
        mp3 = os.path.join(H, 'vo_test5', REUSE[key] + '.mp3') if key in REUSE else os.path.join(H, 'vo', key + '.mp3')
        if key not in REUSE and not os.path.exists(mp3):
            tts(VOICE[who], text, mp3)
        # trim leading/trailing silence, mono 44.1k
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-af',
                        'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse',
                        '-ac', '1', '-ar', '44100', wav], check=True)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True).stdout)
    dur[key] = round(d, 3)
    print(f'{key:4} {who:11} {d:5.2f}s  credits {used}', flush=True)
json.dump(dur, open(os.path.join(H, 'vo', 'durations.json'), 'w'), indent=1)
print('TOTAL voice seconds', round(sum(dur.values()), 1), 'credits used this run', used)
