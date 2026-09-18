---
description: "Write a short video script (a Reel, a TikTok, a Short, a video ad) and, when there is no footage, assemble a slideshow cut from statics with captions: the hook in the first three seconds, the structure by beats, the on-screen text rules, five to eight hook variants per body. Use when the owner says make a video, a Reel, a TikTok, a script, a 15-second ad, or when the brief lists video."
---

# Video script

A video is a hook, a promise kept by second six, a re-hook every five to
fifteen seconds, and a call to action said word for word. The middle is
beats, not prose. `references/hooks.md` holds the hook classes with
examples, the ten structures with 15 s and 30 s beat timings, the
on-screen text rules, the metrics and what to change when each is low.
Read the structure you are using and the hook section, not the file.

## The record

One creative (`--kind video`) with `script.md` beside `creative.md`:

```
creatives/generated/<id>/
  creative.md      kind: video; copy.caption (organic) or copy.primary_text (ad); claims; files
  script.md        the script (below)
  slides/          when it is a slideshow cut: the frames, rendered like carousel cards
  cut.mp4          when assembled here (scripts/video.py)
```

`script.md`:

```markdown
---
type: script
length: 15                     # seconds
structure: problem-solution    # from references/hooks.md
hooks:                         # the five to eight openers to test, word for word
  - "Six weeks of 'someone will be in touch'."
  - "Who fits the kitchen you were sold?"
cta: "Book a workshop visit. Link in bio."   # word for word
---

| t (s) | on screen (text)                 | spoken / sound                          | picture (beat)                          |
|------:|----------------------------------|-----------------------------------------|-----------------------------------------|
| 0–3   | Six weeks of "someone will be in touch" | the hook, spoken                    | the empty room, phone in hand           |
| 3–6   | We measure. We draw. We build.   | one line on the mechanism               | the workshop bench, hands               |
| …     |                                  |                                         |                                         |
| 12–15 | Book a workshop visit            | the cta, spoken                         | the finished kitchen, wide              |
```

Five to ten words a second of on-screen text; the keyword phrase on
screen in the first second and spoken; captions on; the words inside the
9:16 safe zone (`specs/README.md`).

## Where the pictures come from

There are exactly three sources of moving pictures, and the first is the
best:

1. **The owner's own footage**, in `media/clips` (`sources` skill: the
   owner uploads it, or mirrors it from a brain or website in the
   project). `python3 scripts/media.py --clips` lists what is there, how
   long each one is, and which have a consent note.
2. **The app's own cards**: the branded stills it renders for any
   creative, held with a slow push. This is what an app with no footage
   can make on its own, and it is honest: a card is not pretending to be
   film.
3. **A generated clip**, four to eight seconds, only when a provider is
   connected and only for a beat that needs motion.

`scripts/video.py` cuts all three into one file. The edit list is
`shots.json` beside the creative, in order:

```json
[{"slide": "slides/01.png", "seconds": 2},
 {"clip": "media/clips/bench.mp4", "in": 4.0, "out": 7.5},
 {"clip": "clip-02.mp4", "in": 0, "out": 5, "mute": true},
 {"slide": "slides/04.png", "seconds": 2.5}]
```

Footage is trimmed to its `in` and `out`, then scaled and centre-cropped
to the ratio, so landscape phone video becomes a vertical cut without
letterboxing (check the crop: what matters must be near the middle).
Without a `shots.json` it falls back to a slideshow of every card.

```bash
python3 scripts/media.py --clips                    # what footage exists
python3 scripts/captions.py --script <id>/script.md --out <id>/caps.ass
python3 scripts/video.py <id> --captions            # the cut
```

## Which kind of video this business can make

- **Talking head**: the owner on a phone, one take, the script's hook and
  cta read word for word, the middle from memory. Best for trust; needs
  the owner's face and ten minutes.
