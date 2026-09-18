#!/usr/bin/env python3
"""The app's own checks (CREATIVES.md, DESIGN.md, the specs), run before
showing work:

    python3 scripts/check.py [--status generated] [<id> …]

- the brand notes and the fact notes the creatives draw on exist
- every creative.md has the required fields, its id matches its folder, its
  status matches the folder it sits in, every listed file exists, every
  claim names a source that exists, history is a list
- the copy gate: no refused phrases, no em dashes, hashtags empty on an ad,
  Meta's personal-attributes phrasings absent, the platform's length limits
  (specs/<platform>.md) respected
- the specs are not stale (last_verified within 90 days)
- the rendered master has the right size (delegated to qa.py when present)

Exit 1 with the findings when something is off.
"""

import argparse
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (KINDS, PLATFORMS, STATUSES, copy_findings, creative_dirs, read_record, root)  # noqa: E402

REQUIRED = ["type", "id", "platform", "kind", "format", "status", "files", "copy", "claims", "history"]

# the text limits the specs state; check.py holds the ones that are hard
# limits or "See more" cutoffs (specs/*.md carry the sources)
LIMITS = {
    "meta": {"headline": (40, "Meta headline shows 40 characters (27 on the Facebook feed)"),
             "primary_text": (125, "Meta primary text shows about 125 characters before See more"),
             "description": (25, "Meta description shows 25 characters")},
    "linkedin": {"headline": (70, "LinkedIn headline: 70 recommended, 200 max"),
                 "primary_text": (150, "LinkedIn intro text: 150 recommended, 600 max")},
    "tiktok": {"caption": (100, "TikTok ad caption: 100 max, about 45 visible")},
    "google": {"headline": (30, "Google headline: 30 max"), "primary_text": (90, "Google description: 90 max")},
    "pinterest": {"headline": (100, "Pinterest title: 100 max, about 40 visible"), "primary_text": (500, "Pinterest description: 500 max")},
    "youtube": {"headline": (70, "YouTube title: about 70 visible")},
    "gbp": {"primary_text": (1500, "Google Business Profile post: 1,500 max")},
}
HARD = {"linkedin": {"headline": 200, "primary_text": 600}, "meta": {"headline": 40}, "tiktok": {"caption": 100},
        "google": {"headline": 30, "primary_text": 90}, "pinterest": {"headline": 100, "primary_text": 500}}


