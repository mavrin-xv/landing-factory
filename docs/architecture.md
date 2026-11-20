# Architecture

The pack is seven skills and nine Python scripts. There is no server and no database. Each project
is a folder: the brief, the facts file, the architecture, the page, the round's `gates.json` and the
script outputs. An agent or a person can pick up any round from those files.

## Data flow

```
 inputs                        scripts                 files
 ------                        -------                 -----
 reference URL or file      -> recon.py            ->  <name>-recon.json, 1440/390/first-screen PNGs, slices
 <name>-recon.json          -> ref_map.py          ->  reference-map.md (one row per block)
 brief, map, facts          -> (agent + owner)     ->  architecture.md
 page + facts + promise     -> copy_lint.py        ->  heading skeleton, FAIL/WARN lines
 copy-scores.json           -> copy_score.py       ->  PASS or REWRITE with the lowest dimension
 page + CSS                 -> design_lint.py      ->  FAIL/WARN lines per section
 page + gates.json          -> gates.py            ->  anchors, files, H1, counts, banned strings, classes
 site folder                -> shot.py             ->  full pages and slices at 1440 and 390, runtime errors
 page + promise             -> first_screen.py     ->  7 checks, trust faults, first-screen.png, fix list
 cro-scores.json            -> cro_score.py        ->  weighted total, grade, staged fix list
```

## Which skill owns what

| Skill | Reads | Produces | Gate it owns |
|---|---|---|---|
| reference-recon | the reference | screenshots, recon JSON, reference map, asset list | every block decided |
| landing-copy | brief, architecture, facts | the words | copy lint, copy gate |
| landing-design | architecture, copy, tokens | HTML and CSS | design lint |
| landing-qa | the site folder | screenshots, wiring report | shot, gates |
| first-screen-check | the page, the clicked promise | first-screen report | no FAIL, no trust fault |
| cro-audit | page, screenshots, page job | weighted score and fix list | not BLOCK, grade C or better |
| landing-factory | all of the above | the round report | all gates before the owner sees a round |

## Design rules

- **Facts in a file.** The copy lint compares every number on the page with `facts.md`. A number with no
  source is a FAIL, so invented proof cannot slip in through a rewrite.
- **Mobile first, checked at the phone size.** The base CSS is the 390 layout; the first-screen check
  opens a 390x664 window because that is where most paid traffic lands.
- **Scripts count, people judge.** Proof candidates, the copy gate and the CRO score are filled by a
  reader; scripts only total, gate and order them.
- **Unknown is not a pass.** A check that cannot run (no browser, an image it could not measure) prints
  SKIP with the reason.
- **Rounds are reversible.** Every round starts with a backup of the previous page, and the build edits
  fail loudly when the text they expect to replace is missing.
- **Local only.** Pages are served on 127.0.0.1 for checks. Nothing in the pack deploys.

## Dependencies

`recon.py`, `shot.py` and `first_screen.py` use Playwright with Chromium and Pillow; each prints the
install line and exits when they are missing. `first_screen.py --static` runs without them. The other
six scripts use the Python standard library only.
