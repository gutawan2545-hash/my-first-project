"""ซับไทย + อังกฤษแบบขึ้นทีละช่วงตามเสียงพูด ตามมาตรฐานช่อง:
ไทยตัวหนาสีเหลือง #ffd84a ขอบเข้ม ไม่เกิน 4 บรรทัด (ใช้ช่วงละไม่เกิน 2 บรรทัดให้อ่านทัน) ขนาด 20 ในเฟรม 540
อังกฤษ Inter สีขาว ขอบเข้ม ขนาด 13 ไม่เกิน 3 บรรทัด จัดกลางที่ราว y 712
รัน: python3 subs.py -> subs/chunks.json + subs.html แล้ว node render_subs.js -> subs/NNN.png"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, 'subs'), exist_ok=True)

EN = {
 1: "If today were your wedding day, and just as you were about to put the ring on the groom, a woman walked in and said she was his wife, what would you do?",
 2: "A wedding at a luxury hotel. White flowers along the aisle, a glittering chandelier, every guest applauding the couple.",
 3: "You'd been together three years. He was so perfect you never once doubted him.",
 4: "Until the ballroom doors swung open.",
 5: "A woman in a black dress walked in, wearing a wedding ring exactly like yours.",
 6: "I'm sorry, but the man you're about to marry... is my husband.",
 7: "The groom told everyone she was an ex with mental health problems, and had security take her away.",
 8: "Before she left, she turned to you and said just one thing.",
 9: "Tonight, don't let him take the ring off your finger. No matter what.",
 10: "The wedding went on, but you started noticing things.",
 11: "Almost no one on the groom's side took a single photo.",
 12: "His mother called you by the wrong name. Twice.",
 13: "The photographer let slip: this year looks better than last time.",
 14: "The hotel staff looked at you with pity.",
 15: "While he was seeing the guests off, you went through his phone.",
 16: "You found wedding albums going back years. Same hotel, same flowers, same groom. Never the same bride.",
 17: "And the woman in black was last year's bride.",
 18: "You searched each bride's name online.",
 19: "Every one of them was reported missing, just one day after the wedding.",
 20: "When you tried to run, the elevator kept bringing you back to the same floor.",
 21: "Your phone rang. It was the woman in black.",
 22: "He isn't my husband... I was just a bride, like you.",
 23: "And if you want to live, you have to find the next woman to marry him instead.",
 24: "Three knocks at the door.",
 25: "Darling, open the door. It's time to take off the ring.",
}

def thai_lines(text, n=22):
    """ตัดบรรทัดตรงรอยต่อของคำ (ใช้ตัวตัดคำภาษาไทย) ไม่ตัดกลางคำ"""
    from pythainlp.tokenize import word_tokenize
    toks = word_tokenize(text, engine='newmm', keep_whitespace=True)
    lines = []; cur = ''
    for t in toks:
        if t.isspace():
            if cur and len(cur) >= n * .7: lines.append(cur); cur = ''
            elif cur: cur += ' '
            continue
        if cur and len(cur.rstrip()) + len(t) > n:
            lines.append(cur.rstrip()); cur = t
        else:
            cur += t
    if cur.strip(): lines.append(cur.strip())
    return lines

def chunks_for(th, en):
    ls = thai_lines(th)
    groups = [ls[i:i + 2] for i in range(0, len(ls), 2)]
    if len(groups) > 1 and len(groups[-1]) == 1 and len(''.join(groups[-1])) < 8:
        last = groups.pop(); groups[-1] += last
    # แบ่งอังกฤษตามสัดส่วนตัวอักษรไทย
    words = en.split(' '); total = sum(len(''.join(g)) for g in groups); out = []; wi = 0; acc = 0
    for gi, g in enumerate(groups):
        acc += len(''.join(g))
        upto = len(words) if gi == len(groups) - 1 else round(len(words) * acc / total)
        out.append(dict(th=g, en=' '.join(words[wi:upto]), w=len(''.join(g)))); wi = upto
    return out

def main():
    rep = json.load(open(os.path.join(HERE, 'vo', 'report.json')))['lines']
    data = {}
    for key, d in rep.items():
        data[d['shot']] = chunks_for(d['text'], EN[d['shot']])
    json.dump(data, open(os.path.join(HERE, 'subs', 'chunks.json'), 'w'), ensure_ascii=False, indent=1)
    svgs = []
    for n, chs in sorted(data.items()):
        for k, c in enumerate(chs):
            th = c['th']; en_lines = []
            cur = ''
            for w in c['en'].split(' '):
                if len(cur) + len(w) + 1 > 46 and cur: en_lines.append(cur); cur = w
                else: cur = (cur + ' ' + w).strip()
            if cur: en_lines.append(cur)
            en_lines = en_lines[:3]
            lh_t, lh_e = 27, 17
            block = len(th) * lh_t + 6 + len(en_lines) * lh_e
            y0 = 712 - block / 2 + 20
            t = ''.join(f'<text x="270" y="{y0 + i * lh_t:.0f}" class="th">{l}</text>' for i, l in enumerate(th))
            ye = y0 + (len(th) - 1) * lh_t + 6 + lh_e
            e = ''.join(f'<text x="270" y="{ye + i * lh_e:.0f}" class="en">{l.replace("&", "&amp;")}</text>' for i, l in enumerate(en_lines))
            svgs.append(f'<svg id="s{n:02d}_{k}" viewBox="0 0 540 960" width="540" height="960" xmlns="http://www.w3.org/2000/svg">{t}{e}</svg>')
    html = ('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@700&family=Inter:wght@600&display=swap">'
            '<style>html,body{margin:0;background:transparent}svg{display:block}'
            '.th{font-family:"IBM Plex Sans Thai";font-weight:700;font-size:20px;fill:#ffd84a;stroke:#1a1410;stroke-width:5px;paint-order:stroke;stroke-linejoin:round;text-anchor:middle}'
            '.en{font-family:Inter,sans-serif;font-weight:600;font-size:13px;fill:#ffffff;stroke:#14121a;stroke-width:3.4px;paint-order:stroke;stroke-linejoin:round;text-anchor:middle}</style>'
            + ''.join(svgs))
    open(os.path.join(HERE, 'subs.html'), 'w').write(html)
    print('chunks', sum(len(v) for v in data.values()))

if __name__ == '__main__':
    main()
