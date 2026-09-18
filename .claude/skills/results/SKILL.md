---
description: "Record what a campaign's creatives did and decide what to make next: the numbers from the owner's own ad account (a Meta, Google or LinkedIn connection) or from what the owner pastes, written to campaigns/<slug>/results.md against each creative's angle, format and hook, then the one variable to iterate. Use when the owner says how did it do, here are the numbers, what should we change, or after a batch has run three to five days."
---

# Results

A creative's record says what it was (angle, format, hook, awareness);
`results.md` says what it did. Together they make the next batch a
decision instead of a guess. The rule is one variable at a time: hooks
first, then format, then angle.

## Where the numbers come from

1. **The owner's ad account**, through a connection the owner granted
   (Meta Marketing API insights at ad level with placement breakdowns;
   Google Ads; LinkedIn ad analytics). `list_connections()` from
   `tools/taskandtool.py` says what this app holds; call through the
   proxy (`call_connection(slug, "GET", path, query)`) for the last seven
   days at ad level: impressions, reach, frequency, 3-second plays,
   ThruPlays, link clicks, results, spend. Map each ad to its creative by
   the id the owner used when uploading (ask them to name ads by our
   `id`).
2. **Pasted by the owner** when there is no connection: a screenshot (Read
   it) or a table. Write what they gave, dated, and say what was missing.
3. **Organic**: saves, sends, comments, reach per post, from the
   platform's insights the owner pastes; the metric the platform file
   names as the one that matters.

## What to compute

Per creative, and per angle, format and hook across creatives:

- hook rate (3-second plays over impressions; 2-second on TikTok),
  hold rate (ThruPlays over 3-second plays), outbound CTR, cost per
  result, frequency; the working targets are hook over 30%, hold over
  10%, CTR over 1% (vendor benchmarks, so a direction, not a law);
- for statics without video metrics: CTR and cost per result, and the
  relative ranking inside the batch;
- the refresh triggers: CTR down 10% week on week, CPA up 15%, frequency
  over 3.

`campaigns/<slug>/results.md` is a dated table, one row per creative per
period, plus a "what we learned" list in plain sentences, each one tied
to an angle, format or hook, never to "the creative".

## What to change

- Low hook rate: the first three seconds or the first line; new hooks on
  the same body (five to eight), nothing else changes.
- Hook fine, hold low: the promise is not kept by second six; the
  structure or the beats.
- Hold fine, CTR low: the offer or the call to action; the primary text.
- CTR fine, cost per result high: the landing page or the audience, not
  the creative; say so.
- Everything fine, then fading: frequency; a new concept, not a variant.

Write the next batch as rows in `angles.md` with the reason each row
exists ("hook variant of #3, which held at 14% but hooked at 21%"). Then
the craft skill makes them. Winners move to `creatives/posted/` with the
URL when the owner confirms; losers to `rejected/` with the number that
decided it, so they are not remade next month.
