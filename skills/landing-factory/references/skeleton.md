# The default skeleton

A starting order for a one-offer landing page for cold traffic. It follows the questions a skeptical
visitor asks, in the order they ask them. Change it when the page job says so (see
`../cro-audit/references/page-jobs.md`), and write the reason in `architecture.md`.

| # | Block | The question it answers | Must carry |
|---|---|---|---|
| 1 | Header | Where am I | logo, one CTA with the page's one action, nothing else (64 to 80px, one line) |
| 2 | Hero | What is this, what does it cost, what do I do | H1 (2 lines at most on desktop), a sub of 20 words or fewer with the outcome and the cost, one CTA, a real product visual; one sourced proof line is allowed inside the sub |
| 3 | Proof row | Do people like me use it | logos or a rating, 2 columns on mobile, directly under the hero |
| 4 | Mechanism | How does it work | a numbered loop of 3 to 5 steps, each a verb and an object |
| 5 | Components | What exactly do I get | every component with what it does for the buyer; a bento sized to the content |
| 6 | Segments | Is it for me | 2 to 4 named buyer types, each with the result for that type |
| 7 | Proof wall | Does it work | quotes, numbers or cases, true and sourced; labelled if they are examples |
| 8 | Offer | What does it cost, what is the catch | value stack, one honest price anchor, one plan button |
| 9 | About | Who is behind it | a face or a fact, one short paragraph |
| 10 | FAQ | What about my objection | the real objections; refund and "all sales final" rules live here, not in the hero |
| 11 | Final CTA | What now | the H1 promise restated as a next step, the same CTA label |
| 12 | Footer | Legal | contacts, policies |

## Rules that come with it

- **One action.** Every CTA on the page has the same label and goes to the same place.
- **The heading skeleton sells alone.** Read H1 to H3 top to bottom with no paragraphs. If it does
  not explain the offer, the page will not either. `copy_lint.py` prints it.
- **Deletion test.** For each block, ask what the visitor loses if it disappears. Nothing means cut it.
- **Proof next to its claim.** A number about speed sits in the mechanism, not in a proof wall three
  screens later.
- **Every block has a visual.** A heading plus paragraphs is a block nobody reads.
  `design_lint.py` fails it.
- **Not in the hero:** a tagline under the CTA, a strip of badges or avatars, a pricing teaser, feature
  bullets. They push the CTA down and dilute the one message.
