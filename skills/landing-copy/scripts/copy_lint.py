#!/usr/bin/env python3
"""Lint the copy of a landing page (HTML) for the faults that cost trust or clarity. Exit 1 on FAIL.

Usage:
  python3 copy_lint.py <page.html> [--facts facts.md] [--promise "ad phrase"] [--allow "word,word"]

FAIL (blocks shipping):
  dash          em or en dash in visible text (reads as machine-written; use a comma, colon or period)
  hype          a word from the hype list (unlock, seamless, game changer, revolutionary, ...)
  fake-urgency  countdowns, "only N left", "offer ends tonight", "last chance" with no real deadline
  promise       income or result promises: "guaranteed results", "passive income", "make $N a day"
  unsourced     a number in visible text that does not appear in --facts (prices, counts, percents)
  h1            no H1, or more than one
  hero-sub      the first paragraph after the H1 is longer than 20 words
  ad-match      --promise given and the phrase is not in the first 80 words
WARN (look at it):
  h1-long       H1 over 12 words
  generic-cta   "Submit", "Learn more", "Click here", "Get started" with nothing after it
  cta-count     more than one distinct primary CTA label (one page, one action)

Also prints the heading skeleton: read the H1 to H3 alone, top to bottom. If that list does not sell
the offer, the sections do not either.
Standard library only.
"""
import argparse, re, sys
from html.parser import HTMLParser

HYPE = r"\b(unlock\w*|unleash\w*|game[- ]?changer|seamless\w*|revolutioni[sz]\w*|supercharge\w*|effortless\w*|cutting[- ]edge|best[- ]in[- ]class|world[- ]class|next[- ]gen\w*|elevate\w*|transformative|synerg\w*|state[- ]of[- ]the[- ]art|in today's world)\b"
URGENCY = r"\b(only \d+ (left|spots?|seats?)|offer ends (today|tonight|soon)|last chance|hurry|ends in \d+|limited time only|before it'?s gone)\b"
PROMISE = r"\b(guaranteed (results?|income|sales|traffic|views)|passive income|make \$?\d[\d,.]*k? (a|per) (day|week|month)|risk[- ]free income|get rich)\b"
GENERIC_CTA = {"submit", "learn more", "click here", "get started", "read more", "more", "go"}
NUM = re.compile(r"(?<![\w#-])[$€£]?\d[\d,.]*(?:\s?(?:%|k|K|x|M|min|minutes|hours|days|cups|bags))?")


class Copy(HTMLParser):
    """Collects text blocks in document order. Text inside a nested tag counts for every open block,
    so a <p> with a <strong> inside still has its full sentence."""
    BLOCK = ("h1", "h2", "h3", "p", "li", "a", "button", "figcaption", "td", "th", "dt", "dd", "label")

    def __init__(self):
        super().__init__(); self.skip = 0; self.open = []; self.blocks = []; self.all = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "template"):
            self.skip += 1; return
        if tag in self.BLOCK:
            cls = dict(attrs).get("class") or ""
            b = {"tag": tag, "text": "", "cta": tag == "button" or bool(re.search(r"\b(btn|button|cta)\b", cls))}
            self.blocks.append(b); self.open.append(b)

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "template"):
            self.skip = max(0, self.skip - 1); return
        for i in range(len(self.open) - 1, -1, -1):
            if self.open[i]["tag"] == tag:
                del self.open[i:]; break

    def handle_data(self, d):
        if self.skip or not d.strip():
            return
        self.all.append(d)
        for b in self.open:
            b["text"] += " " + d


def norm(t):
    return re.sub(r"\s+", " ", t).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page"); ap.add_argument("--facts"); ap.add_argument("--promise")
    ap.add_argument("--allow", default="", help="comma-separated phrases or numbers allowed on purpose")
    a = ap.parse_args()
    html = open(a.page, encoding="utf-8").read()
    p = Copy(); p.feed(html)
    blocks = [dict(b, text=norm(b["text"])) for b in p.blocks if norm(b["text"])]
    visible = norm(" ".join(p.all))
    allow = [x.strip().lower() for x in a.allow.split(",") if x.strip()]
    fails, warns = [], []

    for ch, nm in (("—", "em dash"), ("–", "en dash")):
        if ch in visible:
            ctx = [b["text"][:60] for b in blocks if ch in b["text"]][:3]
            fails.append(f"dash: {nm} x{visible.count(ch)} in {ctx}")
    for rx, kind in ((HYPE, "hype"), (URGENCY, "fake-urgency"), (PROMISE, "promise")):
        for m in sorted(set(x.group(0) for x in re.finditer(rx, visible, re.I))):
            if m.lower() not in allow:
                fails.append(f"{kind}: {m!r}")
    if re.search(r"data-countdown|class=\"[^\"]*countdown", html, re.I):
        fails.append("fake-urgency: a countdown element in the markup")

    h1s = [b for b in blocks if b["tag"] == "h1"]
    if len(h1s) != 1:
        fails.append(f"h1: {len(h1s)} found (want 1)")
    if h1s:
        h1 = h1s[0]; words = len(h1["text"].split())
        if words > 12:
            warns.append(f"h1-long: {words} words: {h1['text']!r}")
        i = blocks.index(h1)
        sub = next((b for b in blocks[i + 1:i + 6] if b["tag"] == "p"), None)
        if sub and len(sub["text"].split()) > 20:
            fails.append(f"hero-sub: {len(sub['text'].split())} words (max 20): {sub['text'][:90]!r}")

    if a.promise:
        first = " ".join(visible.split()[:80]).lower()
        if norm(a.promise).lower() not in first:
            fails.append(f"ad-match: {a.promise!r} is not in the first 80 words")

    if a.facts:
        facts = open(a.facts, encoding="utf-8").read().lower()
        seen = set()
        for b in blocks:
            for m in NUM.finditer(b["text"]):
                n = m.group(0).strip()
                core = re.match(r"[$€£]?\d[\d,.]*", n).group(0).rstrip(".,")
                if not core or core in seen or len(core.strip("$€£")) == 0:
                    continue
                seen.add(core)
                if core.lower() in allow or n.lower() in allow:
                    continue
                if core.lower() not in facts:
                    fails.append(f"unsourced: {n!r} in {b['text'][:60]!r} (add it to the facts file with its source, or cut it)")

    ctas = [b["text"] for b in blocks if b["cta"]]
    for c in sorted(set(ctas)):
        if c.lower().strip(" .!>") in GENERIC_CTA:
            warns.append(f"generic-cta: {c!r} says nothing about what happens next")
    distinct = sorted(set(c.lower() for c in ctas))
    if len(distinct) > 2:
        warns.append(f"cta-count: {len(distinct)} different CTA labels {distinct[:5]}: pick one action and repeat it")

    print("heading skeleton (read it alone, does it sell?):")
    for b in blocks:
        if b["tag"] in ("h1", "h2", "h3"):
            print(f"  {'  ' * (int(b['tag'][1]) - 1)}{b['tag'].upper()} {b['text']}")
    print(f"words: {len(visible.split())}  CTAs: {len(ctas)} ({len(distinct)} distinct)")
    for w in warns:
        print("WARN", w)
    for f in fails:
        print("FAIL", f)
    print("copy_lint: all green" if not fails else f"copy_lint: {len(fails)} fail(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
