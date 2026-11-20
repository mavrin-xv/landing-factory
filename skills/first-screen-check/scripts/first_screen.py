#!/usr/bin/env python3
"""What a phone user sees before scrolling: 7 checks on a 390x664 screen plus trust faults anywhere
on the page, ranked into a fix list with one "Fix first". Exit 1 when a check fails.

Usage:
  python3 first_screen.py <url | local .html> [--promise "ad phrase"] [--out dir] [--static]

  A local file is served on 127.0.0.1. --out saves first-screen.png there.
  --static  no browser: reads the HTML and treats the first 80 visible words as the first screen.
            Use it when Playwright is not installed; the screenshot wins when they disagree.

Checks (first screen, 390x664 CSS px):
  1 promise    the --promise phrase is visible on the first screen (skipped without --promise)
  2 headline   one H1, fully on the first screen
  3 cta        a link or button styled as a CTA (class btn/button/cta, or a <button>) on the first screen
  4 proof      JUDGE: candidate proof text is listed (ratings, review counts, logos); a person decides
  5 covered    no fixed or sticky element (cookie bar, popup, chat bubble) covers more than 25% of the screen
  6 hero-bytes the largest image on the first screen is under 1 MB
  7 viewport   <meta name="viewport"> present
Trust faults (whole page): lorem ipsum or TODO left in, placeholder prices ($0, 9,999, 0.00, XX),
template text ("this template", "your headline here"), aggregateRating in JSON-LD with no visible
reviews, links to staging hosts (localhost, *.webflow.io, *.vercel.app, *.netlify.app, *.pages.dev).
Ranking: cta and covered first, then promise, proof, headline, hero-bytes, viewport, then faults.
"""
import argparse, http.server, json, os, re, socket, sys, threading
from functools import partial
from html.parser import HTMLParser

ORDER = ["cta", "covered", "promise", "proof", "headline", "hero-bytes", "viewport"]
WHY = {
    "cta": "nobody scrolls to find the button; the first screen has to offer the next step",
    "covered": "an overlay hides the offer on the one screen that decides stay or leave",
    "promise": "the visitor clicked a promise; if the page does not repeat it they think they landed wrong",
    "proof": "a claim with no proof nearby reads as an ad",
    "headline": "the H1 has to say what this is before anything else loads",
    "hero-bytes": "a heavy hero image is the slowest thing on a phone connection",
    "viewport": "without it phones render the desktop layout zoomed out",
}
PROOF_RX = r"(\d[\d,.]*\s*(reviews?|ratings?|customers|orders|subscribers|stars?)|★|rated \d|\d\.\d\s*/\s*5|trusted by|as seen in)"

FIRST = r"""
() => {
  const H = innerHeight, W = innerWidth;
  const inView = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && r.top < H && r.bottom > 0 && r.left < W && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const full = el => { const r = el.getBoundingClientRect(); return r.top >= -1 && r.bottom <= H + 1; };
  const texts = [];
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walk.nextNode()) { const n = walk.currentNode, p = n.parentElement;
    if (p && n.textContent.trim() && !['SCRIPT','STYLE','NOSCRIPT'].includes(p.tagName) && inView(p)) texts.push(n.textContent.trim().replace(/\s+/g,' ')); }
  const h1s = [...document.querySelectorAll('h1')];
  const ctas = [...document.querySelectorAll('a, button')].filter(e => inView(e) &&
     (e.tagName === 'BUTTON' || /\b(btn|button|cta)\b/i.test(e.className || ''))).map(e => e.innerText.trim().replace(/\s+/g,' '));
  const cover = [];
  for (const el of document.querySelectorAll('body *')) { const s = getComputedStyle(el);
    if ((s.position === 'fixed' || s.position === 'sticky') && inView(el)) { const r = el.getBoundingClientRect();
      const area = Math.max(0, Math.min(r.right, W) - Math.max(r.left, 0)) * Math.max(0, Math.min(r.bottom, H) - Math.max(r.top, 0));
      const share = area / (W * H);
      const isNav = r.top <= 1 && r.height <= 90;
      if (share > 0.25 && !isNav) cover.push((el.tagName.toLowerCase() + '.' + (el.className || '')).slice(0, 60) + ' ' + Math.round(share * 100) + '%'); } }
  const imgs = [...document.images].filter(inView).map(i => { const r = i.getBoundingClientRect();
    const e = performance.getEntriesByName(i.currentSrc || i.src)[0];
    return {src: i.getAttribute('src'), area: Math.round(r.width * r.height), bytes: e ? (e.encodedBodySize || e.transferSize || 0) : null}; })
    .sort((a, b) => b.area - a.area);
  return {text: texts.join(' | '), h1: h1s.map(h => h.innerText.trim()), h1_full: h1s.length ? full(h1s[0]) && inView(h1s[0]) : false,
          ctas: [...new Set(ctas)].filter(Boolean), cover, imgs: imgs.slice(0, 3),
          viewport: !!document.querySelector('meta[name=viewport]')};
}
"""


