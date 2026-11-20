---
name: cro-audit
description: Audits a landing page for conversion against the job it has (cold sale, warm sale, waitlist, lead magnet, high-ticket, local service). A reviewer scores 12 weighted dimensions, a script totals them to 100 with a hard gate on the first screen, grades A to F, and orders the fixes by stage and points lost into quick wins, high-impact changes and test ideas. Use when the user asks "why doesn't this page convert", "CRO audit", "review my landing page", "what should we test", or before a page gets paid traffic.
---

# CRO audit

Find what stops a visitor from acting, in the order worth fixing. The score is a structured review,
not a prediction; its value is the fix order.

## Inputs

- The page (URL or file) and its screenshots at 390 and 1440 (landing-qa's `shot.py`).
- The page job and the traffic source. Table: `references/page-jobs.md`.
- The ad or post the visitor clicked.
- Any real numbers the owner has (conversion rate, bounce, scroll depth), with their source.

## Steps

1. **Set the page job.** Write it in a copy of `templates/cro-scores.json`. A page is judged against
   its job; a waitlist with no price is fine, a cold sale with no price is not.
2. **Run first-screen-check** first. Its result feeds headline, above_fold, cta and message_match.
3. **Score the 12 dimensions** 0 to 10 with the anchors in `references/rubric.md`. Write a note for every
   score under 8: the block, what is wrong.
4. **Total it.** `python3 scripts/cro_score.py cro-scores.json`. It applies the weights, the first-screen
   hard gate (under 60% of the first five dimensions is BLOCK), the grade, and the ordered fix list.
5. **Write the fixes** in three groups: quick wins, high impact, test ideas. Each names the
   dimension, the block, the exact change and, for copy, two alternative lines.
6. **Hand back** to the build loop (landing-factory) or to the owner as a TEARDOWN report.

## Gates

- The page job is set before any score.
- Every score under 8 has a note naming the block.
- Verdict not BLOCK and grade C or better before paid traffic.
- No outside conversion statistic in the report without its source next to it.

## Output

```
CRO audit: site/index.html (page job: cold subscription, paid social traffic)
  dimension      score  weight  points  note
  headline           8      18    14.4
  cta                8      15    12.0
  ...
  trust              6       5     3.0  no real product photo yet (placeholder), no named roasters in About
  first-screen gate: 53.8 of 67 (80%, needs 60%)
  total 78.3 of 100, grade B, verdict B
fix list (fix order stage, then points lost):
  1. [2 headline] headline: 3.6 points lost.
  ...
```

Full run: `examples/northwind-roasters/out/cro_score.txt` from `examples/northwind-roasters/cro-scores.json`.

## Failure modes

| Trap | What it looks like | Instead |
|---|---|---|
| Generic ideal | a waitlist marked down for "no pricing" | score against the page job |
| Polish first | button colors debated while the headline is a slogan | the fix order: job, headline, sections, proof, friction, polish |
| Borrowed statistics | "red buttons convert 21% better" | only numbers with a source, ideally the owner's own |
| Score as forecast | "grade B means 4% conversion" | the score orders fixes; tests measure conversion |
| Vague fixes | "improve trust" | the block, the exact change, two alternative lines |
| Good FAQ hides a bad hero | total 70, first screen weak | the hard gate blocks it |
| One reviewer's taste | a 3 where a colleague gives an 8 | two reviewers on the big five; talk when they differ by more than 2 |
