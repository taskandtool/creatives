---
type: spec
platform: meta
last_verified: 2026-09-07
sources:
  - https://www.facebook.com/business/ads-guide/image/facebook-feed (fetched 2026-09-07)
  - https://www.facebook.com/business/ads-guide/update/video/instagram-reels (fetched 2026-09-07)
  - https://www.facebook.com/business/ads-guide/update/carousel/facebook-feed (fetched 2026-09-07)
  - research/4-ad-paradigms.md (Specs 2026, Ad vs organic, Policy)
  - research/5-generation-tooling.md (Pipeline realities)
---

# Meta: Facebook and Instagram

Re-verify rule: if `last_verified` is older than 90 days, check every number against the Meta ads guide before building against this sheet, then update the date. The Stories image page was not reachable on 2026-09-07; Stories numbers below are from the research notes and Reels.

## Image sizes

| Placement | Ratio | Size | Source |
|---|---|---|---|
| Feed (FB and IG), default master | 4:5 | 1080×1350; Meta recommends 1440×1800 | Meta feed guide (verified); research note 4 says 1:1 underperforms 4:5 |
| Feed square | 1:1 | 1080×1080 | research note 4 |
| Feed landscape, link ads | 1.91:1 | 1200×628 | research note 4 |
| Reels and Stories | 9:16 | 1080×1920; Meta recommends 1440×2560 for Reels video | Meta Reels guide (verified) |
| Carousel card | 1:1 | at least 1080×1080, 2 to 10 cards | Meta carousel guide (verified) |

Feed minimums: 600 wide, 750 tall at 4:5, ratio tolerance 3% (verified). Research note 4 says a short edge under 1080 is penalised; unverified.

## Files

| Item | Limit | Source |
|---|---|---|
| Image file size | 30 MB | Meta feed and carousel guides (verified) |
| Image formats | JPG or PNG | Meta feed guide (verified) |
| Video file size | 4 GB | Meta Reels and carousel guides (verified) |
| Video formats | MP4, MOV; H.264, AAC stereo 128 kbps or more | Meta Reels guide (verified) |
| Video length, Reels | 0 s to 15 min | Meta Reels guide (verified) |
| Video length, carousel card | 1 s to 240 min | Meta carousel guide (verified) |
| Working length for ads | 15 to 35 s; hook by 3 s, pay off the hook by about 6 s | research note 4 (Reloop, Motion), unverified |

## Safe zones

| Placement | Keep clear | Source |
|---|---|---|
| Reels and Stories 9:16 | top 14%, bottom 35%, sides 6% | Meta Reels guide (verified 2026-09-07). The research notes marked this unverified; it now matches Meta's own wording |
| Feed 4:5 | top 14%, bottom 20% | research note 4, unverified |

The 20% text-overlay rule was dropped in September 2020 (research note 5). Text density is a taste call, not a policy one.

## Text limits (ads)

Meta's guide lists "recommended" lengths, which are what shows before truncation, not hard caps. The research notes give the practical limits. Where they differ, both are listed.

| Field | Limit | Where it shows | Source |
|---|---|---|---|
| Primary text | about 125 chars before "See more" (line based); Meta recommends 50 to 150 on feed, 44 on Reels | above the creative | research note 4; Meta feed and Reels guides (verified) |
| Headline | 40 max; 27 shows on FB feed; 10 as Reels overlay; carousel card 45 (research) or 20 (Meta recommended); conflicting | below the creative, bold | research note 4; Meta feed and carousel guides (verified) |
| Description | 25 (research) or 18 on carousel cards (Meta recommended); conflicting | Marketplace, Audience Network, search, in-stream only; not shown on feed | research note 4; Meta carousel guide (verified) |
| Carousel primary text | 80 recommended | above the cards | Meta carousel guide (verified) |
| Text variations | up to 5 per field | Meta tests them | research note 4 |

Copy guidance from research note 4: cold feed copy 40 to 80 words, retargeting 150 to 250 words, one idea per ad, CTA is a verb plus an expectation, no hashtags in ads (they are an exit point), do not reuse search headlines on Meta.

## Policy notes (research note 4, Meta policy pages)

- Personal attributes. Never imply knowledge of race, religion, age, sexual orientation, gender identity, disability, health condition, financial status, criminal record, or name. "Do you have diabetes?" is banned. "Bulimia counseling available" is allowed. Write about the product or the outcome, never about "your condition". "Who it's for" callouts must stay on job or situation, not protected attributes.
- Health and appearance. Before and after only for general cosmetic claims, 18 and over. No fat-pinch or body-part close-ups. No cure claims.
- Comparisons. Naming competitors in "us vs them" statics invites policy flags; keep the takedown tone off.
- FTC. Atypical results need a "generally expected results" line. Creators must disclose paid relationships.
- No hashtags in ad copy.

## Organic notes

| Item | Value | Source |
|---|---|---|
| Instagram caption cutoff | about 125 chars before "more"; front-load the point | research note 4 (same line rule as primary text), unverified for organic |
| Instagram caption max | 2,200 chars | common figure, unverified |
| Hashtags | none in ads; organic keep to a few relevant ones, never a block | research note 4 for ads; organic count unverified |
| Post ratio | 4:5 for feed, 9:16 for Reels and Stories, composed separately | research note 5 |
