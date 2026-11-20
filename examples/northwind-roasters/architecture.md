# Page architecture: Northwind Roasters subscription

## Page job
- Traffic and temperature: paid social, cold. Visitors have never heard of the roaster.
- The promise they clicked: "Fresh-roasted coffee at your door".
- The one action: start a subscription (button label "Start my first bag", repeated).
- Reference and mode: Contoso Beans tea page (the fixture in `reference/`), reskin. We keep its order of
  skeptic answers and its one-plan offer; the design tokens, copy and images are ours.

## Design read
Reading this as: a consumer subscription page for home coffee drinkers, with a warm editorial
language, leaning toward a serif display face, off-black ink on paper, one rust accent, no motion
beyond hover.

## Sections, in skeptic order

| # | Section | Job | Visual it carries | Reference block | Proof next to it |
|---|---|---|---|---|---|
| 1 | Hero | What is this, what does it cost, what do I do | product photo (placeholder for now) | hero | price and "4.7 of 5 in 1,240 reviews" in the sub (moved up in round 2) |
| 2 | Logo row | Do people like me drink it | logo row, 2 columns on mobile | "Served at" | cafes that pour it |
| 3 | How a bag gets to you | How does it work | numbered loop, 4 steps | "How it works" | roast date printed on the bag |
| 4 | What is in every box | What exactly do I get | bento of 4 tiles, one big | "What is in every box" | |
| 5 | Who it is for | Is it for me | 3 segment tiles, unequal widths | NEW: the reference has no segments | |
| 6 | Proof wall | Does it work | quote cards | "What drinkers say" | quotes labelled as examples |
| 7 | Offer | What does it cost, what is the catch | value stack table and price | "One plan" | cafe price anchor |
| 8 | About | Who is behind it | big year stat | NEW: cold traffic needs a face | founding year |
| 9 | FAQ | What about my objection | accordion | "Questions" | refund rule lives here |
| 10 | Final CTA | What now | small product image | NEW | |

## Heading skeleton
Fresh-roasted coffee at your door. How a bag gets to you. What is in every
box. Who it is for. What subscribers say. One plan, two speeds. Who roasts it. Questions. Your first
bag roasts on the next roast day.

## Friction budget
- Fields on this page: 0 (checkout is a separate page).
- Steps to pay: button, then checkout.
- Decisions: one (two or four weeks), made at checkout.
- Exits: none besides the CTA.

## Cut and why
- A discount code banner: the brief has no real promotion, so it would be fake urgency.
- A comparison table against supermarket brands: no sourced numbers for it.
- A second plan card: one plan with two speeds is one decision, two cards are two.

## Open questions for the owner
- A real product photo for the hero and the final CTA (placeholder is flagged in the asset report).
- Names and a photo of the two roasters for About.
