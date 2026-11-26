"""EP.01 realistic sound effects via ElevenLabs sound generation (owner approved ~950 credits)."""
import json, os, urllib.request, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SFX = {
    'birds_beach': ('Tropical island morning ambience, gentle waves on a sandy beach, birds chirping in palm trees, light breeze, realistic field recording', 6),
    'waves_rough': ('Big ocean waves crashing hard on granite rocks, strong wind, spray, stormy sea, realistic', 6),
    'scooter_pass': ('A small 125cc motor scooter passing by quickly from left to right, engine buzz with doppler, realistic', 3),
    'thunder': ('Deep rolling thunder clap in a tropical storm, distant rumble, realistic', 5),
    'rain_roof': ('Heavy tropical rain falling on a tin roof and leaves at night, realistic ambience', 6),
    'gecko': ('Tokay gecko calling at night, the classic tokeh tokeh call, two croaks, realistic', 3),
    'wok_sizzle': ('Busy restaurant kitchen, wok stir frying with loud sizzle and metal spatula clanks, gas burner roar', 5),
    'bkk_traffic': ('Bangkok traffic jam at night heard from inside a taxi, idling engines, distant car horns, muffled', 5),
    'harbor': ('Busy tropical island pier, ferry horn in the distance, water lapping on wooden pier, seagulls, people', 6),
    'night_insects': ('Tropical night ambience, crickets and insects, very soft distant sea, quiet', 6),
    'whoosh': ('Fast cinematic whoosh transition, airy swoosh', 2),
}
for k, (prompt, d) in SFX.items():
    mp3 = os.path.join(H, 'sfx', k + '.mp3')
    if os.path.exists(mp3):
        continue
    body = json.dumps({'text': prompt, 'duration_seconds': d, 'prompt_influence': 0.5}).encode()
    req = urllib.request.Request('https://api.elevenlabs.io/v1/sound-generation', data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=180) as r:
        open(mp3, 'wb').write(r.read())
    print(k, flush=True)
for k in SFX:
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(H, 'sfx', k + '.mp3'), '-ac', '1', '-ar', '48000', os.path.join(H, 'sfx', k + '.wav')], check=True)
