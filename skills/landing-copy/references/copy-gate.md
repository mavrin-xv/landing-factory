# The copy gate

Seven dimensions, each scored 1 to 10 by a reader who did not write the copy (a second agent, a
colleague, the owner). `scripts/copy_score.py` applies the pass rules.

## Pass rules

- Every dimension 7 or more.
- Total 56 of 70 or more. When the offer is new and has no proof yet, set proof to null; the bar
  becomes 48 of 60.
- At most three passes. If pass 3 still fails, the problem is the offer or the page job, not the
  lines. Go back to `architecture.md`.

## Anchors

| Dimension | 4 | 7 | 10 |
|---|---|---|---|
| Clarity | after the first screen I still cannot say what is sold | I can say what it is and who it is for | a stranger repeats the offer and the price after five seconds |
| Specificity | adjectives: fresh, premium, perfect | one or two concrete facts per block | every claim is a number, a name or a mechanism from the facts file |
| Voice | could be any company in the category | consistent and plain | sounds like the owner talking to one buyer |
| Desire | describes the seller's process | names the buyer's result | the result is something the buyer can picture on a normal day |
| Proof | none, or proof that cannot be checked | sourced numbers or real quotes, placed somewhere | sourced proof next to every main claim |
| Urgency | fake (countdown, "only 3 left") or none and the page drags | a real reason to act now, stated once | the reason to act now is part of the offer itself (next roast day, cohort start) |
| Flow | blocks in random order, repeated points | follows the skeptic order | each block answers the question the previous one raised |

## Northwind Roasters, pass 1 and pass 2

Pass 1 scored desire 6: the hero said "Roasted Monday and Thursday, shipped in 48 hours", which is the
seller's logistics. Pass 2 moved the roast date on the bag into the mechanism and the box, and the
hero to "Fresh-roasted coffee at your door". Scores and notes: `examples/northwind-roasters/copy-scores.json`.

## Who scores

Not the writer. The writer scores high. Use a fresh agent with only the page and this file, or a
person. Write a note for every dimension under 9; the note is what the next pass fixes.
