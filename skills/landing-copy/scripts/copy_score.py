#!/usr/bin/env python3
"""The copy gate: 7 dimensions scored 1 to 10 by a reader, checked against fixed pass rules.

Usage:
  python3 copy_score.py <scores.json>

scores.json (template: templates/copy-scores.json):
{
  "page": "index.html", "pass": 1,
  "scores": {"clarity": 8, "specificity": 7, "voice": 8, "desire": 7, "proof": 6, "urgency": 7, "flow": 8},
  "notes":  {"proof": "the only proof is a review count with no source"}
}
Set "proof" to null when the offer is new and has no proof yet; the bar becomes 48 of 60.

Pass rules: every dimension 7 or more, and a total of 56 of 70 or more (48 of 60 without proof).
After 3 passes that still fail, stop rewriting lines: the problem is the offer or the page job,
go back to the architecture. Anchors for each score: references/copy-gate.md.
Exit 1 when the copy fails the gate. Standard library only.
"""
import json, sys

DIMS = ["clarity", "specificity", "voice", "desire", "proof", "urgency", "flow"]


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); sys.exit(0 if len(sys.argv) > 1 else 2)
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    s, notes = d.get("scores", {}), d.get("notes", {})
    missing = [k for k in DIMS if k not in s]
    if missing:
        sys.exit(f"missing dimensions: {missing}")
    used = [k for k in DIMS if s[k] is not None]
    total, bar = sum(s[k] for k in used), (56 if len(used) == 7 else 48)
    low = [k for k in used if s[k] < 7]
    print(f"copy gate for {d.get('page', '?')}, pass {d.get('pass', 1)}")
    for k in DIMS:
        v = s[k]
        mark = "n/a" if v is None else ("LOW" if v < 7 else "ok")
        print(f"  {k:<12} {'-' if v is None else v:>3}  {mark:<4} {notes.get(k, '')}")
    print(f"  total {total} of {len(used) * 10} (bar {bar})")
    ok = not low and total >= bar
    if ok:
        print("copy gate: PASS")
    else:
        why = []
        if low:
            why.append("below 7: " + ", ".join(low))
        if total < bar:
            why.append(f"total {total} < {bar}")
        print("copy gate: FAIL (" + "; ".join(why) + ")")
        if int(d.get("pass", 1)) >= 3:
            print("third failed pass: stop editing lines, revisit the offer and the page job in architecture.md")
        else:
            print("rewrite the lowest dimension first, then score again with pass +1")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
