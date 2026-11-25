"""สร้างเสียงประกอบจริงด้วย ElevenLabs Sound Effects → sfx/NAME.mp3
ใช้เครดิต! รันได้เฉพาะเมื่อผู้ใช้อนุมัติเครดิตแล้ว: python3 gen_sfx.py --approved [ชื่อ ...]
ราคาโดยประมาณ ~40 เครดิตต่อวินาทีเมื่อกำหนดความยาว (ไฟล์ที่มีอยู่แล้วจะข้าม)"""
import os, sys, json, urllib.request

SFX = {  # ชื่อ: (คำบรรยาย, วินาที)
    'applause':   ('Polite warm applause from about 80 wedding guests in a large elegant hotel ballroom, natural room reverb, no cheering, no whistles', 4),
    'door_bang':  ('Heavy tall wooden double doors of a grand hotel ballroom thrown open and slamming hard against the walls, deep boom with long hall reverb', 2.5),
    'thunder':    ('Close loud thunder crack followed by a long deep rolling rumble, heard from inside a big building, cinematic, no rain', 6),
    'rain':       ('Steady heavy rain hitting tall glass windows, heard from inside a quiet luxury hall, soft and even, seamless loop', 10),
    'heels':      ('Slow confident high heel footsteps on a polished marble floor in a large quiet hall, one woman walking toward the listener, light reverb', 4),
    'guard_steps':('Firm quick men dress shoe footsteps on marble floor, security guard walking a few steps then stopping, indoor reverb', 2.5),
}

def gen(name, text, dur):
    out = os.path.join('sfx', name + '.mp3')
    if os.path.exists(out): print('skip', out); return 0
    body = json.dumps({'text': text, 'duration_seconds': dur, 'prompt_influence': 0.5}).encode()
    req = urllib.request.Request('https://api.elevenlabs.io/v1/sound-generation', data=body,
                                 headers={'Content-Type': 'application/json', 'xi-api-key': 'proxy-injected'})
    with urllib.request.urlopen(req, timeout=120) as r: open(out, 'wb').write(r.read())
    print('ok', out, f'~{int(dur * 40)} credits'); return dur * 40

if __name__ == '__main__':
    names = [a for a in sys.argv[1:] if not a.startswith('--')] or list(SFX)
    est = sum(SFX[n][1] * 40 for n in names)
    if '--approved' not in sys.argv:
        print(f'ยังไม่รัน: ประมาณ {est:.0f} เครดิต สำหรับ {names} · เพิ่ม --approved เมื่อผู้ใช้อนุมัติแล้ว'); sys.exit(0)
    os.makedirs('sfx', exist_ok=True)
    used = sum(gen(n, *SFX[n]) for n in names)
    print('ใช้ประมาณ', int(used), 'เครดิต')
