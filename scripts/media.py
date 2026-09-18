#!/usr/bin/env python3
"""Index the business's own pictures and video in media/, so the AI knows
what it has before it asks a model to invent something.

    python3 scripts/media.py                  index media/ and report
    python3 scripts/media.py --for 9:16       what is usable at that ratio
    python3 scripts/media.py --clips          only the video
    python3 scripts/media.py --json

Writes media/_index.json: one record per file with its kind, pixel size,
orientation, duration (video), bytes, and whether media/_notes.md has a
line for it. Photographs need Pillow; video needs ffprobe (both are
installed by setup.sh). A file the tools cannot read is listed as
unreadable rather than skipped silently.

What the report tells you, in the order it matters:

  usable          files with a note in _notes.md, big enough for the ratio
  no note yet     files nobody has said may be used: ask the owner
  too small       a picture under the placement's pixel size
  too big to mirror   over 20 MB, so a mirror from a brain or website
                  will not carry it (the owner exports a smaller one)
"""

import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import RATIOS, root  # noqa: E402

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"}
CLIP_EXT = {".mp4", ".mov", ".m4v", ".webm", ".avi"}
MIRROR_CAP = 20 * 1024 * 1024      # the platform's per-file mirror limit
MIRROR_TOTAL = 200 * 1024 * 1024   # and per folder


def probe_clip(path):
    """(width, height, seconds) or None; needs ffprobe."""
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height:format=duration", "-of", "json", path],
            capture_output=True, text=True, timeout=60)
        data = json.loads(p.stdout or "{}")
        stream = (data.get("streams") or [{}])[0]
        w, h = stream.get("width"), stream.get("height")
        dur = float((data.get("format") or {}).get("duration") or 0)
        return (w, h, round(dur, 2)) if w and h else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def probe_photo(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:  # noqa: BLE001
        return None


def noted_files(app):
    """The file names _notes.md mentions, so an unasked file is visible."""
    path = os.path.join(app, "media", "_notes.md")
    if not os.path.isfile(path):
        return set()
    text = open(path, encoding="utf-8").read()
    names = set()
    for m in re.finditer(r"[\w./-]+\.(?:jpe?g|png|webp|heic|tiff?|mp4|mov|m4v|webm|avi)", text, re.I):
        if "(example)" not in text[max(0, m.start() - 40):m.start()]:
            names.add(os.path.basename(m.group(0)))
    return names


def index(app):
    base = os.path.join(app, "media")
    noted = noted_files(app)
    out, total = [], 0
    for dirpath, _dirs, files in os.walk(base):
        for name in sorted(files):
            if name.startswith(".") or name.startswith("_") or name == "README.md":
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, app)
            ext = os.path.splitext(name)[1].lower()
            if ext not in PHOTO_EXT and ext not in CLIP_EXT:
                continue
            size = os.path.getsize(path)
            total += size
            rec = {"file": rel, "name": name, "bytes": size, "noted": name in noted,
                   "mirrorable": size <= MIRROR_CAP}
            if ext in PHOTO_EXT:
                rec["kind"] = "photo"
                dims = probe_photo(path)
                if dims:
                    rec["width"], rec["height"] = dims
                    rec["orientation"] = orientation(*dims)
                else:
                    rec["unreadable"] = True
            else:
                rec["kind"] = "clip"
                probed = probe_clip(path)
                if probed:
                    rec["width"], rec["height"], rec["seconds"] = probed
                    rec["orientation"] = orientation(probed[0], probed[1])
                else:
                    rec["unreadable"] = True
            out.append(rec)
    return out, total


def orientation(w, h):
    r = w / h if h else 1
    if r > 1.2:
        return "landscape"
    if r < 0.85:
        return "portrait"
    return "square"


def fits(rec, ratio):
    """Whether a photo has the pixels for that placement's master."""
    want_w, want_h = RATIOS.get(ratio, (1080, 1350))
    w, h = rec.get("width"), rec.get("height")
    if not w or not h:
        return False
    # a picture is usable when it covers the master's short edge after a crop
    return min(w, h) >= min(want_w, want_h) * 0.9


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--for", dest="ratio", choices=sorted(RATIOS))
    ap.add_argument("--clips", action="store_true")
    ap.add_argument("--photos", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    app = root()
    base = os.path.join(app, "media")
    if not os.path.isdir(base):
        print("no media/ folder; the owner's own pictures and video go there (media/README.md)")
        sys.exit(0)

    records, total = index(app)
    with open(os.path.join(base, "_index.json"), "w", encoding="utf-8") as fh:
        json.dump({"files": records, "total_bytes": total}, fh, indent=2)
        fh.write("\n")

    if args.clips:
        records = [r for r in records if r["kind"] == "clip"]
    if args.photos:
        records = [r for r in records if r["kind"] == "photo"]
    if args.json:
        print(json.dumps(records, indent=2))
        return

    if not records:
        print("media/ is empty. The owner's own photographs and clips are the best material there is:")
        print("  - they can upload them in the Files tab or send them in chat")
        print("  - or mirror them from a Company Brain or website in this project (media/README.md)")
        print("  - or, if this app crawled the site, the sources skill copies the real photos across")
        return

    usable, no_note, too_small, too_big, unreadable = [], [], [], [], []
    for r in records:
        if r.get("unreadable"):
            unreadable.append(r)
            continue
        if not r["mirrorable"]:
            too_big.append(r)
        if not r["noted"]:
            no_note.append(r)
            continue
        if args.ratio and r["kind"] == "photo" and not fits(r, args.ratio):
            too_small.append(r)
            continue
        usable.append(r)

    def line(r):
        shape = f"{r.get('width', '?')}x{r.get('height', '?')} {r.get('orientation', '')}"
        dur = f" {r['seconds']}s" if r.get("seconds") else ""
        return f"  {r['file']:<44} {r['kind']:<6} {shape}{dur}  {r['bytes'] // 1000} KB"

    print(f"media/: {len(records)} file(s), {total // 1_000_000} MB" + (f", for {args.ratio}" if args.ratio else ""))
    for label, group, note in [
        ("usable", usable, ""),
        ("no note yet (ask the owner what it shows and whether it may be used)", no_note, ""),
        ("too small for this placement", too_small, ""),
        ("too big for a mirror (over 20 MB; a mirror from a brain or website will skip it)", too_big, ""),
        ("unreadable (needs Pillow for photos, ffprobe for video)", unreadable, ""),
    ]:
        if group:
            print(f"\n{label}: {len(group)}{note}")
            for r in group[:20]:
                print(line(r))
            if len(group) > 20:
                print(f"  … and {len(group) - 20} more")
    if total > MIRROR_TOTAL:
        print(f"\nnote: media/ is {total // 1_000_000} MB, over the 200 MB a mirror carries; a mirror into another app would stop short.")


if __name__ == "__main__":
    main()
