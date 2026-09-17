# Visual prompts

How to ask an image model for the picture behind a creative so that it is
this business's picture and not the internet's average of one. The template
sets the words, the logo and the colours; the model paints the scene, and
the scene is where a creative looks generic or looks made. Read this before
the first `scripts/imagegen.py` of a campaign, then work from the format's
recipe below.

## The prompt shape

Every prompt has six parts, in this order, in plain sentences. The script
appends the no-text rule; you write the rest.

1. **Subject and moment.** The owner's actual subject (their work, place,
   product, material, tool, hands) at one specific moment, mid-action or
   just after: "the finished {subject} the morning after, the tools packed
   but one still on the bench". Never the category word on its own.
2. **Composition and point of view.** Where the camera is, what is in the
   frame, what is cropped. Eye level and slightly to the side for work;
   above and close for materials; from the doorway for a room.
3. **Environment, material, light, colour.** Name the materials and the
   light source from the brand's slots ({materials}, {light}): a material
   and a window, a time of day, whether the sun is direct. Colour by
   naming the one object that carries it, not by adjectives.
4. **Copy-space.** Where the words will go and how empty it must be: "the
   lower third is a plain painted wall with nothing on it", "the left half
   is a clean plaster wall". The template's band or scrim sits there.
5. **Mood as visible properties.** Not "warm and trustworthy" but "soft
   shadows, a little dust in the light, nothing staged, a mug half
   drunk". Mood words on their own produce stock.
6. **Exclusions**, as what to show instead where possible (models follow
   "an empty street" better than "no cars"): "the room is empty of
   people", "the surfaces are bare except the pencil".

Keep it to six to ten sentences. A prompt that lists twenty adjectives gets
twenty averaged clichés.

## Pairing it with the brand

The brand notes decide the look before the format does. Pull from them
every time:

- `brand/visual-identity.md` → **Imagery**: what the business's own
  photography shows and never shows, its settings, its light, its
  materials, its palette in the scene. This block is the **style anchor**:
  one paragraph you reuse, verbatim, at the end of every prompt in a
  campaign, so the set looks like one brand. `scripts/imagegen.py --brand`
  appends it for you; `campaigns/<slug>/style.md` holds a campaign's own
  anchor when the campaign departs from the brand's default (`--anchor`).
- `brand/visual-identity.md` → **Colours**: the brand's colour appears in
  the scene on one object ("the brand's green on the van door"), never as
  a tint over everything. With Black Forest Labs the hex may be bound to
  that object in the prompt ("a van door in #1b4332").
- `brand/do-and-dont.md`: what the brand never shows. A rule there beats
  anything here.
- `brand/audience.md`: the people in the picture, when there are any,
  are the audience's people (a homeowner in a real coat, not a model), in
  the audience's places.
- **The owner's own photographs** beat everything. A product shot or a
  photo of the place goes in as a reference (`--ref`) with the product
  lock: "keep the exact label, shape, logo, colour, material and
  proportions of the reference; change only the setting." Real photos of
  real work are used as they are, in the `photo` template, before any
  generation is considered.

An industry changes the slots, not the shape. The same before/after guide
asks for a different scene for every trade because {subject}, {setting},
{light} and {materials} are different; the guide's composition, its
copy-space and its policy stay. Nothing about an industry is in the repo;
it arrives with the brand notes.

## The format guides and the slots

The visual language of each format is universal and ships in
`prompts/<format>.md`; what is specific to the business is a small set of
slots the brand notes fill at run time. `scripts/prompt.py` assembles the
prompt:

```bash
python3 scripts/prompt.py --slots                              # what the notes fill, what is missing
python3 scripts/prompt.py --format before-after --side before --out uploads/before.txt
python3 scripts/prompt.py --format before-after --side after  --out uploads/after.txt
python3 scripts/imagegen.py --prompt-file uploads/before.txt --ratio 4:5 --out creatives/generated/<id>/before.png
```

