# Lessons from real build rounds

Each line below cost at least one revision round on a real project. Names, products and numbers are
removed; the rule stays. Read this before round 1 and again when a round goes sideways.

## Reference and structure

1. **Re-read the reference first screen every round.** After four rounds of small fixes the hero had
   drifted into a different page. The owner's note was "it looked like the reference on day one".
2. **Map every reference block.** A block skipped in recon came back as feedback two rounds later.
   `ref_map.py` lists every block; each gets keep, change or drop with a reason.
3. **Reskin, not replica.** The owner wanted the structure and pacing of the reference, not its
   look. Copying its colors made the page read as a knock-off. Decide the mode before building.
4. **The mechanism is a numbered loop.** A paragraph explaining "how it works" was skipped by every
   reader. Four numbered steps with a verb each were read.

## Copy

5. **Sell the buyer's result, not the seller's process.** A hero about the team's method lost to a
   hero about what the buyer has at the end of week one.
6. **Cold traffic needs plain words.** Insider terms in the hero (the category's jargon) were the
   first thing the owner cut. If a stranger cannot repeat the offer after five seconds, rewrite.
7. **The sub carries the outcome and the cost.** Visitors who did not see a price in the first screen
   assumed it was high.
8. **Big true numbers only, once.** Small numbers (a count of 15 of something) read as small. Showing
   the same number in three blocks read as padding. Invented numbers are never an option.
9. **The refund rule goes in the FAQ.** "All sales final" in the hero cut clicks on a test; in the FAQ
   it answered the people who looked for it.

## Visuals

10. **Every section carries a visual.** Text-only blocks were the ones the owner called "empty".
11. **UI mocks must match the real product.** A made-up dashboard drew the question "where is this
    screen?" from the first reviewer. Use real screenshots, or a clearly abstract diagram.
12. **One accent color.** A second accent made two CTAs compete.
13. **Bento cells match the content.** Five slots for four items left an empty cell that looked like a
    bug on desktop.
14. **Logo rows are a structured grid**, two columns on mobile. A free-flowing wrap of logos looked
    broken at 390.
15. **Video: muted, playsinline, a poster.** Without a poster the hero was a black box on mobile until
    the video loaded.

## Build

16. **Mobile first at 390, desktop added at 820.** A page built at 1440 and squeezed down needed a full
    round of mobile fixes.
17. **No lazy loading above the fold.** Lazy hero images were blank in every full-page screenshot and
    on slow connections.
18. **CTA labels do not wrap.** `white-space: nowrap` on buttons; a two-line button reads as two buttons.
19. **Back up every round.** One round that overwrote the previous page cost the owner's favourite
    version of a section.
20. **Edit through a script that fails loudly.** A search-and-replace that matched nothing shipped a
    round with the fix missing and every gate green.
21. **Preview links only.** Going live is the owner's decision, after reading the screenshots.
