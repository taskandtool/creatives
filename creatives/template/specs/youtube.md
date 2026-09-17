---
type: spec
platform: youtube
last_verified: 2026-09-07
sources:
  - https://support.google.com/youtube/answer/72431 (custom thumbnails, fetched 2026-09-07)
  - research/4-ad-paradigms.md (Specs 2026)
  - research/5-generation-tooling.md (Pipeline realities)
---

# YouTube

Re-verify rule: if `last_verified` is older than 90 days, check every number against YouTube Help before building against this sheet, then update the date.

## Thumbnails (long-form video)

| Item | Value | Source |
|---|---|---|
| Ratio | 16:9 | YouTube Help 72431 (verified) |
| Size | 1280×720 working size; YouTube Help now lists 3840×2160 with a minimum width of 640 | research notes 4 and 5 (1280×720); YouTube Help 72431 (3840×2160, verified 2026-09-07); conflicting, both accepted |
| File size | 2 MB uploading from mobile; 50 MB from desktop | YouTube Help 72431 (verified). Research note 5 lists 2 MB as the ceiling; keep exports under 2 MB so they upload from anywhere |
| Formats | JPG or PNG | YouTube Help 72431 (verified) |

Composition notes:

- Thumbnails render at about 168 px wide in the sidebar and around 360 px in a mobile feed. Test at that size: one face or object, 3 to 5 words at most, high contrast. This is a taste rule, not a platform spec (unverified).
- The bottom right corner carries the duration badge; keep text out of it.

## Shorts

| Item | Value | Source |
|---|---|---|
| Ratio | 9:16 | YouTube Help 72431 lists 9:16 for Shorts thumbnails (verified) |
| Size | 1080×1920 | research note 5 (common 9:16 master) |
| Shorts thumbnail | 9:16, YouTube Help lists 2160×3840 with minimum height 640 | YouTube Help 72431 (verified) |
| Length | up to 3 minutes; 15 to 35 s working range for ad-style cuts | length limit is a common figure, unverified; working range from research note 4 |

Shorts safe zone: YouTube does not publish percentages. Use the common 9:16 box from the README (top 14%, bottom 35%, sides 6%) and treat the right rail as busy the way TikTok's is (about 10%). The Shorts title and channel name sit over the bottom band, so the bottom 20% at minimum must be clear (unverified).

## Titles

| Item | Value | Source |
|---|---|---|
| Title visible | about 70 chars before truncation in most surfaces | brief and common figure, unverified |
| Title max | 100 chars | common figure, unverified |

Put the keyword and the hook in the first 40 chars; search and suggested surfaces cut earlier than the watch page.

## Video ads (skippable in-stream)

Not covered by the research notes. Google Ads video specs are on the Google Ads Help site; re-verify there before building. The general rules from research note 4 still apply: hook in the first 3 to 5 s (the skip button appears at 5 s), no logo frame one, script hook and CTA word for word.

## Files (research note 5)

- Emit JPG or PNG, sRGB embedded, not WebP.
- Video: H.264 MP4, AAC audio.
