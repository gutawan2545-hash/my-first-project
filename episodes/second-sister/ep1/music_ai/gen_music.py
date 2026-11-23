"""Five 30 s ElevenLabs Music cues for EP1 (user ceiling for music: 3,000 credits; the API reports no cost, so kept small).
The two earlier tests are reused: test_night.mp3 (eerie) and test_chant.mp3 (sacred chant)."""
import json, urllib.request, os, sys
BASE = ["Gregorian-flavoured sacred horror score", "convent chapel", "women's choir chanting softly in Latin", "pipe organ", "stone church reverb"]
CUES = {
 "calm":      "Gentle, warm daytime convent music: soft pipe organ chords, slow tender piano melody, distant women's choir humming a hymn, peaceful but with a faint melancholy, light and airy, no drums",
 "memory":    "Sad nostalgic memory cue: lonely solo piano lullaby with music box doubling, soft women's choir 'ah' far away, slow, fragile, tearful, organ pad underneath, no drums",
 "tension":   "Creeping horror tension: low cello and bass drone, pulsing heartbeat-like low organ pedal, whispered Latin chant fragments, dissonant high strings slowly rising, suspense building, no melody, no drums kit",
 "aftermath": "Grim aftermath after a death at a convent: slow funeral dirge, low male and female choir chanting a requiem, deep organ, very sparse, solemn and cold, no drums",
 "ending":    "Mysterious cliffhanger ending: solemn Latin chant motif by women's choir building slowly with pipe organ and strings into an unresolved haunting chord, cinematic, no drums",
}
for name, prompt in CUES.items():
    out = f"{name}.mp3"
    if os.path.exists(out): continue
    body = {"prompt": prompt + ". Style: " + ", ".join(BASE) + ". Instrumental only, no lyrics in Thai or English.", "music_length_ms": 30000, "model_id": "music_v1"}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: open(out, "wb").write(r.read())
        print("ok", name, flush=True)
    except urllib.error.HTTPError as e:
        print("FAIL", name, e.code, e.read()[:300]); sys.exit(1)
