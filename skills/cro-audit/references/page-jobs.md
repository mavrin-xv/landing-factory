# Page jobs

Score a page against the job it has, not against a generic ideal. A waitlist page with no price is
fine; a cold sales page with no price is not. Write the job at the top of `cro-scores.json`.

| Job | Visitor | What the first screen must do | What the page must have | Common mistake |
|---|---|---|---|---|
| cold sale | never heard of you, from an ad or post | promise match, outcome, cost, one CTA | mechanism, proof, segments, offer, FAQ | assuming the visitor knows the brand |
| warm sale | read your posts or emails | the offer and the price | the offer, proof, objections | re-explaining what they already know, burying the price |
| waitlist | curious, the product is not out | what it will be and when | one field, what they get for joining | asking for five fields |
| lead magnet | wants the free thing | what the free thing is and what it solves | a preview of it, one field | selling the paid product before they have the free one |
| high-ticket | considering a large purchase | who it is for and the result | cases, the process, the person, a call booking | a buy button for something that needs a conversation |
| local service | nearby, needs it soon | the service, the area, the phone number | hours, reviews, a map, prices or ranges | hiding the phone number below the fold |

## Traffic source changes the hero

- **Paid social:** the visitor was interrupted. The hero must repeat the ad's words and image.
- **Search:** the visitor typed a query. The H1 must answer that query.
- **Email:** the visitor clicked a specific promise. The first screen continues that sentence.
- **Direct or referral:** the visitor knows the name. The offer can come faster.

## Fix order

When a page has many problems, fix them in this order, because a later fix is wasted if an earlier
one is wrong:

1. Page job (the wrong job makes every other score meaningless)
2. Headline and message match
3. Section choice (which blocks exist, in which order)
4. Proof placement
5. Friction (fields, steps, decisions, exits)
6. Polish (copy lines, spacing, speed)

`scripts/cro_score.py` sorts its fix list by these stages, then by points lost.
