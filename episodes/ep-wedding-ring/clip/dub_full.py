"""พากย์ช็อต 2 และ 10-25 ใหม่แบบมีอารมณ์ (ผู้ใช้อนุมัติราว 1,000 เครดิต) ผู้บรรยายมั่นใจ ไม่แอ็กติ้งเกิน
ผู้หญิงชุดดำทางโทรศัพท์ เศร้าแล้วเย็นชา · เจ้าบ่าวหลังประตู หวานแต่น่ากลัว"""
import json, os, urllib.request
VOICE = {'N': 'IM6pYHlwZQDuZqGBrSYI', 'W': 'XB0fDUnXU5powFXDhCwa', 'G': 'N2lVS1w4EtoT3dr4eOWO'}
CEILING = 1000
L = [
 ('10f', 'N', '[serious] งานแต่งดำเนินต่อไป... แต่คุณเริ่มสังเกตเห็นความผิดปกติ', .5),
 ('11f', 'N', 'แขกฝั่งเจ้าบ่าว แทบไม่มีใครถ่ายรูปเลย', .5),
 ('12f', 'N', 'แม่ของเจ้าบ่าว เรียกคุณผิดชื่อถึงสองครั้ง', .5),
 ('13f', 'N', '[tense] ช่างภาพเผลอพูดว่า... ปีนี้จัดงานสวยกว่าครั้งที่แล้ว', .5),
 ('14f', 'N', 'พนักงานโรงแรมมองคุณ ด้วยสายตาสงสาร', .5),
 ('15f', 'N', '[low voice] คุณแอบค้นโทรศัพท์ของเจ้าบ่าว ระหว่างที่เขาออกไปส่งแขก', .5),
 ('16f', 'N', '[serious] คุณพบอัลบั้มภาพงานแต่งงานย้อนหลังหลายปี ทุกงานจัดในโรงแรมเดียวกัน ใช้ดอกไม้แบบเดียวกัน เจ้าบ่าวคนเดียวกัน... แต่เจ้าสาวไม่เคยซ้ำหน้า', .5),
 ('17f', 'N', '[dramatic] และผู้หญิงชุดดำที่เดินเข้ามาในงาน... คือเจ้าสาวของปีที่แล้ว', .5),
 ('18f', 'N', 'คุณลองค้นชื่อเจ้าสาวแต่ละคนบนอินเทอร์เน็ต', .5),
 ('19f', 'N', '[grave] ทุกคน... มีประกาศตามหาคนหาย หลังจากวันแต่งงานเพียงหนึ่งวัน', .5),
 ('20f', 'N', '[urgent] เมื่อคุณพยายามหนีออกจากโรงแรม ลิฟต์กลับพาคุณมาที่ชั้นเดิม ซ้ำแล้วซ้ำเล่า', .5),
 ('21f', 'N', '[tense] โทรศัพท์ดังขึ้น... เป็นเบอร์ของผู้หญิงชุดดำ', .5),
 ('22f', 'W', '[sadly] มันไม่ใช่สามีของฉันหรอกค่ะ... ฉันแค่เคยเป็นเจ้าสาวเหมือนคุณ', .5),
 ('23f', 'W', '[coldly] แล้วถ้าคุณอยากรอด... คุณต้องหาผู้หญิงคนต่อไป มาแต่งงานกับมันแทน', .5),
 ('24f', 'N', 'เสียงเคาะประตูดังขึ้นสามครั้ง', .5),
 ('25f', 'G', '[sweetly] ที่รัก... เปิดประตูให้ผมหน่อย [menacing whisper] ถึงเวลาถอดแหวนแล้วครับ', .0),
]
tot = sum(len(t) for _, _, t, _ in L); print('total chars', tot)
if tot > CEILING: raise SystemExit('over ceiling')
used = 0; out = {}
for key, who, text, stab in L:
    p = f'vo/{key}.mp3'
    if os.path.exists(p): continue
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE[who]}?output_format=mp3_44100_128',
        data=json.dumps({'text': text, 'model_id': 'eleven_v3', 'voice_settings': {'stability': stab}}).encode(), headers={'Content-Type': 'application/json'})
    open(p, 'wb').write(urllib.request.urlopen(req, timeout=180).read()); used += len(text); out[key] = dict(who=who, text=text); print(key, used, flush=True)
json.dump(dict(used=used, lines=out), open('vo/report_full.json', 'w'), ensure_ascii=False, indent=1)
print('DONE', used)
