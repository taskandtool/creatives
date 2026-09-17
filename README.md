# Creatives

A Task & Tool **Starter App**: ad creatives and social posts for one
business, made on its own machine from its brand and its facts, and
approved before anything is posted. It makes the material; it never
posts. The outputs are files the owner reviews in chat, a client approves
through a portal, and a publisher posts.

Built for Claude Code. Installed with one click on Task & Tool, or dropped
into any project by hand (below). MIT licensed.

## What is in the box

```
creatives/       the shape, the loop and the scripts; setup.sh; template/ (the app that is copied in on install)
sources/         the brand and fact notes: mirrored from a Company Brain or a website, or collected here (tt-crawl)
brief/           the campaign brief, agreed with the owner before the first creative
angles/          angles and the claims ledger; the 3×3 starter set (references/strategy.md)
static-ad/       one image, one idea: 45 formats as recipes, drawn from every published catalogue
                 (references/formats.md, which says where the list comes from) and the
                 image-prompt craft with the brand's style anchor (references/visual-prompts.md)
carousel/        swipe posts, LinkedIn documents, carousel ads
video-script/    hooks, the ten structures with beat timings, slideshow cuts (references/hooks.md)
social-post/     organic posts per platform (references/<platform>.md, repurpose.md)
research/        competitor ads through an Apify or Foreplay connection; the swipe file and the winner score
review/          the copy gate, the claims, the specs, the render, the voice
results/         the numbers against angle, format and hook; what to iterate
starter-app.json the manifest Task & Tool reads: name, blurb, directive, state-aware suggestions
```

Each `<skill>/SKILL.md` is a Claude Code skill; the references beside them
are what the skill points at when it needs the detail. The scripts in
`creatives/template/scripts/` are plain Python (Pillow and requests, which
`setup.sh` installs). Tests sit beside the code (`creatives/test_scripts.py`)
and never ship to a machine.

## The app it makes

```
brand/  public/         the brand and fact notes (the website's shapes; a brain or a website can own them by mirror)
DESIGN.md               the design contract: tokens in templates/brand.css, type at 1080 wide, compositions, refuse list
CREATIVES.md            what a creative is on disk and how it moves; the portal's decision record
specs/<platform>.md     sizes, limits, safe zones, policy, each with a last_verified date (90 days, then re-verify)
campaigns/<slug>/       brief.md · angles.md · claims.md · results.md;  campaigns/CURRENT names the one in hand
creatives/<status>/<id>/   creative.md (typed frontmatter) + master.png, placements, slides/, script.md, cut.mp4
inbox/decisions/        a portal's or a publisher's answers, arriving by mirror; status.py apply takes them in
media/                  the business's own photographs and clips: uploaded, or mirrored from a brain or
                        website (photos/, clips/, _index.json, _notes.md for what may be used)
swipe/                  saved competitor and reference creatives, tagged
prompts/                the universal visual guide per format, with the slots the brand fills (scripts/prompt.py)
templates/              seventeen HTML compositions the renderer fills; brand.css; fonts/
scripts/                new · prompt · render · imagegen · videogen · captions · media · resize · qa · check · status · carousel · video · fonts
```

The board is folders: `generated → approved → scheduled → posted` (or
`rejected`), one folder per creative, moved by `scripts/status.py`. A client
portal mirrors `creatives/generated` to show what needs a decision and
writes decision files back into `inbox/decisions/`; a publisher mirrors
`creatives/approved`. Mirrors are a platform feature; the folder shapes are
this repo's convention.

## How a creative is made

The template carries the words, the logo and the colours; an image model
only ever paints the scene. `render.py` fills an HTML template from
`fields.json`, renders it through the Obscura headless browser at 2x, and
downsamples to the platform's size; `imagegen.py` asks whichever image
model the app has a key for (OpenRouter, Gemini, Black Forest Labs, fal,
OpenAI, in that order, with the no-text rule appended to every prompt);
`qa.py` measures the token pairs, the size, the bytes, the contrast behind
every text box and the 9:16 safe zone; `check.py` validates every record,
the claims against their sources, the copy gate (the phrases and shapes
generated text falls into, em dashes, hashtags on ads, Meta's
personal-attributes phrasings) and the platform's text limits.

## Install

**On Task & Tool.** Pick Creatives from the Starter Apps: as a new app in a
project, or into an existing app from its Settings. The platform copies the
skill folders into the app, runs `setup.sh`, and tells the AI what arrived.

**Anywhere else.** The same thing by hand, in an empty directory where
Claude Code runs:

```
git clone https://github.com/taskandtool/creatives /tmp/creatives
mkdir -p .claude/skills
cp -R /tmp/creatives/creatives /tmp/creatives/sources /tmp/creatives/brief /tmp/creatives/angles \
      /tmp/creatives/static-ad /tmp/creatives/carousel /tmp/creatives/video-script /tmp/creatives/social-post \
      /tmp/creatives/research /tmp/creatives/review /tmp/creatives/results .claude/skills/
bash .claude/skills/creatives/setup.sh
```

`setup.sh` seeds the app, installs Pillow, requests and tt-crawl with pip,
and the Obscura binary for Linux x86_64 or aarch64 (elsewhere `render.py`
writes the HTML and stops). Off the platform, `attach_files` (the bridge
that puts a file into the Task & Tool chat) is not there; the rendered
files are on disk.

## Third-party tools it installs

- [Obscura](https://github.com/h4ckf0r0day/obscura), Apache-2.0, a Rust
  headless browser with its own rendering engine. It renders every creative;
  it loads no system fonts, so the brand's fonts go through `templates/fonts/`
  (`scripts/fonts.py` fetches Google Fonts, which the OFL allows in ads).
- [Pillow](https://python-pillow.org/), [requests](https://requests.readthedocs.io/),
  and [tt-crawl](https://github.com/taskandtool/crawler) (the site reader,
  used only when the app collects its own sources).
- ffmpeg, a static build installed by `setup.sh` when the machine has none, for slideshow cuts.

## Spec

Purpose      — ad creatives and organic posts for one business, on brand, from real facts, approved before posting.
Shape        — files. Not served.
Audience     — internal: the app's AI and the owner through chat; a client through a portal by mirror.
Data         — owns creatives/ and campaigns/; reads brand/ and public/ (its own, or a brain's or a
               website's by mirror); writes nothing into other apps. No database.
Auth         — none.
Needs        — optional connections: an image model key (openrouter, gemini, bfl, fal, openai), Apify or
               Foreplay for research, the owner's ad accounts for results. Asked for with request_connection.
Build        — skills plus the scripts (Python), the HTML templates, the spec sheets.
Depends on   — nothing. A brain or a website upstream by mirror; a portal or a publisher downstream by mirror.
Add / remove — install seeds the app and installs the tools; removal leaves the files, they are the owner's.

## Developing this Starter App

- **Tests, no machine:** `python3 creatives/test_scripts.py` (a fake `obscura` on the
  PATH stands in for the renderer; ffmpeg is used when present).
- **On the platform:** Task & Tool's own repo clones this one into its packs
  folder and runs it through the real install path on a real machine
  (`dev/live_creatives.exs`) before a release is pinned.

A pre-push secret scan guards this repository. It holds no credentials by
design: keys arrive through the platform's Connections, never through
this repo.

## License

MIT. See `LICENSE`.
