#!/usr/bin/env python3
"""Cut a social video on this machine with ffmpeg: the owner's own clips,
the app's rendered cards, or both, with the captions burnt in.

    python3 scripts/video.py <creative-dir|id> [--length 15] [--fps 30] [--ratio 9:16]
                             [--captions] [--voice voice.mp3] [--music music.mp3] [--music-db -18]
                             [--out cut.mp4]

**What it cuts.** A `shots.json` in the creative's folder is the edit
list, one entry per shot, in order:

    [{"clip": "media/clips/bench.mp4", "in": 2.0, "out": 5.5},
     {"slide": "slides/02.png", "seconds": 3},
     {"clip": "media/clips/fit.mp4", "in": 0, "out": 4, "mute": true}]

A `clip` is the owner's own footage from `media/` (or anywhere in the
app), trimmed from `in` to `out`, scaled and centre-cropped to the
ratio. A `slide` is one of the app's rendered cards, held for `seconds`
with a slow push. Mix them freely: a hook card, then footage, then a
closing card is the usual shape.

Without a `shots.json` it falls back to a **slideshow** of every
`slides/NN.png`, which is what an app with no footage can make: equal
shares of `--length`, or per-frame seconds in `slides/durations.json`.

Audio: the clips' own sound is used when a shot is not muted and no
`--voice` is given; `--voice` replaces it; `--music` sits under either.
`--captions` burns `caps.ass` (scripts/captions.py) through libass in the
brand's font. Needs ffmpeg, which setup.sh installs. Records the file in
creative.md `files`.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import RATIOS, die, find_creative, read_record, root, write_record  # noqa: E402


def probe_seconds(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    try:
        return float(p.stdout.strip())
    except ValueError:
        return None


def has_audio(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return bool(p.stdout.strip())


def load_shots(app, d, args, frames):
    """[(kind, payload, seconds)] from shots.json, else the slideshow."""
    path = os.path.join(d, "shots.json")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            raw = json.load(fh)
        shots = []
        for i, shot in enumerate(raw, start=1):
            if shot.get("clip"):
                src = shot["clip"] if os.path.isabs(shot["clip"]) else os.path.join(app, shot["clip"])
                if not os.path.isfile(src):
                    src_in_creative = os.path.join(d, shot["clip"])
                    if os.path.isfile(src_in_creative):
                        src = src_in_creative
                    else:
                        die(f"shot {i}: no clip at {shot['clip']} (the owner's footage lives in media/clips; scripts/media.py lists it)")
                start = float(shot.get("in", 0))
                end = shot.get("out")
                if end is None:
                    dur = probe_seconds(src)
                    if dur is None:
                        die(f"shot {i}: could not read {shot['clip']}; give it an \"out\"")
                    end = dur
                seconds = max(0.2, float(end) - start)
                shots.append(("clip", {"src": src, "in": start, "seconds": seconds, "mute": bool(shot.get("mute"))}, seconds))
            elif shot.get("slide"):
                src = os.path.join(d, shot["slide"]) if not os.path.isabs(shot["slide"]) else shot["slide"]
                if not os.path.isfile(src):
                    die(f"shot {i}: no slide at {shot['slide']}")
                shots.append(("slide", {"src": src}, float(shot.get("seconds", 3))))
            else:
                die(f"shot {i}: needs a \"clip\" or a \"slide\"")
        return shots
    if not frames:
        die("no shots.json and no slides/NN.png: nothing to cut. The owner's clips go in media/clips and are listed in shots.json; the app's cards are rendered into slides/.")
    durations = None
    dpath = os.path.join(d, "slides", "durations.json")
    if os.path.isfile(dpath):
        with open(dpath, encoding="utf-8") as fh:
            durations = json.load(fh)
    if not durations or len(durations) != len(frames):
        durations = [args.length / len(frames)] * len(frames)
    return [("slide", {"src": f}, float(s)) for f, s in zip(frames, durations)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--length", type=float, default=15.0, help="the slideshow fallback's total length")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--ratio", help="9:16, 4:5, 1:1, 16:9 (default: the creative's own)")
    ap.add_argument("--voice")
    ap.add_argument("--music")
    ap.add_argument("--music-db", type=float, default=-18.0)
    ap.add_argument("--captions", nargs="?", const="auto", help="burn an ASS caption file; 'auto' finds caps.ass beside the creative")
    ap.add_argument("--out", default="cut.mp4")
    args = ap.parse_args()
    if not shutil.which("ffmpeg"):
        die("ffmpeg is not installed (setup.sh installs a static build)", 2)
    app = root()
    d = args.target if os.path.isdir(args.target) else find_creative(app, args.target)[1]
    if not d:
        die(f"no creative {args.target}")

    rec_path = os.path.join(d, "creative.md")
    fm, body = read_record(rec_path) if os.path.isfile(rec_path) else ({}, "")
    ratio = args.ratio or str(fm.get("ratio") or "9:16")
    w, h = RATIOS.get(ratio, RATIOS["9:16"])
    w, h = w - (w % 2), h - (h % 2)

    slides_dir = os.path.join(d, "slides")
    frames = ([os.path.join(slides_dir, f) for f in sorted(os.listdir(slides_dir)) if re.fullmatch(r"\d+\.png", f)]
              if os.path.isdir(slides_dir) else [])
    shots = load_shots(app, d, args, frames)

    inputs, filters, video_parts, audio_parts = [], [], [], []
    for i, (kind, payload, seconds) in enumerate(shots):
        if kind == "clip":
            # trim, then cover the frame: scale so the short edge fills, then centre crop
            inputs += ["-ss", f"{payload['in']:.3f}", "-t", f"{seconds:.3f}", "-i", payload["src"]]
            filters.append(
                f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
                f"fps={args.fps},format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v{i}]"
            )
            if not payload["mute"] and not args.voice and has_audio(payload["src"]):
                audio_parts.append(f"[{i}:a]aresample=async=1,asetpts=PTS-STARTPTS[a{i}]")
        else:
            n = max(2, int(round(seconds * args.fps)))
            # exactly one input frame: zoompan emits `d` frames for every frame
            # it is given, so a looped input would hold the first card for the
            # whole cut (and it did, until this was fixed)
            inputs += ["-i", payload["src"]]
            filters.append(
                f"[{i}:v]scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase,crop={w * 2}:{h * 2},"
                f"zoompan=z='min(zoom+{1.06 / n:.6f},1.06)':d={n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={args.fps},"
                f"trim=duration={seconds:.3f},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[v{i}]"
            )
        video_parts.append(f"[v{i}]")

    total = sum(s for _, _, s in shots)
    fc = ";".join(filters) + ";" + "".join(video_parts) + f"concat=n={len(shots)}:v=1:a=0[vcat]"

    caps = None
    if args.captions:
        caps = os.path.join(d, "caps.ass") if args.captions == "auto" else args.captions
        if not os.path.isfile(caps):
            die(f"no caption file at {caps} (scripts/captions.py writes one)")
        fonts_dir = os.path.join(app, "templates", "fonts")
        esc = caps.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        fdir = fonts_dir.replace("\\", "/").replace(":", "\\:")
        fc += f";[vcat]subtitles='{esc}':fontsdir='{fdir}':original_size={w}x{h}[v]"
    else:
        fc += ";[vcat]null[v]"

    # audio: a voice track wins; else the clips' own sound; music sits under
    extra, amap, ai = [], [], len(shots)
    if args.voice:
        extra += ["-i", args.voice]
        amap.append(f"[{ai}:a]aresample=async=1[a_voice]")
        ai += 1
        voice_seconds = probe_seconds(args.voice)
        if voice_seconds and not os.path.isfile(os.path.join(d, "shots.json")):
            total = max(voice_seconds + 0.4, 3.0)
    if args.music:
        extra += ["-stream_loop", "-1", "-i", args.music]
        amap.append(f"[{ai}:a]volume={args.music_db}dB[a_music]")
        ai += 1

    have_clip_audio = bool(audio_parts) and not args.voice
    if have_clip_audio:
        # only some shots have sound, so pad the silent ones to keep sync
        fc += ";" + ";".join(audio_parts)
        pieces = []
        for i, (kind, payload, seconds) in enumerate(shots):
            if kind == "clip" and not payload["mute"] and not args.voice and has_audio(payload["src"]):
                pieces.append(f"[a{i}]")
            else:
                fc += f";anullsrc=r=44100:cl=stereo,atrim=0:{seconds:.3f},asetpts=PTS-STARTPTS[s{i}]"
                pieces.append(f"[s{i}]")
        fc += ";" + "".join(pieces) + f"concat=n={len(shots)}:v=0:a=1[a_clips]"

    sources = [n for n, present in (("[a_voice]", args.voice), ("[a_music]", args.music), ("[a_clips]", have_clip_audio)) if present]
    if amap and not have_clip_audio:
        fc += ";" + ";".join(amap)
    elif amap:
        fc += ";" + ";".join(amap)
    if len(sources) > 1:
        fc += ";" + "".join(sources) + f"amix=inputs={len(sources)}:duration=first:dropout_transition=2[a]"
    elif len(sources) == 1:
        fc += f";{sources[0]}anull[a]"

    out = os.path.join(d, args.out)
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, *extra, "-filter_complex", fc, "-map", "[v]"]
    if sources:
        cmd += ["-map", "[a]", "-c:a", "aac", "-b:a", "128k"]
    cmd += ["-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-r", str(args.fps), out]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        die(f"ffmpeg failed: {p.stderr[-900:]}")

    if os.path.isfile(rec_path):
        files = list(fm.get("files") or [])
        if args.out not in files:
            files.append(args.out)
        fm["files"] = files
        write_record(rec_path, fm, body)
    secs = probe_seconds(out)
    kinds = ", ".join(f"{sum(1 for k, _, _ in shots if k == kind)} {kind}{'s' if sum(1 for k, _, _ in shots if k == kind) != 1 else ''}"
                      for kind in ("clip", "slide") if any(k == kind for k, _, _ in shots))
    print(f"{os.path.relpath(out, app)} {w}x{h} {secs:.1f}s ({os.path.getsize(out) // 1000} KB, {kinds}"
          + (", captions burnt in" if caps else "") + (", sound" if sources else ", silent") + ")")


if __name__ == "__main__":
    main()
