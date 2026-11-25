"""พากย์ตอนงานแต่งด้วย ElevenLabs v3 ตรวจทุกเทกด้วยระบบถอดเสียง อัดใหม่เฉพาะประโยคที่ไม่ชัด
หยุดเองก่อนใช้เกินเพดานเครดิต คีย์ถูกใส่โดย proxy ของเครือข่าย ไฟล์นี้ไม่มีคีย์
ผู้บรรยาย = เสียงตะวัน · ผู้หญิงชุดดำ = Lily (คลังมาตรฐาน) · เจ้าบ่าว = Callum (คลังมาตรฐาน)"""
import json, os, re, subprocess, difflib, urllib.request, urllib.error

API = 'https://api.elevenlabs.io/v1'
VOICE = {'N': 'IM6pYHlwZQDuZqGBrSYI', 'W': 'pFZP5JQG7iQjIQuC4Bkx', 'G': 'N2lVS1w4EtoT3dr4eOWO'}
FALLBACK = {'W': 'XB0fDUnXU5powFXDhCwa', 'G': 'JBFqnCBsd6RMkjVDRZzb'}
CEILING = 2200
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, 'vo'), exist_ok=True)
used = 0

def lines():
    out = []
    for l in open(os.path.join(HERE, '..', 'script.md')):
        m = re.match(r'^(\d+)\. (.*)$', l.strip())
        if not m or int(m.group(1)) > 25: continue
        n, t = int(m.group(1)), m.group(2)
        t = re.sub(r'^\(.*?\)\s*', '', t)
        parts = re.split(r'(\[[^\]]*\])', t); who = 'N'; k = 0
        for p in parts:
            if p.startswith('['):
                who = 'W' if 'ผู้หญิง' in p else ('G' if 'เจ้าบ่าว' in p else 'N'); continue
            p = p.replace('"', '').strip()
            if p:
                out.append((f'{n:02d}{"abc"[k]}', n, who, p)); k += 1
    return out

TAG = {'N': '', 'W': '[quietly] ', 'G': '[softly] '}

def tts(voice, text, stability):
    req = urllib.request.Request(f'{API}/text-to-speech/{voice}?output_format=mp3_44100_128',
                                 data=json.dumps({'text': text, 'model_id': 'eleven_v3', 'voice_settings': {'stability': stability}}).encode(),
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()

def stt(path):
    out = subprocess.run(['curl', '-s', '-X', 'POST', f'{API}/speech-to-text', '-F', 'model_id=scribe_v1', '-F', 'language_code=tha', '-F', f'file=@{path}'],
                         capture_output=True, text=True, timeout=180).stdout
    try:
        return json.loads(out).get('text')
    except Exception:
        return None

norm = lambda s: re.sub(r'[\s\.\?\!…,"\'“”]|\[[^\]]*\]', '', s or '')
report = {}
for key, n, who, text in lines():
    full = TAG[who] + text
    takes = []
    for take, stab in enumerate([0.5, 1.0], start=1):
        if used + len(full) > CEILING:
            print(f'STOP before {key}: would pass {CEILING} (used {used})'); break
        voice = VOICE[who]
        try:
            audio = tts(voice, full, stab)
        except urllib.error.HTTPError as e:
            msg = e.read()[:200]
            if who in FALLBACK and voice != FALLBACK[who]:
                print(f'{key}: voice {voice} failed ({e.code} {msg!r}), using fallback'); VOICE[who] = FALLBACK[who]
                audio = tts(VOICE[who], full, stab)
            else:
                raise
        used += len(full)
        path = os.path.join(HERE, 'vo', f'{key}_t{take}.mp3'); open(path, 'wb').write(audio)
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout or 0)
        heard = stt(path)
        score = difflib.SequenceMatcher(None, norm(text), norm(heard)).ratio() if heard else None
        takes.append(dict(path=os.path.basename(path), dur=round(dur, 2), score=score, heard=heard))
        print(f'{key} [{who}] take{take} {dur:.2f}s score={score} (credits {used})', flush=True)
        if score is None or score >= 0.85: break
    if takes:
        best = max(takes, key=lambda t: t['score'] or 0)
        report[key] = dict(shot=n, who=who, text=text, best=best, takes=takes, voice=VOICE[who])
    json.dump(dict(used=used, voices=VOICE, lines=report), open(os.path.join(HERE, 'vo', 'report.json'), 'w'), ensure_ascii=False, indent=1)
print('DONE credits used', used)
