#!/usr/bin/env python3
"""The creatives board (CREATIVES.md): list, move, and apply decisions.

    python3 scripts/status.py list [--status generated]
    python3 scripts/status.py move <id> <status> [--note "…"] [--by owner]
                              [--scheduled-for 2026-09-12T09:00:00+01:00] [--post-url URL]
    python3 scripts/status.py apply            # inbox/decisions/*.md from a portal or publisher

`move` moves the folder creatives/<from>/<id> to creatives/<status>/<id>,
sets `status`, appends to `history`, and sets `scheduled_for` / `posted_at`
+ `post_url` when the step needs them (and refuses the step without them).
`apply` reads every decision file not yet applied (inbox/.applied.json
remembers which), moves the creative, records the note, and prints what
changed; a `comment` moves nothing.
"""

import argparse
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (STATUSES, creative_dirs, die, find_creative, now_iso, read_record,  # noqa: E402
                    root, write_record)


def cmd_list(app, status):
    rows = creative_dirs(app, [status] if status else None)
    if not rows:
        print("no creatives yet (scripts/new.py makes one)")
        return
    width = max(len(name) for _, name, _ in rows)
    for st, name, d in rows:
        fm, _ = read_record(os.path.join(d, "creative.md"))
        extra = ""
        if st == "scheduled" and fm.get("scheduled_for"):
            extra = f"  for {fm['scheduled_for']}"
        if st == "posted" and fm.get("post_url"):
            extra = f"  {fm['post_url']}"
        print(f"{st:<10} {name:<{width}}  {fm.get('platform', '?'):<9} {fm.get('kind', '?'):<8} {fm.get('title', '')}{extra}")


def move(app, cid, to, note=None, by="owner", scheduled_for=None, post_url=None):
    if to not in STATUSES:
        die(f"status must be one of {', '.join(STATUSES)}")
    frm, d = find_creative(app, cid)
    if not d:
        die(f"no creative with id {cid}")
    path = os.path.join(d, "creative.md")
    fm, body = read_record(path)
    if to in ("approved", "scheduled", "posted") and fm.get("kind") in ("static", "carousel") and not fm.get("files"):
        die(f"{to} needs a rendered file first (render.py); a {fm.get('kind')} with nothing to show is not approvable")
    if to == "scheduled" and not (scheduled_for or fm.get("scheduled_for")):
        die("scheduled needs --scheduled-for (ISO 8601 with an offset)")
    if to == "posted" and not (post_url or fm.get("post_url")):
        die("posted needs --post-url")
    if scheduled_for:
        fm["scheduled_for"] = scheduled_for
    if post_url:
        fm["post_url"] = post_url
    if to == "posted" and not fm.get("posted_at"):
        fm["posted_at"] = now_iso()
    entry = {"status": to, "at": now_iso(), "by": by}
    if note:
        entry["note"] = note
    fm["status"] = to
    fm["history"] = list(fm.get("history") or []) + [entry]
    write_record(path, fm, body)
    if frm != to:
        dest = os.path.join(app, "creatives", to, cid)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.exists(dest):
            die(f"{dest} already exists")
        shutil.move(d, dest)
    return frm, to


def comment(app, cid, note, by):
    _, d = find_creative(app, cid)
    if not d:
        die(f"no creative with id {cid}")
    path = os.path.join(d, "creative.md")
    fm, body = read_record(path)
    fm["history"] = list(fm.get("history") or []) + [{"status": fm.get("status"), "at": now_iso(), "by": by, "note": note}]
    write_record(path, fm, body)


def cmd_apply(app):
    inbox = os.path.join(app, "inbox", "decisions")
    if not os.path.isdir(inbox):
        print("no inbox/decisions folder; nothing to apply")
        return
    applied_path = os.path.join(app, "inbox", ".applied.json")
    applied = set()
    if os.path.isfile(applied_path):
        applied = set(json.load(open(applied_path)))
    changed = []
    for name in sorted(os.listdir(inbox)):
        if not name.endswith(".md") or name in applied:
            continue
        fm, body = read_record(os.path.join(inbox, name))
        if fm.get("type") != "decision" or not fm.get("creative") or not fm.get("decision"):
            print(f"skipped {name}: not a decision (type, creative, decision)")
            continue
        cid, decision, by = fm["creative"], fm["decision"], str(fm.get("by") or "portal")
        note = body.strip() or None
        try:
            if decision == "approve":
                move(app, cid, "approved", note, by)
            elif decision == "reject":
                move(app, cid, "rejected", note, by)
            elif decision == "schedule":
                move(app, cid, "scheduled", note, by, scheduled_for=fm.get("scheduled_for"))
            elif decision == "posted":
                move(app, cid, "posted", note, by, post_url=fm.get("post_url"))
            elif decision == "comment":
                comment(app, cid, note or "(no text)", by)
            else:
                print(f"skipped {name}: unknown decision {decision}")
                continue
        except SystemExit as e:
            print(f"could not apply {name}: {e}")
            continue
        applied.add(name)
        changed.append((cid, decision, by, note))
    with open(applied_path, "w") as fh:
        json.dump(sorted(applied), fh, indent=2)
    if not changed:
        print("nothing new to apply")
    for cid, decision, by, note in changed:
        print(f"{decision:<8} {cid}  by {by}" + (f"  note: {note[:80]}" if note else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.add_argument("--status", choices=STATUSES)
    p = sub.add_parser("move")
    p.add_argument("id")
    p.add_argument("status", choices=STATUSES)
    p.add_argument("--note")
    p.add_argument("--by", default="owner")
    p.add_argument("--scheduled-for")
    p.add_argument("--post-url")
    sub.add_parser("apply")
    args = ap.parse_args()
    app = root()
    if args.cmd == "list":
        cmd_list(app, args.status)
    elif args.cmd == "move":
        frm, to = move(app, args.id, args.status, args.note, args.by, args.scheduled_for, args.post_url)
        print(f"{args.id}: {frm} -> {to}")
    elif args.cmd == "apply":
        cmd_apply(app)


if __name__ == "__main__":
    main()
