# Creative strategy

The strategy the agent encodes before it makes anything: who the ad is for and how much they already know, what we are saying, how many ads to make, how to test them on a small budget, and when to replace them. The worked examples use a made-up business, Harlow Joinery, a workshop in Bristol that makes fitted kitchens. Numbers in examples are illustrative and must come from the claims ledger before use.

Sources: Meta's Andromeda ranking change (global from Oct 2025), Segwise and Admetrics on concept diversity, Dara Denney, Jordan Glickman's brief template, Reloop and AdRoast test benchmarks (vendor figures, not independently verified), Meta and Pinterest policy pages, the FTC endorsement guides.

## Awareness levels

| Level | Who they are | What they need from the ad | Default formats | Copy length (primary text) |
|---|---|---|---|---|
| Cold | Has the problem or the situation, has not heard of us | A reason to stop: the problem named, or a situation they recognise. No offer, no price, no logo first. | Problem-agitate-solve, who it's for, sticky note, native-UI mimic, founder note, meme | 40 to 80 words |
| Warm | Has seen us, visited the site, or engaged with a post; has the problem in mind | Reasons to believe: proof, comparison, mechanism, answers to the objection | Testimonial, us vs them, listicle, feature callout, checklist, myth vs fact, FAQ, advertorial | 80 to 150 words |
| Hot | Has enquired, abandoned a form, or asked for a quote | A reason to act now: the offer, what is included, the deadline, the risk reversal | Offer stack, product on colour, big statistic, quote card, press | 150 to 250 words, or short with the offer on the image |

Rules that follow from the table:
- A cold audience is never sent an offer stack or a statistic; they have no context for either.
- A hot audience is never sent a problem ad; they know the problem and want the terms.
- The landing page matches the level: cold to an explainer or the work, warm to the proof page, hot to the booking form.

## Angle taxonomy

An angle is what the ad is saying. Five kinds:

| Angle | What it argues | Harlow Joinery example |
|---|---|---|
| Outcome | What life is like after | "Drawers that still close in 2036." |
| Problem | What is wrong now and what it costs | "The 40 mm filler strip is what happens when nobody measured the room." |
| Social proof | Others chose us and it went well | "'The drawing was the kitchen. Nothing changed on fit day.' Ruth, Redland." |
| Mechanism | How we do it differently, the reason to believe | "The joiner who measures is the joiner who fits." |
| Comparison | Us against the category | "Flat-pack is cut down on site. Ours is cut to your walls in the workshop." |

An ad carries one angle. If it needs two, it is two ads.

## Angles x formats x hooks

Hooks are the first line. Five classes: problem, number, question, social proof, pattern interrupt (the full video taxonomy is in `video-script/references/hooks.md`). The table gives the formats that suit each angle and the hook classes that open it best. Read it as a menu, not a rule.

