---
description: "Write the campaign brief with the owner: product, audience and awareness level, the belief and the objection, the one message, the proof, platforms and formats, constraints, the number that decides. Use before any creative is made, when the owner says let's run a campaign, I want ads for, start with, or when there is no campaigns/<slug>/brief.md yet."
---

# Brief

A creative made without a brief is a guess in brand colours. The brief is
one file, `campaigns/<slug>/brief.md` (from `briefs/_template.md`), agreed
with the owner before the first `new.py`, and it is short: every field is
a fact or a decision, and an adjective is neither.

## How it is written

1. **From the notes first.** Read `brand/positioning.md`, `audience.md`,
   `voice.md`, `public/services.md`, `public/proof.md`, and any earlier
   `campaigns/*/results.md`. Draft every field you can from them, with the
   note named in `sources`. Do not ask the owner what the notes already
   say.
2. **One conversation for the rest.** Ask, in one message, only the fields
   the notes cannot fill, in this order of importance: the offer for this
   campaign (which service, what is included, the price if it is stated);
   who it is for this time and how warm they are (cold: they do not know
   the business; warm: they have seen it; hot: they asked for a quote);
   the objection (what the one-star review says, or what people hesitate
   over: price, time, trust, mess); the proof (a number, a named job, a
   review) and where it is written; the platforms and how much a day; the
   constraint (a policy category such as health or finance, dates, what is
   off limits); the one number that decides (leads a week, booked visits,
   cost per lead) and what would make them stop or scale.
3. **The message.** From the answers, write one sentence the customer
   should feel after seeing the campaign. Read it back to the owner.
   "After seeing this, a Bristol homeowner planning a kitchen should feel
   that the people who draw it are the people who fit it" is a message;
   "quality and trust" is not.
4. **Agree it.** Show the brief, ask "is any line wrong?", set
   `status: agreed`, write the slug into `campaigns/CURRENT`. Then the
   `angles` skill.

## The fields, and what a bad answer looks like

| Field | Good | Not yet |
|---|---|---|
| product | "Fitted kitchens, measured and drawn by us, built in the workshop, fitted in three days" | "our services" |
| audience | "Homeowners in BS3 to BS9 renovating a kitchen, comparing three or four makers" | "everyone who needs a kitchen" |
| awareness | cold | "all" |
| objection | "They think a workshop kitchen costs more than a showroom one" | "price" |
| message | one sentence in the customer's shoes | a list of benefits |
| proof | "public/proof.md#2 (the Clifton review), public/team.md (two people)" | "our reviews" |
| kpi | "booked workshop visits; stop at £40 a booking, scale under £20" | "engagement" |

## What the brief is not

Not a strategy document, not a persona deck, not a place for the brand's
values. Those live in the notes. The brief is the campaign's decisions,
and it changes only when a decision changes (a new line in `updated`, the
old value kept in the body under "Changed").
