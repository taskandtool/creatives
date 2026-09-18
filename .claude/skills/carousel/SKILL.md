---
description: "Make a carousel: an Instagram or Facebook swipe post, a LinkedIn document, a Meta carousel ad. The first card is the hook, one idea per card, the last card the recap and the ask, every card rendered through the templates as its own frame. Use when the owner says make a carousel, a swipe post, a document post, a PDF for LinkedIn, or when the format is educational, listicle, FAQ, myth vs fact, checklist, or a job recap."
---

# Carousel

A carousel is a static ad that unfolds: the reader gives one swipe per
card, and each card must earn the next. On Instagram carousels lead saves
(nine times a single image) and get reach past ten cards; on LinkedIn a
document post is the highest-engagement format and gives a small account
the most impressions (`social-post/references/` has the numbers).

## Shape

One creative (`--kind carousel`), its cards under `slides/` as numbered
PNGs, one `fields-<nn>.json` per card, and `creative.md` carrying the
caption or the ad copy and the claims for every card.

```
creatives/generated/<id>/
  creative.md         kind: carousel; files: [slides/01.png, …]; copy.caption or copy.primary_text
  fields-01.json …    each card's template and fields (statement, listicle, quote, before-after, photo…)
  slides/01.png …     rendered by render.py per card
  document.pdf        LinkedIn only: the cards as one PDF (scripts/carousel.py)
```

## The cards

1. **Card 1 is the hook**: eight words or fewer, big type, a promise or a
   number, and a swipe cue (an arrow or "1/7"). It looks like the start
   of something, never like a finished quote card. Template `statement`
   with the headline alone, or `photo` with the scrim band.
2. **Cards 2 to N are one idea each**, 25 words or fewer, numbered where
   the content is a sequence (`listicle` one item per card, `checklist`,
   `us-vs-them` one row per card, `quote` one review per card,
   `before-after` one pair per card). Six to ten cards for a small
   account; more only when every card earns its place.
3. **The last card is the recap and the ask**: the one thing to remember,
   then "Save this", "Send this to someone who…", or the ad's call to
   action. Never a bare logo card.
4. Same template family and tone across the deck; the accent appears once
   per card at most; page numbers in the label style.

## Making it

```bash
python3 scripts/new.py --platform meta --kind carousel --format listicle --campaign <slug> --ratio 1:1 --title "…"
# write creative.md (copy, claims) and fields-01.json … fields-07.json
python3 scripts/carousel.py <id>          # renders every fields-NN.json to slides/NN.png, records files, LinkedIn PDF when --pdf
python3 scripts/qa.py <id> && python3 scripts/check.py <id>
```

Ratios: Instagram and Facebook 1:1 (4:5 works and shows more); Meta
carousel ads 1:1; LinkedIn documents 1:1 or 4:5 portrait, as a PDF under
100 MB and ten pages or fewer for ads.

## Copy

- The caption (organic) restates card 1's hook in its first 125
  characters, expands one card, and ends with the ask that matches the
  metric ("Save this" for saves, "Send this to…" for shares). Hashtags
  last, three to five, relevant.
- The primary text (ad) is the same as a static's: 40 to 80 words cold,
  one idea, the claim and its proof, the call to action. No hashtags.
- Every fact on any card is in `claims.md`. A card that needs a
  disclaimer is a card that needs a different claim.

## Show

Attach the cards in order (up to six per call; a longer deck in two
calls, saying "cards 1 to 6" and "7 to 10"), with one line: the angle,
the format, the number of cards. On LinkedIn attach the PDF too.
