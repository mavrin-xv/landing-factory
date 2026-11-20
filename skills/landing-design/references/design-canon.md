# Design canon

Rules for a landing page that does not look generated. Parts of sections 1, 3 and 6 are adapted from
taste-skill by Leonxlnx (https://github.com/Leonxlnx/taste-skill, MIT; license text in
THIRD_PARTY_NOTICES.md at the repo root). The rest comes from build rounds on real projects.

## 1. Read the brief, then commit

Before any CSS, write one line in `architecture.md`:

> Reading this as: <page kind> for <audience>, with a <feel> language, leaning toward <type pairing,
> color roles, motion level>.

Ask the owner one question only when the brief points two ways that lead to different pages (luxury
or friendly, dense or calm). Otherwise commit to the read and build.

## 2. Tokens

- **Ink is never pure black.** Use an off-black (#1f1a17, #14181c). Pure #000 on white is harsh and
  reads as a default. `design_lint.py` fails it.
- **One accent color**, used for the CTA, key numbers and the mechanism. A second saturated color
  makes two things compete for the click.
- **Two font families at most.** A display face for headings, a text face for the rest. One icon font.
- **Radius, spacing and shadow come from a short scale**, set once as CSS variables.
- **Contrast meets WCAG AA:** 4.5:1 for body text, 3:1 for large text.

## 3. Anti-defaults (the tells of a generated page)

| Default | Instead |
|---|---|
| Purple-to-blue gradient hero | a color that comes from the product or the brand |
| Three equal cards in a row | sizes that follow the content: one big and two small, a list, a table |
| Inter on slate-gray everything | a display face with character for headings |
| Neon glow, glassmorphism on everything | flat surfaces, one shadow level |
| Hand-drawn inline SVG icons | one icon font, one weight |
| A fake dashboard built from divs | a real screenshot, or an honest diagram |
| "Acme", "John Doe", 99.99% uptime, 10,000+ users | real names and real numbers from the facts file, or none |
| Section numbers as eyebrows (01, 02, 03) | the heading alone |
| The middle dot as a separator everywhere | commas, line breaks |
| Em dashes in copy | commas, colons, periods |

## 4. The hero

- Fits the first viewport at 390x664 and at 1440x900.
- H1 at most two lines on desktop, short enough to stay at four or fewer on a phone.
- Sub of 20 words or fewer: the outcome and the cost.
- Four text elements at most: H1, sub, CTA, and one proof line if there is a sourced one.
- A real product visual. Not an abstract blob.
- Not in the hero: a tagline under the CTA, a strip of trust badges or avatars, a pricing teaser,
  feature bullets. The logo row goes directly under the hero.

## 5. Layout across the page

- **Navigation** on one line, 64 to 80px high, logo plus one CTA.
- **No layout family twice in a row.** A bento, then a loop, then a list, then a wall.
- **At most two zigzag (image left, image right) sections in a row.**
- **Eyebrows (small labels above headings): one per three sections at most.** More reads as a
  template. `design_lint.py` counts them.
- **No split headers** (heading on the left, paragraph on the right) on more than one section.
- **Bento cells match the content.** Count the items, then design the grid. No empty cells.
- **Every section declares its mobile collapse.** Write it in the CSS comment or the architecture:
  "4 columns become a 1-column list at 390".
- **Every section carries a visual:** an image, a numbered loop, a table, a stat, a grid of tiles, an
  accordion. A heading plus paragraphs fails `design_lint.py`.

## 6. Mobile first

- Base CSS is the 390 layout. Desktop is added with `@media (min-width: 820px)`.
- Logo rows: a structured grid, two columns at 390.
- Buttons: `white-space: nowrap`.
- No horizontal scroll at 390. `shot.py --overflow` lists the element that causes it.

## 7. Media

- Video: `muted playsinline autoplay loop` plus a `poster` that shows a real frame.
- No `loading="lazy"` on anything in the first two sections.
- The largest image in the first screen under 1 MB; `first_screen.py` measures it.
- Images at their native size or smaller. Never upscale.