| Slot | Filled from | Example of the kind of thing (never shipped, always the brand's own) |
|---|---|---|
| `{subject}` | `visual-identity.md` → Imagery → what the owner's photography shows | the work in progress, the finished job, the product, the material |
| `{setting}` | Imagery → Settings | the workshop, the van, the customer's room, the counter, the site |
| `{light}` | Imagery → Light | north window, overcast, one lamp, dawn |
| `{materials}` | Imagery → Materials and objects that carry the brand | what the trade handles, and the one object that carries the brand's colour |
| `{people}` | Imagery → People | none; hands and backs only; the owner by name with permission |
| `{never}` | Imagery → Never shows | what the brand never shows |
| `{anchor}` | Imagery → Style anchor | one paragraph, reused at the end of every prompt |
| `{offer}` | the campaign's `brief.md` → product | what this campaign sells |
| `{audience_place}` | `audience.md` → Where they are when it matters | the place and moment the need shows up |

A slot the notes do not fill is printed as a question, never guessed; the
`sources` skill (or the brain) fills the Imagery block from the crawl and
the owner's words, and the AI can pass `--subject "…"` for one prompt when
the moment needs it. Edit the assembled prompt when the format guide's
moment is not this creative's moment; keep its shape.

The guides: `_general` (inherited by all: composition, light and colour,
mood as visible properties, people, show-instead-of-omit, never), `photo`
(a scene behind a statement), `before-after` (two matched frames; the
change in a person is never a body), `testimonial` (the thing the review
praises, never the reviewer), `product` (the reference product on the
brand's ground), `feature-callout` (room for the arrows), `environment`
(the reader's place at the moment of need: statistic, problem, who it's
for, listicle), `backdrop` (a quiet scene behind a template-only card).
Formats that render entirely from the template (`quote`, `us-vs-them`,
`offer`, `listicle`, `checklist`, `note`, `screenshot`) need no picture.
Add a guide by copying the closest one and keeping its sections: the
composition for the format, the prompt template with slots, the hooks
that fit the picture, the pitfalls, the policy.

## The style anchor

One paragraph, written once per brand from `visual-identity.md` →
Imagery, reused at the end of every prompt:

> "Photographed, not illustrated. {setting}: {materials}, {light}, the
> brand's colour on one thing in the frame. {people}. Nothing staged,
> nothing polished, {never}."

Write it in the same six-part vocabulary. `scripts/imagegen.py --brand`
reads it from the note; a campaign that needs its own writes
`campaigns/<slug>/style.md` and passes `--anchor`. Consistency comes from
the anchor and from reference images, not from seeds (Gemini and OpenAI
have none).

## The tells to refuse in a generated picture

Refuse, and re-prompt when you see them:

- A stranger smiling at the camera; a handshake; a pointing finger; a
  laptop on a desk with coffee; a headset; a team high-five.
- Plastic skin, too-perfect teeth, six fingers, a hand holding a tool
  wrong.
- The HDR look: every surface lit, no shadows, saturated to the edge;
  purple-and-teal grading; a glow around edges; lens flare.
- Painted text, logos, numbers, interfaces, arrows, charts. The template
  does those. Any lettering in the picture means a re-prompt.
- Symmetry and centering by default; a subject floating on a gradient;
  a room with no wear at all.
- "Cinematic, 8k, ultra-detailed, trending" in the prompt. Those words
  are how the average is summoned.
- Anything the brand's do-and-dont forbids; anything from a competitor's
  reference (structure may be borrowed, never the image).

## Provider notes

- **OpenRouter** (Gemini, GPT Image, FLUX through one key): pass the
  aspect ratio; references as data URLs; no seed on the Gemini models.
- **Gemini direct**: up to fourteen reference images; describe the scene,
  do not list keywords; say what to show instead of what to omit.
- **Black Forest Labs (FLUX)**: hex colours work when bound to an object
  ("the van door in #1b4332"); seeds exist and repeat a composition.
- **fal**: the same models by another road; references as image URLs.
- **OpenAI GPT Image**: the best at painted text, which we never want; use
  it for photoreal people only when the brand shows people.

## The loop

Generate two or three candidates for the same prompt (`--seed` where the
provider has one, otherwise the same prompt twice), Read the PNGs, keep
the one that passes the tells above, render the creative, look again at
25% scale. A picture that needs the headline to explain it is the wrong
picture. Record the prompt in the creative's body and the provider and
cost in `visual.png.json` (the script writes it).
