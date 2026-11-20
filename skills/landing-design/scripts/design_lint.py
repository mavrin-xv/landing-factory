#!/usr/bin/env python3
"""Static design lint for a landing page: the template tells a screenshot review misses. Exit 1 on FAIL.

Usage:
  python3 design_lint.py <page.html> [--css css/a.css,css/b.css] [--allow-svg] [--accents N]

Reads the page and its local stylesheets (from <link rel="stylesheet">, or --css).
FAIL:
  viewport      no <meta name="viewport">
  pure-black    #000 or #000000 used as a color (use an off-black token)
  video         <video> without muted + playsinline + poster (autoplay is blocked, the first frame is blank)
  lazy-hero     loading="lazy" on an image in the first section (it can render blank above the fold
                and in full-page screenshots)
  eyebrows      more small labels above headings than one per 3 sections (class names with
                eyebrow, kicker, overline or pretitle)
  text-section  a <section> with a heading and paragraphs but no visual at all (img, video, svg,
                picture, canvas, table, ol, figure, details for an FAQ accordion, or an element whose class says diagram, loop,
                scheme, mock, chart, logos, wall, grid, tile or stat)
WARN:
  accents       more than --accents (default 2) saturated colors in the CSS: one accent page-wide
  fonts         more than 2 font families
  svg           inline <svg> elements (hand-drawn icons drift; use one icon font) unless --allow-svg
  three-cards   grid-template-columns: repeat(3, 1fr), the generic three equal cards row
  desktop-first max-width media queries and no min-width ones (build for 390 first)
  layout-repeat two sections in a row with the same class list (same layout family twice)
Standard library only.
"""
import argparse, colorsys, math, os, re, sys
from html.parser import HTMLParser

VISUAL_TAGS = {"img", "video", "svg", "picture", "canvas", "table", "ol", "figure", "iframe", "details"}
VISUAL_CLASS = re.compile(r"(diagram|loop|scheme|mock|chart|logos?|wall|grid|tiles?|stat|steps|gallery|media|shot)", re.I)
EYEBROW = re.compile(r"(eyebrow|kicker|overline|pretitle)", re.I)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.viewport = False; self.css = []; self.videos = []; self.svg = 0
        self.sections = []; self.depth = 0; self.cur = None; self.eyebrows = 0; self.first_lazy = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = a.get("class") or ""
        if tag == "meta" and (a.get("name") or "").lower() == "viewport":
            self.viewport = True
        if tag == "link" and "stylesheet" in (a.get("rel") or "") and a.get("href") and not a["href"].startswith("http"):
            self.css.append(a["href"])
        if tag == "video":
            self.videos.append(a)
        if tag == "svg":
            self.svg += 1
        if EYEBROW.search(cls):
            self.eyebrows += 1
        if tag in ("section", "header") and self.cur is None:
            self.cur = {"tag": tag, "cls": cls.strip(), "id": a.get("id"), "visual": False, "heading": False, "p": 0}
            self.sections.append(self.cur); self.depth = 0
        if self.cur is not None:
            if tag == self.cur["tag"]:
                self.depth += 1
            if tag in VISUAL_TAGS or VISUAL_CLASS.search(cls):
                self.cur["visual"] = True
            if tag in ("h1", "h2", "h3"):
                self.cur["heading"] = True
            if tag == "p":
                self.cur["p"] += 1
            if tag == "img" and (a.get("loading") or "").lower() == "lazy" and len(self.sections) <= 2:
                self.first_lazy.append(a.get("src"))

    def handle_endtag(self, tag):
        if self.cur is not None and tag == self.cur["tag"]:
            self.depth -= 1
            if self.depth <= 0:
                self.cur = None


def saturated(hexv):
    hexv = hexv.lstrip("#")
    if len(hexv) == 3:
        hexv = "".join(c * 2 for c in hexv)
    r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return s > 0.35 and 0.15 < l < 0.85


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page"); ap.add_argument("--css"); ap.add_argument("--allow-svg", action="store_true")
    ap.add_argument("--accents", type=int, default=2)
    a = ap.parse_args()
    html = open(a.page, encoding="utf-8").read()
    base = os.path.dirname(os.path.abspath(a.page))
    p = Page(); p.feed(html)
    sheets = a.css.split(",") if a.css else p.css
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))
    for sh in sheets:
        path = os.path.join(base, sh)
        if os.path.exists(path):
            css += "\n" + open(path, encoding="utf-8").read()
    css_nc = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    fails, warns = [], []

    if not p.viewport:
        fails.append("viewport: no <meta name=\"viewport\">")
    if re.search(r"#000(000)?\b(?![0-9a-f])", css_nc, re.I) or re.search(r"rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)", css_nc):
        fails.append("pure-black: #000 in the CSS, use an off-black token")
    for v in p.videos:
        miss = [k for k in ("muted", "playsinline", "poster") if k not in v]
        if miss:
            fails.append(f"video: {v.get('src') or 'video'} missing {', '.join(miss)}")
    for s in p.first_lazy:
        fails.append(f"lazy-hero: loading=\"lazy\" on {s} in the first screen area")
    real = [s for s in p.sections if s["tag"] == "section"]
    cap = max(1, math.ceil(len(p.sections) / 3))
    if p.eyebrows > cap:
        fails.append(f"eyebrows: {p.eyebrows} labels above headings for {len(p.sections)} sections (max {cap})")
    for s in real:
        if s["heading"] and s["p"] and not s["visual"]:
            fails.append(f"text-section: <section{' id=' + s['id'] if s['id'] else ''}> is a heading plus paragraphs with no visual")

    colors = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", css_nc)}
    accents = sorted(c for c in colors if saturated(c))
    if len(accents) > a.accents:
        warns.append(f"accents: {len(accents)} saturated colors {accents[:6]} (want {a.accents} or fewer)")
    fams = {f.split(",")[0].strip().strip("'\"").lower() for f in re.findall(r"font-family\s*:\s*([^;}]+)", css_nc)}
    fams = {f for f in fams if f and not f.startswith("var(") and f not in ("inherit", "system-ui", "sans-serif", "serif", "monospace")}
    if len(fams) > 2:
        warns.append(f"fonts: {len(fams)} families {sorted(fams)}")
    if p.svg and not a.allow_svg:
        warns.append(f"svg: {p.svg} inline <svg> (icons belong in one icon font; diagrams are fine, pass --allow-svg)")
    if re.search(r"grid-template-columns\s*:\s*repeat\(\s*3\s*,\s*1fr\s*\)", css_nc):
        warns.append("three-cards: repeat(3, 1fr) found, check it is not the generic three equal cards row")
    if re.search(r"@media[^{]*max-width", css_nc) and not re.search(r"@media[^{]*min-width", css_nc):
        warns.append("desktop-first: only max-width media queries; design at 390 and add desktop with min-width")
    for x, y in zip(real, real[1:]):
        if x["cls"] and x["cls"] == y["cls"]:
            warns.append(f"layout-repeat: two sections in a row with class \"{x['cls']}\"")

    print(f"design_lint: {len(p.sections)} sections, {len(sheets)} stylesheet(s), {len(accents)} accent color(s), "
          f"{p.eyebrows} eyebrow(s), {len(p.videos)} video(s)")
    for w in warns:
        print("WARN", w)
    for f in fails:
        print("FAIL", f)
    print("design_lint: all green" if not fails else f"design_lint: {len(fails)} fail(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
