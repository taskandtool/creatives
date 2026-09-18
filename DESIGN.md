# DESIGN.md

The design contract for everything this app renders: the brand's colours
and fonts as tokens, the rules a static ad, a carousel card, or a thumbnail
follows, and what to refuse. The values live in `templates/brand.css`; this
file says what each is for. Set both from the brand notes in `brand/`
("Updating from the brand", at the end). The AI reads this before it
composes anything; `scripts/qa.py` enforces the parts that can be measured.

A website has a page to fill and a reader who scrolls. A creative has one
frame, one second, and one idea. Everything below follows from that.

## Identity

Filled once from the brief, before the first creative is made. A file whose
Identity is still "to fill" is a template.

```text
Business:          to fill — what it sells, in its own words
Reader:            to fill — who scrolls past this, and what they are in the middle of
One idea:          to fill — the single thing a creative may say (the brief's message)
Signature:         to fill — the one visual move that makes these recognisably this brand's
Rejection:         to fill — the ad look this brand refuses (e.g. stock smiles, purple gradients)
Photography:       to fill — real photos the owner has; until then, generated visuals of what kind
```

## Tokens (`templates/brand.css`)

Two layers, as on the website. **Brand colours** are what the business
owns, copied from `brand/visual-identity.md`. **Roles** say what each is
for; templates use roles only.

| Token | Value | Role |
|---|---|---|
| `--brand-primary` | #2f5bea | The business's main colour. |
| `--brand-dark` | #14110d | Its dark. |
| `--brand-light` | #f6f3ec | Its light. |
| `--brand-neutral` | #57514a | Its secondary text colour. |
| `--ground` | brand light | The default ground of a card. |
| `--ground-dark` | brand dark | The dark ground: a statement card, a caption bar. |
| `--ink` | #191612 | Words on the light ground (16:1). |
| `--ink-2` | brand neutral | Secondary words on the light ground (7.1:1). |
| `--ink-on-dark` | brand light | Words on the dark ground (17:1). |
| `--accent` | brand primary | The one action colour: the call-to-action pill, an underline, one bar. Never body text on the light ground unless it reaches 4.5:1 there. |
| `--accent-ink` | #ffffff | Words on the accent (5.5:1). |
| `--scrim` | rgb(20 17 13 / 0.72) | The band behind words placed over a photo. Words never sit on a photo without it. |
| `--font-display` | Bricolage Grotesque | Headlines. |
| `--font-body` | Inter | Everything else. Replace both from the brand; Inter is the placeholder, not a choice. |

Rules:

- Every pair of words and ground reaches 4.5:1 (3:1 for the display size).
  `scripts/qa.py` measures the token pairs and samples the pixels behind
  each text box in the render.
- The accent appears once per creative, on the action or on one bar.
- Photographs and generated visuals carry the colour; the frame around
  them stays in the tokens.
- A brand colour that fails as text becomes a ground with its own ink.

## Type at 1080 wide

Sizes are for a 1080 px wide master; `scripts/render.py` scales them with
the size. Nothing on a creative renders below the label size.

| Class | Size | Line height | Weight | Use |
|---|---|---|---|---|
| `.headline` | 96 px (72 on 1:1, 112 on 9:16) | 1.0 | 700 | The one line. Twelve words or fewer. |
| `.body` | 44 px | 1.25 | 400 | The supporting line. Two lines at most. |
| `.cta` | 40 px | 1 | 600 | The action, in a pill on the accent. Verb first. |
| `.label` | 30 px | 1.2 | 600, tracked +0.06em, upper case | One small line: the business name, a category, a date. Never a paragraph. |
| `.giant` | 260 px | 0.9 | 700 | One number or one word as the visual (a statistic, a price). Once. |

Rules:

- A static carries at most three text elements: headline, body, cta (a
  label is a fourth only when it orients). Twelve words on the image, or
  fewer. Longer thoughts belong in the primary text beside the ad.
- Headlines use `--font-display`; everything else the body face.
- Words sit inside the safe zone of the placement (`specs/README.md`) and
  never touch the edge: 72 px of margin at 1080 wide.
- No text in the generated visual. The model paints the scene; the
  template sets the words in the brand's face.

## Composition

Each format in `static-ad/references/formats.md` names its template
(`templates/*.html`). The templates are the compositions; the AI fills
fields (`fields.json`) and does not lay out by hand:

- `statement`: a headline on a ground, the cta beneath, the business name
  as a label. The plainest ad and often the best.
- `photo`: a visual with a scrim band carrying the headline and cta.
- `quote`: a testimonial in large type with who said it and where.
- `us-vs-them`: two columns, three to five rows, ticks on ours.
- `before-after`: two frames side by side with labels, or top and bottom
  on 9:16.
- `offer`: the offer, what is included, the price or saving, the deadline,
  the cta.
- `listicle`: a title and three to five numbered lines.
- `product`: the product or work on a coloured ground with one line.
- `checklist`: a title and boxes, ticked or not.
- `note`: a hand-written-looking note on a paper tint (the sticky-note
  format); the one template allowed a rotation, 2 degrees.
- `screenshot`: a native-UI mimic (a message thread, a notification, a
  review card) drawn in the template, not faked in an image.

One idea per creative. If a second idea wants in, it is the next creative.

## Depth, edges, motion

Flat. A card has no shadow; a frame inside a card has a 2 px rule in the
ink at 14%. Corners: 24 px on a pill, 32 px on an inner frame, 0 on the
card itself (the platform rounds it). No gradients on grounds, no glow, no
blur, no glass. Video adds motion; a static has none.

## Refuse

- Purple, indigo, or violet accents; blue-to-purple gradients; gradient
  text; glows; glass.
- Stock-photo scenes: a smiling stranger, a handshake, a laptop on a
  desk, a pointing person. A generated visual shows the owner's actual
  subject (the work, the place, the product, the material) or nothing.
- Text painted by an image model. Fake interfaces painted by an image
  model (use the `screenshot` template).
- Emoji as bullets or decoration. Icons in coloured circles. A logo bigger
  than the headline. More than one accent.
- Invented reviews, counts, awards, prices, or "as seen in" logos. A claim
  without a source in the claims ledger.
- "It's not X, it's Y"; a tricolon ("Fast. Simple. Done."); "Say goodbye
  to"; "next level"; "Whether you're X or Y"; em dashes; hashtags in an
  ad; "Learn more" as the call to action.
- Meta's personal-attributes line: never words that imply knowledge of
  the reader's health, finances, age, religion, or the like ("Struggling
  with X?"). Say what the product does.
- Text over a photo without the scrim. Anything under 4.5:1. Anything in
  the platform's UI zone (`specs/`).

## Updating from the brand

1. Read `brand/visual-identity.md`, `positioning.md`, `voice.md`,
   `do-and-dont.md`.
2. `templates/brand.css`: the brand colours as hex, the two font families
   (self-hosted files in `templates/fonts/`, or a Google Fonts family the
   renderer can fetch), then the roles. Run `python3 scripts/qa.py --tokens`;
   a pair under 4.5:1 means the role gets a different value.
3. The logo: `brand/logo/<file>.svg` (or png), named in `fields.json` as
   `logo`; the templates place it as a label-sized mark, never larger than
   the headline.
4. This file: the token table's values, the fonts, the Identity block, and
   any rule `do-and-dont.md` adds (a colour never used, a word never
   used).
5. Re-render anything in `creatives/generated/` (`scripts/render.py --all
   generated`); approved creatives are not re-rendered without asking.

When `brand/_mirror.md` exists the notes belong to the Company Brain (or
the website): change a brand fact there, then re-apply it here.
