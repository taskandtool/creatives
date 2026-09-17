#!/usr/bin/env python3
"""Scaffold one creative under creatives/generated/ (CREATIVES.md).

    python3 scripts/new.py --platform meta --kind static --format us-vs-them \
        --campaign autumn-kitchens --ratio 4:5 --title "Showroom vs workshop" \
        [--angle comparison] [--awareness cold] [--template us-vs-them]

Makes creatives/generated/<YYYY-MM-DD-format-platform-nn>/ with creative.md
(the record, status generated, an empty claims ledger) and fields.json (the
template's fields, with the brand name filled from public/business.md and
the rest left for the AI to write). Prints the folder. The record's copy
and the fields are written by the AI next; render.py turns fields.json into
master.png.
"""

import argparse
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ANGLES, AWARENESS, KINDS, PLATFORMS, RATIOS, die, now_iso, read_record,  # noqa: E402
                    root, write_record)

TEMPLATE_FIELDS = {
    "statement": {"headline": "", "body": "", "cta": "", "tone": ""},
    "photo": {"image": "visual.png", "headline": "", "body": "", "cta": ""},
    "quote": {"quote": "", "who": "", "where": "", "cta": "", "tone": ""},
    "us-vs-them": {"headline": "", "left_label": "Them", "right_label": "Us", "rows": [{"left": "", "right": ""}], "cta": "", "tone": ""},
    "before-after": {"before_image": "before.png", "after_image": "after.png", "before_label": "Before", "after_label": "After", "headline": "", "cta": "", "stacked": False, "tone": ""},
    "offer": {"headline": "", "includes": [""], "price": "", "was": "", "deadline": "", "cta": "", "tone": ""},
    "listicle": {"headline": "", "items": [{"n": "01", "text": ""}], "cta": "", "tone": ""},
    "product": {"image": "visual.png", "headline": "", "label": "", "cta": "", "ground": ""},
    "checklist": {"headline": "", "items": [{"text": "", "done": True}], "cta": "", "tone": ""},
    "note": {"text": "", "signoff": ""},
    "screenshot": {"thread": {"messages": [{"text": "", "mine": False}]}, "notification": None, "review": None, "comment": None, "app": None},
    "banner": {"offer": "", "headline": "", "terms": "", "cta": "", "ground": ""},
    "snapshot": {"image": "visual.png", "caption": ""},
    "steps": {"headline": "", "steps": [{"n": "1", "title": "", "text": ""}], "cta": "", "tone": ""},
    "proof-stack": {"rating": "", "count": "", "source": "", "quotes": [{"text": "", "who": ""}], "cta": "", "tone": ""},
    "grid": {"headline": "", "columns": 2, "cells": [{"image": "", "text": ""}], "cta": "", "tone": ""},
    "stats": {"headline": "", "stats": [{"value": "", "label": ""}], "source": "", "cta": "", "tone": ""},
}

