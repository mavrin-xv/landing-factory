# Copy canon

How to write the words of a one-offer landing page. The examples use Northwind Roasters, an invented
coffee subscription.

## 1. Value logic: four blocks

A buyer weighs four things. Each becomes a visible part of the page.

| Lever | The question | Where it shows | Northwind example |
|---|---|---|---|
| Dream outcome | what do I have at the end | H1 and the segments | fresh coffee at the door without remembering to buy it |
| Likelihood | will it work for me | the mechanism, the proof wall | the roast date printed on the bag; ratings |
| Time | how fast | the sub, the mechanism | ships within 48 hours of roasting |
| Effort | what do I have to do | the mechanism, the FAQ | pick a profile once; skip online |

Raise the first two, lower the last two. If a block does none of the four, it is a candidate for the
deletion test.

## 2. Skeptic order

Answer the questions in the order a stranger asks them: what is this, is it for me, does it work,
what is the catch, what now. The default skeleton (`../landing-factory/references/skeleton.md`)
follows this order.

## 3. The hero

- **H1:** what the buyer gets, in their words. 12 words or fewer. Not the brand name, not a slogan.
- **Sub:** the outcome and the cost in 20 words or fewer. "Every two or four weeks, $16 a bag with
  shipping."
- **CTA:** the action and what it starts. "Start my first bag", not "Submit" or "Get started".
- **Promise match:** the first screen repeats the words of the ad or post the visitor clicked.
  `copy_lint.py --promise` checks the first 80 words.

## 4. Proof

- True only. Every number, rating, count and quote is in `facts.md` with a source.
  `copy_lint.py --facts` fails a number that is not.
- Big numbers or none. A small count reads as small.
- Shown once. The same number in three blocks reads as padding.
- Next to the claim it proves.
- Example quotes in a demo are labelled as examples.

## 5. Offer

- A value stack: every component with what it does for the buyer.
- One honest price anchor: a real alternative the buyer knows, with a source. Not an invented
  "was $99".
- One plan, or one plan pushed. Every extra option is a decision that can stall the click.
- No fake scarcity: no countdowns, no "only 3 left" unless it is true and visible in the product.
- No income or result promises: no "guaranteed results", no "make $N a day", no "passive income".
- The refund rule and "all sales final" live in the FAQ.

## 6. Segments

Name two to four buyer types and the result for each. A visitor who does not see themselves will not
read further. "Espresso at home", "one filter cup a morning", "a small office".

## 7. Words

- Plain words for a cold audience. If the category has jargon, the hero has none of it.
- Short sentences. One idea each.
- No hype words (unlock, seamless, revolutionary, game changer, next-gen, elevate, world-class).
- No em or en dashes.
- Specific beats general: "roasted within 48 hours of shipping" beats "always fresh".

## 8. The heading skeleton

Read H1 to H3 alone, top to bottom. It must explain the offer without the paragraphs. `copy_lint.py`
prints it at the top of its output.

## 9. Friction audit

Count, for the path from landing to paid: fields, steps, decisions, exits. Write the counts in
`architecture.md`. Every item needs a reason to exist.
