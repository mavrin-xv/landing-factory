# The asset ladder

Every visual slot on the page gets filled from the highest rung available. Never skip down a rung
without writing why, and never ship a rung-4 placeholder without listing it in the report.

| Rung | Source | Rule |
|---|---|---|
| 1 | The owner's real file: product photo, screenshot, video, logo | use at its native size or smaller; never upscale a low-resolution file, ask for a bigger one |
| 2 | A CSS or typographic treatment: a big number, a structured list, a table, a numbered loop | good for mechanisms, value stacks and stats; it is honest because it shows text, not a fake object |
| 3 | A tight crop of a real file the owner already has | a detail of a product photo can carry a section the full photo already carried |
| 4 | A flagged placeholder | a plain block that says PLACEHOLDER and what belongs there; listed in the report under "assets owed" |

## Never

- Stretch a small image to fill a hero. It looks blurry on every phone with a dense screen.
- Draw a fake product UI out of divs. Reviewers ask where that screen is in the real product.
- Use the reference's images, illustrations or logos, even "for now". Placeholders get shipped.
- Generate a photo of a product that does not look like the product.
- Hand-draw icons as inline SVG one by one. Use one icon font for the whole page so weights match.

## The report line

```
assets owed:
  hero        img/bag-placeholder.jpg   PLACEHOLDER: real product photo, 1200x800 or larger
  final CTA   img/bag-placeholder.jpg   PLACEHOLDER: same photo, any crop
```
