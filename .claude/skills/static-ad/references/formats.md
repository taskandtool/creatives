# Static ad formats

A catalogue of static ad formats, each written as a recipe the agent follows. Every recipe has the same seven lines so the agent can pick one, fill it from the brief and the claims ledger, and hand the result to a template. The worked examples use a made-up business, Harlow Joinery, a workshop in Bristol that makes fitted kitchens; the copy patterns in brackets are the reusable part, the example only shows the pattern filled. Every number in an example is illustrative; the agent replaces it with a figure from the claims ledger or drops it.

## Where this list comes from

The 45 formats below are the union of the static formats named by the catalogues that publish them, checked on 7 Sep 2026: Motion's visual-format library (113 named formats, tagged across $1.29 billion of spend and 578,750 creatives in its Creative Benchmarks 2026), Motion's static-ads playbook, Common Thread Collective's 30 types, Demand Curve's format lesson, Contrast Digital's 13 styles, Superscale's static-ad guide, Hawky, Backlinko's 14 examples, Adrio's 7 formats and 12 examples, Konstant Kreative's prompt types, Fraggell's six, and Alex Cooper's (Adcrate) public writing on his 40-format static playbook (the playbook itself is behind a sign-in). A format is here when at least two of those name it; the order inside each group follows how many name it. Hit rates and spend shares are Motion's own reporting from that benchmark and are not independently verified; no other performance figure below is verified unless it says so.

Every description, recipe and example below is written for this repository. Nothing is copied from those sources: what was taken from them is the name of a format (industry vocabulary that no one owns) and, where a figure is quoted, the figure with its source named beside it. Motion's library states that it is published to be cited, and asks to be cited as: "Motion — Creative analytics platform for paid social. See: https://motionapp.com/llm-info". This repository is not affiliated with, endorsed by, or licensed from Motion or any other source named here. A statistic here is a fact reported by the named source and is quoted for reference; the words around it are ours.

What the benchmark says about the field, before any single format: text-only and product-image-with-text creatives lead both hit-rate leaderboards; the offer-first banner is 21.9% of creatives and 29.3% of spend at an 8.6% hit rate; testimonial is 13.3% of spend at 6.5%; the formats that punch above their use are the letter (about 1.7x), unconventional text placement (about 1.5x), the post-it (about 1.3x) and celebrity or expert endorsement (2.1x). Lo-fi is 14% of ads and 42% of top performers.

## How to choose

- An ad is one **angle** (what we are saying) in one **format** (how the image is built) with one **hook** (the first line). Pick all three on purpose. The angle taxonomy and the angle x format x hook matrix live in `angles/references/strategy.md`.
- **One idea per ad.** If a draft carries two claims, split it into two ads.
- **The 3 x 3 starter set.** For a new business or campaign, produce three angles in three formats each, nine ads. A sensible default for a service business: outcome, social proof and problem, each in a photo + statement, a testimonial and one native or lo-fi format. For a business with an offer, the offer-first banner is in the first nine.
- **Distinct concepts beat variants.** Since Meta's Andromeda ranking rollout (global, Oct 2025) an ad set does better with 8 to 15 ads that each carry a different angle than with one ad in twelve colourways. Keep similarity between concepts in an ad set under about 40% (Segwise figure, unverified). Vary the copy shape too: a question, a list, a quote, a statement.
- **Lo-fi wins more often than it is used.** Sticky notes, screenshots, text threads and phone photos are not a fallback for a business without a photographer; they are a first choice.
- **Funnel stage** in each recipe: top (cold, has not heard of us), mid (warm, has seen us or has the problem in mind), bottom (hot, has visited, enquired or abandoned).
- **Templates.** Each recipe names one of the HTML templates: statement, photo, quote, us-vs-them, before-after, offer, banner, listicle, checklist, steps, product, snapshot, proof-stack, grid, stats, note, screenshot. "Photo + statement" means a generated or supplied image with a headline overlay through the `photo` template; the picture's prompt comes from `prompts/<guide>.md` through `scripts/prompt.py`.
- **Sizes.** Feed 4:5 at 1080 x 1350 (1:1 underperforms); Stories and Reels 9:16 at 1080 x 1920 with copy kept out of the top 14% and bottom 35%. Meta penalises images with a short edge under 1080 (unverified).

## The recipes

### Us vs them
When: Mid funnel. The buyer is comparing options and the business wins on criteria the buyer already cares about.
Structure: Two columns, "the alternative" on the left and the business on the right (the template ticks the right column and crosses the left), three to five rows of the buyer's real criteria with a tick, a cross or a short value in each cell.
Copy: Header names the two columns; rows are the buyer's criteria, not ours. Example: column heads "A flat-pack kitchen" and "Harlow Joinery". Rows: "Made to fit your walls: yes / cut down on site", "Carcass: 18 mm birch ply / chipboard", "Who fits it: the joiner who made it / whoever the retailer sends", "Lead time: 8 weeks / 2 to 12 weeks", "Repairable in ten years: yes / discontinued range".
Visual: Flat table on a plain ground, brand colour on our column header only. Optional small product photo above the table. No copy-space needed beyond the table.
Why it works: It does the comparison the buyer was going to do anyway, on our terms.
Pitfalls: Naming a competitor invites disapproval, a trademark complaint and a takedown tone; compare against a category ("a showroom chain", "flat-pack"). Every cell must be true for the whole category, not one bad example. Rows the buyer does not care about (our founding year) waste the format. Keep to five rows or it becomes unreadable at feed size.
Template: us-vs-them

