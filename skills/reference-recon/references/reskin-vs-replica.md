# Reskin or replica

Decide this before the first line of HTML. It changes what you take from the reference and what you
must leave behind.

| | Reskin (the default) | Replica |
|---|---|---|
| When | the owner likes another site's page and wants the same effect for their own offer | the owner owns the reference (their old site, a page they paid for) and wants it rebuilt |
| Take | section order, pacing, the job each block does, the first-screen composition, the density | layout, spacing, type scale, motion, everything visible |
| Do not take | colors, fonts, logos, photos, illustrations, text, trademarks | anything owned by a third party (stock under the old license, embedded fonts without a license) |
| Design system | ours wins on every conflict | the reference's tokens, measured by recon |
| Copy | written from our brief and facts | the owner's own copy |
| Check | someone who knows the reference should not mistake our page for it | a side-by-side at 390 and 1440 looks the same |

## Why reskin is the default

Copying another company's look makes the page read as a knock-off to anyone who has seen the original,
and copies text and images that you have no right to use. What converts on the reference is almost
never its color: it is the order of answers, the first screen and the proof placement. Those transfer.

## What recon measures for each mode

- Both: section list with heights, headings, media counts; the first screen at 390x664 with its text and
  CTAs; full-page screenshots at 390 and 1440.
- Reskin: the job of each block (`ref_map.py`), the first-screen composition, the density (sections per
  1000px), where proof sits relative to claims.
- Replica: also the tokens (fonts, colors, radii, backgrounds) from `<name>-recon.json`, which become
  the CSS variables.
