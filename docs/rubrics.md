# Rubrics

Three checks in the pack produce a verdict a person can argue with: the copy gate, the first-screen
check and the CRO score. All three are rubrics written by the authors for this pack. None of the
weights or bars below is a measured conversion effect; change them when your own tests say so.

## Copy gate

A reader who did not write the copy scores seven dimensions from 1 to 10: clarity, specificity,
voice, desire, proof, urgency and flow. The bar in `copy_score.py` is every dimension at 7 or more and
a total of 56 of 70, an average of 8 per dimension. The anchors for each score are in
`skills/landing-copy/references/copy-gate.md`. A page with no proof yet drops that dimension and needs
48 of 60. After three failed passes the script tells you to stop editing lines and revisit the offer.

## First-screen check

Seven checks in a 390x664 window: promise, headline, CTA, proof, overlays, hero image weight and the
viewport tag, plus a whole-page scan for trust faults. The window is an iPhone-class width minus the
browser bars, and the thresholds (overlays under a quarter of the screen, a hero image under 1 MB)
are the authors' defaults documented in `skills/first-screen-check/references/checks.md`. Proof is
always JUDGE: the script lists candidates and a person decides.

## CRO score

Twelve dimensions scored 0 to 10, weighted to 100 by `cro_score.py`. The weights put the first screen
first: headline 18, CTA 15, above the fold 12, message match 12 and proof 10, which together hold 67
of the 100 points. Under 60% of those 67 points is BLOCK whatever the total. Grades run A at 85, B at
75, C at 65 and D at 50; anchors for each dimension are in `skills/cro-audit/references/rubric.md`.

The fix list orders problems by stage (page job, headline, section choice, proof placement, friction,
polish) and then by points lost, because a later fix is wasted when an earlier one is wrong. The
stages are documented in `skills/cro-audit/references/page-jobs.md`.

## How the three fit

The first-screen check feeds the first four CRO dimensions; the copy gate feeds copy, headline and
persuasion. A round is shown to the owner only when the copy gate passes, the first-screen check has
no FAIL and the CRO verdict is not BLOCK, as listed in `skills/landing-factory/SKILL.md`.
