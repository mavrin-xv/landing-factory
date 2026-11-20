# AGENTS.md

Guidance for an AI agent working with or on this repo.

## Using the pack
- Skills: `landing-factory` (the round loop), `reference-recon`, `landing-design`, `landing-copy`, `first-screen-check`, `cro-audit`, `landing-qa`. Each `SKILL.md` lists its inputs, gates and output.
- Fill the brief before building. Price, proof, refund terms and quotes come from the owner; a blank is a question, never a guess.
- Copy uses only facts in `facts.md`. Never invent numbers, ratings, reviews, logos or testimonials.
- Run the scripts for counts, checks and scores; do not redo them in the prompt. Read every screenshot slice the scripts save.
- Back up the page before each round (`page-vN.html`). Never deploy live; show a local preview or a preview link the owner set up.
- On a reskin, never use the reference's logos, photos, illustrations or text.
- `recon.py`, `shot.py` and `first_screen.py` need Playwright and Pillow. Without them, say so and use `first_screen.py --static`; do not report a screenshot check as passed.
- Python: `python3` on Windows, `python3` elsewhere. In Git Bash, set `MSYS_NO_PATHCONV=1` before an argument that starts with `/`.

## Changing the pack
- Keep `SKILL.md` under 500 lines; detail goes in `references/`.
- Script changes: re-run the example and update the outputs in `examples/northwind-roasters/out/`:
  ```
  E=examples/northwind-roasters
  python3 skills/reference-recon/scripts/recon.py $E/reference/index.html $E/out --name contoso
  python3 skills/reference-recon/scripts/ref_map.py $E/out/contoso-recon.json --out $E/out/reference-map.md
  python3 skills/landing-copy/scripts/copy_lint.py $E/site/index.html --facts $E/facts.md --promise "fresh-roasted coffee at your door"
  python3 skills/landing-copy/scripts/copy_score.py $E/copy-scores.json
  python3 skills/landing-design/scripts/design_lint.py $E/site/index.html
  python3 skills/landing-qa/scripts/gates.py $E/site/index.html $E/gates.json
  python3 skills/landing-qa/scripts/shot.py $E/site index.html $E/out/shots --overflow
  python3 skills/first-screen-check/scripts/first_screen.py $E/site/index.html --promise "fresh-roasted coffee at your door" --out $E/out
  python3 skills/cro-audit/scripts/cro_score.py $E/cro-scores.json
  ```
- Delete `out/shots/` after reading the slices; it is not committed.
- Fail visibly: a check that could not run prints SKIP with the reason, never PASS.
