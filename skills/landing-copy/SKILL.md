---
name: landing-copy
description: Writes and checks the words of a one-offer landing page. It turns the offer into a hero with the outcome and the cost, a mechanism, segments, proof and an honest offer block in skeptic order, then lints the copy for dashes, hype, fake urgency, income promises and numbers missing from the facts file, and scores it on a 7-dimension gate. Use when writing or rewriting landing page copy, when the user says "write the copy", "the hero is weak", "nobody understands what we sell", "check this copy", or pastes copy from a copywriter for a page.
---

# Landing copy

Write the page so a stranger understands the offer in five seconds and believes it by the offer
block. Every claim comes from the facts file; nothing is invented to fill a block.

## Inputs

- The brief and `architecture.md` (page job, sections, heading skeleton).
- The facts file: every number, rating, count and quote with its source (`templates/facts.md`).
- The promise the visitor clicked (ad headline or post line), word for word.
- Existing copy, if this is a rewrite or BUILD FROM COPY.

## Steps

1. **Map the value logic.** Dream outcome, likelihood, time, effort: write where each shows on the page.
   Canon: `references/copy-canon.md`.
2. **Write the heading skeleton first.** H1 to H3 only, in skeptic order. Read it alone; it must sell.
3. **Write the hero.** H1 with the buyer's result in 12 words or fewer; a sub with the outcome and the
   cost in 20 words or fewer; a CTA named by what it starts; the clicked promise in the first screen.
4. **Write the blocks** in the order of the architecture. Proof sits next to its claim. The offer has a
   value stack, one honest anchor and one plan. The refund rule goes in the FAQ.
5. **Lint.** `python3 scripts/copy_lint.py index.html --facts facts.md --promise "the clicked phrase"`.
   Every FAIL is fixed or the number goes into the facts file with a source.
6. **Score.** A reader who did not write it scores the seven dimensions in a copy of
   `templates/copy-scores.json`, using the anchors in `references/copy-gate.md`. Then
   `python3 scripts/copy_score.py copy-scores.json`.
7. **Rewrite the lowest dimension** and score again with pass +1. After a third failed pass, stop
   editing lines and take the offer and the page job back to the owner.

## Gates

- `copy_lint.py` green with `--facts` and `--promise`.
- Copy gate PASS: every dimension 7 or more, total 56 of 70 (48 of 60 with no proof yet).
- One CTA label across the page.
- No number, rating or quote without a source in the facts file.
- No income or result promise, no fake scarcity.

## Output

```
heading skeleton (read it alone, does it sell?):
  H1 Fresh-roasted coffee at your door
    H2 How a bag gets to you
    H2 What is in every box
    H2 Who it is for
    ...
words: 439  CTAs: 4 (1 distinct)
copy_lint: all green
```

```
copy gate for site/index.html, pass 2
  desire         7  ok   pass 1 was 6: the hero sold logistics only
  total 56 of 70 (bar 56)
copy gate: PASS
```

Full outputs: `examples/northwind-roasters/out/copy_lint.txt`, `examples/northwind-roasters/out/copy_score.txt`.

## Failure modes

| Trap | What it looks like | Instead |
|---|---|---|
| Seller's process in the hero | "Roasted Monday and Thursday in small batches" | the buyer's result: "Fresh-roasted coffee at your door" |
| Price hidden | the cost appears only in the offer block | the sub carries the cost |
| Invented proof | "Loved by 10,000 coffee lovers" with no source | numbers from the facts file only, or none |
| Fake urgency | a countdown that resets on reload | a real reason (the next roast day), stated once |
| Income promise | "make $500 a week" on a course page | describe what the buyer learns and does |
| Jargon for cold traffic | category insider terms in the H1 | words a stranger would use |
| Many CTA labels | "Buy", "Start", "Try it", "Join" | one label, repeated |
| Writer scores own copy | every dimension 9 | a fresh reader with only the page and the anchors |
