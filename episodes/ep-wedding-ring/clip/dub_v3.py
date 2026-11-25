"""พากย์รอบ 3: ผู้บรรยายมั่นใจขึ้น (ไม่ใช้แท็ก nervous/จุดไข่ปลาเยอะ) ประโยคเปิดตามถ้อยคำใหม่ของผู้ใช้
ช็อต 7 เปลี่ยนเป็นเจ้าบ่าวพูดเอง (ผู้ใช้สั่ง) · ผู้ใช้อนุมัติพากย์ราว 550 เครดิต"""
import json, os, urllib.request
API = 'https://api.elevenlabs.io/v1'
VOICE = {'N': 'IM6pYHlwZQDuZqGBrSYI', 'W': 'XB0fDUnXU5powFXDhCwa', 'G': 'N2lVS1w4EtoT3dr4eOWO'}
CEILING = 650
HERE = os.path.dirname(os.path.abspath(__file__))
LINES = [
    ('01c', 'N', '[confidently] ถ้าวันนี้เป็นวันแต่งงานของคุณ แต่ในขณะที่คุณกำลังจะสวมแหวนให้เจ้าบ่าว จู่ ๆ ก็มีผู้หญิงคนหนึ่งเดินเข้ามากลางงาน แล้วบอกว่าเธอคือภรรยาของผู้ชายที่คุณกำลังจะแต่งงานด้วย... คุณจะทำยังไงคะ?', .5),
    ('03c', 'N', '[warmly] คุณคบกับแฟนมาสามปี เขาเป็นผู้ชายที่สมบูรณ์แบบ จนคุณไม่เคยคิดสงสัยอะไรในตัวเขาเลย', .5),
    ('04c', 'N', '[dramatic] จนกระทั่ง... ประตูห้องจัดเลี้ยงเปิดออก', .5),
    ('05c', 'N', '[serious] ผู้หญิงคนหนึ่งในชุดเดรสสีดำเดินเข้ามา เธอสวมแหวนแต่งงาน แบบเดียวกับคุณทุกประการ', .5),
    ('07g', 'G', '[forced calm] ทุกคนครับ ใจเย็น ๆ นะครับ ผู้หญิงคนนี้เป็นแฟนเก่าของผมเอง เธอมีปัญหาทางจิต [sharply] เจ้าหน้าที่ครับ พาเธอออกไปที', .5),
    ('08c', 'N', '[calmly] ก่อนออกจากงาน เธอหันมามองคุณ แล้วพูดเพียงประโยคเดียว', .5),
]
used = 0; out = {}
for key, who, text, stab in LINES:
    if used + len(text) > CEILING: print('STOP before', key, 'used', used); break
    req = urllib.request.Request(f'{API}/text-to-speech/{VOICE[who]}?output_format=mp3_44100_128',
                                 data=json.dumps({'text': text, 'model_id': 'eleven_v3', 'voice_settings': {'stability': stab}}).encode(),
                                 headers={'Content-Type': 'application/json'})
    audio = urllib.request.urlopen(req, timeout=180).read(); used += len(text)
    open(os.path.join(HERE, 'vo', f'{key}.mp3'), 'wb').write(audio); out[key] = dict(who=who, text=text)
    print(key, who, 'credits', used, flush=True)
json.dump(dict(used=used, lines=out), open(os.path.join(HERE, 'vo', 'report_v3.json'), 'w'), ensure_ascii=False, indent=1)
print('DONE', used)
