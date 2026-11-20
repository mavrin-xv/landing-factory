---
name: landing-design
description: Designs and builds the HTML and CSS of a landing page that does not look generated. It commits to one written design read, sets tokens with one accent and an off-black ink, builds mobile first at 390, gives every section a visual, sizes grids to the content, and lints the result for the tells of a template page. Use when building or restyling a landing page, when the user says "make it look less AI", "it looks like a template", "design the sections", "fix the mobile layout", or after the copy for a landing page is written.
---

# Landing design

Build the page so it looks made for this offer. The canon lists the defaults that make a page read
as generated and what to do instead; the lint catches the ones a script can see.

## Inputs

- `architecture.md` with the page job, the sections and the visual each one carries.
- The copy (from landing-copy) and the facts file.
- Brand tokens, or the design read line if there are none.
- The reference map and first-screen shot from reference-recon.
- The assets, with placeholders marked.

## Steps

1. **Write the design read** in one line at the top of `architecture.md`: "Reading this as: <page kind>
   for <audience>, with a <feel> language, leaning toward <type, color roles, motion>". Ask the owner
   one question only if the brief points two ways. Canon: `references/design-canon.md`.
2. **Set the tokens** as CSS variables: off-black ink, paper, one accent, muted, line, radius, two font
   families at most. Start from `templates/page/css/site.css`.
3. **Build the 390 layout first.** Base CSS is mobile. Every section gets a visual: product image,
   numbered loop, table, tiles, stat, accordion.
4. **Add desktop at `min-width: 820px`.** Count the items in each grid before designing it; no empty
   cells. No layout family twice in a row.
5. **Media rules:** video `muted playsinline` with a `poster`; no `loading="lazy"` in the first two
   sections; images at native size or smaller; one icon font, no hand-drawn inline SVG icons.
6. **Lint.** `python3 scripts/design_lint.py index.html`. FAILs block; WARNs get a look and a reason.
7. **Screenshot and read** with landing-qa's `shot.py`. Fix what the eye finds (an empty bento cell,
   a wrapped button), then lint again.

## Gates

- `design_lint.py` green.
- The hero fits 390x664: H1, sub, CTA and the top of the visual.
- One accent color, two font families at most, no pure black.
- Every section has a visual; every grid is full at 1440.
- No horizontal scroll at 390 (`shot.py --overflow`).

## Output

```
design_lint: 11 sections, 1 stylesheet(s), 1 accent color(s), 0 eyebrow(s), 0 video(s)
design_lint: all green
```

A failing run names the block:

```
FAIL text-section: <section id=about> is a heading plus paragraphs with no visual
FAIL pure-black: #000 in the CSS, use an off-black token
WARN three-cards: repeat(3, 1fr) found, check it is not the generic three equal cards row
```

Example page and CSS: `examples/northwind-roasters/site/index.html`, `examples/northwind-roasters/site/css/site.css`.

## Failure modes

| Trap | What it looks like | Instead |
|---|---|---|
| The generated look | purple gradient, three equal cards, Inter on slate | a design read from the brief, sizes from the content |
| Fake product UI | a dashboard drawn with divs | a real screenshot or an honest diagram |
| Desktop first | a 1440 layout squeezed to 390 with max-width queries | base CSS at 390, desktop with min-width |
| Empty bento cell | five slots for four items | count the items, then design the grid |
| Eyebrow on every section | small uppercase labels above every heading | one per three sections at most |
| Text-only section | heading plus two paragraphs | give it a loop, a table, a stat or an image |
| Second accent | two CTA colors compete | one accent for every CTA and key number |
| Blank hero in screenshots | lazy image or video without a poster | eager images above the fold, poster on every video |
