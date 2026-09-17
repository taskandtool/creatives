---
type: spec
platform: all
last_verified: 2026-09-07
sources:
  - research/4-ad-paradigms.md (Specs 2026 section)
  - research/5-generation-tooling.md (Pipeline realities section)
---

# Platform spec sheets

Re-verify rule: if `last_verified` in a sheet is older than 90 days, re-verify that sheet against the platform's official help page before any creative is built against it. Then update `last_verified` and the `sources` list. Do not build on a stale sheet.

## What these sheets are

One file per platform. Each holds the sizes, ratios, file limits, text limits, and policy notes an agent needs to compose and QA a creative for that platform. Every number carries its source. A number marked "unverified" came from a secondary source and has not been checked against the platform's own page. A number marked "conflicting" has two sources that disagree; both values are given.

| Sheet | Covers |
|---|---|
| `meta.md` | Facebook and Instagram, paid and organic |
| `linkedin.md` | LinkedIn paid formats and organic posts |
| `tiktok.md` | TikTok in-feed video, Spark Ads, organic |
| `google.md` | Performance Max and Responsive Display Ads |
| `pinterest.md` | Pins and Pinterest ads |
| `youtube.md` | Thumbnails and Shorts |

## How to re-verify a sheet

1. Open the platform's official ads guide or help centre page (the URL is in `sources`). Vendor blogs are not a source.
2. Check every number in the tables. Change what moved. Remove "unverified" only when the official page shows the number.
3. Set `last_verified` to today's date.
4. If the official page is unreachable, keep the old date and say so in the sheet. Do not bump the date on a guess.

## The common 9:16 safe-zone box

Vertical placements (Reels, Stories, TikTok, Shorts) overlay UI on the frame. Keep text, logos, and anything that matters inside this box:

| Edge | Keep clear | Source |
|---|---|---|
| Top | 14% | Meta Reels ads guide (verified 2026-09-07); research note 5 says the same box is unverified across other platforms |
| Bottom | 35% | Meta Reels ads guide (verified 2026-09-07) |
| Sides | 6% each | Meta Reels ads guide (verified 2026-09-07) |
| Right rail on TikTok | about 10% extra | research note 5, unverified |

At 1080×1920 that is roughly: top 270 px, bottom 672 px, sides 65 px. The usable band is about 950×978. TikTok's own numbers vary by caption length; use TikTok's downloadable template for TikTok (see `tiktok.md`).

## 9:16 is composed separately, never cropped from 4:5

A 4:5 master (1080×1350) cropped to 9:16 loses the sides and puts the headline in the overlay zones. Compose a separate 9:16 layout with its own copy positions inside the safe box. The same rule applies in reverse: do not crop 9:16 down to 4:5 or 1:1. Source: research note 5, Pipeline realities.

## Output conventions (from research note 5)

- Emit JPG or PNG. Not WebP.
- Convert to sRGB and embed the profile. Sharp strips ICC by default; use `.withMetadata()`. Pillow saves no profile unless `icc_profile` is passed.
- Text on image at 1080 wide: body at least 36 px, headline at least 60 px. Contrast 4.5:1 body and 3:1 large text, sampled against the darkest and lightest region under the overlay.
- QA gate every export on dimensions, file size, safe-zone intersection, and the sRGB tag.