class Static(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.words = []; self.h1 = []; self.in_h1 = False; self.h1_at = None
        self.ctas = []; self.in_cta = None; self.viewport = False; self.imgs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        if tag == "meta" and (a.get("name") or "").lower() == "viewport":
            self.viewport = True
        if tag == "h1":
            self.in_h1 = True; self.h1.append("")
            if self.h1_at is None:
                self.h1_at = len(self.words)
        if tag in ("a", "button") and (tag == "button" or re.search(r"\b(btn|button|cta)\b", a.get("class") or "")):
            self.in_cta = len(self.words); self.ctas.append(["", len(self.words)])
        if tag == "img" and len(self.words) < 80:
            self.imgs.append({"src": a.get("src"), "area": None, "bytes": None})

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self.skip = max(0, self.skip - 1)
        if tag == "h1":
            self.in_h1 = False
        if tag in ("a", "button"):
            self.in_cta = None

    def handle_data(self, d):
        if self.skip or not d.strip():
            return
        self.words += d.split()
        if self.in_h1:
            self.h1[-1] += " " + d.strip()
        if self.in_cta is not None and self.ctas:
            self.ctas[-1][0] += " " + d.strip()



class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

def serve(path):
    root, page = os.path.dirname(os.path.abspath(path)), os.path.basename(path)
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    h = partial(Quiet, directory=root)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), h)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{port}/{page}"


def fetch_html(target):
    if os.path.exists(target):
        return open(target, encoding="utf-8").read()
    from urllib.request import Request, urlopen
    req = Request(target, headers={"User-Agent": "Mozilla/5.0 (compatible; first-screen-check)"})
    return urlopen(req, timeout=30).read().decode("utf-8", "replace")


