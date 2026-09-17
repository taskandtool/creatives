---
description: "Make and manage ad creatives and social posts for this business: the app's shape (brand and fact notes, the brief, the specs, the templates, the board of creatives from generated to posted), the scripts that render, generate, check and move them, and the loop of showing work in chat. Use for any creative work here and when the owner says make an ad, make some posts, show me options, what is waiting for approval, or what did we post."
---

# Creatives

This app makes the material and never posts it. A creative is one folder
under `creatives/<status>/` with a `creative.md` record beside its files
(`CREATIVES.md` is the contract); the brand lives in `brand/` and the facts
in `public/` (the website's shapes, so a Company Brain or a website can own
them by mirror; the `sources` skill fills them otherwise); `DESIGN.md` is
the design contract for anything rendered; `specs/<platform>.md` are the
sizes, limits and policy notes with a `last_verified` date. The other
skills are the crafts: `brief`, `angles`, `static-ad`, `carousel`,
`video-script`, `social-post`, `research`, `review`, `results`.

## Setup on this machine

`setup.sh` beside this file seeds the app from `template/` into an empty
app directory, initialises git, installs Pillow and requests, the Obscura
headless browser (the renderer), and `tt-crawl` (the site reader the
`sources` skill uses). It is idempotent:

```bash
bash ${CLAUDE_SKILL_DIR}/setup.sh
```

Check the tools before the first render:

```bash
obscura --version && python3 -c "import PIL, requests; print('ok')"
python3 scripts/imagegen.py --check          # which image model has a key (exit 3: none yet)
```

## The loop

1. **Sources.** `brand/` and `public/` are filled: mirrored from a brain or
   a website (`_mirror.md` present), or written by the `sources` skill.
   Nothing is made from notes still marked "to fill".
2. **Brand into the templates.** "Updating from the brand" in `DESIGN.md`:
   `templates/brand.css` (colours as hex, the roles), the fonts
   (`python3 scripts/fonts.py --from-brand`, or a licensed font by hand),
   the logo file. `python3 scripts/qa.py --tokens` must pass.
3. **Brief and angles.** `campaigns/<slug>/brief.md` agreed with the owner
   (`brief` skill), `angles.md` and `claims.md` (`angles` skill),
   `campaigns/CURRENT` set to the slug.
4. **Make.** The craft skill for the deliverable. Each creative:
   `scripts/new.py` → write `creative.md` (copy, claims, the rationale) and
   `fields.json` → `scripts/imagegen.py` when the template takes a visual
   → `scripts/render.py` → `scripts/resize.py` → `scripts/qa.py`.
5. **Check and show.** `python3 scripts/check.py` (records, the copy gate,
   the limits, the specs) must say ok. Then attach the masters to your
   reply so the owner sees them in the chat and can click to enlarge:

   ```python
   from tools.taskandtool import attach_files
   attach_files(["creatives/generated/<id>/master.png", …], "Three angles for the autumn campaign")
   ```

   Ask one question: which to approve, what to change.
6. **Decide.** The owner's answer moves the creative: `python3
   scripts/status.py move <id> approved --note "…"` (or `rejected` with the
   reason). A client portal's or a publisher's answers arrive as files in
   `inbox/decisions/`; `python3 scripts/status.py apply` takes them in and
   prints the comments to act on.
7. **Schedule and post** happen elsewhere: a publisher app reads
   `creatives/approved/` by mirror, or the owner posts by hand and tells
   you the URL (`status.py move <id> posted --post-url …`). Never post from
   here.
8. **Results.** When the owner has the numbers (or an ad-account
   connection gives them), the `results` skill writes
   `campaigns/<slug>/results.md` and says what to iterate.

`python3 scripts/status.py list` is the board at any time.

## Rules the scripts enforce, so you do not have to remember them

- A record without its required fields, a claim without a source, a file
  listed but missing, copy with a refused phrase or an em dash, hashtags on
  an ad, a headline over twelve words, text over the platform's cutoff:
  `check.py` fails.
- A master at the wrong size, over the byte limit, text on pixels under
  3:1, text inside the 9:16 UI zone: `qa.py` fails.
- Approving a static or a carousel with nothing rendered, scheduling
  without a date, posting without a URL: `status.py` refuses.
- A spec sheet older than 90 days: `check.py` says so; re-verify it
  against the platform's help page and update `last_verified` before
  building against it.

## Images

The template carries the words, the logo and the colours; an image model
only ever paints the scene (`DESIGN.md`: Refuse). `scripts/imagegen.py`
uses whichever provider has a key in the environment (OpenRouter, Gemini,
Black Forest Labs, fal, OpenAI, in that order) and appends the no-text
rule to every prompt. Without one, ask the owner once, through
Connections, never in chat:

```python
from tools.taskandtool import request_connection
request_connection("openrouter", why="generate the pictures behind the ads (one key covers Gemini, GPT Image and FLUX)", auth="api_key", delivery="machine")
```

The key lands in `~/.env` as `OPENROUTER_API_KEY` after the owner grants
it; a Gemini key (`gemini` → `GEMINI_API_KEY`) or a fal key work the same
way. Until then, make the creatives that need no picture (`statement`,
`quote`, `us-vs-them`, `offer`, `listicle`, `checklist`, `note`,
`screenshot`) and the ones that use the owner's own photos.

Real photographs beat generated ones every time they exist: the owner's
work, place, product, people (with permission). Ask for them first.

## Showing work

Never describe a creative when you can show it. Attach the master (and
the phone-size placement when it differs) with a one-line caption naming
the angle and the format. For a set, attach up to six in one call, in the
order the owner should read them, and say what differs between them in
one line each. Screenshots of a rendered page (a carousel in sequence)
go through `uploads/` (ignored by git).

## Git

Commit at milestones with short plain messages: a batch made, a batch
approved, results in. Never commit `uploads/`, `render.html`, or any
credential. Font files under `templates/fonts/` are fine.