### Before/after
When: Mid to bottom funnel. There is a visible transformation the business can show with its own photos.
Structure: Two frames side by side or stacked, labelled Before and After, one short line under or over them.
Copy: "[What it was] to [what it is], [time or place]". Example: "A 1970s galley in Bishopston, before and after. Eight weeks from survey to fit." Non-literal variant for a service with nothing to photograph: "Before: three quotes, three drawings, three different measurements. After: one joiner measures, draws and fits."
Visual: The two photographs, same angle, same crop, same light where possible. Copy-space is a band across the top or bottom, or the labels only.
Why it works: The eye finds the difference before the reader has decided whether to read.
Pitfalls: Meta restricts before/after for health, weight and skincare (allowed only for general cosmetic use, 18+, no close-ups implying a flaw); Pinterest bans the format outright. Never generate or composite the "after" of a real job; if the pair is illustrative, say so on the image. Mismatched angles or lighting read as a fake.
Template: before-after

### Testimonial or review screenshot
When: Warm audiences. The business has at least one specific, sourced review.
Structure: The review as a screenshot or a quote card, the reviewer's first name and town, a small product or job photo, and one proof detail under it.
Copy: The most specific sentence of the review as the hook, then the rest, then one fact. Example: "'They measured the room twice and the drawers still close on a wall that isn't square.' Ruth, Redland. Google review, March 2026. Solid oak fronts, birch ply carcass, fitted in four days."
Visual: A real screenshot (Google, Checkatrade, Trustpilot) with the platform chrome kept, or a quote card in the brand type. Copy-space is the card itself; the photo sits behind or beside it.
Why it works: A stranger's specific complaint resolved is more believable than any claim we make ourselves.
Pitfalls: Vague praise ("great service, would recommend") has no hook; pick the review with a detail. Never invent a review or a name, and never edit the wording; FTC and ASA rules treat that as a fake endorsement. If results are unusual, say what is typical. Variants: Social Proof Mashup (three to five short reviews stacked) and Social Comments (a post with its own comments).
Template: quote or screenshot

### Sticky note
When: Top to mid funnel. One short message that should not look like an ad.
Structure: A single handwritten note on a plain or photographed ground, one to twelve words, the logo small or absent.
Copy: One thought, written the way a person writes a reminder. Example: "Measure the room before you order the kitchen. Or we will." Or: "Drawers that still close in 2036."
Visual: A yellow or brand-tinted note, handwritten type or a real photographed note on a worktop, a fridge, a site wall. Copy-space is the note.
Why it works: It breaks the pattern of polished feed content and reads as a person's thought, so it earns the second it needs.
Pitfalls: Two notes, or a note plus a headline, kills it. A polished "handwritten" font on a perfect gradient reads as an ad again. The message must stand alone; no explanation on the image.
Template: note

### Native-UI mimic
When: Mid funnel. A relatable moment of the buyer's problem can be shown as something that happens on their phone.
Structure: A faithful copy of one phone interface with the message inside it: a text thread, a notification, a Notes app page, an AirDrop prompt, a checkout screen, an email, a calendar entry.
Copy: One relatable pain in the interface's own voice, then one specific benefit. Examples for Harlow Joinery:
- Text thread: "Fitter's cancelled again" / "Third time?" / "Third time." / "Harlow send the joiner who built it. Same person, start to finish."
- Notification: "Harlow Joinery: Your kitchen is cut. Fitting starts Monday 14th."
- Notes app: title "Kitchen quotes", lines "Showroom chain: 3 visits, still no drawing", "Harlow: measured Tuesday, drawing Friday, price on the drawing".
- AirDrop: "Harlow Joinery would like to share 'Your kitchen, drawn to your walls.pdf'".
- Checkout: line items "Survey: £0", "Drawings: included", "Fitting by the maker: included".
- Email: subject "Your kitchen is in the workshop", preview "Photos of the oak fronts attached, fitting in 12 days."
- Calendar: "Survey, Harlow Joinery, Thursday 10:00, 45 min. They measure, you keep the drawings."
Visual: The interface at real proportions on a plain ground or a phone photo. Copy-space is the interface; nothing outside it except a small logo if the interface does not carry the name.
Why it works: The reader's eye has been trained to read these screens first and without deciding to.
Pitfalls: Polish is the enemy; a wrong font, wrong spacing or a made-up interface breaks the effect. Generic dialogue ("Hey, have you tried Harlow?") reads as an ad on the first line. Do not fake a real person's name or a real notification from another brand. Keep to one screen.
Template: screenshot

