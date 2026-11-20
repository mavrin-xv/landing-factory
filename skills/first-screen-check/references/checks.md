# First-screen checks

Most paid social and search traffic lands on a phone. What fits in a 390x664 CSS pixel window (an
iPhone-class screen minus the browser bars) decides whether the visitor scrolls. These checks look
only at that window, plus trust faults anywhere on the page.

## The seven checks

| # | Check | Pass | Why it matters |
|---|---|---|---|
| 1 | promise | the phrase from the ad or post is visible | a visitor who does not see what they clicked on assumes they landed on the wrong page |
| 2 | headline | exactly one H1, fully visible | an H1 cut by the fold reads as half a sentence |
| 3 | cta | a button or CTA-styled link is visible | a visitor who has to scroll to find the action often does not |
| 4 | proof | JUDGE: the script lists candidates (ratings, review counts, logo names), a person decides | a claim with nothing next to it reads as an ad |
| 5 | covered | no fixed or sticky element covers more than 25% | a cookie bar plus a chat bubble can hide the CTA on a small phone |
| 6 | hero-bytes | the largest image in view is under 1 MB | a heavy hero is the usual cause of a slow Largest Contentful Paint on mobile |
| 7 | viewport | `<meta name="viewport">` present | without it the phone renders a shrunken desktop page |

Proof is a JUDGE check on purpose. A script can find "4.7 of 5"; it cannot tell a real rating from a
made-up one, or a logo row the owner may show from one they may not.

## Trust faults (whole page)

| Fault | Example |
|---|---|
| lorem | "Lorem ipsum" left in a block nobody reviewed |
| todo | TODO, TBD, FIXME in visible text |
| template text | "your headline here", "this template" |
| placeholder price | $0, 9,999, 0.00, XX |
| hidden rating | aggregateRating in JSON-LD with no reviews visible on the page |
| staging host | links to localhost, *.webflow.io, *.vercel.app, *.netlify.app, *.pages.dev |

Any fault fails the run. They are the details a buyer notices and a team stops seeing.

## Ranking

The fix list puts one item first: CTA and covered (the visitor cannot act), then promise, proof,
headline, hero-bytes, viewport, then the trust faults. Fix the first item, run again.

## Proof versus the hero canon

The design canon bans a strip of trust badges in the hero. The proof check wants proof on the first
screen. Both hold when the proof is one sourced line inside the sub ("Rated 4.7 of 5 in 1,240
reviews"), or when the logo row directly under a compact hero is visible at 390x664. The Northwind
example shows both rounds: `examples/northwind-roasters/out/first_screen-round1.txt` (proof JUDGE with
no candidates) and `examples/northwind-roasters/out/first_screen.txt` (one candidate, inside the sub).

## Static mode

`--static` reads the HTML without a browser and treats the first 80 visible words as the first screen.
It cannot check covered or hero-bytes. Use it when Playwright is not installed; when the two modes
disagree, the screenshot is right.
