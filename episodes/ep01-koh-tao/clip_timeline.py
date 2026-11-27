"""EP.01 timeline: voice lines laid end to end with short breaths between them, plus subtitles.
All shot pages use this global clock, so subtitles and graphics stay continuous across cuts."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'vo', 'durations.json')))
FPS = 24

# (key | ('gap', seconds)); default breath between lines .2 s, quick exchanges .12 s
SEQ = ['N01', ('gap', .15), 'J01', ('gap', .6), 'N02', 'N03', ('gap', .3), 'J02', ('gap', 1.6),
       'N04', ('gap', .9), 'U01', ('gap', .2), 'G01', ('gap', .3), 'J03', ('gap', .8),
       'N05', ('gap', 1.0), 'N06', ('gap', .6), 'N07', ('gap', 1.15), 'J04', ('gap', .8), 'N08', ('gap', .9), 'J05', ('gap', .1), 'S01', ('gap', .15), 'J06', ('gap', .9),
       'N09', ('gap', .1), 'E01', ('gap', .5), 'N10', ('gap', 1.0), 'N11', ('gap', .9), 'J07', ('gap', .2), 'F01', ('gap', 1.25), 'N11b', ('gap', .9),
       'N12', ('gap', .45), 'N13', 'J08', ('gap', .5), 'N14', 'N15', ('gap', 3.6)]
QUICK = {'J01', 'S01', 'J06', 'E01', 'F01', 'N11b'}

T = {}
t = .15
for i, k in enumerate(SEQ):
    if isinstance(k, tuple):
        t += k[1]
        continue
    if T and not (isinstance(SEQ[i - 1], tuple)):
        t += .12 if k in QUICK else .2
    T[k] = (round(t, 3), round(t + D[k], 3))
    t += D[k]
TOTAL = round(t, 2)


def at(key, frac=0.0):
    a, b = T[key]
    return round(a + (b - a) * frac, 3)


WHO = {k: ('narrator' if k[0] == 'N' else {'J': 'james', 'G': 'agent', 'U': 'uncle', 'S': 'staff', 'E': 'electrician', 'F': 'neighbor'}[k[0]]) for k in T}

SUB = {
    'N01': ('เห็นไอ้หนุ่มเสื้อลายดอกนี่ปะ/นี่ไอ้เจม ครูสอนดำน้ำที่เกาะเต่า/ขี่มอไซค์ขึ้นเนินมือเดียว อีกมือถือกาแฟ/เท่อะ', 'See the guy in the flower shirt? That’s James,/a dive instructor on Koh Tao. Coffee in one hand.'),
    'J01': ('ขอบคุณครับป้า!', 'Thanks, auntie!'),
    'N02': ('แต่รู้ปะ สองปีก่อนเนี่ย/มันยังยืนผัดกะเพรา/อยู่ในครัวที่กรุงเทพฯ อยู่เลย', 'But two years ago he was still/stir-frying basil in a Bangkok kitchen.'),
    'N03': ('ไอ้เจมมันกรุงเทพเนทีฟของแท้/ทั้งวันยืนหน้าเตา/เลิกงานก็ไปจมอยู่ในรถติด/วนอยู่อย่างนี้ทุกวัน', 'A true Bangkok kid: all day at the stove,/all evening stuck in traffic. Every day.'),
    'J02': ('พอแล้ว…/ไม่ไหวแล้ว', 'That’s it…/I’m done.'),
    'N04': ('แล้วมันก็ย้ายไปเกาะเต่าจริง ๆ นะ/แต่เกาะเต่าไม่มีสนามบินไง/ของทั้งบ้านก็ต้องขนลงเรือ/ตั้งแต่พัดลม หม้อหุงข้าว ยันกระทะคู่ใจ', 'So he really moved. No airport on Koh Tao,/so the whole house went on a boat, down to his wok.'),
    'U01': ('ลุงไปส่งได้แค่ตีนเนินนะ/ข้างบนนั่นบันได รถขึ้นไม่ได้', 'I can only drop you at the foot of the hill./It’s stairs up there, no cars.'),
    'G01': ('ใกล้ท่าเรือครับพี่/เดินขึ้นไปแป๊บเดียวเอง', 'It’s close to the pier./Just a quick walk up.'),
    'J03': ('แป๊บเดียว…/แป๊บเดียวของใครวะเนี่ย', 'A quick walk…/quick for who?!'),
    'N05': ('เกาะเต่าเล็กแค่ประมาณ 21 ตารางกิโลฯ/แต่เป็นภูเขาซะเยอะ/บ้านก็เลยไปอยู่บนเนินกันหมด', 'Koh Tao is only about 21 km², mostly hills,/so the houses all sit up on slopes.'),
    'N06': ('คืนแรก…/มีรูมเมทมาอยู่ด้วยแล้ว ไม่ต้องหาเลย', 'First night…/a roommate moved in for free.'),
    'N07': ('อยู่เกาะต้องขี่มอไซค์เป็นนะ/มันคือรถไฟฟ้าของที่นี่เลย/ใส่หมวกแล้วค่อย ๆ หัดไป', 'On the island you ride a scooter:/it’s the local train. Helmet on, learn slowly.'),
    'J04': ('ป้า…/สอนผมหน่อยได้มั้ยครับ', 'Auntie…/could you teach me?'),
    'N08': ('สั่งของออนไลน์ก็ได้นะ/แต่ของก็ต้องนั่งเรือมาเหมือนกัน/วันไหนคลื่นแรง เรืองด ก็รอไปเถอะ', 'You can shop online, but parcels ride the boat too./Rough sea, no boat: just wait.'),
    'J05': ('ฮัลโหลพี่/ของผมถึงไหนแล้วครับ', 'Hello? Where’s my parcel now?'),
    'S01': ('ยังอยู่ชุมพรเลยครับ/วันนี้เรือไม่วิ่ง', 'Still in Chumphon./The boat isn’t running today.'),
    'J06': ('งั้นวันนี้ผมก็ไม่วิ่งเหมือนกันครับ', 'Then I’m not running today either.'),
    'N09': ('พายุเข้าที ไฟก็ดับบ้าง/ไฟฉายเลยต้องมีติดบ้านไว้ตลอด', 'Storms knock the power out sometimes,/so every house keeps a torch.'),
    'E01': ('เดี๋ยวก็มาครับพี่/ใจเย็น ๆ', 'It’ll come back, bro./Relax.'),
    'N10': ('ของบางอย่างก็แพงกว่าฝั่งหน่อย/ค่าเรือมันรวมอยู่ในนั้นแล้วไง', 'Some things cost a bit more:/the boat ride is in the price.'),
    'N11': ('เกาะเต่าดังเรื่องดำน้ำ/เพื่อนบ้านก็เลยมาจากทั่วโลก', 'Koh Tao is famous for diving,/so the neighbours come from everywhere.'),
    'J07': ('Hello! You…/eat rice… already?', 'Hello! You… eat rice… already?'),
    'F01': ('กินแล้วครับพี่เจม/วันนี้กินข้าวมันไก่', 'Already ate, James./Chicken rice today.'),
    'N11b': ('…ไทยชัดกว่ามันอีก', '…his Thai is better than James’s.'),
    'N12': ('จากเชฟหน้าเตา/กลายเป็นครูพาคนดำลงไปดูปลา', 'From a chef at the stove/to a teacher taking people down to the fish.'),
    'N13': ('สองปีผ่านไป/จากคนที่เคยบ่นเรื่องรถติด/ตอนนี้มาบ่นเรื่องคลื่นแทน', 'Two years on: he used to moan about traffic,/now he moans about waves.'),
    'J08': ('วันนี้คลื่นแรงอีกแล้ว…/ของไม่มาอีกแน่เลย', 'Rough sea again…/my parcel isn’t coming.'),
    'N14': ('ชีวิตบนเกาะมันไม่ได้ง่ายไปหมดทุกอย่างหรอก/แต่มันก็ไม่มีวันเหมือนเดิมอีกแล้ว', 'Island life isn’t easier in every way,/but it’s never the same again.'),
    'N15': ('แล้วถ้าเป็นคุณล่ะ…/ย้ายมาเป็นชาวเกาะ ไหวมั้ย?', 'And you?/Could you become an islander?'),
}

if __name__ == '__main__':
    for k, (a, b) in T.items():
        print(f'{k}  {a:6.2f} – {b:6.2f}')
    print('TOTAL', TOTAL)