- **B-roll with voice**: the owner's clips of the work, with the script
  spoken over them. When there are none and a beat needs motion (the
  workshop at work, a road at dawn), a video model can make four to eight
  seconds of it:

  ```bash
  python3 scripts/videogen.py --check
  python3 scripts/videogen.py --ratio 9:16 --seconds 6 --out creatives/generated/<id>/clip-02.mp4 \
    --prompt "<the same six-part shape as a picture: subject and moment, camera, environment and light, what stays empty, mood as visible properties, what to show instead>" \
    [--ref creatives/generated/<id>/slides/02.png]
  ```

  It goes through OpenRouter (Veo, Seedance, Wan and others on the one
  key the app may already have for images) or fal; with no key, ask once:
  `request_connection("openrouter", why="a few seconds of generated video
  behind the script", auth="api_key", delivery="machine")`. A clip is
  worth it for one or two beats of a cut, never for a whole video; the
  words stay in the captions, and the owner's real footage, when it
  arrives, replaces it.

  **Say the price before generating.** Generated video is charged by the
  second and usually takes three to five attempts to land, so quote the
  range: the cheap models are around five cents a second (a 30-second cut
  is a pound or two of model spend), the mid tier around six to twelve
  cents, and Veo with its own generated audio is 40 cents a second, which
  is about £12 for 30 seconds before retries. A slideshow with captions
  costs nothing but the machine's time, and for most small businesses it
  is the right answer until they ask for more.

## The other things a video needs, and where they come from

- **A voice.** The owner reading the script on a phone is best and free.
  Failing that, a text-to-speech connection (ElevenLabs is the common
  one; note that its free tier carries no commercial licence, so an ad
  needs a paid tier). Ask with `request_connection` and say why.
- **Footage the business does not have.** Stock video from Pexels or
  Pixabay is free, needs no attribution, and its licence permits ads;
  neither carries model releases, so no recognisable person should carry
  a claim about them. Say in the notes when a shot is stock.
- **A face.** Avatar video (a synthetic presenter reading the script) is
  a paid product with its own API and its own consent rules. It is not
  part of this app; if the owner wants it, say so plainly and let them
  decide, because a synthetic presenter for a local business usually
  reads as less trustworthy than the owner's own phone video.
- **A cut of the owner's footage**: their clips in `media/clips`, trimmed
  to the script's beats in `shots.json`, with the captions over them.
  This is the real thing, and it is what to ask for first: "film these
  four shots on your phone, ten seconds each, landscape or upright,
  whichever is easier".
- **Slideshow cut**: when there is no footage at all. Four to six cards
  (the hook, the beats, the cta) with a slow push and the captions burnt
  in. Honest and quick; not a substitute for the owner's own footage, and
  the record's notes say so.

## Captions, always

Most feeds autoplay muted, so the words on screen are the ad, not a
courtesy. `scripts/captions.py` writes them as an ASS subtitle file and
`scripts/video.py --captions` burns them in with the brand's font:

- **Timing.** From a voice track (`--audio voice.mp3`, timed word by word
  by faster-whisper, about a minute of work per minute of audio on this
  machine), from the script's beat table (`--script script.md`, each row's
  seconds timing its own words), or spread evenly (`--text "…" --seconds
  15`) when there is neither. Real audio gives the best timing; the script
  is close enough for a slideshow.
- **The look.** Three to five words at a time, centred, inside the
  platform's safe band, in the brand's display face at about 4.5% of the
  frame height, with an outline so it reads on any picture. Each word
  turns from the accent colour to the ink colour at the moment it is
  said. `--position`, `--words` and `--size` change it; the defaults are
  the ones that read.
- **The font.** libass reads TTF and OTF, never woff2, so
  `scripts/fonts.py --from-brand` now writes a TTF beside every woff2 it
  fetches. Without one the captions fall back to the machine's default
  face and the script says so; fix it before showing the cut.
- Captions carry the same copy rules as any other words: the claims are in
  the ledger, no refused phrases, no em dashes.

## Rules

- The hook is written last and tested first: five to eight variants per
  body, one body. Test hooks before anything else.
- No logo as frame one, no slow establishing shot, no corporate
  voice-over, no music louder than the words.
- The promise is kept by second six; a re-hook every five to fifteen
  seconds; the cta is spoken and shown.
- Claims on screen are in `claims.md`. A before/after in video follows the
  same policy notes as a static.
- Show: attach the script (as a PDF or the markdown in the reply), the
  frames of a slideshow, or `cut.mp4`; say which hook you recommend and
  why in one line.