### Tweet or Reddit screenshot
When: Top to mid funnel. The business has a customer or owner post, or can write one in the owner's own voice and publish it first.
Structure: A screenshot of a single post, or a post with one reply, on a plain ground.
Copy: Written the way people talk about the problem in public, not the way we describe the product. Example (owner's post): "Fitted a kitchen today where the previous fitters had scribed the plinth to a floor that isn't there any more. Measure the room you have, not the plan." Pair it in the primary text with 150 to 250 words of problem, agitation and solution for the 35+ Facebook feed audience.
Visual: The post at real proportions with real chrome. Copy-space is the post.
Why it works: It mirrors how buyers already discuss the category, so it reads as a conversation rather than an offer.
Pitfalls: Publish the post for real before screenshotting it; a screenshot of a post that does not exist is fabricated proof. Never lift a stranger's post without permission. Do not add a headline outside the screenshot.
Template: screenshot

### Founder note or letter
When: Top to mid funnel. The owner has a reason for starting the business that a buyer would recognise.
Structure: Text only, set as a letter or a note, signed with a first name, optionally a small photo of the owner or workshop.
Copy: Built-because, then the old pain, then one proof, then the ask. Example: "I started Harlow Joinery after fitting other people's kitchens for eleven years and watching the same thing go wrong: the person who measured was never the person who fitted. So here the same joiner does both. Forty kitchens so far, none of them level floors. If you want yours measured properly, book a survey. Tom."
Visual: Plain ground, brand type at reading size, the signature the only decoration. Copy-space is the whole image.
Why it works: A first-person reason is harder to dismiss than a claim, and it gives the reader a person to reply to.
Pitfalls: Corporate tone ("our mission", "we pride ourselves") breaks it. More than about 80 words on the image is unreadable in feed; move the rest to the primary text. The proof must be from the ledger.
Template: note

### Feature callout with arrows
When: Mid funnel. The product has three to five physical details that map to benefits the buyer cares about.
Structure: One product photo with three to five short labels, each attached by a line or arrow to the detail it names.
Copy: Each label is a benefit with the feature as the reason, six words or fewer. Example labels on a kitchen photo: "Solid oak fronts, oiled not lacquered", "18 mm birch ply, not chipboard", "Soft-close runners rated 100,000 cycles", "Scribed to your wall, no filler strip". Optional offer band at the bottom (Motion finds an Offer-First banner on about half of these).
Visual: A clean product or job photo with room around it for labels. Copy-space is the margin around the subject.
Why it works: The reader gets the benefit list without reading a list.
Pitfalls: Overcrowding; five labels is the ceiling. Features without the benefit ("18 mm ply") mean nothing to a buyer. Labels must point at the real detail, not float.
Template: product

### Press "as seen in"
When: Mid to bottom funnel, higher-value purchases where trust is the bottleneck.
Structure: One product or job photo, a row of outlet logos or a single quoted headline with the outlet name.
Copy: The outlet's own words, attributed. Example: "'A Bristol workshop that measures twice.' Bristol Post, May 2026." Or a logo row: Bristol Post, House & Garden, Homebuilding & Renovating, only if each has covered the business.
Visual: Photo above, press band below. Copy-space is the band.
Why it works: A third party has already spent its credibility on us.
Pitfalls: Cannot be faked; every logo needs a real piece the agent can link to in the ledger. Outlets the buyer does not know add nothing. A paid placement is not press; label it if used.
Template: quote or product

### Offer stack / price anchor
When: Warm and retargeting audiences. There is a concrete offer with a deadline or a limit.
Structure: The offer as the header, three to five stacked items with a value each, the price or the saving, the deadline, one line of risk reversal, the call to action.
Copy: Example: "Autumn fitting slots. Survey and drawings (usually £250): included. Fitting by the joiner who made it: included. Ten-year guarantee on carcasses: included. Four slots left before Christmas. Book a survey."
Visual: Plain ground or a photo faded behind a band. Copy-space is the full width; the offer header is the largest type.
Why it works: Listing what is included makes the price feel earned before the reader sees it.
Pitfalls: A fake deadline or a fake "usually £250" is a pricing claim the ASA will act on; the ledger must hold the normal price. Do not send a cold audience here; they have no context for the offer. Keep the stack to five lines.
Template: offer

### Meme or reaction
When: Top funnel, only when the product fits the meme's logic without explanation.
Structure: A known meme template or a reaction photo with one caption line in the meme's own convention.
Copy: The joke is about the buyer's situation, and the product is the punchline or the caption. Example: two-panel reaction, top "Kitchen fitter says he'll be there Monday", bottom "Which Monday". Caption: "Harlow Joinery. The joiner who built it fits it. Dates on the drawing."
Visual: The meme image with its usual text placement. Copy-space is where the meme puts it.
Why it works: The reader recognises the format before the message and is already amused when the name arrives.
Pitfalls: If the meme needs the product explained, it fails. Meme images are often someone's copyright; use a photograph the business owns or a licensed stock image in the same shape. Memes date within weeks.
Template: photo + statement

### Reasons-why listicle
When: Mid funnel. The business has three to five reasons, each of which is a small proof rather than an adjective.
Structure: A numbered list of three to five lines, a header that promises the count, optional photo.
Copy: "[N] reasons [audience] choose [business]", each reason a fact. Example: "3 reasons Bristol homeowners pick Harlow Joinery. 1. One joiner measures, draws and fits. 2. 18 mm birch ply carcasses, not chipboard. 3. Drawings before a deposit, so you see the kitchen before you pay." Text versions of this outperform talking-head versions.
Visual: Plain ground or a photo with a solid band for the list. Copy-space is the band.
Why it works: A count sets an expectation of effort that is cheap to meet, and each line is a separate reason to believe.
Pitfalls: Adjectives instead of proof ("1. Quality. 2. Service. 3. Value.") is the standard failure. More than five lines is a wall of text at feed size.
Template: listicle

### Big statistic
When: Mid to late funnel where trust is the bottleneck. Not for cold audiences, who have no context for the number.
Structure: One number set very large, one line of context under it, the source small.
Copy: "[Number] [what it counts]. [Source or period]." Example: "0 callbacks in 2025. 38 kitchens fitted, none needed a return visit. Harlow Joinery job log."
Visual: Plain ground, the number filling half the height, brand type. Copy-space is the whole image.
Why it works: A single verifiable number is the fastest proof there is.
Pitfalls: The number must be in the ledger with its source and date. Percentages without a base ("98% satisfied") are unverifiable and read as a tell. Two numbers on one image is two ads.
Template: statement

### Problem-agitate-solve
When: Top funnel, the default cold format. The buyer has the problem but has not thought of us.
Structure: The problem named as the header, a visual of the problem, the specific result as the resolution, the call to action.
Copy: Problem, then what it costs, then the result. Example: "Your kitchen fitter didn't measure the room. Now there's a 40 mm filler strip by the fridge and a drawer that hits the wall. We measure twice and cut in our own workshop. Book a survey." In video the split is about 60% problem and agitation, 40% solution; on a static, keep the problem to the header and the image.
Visual: A photo of the problem (the filler strip, the drawer that hits the wall) with the copy in a band. Copy-space is the band, top or bottom.
Why it works: The reader recognises their own situation before they recognise an ad.
Pitfalls: Agitating with fear the buyer does not feel reads as a sales tactic. Do not imply anything about the reader personally (see the Meta personal attributes note under Who it's for).
Template: photo + statement

### Product on a coloured ground / studio shot
When: Any stage; the workhorse for retargeting and catalogue ads.
Structure: The product or a detail of it on a flat colour or a studio backdrop, the name and one line of copy.
Copy: The product name and one fact. Example: "Oak shaker fronts, oiled. Made in Bristol, fitted by the maker." For retargeting, swap the line for the offer.
Visual: A generated or shot image of the object on a single brand-adjacent colour, copy-space in a clear third of the frame. The colour should not be a tint of the product.
Why it works: Nothing competes with the object; the reader knows in a glance what is being sold.
Pitfalls: Generated product images must not show a product the business does not make or a room it did not fit; label illustrative renders as such. Bland at cold reach; it needs the offer or the fact to earn a stop.
Template: product

### Who it's for (and not for)
When: Top funnel, where a demographic or role hook is the strongest opener. Lower volume, better cost per acquisition. Dara Denney's 2025 review of top hooks put demographic hooks first (secondary source, unverified).
Structure: A statement naming the audience by situation, optionally a second line naming who it is not for, one photo.
Copy: "[Situation], this is for you. [One line of why.] Not for [situation]." Example: "Renovating a Victorian terrace in Bristol? This is for you. We make kitchens to fit walls that aren't square. Not for you if you want it next week: our lead time is eight weeks."
Visual: Photo of the situation (the terrace, the odd-shaped room), copy in a band. Copy-space is the band.
Why it works: Naming the situation gives the reader permission to stop and the rest to scroll on, which improves who clicks.
Pitfalls: Meta's personal attributes policy: never assert or imply knowledge of the reader's race, religion, age, sexual orientation, gender identity, disability, health, financial status, criminal record or name. "Over 60?" is banned; "Kitchens for retirement homes" is allowed. Write about the situation, the home or the product, never "your" condition. The "not for" line must be true and useful, not a humblebrag.
Template: statement or photo + statement

### Whiteboard or hand-drawn
When: Mid funnel. The topic is complex or dull and a sketch explains it faster than a photo would.
Structure: A hand-drawn diagram or a whiteboard photo with marker writing, one caption.
Copy: The drawing carries the idea; the caption names it. Example: a sketch of a wall with a 12 mm lean marked, a cabinet scribed to it, and the note "This is why we measure twice." Caption: "Old houses lean. We cut the cabinet to the wall, not the wall to the cabinet."
Visual: A real whiteboard or paper photographed, or a drawn asset in a single marker colour. Copy-space is the board.
Why it works: It looks like someone explaining, not someone selling.
Pitfalls: A polished vector "sketch" loses the effect. More than one idea on the board is a lecture. Handwriting must be legible at 1080 wide.
Template: note

### Four-panel checkerboard grid
When: Mid funnel. The business has two or more product photos and two or more short claims and wants carousel density in one static.
Structure: A 2 x 2 grid alternating copy tiles and photo tiles, so each row has one of each.
Copy: Each copy tile is one claim of six words or fewer. Example: tile 1 "Made in our Bristol workshop", tile 2 photo of the bench, tile 3 photo of a fitted kitchen, tile 4 "Fitted by the joiner who made it".
Visual: Two photos and two solid-colour copy tiles, brand colour, equal squares. Copy-space is the two solid tiles.
Why it works: Four tiles read as four proofs of one story in the time a single image gets.
Pitfalls: Four claims with no photo is a listicle done badly; keep the alternation. Photos must be the business's own. The whole grid must still make sense at thumbnail size.
Template: product or listicle

### Anti-ad
When: Top funnel. The business can lead with a negative review, an admission or a joke at its own expense and answer it.
Structure: The objection large, the answer smaller under it, optionally the objection as a screenshot of a real comment.
Copy: The objection in the critic's words, then the reply. Example: "'Eight weeks is a long wait for a kitchen.' It is. It is also how long it takes to make one properly rather than pick one off a shelf. Book a survey and we will tell you the exact date." Variant: the "sceptic in the comments" rebuttal, a real doubting comment answered under the post.
Visual: Plain ground for the text version, or the real comment screenshot above a photo. Copy-space is the top half.
Why it works: Admitting the weakness first removes the reader's reason to distrust the rest.
Pitfalls: The objection must be one the business really faces; a straw man is obvious. Do not fabricate a negative review. The answer has to be a real answer, not a reframe.
Template: quote or statement

### Advertorial
When: High-consideration purchases, mid funnel. The reader wants to learn before they buy.
Structure: An editorial headline, one photo, two or three bullet findings, a source line, a soft call to action.
Copy: Headline in the register of a magazine piece, not an offer. Example: "Why fitted kitchens in older Bristol homes fail at the walls. Three things a joiner checks before cutting: whether the floor is level (most are not), whether the walls are plumb (a 12 mm lean is common), where the services come through. Source: Harlow Joinery survey notes, 2025. Read the full checklist."
Visual: Photo as a magazine would crop it, the headline over or under it, bullets in a column. Copy-space is a third of the frame.
Why it works: It answers the question the buyer typed into a search box, so it is read rather than skipped.
Pitfalls: A wall of text at feed size; the bullets stay short and the long version lives on the landing page. Label it as an ad where the platform requires. Findings need a source in the ledger, even if the source is our own job notes.
Template: listicle or photo + statement

### First-frame iteration
When: Any stage where a video already exists. Takes the opening frame of a winning video and turns it into a static, then iterates the headline.
Structure: A screenshot of the video's first frame, the spoken hook set as the on-screen headline, nothing else.
Copy: The hook, word for word, as the headline. Example from a Harlow Joinery talking-head video: frame of the joiner holding a scribed cabinet end, headline "This is the bit your fitter skips." Iterate by swapping the headline for the other tested hooks against the same frame.
Visual: The video frame, copy-space where the video's caption sat. Keep any lo-fi quality; it is part of why the video worked.
Why it works: The video has already proven the frame stops people; the static reuses that proof cheaply and 30 headlines can be tested from one frame.
Pitfalls: Only from a video that performed. Do not tidy the frame; a graded, cropped version is a different ad. Check the frame has no face of a person who has not consented to stills.
Template: photo + statement

### Checklist
When: Mid funnel. The buyer is preparing to choose and a list of things to check positions the business as the one that passes.
Structure: A header naming the decision, four to six tick-box lines, the business's name last or in the header.
Copy: "[N] things to check before [decision]", each line a check the business passes and many competitors do not. Example: "Before you order a fitted kitchen, check: the carcass material is named on the quote; the person measuring is the person fitting; the drawings arrive before the deposit; the guarantee covers the carcass as well as the hinges. Harlow Joinery passes all four."
Visual: Plain ground, tick boxes ticked, or a printed checklist photographed on a worktop. Copy-space is the whole image.
Why it works: The reader takes the list into their next quote, and it is written in our favour.
Pitfalls: Any line we do not pass. Lines that only we could pass read as rigged. Six lines is the limit.
Template: checklist

### Myth vs fact
When: Mid funnel. The category has a belief that stops buyers and the business can correct it with evidence.
Structure: Two blocks, "Myth" and "Fact", the myth struck through or in a muted colour, the fact in brand colour, a source line.
Copy: Example: "Myth: a made-to-fit kitchen costs twice a showroom one. Fact: our average 2025 kitchen came in 18% above the equivalent showroom range, with the survey, drawings and fitting included. Source: Harlow Joinery quotes, 2025." Or: "Myth: eight weeks is slow. Fact: showroom lead times in Bristol ran 2 to 12 weeks in 2025, and ours includes fitting."
Visual: Plain ground, two stacked blocks, or a photo behind a band. Copy-space is the full image.
Why it works: The reader holds the myth already; correcting it moves them without asking them to believe a claim from nothing.
Pitfalls: The fact needs a source in the ledger; a myth corrected by an opinion is two opinions. Do not name a competitor as the source of the myth. Health and finance myths carry policy risk; keep to the product.
Template: us-vs-them or statement

### Quote card
When: Any stage. A single sentence from the owner, a customer or a third party carries the whole message.
Structure: The sentence large, the attribution small, a plain or textured ground, no photo needed.
Copy: The quote and who said it, with the source where it is a customer or press. Example (owner): "'We cut the cabinet to the wall, not the wall to the cabinet.' Tom Harlow, Harlow Joinery." Example (customer): "'The drawing was the kitchen. No surprises on fit day.' Priya, Southville, Google review, June 2026."
Visual: Brand type at display size, quotation marks as the only ornament. Copy-space is the whole image.
Why it works: One good sentence is read in the time a photo is glanced at.
Pitfalls: Customer quotes must be real and unedited. An owner "quote" that is a slogan is a statement, not a quote; use the statement template and drop the marks. Over 20 words needs a smaller size and loses the format.
Template: quote

### FAQ / "people ask us"
When: Mid funnel. The same question arrives in every enquiry and the answer is a reason to buy.
Structure: The question as the header in the customer's words, the answer under it, one photo or a plain ground.
Copy: "People ask us: [question]. [Answer in two sentences.]" Example: "People ask us: do you fit kitchens in flats with no lift? Yes. We make the carcasses in sections that fit a stairwell and assemble them in the room. Thirty-one flats in Clifton and Redland so far."
Visual: Plain ground with the question in brand colour, or a photo of the situation the question is about. Copy-space is the top half.
Why it works: A question the reader has already asked themselves is the shortest route to their attention.
Pitfalls: A question nobody asks ("What makes Harlow different?") is a slogan in disguise; take questions from the enquiry inbox or `public/faq.md`. The answer must be true for every case, or say when it is not.
Template: statement

### Offer-first banner
When: Bottom and mid funnel, and any retargeting. The single most used and most funded static format (Motion: 21.9% of creatives, 29.3% of spend, 8.6% hit rate). Use when there is a real offer with a real end date.
Structure: The offer as the biggest thing on the frame (a number, a word), one line of what it applies to, the terms small, the call to action.
Copy: "[The offer, as a number or two words]. [What it is on]. [Until when or for whom]." Example: "£300 off. Any kitchen drawn in October. Ends 31 October."
Visual: The template's ground in the brand's colour, or a product photo behind a scrim; no scene needed.
Why it works: A warm reader already knows the business; the only new information is the offer, so the ad says only that.
Pitfalls: Fake deadlines and perpetual "sales"; an offer without a mechanism to claim it; stacking urgency words; using it on cold traffic that has no context.
Template: banner

### Headline-only (text-only)
When: Any stage. Motion's top asset type by hit rate. Use when the claim is stronger than any picture the business has.
Structure: One line of large type on a plain ground, the business name small, a call to action or none.
Copy: "[The claim in the customer's words, twelve words or fewer]." Example: "The people who draw your kitchen are the people who fit it."
Visual: None. The ground and the type are the ad; the accent appears once at most.
Why it works: In a feed of pictures a plain sentence is the interruption, and it reads in one second.
Pitfalls: A vague claim ("quality you can trust"); a headline that needs a second line; decorative type; a gradient ground.
Template: statement

### Lifestyle / product in use
When: Top and mid funnel. The product or the work in the customer's own setting, being used.
Structure: A photograph with the words in a band at the bottom or top; the product or the work is the subject, a person appears by their hands or back.
Copy: "[The outcome for the person, one line]. [The call to action]." Example: "Cooking in it by Friday. Book a workshop visit."
Visual: The owner's own photo first; otherwise the `photo` prompt guide with the setting filled from the brand's Imagery block. The copy-space is the plainest third of the frame.
Why it works: The reader sees the product in a life that looks like theirs, not on a white ground.
Pitfalls: Stock lifestyle (a stranger smiling); a scene so styled it reads as a catalogue; a product too small to recognise.
Template: photo

### Phone snapshot (UGC-style photo, the ugly ad)
When: Top funnel. A photo that looks like a customer or the owner took it on a phone, one caption chip, nothing else.
Structure: The photo fills the frame; one short caption in a white chip, as a phone's own caption would be; no headline, no logo.
Copy: "[One sentence a person would type under their own photo]." Example: "Day three and the doors are on."
Visual: A real phone photo (the owner's, or a customer's with permission) is the point; a generated one follows the `snapshot` prompt guide (flash, tilt, a bit of mess) and the record's notes say it is illustrative.
Why it works: It does not look like an ad, so the reader's ad filter does not fire; lo-fi is 42% of top performers.
Pitfalls: Making it look designed; a caption that sells; a generated photo passed off as a customer's.
Template: snapshot

### How it works (mechanism, infographic)
When: Mid funnel, for a product or service whose method is the difference. Also the "three steps" ad.
Structure: A title, then three or four numbered steps down the frame, each a short title and one line.
Copy: "[Title: the promise]. 1 [step] 2 [step] 3 [step]." Example: "How a kitchen gets fitted in three days. 1 We measure. 2 We build it in the workshop. 3 The same two people fit it."
Visual: None needed; the numbers and the type carry it. A small photo per step only when the owner has them.
Why it works: A method is a reason to believe; three steps is the number a reader keeps.
Pitfalls: More than four steps; steps that are features in disguise; a diagram the reader must study.
Template: steps

### Social proof mashup (trust stack)
When: Mid and bottom funnel. Several forms of proof on one frame: a rating, a count, two short quotes, a badge.
Structure: The rating big, the count beside it, the source small, then two quotes in frames, then the call to action.
Copy: "[Rating] [count of reviews] on [source]. "[Quote one]" [who]. "[Quote two]" [who]." Example: "4.9 from 118 reviews on Google. "They measured twice and it shows." Ruth, Redland."
Visual: None; every element is text from the ledger. Never a star graphic the model painted.
Why it works: One review can be luck; a rating plus a count plus two voices reads as a pattern.
Pitfalls: Any number not in the ledger; rounding a rating up; quotes edited; a source that cannot be checked.
Template: proof-stack

### Comment response (reply to a comment)
When: Mid funnel. A real question or objection from a comment, quoted, and the business's reply under it.
Structure: The comment as a card (the commenter's first name, the words), the reply below it marked as the business's, a small business label.
Copy: "[The comment, verbatim]. [Business] replied: [the answer, plain, one claim]." Example: "Do you do just the doors? Harlow Joinery replied: Yes, and we fit them the same week we make them."
Visual: The `screenshot` template's comment variant; no picture.
Why it works: It answers the question the reader was about to ask, in public, with the objection stated by someone else.
Pitfalls: Inventing the comment; editing the commenter's words; a reply that turns into a pitch; using a real name without permission.
Template: screenshot

### Grid (starter pack, the range, an education grid)
When: Top and mid funnel. Four to nine small pictures with captions that together say "this is what we do" or "these are the options".
Structure: A 2x2 or 3x3 grid of frames, each with a photo and a short caption chip, a small headline above, an optional call to action.
Copy: "[Headline: the set]. [Caption per cell, two or three words]." Example: "This year's kitchens. Southville. Clifton. Bedminster. Bishopston."
Visual: The owner's photos, one per cell; without photos, the cells carry words only and the format is a listicle instead.
Why it works: Range and variety in one glance; the grid holds the eye longer than one picture.
Pitfalls: Cells that are all the same photo; more than nine; captions that are sentences; a grid used to hide that there is no single strong picture.
Template: grid

### Expert or endorsement (celebrity, authority)
When: Mid funnel, when a named person with standing has said something true about the business, with permission. Motion's highest spend-to-use ratio (2.1x), rarely available to a small business.
Structure: The quote large, the person's name and standing beneath it, their photo only with permission.
Copy: ""[The quote, verbatim]." [Name], [what makes them worth listening to]." Example: ""The only fitters I recommend." Jane Doe, building surveyor, Bristol."
Visual: The `quote` template; a photo of the person only with written permission.
Why it works: Borrowed standing; the reader trusts the endorser's judgement more than the advertiser's claim.
Pitfalls: An endorsement that was paid and does not say so (FTC and ASA rules); a quote taken from a review and presented as an endorsement; a face without permission.
Template: quote

### Benefit stack (value proposition, specs)
When: Mid and bottom funnel. Three to six ticked benefits, or the specs, under a headline.
Structure: A headline, then ticked lines, then the call to action.
Copy: "[Headline: the offer]. ✓ [benefit] ✓ [benefit] ✓ [benefit]." Example: "A kitchen from the workshop. ✓ Measured by the maker. ✓ Built in birch ply. ✓ Fitted in three days."
Visual: None; or a product photo beside the list on a 1.91:1.
Why it works: A warm reader wants the list; it is the comparison they were going to make.
Pitfalls: Features with no benefit; more than six; adjectives in the list; a benefit that is not in the ledger.
Template: checklist

### Urgency (countdown, seasonal, event)
When: Bottom funnel, with a real date: a season's last slots, an event, a price rise.
Structure: The date or the count as the biggest thing, what happens on it, the call to action.
Copy: "[What ends and when]. [What to do before then]." Example: "Six fitting slots left before Christmas. Book a visit this week."
Visual: The banner ground; no scene.
Why it works: A true deadline resolves a decision the reader was postponing.
Pitfalls: A deadline that moves; a countdown to nothing; urgency words stacked ("hurry, last chance, now"); using it more than once a quarter.
Template: banner

### App or interface mockup (in-app proof shot)
When: Mid funnel, for anything with a screen or a result that shows on one: a quote, a booking, a dashboard, a delivery notice.
Structure: A phone-shaped card with a title and a few rows (label and value), one highlighted line, the business name small.
Copy: "[Screen title]. [Row: label, value] x3. [The line that matters, in the accent]." Example: "Your drawing. Measured: Tuesday. Drawn: Friday. Price: on the drawing. Fitting: 3 days."
Visual: The `screenshot` template's app variant; a real screenshot of the real product beats it when one exists. Never an interface painted by an image model.
Why it works: A screen reads as evidence, not as a claim.
Pitfalls: A mocked-up screen for a product that has no screen; numbers not in the ledger; a fake brand's interface.
Template: screenshot

### Editorial (magazine style)
When: Top funnel for a considered purchase; a still image with a magazine's restraint.
Structure: A photograph with a lot of empty space, a small headline in the margin or a thin band, the business name as a small label.
Copy: "[A short line, under eight words, that reads like a caption]." Example: "Made on Cumberland Road."
Visual: The owner's best photograph, or the `photo` guide with the copy-space set to a wide margin; the template's band kept thin.
Why it works: It reads as content in a feed of ads.
Pitfalls: Restraint that becomes a picture with no message; a stock image; a logo bigger than the words.
Template: photo

### Flat lay
When: Mid funnel, for a product with parts, a kit, a bundle, or a menu of options.
Structure: The items arranged on a plain ground from directly above, evenly spaced, one label line.
Copy: "[What is in it, as a count or a name]." Example: "Everything in the fitting kit."
Visual: The owner's product photo from above (the `product` guide with the camera directly above); the brand's colour as the ground.
Why it works: Everything at once, in order; the reader takes inventory.
Pitfalls: Items too small to read; a busy ground; props that are not for sale.
Template: product

### Text in context (a sign, a billboard, a mug)
When: Top funnel. The headline appears on a real object in the scene: a sign, a van, a wall, a board. Motion: unconventional text placement punches about 1.5x above its use.
Structure: A photograph in which the words are part of the world, set by the template over a flat surface in the picture.
Copy: "[The claim, six words or fewer]." Example: "Kitchens fitted by their makers."
Visual: The `photo` guide with the copy-space named as a flat surface in the scene (a painted board, a van side, a plain wall) and the words placed there by the template.
Why it works: The eye reads a sign in a scene before it reads a headline on a card.
Pitfalls: Asking the image model to paint the words (it misspells them); a surface that is not flat; text that competes with the object.
Template: photo

### Objection-led (skeptic to customer)
When: Mid funnel. The reader's doubt, said first, then the answer.
Structure: The objection as the headline, the answer as the body, the call to action; or two columns, the doubt and the fact.
Copy: ""[The objection, as the reader would say it]." [The answer, one claim from the ledger]." Example: ""A workshop kitchen costs more." It costs what a showroom's does, and the same two people fit it."
Visual: None; the `statement` or the `us-vs-them` template.
Why it works: Naming the doubt earns the right to answer it.
Pitfalls: Straw objections; an answer that is a slogan; an objection about a competitor by name.
Template: us-vs-them

### Illustration (cartoon, comic strip)
When: Top funnel, when the brand's identity is drawn rather than photographed, or the idea is abstract.
Structure: A drawn scene or a two-panel strip with the words in the template's band, not in speech bubbles the model draws.
Copy: "[The idea in one line]." Example: "Two people, one kitchen, start to finish."
Visual: The `illustration` prompt guide; the brand's Imagery block must say the brand is drawn, otherwise this format is off-brand.
Why it works: A drawing reads as a point of view; it cannot be mistaken for stock.
Pitfalls: A cartoon style the brand does not own; text drawn by the model; cuteness.
Template: photo

### Case study (results)
When: Bottom funnel, business-to-business or a considered purchase. Two or three numbers with what they measure and the source.
Structure: A headline naming the job, then two or three big numbers each with a label, the source small, the call to action.
Copy: "[Headline: the job]. [Number] [what it measures] x3. [Source]." Example: "The Clifton kitchen. 3 days to fit. 0 return visits. 1 drawing."
Visual: None; the numbers are the picture.
Why it works: Specific numbers about one job are harder to disbelieve than a claim about all jobs.
Pitfalls: Numbers not in the ledger; a result most customers will not get without saying what is typical; a client named without permission.
Template: stats

### Giveaway or contest
When: Top funnel, for reach and list building, with the platform's rules followed.
Structure: The prize as the biggest thing, how to enter in one line, the closing date, the terms line.
Copy: "Win [the prize]. [How to enter]. Closes [date]." Example: "Win a drawing of your kitchen. Book a visit before 30 October. Closes 31 October."
Visual: The banner ground or a photo of the prize.
Why it works: A prize is an offer with no price.
Pitfalls: "Tag a friend" and "share to enter" mechanics Meta demotes as engagement bait; no terms; a prize unrelated to the business.
Template: banner

### Badge or certification
When: Mid funnel, when the business holds a real accreditation, award or guarantee.
Structure: The badge's claim as a headline, the issuer as a label, one line of what it means for the reader.
Copy: "[The accreditation]. [Issuer]. [What it means for you]." Example: "Guild of Master Craftsmen. Since 2019. Every kitchen inspected before you pay."
Visual: The real badge file from the owner as the mark; never a badge drawn by a model.
Why it works: Third-party standing in one glance.
Pitfalls: A badge the business does not hold; a drawn badge; an award with no issuer.
Template: statement

## Copy rules for any static

1. **Twelve words or fewer on the image.** The rest goes in the primary text. Reviews and letters are the exception; keep them under 80 words and set them at reading size.
2. **Hook first.** The first line on the image is the reason to stop, never the business name. The name goes small or in the profile.
3. **Verb-first call to action.** "Book a survey", "See the kitchens", "Get the checklist". Not "Learn more", "Click here" or "Get started".
4. **No hashtags** on the image or in ad copy; they are an exit from the ad.
5. **No "It's not X, it's Y"** or "not just X but Y". It is the strongest single tell of generated copy.
6. **No tricolons.** No "No fuss. No filler. No delay." At most one list of three per ad, and only when the list really has three things.
7. **No invented proof.** No numbers, names, reviews, awards, press or prices that are not in the claims ledger. An empty proof slot is fine; a fake one is not.
8. **The claims ledger.** Every fact on an ad (a number, a quote, a lead time, a price, a material) is written in `campaigns/<slug>/claims.md` with its source and date before the ad is generated. The reviewer checks the ad against the ledger, not the other way round. If a claim is unusual (a result most customers will not get), the ad says what is typical.
9. **Specific over adjective.** "18 mm birch ply" not "quality materials". "Eight weeks" not "fast". If a sentence has no noun, number, place or date from the brief, rewrite it or cut it.
10. **Plain words.** No bespoke, seamless, elevate, unlock, journey, solutions, passionate, world-class, next level. The brand's own never-list in `brand/voice.md` applies on top.
11. **Policy on every draft.** Personal attributes (Meta): describe the product or the situation, never the reader. Before/after: not for health, weight or skincare. Competitors: a category, never a name. Endorsements: real, unedited, disclosed if paid.
12. **Landing page matches the hook.** The page the ad sends to must say the same thing in the same words, or the click is wasted.
