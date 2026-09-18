# Creatives

A Task & Tool **Starter App**: ad creatives and social posts for one
business, made on its own machine from its brand and its facts, and
approved before anything is posted. It makes the material; it never
posts. The outputs are files the owner reviews in chat, a client approves
through a portal, and a publisher posts.

The repository *is* the app: what you clone is what runs. Installed with one
click on Task & Tool, or cloned into a project of your own (below). MIT
licensed.

## What is in the box

The app itself is at the root, and the skills that know how to work on it
are beside it:

```
.claude/skills/
  creatives/     the shape, the loop and the scripts
  sources/       the brand and fact notes: mirrored from a Company Brain or a website, or collected here (tt-crawl)
  brief/         the campaign brief, agreed with the owner before the first creative
  angles/        angles and the claims ledger; the 3×3 starter set (references/strategy.md)
  static-ad/     one image, one idea: 45 formats as recipes, drawn from every published catalogue
                 (references/formats.md, which says where the list comes from) and the
                 image-prompt craft with the brand's style anchor (references/visual-prompts.md)
  carousel/      swipe posts, LinkedIn documents, carousel ads
  video-script/  hooks, the ten structures with beat timings, slideshow cuts (references/hooks.md)
  social-post/   organic posts per platform (references/<platform>.md, repurpose.md)
  research/      competitor ads through an Apify or Foreplay connection; the swipe file and the winner score
  review/        the copy gate, the claims, the specs, the render, the voice
  results/       the numbers against angle, format and hook; what to iterate
.taskandtool/setup.sh  Pillow, requests, tt-crawl, the Obscura renderer, a static ffmpeg
AGENTS.md        what the AI reads first; CLAUDE.md imports it
starter-app.json the manifest: the connections it can use, what "ready" means, and the suggestions an
                 empty chat offers
```

Each `<skill>/SKILL.md` is a skill the harness loads on demand; the
references beside them are what the skill points at when it needs the
detail. The scripts in `scripts/` are plain Python (Pillow and requests,
which `.taskandtool/setup.sh` installs), and the tests sit with the skill
(`.claude/skills/creatives/test_scripts.py`).

## The app itself

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

**On Task & Tool.** Pick Creatives when you create an app. The machine
clones this repository into the app, pinned to a reviewed commit, and runs
`.taskandtool/setup.sh`. Nothing is sent into your chat: the manifest's
suggestions are what an empty chat offers.

**Anywhere else.** Clone it and start working in it:

```
git clone https://github.com/taskandtool/creatives my-creatives
cd my-creatives
bash .taskandtool/setup.sh
```

The setup installs Pillow, requests and tt-crawl with pip, and the Obscura
binary for Linux x86_64 or aarch64 (elsewhere `render.py` writes the HTML
and stops). Off the platform, `attach_files` (the bridge that puts a file
into the Task & Tool chat) is not there; the rendered files are on disk.

## Third-party tools it installs

- [Obscura](https://github.com/h4ckf0r0day/obscura), Apache-2.0, a Rust
  headless browser with its own rendering engine. It renders every creative;
  it loads no system fonts, so the brand's fonts go through `templates/fonts/`
  (`scripts/fonts.py` fetches Google Fonts, which the OFL allows in ads).
- [Pillow](https://python-pillow.org/), [requests](https://requests.readthedocs.io/),
  and [tt-crawl](https://github.com/taskandtool/crawler) (the site reader,
  used only when the app collects its own sources).
- ffmpeg, a static build installed by `.taskandtool/setup.sh` when the machine has none, for slideshow cuts.

## What it is for, and what it is not

It makes creatives; it never posts. It owns `creatives/` and `campaigns/`,
reads `brand/` and `public/` (its own, or a Company Brain's or a website's
by mirror), and writes into no other app. Files are the whole model — no
database, nothing served, no login.

Everything it can connect to is optional and asked for when it is actually
needed: an image model key (openrouter, gemini, bfl, fal, openai), Apify or
Foreplay for competitor research, the owner's ad accounts for results.
Upstream, a brain or a website by mirror; downstream, a portal or a
publisher by mirror. Removing the app leaves the files. They are the
owner's.

## Developing this Starter App

- **Tests, no machine:** `python3 .claude/skills/creatives/test_scripts.py`
  (a fake `obscura` on the PATH stands in for the renderer; ffmpeg is used
  when present).
- **On the platform:** Task & Tool's own repo keeps a working clone under
  `starter_apps/` and runs it through the real install path on a real machine
  (`dev/live_creatives.exs`) before a release is pinned.

A pre-push secret scan guards this repository. It holds no credentials by
design: keys arrive through the platform's Connections, never through
this repo.

## License

MIT. See `LICENSE`.
