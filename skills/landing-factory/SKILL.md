---
name: landing-factory
description: Builds a converting landing page from a reference URL and a brief, in rounds. It reverses the reference, writes the page architecture, applies a design canon and a copy canon, builds mobile first, and runs the gates (copy lint, design lint, wiring, screenshots, first screen, copy score, CRO score) before every round is shown. Use when the user asks to "make a landing page like this one", "build a sales page", "clone this site for my product", "redo our landing", "fix the landing after feedback", or sends a reference URL with an offer.
---

# Landing factory

Turn "make it like this page, but for my product" into a page that passes the checks a buyer and a
reviewer would make, in rounds the owner can follow. This skill is the loop; the six other skills
do one step each.

## Inputs

- A reference URL (or a saved page), and what the owner likes about it.
- The offer: product, buyer, price, what is in the box, refund terms. `templates/brief-checklist.md`
  lists every line; a blank line is a question for the owner.
- The traffic: source, temperature, the promise they clicked.
- True facts the page may use, each with a source, in a facts file (`templates/facts.md`).
- Brand assets, or "none yet".

## Steps

1. **Pick the mode.** FULL BUILD, BUILD FROM COPY, TEARDOWN or REVISION ROUND. Table and rules:
   `references/build-rounds.md`.
2. **Fill the brief.** Copy `templates/brief-checklist.md` next to the project and fill it with the
   owner. Do not guess the price, the proof or the refund terms.
3. **Reverse the reference** with the reference-recon skill: screenshots, the first screen at 390x664,
   tokens, sections, and `reference-map.md`. Decide reskin or replica.
4. **Write the architecture** from `templates/architecture.md`: the page job, the design read line,
   one job per section in skeptic order (`references/skeleton.md`), the heading skeleton, the friction
   budget, what was cut and why. Show it to the owner before building if anything in it is a guess.
5. **Write the copy** with the landing-copy skill. Run `copy_lint.py` and score it with the copy gate.
6. **Build** with the landing-design skill: tokens first, 390 first, one visual per section. Start
   from `templates/page/index.html` and `templates/page/css/site.css`. Fill visuals from the asset
   ladder and list every placeholder.
7. **Run the gates** with the landing-qa skill (`shot.py`, `gates.py`) and the first-screen-check
   skill. Read every screenshot slice at 390, then 1440.
8. **Score** with the cro-audit skill. BLOCK or D/F means another round before the owner sees it.
9. **Show the round:** preview link, the 390 screenshots, the gate outputs, the assets owed, and the
   open questions. Never deploy live.
10. **Next round:** back up to `page-vN.html`, re-read the reference first screen, map each feedback
    point, edit, run the gates again, report point by point. Rules: `references/build-rounds.md`.

Read `references/lessons.md` before round 1. Each line cost a real round.

## Gates

A round is shown to the owner only when all of these hold:

- `copy_lint.py` green, with `--facts` and `--promise`.
- `design_lint.py` green.
- `gates.py` green with the round's `gates.json`.
- `shot.py --overflow` green at 1440 and 390, and every slice read.
- `first_screen.py`: no FAIL, no trust fault, proof judged.
- Copy gate PASS (or a third failed pass escalated to the owner as an offer problem).
- CRO verdict not BLOCK, grade C or better.
- The previous round is backed up and every placeholder is listed.

## Output

```
round 2: examples/northwind-roasters/site/index.html
  copy_lint     all green (448 words, 4 CTAs, 1 label)
  design_lint   all green (11 sections, 1 accent)
  gates         all green
  shot          1440 OK, 390 OK, 0 errors, 0 blank images
  first screen  7 checks pass, proof candidate "1,240 reviews" (inside the sub)
  copy gate     PASS 56/70 (pass 2)
  CRO           78.3/100, grade B, first-screen gate 80%
assets owed:    hero photo, final CTA photo (placeholders)
feedback map:   1. "proof is missing up top" -> rating moved into the hero sub
open questions: names and photo of the roasters for About
```

The full worked example, with every input and every script output, is `examples/northwind-roasters/`.

## Failure modes

| Trap | What it looks like | Instead |
|---|---|---|
| Building before the brief | a pretty page with a guessed price and invented proof | fill the brief; blanks go to the owner |
| Replica by accident | the reference's colors and photos on our product | decide reskin or replica in recon; reskin is the default |
| Drift across rounds | round 5 no longer resembles the reference the owner liked | re-read the reference first screen at the start of every round |
| Gates green, page wrong | scripts pass, the bento has an empty cell | read every slice at 390 and 1440 |
| Silent no-op edit | the fix "applied", nothing changed | a build script whose replace fails when the old text is missing |
| Overwritten favourite | the owner asks for round 2's hero back, it is gone | back up every round before editing |
| Live by accident | a preview command pointed at production | preview only; going live is the owner's call |
| Endless line edits | copy fails the gate three times | stop and revisit the offer and the page job |
