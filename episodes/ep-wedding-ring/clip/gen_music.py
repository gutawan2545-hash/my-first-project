"""เพลงประกอบจริงด้วย ElevenLabs Music → music/A_wedding.mp3, music/B_thriller.mp3 (ผู้ใช้อนุมัติเพดาน 2,000 เครดิต)
ความยาวแต่ละท่อนคำนวณจากไทม์ไลน์ของคลิป (out/test_timeline.json) ให้เพลงเปลี่ยนตรงกับเหตุการณ์
รัน: python3 gen_music.py --approved [A] [B]"""
import json, os, sys, urllib.request, urllib.error
tl = json.load(open('out/test_timeline.json')); T0 = tl['t0']; bang = tl['bang']; END = tl['total']
NEG = ['vocals', 'singing', 'choir lyrics', 'drums kit', 'electronic beat', 'EDM', 'pop']
def sec(name, a, b, styles): return dict(section_name=name, positive_local_styles=styles, negative_local_styles=[], duration_ms=int(round((b - a) * 1000)), lines=[])
CUES = {
 'A_wedding': dict(positive_global_styles=['cinematic orchestral film score', 'instrumental', 'elegant', 'luxury hotel wedding'], negative_global_styles=NEG, sections=[
     sec('hook', 0, T0['s3'], ['soft solo piano with gentle strings', 'mysterious and intriguing', 'a hint of unease under the beauty', 'slow, sparse']),
     sec('wedding', T0['s3'], bang + 0.3, ['grand wedding processional', 'warm pipe organ with lush strings and harp', 'joyful, romantic, majestic', 'major key']),
 ]),
 'B_thriller': dict(positive_global_styles=['dark cinematic horror thriller score', 'instrumental', 'orchestral', 'eerie, elegant, suspenseful'], negative_global_styles=NEG, sections=[
     sec('intrusion', bang + 1.4, T0['s6'], ['eerie detuned music box melody', 'low sustained cello drone', 'slow, cold, mysterious']),
     sec('her words', T0['s6'], T0['s7a'], ['tremolo strings', 'soft heartbeat-like low pulse', 'creeping tension building']),
     sec('confrontation', T0['s7a'], T0['s9'], ['urgent driving staccato strings ostinato', 'timpani hits', 'rising tension, faster']),
     sec('warning', T0['s9'], T0['s9r'] - .5, ['sudden drop to near silence', 'high thin sustained violin', 'low ominous piano notes', 'chilling']),
     sec('dread', T0['s9r'] - .5, END + .5, ['dissonant orchestral swell rising to a sharp cutoff', 'horror']),
 ]),
}
if os.path.exists('out/full_timeline.json'):
    F = json.load(open('out/full_timeline.json'))['t0']
    CUES['C_night'] = dict(positive_global_styles=['dark cinematic horror mystery score', 'instrumental', 'orchestral', 'eerie and elegant'], negative_global_styles=NEG, sections=[
        sec('unease', F['s10'], F['s15'], ['quiet uneasy suspense', 'soft pizzicato strings and low cello', 'curious, something is wrong']),
        sec('searching', F['s15'], F['s17'], ['tense ticking pulse', 'muted piano notes', 'secretive investigation']),
        sec('revelation', F['s17'], F['s18'], ['heavy dark orchestral hit then a low ominous drone']),
        sec('missing', F['s18'], F['s20'], ['rising dread', 'dissonant strings slowly swelling', 'ends with a deep hit']),
        sec('trapped', F['s20'], F['s22'], ['claustrophobic repeating eerie motif', 'pulsing low strings', 'panic underneath']),
        sec('the call', F['s22'], F['s24'], ['hushed and haunting', 'sparse piano and breathy high strings', 'sad and cold']),
        sec('knocking', F['s24'], F['s26'], ['near silence', 'very low sub drone', 'unbearable tension']),
        sec('terror', F['s26'], F['s27'] + .4, ['high violin cluster swelling', 'sharp cutoff']),
    ])
if __name__ == '__main__':
    names = [a for a in sys.argv[1:] if not a.startswith('--')] or list(CUES)
    for n in names:
        print(n, [(s['section_name'], s['duration_ms']) for s in CUES[n]['sections']])
    if '--approved' not in sys.argv: print('ยังไม่รัน (เพิ่ม --approved)'); sys.exit(0)
    os.makedirs('music', exist_ok=True)
    for n in names:
        body = json.dumps({'composition_plan': CUES[n], 'model_id': 'music_v1', 'respect_sections_durations': True}).encode()
        req = urllib.request.Request('https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128', data=body, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                open(f'music/{n}.mp3', 'wb').write(r.read())
                print('ok', n, {k: v for k, v in r.headers.items() if 'cost' in k.lower() or 'character' in k.lower() or 'credit' in k.lower()})
        except urllib.error.HTTPError as e:
            print('ERR', n, e.code, e.read()[:600].decode(errors='ignore'))
