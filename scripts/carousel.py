#!/usr/bin/env python3
"""Render a carousel's cards: every fields-NN.json in the creative's folder
through its template into slides/NN.png, recorded in creative.md `files`,
and (for LinkedIn) the cards as one PDF.

    python3 scripts/carousel.py <creative-dir|id> [--size 1080x1080] [--dpr 2] [--pdf]

Each fields-NN.json is a normal template fields file (templates/README.md)
with its own `template`; the size is shared across the deck. The deck's
copy and claims live in creative.md as for any creative.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import die, find_creative, read_record, root, write_record  # noqa: E402
from render import render_one  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--size")
    ap.add_argument("--dpr", type=int, default=2)
    ap.add_argument("--pdf", action="store_true", help="also write document.pdf from the slides (LinkedIn)")
    args = ap.parse_args()
    app = root()
    d = args.target if os.path.isdir(args.target) else find_creative(app, args.target)[1]
    if not d:
        die(f"no creative {args.target}")
    cards = sorted(f for f in os.listdir(d) if re.fullmatch(r"fields-\d+\.json", f))
    if not cards:
        die("no fields-NN.json files (one per card; templates/README.md lists the fields)")
    slides = os.path.join(d, "slides")
    os.makedirs(slides, exist_ok=True)
    made = []
    for card in cards:
        n = re.search(r"(\d+)", card).group(1).zfill(2)
        # render_one reads fields.json; point it at this card through a temporary alias
        alias = os.path.join(d, "fields.json")
        backup = None
        if os.path.exists(alias):
            backup = open(alias, encoding="utf-8").read()
        with open(os.path.join(d, card), encoding="utf-8") as fh:
            payload = fh.read()
        with open(alias, "w", encoding="utf-8") as fh:
            fh.write(payload)
        try:
            render_one(app, d, args.size, None, args.dpr, os.path.join("slides", f"{n}.png"))
        finally:
            # keep the measured boxes with the card, restore the deck's fields.json
            with open(alias, encoding="utf-8") as fh:
                measured = fh.read()
            with open(os.path.join(d, card), "w", encoding="utf-8") as fh:
                fh.write(measured)
            if backup is None:
                os.remove(alias)
            else:
                with open(alias, "w", encoding="utf-8") as fh:
                    fh.write(backup)
        made.append(f"slides/{n}.png")

    rec = os.path.join(d, "creative.md")
    fm, body = read_record(rec)
    files = [f for f in (fm.get("files") or []) if not str(f).startswith("slides/")] + made
    if args.pdf:
        try:
            from PIL import Image
            imgs = [Image.open(os.path.join(d, m)).convert("RGB") for m in made]
            pdf = os.path.join(d, "document.pdf")
            imgs[0].save(pdf, "PDF", save_all=True, append_images=imgs[1:], resolution=150)
            files.append("document.pdf")
            print(f"document.pdf ({len(imgs)} pages, {os.path.getsize(pdf) // 1000} KB)")
        except ImportError:
            print("Pillow missing: no PDF")
    fm["files"] = files
    fm["kind"] = "carousel"
    write_record(rec, fm, body)
    print(f"{os.path.basename(d)}: {len(made)} card(s) in slides/")


if __name__ == "__main__":
    main()
