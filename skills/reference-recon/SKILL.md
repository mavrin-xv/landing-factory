---
name: reference-recon
description: Reverses a reference landing page into what a build needs. It takes full-page and first-screen screenshots at 1440 and 390, extracts design tokens and the copy of every section, and writes a reference map where each block gets a job, a visual and a keep, change or drop decision. Use when the user sends a page to copy or learn from, says "make it like this site", "clone this landing", "what does this page do well", or before any landing page build that starts from a reference.
---

# Reference recon

See what the reference does before deciding what to take. Most "make it like this" briefs are about
the order of answers and the first screen, not the colors; recon makes that visible and writes it down.

## Inputs

- The reference: a URL, a saved `.html` file, or a folder with the page and its assets.
- What the owner likes about it (the first screen, one section, the pacing, the motion).
- The mode, if already known: reskin (default) or replica. Guide: `references/reskin-vs-replica.md`.

## Steps

1. **Run recon.** `python3 scripts/recon.py <url|file|folder> <out> --name ref`. It saves
   `ref-1440.png`, `ref-390.png`, `ref-first-screen.png` (390x664), slices, and `ref-recon.json` with
   tokens, sections, the first-screen text and CTAs. A local file is served on 127.0.0.1, so it works
   offline. Without Playwright installed, the script prints the install line and stops.
2. **Read every slice.** Start with the first screen at 390. The JSON tells you what the page says;
   the slices tell you how it says it.
3. **Write the reference map.** `python3 scripts/ref_map.py <out>/ref-recon.json --out reference-map.md`
   gives one row per block with a guessed job. Fill in the visual it carries, our block, keep, change
   or drop, and why. Template: `templates/reference-map.md`.
4. **Decide the mode** and write it at the top of the map. On a reskin, list what must not be copied:
   logos, photos, illustrations, text, trademarks.
5. **List the assets** each of our blocks needs and where each comes from, using the ladder in
   `references/asset-ladder.md`. Every placeholder goes in a list for the owner.
6. **Hand over** the map, the first-screen shot and the asset list to the architecture step
   (`templates/architecture.md`).

## Gates

- Every reference block appears in the map with a decision and a reason.
- Every block on our page points at a reference block or is marked NEW with a reason.
- The mode is written down; on a reskin, the "do not copy" list exists.
- No reference image, logo, illustration or text is in our asset list.

## Output

```
title: Contoso Beans: tea, delivered
h1: Loose-leaf tea that shows up before you run out
sections: 7
   1. section h637   H1: Loose-leaf tea that shows up before you run out    img 0 video 0 svg 0
   2. section h202   H2: Served at                                          img 0 video 0 svg 0
   3. section h248   H2: How it works                                       img 0 video 0 svg 0
   ...
first-screen CTAs (390x664): ['Start for $12']
```

Then `reference-map.md`. Example run on an invented reference: `examples/northwind-roasters/out/recon.txt`,
`examples/northwind-roasters/out/contoso-recon.json` and `examples/northwind-roasters/out/reference-map.md`.

## Failure modes

| Trap | What it looks like | Instead |
|---|---|---|
| Recon by memory | "the reference had a big hero, I remember" | run the script, read the slices |
| Desktop only | the 1440 shot read, the 390 shot skipped | the first screen at 390 is the one most visitors see |
| Copying the look on a reskin | the reference's palette on our page | take the order and the jobs; our tokens win |
| Skipped blocks | a reference section left out of the map comes back as feedback | `ref_map.py` lists every block; decide each one |
| Reference assets "for now" | their photo in our hero until ours arrives | a flagged placeholder, listed for the owner |
| Upscaled images | a 600px logo stretched to 1200px | native size or smaller; ask for a bigger file |
| Lazy content missed | sections that load on scroll are missing from the JSON | the script scrolls first; check the section count against the slices |
