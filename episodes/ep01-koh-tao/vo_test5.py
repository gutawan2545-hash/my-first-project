"""Script v5 voice test: narrator line N01 two ways (owner picks). Ceiling 300 credits."""
import json, os, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
API = 'https://api.elevenlabs.io/v1'
V = 'yq05eeRaHPMGuWTVpqeP'   # Tonce
TESTS = {
    'A_creative': ('[chuckles] เห็นไอ้หนุ่มเสื้อลายดอกนี่ปะ… นี่ไอ้เจม ครูสอนดำน้ำที่เกาะเต่า ขี่มอไซค์ขึ้นเนินมือเดียว อีกมือถือกาแฟ… เท่อะ', 0.0),
    'B_directed': ('[chuckles] เห็นไอ้หนุ่มเสื้อลายดอกนี่ปะ… [pause] นี่แหละ ไอ้เจม ครูสอนดำน้ำที่เกาะเต่า [excited] ขี่มอไซค์ขึ้นเนินมือเดียว อีกมือถือกาแฟ… [laughs] เท่อะ', 0.5),
}
used = 0
for name, (text, stab) in TESTS.items():
    used += len(text)
    assert used <= 300
    body = json.dumps({'text': text, 'model_id': 'eleven_v3', 'voice_settings': {'stability': stab}}).encode()
    req = urllib.request.Request(f'{API}/text-to-speech/{V}?output_format=mp3_44100_128', data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=180) as r:
        open(os.path.join(H, 'vo_test5', name + '.mp3'), 'wb').write(r.read())
    print(name, len(text))
print('chars', used)
