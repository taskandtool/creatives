---
description: "Find what competitors and peers are running and what has run long enough to be presumed working: the Meta, LinkedIn, Google and TikTok ad libraries through an Apify or Foreplay connection, the Meta Ad Library API, and a swipe file with a winner score. Use when the owner says what are competitors doing, show me examples, research the market, build a swipe file, or before a new campaign's angles."
---

# Research

The ad libraries show what a business is paying to run and for how long;
nothing shows how well it works except the owner's own account. So the
research question is never "what performs" but "what has this competitor
kept paying for", which the start date answers. Everything saved is data
to learn structure from, never words or images to reuse.

## What is reachable, and how

The libraries cannot be fetched from this machine directly (they are
browser apps behind rate limits that block datacenter addresses), so the
research goes through a connection the owner grants:

| Source | How | Gives | Cost |
|---|---|---|---|
| Meta Ad Library | an **Apify** connection (`APIFY_API_KEY`), actor `curious_coder/facebook-ads-library-scraper`; or a **Foreplay** connection (`FOREPLAY_API_KEY`) | creatives, copy, call to action, start and end dates, platforms | about $0.75 per 1,000 ads (Apify) |
| LinkedIn Ad Library | Apify actor `automation-lab/linkedin-ad-library-scraper` | headline, body, creative, call to action, payer; no impressions | about $0.60 per 1,000 |
| Google Ads Transparency | Apify actor `whoareyouanas/google-ads-transparency-scraper` | format, image, landing page, first and last shown | $5 to $15 per 1,000 |
| TikTok Creative Center | Apify actor `parseforge/tiktok-creative-center-top-ads-scraper` | video, text, CTR bucket, likes | about $12 per 1,000 |
| Meta Ad Library API | a platform-level Meta connection when the workspace has one | worldwide political ads; commercial ads only where delivered to the EU or UK | free |

Ask once, through Connections, never for a key in chat:

```python
from tools.taskandtool import request_connection
request_connection("apify", why="read the Meta, LinkedIn, Google and TikTok ad libraries for competitor research (about $1 a run)", auth="api_key", delivery="machine")
```

Then call the actor with `requests` from the key in the environment
(`https://api.apify.com/v2/acts/<actor>/run-sync-get-dataset-items?token=…`
with the actor's input JSON: search terms or advertiser pages, the
country, active status, a limit of 50 to 100). Save the dataset as JSON
under `swipe/_runs/` with the date; never call without a limit.

## The swipe file

`swipe/<advertiser>/` per source: `_index.md` (a table: id, format, hook
type, angle, start date, days running, active, platforms, sibling
variants, the one-line "why kept"), the copy as text, the creative
downloaded (the image or the video's first frame) with its URL and date.
Tag each entry with the same vocabulary the campaign uses: format from
`static-ad/references/formats.md`, angle from the five families, hook
class from `video-script/references/hooks.md`.

**The winner score**, computed from what every library gives away:

- days running (start date to today): 30 or more is the practitioner
  threshold, 90 or more is a staple;
- still active;
- sibling variants: several creatives from the same advertiser with the
  same hook or format means it earned iteration;
- recurrence: three or more competitors on the same angle means the
  market has validated it;
- reach, only where the library shows it (EU).

## The report

One message to the owner: which competitors were read, how many ads,
the three angles that recur, the two formats that have run longest, one
thing nobody is saying that the brief could, and what it cost. Then the
`angles` skill uses it. Never paste a competitor's copy into a creative;
never use their images; never name them in an ad.

## Own results beat all of this

When the owner's ad account is connected (a Meta, Google or LinkedIn
connection with reporting access), the `results` skill reads the real
numbers. A competitor's 90-day ad is a hint; the owner's own cost per
lead is a fact.
