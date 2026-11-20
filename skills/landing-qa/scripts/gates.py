#!/usr/bin/env python3
"""Wiring gate for a landing page build round. Exit 1 on any failure.

Usage:
  python3 gates.py <page.html> <gates.json>

Always checked:
  - every href="#id" points at an element with that id
  - every local src/href (images, css, js, video, poster) exists on disk
  - the page has exactly one <h1> and a <meta name="viewport">
  - a CSS class listed in "classes" is not defined in two stylesheets (the collision trap: a new
    .tree or .ab silently picks up rules from an older file and the block renders wrong)

gates.json (all keys optional):
{
  "counts":  {"data-plan=\\"monthly\\"": 1, "href=\\"#offer\\"": 3},  exact count of each string,
                                                                       for wiring that must survive edits
  "zero":    ["lorem", "TODO", "old-product-name"],                   must not appear anywhere (case-insensitive)
  "css":     ["css/base.css", "css/site.css"],                        stylesheets to check for collisions,
                                                                       the newest last
  "classes": ["wtree", "abx"]                                         classes this round added
}
Copy rules (dashes, hype words, unsourced numbers) live in landing-copy's copy_lint.py.
Standard library only.
"""
import json, os, re, sys
from html.parser import HTMLParser


class Facts(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids, self.anchors, self.local, self.h1, self.viewport = set(), [], [], 0, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and (a.get("name") or "").lower() == "viewport":
            self.viewport = True
        for k in ("href", "src", "poster"):
            v = a.get(k)
            if not v:
                continue
            if k == "href" and v.startswith("#") and len(v) > 1:
                self.anchors.append(v[1:])
            elif not re.match(r"^(https?:|mailto:|tel:|data:|#|//|javascript:)", v, re.I):
                self.local.append(v.split("#")[0].split("?")[0])
        if a.get("srcset"):
            for part in a["srcset"].split(","):
                u = part.strip().split(" ")[0]
                if u and not re.match(r"^(https?:|data:|//)", u):
                    self.local.append(u)


def main():
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); sys.exit(0 if len(sys.argv) > 1 else 2)
    page, cfg = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
    html = open(page, encoding="utf-8").read()
    base = os.path.dirname(os.path.abspath(page))
    f = Facts(); f.feed(html)
    fail = []

    for a in sorted(set(f.anchors)):
        if a not in f.ids:
            fail.append(f"anchor #{a} has no element with id=\"{a}\"")
    for p in sorted(set(f.local)):
        if p and not os.path.exists(os.path.join(base, p.lstrip("/"))):
            fail.append(f"missing local file: {p}")
    if f.h1 != 1:
        fail.append(f"<h1> count {f.h1} (want 1)")
    if not f.viewport:
        fail.append("no <meta name=\"viewport\">: phones render the desktop layout zoomed out")

    for s, n in cfg.get("counts", {}).items():
        c = html.count(s)
        if c != n:
            fail.append(f"count {s!r}: {c} (want {n})")
    low = html.lower()
    for s in cfg.get("zero", []):
        if s.lower() in low:
            fail.append(f"must be gone: {s!r} x{low.count(s.lower())}")

    sheets = cfg.get("css", [])
    texts = {}
    for sh in sheets:
        path = os.path.join(base, sh)
        if not os.path.exists(path):
            fail.append(f"css file not found: {sh}"); continue
        texts[sh] = open(path, encoding="utf-8").read()
    for cl in cfg.get("classes", []):
        rx = re.compile(r"\.%s(?![\w-])" % re.escape(cl))
        where = [sh for sh, t in texts.items() if rx.search(t)]
        if len(where) > 1:
            fail.append(f"class .{cl} is defined in {where}: rename the new one")

    print("\n".join("FAIL " + x for x in fail) if fail else
          f"gates: all green ({len(set(f.anchors))} anchors, {len(set(f.local))} local files, "
          f"{len(cfg.get('counts', {}))} counts, {len(cfg.get('zero', []))} zero rules)")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
