#!/usr/bin/env python3
"""Placements from a master (specs/*.md): the sizes a platform takes for
the master's ratio, in sRGB, as PNG or JPEG under the byte limit.

    python3 scripts/resize.py <creative-dir|id> [--jpeg] [--all-ratios]

A master is only ever resized within its own ratio (1080×1350 → 1440×1800,
1200×1200 → 1080×1080). A different ratio is a different composition:
render.py with --size makes it from the same fields. --all-ratios lists
which sizes the platform wants that are still missing, so the AI renders
them, and never crops. Records the new files in creative.md `files`.
Needs Pillow.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import find_creative, read_record, root, write_record  # noqa: E402
from qa import MAX_BYTES, SIZES  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--jpeg", action="store_true", help="write JPEG (q85) instead of PNG for the placements")
    ap.add_argument("--all-ratios", action="store_true", help="list the platform's other ratios still to render")
    args = ap.parse_args()
    try:
        from PIL import Image, ImageCms
    except ImportError:
        print("Pillow is not installed (setup.sh installs it)", file=sys.stderr)
        sys.exit(1)

    app = root()
    d = args.target if os.path.isdir(args.target) else find_creative(app, args.target)[1]
    if not d:
        print(f"no creative {args.target}", file=sys.stderr)
        sys.exit(1)
    path = os.path.join(d, "creative.md")
    fm, body = read_record(path)
    platform, ratio = fm.get("platform"), str(fm.get("ratio") or "")
    master = os.path.join(d, "master.png")
    if not os.path.isfile(master):
        print("no master.png; render.py first", file=sys.stderr)
        sys.exit(1)

    img = Image.open(master).convert("RGB")
    srgb = ImageCms.createProfile("sRGB")
    icc = ImageCms.ImageCmsProfile(srgb).tobytes()
    wanted = SIZES.get(platform, {}).get(ratio, [])
    files = list(fm.get("files") or [])
    if "master.png" not in files:
        files.append("master.png")
    made = []
    for (w, h) in wanted:
        if (w, h) == img.size:
            continue
        name = f"{w}x{h}.{'jpg' if args.jpeg else 'png'}"
        out = img.resize((w, h), Image.LANCZOS)
        target = os.path.join(d, name)
        if args.jpeg:
            out.save(target, "JPEG", quality=85, icc_profile=icc, optimize=True)
        else:
            out.save(target, "PNG", icc_profile=icc, optimize=True)
        limit = MAX_BYTES.get(platform, 30_000_000)
        if os.path.getsize(target) > limit and not args.jpeg:
            out.save(target[:-4] + ".jpg", "JPEG", quality=85, icc_profile=icc, optimize=True)
            os.remove(target)
            name = name[:-4] + ".jpg"
        if name not in files:
            files.append(name)
        made.append(name)
    # the master itself gets the sRGB tag too
    img.save(master, "PNG", icc_profile=icc, optimize=True)
    fm["files"] = files
    write_record(path, fm, body)
    print(f"{os.path.basename(d)}: " + (", ".join(made) if made else "no other size for this ratio") + " (sRGB tagged)")
    if args.all_ratios:
        others = [r for r in SIZES.get(platform, {}) if r != ratio]
        if others:
            print("other ratios this platform takes, each its own render (render.py --size): " + ", ".join(f"{r} {SIZES[platform][r][0][0]}x{SIZES[platform][r][0][1]}" for r in others))


if __name__ == "__main__":
    main()
