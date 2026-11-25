"""ผู้ใช้สั่งแก้บทช็อต 20 (เล่าเป็น "ฉัน") และ 21 (เบอร์ไม่ทราบชื่อโทรเข้ามา แล้วกลายเป็นเบอร์ผู้หญิงชุดดำ) ฉบับเดิม vo/20f_old.mp3, 21f_old.mp3"""
import json, urllib.request
V = 'IM6pYHlwZQDuZqGBrSYI'
L = [('20f', '[urgent] ตอนที่ฉันกำลังพยายามหนีออกจากโรงแรม... ลิฟต์กลับพาฉันมาอยู่ที่จุดเดิม ซ้ำแล้วซ้ำเล่า'),
     ('21f', '[tense] จู่ ๆ ก็มีเบอร์ไม่ทราบชื่อโทรเข้ามา... พอรับสาย ปรากฏว่าเป็นเบอร์ของผู้หญิงชุดดำ')]
used = 0
for k, t in L:
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{V}?output_format=mp3_44100_128',
        data=json.dumps({'text': t, 'model_id': 'eleven_v3', 'voice_settings': {'stability': .5}}).encode(), headers={'Content-Type': 'application/json'})
    open(f'vo/{k}.mp3', 'wb').write(urllib.request.urlopen(req, timeout=180).read()); used += len(t); print(k, used)
