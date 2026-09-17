#!/usr/bin/env python3
"""Captions for a social video, burnt in, in the brand's font.

    python3 scripts/captions.py --script creatives/generated/<id>/script.md --out <id>/caps.ass
    python3 scripts/captions.py --audio voice.mp3 --out caps.ass          # timed by transcription
    python3 scripts/captions.py --text "Half price today. Ends Friday." --seconds 6 --out caps.ass

Most feeds autoplay muted, so the words on the screen are the ad. This
writes an ASS subtitle file: the brand's font (`templates/fonts/`), the
platform's safe band, three to five words a group, and each word lighting
up as it is said (the `\\k` tag libass fills at the word's own moment).
`scripts/video.py --captions` burns it in with one ffmpeg filter.

Timing comes from, in order of preference:

  --audio     a voice track, timed by faster-whisper's word timestamps
              (`pip install faster-whisper`; CPU, about a minute a minute)
  --script    the beat table in script.md: each row's `t (s)` range times
              its on-screen text, and the words are spread inside it
  --text      even spread across --seconds; the honest fallback

Fonts: libass reads TTF and OTF, never woff2. `scripts/fonts.py` writes a
TTF beside every woff2 when fontTools is installed; without one the
caption falls back to the machine's default face and says so.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import die, read_record, root  # noqa: E402

# the 9:16 band that clears both platforms' UI (specs/README.md; the
# numbers are the owner's to nudge per platform, not a law)
SAFE = {"9:16": (0.20, 0.72), "1:1": (0.10, 0.80), "4:5": (0.10, 0.78), "16:9": (0.08, 0.80)}
SIZES = {"9:16": (1080, 1920), "1:1": (1080, 1080), "4:5": (1080, 1350), "16:9": (1920, 1080)}


def brand_font(app):
    """(family, dir) for the display face, when a TTF or OTF exists for
    libass to read. woff2 alone is not enough."""
    fonts_dir = os.path.join(app, "templates", "fonts")
    css = os.path.join(app, "templates", "brand.css")
    family = None
    if os.path.isfile(css):
        m = re.search(r'--font-display:\s*"([^"]+)"', open(css, encoding="utf-8").read())
        if m:
            family = m.group(1)
    usable = [f for f in os.listdir(fonts_dir) if f.lower().endswith((".ttf", ".otf"))] if os.path.isdir(fonts_dir) else []
    return family, fonts_dir, usable


def hex_to_ass(hex_colour, alpha="00"):
    """ASS colours are &HAABBGGRR: alpha first, then blue, green, red."""
    h = (hex_colour or "#ffffff").lstrip("#")
    if len(h) != 6:
        h = "ffffff"
    return f"&H{alpha}{h[4:6]}{h[2:4]}{h[0:2]}"


def theme_colours(app):
    css = os.path.join(app, "templates", "brand.css")
    text = open(css, encoding="utf-8").read() if os.path.isfile(css) else ""
    raw = dict(re.findall(r"--([a-z0-9-]+):\s*([^;]+);", text))

    def hexof(name, fallback):
        v = (raw.get(name) or "").strip()
        m = re.match(r"var\(--([a-z0-9-]+)\)", v)
        if m:
            v = (raw.get(m.group(1)) or "").strip()
        return v if re.fullmatch(r"#[0-9a-fA-F]{6}", v) else fallback

    return hexof("ink-on-dark", "#ffffff"), hexof("accent", "#ffd166"), hexof("ground-dark", "#101010")


def cs(seconds):
    return max(0, int(round(seconds * 100)))


def ass_time(seconds):
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def group_words(words, per_group=4):
    """[(start, end, [(word, dur), …])] in groups of at most per_group,
    broken early at sentence ends."""
    groups, cur = [], []
    for w in words:
        cur.append(w)
        ends_sentence = w["word"].rstrip().endswith((".", "!", "?"))
        if len(cur) >= per_group or ends_sentence:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return [(g[0]["start"], g[-1]["end"], g) for g in groups]


def words_from_audio(path, language=None):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        die("faster-whisper is not installed (python3 -m pip install faster-whisper); time the captions from the script instead (--script)", 2)
    model = WhisperModel(os.environ.get("WHISPER_MODEL", "small"), device="cpu", compute_type="int8")
    segments, _ = model.transcribe(path, word_timestamps=True, language=language)
    out = []
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if text:
                out.append({"word": text, "start": w.start, "end": w.end})
    if not out:
        die("no words were heard in that audio")
    return out


def words_from_script(path):
    """The beat table in script.md: rows of | t (s) | on screen | … |."""
    _, body = read_record(path)
    words = []
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or not re.match(r"^\d", cells[0]):
            continue
        m = re.match(r"(\d+(?:\.\d+)?)\s*[-–—to]+\s*(\d+(?:\.\d+)?)", cells[0])
        if not m:
            continue
        start, end = float(m.group(1)), float(m.group(2))
        text = re.sub(r"\s+", " ", cells[1]).strip().strip('"')
        toks = [t for t in text.split(" ") if t]
        if not toks or end <= start:
            continue
        step = (end - start) / len(toks)
        for i, tok in enumerate(toks):
            words.append({"word": tok, "start": start + i * step, "end": start + (i + 1) * step})
    if not words:
        die("no beat rows found in the script (a table of | t (s) | on screen | …)")
    return words


def words_from_text(text, seconds):
    toks = [t for t in re.sub(r"\s+", " ", text).strip().split(" ") if t]
    if not toks:
        die("--text was empty")
    step = seconds / len(toks)
    return [{"word": t, "start": i * step, "end": (i + 1) * step} for i, t in enumerate(toks)]


def build_ass(app, words, ratio, per_group, position, font_size=None):
    w, h = SIZES.get(ratio, SIZES["9:16"])
    top, bottom = SAFE.get(ratio, SAFE["9:16"])
    y = int(h * (bottom if position == "bottom" else top if position == "top" else 0.5))
    family, fonts_dir, usable = brand_font(app)
    ink, accent, ground = theme_colours(app)
    size = font_size or int(h * 0.045)
    primary = hex_to_ass(ink)          # the word once it has been said
    secondary = hex_to_ass(accent)     # the word before it is said
    outline = hex_to_ass(ground)
    face = family if (family and usable) else "Sans"

    head = f"""[Script Info]
