# ปกตอนที่ 2: ถ้าวันนี้เป็นวันแต่งงานของคุณ (ภาพหลัก: เจ้าสาวหน้าตกใจฉากหน้า ผู้หญิงชุดดำยืนในกรอบประตูด้านหลัง ไม่เฉลยปม)
import base64
EP = {
    'episode': 'ตอนที่ 2',
    'title1': 'ถ้าวันนี้เป็นวัน',
    'title2_before': '', 'title2_hl': 'แต่งงาน', 'title2_after': 'ของคุณ',
    'rule': 'กฎข้อเดียว • อย่าให้เขาถอดแหวน',
}
_img = base64.b64encode(open('eps/ep2_wedding_art.jpg', 'rb').read()).decode()
ART = f'''
<rect width="540" height="960" fill="url(#bg)"/>
<image href="data:image/jpeg;base64,{_img}" width="540" height="960"/>
<ellipse cx="400" cy="640" rx="170" ry="260" fill="url(#halo)" style="mix-blend-mode:screen"/>
<rect width="540" height="520" fill="url(#topfade)"/>
<rect width="540" height="960" fill="url(#vig)"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".09" style="mix-blend-mode:screen"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".06" style="mix-blend-mode:overlay"/>
'''