def browser_facts(target, out):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    httpd, url = serve(target) if os.path.exists(target) else (None, target)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            ctx = b.new_context(viewport={"width": 390, "height": 664}, device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = ctx.new_page()
            pg.goto(url, wait_until="load", timeout=90000)
            pg.wait_for_timeout(3000)  # cookie bars, chat bubbles and rating widgets load late
            facts = pg.evaluate(FIRST)
            if out:
                os.makedirs(out, exist_ok=True)
                pg.screenshot(path=os.path.join(out, "first-screen.png"))
            b.close()
    finally:
        if httpd:
            httpd.shutdown()
    return facts


def static_facts(html):
    s = Static(); s.feed(html)
    ctas = [c.strip() for c, pos in s.ctas if pos < 80 and c.strip()]
    h1_full = s.h1_at is not None and s.h1_at + len(s.h1[0].split()) <= 80
    return {"text": " ".join(s.words[:80]), "h1": [h.strip() for h in s.h1], "h1_full": h1_full,
            "ctas": ctas, "cover": [], "imgs": s.imgs[:3], "viewport": s.viewport, "static": True}


def faults(html):
    out = []
    vis = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", vis)
    for rx, what in ((r"lorem ipsum", "lorem ipsum left in"), (r"\b(TODO|TBD|FIXME)\b", "TODO/TBD left in"),
                     (r"(this template|your headline here|your text here|placeholder text)", "template text left in"),
                     (r"[$€£]\s?0(\.00)?\b(?![.,]\d)", "placeholder price ($0)"), (r"[$€£]?\s?9[,.]?999\b", "placeholder price (9,999)"),
                     (r"[$€£]\s?XX\b", "placeholder price (XX)")):
        m = re.search(rx, text, re.I if what != "TODO/TBD left in" else 0)
        if m:
            out.append(f"{what}: {m.group(0)!r}")
    for blob in re.findall(r"<script[^>]+application/ld\+json[^>]*>(.*?)</script>", html, re.S | re.I):
        if "aggregateRating" in blob and not re.search(r"\breviews?\b", text, re.I):
            out.append("aggregateRating in JSON-LD but no reviews visible on the page")
    for m in sorted(set(re.findall(r"https?://(localhost[:/][^\"' ]*|[\w.-]+\.(?:webflow\.io|vercel\.app|netlify\.app|pages\.dev))", html))):
        out.append(f"link to a staging host: {m}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target"); ap.add_argument("--promise"); ap.add_argument("--out"); ap.add_argument("--static", action="store_true")
    a = ap.parse_args()
    html = fetch_html(a.target)
    f = None if a.static else browser_facts(a.target, a.out)
    if f is None:
        if not a.static:
            print("note: Playwright not installed, falling back to --static (pip install playwright && python -m playwright install chromium)")
        f = static_facts(html)
    res = {}
    if a.promise:
        ok = re.sub(r"\s+", " ", a.promise).lower() in re.sub(r"\s+", " ", f["text"]).lower()
        res["promise"] = ("PASS" if ok else "FAIL", f"{a.promise!r} {'is' if ok else 'is not'} on the first screen")
    else:
        res["promise"] = ("SKIP", "no --promise given (pass the ad's offer phrase)")
    if len(f["h1"]) != 1:
        res["headline"] = ("FAIL", f"{len(f['h1'])} H1 on the page")
    else:
        res["headline"] = ("PASS" if f["h1_full"] else "FAIL", f"{f['h1'][0]!r} {'fully on' if f['h1_full'] else 'not fully on'} the first screen")
    res["cta"] = ("PASS", f"{f['ctas']}") if f["ctas"] else ("FAIL", "no CTA-styled link or button on the first screen")
    proof = sorted(set(m.group(0) for m in re.finditer(PROOF_RX, f["text"], re.I)))
    res["proof"] = ("JUDGE", f"candidates: {proof}" if proof else "no rating, review count or logo text found on the first screen")
    res["covered"] = ("FAIL", f"{f['cover']}") if f["cover"] else ("PASS" if not f.get("static") else "SKIP",
                      "no overlay over 25%" if not f.get("static") else "needs the browser")
    big = f["imgs"][0] if f["imgs"] else None
    if not big:
        res["hero-bytes"] = ("PASS", "no image on the first screen")
    elif big["bytes"] is None:
        res["hero-bytes"] = ("SKIP", f"size of {big['src']} not measured")
    else:
        res["hero-bytes"] = ("PASS" if big["bytes"] < 1_000_000 else "FAIL", f"{big['src']} {big['bytes'] // 1024} KB")
    res["viewport"] = ("PASS", "present") if f["viewport"] else ("FAIL", "missing")

    mode = "static, first 80 words" if f.get("static") else "browser, 390x664"
    print(f"first screen ({mode}): {a.target}")
    for i, k in enumerate(["promise", "headline", "cta", "proof", "covered", "hero-bytes", "viewport"], 1):
        st, msg = res[k]
        print(f"  {i} {k:<11} {st:<5} {msg}")
    fl = faults(html)
    print(f"trust faults: {len(fl)}")
    for x in fl:
        print("  -", x)
    ranked = [k for k in ORDER if res[k][0] == "FAIL"]
    if res["proof"][0] == "JUDGE" and not proof:
        ranked.insert(ranked.index("headline") if "headline" in ranked else len(ranked), "proof")
    print("fix list:")
    n = 0
    for k in ranked:
        n += 1
        print(f"  {n}. {'[Fix first] ' if n == 1 else ''}{k}: {res[k][1]}. Why: {WHY[k]}.")
    for x in fl:
        n += 1
        print(f"  {n}. {'[Fix first] ' if n == 1 else ''}fault: {x}")
    if not n:
        print("  nothing to fix on the first screen; judge the proof candidates by eye")
    hard = [k for k in ranked if res[k][0] == "FAIL"]
    sys.exit(1 if hard or fl else 0)


if __name__ == "__main__":
    main()
