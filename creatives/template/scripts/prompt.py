#!/usr/bin/env python3
"""Assemble the image prompt for a creative: the format's universal visual
guide (prompts/<format>.md) with its brand slots filled from the notes,
the general design language, and the brief's offer.

    python3 scripts/prompt.py --format before-after --side before [--campaign <slug>] [--out prompt.txt]
    python3 scripts/prompt.py --format photo --subject "the finished work" [--json]
    python3 scripts/prompt.py --slots                # what the brand notes fill, and what is missing

The slots ({subject}, {setting}, {light}, {materials}, {people}, {never},
{anchor}) come from brand/visual-identity.md → Imagery; {offer} and
{audience_place} from the campaign's brief.md and brand/audience.md. A
slot the notes do not fill is printed as a question, never guessed; pass
--subject / --setting / … to fill one for this prompt. The output is the
prompt the AI hands to scripts/imagegen.py (which appends the no-text
rule), edited by hand when the moment needs it.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import die, read_record, root  # noqa: E402

SLOT_LABELS = {
    "subject": ["what the owner's photography shows", "photography the business owns", "subjects"],
    "setting": ["settings", "setting"],
    "light": ["light"],
    "materials": ["materials and objects that carry the brand", "materials"],
    "people": ["people"],
    "never": ["never shows", "what it never shows", "never"],
    "anchor": ["style anchor"],
}
DEFAULTS = {
    "people": "The scene is empty of people",
}


def imagery_slots(app):
    """{slot: text} from the Imagery block's bold bullets; unfilled ones absent."""
    note = os.path.join(app, "brand", "visual-identity.md")
    if not os.path.isfile(note):
        return {}
    text = open(note, encoding="utf-8").read()
    block = text.split("## Imagery")[1].split("\n## ")[0] if "## Imagery" in text else ""
    found = {}
    for line in block.splitlines():
        m = re.match(r"^\s*-\s*\*\*([^*]+):\*\*\s*(.*)$", line)
        if not m:
            continue
        label, value = m.group(1).strip().lower(), m.group(2).strip()
        if not value or "to fill" in value:
            continue
        for slot, labels in SLOT_LABELS.items():
            if any(label.startswith(l) for l in labels) and slot not in found:
                # slots sit mid-sentence, so they lose their full stop; the anchor is whole sentences and keeps it
                found[slot] = value if slot == "anchor" else value.rstrip(".")
    return found


def brief_slots(app, campaign):
    out = {}
    if not campaign:
        cur = os.path.join(app, "campaigns", "CURRENT")
        if os.path.isfile(cur):
            campaign = open(cur, encoding="utf-8").read().strip()
    if campaign:
        brief = os.path.join(app, "campaigns", campaign, "brief.md")
        if os.path.isfile(brief):
            fm, _ = read_record(brief)
            product = fm.get("product")
            if isinstance(product, str) and product and "to fill" not in product:
                out["offer"] = product
    aud = os.path.join(app, "brand", "audience.md")
    if os.path.isfile(aud):
        text = open(aud, encoding="utf-8").read()
        m = re.search(r"\*\*Where they are when it matters:\*\*\s*(.+)", text) or re.search(r"\*\*Who they are:\*\*\s*(.+)", text)
        if m and "to fill" not in m.group(1):
            out["audience_place"] = m.group(1).strip().rstrip(".")
    return out


def load_guide(app, fmt):
    path = os.path.join(app, "prompts", f"{fmt}.md")
    if not os.path.isfile(path):
        avail = sorted(f[:-3] for f in os.listdir(os.path.join(app, "prompts")) if f.endswith(".md") and not f.startswith("_"))
        die(f"no prompt guide for {fmt} (prompts/: {', '.join(avail)}); template-only formats need no picture")
    fm, body = read_record(path)
    return fm, body


def template_text(body, side=None):
    """The '## Prompt template' section (or '## Prompt template, <side>')."""
    sections = re.split(r"^## ", body, flags=re.M)
    wanted = None
    for sec in sections:
        title = sec.split("\n", 1)[0].strip().lower()
        if side and title == f"prompt template, {side}":
            wanted = sec
            break
        if not side and title == "prompt template":
            wanted = sec
    if not wanted and side:
        die(f"this guide has no 'Prompt template, {side}' section")
    if not wanted:
        die("this guide has no 'Prompt template' section")
    lines = [l for l in wanted.split("\n", 1)[1].strip().splitlines() if l.strip()]
    return " ".join(l.strip() for l in lines)


def fill(text, slots):
    missing = []

    def sub(m):
        key = m.group(1)
        if key in slots and slots[key]:
            return slots[key]
        missing.append(key)
        return "{" + key + "}"

    return re.sub(r"\{([a-z_]+)\}", sub, text), sorted(set(missing))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--format", help="prompts/<format>.md")
    ap.add_argument("--side", choices=["before", "after"], help="for before-after")
    ap.add_argument("--campaign")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--slots", action="store_true", help="print the slots the notes fill and exit")
    for slot in list(SLOT_LABELS) + ["offer", "audience_place", "style"]:
        ap.add_argument(f"--{slot}", help=f"fill {{{slot}}} for this prompt")
    args = ap.parse_args()
    app = root()

    slots = dict(DEFAULTS)
    slots.update(imagery_slots(app))
    slots.update(brief_slots(app, args.campaign))
    for slot in list(SLOT_LABELS) + ["offer", "audience_place", "style"]:
        v = getattr(args, slot)
        if v:
            slots[slot] = v

    if args.slots:
        for slot in list(SLOT_LABELS) + ["offer", "audience_place"]:
            print(f"{slot:<15} {slots.get(slot) or '(missing: fill brand/visual-identity.md Imagery, or pass --' + slot + ')'}")
        return
    if not args.format:
        die("--format is required (or --slots)")

    fm, body = load_guide(app, args.format)
    text, missing = fill(template_text(body, args.side), slots)
    # tidy the joins the slots leave behind
    text = re.sub(r"\s+", " ", text).replace(" .", ".").replace("..", ".").strip()
    if args.json:
        print(json.dumps({"format": args.format, "side": args.side, "prompt": text, "missing": missing, "templates": fm.get("templates")}, indent=2))
    else:
        print(text)
        if missing:
            print("\nslots the notes do not fill (ask the owner, or pass --<slot>): " + ", ".join(missing), file=sys.stderr)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")


if __name__ == "__main__":
    main()
