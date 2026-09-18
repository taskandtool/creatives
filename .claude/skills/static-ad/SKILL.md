---
description: "Make a static ad creative (one image, one idea) from an angle: pick the format from the catalogue of 25 proven ones, write the twelve words and the primary text in the brand's voice, generate or place the visual, render it through the template at the platform's sizes, and pass qa and check. Use when the owner says make an ad, make the statics, a Facebook ad, an Instagram ad, a LinkedIn ad, a Google image, or when angles.md has rows not yet made."
---

# Static ad

One frame, one second, one idea. `references/formats.md` is the catalogue:
45 formats with when to use each, the structure, the copy pattern, the
visual, the psychology, the pitfalls, and the template it renders through.
Read the entry for the format you are making, not the whole file, and
`DESIGN.md` for what the render must obey.

## Before the first one

- `campaigns/CURRENT` names the campaign; its `brief.md` is agreed and
  `angles.md` has the rows; `claims.md` has the facts.
- `brand/voice.md` is filled; `templates/brand.css` is set from the brand
  (`python3 scripts/qa.py --tokens` passes); the fonts are in
  `templates/fonts/` (`scripts/fonts.py --from-brand`).
- `python3 scripts/imagegen.py --check` says which image provider exists.
  With none, make the formats that need no picture first (`statement`,
  `quote`, `us-vs-them`, `offer`, `listicle`, `checklist`, `note`,
  `screenshot`) and ask for a key once (`creatives` skill: Images).
- The owner's real photographs, if any, are in `raw/` or `uploads/`; they
  beat anything generated.

## One creative

1. **Scaffold.** `python3 scripts/new.py --platform meta --kind static
   --format us-vs-them --campaign <slug> --ratio 4:5 --title "…"` (the
   ratio the platform leads with: Meta feed 4:5, LinkedIn 1.91:1 or 1:1,
   Google 1.91:1 and 1:1, Pinterest 2:3; a 9:16 is its own render).
2. **Words.** In `creative.md`: `copy.headline` (twelve words or fewer,
   the hook, in the voice), `copy.primary_text` (the words beside the ad:
   40 to 80 for cold, 150 to 250 for warm; one idea; the claim and its
   proof; the call to action as a verb and an object), `copy.cta`, and
   `claims` (each fact with its `claims.md` number or note). The body:
   why this creative, the visual prompt if any, notes for the owner.
   Then `fields.json`: the template's fields (`templates/README.md`),
   the same words, never a second headline.
3. **Visual**, when the template takes one (`photo`, `product`,
   `before-after`). The owner's photo first. Otherwise the prompt is
   assembled, not improvised: the format's universal guide in
   `prompts/<format>.md` (its composition, light, copy-space and policy)
   with the brand's slots filled from the notes:

   ```bash
   python3 scripts/prompt.py --slots                                    # what the brand fills; what is missing
   python3 scripts/prompt.py --format photo --out uploads/visual.txt    # or --format before-after --side before
   python3 scripts/imagegen.py --prompt-file uploads/visual.txt --ratio 4:5 \
     --out creatives/generated/<id>/visual.png [--ref uploads/product.png]
   ```

   A missing slot is a question for the owner (or a fact from the crawl
   the `sources` skill should have written), never a guess. Edit the
   assembled prompt only for this creative's moment; keep its shape and
   its ending (the anchor; the script adds the no-text rule). A product
   photo goes in as `--ref` with the product lock ("keep the exact label,
   shape, logo, colour, material and proportions; change only the
   setting"). Generate two or three candidates, read them, refuse any
   with the tells in `references/visual-prompts.md` (a smiling stranger,
   plastic skin, painted text, the HDR glow, purple grading), keep one,
   and write the prompt into the record's body.
4. **Render.** `python3 scripts/render.py <id>` → `master.png`. Look at it
   (Read the PNG). Wrong hierarchy, a wrapped headline, a cramped pill,
   text over a busy patch: change the words or the fields, render again.
   Two passes is normal.
5. **Sizes.** `python3 scripts/resize.py <id>` for the platform's other
   sizes in this ratio. A 9:16 for Stories or Reels is a second creative
   (`--ratio 9:16`, template composed for it), never a crop.
6. **Gates.** `python3 scripts/qa.py <id>` and `python3 scripts/check.py
   <id>` must say ok. Fix what they list; do not argue with them.
7. **Show.** Attach `master.png` (and the 9:16 when made) with one line:
   the angle and the format. Ask what to change or whether to approve.

## A batch

Three angles × the format that shows each best (from `angles.md`), three
creatives, one message with all three attached and one line each. Then
the six alternatives when the owner wants the full 3×3. Never three
colourways of one idea.

## Copy rules for the frame

- Twelve words or fewer on the image. The rest goes in the primary text.
- Hook first: the reader's problem, the outcome, the number, the
  comparison, or the quote. Never the business name first.
- The call to action names the next step: "Book a workshop visit",
  "See the Clifton kitchen", "Get the drawing". Never "Learn more".
- No hashtags. No emoji. No "It's not X, it's Y". No tricolon. No
  invented proof. Nothing that implies knowledge of the reader's health,
  money, age, or the like (Meta's personal-attributes rule): say what the
  product does, not what the reader suffers.
- The claims ledger is the only source of facts; a result most customers
  will not get says what is typical.

## Policy notes by format

Before/after is restricted in health and skincare and banned on
Pinterest; a comparison names the category, never a competitor; a
testimonial is quoted as written, with permission to use the name; an
endorsement that was paid says so. The platform's sheet in `specs/` has
the rest.
