---
description: "Review creatives before they are shown or approved: the copy gate (the phrases and shapes generated text falls into), the claims against the ledger, the platform's limits and policy, the render against DESIGN.md, and whether it sounds like this business. Use before attaching a batch, when the owner says check these, does this sound like us, is this allowed, or when check.py or qa.py report findings."
---

# Review

Two passes: the scripts, then the eye. The scripts catch what is
checkable; the eye catches what is generic.

## Pass one: the scripts

```bash
python3 scripts/check.py            # records, the copy gate, the limits, the claims, the specs
python3 scripts/qa.py <id> …        # size, bytes, contrast behind the words, the 9:16 zone
```

Fix every finding at the source (the words in `creative.md` and
`fields.json`, the token in `brand.css`, the claim in `claims.md`), render
again, run again. A finding is never argued with in the reply to the
owner; it is fixed or the creative is not shown.

## Pass two: the eye, in this order

1. **Truth.** Every fact on the frame and in the primary text is in
   `campaigns/<slug>/claims.md` with a source that exists. A number the
   owner said in chat is in `raw/transcripts/` first. A typical result is
   stated when the claim is an unusual one.
2. **Voice.** Read `brand/voice.md`'s signatures and never-list, then the
   copy aloud. Would the owner say this sentence? Does it use their nouns
   (from the lexicon) and not a marketer's? Is there one particular in it
   (a place, a material, a number, a name)? A line that could be any
   business's line is rewritten.
3. **Shape.** The generated-text tells, strongest first: the negation
   pivot ("It's not X, it's Y"), the tricolon, significance inflation
   ("stands as a testament"), promotional adjectives with nothing behind
   them, the "-ing" rider, uniform sentence length across the primary
   text, "Whether you're", "Say goodbye to", "next level", em dashes.
   Rewrite the whole line, never patch the phrase.
4. **One idea.** The frame says one thing; the primary text supports that
   thing; the call to action is the next step for that thing. A second
   idea is the next creative.
5. **The render.** Twelve words or fewer on the image; the headline reads
   at a glance at phone size (Read the PNG at 25% scale: if it is not
   legible, it is not legible in the feed); one accent; the words inside
   the safe zone; nothing that looks like a stock photo or a painted
   interface; the logo smaller than the headline.
6. **Policy.** The platform's sheet in `specs/`: personal attributes,
   health before/after, competitor naming, endorsement disclosure,
   Pinterest's bans, Google's synthetic-content note.
7. **The set.** Across a batch: are they distinct concepts or one concept
   in variants? Do they cover the angles the brief chose? Is the cold
   reader met before the mechanism?

## What to say to the owner

One line per creative: the angle, the format, and the one thing you
changed in review (or "clean"). Then the questions review raised, each
one a fact only the owner can supply. Never a list of what the scripts
found; those are fixed before the owner sees anything.
