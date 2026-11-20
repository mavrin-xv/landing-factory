# CRO rubric

Twelve dimensions, each scored 0 to 10 by a reviewer, weighted to 100 points by
`scripts/cro_score.py`. The weights are a starting rubric that puts the first screen first; they
are not measured conversion effects. Pass `--weights` with your own when your tests say otherwise.

| Dimension | Weight | 3 | 6 | 9 |
|---|---|---|---|---|
| headline | 18 | a slogan or the brand name | says what it is | says what the buyer gets, in their words, under 12 words |
| cta | 15 | "Submit", several different labels, below the fold | one label, visible | one action named by its result, repeated with the same label, never wraps |
| above_fold | 12 | the first screen is a big image and a logo | H1 and CTA visible at 390 | H1, sub with outcome and cost, CTA, product visual and one proof line at 390x664 |
| message_match | 12 | the page does not mention what the ad promised | the topic matches | the ad's words and image are on the first screen |
| proof | 10 | none, or unverifiable | real proof somewhere | sourced proof next to each main claim |
| persuasion | 8 | no reason to choose this over doing nothing | one anchor or one comparison | value stack, honest anchor, the reason to act now built into the offer |
| copy | 8 | jargon, long paragraphs, hype | plain and short | specific, one idea per sentence, the heading skeleton sells alone |
| objections | 5 | none answered | an FAQ exists | the real objections, in the buyer's words, with the refund rule |
| trust | 5 | stock photos, no people, placeholders | contacts and policies | real product, real people, real place |
| form | 4 | many fields, no reason for each | short | the fewest fields that do the job, each with a reason |
| mobile | 2 | horizontal scroll or broken blocks at 390 | works at 390 | built for 390 first |
| speed | 1 | hero image over 1 MB, layout shifts | acceptable | small hero, no shifts |

## The hard gate

The first five dimensions (headline, cta, above_fold, message_match, proof) hold 67 of the 100
points. If they earn under 60% of those points, the verdict is BLOCK whatever the total. A page whose
first screen fails does not get saved by a good FAQ.

## Grades

A 85 or more, B 75 or more, C 65 or more, D 50 or more, F below 50. The script exits 1 on BLOCK, D or F.

## Output

Three groups, in this order:

- **Quick wins:** a change under an hour that recovers points (a CTA label, a sub line, a proof line moved up).
- **High impact:** changes in stages 1 to 3 of the fix order (page job, headline, section choice).
- **Test ideas:** changes where the reviewer is not sure; each with the metric that would decide it.

Each item names the dimension, the block, the exact change, and for copy changes two alternative lines.

## Honest use

- A score is a reviewer's judgement on a fixed scale, not a prediction of conversion rate.
- Two reviewers who disagree by more than 2 points on a dimension should talk before averaging.
- Never quote outside conversion statistics in an audit unless you have the source next to it.