def check_creative(app, status, cid, d, findings):
    path = os.path.join(d, "creative.md")
    fm, body = read_record(path)
    rel = os.path.relpath(path, app)
    for k in REQUIRED:
        if k not in fm:
            findings.append(f"{rel}: missing `{k}`")
    if fm.get("type") != "creative":
        findings.append(f"{rel}: type must be creative")
    if fm.get("id") != cid:
        findings.append(f"{rel}: id {fm.get('id')!r} does not match the folder {cid}")
    if fm.get("status") != status:
        findings.append(f"{rel}: status {fm.get('status')!r} but the folder is creatives/{status}/")
    if fm.get("platform") not in PLATFORMS:
        findings.append(f"{rel}: platform must be one of {', '.join(PLATFORMS)}")
    if fm.get("kind") not in KINDS:
        findings.append(f"{rel}: kind must be one of {', '.join(KINDS)}")
    if not isinstance(fm.get("history"), list) or not fm.get("history"):
        findings.append(f"{rel}: history must be a non-empty list")
    files = fm.get("files") or []
    if not isinstance(files, list):
        findings.append(f"{rel}: files must be a list")
        files = []
    for f in files:
        if not os.path.isfile(os.path.join(d, str(f))):
            findings.append(f"{rel}: listed file {f} is missing")
    if status in ("approved", "scheduled", "posted") and fm.get("kind") in ("static", "carousel") and not files:
        findings.append(f"{rel}: a {status} {fm.get('kind')} must list its rendered files")
    for c in fm.get("claims") or []:
        src = c.get("source") if isinstance(c, dict) else None
        if not src:
            findings.append(f"{rel}: a claim has no source ({c!r})")
        elif not os.path.exists(os.path.join(app, str(src).split("#")[0])):
            findings.append(f"{rel}: claim source {src} does not exist")
    if "to fill" in body:
        findings.append(f"{rel}: the body still says 'to fill'")

    copy = fm.get("copy") or {}
    if not isinstance(copy, dict):
        findings.append(f"{rel}: copy must be a map")
        return
    is_ad = fm.get("kind") in ("static", "carousel", "video")
    hashtags = copy.get("hashtags") or []
    if is_ad and hashtags:
        findings.append(f"{rel}: an ad carries no hashtags (they are an exit)")
    for field, text in copy.items():
        if not isinstance(text, str) or not text:
            continue
        for rule, match in copy_findings(text, ad=is_ad):
            findings.append(f"{rel}: copy.{field}: {rule}: \"{match}\"")
        if field == "cta" and re.match(r"^(learn more|click here|read more|find out more)$", text.strip(), re.I):
            findings.append(f"{rel}: copy.cta \"{text}\" says nothing; a verb and an object")
    if is_ad and copy.get("headline") and len(copy["headline"].split()) > 12:
        findings.append(f"{rel}: copy.headline is {len(copy['headline'].split())} words; twelve or fewer on a creative")
    platform = fm.get("platform")
    for field, (limit, why) in LIMITS.get(platform, {}).items():
        text = copy.get(field)
        if isinstance(text, str) and len(text) > limit:
            hard = HARD.get(platform, {}).get(field)
            if hard and len(text) > hard:
                findings.append(f"{rel}: copy.{field} is {len(text)} characters, over the limit ({why})")
            elif not hard or len(text) > limit:
                # past what shows before the fold: fine when the words earn it, so a note, not a finding
                print(f"note: {rel}: copy.{field} is {len(text)} characters, past the visible cutoff ({why})")


def check_specs(app, findings):
    specs = os.path.join(app, "specs")
    if not os.path.isdir(specs):
        findings.append("specs/ is missing (the platform sheets)")
        return
    for name in sorted(os.listdir(specs)):
        if not name.endswith(".md") or name == "README.md":
            continue
        fm, _ = read_record(os.path.join(specs, name))
        lv = fm.get("last_verified")
        try:
            d = date.fromisoformat(str(lv))
        except (TypeError, ValueError):
            findings.append(f"specs/{name}: last_verified must be a date")
            continue
        if (date.today() - d).days > 90:
            print(f"note: specs/{name} was last verified {lv}, over 90 days ago; re-verify before building against it")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--status", choices=STATUSES)
    args = ap.parse_args()
    app = root()
    findings = []

    for f in ["brand/voice.md", "brand/visual-identity.md", "brand/positioning.md", "public/business.md", "public/proof.md", "DESIGN.md", "CREATIVES.md", "templates/brand.css"]:
        if not os.path.exists(os.path.join(app, f)):
            findings.append(f"{f} is missing")
    if os.path.exists(os.path.join(app, "brand", "_mirror.md")):
        print("note: brand/ is a mirror; change brand facts at the source, then re-apply them here")

    check_specs(app, findings)
    rows = creative_dirs(app, [args.status] if args.status else None)
    if args.ids:
        rows = [r for r in rows if r[1] in args.ids]
        missing = set(args.ids) - {r[1] for r in rows}
        for m in missing:
            findings.append(f"no creative with id {m}")
    for status, cid, d in rows:
        check_creative(app, status, cid, d, findings)

    # the rendered masters, when qa.py and Pillow are available
    try:
        import qa  # noqa: F401
        for status, cid, d in rows:
            if os.path.isfile(os.path.join(d, "master.png")):
                findings.extend(f"{cid}: {f}" for f in qa.check_dir(app, d))
    except ImportError:
        pass

    if findings:
        print(f"check: {len(findings)} finding(s)\n  - " + "\n  - ".join(findings), file=sys.stderr)
        sys.exit(1)
    print(f"check: ok ({len(rows)} creative(s))")


if __name__ == "__main__":
    main()