; Written by scripts/captions.py; the brand's face, the platform's safe band, one word at a time.
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{face},{size},{primary},{secondary},{outline},&H80000000,-1,0,0,0,100,100,1,0,1,{max(3, size // 14)},0,2,{int(w * 0.06)},{int(w * 0.06)},{int(h * 0.05)},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for start, end, group in group_words(words, per_group):
        body = "".join("{\\k%d}%s " % (cs(wd["end"] - wd["start"]), wd["word"]) for wd in group).strip()
        lines.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end + 0.15)},Cap,,0,0,0,,{{\\pos({w // 2},{y})}}{body}")
    return head + "\n".join(lines) + "\n", face, usable


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audio", help="a voice track; times the words by transcription")
    ap.add_argument("--script", help="script.md, timed by its beat table")
    ap.add_argument("--text", help="the words, spread evenly across --seconds")
    ap.add_argument("--seconds", type=float, default=15.0)
    ap.add_argument("--ratio", default="9:16", choices=sorted(SIZES))
    ap.add_argument("--words", type=int, default=4, help="words per caption group (3 to 5 reads best)")
    ap.add_argument("--position", default="bottom", choices=["top", "middle", "bottom"])
    ap.add_argument("--size", type=int, help="font size in the video's own pixels")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    app = root()

    if args.audio:
        words = words_from_audio(args.audio)
    elif args.script:
        words = words_from_script(args.script)
    elif args.text:
        words = words_from_text(args.text, args.seconds)
    else:
        die("one of --audio, --script or --text")

    ass, face, usable = build_ass(app, words, args.ratio, args.words, args.position, args.size)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(ass)
    groups = ass.count("Dialogue:")
    print(f"{args.out}: {groups} caption group(s), {len(words)} words, {face}")
    if not usable:
        print("note: no TTF or OTF in templates/fonts, so the captions fall back to the machine's default face; run scripts/fonts.py --from-brand to fetch one", file=sys.stderr)


if __name__ == "__main__":
    main()