| Angle | Formats that suit it | Hooks that open it |
|---|---|---|
| Outcome | Before/after, photo + statement, quote card, product on colour, first-frame static | Number ("Eight weeks from survey to fit"), question ("What does a kitchen look like ten years in?"), pattern interrupt (result-first frame) |
| Problem | Problem-agitate-solve, native-UI mimic, sticky note, meme, anti-ad, who it's for | Problem ("Your fitter didn't measure the room"), question ("Why is there a filler strip by your fridge?"), pattern interrupt (the problem photographed) |
| Social proof | Testimonial, tweet or Reddit screenshot, press, big statistic, quote card, four-panel grid | Social proof (the quote as the first line), number ("38 kitchens, 0 callbacks"), problem (the reviewer's complaint resolved) |
| Mechanism | Feature callout, whiteboard, founder note, tutorial-style listicle, advertorial, FAQ | Number ("Three things I check before I cut"), question ("Why do we measure twice?"), problem ("Nobody tells you who actually fits it") |
| Comparison | Us vs them, myth vs fact, checklist, offer stack (price anchor) | Question ("Flat-pack or made to fit?"), number ("18% more, fitting included"), problem ("Showroom kitchens are designed for rooms that don't exist") |

## The 3 x 3 starter set

The minimum for a new business or a new campaign: three angles, three formats each, nine ads in one ad set. Formats within an angle should differ in kind (one text, one photo, one lo-fi) so the nine are nine concepts, not three concepts in three sizes.

Default for a service business with no prior ads:

| | Format 1 (text) | Format 2 (photo) | Format 3 (lo-fi) |
|---|---|---|---|
| Problem | Problem-agitate-solve statement | Photo + statement of the problem | Text-thread mimic |
| Social proof | Quote card | Testimonial with job photo | Review screenshot |
| Mechanism | Reasons-why listicle | Feature callout with arrows | Whiteboard sketch |

Each ad gets its own hook. Swap an angle for Outcome or Comparison when the brief's core objection points there (price objection: comparison; "will it look right": outcome).

## Small-budget testing cadence

- **Sandbox ad set.** One ad set, ABO (ad set budget), broad targeting with only the location set, campaign objective matching the real goal (leads or sales, not traffic).
- **Budget.** $10 to $20 a day (or the local equivalent) for the whole set.
- **Batch.** 3 to 4 concepts at a time, or the full nine at the higher budget. For each concept 2 to 3 hook variants at most.
- **Duration.** 3 to 5 days before any decision; ads need about 1,000 impressions each to be read.
- **Promote** an ad to the main campaign when hook rate is above 30%, hold rate above 10% (video) and outbound CTR above 1%.
- **Kill** an ad at 1,000 impressions if CTR is below 1.5% (working figure, vendor-sourced, unverified). For statics, hook rate does not apply; use CTR and cost per landing-page view.
- **Record** every result in `campaigns/<slug>/results.md` against the ad's angle, format and hook, so the next batch is chosen from evidence.

## Iterate one variable, hooks first

When an ad is close but not over the line, change one thing and rerun:
1. **Hook** (the first line or first 3 seconds). Cheapest change, biggest effect. 5 to 8 hooks per body.
2. **Format** (same angle and hook, different construction).
3. **Angle** (same audience, different argument). This is a new concept, not an iteration.
4. **Offer or CTA** last, and only for warm and hot audiences.
Never change two of these at once; the result cannot be read.

## Refresh triggers

Replace the ad, not the campaign, when any of these holds for a week:
- CTR down 10% week on week
- Cost per acquisition up 15% against the previous fortnight
- Frequency over 3 on the audience the ad is running to
Expect fatigue in 2 to 3 weeks for a small local audience. Keep a bench of 2 to 3 untested concepts so a refresh is a swap, not a scramble. The first-frame static of a winning video and a new hook on a winning body are the cheapest refreshes.

## The brief fields

The brief is written to `campaigns/<slug>/brief.md` before any ad is made and every ad is checked against it. Fields, after Glickman's template:

1. **Context:** brand, product or service, objective (leads, bookings, sales, followers), platforms, formats, live dates, budget.
2. **Audience:** the segment in the brief's own words; awareness level (cold, warm, hot); the core belief they hold about the category; the core objection, taken from one- and two-star reviews of the category or from lost enquiries.
3. **Single message:** "After seeing this, the customer should feel ___." One sentence. Value proposition in one line. Proof for it, from the claims ledger, with source and date.
4. **Hook direction:** 3 to 5 hooks, each labelled with its class, one recommended.
5. **Creative direction:** reference examples (links or files in `swipe/`), not adjectives; talent (owner, fitter, customer, none); audio; on-screen text; CTA verb and what happens after the click; specs by platform from `specs/`.
6. **Benchmarks and test protocol:** the targets from the cadence above, the kill rule, the date of the first read.
7. **Constraints:** the brand never-list from `brand/voice.md`, policy notes (personal attributes, before/after, competitors, endorsements), anything the owner has vetoed.

A brief with an empty proof field produces ads with no numbers. That is correct; the ledger is filled, not the ad.

## Ad copy, organic post copy and website copy

Three jobs, three sets of rules. The agent does not reuse one as another.

**Ad copy** must earn attention it has not been given, in 1 to 3 seconds, from someone who did not ask.
- Hook first, name last. One idea. A verb-first CTA with an expectation ("Book a survey, we come within a week").
- Cold: 40 to 80 words of primary text; warm and hot: 150 to 250. About 125 characters show before "See more" on Meta; the hook lives inside them.
- Proof ranked: numbers, then authority, then an outcome testimonial, then press.
- No hashtags. No "Learn more". No search headlines reused on Meta.
- The landing page repeats the hook.
- Default frameworks: PAS for cold, AIDA for warm long copy, Hook-Story-Offer for founder video, FAB to tighten one claim.

**Organic post copy** assumes some attention and is measured by comments and saves, not clicks.
- First 100 to 150 characters carry the point; that is what shows before "See more".
- One observation from the work, in first person, with a particular (a job, a street, a material, a number). A question is a good ending; a CTA is not.
- No links in the body on LinkedIn (put it in the first comment); Instagram links are dead anyway. Hashtags: none, or three to five that people actually follow; never a block of twenty.
- Vary sentence length. One line per paragraph throughout is the "broetry" tell; use a single-line paragraph once, for the line that matters.
- It can be longer than an ad (LinkedIn 1,300 to 2,000 characters does well) but it cannot be an ad with the price removed.

**Website copy** answers intent; the reader arrived looking for something.
- Lead with the answer to the query the page ranks for, then the proof, then the next step.
- Full sentences, one claim per section, the same nouns for the same things throughout the site.
- Every section carries a proper noun, number, place or date from the brief; sections without one are cut.
- Proof slots that are empty stay empty and visible; nothing is invented to fill them.
- Written to be read twice, not to stop a thumb; no hooks, no urgency, no "See more" tricks.

Common to all three: the claims ledger, the brand never-list, no "It's not X, it's Y", no tricolons for effect, no personal-attribute targeting in the words, British spelling unless the brand's samples say otherwise.
