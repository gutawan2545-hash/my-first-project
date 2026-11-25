"""พากย์เจ้าบ่าวช็อต 7 ใหม่ให้มีอารมณ์: ลนลาน → หัวเราะกลบเกลื่อน → ตะคอกไล่ (ผู้ใช้อนุมัติ 400 เครดิต ลอง 3 แบบ)"""
import json, os, urllib.request
V = 'N2lVS1w4EtoT3dr4eOWO'
T = ('[panicked] เอ่อ... ทุกคนครับ! ใจเย็น ๆ ก่อนนะครับ [nervous laugh] ผู้หญิงคนนี้เป็นแฟนเก่าผมเอง เธอป่วยทางจิตครับ '
     '[shouting angrily] เจ้าหน้าที่! พาเธอออกไปเดี๋ยวนี้!')
TAKES = [('07g_t1', 0.0), ('07g_t2', 0.0), ('07g_t3', 0.5)]
used = 0
for key, stab in TAKES:
    if used + len(T) > 400: print('STOP', used); break
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{V}?output_format=mp3_44100_128',
        data=json.dumps({'text': T, 'model_id': 'eleven_v3', 'voice_settings': {'stability': stab}}).encode(), headers={'Content-Type': 'application/json'})
    open(f'vo/{key}.mp3', 'wb').write(urllib.request.urlopen(req, timeout=180).read()); used += len(T); print(key, used, flush=True)
