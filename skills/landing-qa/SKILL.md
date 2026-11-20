---
name: landing-qa
description: Runs the checks a landing page build round needs before anyone sees it. It serves the page locally, takes full-page screenshots and readable slices at 1440 and 390, reports horizontal overflow, console errors, failed requests and blank images, and runs a wiring gate for broken anchors, missing files, the H1 count, required CTA counts, banned strings and CSS class collisions. Use when a build or revision round is done, when the user says "check the page", "QA the landing", "take screenshots", "is anything broken", or before sending a preview link.
---

# Landing QA

Catch the broken things before the owner does. Scripts find the wiring faults; the slices make a
person look at every part of the page at both widths.

## Inputs

- The site folder and the page file(s).
- `gates.json` for this round (start from `templates/gates.json`): required counts, banned strings,
  stylesheets, classes added this round.
- The facts file and the clicked promise, for the copy and first-screen checks.

## Steps

1. **Screenshots and runtime checks.**
   `python3 scripts/shot.py <site> index.html <out> --overflow`. It reports scrollWidth, console errors,
   failed requests and blank images per width, and saves full pages and slices.
2. **Wiring gate.** `python3 scripts/gates.py <site>/index.html gates.json`. Anchors, local files, one H1,
   viewport, counts (every CTA wired to the offer), banned strings, class collisions.
3. **Copy, design and first screen.** Run `../landing-copy/scripts/copy_lint.py`,
   `../landing-design/scripts/design_lint.py` and `../first-screen-check/scripts/first_screen.py`.
4. **Read every slice,** 390 first, with `references/qa-checklist.md` open.
5. **Fix and rerun** until all green. A fix that touches another block means the whole set runs again.
6. **Report** the outputs, the slices read, and the placeholders still owed.

## Gates

- `shot.py` exits 0 at both widths.
- `gates.py` exits 0.
- copy_lint, design_lint and first_screen green.
- Every slice read; the by-eye list in `references/qa-checklist.md` ticked.

## Output

```
index.html 1440px  scrollWidth 1440 OK  errors 0  blank images 0  PASS
index.html 390px  scrollWidth 390 OK  errors 0  blank images 0  PASS
index.html 1440px: 3 slices, read every one
index.html 390px: 2 slices, read every one
shot: all green
gates: all green (1 anchors, 2 local files, 2 counts, 4 zero rules)
```

Example outputs: `examples/northwind-roasters/out/shot.txt`, `examples/northwind-roasters/out/gates.txt`,
config `examples/northwind-roasters/gates.json`.

## Failure modes

| Trap | What it looks like | Instead |
|---|---|---|
| Green scripts, broken look | an empty grid cell nobody saw | read every slice at both widths |
| Overflow at 390 only | the page scrolls sideways on phones | `--overflow` lists the element; fix its width or min-width |
| CTA rewired by an edit | one button now points at `#plans`, which no longer exists | `counts` in `gates.json` pins every CTA |
| Class collision | a new block styled by an old stylesheet's rule | list new classes in `classes`; prefix per block |
| Blank lazy images | the full-page screenshot has a white hero | no lazy loading above the fold; the script scrolls but cannot fix it |
| Leftover strings | the reference's brand name in alt text | `zero` in `gates.json` lists it |
| Gates run on the wrong file | the build wrote `page-v3.html`, gates checked `index.html` | one path per round, the same in the build script and the gates |
