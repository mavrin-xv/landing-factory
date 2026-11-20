#!/usr/bin/env python3
"""Turn a recon JSON into a reference map: one row per reference section, with columns you fill in
for your own page (our block, the job it does, the visual it carries, keep / change / drop).

Usage:
  python3 ref_map.py <name>-recon.json [--out reference-map.md]

The map is the contract for a reskin: every block on your page points at a reference block, or is
marked NEW with a reason. Re-read it against the reference's first screen at the start of every round.
Standard library only.
"""
import argparse, json, sys

JOB_HINTS = [  # first matching word in the section's headings or text suggests the job it does
    ("faq", "objections"), ("question", "objections"), ("pricing", "offer"), ("price", "offer"),
    ("plan", "offer"), ("how it works", "mechanism"), ("step", "mechanism"), ("review", "proof"),
    ("testimonial", "proof"), ("customers", "proof"), ("trusted", "proof"), ("for ", "segments"),
    ("about", "about"), ("team", "about"), ("feature", "components"), ("what you get", "components"),
]


def guess_job(sec, i, n):
    if i == 0 and sec["tag"] == "header":
        return "navigation"
    if any(h.startswith("H1") for h in sec["headings"]):
        return "hero: what it is + first CTA"
    if i == n - 1 and sec["tag"] == "footer":
        return "footer"
    blob = " ".join(sec["headings"] + sec["text"][:8]).lower()
    for word, job in JOB_HINTS:
        if word in blob:
            return job
    return "?"


def visual(sec):
    m = sec["media"]
    bits = [f"{k} {v}" for k, v in m.items() if v]
    return ", ".join(bits) if bits else "text only (needs a visual)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recon"); ap.add_argument("--out")
    a = ap.parse_args()
    d = json.load(open(a.recon, encoding="utf-8"))
    secs = d.get("sections", [])
    lines = [f"# Reference map: {d.get('title') or d.get('source')}", "",
             f"Reference H1: {d.get('h1')}", "",
             f"Reference first screen (390x664) CTAs: {', '.join(d.get('first_screen_ctas') or []) or 'none found'}", "",
             "| # | Reference block (first heading) | Job it does | Visual it carries | Our block | Keep / change / drop | Why |",
             "|---|---|---|---|---|---|---|"]
    for i, s in enumerate(secs):
        head = (s["headings"][0].split(": ", 1)[-1] if s["headings"] else (s["text"][0] if s["text"] else "(empty)"))[:70]
        lines.append(f"| {i + 1} | {head.replace('|', '/')} | {guess_job(s, i, len(secs))} | {visual(s)} |  |  |  |")
    lines += ["", "Rows for blocks the reference does not have: add them below with `NEW` in the first column and a reason.",
              "", "Tokens seen (do not copy on a reskin, read them for density and rhythm):", ""]
    t = d.get("tokens", {})
    for k in ("fonts", "colors", "backgrounds", "radii"):
        lines.append(f"- {k}: " + "; ".join(f"{v} ({c})" for v, c in t.get(k, [])[:6]))
    text = "\n".join(lines) + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text); print(f"wrote {a.out} ({len(secs)} reference blocks)")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
