#!/usr/bin/env python3
"""Weighted CRO score for one landing page, from 12 dimensions a reviewer scored 0 to 10.

Usage:
  python3 cro_score.py <cro-scores.json> [--weights weights.json]

cro-scores.json (template: templates/cro-scores.json):
{
  "page": "index.html", "page_job": "cold",
  "scores": {"headline": 7, "above_fold": 6, "cta": 8, "message_match": 5, "proof": 4, "persuasion": 6,
             "copy": 7, "objections": 6, "trust": 7, "form": 8, "mobile": 9, "speed": 9},
  "notes":  {"message_match": "the ad says 'first bag free', the page never says it"}
}

Points = score / 10 x weight. Default weights (sum 100): headline 18, cta 15, above_fold 12,
message_match 12, proof 10, persuasion 8, copy 8, objections 5, trust 5, form 4, mobile 2, speed 1.
They are a starting rubric, not a measurement; pass --weights to use your own.

Hard gate: the first five (headline, above_fold, cta, message_match, proof) carry 67 of 100 points.
If they earn under 60% of those points the verdict is BLOCK whatever the total: polish below the fold
does not save a page whose first screen fails. Grades: A 85+, B 75+, C 65+, D 50+, F below.
The fix list orders dimensions by points lost, inside the fix order: page job, headline, section
choice, proof placement, friction, polish.
Exit 1 on BLOCK or grade D/F. Standard library only.
"""
import argparse, json, sys

WEIGHTS = {"headline": 18, "cta": 15, "above_fold": 12, "message_match": 12, "proof": 10, "persuasion": 8,
           "copy": 8, "objections": 5, "trust": 5, "form": 4, "mobile": 2, "speed": 1}
GATE = ["headline", "above_fold", "cta", "message_match", "proof"]
STAGE = {"headline": "2 headline", "message_match": "2 headline", "above_fold": "3 section choice",
         "persuasion": "3 section choice", "objections": "3 section choice", "proof": "4 proof placement",
         "trust": "4 proof placement", "cta": "5 friction", "form": "5 friction", "copy": "6 polish",
         "mobile": "6 polish", "speed": "6 polish"}


def grade(t):
    return "A" if t >= 85 else "B" if t >= 75 else "C" if t >= 65 else "D" if t >= 50 else "F"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scores"); ap.add_argument("--weights")
    a = ap.parse_args()
    d = json.load(open(a.scores, encoding="utf-8"))
    w = dict(WEIGHTS)
    if a.weights:
        w.update(json.load(open(a.weights, encoding="utf-8")))
    s, notes = d.get("scores", {}), d.get("notes", {})
    missing = [k for k in w if k not in s]
    if missing:
        sys.exit(f"missing dimensions: {missing}")
    bad = [k for k in w if not (isinstance(s[k], (int, float)) and 0 <= s[k] <= 10)]
    if bad:
        sys.exit(f"scores must be 0..10: {bad}")
    wsum = sum(w.values())
    pts = {k: s[k] / 10 * w[k] * 100 / wsum for k in w}
    total = sum(pts.values())
    gmax = sum(w[k] for k in GATE) * 100 / wsum
    gpts = sum(pts[k] for k in GATE)
    blocked = gpts < 0.6 * gmax
    print(f"CRO audit: {d.get('page', '?')} (page job: {d.get('page_job', '?')})")
    print(f"  {'dimension':<14}{'score':>6}{'weight':>8}{'points':>8}  note")
    for k in sorted(w, key=lambda k: -w[k]):
        print(f"  {k:<14}{s[k]:>6}{w[k]:>8}{pts[k]:>8.1f}  {notes.get(k, '')}")
    print(f"  first-screen gate: {gpts:.1f} of {gmax:.0f} ({gpts / gmax:.0%}, needs 60%)")
    g = grade(total)
    verdict = "BLOCK" if blocked else g
    print(f"  total {total:.1f} of 100, grade {g}, verdict {verdict}")
    lost = sorted(((w[k] * 100 / wsum - pts[k], k) for k in w), reverse=True)
    lost = [(x, k) for x, k in lost if x > 0.05]
    print("fix list (fix order stage, then points lost):")
    for i, (x, k) in enumerate(sorted(lost, key=lambda t: (STAGE[t[1]], -t[0]))[:6], 1):
        print(f"  {i}. [{STAGE[k]}] {k}: {x:.1f} points lost. {notes.get(k, '')}".rstrip())
    sys.exit(1 if blocked or g in ("D", "F") else 0)


if __name__ == "__main__":
    main()
