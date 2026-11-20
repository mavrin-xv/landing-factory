---
name: first-screen-check
description: Checks what a phone visitor sees before scrolling. It opens the page at 390x664, runs seven checks (promise match, headline, CTA, proof, overlays, hero image weight, viewport), scans the whole page for trust faults such as lorem ipsum, placeholder prices, staging links and hidden ratings, and returns a fix list with one item marked Fix first. Use when the user asks "check the first screen", "above the fold", "why do people bounce", "does the page match the ad", before sending paid traffic to a page, or after every landing page build round.
---

# First-screen check

Most paid traffic lands on a phone and decides in the first screen. This check looks only at that
window, plus the trust faults a buyer notices anywhere, and says which one thing to fix first.

## Inputs

- The page: a URL or a local `.html` file (served on 127.0.0.1 for the check).
- The promise the visitor clicked (ad headline, post line, email subject), word for word.
- Optional: where traffic comes from, to judge the proof candidates.

## Steps

1. **Run it.** `python3 scripts/first_screen.py index.html --promise "the clicked phrase" --out out`.
   It saves `first-screen.png` and prints the seven checks, the trust faults and the fix list.
   Without Playwright, add `--static` (no screenshot, no overlay or weight checks).
2. **Look at `first-screen.png`.** The script reads the DOM; the screenshot shows what a person sees.
3. **Judge the proof.** The script lists candidates. Decide if they are real, sourced and visible
   enough. No candidates on a cold page is a fix.
4. **Fix the Fix-first item**, run again, repeat until no FAIL and no trust fault.
5. **Write the result** into the round report, with the proof judgement.

Every check, why it matters, and how proof fits with the hero rules: `references/checks.md`.

## Gates

- No FAIL in the seven checks.
- Zero trust faults.
- Proof judged by a person, with a reason.
- `first-screen.png` looked at, not only the text output.

## Output

```
first screen (browser, 390x664): site/index.html
  1 promise     PASS  'fresh-roasted coffee at your door' is on the first screen
  2 headline    PASS  'Fresh-roasted coffee at your door' fully on the first screen
  3 cta         PASS  ['Start my first bag']
  4 proof       JUDGE candidates: ['1,240 reviews']
  5 covered     PASS  no overlay over 25%
  6 hero-bytes  PASS  img/bag-placeholder.jpg 21 KB
  7 viewport    PASS  present
trust faults: 0
fix list:
  nothing to fix on the first screen; judge the proof candidates by eye
```

Round 1 of the same page, before the fix: `examples/northwind-roasters/out/first_screen-round1.txt`.

## Failure modes

| Trap | What it looks like | Instead |
|---|---|---|
| Desktop review | the page "looks fine" on a laptop | 390x664 is the screen that decides |
| Ad mismatch | the ad says "first bag free", the page never does | the clicked words on the first screen |
| Script trusted on proof | "4.9 stars" passes because text was found | a person judges every candidate |
| Badge strip to satisfy proof | six badges and avatars crammed under the CTA | one sourced proof line in the sub, or the logo row right under a compact hero |
| Cookie bar hides the CTA | covered fails on small phones only | smaller bar, or bottom placement that leaves the CTA visible |
| Static mode trusted | `--static` passes, the screenshot shows the H1 cut | the screenshot wins |
| Staging links shipped | buttons point at a preview host | the trust-fault scan; fix every one |
