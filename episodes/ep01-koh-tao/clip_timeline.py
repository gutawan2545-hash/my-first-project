"""EP.01 timeline: voice lines laid end to end with short breaths between them, plus subtitles.
All shot pages use this global clock, so subtitles and graphics stay continuous across cuts."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'vo', 'durations.json')))
FPS = 24

# (key | ('gap', seconds)); default breath between lines .2 s, quick exchanges .12 s
SEQ = ['N01', ('gap', .12), 'J01', ('gap', .45), 'N02', 'N03', 'J02', ('gap', 1.5), 'N04', 'U01', ('gap', .15), 'G01', ('gap', .3), 'J03',
       'N05', 'N06', 'N07', ('gap', 1.15), 'J04', 'N08', 'J05', ('gap', .1), 'S01', ('gap', .1), 'J06', 'N09', ('gap', .1), 'E01',
       'N10', 'N11', 'J07', ('gap', .12), 'F01', ('gap', .95), 'N12', ('gap', .35), 'N13', 'J08', 'N14', 'N15', ('gap', 3.6)]
QUICK = {'J01', 'S01', 'J06', 'E01', 'F01'}

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
    'N01': ('เห็นผู้ชายคนนี้มั้ย ชื่อเจม/ครูสอนดำน้ำบนเกาะเต่า/ขี่มอไซค์ขึ้นเนินมือเดียว ชิล ๆ', 'See this guy? That’s James,/a dive instructor on Koh Tao.'),
    'J01': ('ขอบคุณครับป้า!', 'Thanks, auntie!'),
    'N02': ('แต่เชื่อมั้ย สองปีก่อนนะ/หมอนี่ยังยืนผัดกะเพรา/อยู่หน้าเตาในกรุงเทพอยู่เลย', 'But believe it or not, two years ago/he was still stir-frying basil in Bangkok.'),
    'N03': ('เจมเป็นกรุงเทพเนทีฟแท้ ๆ/เป็นเชฟ วัน ๆ อยู่หน้าเตา/เลิกงานก็ไปอยู่บนถนน รถติดยาวไป', 'A born-and-raised Bangkokian chef:/all day at the stove, all night in traffic.'),
    'J02': ('พอกันที', 'I’m done.'),
    'N04': ('เกาะเต่าไม่มีสนามบินนะ/ย้ายบ้านทีก็ต้องขนทั้งชีวิตลงเรือ/พัดลม หม้อหุงข้าว กระทะ ไปหมด', 'No airport on Koh Tao, so a move means/your whole life goes on a boat.'),
    'U01': ('ส่งได้ถึงตีนเนินนะ/บันไดลุงไม่ขึ้น', 'I can drop you at the foot of the hill./I don’t do stairs.'),
    'G01': ('บ้านใกล้ท่าเรือครับ/ขึ้นไปนิดเดียว', 'It’s close to the pier./Just a little way up.'),
    'J03': ('นิดเดียว…/ของใครวะเนี่ย', 'A little way…/says who?!'),
    'N05': ('เกาะเล็กแค่ 21 ตารางกิโล/แต่เป็นเขาซะเยอะ/บ้านเลยชอบไปอยู่บนเนินกันหมด', 'Only about 21 km², mostly hills,/so the houses all sit up on slopes.'),
    'N06': ('คืนแรก…/ได้รูมเมทมาเองไม่ต้องหา', 'First night…/a roommate moved in for free.'),
    'N07': ('บนเกาะนะ/มอไซค์คือบีทีเอสของคุณ/ใส่หมวก แล้วค่อย ๆ หัดไป', 'On the island, a scooter is your BTS./Helmet on, and learn slowly.'),
    'J04': ('ป้าครับ…/สอนหน่อย', 'Auntie…/teach me?'),
    'N08': ('สั่งของออนไลน์ก็ได้/แต่ของต้องนั่งเรือมาเหมือนคุณ/คลื่นแรงเมื่อไหร่ เรืองด ของก็รอไป', 'You can shop online, but parcels ride the boat too./Rough sea, no boat, no parcel.'),
    'J05': ('พี่ครับ/ของผมถึงไหนแล้ว', 'Hi, where’s my parcel now?'),
    'S01': ('ยังอยู่ชุมพรครับ/วันนี้เรืองด', 'Still in Chumphon./No boats today.'),
    'J06': ('งั้นผมก็งดเหมือนกัน', 'Then I’m cancelled too.'),
    'N09': ('พายุเข้าที ไฟก็ดับได้/ไฟฉายเลยกลายเป็นของติดบ้าน', 'Storms can knock the power out,/so a torch lives in every house.'),
    'E01': ('เดี๋ยวก็มาครับ', 'It’ll come back.'),
    'N10': ('ของบางอย่างก็แพงกว่าฝั่งหน่อย/เพราะค่าเรือรวมอยู่ในนั้นแล้ว', 'Some things cost a bit more here:/the boat ride is in the price.'),
    'N11': ('เกาะเต่าดังเรื่องดำน้ำ/เพื่อนบ้านเลยมาจากทั่วโลก', 'Koh Tao is famous for diving,/so the neighbours come from everywhere.'),
    'J07': ('Hello! You…/eat rice already?', 'Hello! You… eat rice already?'),
    'F01': ('กินแล้วครับพี่เจม', 'Already ate, James.'),
    'N12': ('จากเชฟหน้าเตา/กลายเป็นครูพาคนดำลงไปดูปลา', 'From a chef at the stove/to a teacher taking people down to the fish.'),
    'N13': ('สองปีผ่านไป/จากคนที่เคยบ่นเรื่องรถติด/ตอนนี้บ่นเรื่องคลื่นแทน', 'Two years on: he used to moan about traffic,/now he moans about waves.'),
    'J08': ('วันนี้คลื่นแรง…/ของคงไม่มาอีกแล้ว', 'Rough sea today…/my parcel isn’t coming again.'),
    'N14': ('ชีวิตบนเกาะอาจไม่ได้สบายขึ้นทุกอย่าง/แต่มันจะไม่เหมือนเดิมอีกเลย', 'Island life isn’t easier in every way,/but it’s never the same again.'),
    'N15': ('แล้วคุณล่ะ/ถ้าต้องย้ายมาเป็นชาวเกาะ จะไหวมั้ย?', 'What about you?/Could you become an islander?'),
}

if __name__ == '__main__':
    for k, (a, b) in T.items():
        print(f'{k}  {a:6.2f} – {b:6.2f}')
    print('TOTAL', TOTAL)
