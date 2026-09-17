---
type: spec
platform: google
last_verified: 2026-09-07
sources:
  - https://support.google.com/google-ads/answer/7005917 (Responsive Display Ads, fetched 2026-09-07)
  - https://support.google.com/google-ads/answer/9823397 (RDA image sizes, fetched 2026-09-07)
  - research/4-ad-paradigms.md (Specs 2026)
  - research/5-generation-tooling.md (Pipeline realities, Platform-native tools)
---

# Google Ads: Performance Max and Responsive Display

Re-verify rule: if `last_verified` is older than 90 days, check every number against Google Ads Help before building against this sheet, then update the date. The Performance Max asset page could not be reached on 2026-09-07; PMax numbers are from research note 4 and are unverified against the help page.

## Performance Max asset group (research note 4, unverified)

Text assets:

| Asset | Count | Chars | Note |
|---|---|---|---|
| Headlines | 3 to 15 | 30 | at least one must be 15 chars or fewer |
| Long headlines | 1 to 5 | 90 | |
| Descriptions | 2 to 5 | 90 | |
| Business name | 1 | 25 | |

Image assets, up to 20 per ratio:

| Ratio | Recommended | Minimum | Source |
|---|---|---|---|
| 1.91:1 landscape | 1200×628 | 600×314 | research note 4; minimum matches the RDA page (verified) |
| 1:1 square | 1200×1200 | 300×300 | research note 4; minimum matches the RDA page (verified) |
| 4:5 portrait | 960×1200 | not stated | research note 4 |
| 9:16 vertical (video-style placements) | 1080×1920 | not stated | research note 5 |

Logos:

| Ratio | Size | Required |
|---|---|---|
| 1:1 | 1200×1200 | yes |
| 4:1 | 1200×300 | optional |

Video: at least 10 s. If none is supplied Google generates one from the images; supply your own.

## Responsive Display Ads

| Asset | Count | Chars | Source |
|---|---|---|---|
| Headlines | 1 to 5 | 30 | Google Ads Help 7005917 (verified) |
| Long headline | 1 | 90 | Google Ads Help 7005917 (verified) |
| Descriptions | 1 to 5 | 90 (research note 4); an older help page shows 80; conflicting | Google Ads Help 9823397 shows 80; research says 90 |
| Business name | 1 | 25 | research note 4, unverified |

Images, up to 15 in total across ratios (verified), 5 to 10 per ratio recommended:

| Ratio | Recommended | Minimum | Required | Source |
|---|---|---|---|---|
| 1.91:1 | 1200×628 | 600×314 | yes | Google Ads Help 9823397 (verified) |
| 1:1 | 1200×1200 | 300×300 | yes | Google Ads Help 9823397 (verified) |
| 9:16 | 900×1600 | 600×1067 | no | Google Ads Help 9823397 (verified) |

Logos: 1:1 1200×1200 and 4:1 1200×300, cropped clean, no logo overlaid on the images themselves (verified guidance, sizes from research note 5).

## Files

| Item | Value | Source |
|---|---|---|
| Image file size | 5 MB (5120 KB) | Google Ads Help 9823397 (verified) |
| Formats | JPG or PNG | research note 5 (emit JPG or PNG, not WebP) |
| Colour | sRGB embedded | research note 5 |

## Copy rules for Google

- Headlines are assembled by Google in any combination. Every headline must stand alone and must not depend on another one.
- Do not reuse Google search headlines on Meta and vice versa. Search answers intent; social must earn attention (research note 4).
- Keep text off the image. Google assembles text next to the image and may overlay its own.

## Synthetic content attestation (research note 5)

From Google Ads API v25 every uploaded image and video asset must carry a `synthetic_content_info` attestation stating whether it was AI generated or altered. Set it on every asset the pipeline uploads, and set it truthfully. AI backgrounds and AI-generated b-roll count as synthetic even when the logo and copy were composed in HTML.

Related handoff rules: Google's AssetGenerationService is closed beta and Product Studio is a pilot, so upload finished masters through AssetService rather than relying on in-platform generation.
