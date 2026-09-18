#!/usr/bin/env python3
"""Fetch the brand's Google Fonts into templates/fonts/ so the renderer can
use them (Obscura loads no system fonts and only what @font-face names).

    python3 scripts/fonts.py "Bricolage Grotesque:wght@700" "Inter:wght@400;600"
    python3 scripts/fonts.py --from-brand      # the families named in templates/brand.css

Writes templates/fonts/<family>-<weight>[-italic].woff2 and
templates/fonts/fonts.css with one @font-face per file (latin subset).
Google Fonts are licensed under the OFL or Apache; rasterising them into
an ad is allowed. A brand's own licensed font goes into templates/fonts/
by hand with its own @font-face line in fonts.css; whether its licence
covers server-side rendering is the owner's to confirm.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import die, root  # noqa: E402

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def families_from_brand(app):
    css = open(os.path.join(app, "templates", "brand.css"), encoding="utf-8").read()
    out = []
    for name in ("font-display", "font-body"):
        m = re.search(r"--" + name + r":\s*\"([^\"]+)\"", css)
        if m:
            fam = m.group(1)
            out.append(f"{fam}:wght@400;600;700" if name == "font-display" else f"{fam}:wght@400;600")
    return out


def to_ttf(woff2_path):
    """A TTF beside a woff2, for libass. Needs fontTools with brotli;
    returns the path, or None when it is not installed."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    out = woff2_path[:-6] + ".ttf"
    if os.path.isfile(out):
        return out
    try:
        font = TTFont(woff2_path)
        font.flavor = None
        font.save(out)
        return out
    except Exception as e:  # noqa: BLE001
        print(f"  (could not convert {os.path.basename(woff2_path)} to TTF: {e}; video captions will use a fallback face)")
        return None


def fetch(specs, app):
    try:
        import requests
    except ImportError:
        die("requests is not installed (setup.sh installs it)")
    fonts_dir = os.path.join(app, "templates", "fonts")
    os.makedirs(fonts_dir, exist_ok=True)
    rules = []
    for spec in specs:
        family = spec.split(":")[0]
        url = "https://fonts.googleapis.com/css2?family=" + spec.replace(" ", "+") + "&display=swap"
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        if r.status_code != 200:
            die(f"Google Fonts answered {r.status_code} for {family}")
        # blocks: /* latin */ @font-face { font-family: 'X'; font-style: normal; font-weight: 700; src: url(...woff2) format('woff2'); unicode-range: ... }
        blocks = re.findall(r"/\*\s*(\w[\w-]*)\s*\*/\s*(@font-face\s*{[^}]+})", r.text)
        seen = set()
        for subset, block in blocks:
            if subset != "latin":
                continue
            style = re.search(r"font-style:\s*(\w+)", block).group(1)
            weight = re.search(r"font-weight:\s*([\d ]+)", block).group(1).strip().replace(" ", "-")
            src = re.search(r"url\(([^)]+)\)", block).group(1)
            key = (style, weight)
            if key in seen:
                continue
            seen.add(key)
            fname = re.sub(r"[^a-z0-9]+", "-", family.lower()) + f"-{weight}" + ("-italic" if style == "italic" else "") + ".woff2"
            data = requests.get(src, headers={"User-Agent": UA}, timeout=60).content
            with open(os.path.join(fonts_dir, fname), "wb") as fh:
                fh.write(data)
            # libass (the video captions) reads TTF and OTF, never woff2
            ttf = to_ttf(os.path.join(fonts_dir, fname))
            if ttf:
                print(f"  {os.path.basename(ttf)} for the video captions")
            rules.append(
                f"@font-face {{ font-family: \"{family}\"; font-style: {style}; font-weight: {weight.replace('-', ' ')}; "
                f"src: url(\"{fname}\") format(\"woff2\"); }}"
            )
            print(f"{family} {weight} {style}: {fname} ({len(data) // 1000} KB)")
        if not seen:
            print(f"warning: no latin woff2 found for {family}; check the family name and axes")
    css_path = os.path.join(fonts_dir, "fonts.css")
    existing = open(css_path, encoding="utf-8").read() if os.path.isfile(css_path) else ""
    kept = [l for l in existing.splitlines() if l.strip() and not any(f"font-family: \"{s.split(':')[0]}\"" in l for s in specs)]
    with open(css_path, "w", encoding="utf-8") as fh:
        fh.write("/* Fonts the renderer may use. scripts/fonts.py writes the Google Fonts lines; add a licensed font by hand. */\n")
        fh.write("\n".join(kept + rules) + "\n")
    print(f"wrote {os.path.relpath(css_path, app)} ({len(rules)} face(s))")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("specs", nargs="*", help='"Family:wght@400;700"')
    ap.add_argument("--from-brand", action="store_true")
    args = ap.parse_args()
    app = root()
    specs = list(args.specs)
    if args.from_brand:
        specs += families_from_brand(app)
    if not specs:
        die("name a family (\"Inter:wght@400;600\") or pass --from-brand")
    fetch(specs, app)


if __name__ == "__main__":
    main()