# the template a format defaults to (formats.md names the rest explicitly)
FORMAT_TEMPLATES = {
    "statement": "statement", "big-statistic": "statement", "problem-agitate-solve": "statement",
    "who-its-for": "statement", "founder-note": "note", "sticky-note": "note",
    "testimonial": "quote", "quote": "quote", "review": "screenshot", "native-ui": "screenshot",
    "us-vs-them": "us-vs-them", "myth-vs-fact": "us-vs-them", "before-after": "before-after",
    "offer": "offer", "price-anchor": "offer", "listicle": "listicle", "reasons-why": "listicle",
    "checklist": "checklist", "product": "product", "photo": "photo", "faq": "listicle",
    "offer-first": "banner", "sale": "banner", "urgency": "banner", "giveaway": "banner",
    "headline-only": "statement", "text-only": "statement", "bold-claim": "statement", "editorial": "photo",
    "lifestyle": "photo", "product-in-use": "photo", "ugc-photo": "snapshot", "ugly-ad": "snapshot",
    "how-it-works": "steps", "mechanism": "steps", "infographic": "steps",
    "social-proof-mashup": "proof-stack", "trust-stack": "proof-stack", "expert-endorsement": "quote", "celebrity": "quote",
    "comment-response": "screenshot", "app-mockup": "screenshot", "ui-mockup": "screenshot",
    "starter-pack": "grid", "education-grid": "grid", "collage": "grid", "grid-swap": "grid", "flat-lay": "product",
    "benefit-stack": "checklist", "value-prop": "checklist", "specs": "checklist",
    "case-study": "stats", "results": "stats", "three-stat": "stats", "objection-led": "us-vs-them",
    "text-in-context": "photo", "illustration": "photo", "badge": "statement",
}


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:40] or "creative"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--platform", required=True, choices=PLATFORMS)
    ap.add_argument("--kind", default="static", choices=KINDS)
    ap.add_argument("--format", required=True, help="a name from static-ad/references/formats.md, or the post format")
    ap.add_argument("--campaign", required=True, help="campaigns/<slug>/")
    ap.add_argument("--ratio", default="4:5", choices=sorted(RATIOS))
    ap.add_argument("--title", required=True)
    ap.add_argument("--angle", default="outcome", choices=ANGLES)
    ap.add_argument("--awareness", default="cold", choices=AWARENESS)
    ap.add_argument("--template", help="templates/<name>.html (default: the format's usual one)")
    args = ap.parse_args()

    app = root()
    fmt = slug(args.format)
    template = args.template or FORMAT_TEMPLATES.get(fmt, "statement")
    if template not in TEMPLATE_FIELDS:
        die(f"no template named {template}; templates/: {', '.join(sorted(TEMPLATE_FIELDS))}")

    base = os.path.join(app, "creatives", "generated")
    os.makedirs(base, exist_ok=True)
    today = date.today().isoformat()
    prefix = f"{today}-{fmt}-{args.platform}-"
    existing = [d for d in os.listdir(base) if d.startswith(prefix)] + [
        d for s in ("approved", "scheduled", "posted", "rejected")
        if os.path.isdir(os.path.join(app, "creatives", s))
        for d in os.listdir(os.path.join(app, "creatives", s)) if d.startswith(prefix)
    ]
    cid = f"{prefix}{len(existing) + 1:02d}"
    folder = os.path.join(base, cid)
    os.makedirs(folder)

    business = ""
    biz_note = os.path.join(app, "public", "business.md")
    if os.path.isfile(biz_note):
        fm, _ = read_record(biz_note)
        if isinstance(fm.get("name"), str) and fm["name"] not in ("", "to fill"):
            business = fm["name"]

    w, h = RATIOS[args.ratio]
    fields = {"template": template, "size": f"{w}x{h}", "business": business or "to fill", "logo": ""}
    fields.update(TEMPLATE_FIELDS[template])
    with open(os.path.join(folder, "fields.json"), "w", encoding="utf-8") as fh:
        json.dump(fields, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    record = {
        "type": "creative",
        "id": cid,
        "title": args.title,
        "campaign": args.campaign,
        "platform": args.platform,
        "kind": args.kind,
        "format": fmt,
        "angle": args.angle,
        "awareness": args.awareness,
        "ratio": args.ratio,
        "files": [],
        "copy": {"headline": "", "primary_text": "", "cta": "", "caption": "", "hashtags": []},
        "claims": [],
        "status": "generated",
        "history": [{"status": "generated", "at": now_iso(), "by": "ai"}],
        "scheduled_for": None,
        "posted_at": None,
        "post_url": None,
        "sources": [f"campaigns/{args.campaign}/brief.md", "brand/voice.md"],
    }
    body = (
        "Why this creative: to fill (the angle, the hook, who it is for).\n\n"
        "Visual prompt: to fill, or \"none\" when the template carries the visual.\n\n"
        "Notes: to fill (anything the owner should confirm before approving).\n"
    )
    write_record(os.path.join(folder, "creative.md"), record, body)
    print(os.path.relpath(folder, app))


if __name__ == "__main__":
    main()
