# templates/

The compositions `scripts/render.py` fills. `brand.css` holds the tokens
(DESIGN.md explains them); `fonts/` holds the brand's font files and
`fonts.css` (scripts/fonts.py fetches Google Fonts; a licensed font is
added by hand). Each `<name>.html` is a template in a mustache subset:
`{{field}}` escaped, `{{{field}}}` raw, `{{#list}}…{{/list}}`,
`{{^absent}}…{{/absent}}`. The fields each one takes are the keys
`scripts/new.py` writes into `fields.json`:

| Template | Fields |
|---|---|
| `statement` | headline, body?, cta?, tone (`dark` for the dark ground) |
| `photo` | image, headline, body?, cta? (a scrim band over the visual) |
| `quote` | quote, who, where?, cta?, tone |
| `us-vs-them` | headline, left_label, right_label, rows [{left, right}], cta?, tone |
| `before-after` | before_image, after_image, before_label, after_label, headline, cta?, stacked (9:16) |
| `offer` | headline, includes [..], price, was?, deadline?, cta?, tone |
| `listicle` | headline, items [text or {n, text}], cta?, tone |
| `product` | image, headline, label?, cta?, ground? (a brand colour token name) |
| `checklist` | headline, items [{text, done}], cta?, tone |
| `note` | text, signoff? (the sticky note; the only rotation allowed) |
| `screenshot` | one of thread {messages [{text, mine}]}, notification {app, when, title, text}, review {stars, text, who, when}, comment {who, text, reply}, app {title, rows [{left, right}], footer?} |
| `banner` | offer (the number or the words, big), headline, terms?, cta?, ground? (the offer-first sale banner) |
| `snapshot` | image, caption? (a phone photo as the ad, one caption chip, nothing else) |
| `steps` | headline, steps [{n, title, text?}], cta?, tone (how it works, a mechanism, an infographic) |
| `proof-stack` | rating, count, source, quotes [{text, who}], cta?, tone (the social-proof mashup; every item real) |
| `grid` | headline?, columns (2 or 3), cells [{image?, text?}], cta?, tone (starter pack, the range, an education grid) |
| `stats` | headline, stats [{value, label}], source?, cta?, tone (a case study or results) |

Every template also takes `business` (the label) and `logo` (a file under
`brand/logo/`, shown as the mark instead of the name). Add a template by
copying the closest one; keep to the classes in `brand.css`.
