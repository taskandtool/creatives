#!/usr/bin/env python3
"""Quality gates on rendered creatives (DESIGN.md, specs/): the token
pairs, the master's size, the file size, the contrast behind the words,
and the placement's safe zone.

    python3 scripts/qa.py --tokens                 the brand.css text and ground pairs
    python3 scripts/qa.py <creative-dir> […]       one or more folders (or ids)

Needs Pillow for the image checks (setup.sh installs it); the token check
is pure Python. Exit 1 with findings.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import RATIOS, find_creative, read_record, root  # noqa: E402

# the size a platform wants for each ratio, and the byte limit (specs/*.md)
SIZES = {
    "meta": {"4:5": [(1080, 1350), (1440, 1800)], "1:1": [(1080, 1080)], "9:16": [(1080, 1920)], "1.91:1": [(1200, 628)]},
    "linkedin": {"1.91:1": [(1200, 627), (1200, 628)], "1:1": [(1200, 1200), (1080, 1080)], "4:5": [(720, 900), (1080, 1350)]},
    "tiktok": {"9:16": [(1080, 1920)]},
    "google": {"1.91:1": [(1200, 628)], "1:1": [(1200, 1200)], "4:5": [(960, 1200)], "9:16": [(1080, 1920)]},
    "pinterest": {"2:3": [(1000, 1500)]},
    "youtube": {"16:9": [(1280, 720)], "9:16": [(1080, 1920)]},
    "gbp": {"4:3": [(1200, 900)], "1:1": [(1080, 1080)]},
}
MAX_BYTES = {"meta": 30_000_000, "linkedin": 5_000_000, "google": 5_000_000, "pinterest": 20_000_000, "youtube": 2_000_000, "tiktok": 500_000_000, "gbp": 5_000_000}
# the 9:16 box the platforms' UI leaves alone (unverified numerically; specs/README.md)
SAFE_9_16 = (0.06, 0.14, 0.06, 0.35)  # left, top, right, bottom as fractions


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted([luminance(a), luminance(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def background_contrast(ink, pixels, ink_distance=90):
    """The worst contrast between the ink and the pixels behind it. The
    glyphs themselves (and their antialiasing) are in the box too, so pixels
    near the ink colour are left out; None when nothing else is in the box."""
    def dist(p):
        return sum((a - b) ** 2 for a, b in zip(p[:3], ink)) ** 0.5

    background = [p[:3] for p in pixels if dist(p) >= ink_distance]
    if len(background) < max(4, len(pixels) // 20):
        return None
    # the antialiased fringe between ink and ground is a minority of the
    # box: the lower quartile ignores it and still catches a busy or
    # mid-toned ground behind the words
    ratios = sorted(contrast(ink, p) for p in background)
    return ratios[len(ratios) // 4]


def tokens(app):
    """{name: '#rrggbb'} for the hex tokens in templates/brand.css, following
    one level of var()."""
    css = open(os.path.join(app, "templates", "brand.css"), encoding="utf-8").read()
    raw = dict(re.findall(r"--([a-z0-9-]+):\s*([^;]+);", css))
    out = {}
    for name, val in raw.items():
        val = val.strip()
        m = re.match(r"var\(--([a-z0-9-]+)\)", val)
        if m:
            val = raw.get(m.group(1), "").strip()
        if re.fullmatch(r"#[0-9a-fA-F]{6}", val):
            out[name] = val.lower()
    return out


def check_tokens(app):
    t = tokens(app)
    pairs = [("ink", "ground"), ("ink-2", "ground"), ("ink-on-dark", "ground-dark"), ("accent-ink", "accent")]
    findings = []
    for fg, bg in pairs:
        if fg in t and bg in t:
            r = contrast(hex_to_rgb(t[fg]), hex_to_rgb(t[bg]))
            if r < 4.5:
                findings.append(f"tokens: {fg} ({t[fg]}) on {bg} ({t[bg]}) is {r:.1f}:1, under 4.5:1 (DESIGN.md)")
    if "accent" in t and "ground" in t:
        r = contrast(hex_to_rgb(t["accent"]), hex_to_rgb(t["ground"]))
        if r < 3:
            findings.append(f"tokens: accent ({t['accent']}) on ground ({t['ground']}) is {r:.1f}:1; under 3:1 the pill disappears")
    return findings


def check_dir(app, d):
    """Findings for one creative folder's rendered files."""
    findings = []
    try:
        from PIL import Image
    except ImportError:
        return ["Pillow is not installed (setup.sh installs it); image checks skipped"]
    fm, _ = read_record(os.path.join(d, "creative.md"))
    platform, ratio = fm.get("platform"), str(fm.get("ratio") or "")
    master = os.path.join(d, "master.png")
    if not os.path.isfile(master):
        return findings
    img = Image.open(master)
    w, h = img.size
    wanted = SIZES.get(platform, {}).get(ratio) or ([RATIOS[ratio]] if ratio in RATIOS else [])
    if wanted and (w, h) not in wanted:
        findings.append(f"master.png is {w}x{h}; {platform} {ratio} wants {' or '.join(f'{a}x{b}' for a, b in wanted)}")
    size = os.path.getsize(master)
    if size > MAX_BYTES.get(platform, 30_000_000):
        findings.append(f"master.png is {size // 1000} KB, over {platform}'s limit")
    mode = img.mode
    if mode not in ("RGB", "RGBA"):
        findings.append(f"master.png is {mode}; export RGB")
    # contrast behind the words: render.py records each text box in
    # fields.json under _boxes as [x, y, w, h, hex-of-the-text]
    fields_path = os.path.join(d, "fields.json")
    if os.path.isfile(fields_path):
        fields = json.load(open(fields_path))
        rgb = img.convert("RGB")
        for box in fields.get("_boxes") or []:
            x, y, bw, bh, ink = box
            # inset the box a little: getBoundingClientRect includes padding and
            # the antialiased edge of a pill, which are not behind the words
            ix, iy = int(bw * 0.08), int(bh * 0.12)
            region = rgb.crop((max(0, x + ix), max(0, y + iy), min(w, x + bw - ix), min(h, y + bh - iy)))
            if region.size[0] < 2 or region.size[1] < 2:
                continue
            small = region.resize((min(64, region.size[0]), min(64, region.size[1])))
            worst = background_contrast(hex_to_rgb(ink), list(small.getdata()))
            if worst is not None and worst < 3.0:
                findings.append(f"text at ({x},{y}) sits on pixels at {worst:.1f}:1 against its ink; add the scrim or move it")
        if ratio == "9:16":
            l, t, r, b = SAFE_9_16
            for box in fields.get("_boxes") or []:
                x, y, bw, bh, _ = box
                if x < w * l or x + bw > w * (1 - r) or y < h * t or y + bh > h * (1 - b):
                    findings.append(f"text at ({x},{y}) is inside the 9:16 UI zone (top {int(t*100)}%, bottom {int(b*100)}%, sides {int(l*100)}%)")
    for f in fm.get("files") or []:
        p = os.path.join(d, str(f))
        if os.path.isfile(p) and p.lower().endswith((".png", ".jpg", ".jpeg")):
            try:
                Image.open(p).verify()
            except Exception as e:  # noqa: BLE001
                findings.append(f"{f} is not a readable image ({e})")
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("targets", nargs="*", help="creative folders or ids")
    ap.add_argument("--tokens", action="store_true")
    args = ap.parse_args()
    app = root()
    findings = []
    if args.tokens or not args.targets:
        findings += check_tokens(app)
    for t in args.targets:
        d = t if os.path.isdir(t) else find_creative(app, t)[1]
        if not d:
            findings.append(f"no creative {t}")
            continue
        findings += [f"{os.path.basename(d)}: {f}" for f in check_dir(app, d)]
    if findings:
        print(f"qa: {len(findings)} finding(s)\n  - " + "\n  - ".join(findings), file=sys.stderr)
        sys.exit(1)
    print("qa: ok")


if __name__ == "__main__":
    main()
