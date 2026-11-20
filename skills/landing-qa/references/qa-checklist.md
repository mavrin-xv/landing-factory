# QA checklist

Scripts catch wiring. Eyes catch what looks wrong. A round needs both.

## Scripted (all must be green)

| Script | Catches |
|---|---|
| `scripts/shot.py --overflow` | horizontal scroll at 390 or 1440, console errors, failed requests, HTTP 400+, images that did not load |
| `scripts/gates.py` | broken `#anchors`, missing local files, not exactly one H1, no viewport, required counts (every CTA wired), banned strings, class collisions between stylesheets |
| `../landing-copy/scripts/copy_lint.py` | dashes, hype, fake urgency, income promises, unsourced numbers, long hero sub, ad mismatch |
| `../landing-design/scripts/design_lint.py` | pure black, video without poster, lazy hero images, eyebrow overuse, text-only sections |
| `../first-screen-check/scripts/first_screen.py` | the 390x664 first screen: promise, headline, CTA, proof, overlays, hero weight, trust faults |

## By eye (read every slice, 390 first)

- [ ] The hero fits the first screen at 390: H1, sub, CTA, the top of the visual.
- [ ] Nothing overlaps, nothing is cut at the right edge, no orphan word on its own line in the H1.
- [ ] Every section has a visual and the visual says something about the section.
- [ ] Bento and grid cells are full. No empty slot on desktop.
- [ ] Logo rows are a grid, 2 columns at 390.
- [ ] Buttons are one line, same label, same color, enough contrast.
- [ ] Text on images is readable (AA contrast, 4.5:1 for body text).
- [ ] No two consecutive sections use the same layout.
- [ ] Placeholders are listed in the report.
- [ ] The desktop layout at 1440 is not the mobile layout stretched.

## After the owner looks

- [ ] Every point of the owner's feedback is a line in the round report, with what changed.
- [ ] The previous round's page is backed up.
- [ ] Preview link sent. Going live is the owner's call.
