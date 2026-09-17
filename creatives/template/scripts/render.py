#!/usr/bin/env python3
"""Render a creative's fields.json through its template into master.png.

    python3 scripts/render.py <creative-dir|id> [--size 1080x1350] [--template statement]
                              [--dpr 2] [--out master.png] [--html-only]
    python3 scripts/render.py --all generated        # re-render every generated creative

How it works: the template (templates/<name>.html) is filled from
fields.json (a mustache subset: {{name}}, {{{raw}}}, {{#list}}…{{/list}},
{{^absent}}…{{/absent}}), templates/brand.css and templates/fonts/fonts.css
are inlined with --scale set for the size, image paths are made absolute,
and the page is written to render.html beside the fields. Obscura (the
headless browser setup.sh installs) captures exactly the card's box: its
viewport comes from OBSCURA_SHOT_W/H, and its capture is 1x, so the page is
authored at --dpr times the size and downsampled with Pillow for a sharp
result. The text boxes are measured in the page and recorded in fields.json
as `_boxes` for qa.py's contrast and safe-zone checks. Fonts: Obscura loads
no system fonts; anything but Liberation Sans falls back unless
templates/fonts/fonts.css declares it (scripts/fonts.py fetches Google
Fonts into templates/fonts/).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import RATIOS, STATUSES, creative_dirs, die, find_creative, read_record, render_template, root, write_record  # noqa: E402

TEXT_SELECTOR = ".headline,.body,.cta,.label,.giant"
EVAL = (
    "JSON.stringify([...document.querySelectorAll('" + TEXT_SELECTOR + "')].map(e=>{"
    "const r=e.getBoundingClientRect();const c=getComputedStyle(e).color;"
    "return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height),c]}))"
)


def obscura_bin():
    for c in [shutil.which("obscura"), "/usr/local/bin/obscura", os.path.expanduser("~/.local/bin/obscura")]:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


def abs_file_url(path, base):
    p = path if os.path.isabs(path) else os.path.join(base, path)
    return "file://" + os.path.abspath(p)


def inline_css(app, dpr, width, ratio_class):
    css = open(os.path.join(app, "templates", "brand.css"), encoding="utf-8").read()
    fonts_css = os.path.join(app, "templates", "fonts", "fonts.css")
    fonts = open(fonts_css, encoding="utf-8").read() if os.path.isfile(fonts_css) else ""
    fonts_dir = os.path.join(app, "templates", "fonts")
    # font files referenced relatively in fonts.css → absolute file:// URLs
    fonts = re.sub(r"url\((['\"]?)(?!https?:|data:|file:)([^)'\"]+)\1\)",
                   lambda m: f"url('{abs_file_url(m.group(2), fonts_dir)}')", fonts)
    scale = (width / 1080.0) * dpr
    css = css.replace("--scale: 1;", f"--scale: {scale:.4f};")
    return fonts + "\n" + css + f"\n.card {{ }}\n"


def rgb_to_hex(c):
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", c or "")
    if not m:
        return "#000000"
    return "#%02x%02x%02x" % tuple(int(m.group(i)) for i in (1, 2, 3))


def parse_boxes(stdout, dpr):
    """The eval prints its result as JSON (a JSON string holding the array,
    or the array itself), possibly among other lines: take the first line
    that parses into a list of [x, y, w, h, colour]."""
    for line in stdout.splitlines():
        line = line.strip()
        if not line or not (line.startswith("[") or line.startswith('"')):
            continue
        try:
            data = json.loads(line)
            if isinstance(data, str):
                data = json.loads(data)
        except ValueError:
            continue
        if isinstance(data, list):
            out = []
            for item in data:
                try:
                    x, y, bw, bh, color = item
                    out.append([round(x / dpr), round(y / dpr), round(bw / dpr), round(bh / dpr), rgb_to_hex(color)])
                except (TypeError, ValueError):
                    continue
            return out
    return []


def render_one(app, d, size=None, template=None, dpr=2, out="master.png", html_only=False):
    fields_path = os.path.join(d, "fields.json")
    if not os.path.isfile(fields_path):
        die(f"{d}: no fields.json (scripts/new.py makes one)")
    fields = json.load(open(fields_path, encoding="utf-8"))
    rec_path = os.path.join(d, "creative.md")
    fm, body = read_record(rec_path) if os.path.isfile(rec_path) else ({}, "")

    size = size or fields.get("size") or (RATIOS.get(str(fm.get("ratio")), (1080, 1350)) and f"{RATIOS[str(fm.get('ratio'))][0]}x{RATIOS[str(fm.get('ratio'))][1]}")
    m = re.fullmatch(r"(\d+)x(\d+)", str(size))
    if not m:
        die(f"--size must be WxH, got {size}")
    w, h = int(m.group(1)), int(m.group(2))
    template = template or fields.get("template") or "statement"
    tpl_path = os.path.join(app, "templates", f"{template}.html")
    if not os.path.isfile(tpl_path):
        die(f"no template {template} (templates/: {', '.join(sorted(f[:-5] for f in os.listdir(os.path.join(app, 'templates')) if f.endswith('.html')))})")

    ratio_class = "r-" + re.sub(r"[^0-9]", "", str(fm.get("ratio") or ""))
    ctx = dict(fields)
    ctx.update({
        "id": fm.get("id") or os.path.basename(d),
        "width": w * dpr,
        "height": h * dpr,
        "css": inline_css(app, dpr, w, ratio_class),
        "ratio_class": ratio_class,
    })
    ctx.setdefault("business", "")
    ctx.setdefault("tone", "")
    for key in ("image", "before_image", "after_image"):
        if ctx.get(key):
            ctx[key] = abs_file_url(ctx[key], d)
    if ctx.get("logo"):
        ctx["logo"] = abs_file_url(ctx["logo"], app)
    if isinstance(ctx.get("items"), list):
        ctx["items"] = [
            ({"n": f"{i + 1:02d}", "text": it} if isinstance(it, str) else {**{"n": f"{i + 1:02d}"}, **it})
            for i, it in enumerate(ctx["items"])
        ]

    html = render_template(open(tpl_path, encoding="utf-8").read(), ctx)
    html = html.replace('class="card', f'class="card {ratio_class}', 1)
    html_path = os.path.join(d, "render.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    if html_only:
        print(os.path.relpath(html_path, app))
        return

    binary = obscura_bin()
    if not binary:
        die("obscura is not installed (bash .claude/skills/creatives/setup.sh installs it); render.html was written", 2)
    shot = os.path.join(d, f"{out}.raw.png")
    env = dict(os.environ, OBSCURA_SHOT_W=str(w * dpr), OBSCURA_SHOT_H=str(h * dpr))
    url = "file://" + os.path.abspath(html_path)
    common_args = ["--allow-private-network", "--wait-until", "networkidle0", "--wait", "1", "--timeout", "45", "-q"]
    proc = subprocess.run([binary, "fetch", url, *common_args, "-s", shot], env=env, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0 or not os.path.isfile(shot):
        die(f"obscura failed ({proc.returncode}): {(proc.stderr or proc.stdout)[-800:]}")

    # the text boxes, measured in a second run of the same page at the same
    # viewport (the eval's JSON is easier to find on its own stdout)
    boxes = []
    try:
        ev = subprocess.run([binary, "fetch", url, *common_args, "-e", EVAL], env=env, capture_output=True, text=True, timeout=120)
        boxes = parse_boxes(ev.stdout, dpr)
    except (subprocess.SubprocessError, OSError):
        boxes = []

    try:
        from PIL import Image, ImageCms
    except ImportError:
        os.replace(shot, os.path.join(d, out))
        print(os.path.relpath(os.path.join(d, out), app) + " (Pillow missing: not downsampled)")
        return
    img = Image.open(shot).convert("RGB")
    img = img.crop((0, 0, w * dpr, h * dpr))
    if dpr != 1:
        img = img.resize((w, h), Image.LANCZOS)
    icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    target = os.path.join(d, out)
    img.save(target, "PNG", icc_profile=icc, optimize=True)
    os.remove(shot)

    fields["_boxes"] = boxes
    fields["size"] = f"{w}x{h}"
    fields["template"] = template
    with open(fields_path, "w", encoding="utf-8") as fh:
        json.dump(fields, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    if os.path.isfile(rec_path):
        files = list(fm.get("files") or [])
        if out not in files:
            files.append(out)
        fm["files"] = files
        write_record(rec_path, fm, body)
    print(f"{os.path.relpath(target, app)} {w}x{h} ({len(boxes)} text boxes measured)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="a creative folder or id")
    ap.add_argument("--all", choices=STATUSES, help="every creative in this status")
    ap.add_argument("--size")
    ap.add_argument("--template")
    ap.add_argument("--dpr", type=int, default=2)
    ap.add_argument("--out", default="master.png")
    ap.add_argument("--html-only", action="store_true")
    args = ap.parse_args()
    app = root()
    if args.all:
        for _, _, d in creative_dirs(app, [args.all]):
            if os.path.isfile(os.path.join(d, "fields.json")):
                render_one(app, d, args.size, args.template, args.dpr, args.out, args.html_only)
        return
    if not args.target:
        die("a creative folder or id, or --all <status>")
    d = args.target if os.path.isdir(args.target) else find_creative(app, args.target)[1]
    if not d:
        die(f"no creative {args.target}")
    render_one(app, d, args.size, args.template, args.dpr, args.out, args.html_only)


if __name__ == "__main__":
    main()
