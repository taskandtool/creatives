# CREATIVES.md

What a creative is on disk, where it lives as it moves from made to posted,
and how another app (a client portal, a publisher) reads and answers it.
The scripts in `scripts/` implement this; the skills follow it; nothing
here is enforced by the platform, it is a convention between apps.

## One creative is one folder

```
creatives/<status>/<id>/
  creative.md        the record: typed frontmatter + the rationale (below)
  fields.json        what the template rendered: headline, body, cta, colours, image path
  render.html        the composed page the master was rendered from (regenerable)
  visual.png         the generated or supplied picture behind the words, if any
  master.png         the finished creative at its native size (e.g. 1080×1350)
  1x1.png 9x16.png … other placements, each composed or resized on purpose (scripts/resize.py)
  script.md          a video script, when the creative is a video
  slides/            carousel cards, numbered, each a PNG
```

`<id>` is `YYYY-MM-DD-<format>-<platform>-<nn>` (`scripts/new.py` makes it).
A creative never has two folders: moving it between statuses moves the
whole folder (`scripts/status.py move <id> approved`).

## The record: `creative.md`

Markdown with typed frontmatter, the same convention as the brain's notes
and the website's fact notes. Everything a portal or a publisher needs is in
the frontmatter; the body is for people.

```yaml
---
type: creative
id: 2026-09-07-us-vs-them-meta-01
title: Showroom kitchen vs workshop kitchen
campaign: autumn-kitchens           # campaigns/<slug>/
platform: meta                      # meta | linkedin | tiktok | google | pinterest | youtube | gbp
kind: static                        # static | carousel | video | post
format: us-vs-them                  # a name from static-ad/references/formats.md (or the post format)
angle: comparison                   # outcome | problem | social-proof | mechanism | comparison
awareness: cold                     # cold | warm | hot
ratio: "4:5"
files: [master.png, 1x1.png]
copy:
  headline: "Showroom kitchen. Workshop kitchen."
  primary_text: "One is drawn by a salesperson and fitted by whoever is free. The other is measured, drawn, built and fitted by the same two people."
  cta: "Book a workshop visit"
  caption: ""                        # organic posts
  hashtags: []                       # organic only; never in an ad
claims:                              # every factual claim on the creative, with its note
  - text: "built and fitted by the same two people"
    source: public/team.md
status: generated                    # generated | approved | scheduled | posted | rejected
history:
  - { status: generated, at: "2026-09-07T14:02:00Z", by: ai }
scheduled_for: null                  # ISO 8601 with offset, set by the owner or the publisher
posted_at: null
post_url: null
sources: [briefs/autumn-kitchens.md, brand/voice.md, public/team.md]
---

Why this creative: one paragraph, the angle and the hook and who it is for.

Visual prompt: the prompt sent to the image model, verbatim, when one was used.

Notes: anything the owner should know before approving (a claim to confirm,
a photo to replace).
```

Rules the scripts check (`scripts/check.py`):

- `type`, `id`, `platform`, `kind`, `format`, `status`, `files`, `copy`,
  `claims`, `history` are present; `id` matches the folder; `status` matches
  the folder it sits in.
- Every file in `files` exists; every entry in `claims` names a `source`
  that exists.
- The copy passes the copy gate (the writing rules the review skill
  enforces: no refused phrases, no em dashes, hashtags empty for ads) and
  the platform's length limits from `specs/<platform>.md`.
- `master.png` has the size the ratio and platform call for (`scripts/qa.py`).

## The statuses, as folders

```
creatives/generated/    made, not yet seen by the owner (or seen and not decided)
creatives/approved/     the owner (or the client through a portal) said yes
creatives/scheduled/    a publisher has a date for it (scheduled_for is set)
creatives/posted/       live; posted_at and post_url are set
creatives/rejected/     said no; kept with the reason in history, never reused as-is
```

`scripts/status.py list` prints the board. `status.py move <id> <status>
--note "…" --by owner` moves the folder and appends to `history`. Nothing
skips a step by accident: `posted` needs `post_url`, `scheduled` needs
`scheduled_for`, and a move backwards (approved → generated) is allowed with
a note.

## Talking to a client portal or a publisher

Folders are the interface, through the platform's mirrors (an app's folder
copied read-only into another app's folder, refreshed on change):

- **Outbound.** The portal mirrors `creatives/generated` (what needs a
  decision) and `creatives/approved` (what it may show as coming); a
  publisher mirrors `creatives/approved` and `creatives/scheduled`. They
  read `creative.md` and the PNGs. They never write into those folders.
- **Inbound: decisions.** A portal writes one file per decision into a
  folder of its own, which is mirrored onto this app's `inbox/decisions/`:

  ```yaml
  ---
  type: decision
  creative: 2026-09-07-us-vs-them-meta-01
  decision: approve                   # approve | reject | comment | schedule | posted
  by: "Jo Harlow (client)"
  at: "2026-09-08T09:15:00Z"
  scheduled_for: null                 # with `schedule`
  post_url: null                      # with `posted`
  ---
  The note, if any: "Swap the second line for the shorter one."
  ```

  `scripts/status.py apply` reads every decision not yet applied (it keeps
  `inbox/.applied.json`), moves the creative, appends the note to its
  history, and lists what changed so the AI can act on comments. A
  `comment` moves nothing; it lands in the creative's history and the AI
  answers it with a revision (a new creative, or the same id re-rendered
  while it is still in `generated`).

Until a portal exists the owner is the client: they approve in chat, and
the AI runs `status.py move`. The decision file format is the contract a
portal will write to; nothing about it is platform code.

## What a publisher needs from `creative.md`

`platform`, `kind`, `files` (which file is which placement, by name),
`copy` (the fields the platform's API takes: for Meta `primary_text`,
`headline`, `cta`; for LinkedIn `primary_text` as the intro and `headline`;
for organic posts `caption` and `hashtags`), `scheduled_for`. A publisher
that posts writes back `posted` with `post_url` as a decision file, or the
owner tells the AI.
