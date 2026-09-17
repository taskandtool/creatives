---
type: spec
platform: pinterest
last_verified: 2026-09-07
sources:
  - https://help.pinterest.com/en/business/article/pinterest-product-specs (fetched 2026-09-07)
  - research/4-ad-paradigms.md (Specs 2026, Policy)
  - research/5-generation-tooling.md (Pipeline realities)
---

# Pinterest

Re-verify rule: if `last_verified` is older than 90 days, check every number against Pinterest's product specs page before building against this sheet, then update the date.

## Standard Pin and image ad

| Item | Value | Source |
|---|---|---|
| Ratio | 2:3 | Pinterest specs (verified) |
| Size | 1000×1500 | Pinterest specs (verified) |
| Formats | PNG or JPEG | Pinterest specs (verified) |
| Image file size | 20 MB on desktop, 32 MB in app | Pinterest specs (verified) |
| Title | 100 chars max; about the first 40 show (30 for double-byte languages) | Pinterest specs (verified) |
| Description | 800 chars max | Pinterest specs (verified 800). Research note 4 recorded 500 or 800 as conflicting; the official page says 800 |

Longer pins (up to 1:2.1) are accepted for organic but can be cropped in feed; stay at 2:3 for ads.

## Video pin (standard width)

| Item | Value | Source |
|---|---|---|
| Ratio | 1:1, 2:3, 4:5, or 9:16 | Pinterest specs (verified) |
| Formats | MP4, MOV, M4V; H.264 or H.265 | Pinterest specs (verified) |
| File size | up to 2 GB | Pinterest specs (verified) |
| Length | 4 s to 15 min; 6 to 15 s recommended | Pinterest specs (verified) |

## Carousel ad

| Item | Value | Source |
|---|---|---|
| Ratio | 1:1 or 2:3 | Pinterest specs (verified) |
| Cards | 2 to 5 images | Pinterest specs (verified) |
| File size | 20 MB per image | Pinterest specs (verified) |

## Idea ad (vertical)

| Item | Value | Source |
|---|---|---|
| Ratio | 9:16, 1080×1920 | Pinterest specs (verified) |
| Video size | 2 GB in app, 100 MB on web | Pinterest specs (verified) |
| Length | up to 5 min | Pinterest specs (verified) |
| Title | 100 chars | Pinterest specs (verified) |

Idea ads use the common 9:16 safe box from the README; Pinterest does not publish its own percentages (unverified).

## Policy (research note 4)

- Before and after images are banned outright, including split-frame and slider formats.
- Weight-loss language and imagery are banned: no "lose X pounds", no body-shaming, no fat-pinch, no scales as a hero.
- Health, beauty, and fitness advertisers write about the routine, the product, or how it feels, not the body change.
- Testimonials with atypical results still need an FTC "generally expected results" line.

## Pins are search assets

Pinterest is a visual search engine more than a feed. A pin keeps earning impressions for months, and the title and description are indexed.

- Put the primary keyword in the title within the first 40 chars, and again naturally in the description.
- Text on the image is read by people, not the index; keep it to 3 to 5 words and the brand.
- One idea per pin. Make several pins per landing page, each with a different keyword angle, rather than one pin with a long description.
- Use the description's 800 chars for context and secondary keywords; no hashtag blocks.
- Link every pin to a page that matches the title. Pinterest checks the destination.

Sources: research note 4 for the shelf-life and search framing; the keyword placement rules follow from the verified visible-title limit.
