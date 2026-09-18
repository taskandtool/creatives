---
type: spec
platform: tiktok
last_verified: 2026-09-07
sources:
  - https://ads.tiktok.com/help/article/video-ads-specifications (fetched 2026-09-07)
  - research/4-ad-paradigms.md (Video/UGC and Specs 2026)
  - research/5-generation-tooling.md (Pipeline realities)
---

# TikTok

Re-verify rule: if `last_verified` is older than 90 days, check every number against TikTok's ad specifications page before building against this sheet, then update the date.

## Video (in-feed, non-Spark)

| Item | Value | Source |
|---|---|---|
| Ratio | 9:16 vertical (16:9 and 1:1 accepted, not recommended) | TikTok ad specs (verified) |
| Resolution | 1080×1920 target; minimum 540×960 | research note 4 (1080×1920); TikTok ad specs (min 540×960, verified) |
| Length | 15 to 30 s working range; platform allows up to 10 min | research note 4 (15 to 30 s); TikTok ad specs (10 min, verified) |
| File size | 500 MB or less | TikTok ad specs (verified) |
| Formats | MP4, MOV, MPEG, 3GP, AVI | TikTok ad specs (verified) |
| Bitrate | 516 kbps or more | TikTok ad specs (verified) |

## Caption (ad description)

| Item | Value | Source |
|---|---|---|
| Ad caption max | 100 chars | research note 4, unverified |
| Visible before truncation | about 45 (research says 40 to 50) | research note 4, unverified |
| Rendering | white, uniform font, cannot be styled; no clickable links, no @ symbols, no hashtags | TikTok ad specs (verified) |
| Organic caption max | 2,200 chars | common figure, unverified; organic allows far more than the ad field |
| Spark Ads caption | up to 4 lines display, including emoji; no duration restriction | TikTok ad specs (verified) |

## Safe zones

Numbers conflict between sources. TikTok says the safe zone varies by orientation, caption length, and format and publishes downloadable templates (standard and right-to-left). Use the template for the final check.

| Edge | Keep clear | Source |
|---|---|---|
| Top | about 10% | research note 4, unverified |
| Right (like, comment, share rail) | about 10% | research notes 4 and 5, unverified |
| Bottom (caption, sound, progress) | about 20% | research note 4, unverified |
| Meta-style box also used | top 14%, bottom 35%, sides 6% | see README; a stricter box that also clears TikTok's UI |

Practical rule: build inside the stricter box (top 14%, bottom 35%, left 6%, right 10%), then check against TikTok's template.

## Timing and on-screen text (research note 4, TikTok official guidance as quoted there)

| Rule | Value |
|---|---|
| Hook | something that stops the scroll in the first 3 s |
| Proposition | what the product is and why it matters, by 6 s |
| On-screen text pace | 5 to 10 words per second |
| Sound | design for sound on; captions for sound off |
| Re-hook | every 5 to 15 s in longer cuts |

Note on ordering: research note 4 quotes TikTok as "proposition in first 3 s, hook in first 6 s"; the brief for this sheet phrases it as hook in 3 s, proposition by 6 s. The practical test is the same: by 6 s the viewer knows the hook and the offer. Hook rate on TikTok is measured on 2 s plays (Meta uses 3 s). Vendor benchmarks: 30 to 39% competitive, 40% and up elite.

Opening rules: no logo on frame one, no slow establishing shot, no corporate voice-over. Script the hook and the CTA word for word; the middle can be beats.

## Spark Ads

Spark Ads promote an existing organic post from a creator or the brand account. The post's caption, sound, and length carry over, so there is no separate ad copy. Test 5 to 8 hooks per body organically, then Spark the winner (research note 4). The ad specs page says Spark Ads have no duration restriction and display up to 4 caption lines (verified).

## Platform tooling note (research note 5)

TikTok Symphony Creative Studio is GA; its API is early access only. Do not plan on generating inside TikTok. Upload finished masters.
