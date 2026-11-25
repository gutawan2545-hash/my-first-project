"""พากย์ใหม่แบบใส่อารมณ์ (ช่วงทดลอง ช็อต 3-6, 8, 9) ด้วยแท็กอารมณ์ของ eleven_v3 และจังหวะหยุด
คำพูดเหมือนบทเดิมทุกคำ เพิ่มแค่แท็กกับจุดไข่ปลาให้เว้นจังหวะ
เพดานรอบนี้ 560 เครดิต (ผู้ใช้อนุมัติรวม 2,200 ใช้ไปแล้ว 1,623)"""
import json, os, urllib.request
API = 'https://api.elevenlabs.io/v1'
VOICE = {'N': 'IM6pYHlwZQDuZqGBrSYI', 'W': 'XB0fDUnXU5powFXDhCwa'}
CEILING = 560
HERE = os.path.dirname(os.path.abspath(__file__))
LINES = [
    ('03e', 'N', '[warmly] คุณคบกับแฟนมาสามปี... เขาเป็นผู้ชายที่สมบูรณ์แบบ จนคุณไม่เคยคิดสงสัยอะไรในตัวเขาเลย', .35),
    ('04e', 'N', '[tense] จนกระทั่ง... ประตูห้องจัดเลี้ยงเปิดออก', .3),
    ('05e', 'N', '[nervous] ผู้หญิงคนหนึ่งในชุดเดรสสีดำเดินเข้ามา... [gasps] เธอสวมแหวนแต่งงานแบบเดียวกับคุณทุกประการ', .3),
    ('06e', 'W', '[cold] ขอโทษนะคะ... แต่ผู้ชายที่คุณกำลังจะแต่งงานด้วย... เป็นสามีของฉันค่ะ', .35),
    ('08e', 'N', '[quietly] ก่อนออกจากงาน... เธอหันมามองคุณ แล้วพูดเพียงประโยคเดียว', .35),
    ('09e', 'W', '[whispers urgently] คืนนี้... อย่าให้เขาถอดแหวนออกจากนิ้วคุณเด็ดขาด', .3),
]
used = 0; out = {}
for key, who, text, stab in LINES:
    if used + len(text) > CEILING:
        print('STOP before', key, 'used', used); break
    req = urllib.request.Request(f'{API}/text-to-speech/{VOICE[who]}?output_format=mp3_44100_128',
                                 data=json.dumps({'text': text, 'model_id': 'eleven_v3', 'voice_settings': {'stability': stab}}).encode(),
                                 headers={'Content-Type': 'application/json'})
    audio = urllib.request.urlopen(req, timeout=180).read()
    used += len(text)
    p = os.path.join(HERE, 'vo', f'{key}.mp3'); open(p, 'wb').write(audio)
    out[key] = dict(who=who, text=text, path=os.path.basename(p))
    print(key, who, 'credits', used, flush=True)
json.dump(dict(used=used, lines=out), open(os.path.join(HERE, 'vo', 'report_emotion.json'), 'w'), ensure_ascii=False, indent=1)
print('DONE', used)
