# Contributing

Issues and pull requests are welcome.

- **Bug:** include the command, the script's output, and the smallest HTML that reproduces it, with your brand and URLs replaced by example ones.
- **New lint rule:** add it to `copy_lint.py` or `design_lint.py` with a FAIL or WARN label and a one-line reason, list it in the matching canon in `references/`, and show that the Northwind example still passes.
- **New first-screen check or trust fault:** add it to `first_screen.py`, document it in `skills/first-screen-check/references/checks.md`, and place it in the fix ranking.
- **Rubric or weight changes:** show `cro_score.py` before and after on `examples/northwind-roasters/cro-scores.json`, and explain the change in `docs/rubrics.md`.
- **New lesson:** one rule, what it cost, no client names or numbers, added to `skills/landing-factory/references/lessons.md`.
- Only `recon.py`, `shot.py` and `first_screen.py` may need Playwright and Pillow; everything else stays standard library.
- Plain English in docs. No invented benchmarks or conversion statistics; example companies are fictional.

By contributing you agree your work is released under the MIT license.
