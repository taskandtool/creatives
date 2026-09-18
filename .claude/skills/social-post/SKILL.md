---
description: "Write organic social posts in the business's voice, per platform: Instagram captions and carousels, Facebook page posts, LinkedIn posts for the owner and the page, TikTok captions, Google Business Profile updates, Pinterest pins, Threads. One idea into several posts, the pillars and the cadence, the difference from an ad. Use when the owner says write a post, a caption, what should we post this week, a LinkedIn post, a Google update, or repurpose this."
---

# Social post

Organic is not an ad with the price removed. It opens with a specific
moment, a number or a question the reader recognises, it asks for the
low-friction thing that matches the metric (save, send, reply), it keeps
links out of the body, and it is written to be forwarded to one person.
`references/<platform>.md` holds what performs, the norms, and the
recipes per platform; `references/repurpose.md` the pillars, the one-idea
method, the cadence, and the ad-versus-organic rules. Read the platform
file for the post in hand.

## The record

A post is a creative too (`--kind post`), so it sits on the board, gets
approved, and is posted by the owner or a publisher:

```
creatives/generated/<id>/
  creative.md      kind: post; platform; format (from the platform's recipes); copy.caption; copy.hashtags; claims; files
  master.png       when the post has one image (rendered or the owner's photo)
  slides/          when it is a carousel (the carousel skill)
```

`copy.caption` is the whole post text as it will be pasted, line breaks
included; `copy.hashtags` the three to five tags (or none); the body of
`creative.md` says which pillar it serves and what the reader should do
with it.

## Writing one

1. **Pillar and platform.** From `references/repurpose.md`: education,
   proof, behind the scenes, offer (at most one in five), community.
   Which platform this idea is for first, and what metric matters there
   (Instagram saves and sends, Facebook comments, LinkedIn dwell and
   replies, TikTok shares and watch time, GBP clicks).
2. **The recipe.** The platform file names it (educational carousel,
   before/after, behind the scenes, testimonial repost, offer, FAQ,
   personal story with a lesson, contrarian take, "how we did X", job
   recap, event, update…). Follow its structure.
3. **The voice.** `brand/voice.md`: first person where the owner speaks
   (LinkedIn profile, Instagram BTS), the lexicon's nouns, one particular
   per post (a place, a material, a number, a name), the sentence stats.
   A post that could be any business's is rewritten.
4. **The first line** stands alone: the hook and the payoff in the first
   125 characters on Instagram, about 200 on LinkedIn, 80 on Facebook.
   No hashtags, no emoji, no "Welcome to" before it.
5. **The ask** at the end, one, matched to the metric: "Save this", "Send
   this to someone planning a kitchen", "Reply with your worktop", "Link
   in the first comment". Never "Learn more"; never a link in the body on
   Facebook, LinkedIn, X or Threads.
6. **Hashtags** last: three to five relevant ones on Instagram, TikTok and
   LinkedIn; none or one on Facebook; a topic tag on Threads; none on
   GBP.
7. **Claims** in `claims.md`; a review quoted as written with permission;
   customer photos with permission and credit.
8. **The picture.** The owner's real photo first (phone-shot, natural
   light, hands and tools). A rendered frame (`statement`, `quote`,
   `listicle`) when there is none. Never stock.
9. `python3 scripts/check.py <id>`, then attach the picture and paste the
   caption in the reply as a block, so the owner can read it as it will
   appear.

## One idea, five posts

When the owner gives one idea (a job finished, a question customers ask,
a mistake people make), write the set from `references/repurpose.md`: an
Instagram carousel, a Reel or TikTok script (the `video-script` skill), a
LinkedIn post from the owner, a Facebook photo post with a question, a
GBP update, and optionally a pin and a Threads line. Each is its own
creative; each is rewritten for its platform, not pasted across.

## Never

Broetry (one line per sentence building to a moral); engagement bait
("tag a friend", "like if"); hashtag walls; watermarked reposts; links in
the body where the platform punishes them; a stock photo; a review
edited; more than one offer in five posts; the writing skill's refused
phrases (`review` skill); an em dash.
