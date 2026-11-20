#!/usr/bin/env python3
"""Reverse a reference landing page: full-page screenshots at 1440 and 390, a 390x664 first-screen
shot, readable slices, and a JSON file with design tokens and the copy of every section.

Usage:
  python3 recon.py <url | local .html file | local folder> <out_dir> [--name ref] [--json-only]

  A local file or folder is served on 127.0.0.1 on a free port, so the example works offline.
  --json-only   skip the PNG files (tokens and sections only)

Writes:
  <name>-recon.json         tokens (fonts, colors, backgrounds, radii), sections (top, height,
                            headings, leaf text), title, description, H1, first-screen text and CTAs
  <name>-1440.png, <name>-390.png, <name>-first-screen.png
  <name>-<w>-pN.png         slices: 1800 px steps at 1440 (downscaled by half), 2400 px at 390

Read every slice after it runs. The JSON tells you what the page says; the slices tell you how.
Needs Playwright and Pillow:  pip install playwright pillow && python -m playwright install chromium
"""
import argparse, asyncio, http.server, json, os, socket, sys, threading
from functools import partial

try:
    from playwright.async_api import async_playwright
except ImportError:
    sys.exit("recon.py needs Playwright: pip install playwright pillow && python -m playwright install chromium")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

EXTRACT = r"""
() => {
  const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const clean = t => t.trim().replace(/\s+/g, ' ');
  const fonts = {}, colors = {}, bgs = {}, radii = {};
  for (const el of document.querySelectorAll('body *')) {
    if (!vis(el)) continue;
    const s = getComputedStyle(el);
    if ([...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) {
      const k = s.fontFamily.split(',')[0] + ' | ' + s.fontSize + ' | ' + s.fontWeight + ' | lh ' + s.lineHeight;
      fonts[k] = (fonts[k] || 0) + 1; colors[s.color] = (colors[s.color] || 0) + 1;
    }
    if (s.backgroundColor !== 'rgba(0, 0, 0, 0)') bgs[s.backgroundColor] = (bgs[s.backgroundColor] || 0) + 1;
    if (s.borderRadius !== '0px') radii[s.borderRadius] = (radii[s.borderRadius] || 0) + 1;
  }
  const top = (o, n) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n);
  const out = {tokens: {fonts: top(fonts, 20), colors: top(colors, 12), backgrounds: top(bgs, 12),
               radii: top(radii, 10), body_background: getComputedStyle(document.body).backgroundColor},
               sections: []};
  const root = document.querySelector('main') || document.body;
  const blocks = [...root.querySelectorAll('header, section, main > div, footer')]
    .filter(e => vis(e) && e.getBoundingClientRect().height > 120);
  const kept = [];
  for (const b of blocks) {
    if (kept.some(p => p.contains(b))) continue;
    kept.push(b);
    const r = b.getBoundingClientRect();
    out.sections.push({
      top: Math.round(r.top + scrollY), height: Math.round(r.height),
      tag: b.tagName.toLowerCase(), id: b.id || null,
      headings: [...b.querySelectorAll('h1,h2,h3')].filter(vis).map(h => h.tagName + ': ' + clean(h.innerText)).slice(0, 20),
      text: [...new Set([...b.querySelectorAll('p, li, a, button, span, figcaption')]
        .filter(e => vis(e) && e.children.length === 0 && e.innerText.trim().length > 2)
        .map(e => clean(e.innerText)))].slice(0, 50),
      media: {img: b.querySelectorAll('img').length, video: b.querySelectorAll('video').length,
              svg: b.querySelectorAll('svg').length}
    });
  }
  const h1 = document.querySelector('h1');
  out.title = document.title;
  out.description = (document.querySelector('meta[name=description]') || {}).content || null;
  out.h1 = h1 ? clean(h1.innerText) : null;
  return out;
}
"""

FIRST = r"""
() => {
  const H = innerHeight, W = innerWidth;
  const inView = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && r.top < H && r.bottom > 0 && r.left < W && s.visibility !== 'hidden'; };
  const words = [];
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walk.nextNode()) {
    const n = walk.currentNode, p = n.parentElement;
    if (!p || !n.textContent.trim() || ['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(p.tagName)) continue;
    if (inView(p)) words.push(n.textContent.trim().replace(/\s+/g, ' '));
  }
  const ctas = [...document.querySelectorAll('a, button')].filter(inView)
    .map(e => e.innerText.trim().replace(/\s+/g, ' ')).filter(t => t && t.length < 60);
  return {first_screen_text: words.join(' | '), first_screen_ctas: [...new Set(ctas)]};
}
"""



class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

def serve(path):
    root = path if os.path.isdir(path) else os.path.dirname(os.path.abspath(path))
    page = "" if os.path.isdir(path) else os.path.basename(path)
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    handler = partial(Quiet, directory=root)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{port}/{page}"


async def scroll_through(pg, step=600, pause=300):
    h = await pg.evaluate("document.documentElement.scrollHeight"); y = 0
    while y < h:  # lazy blocks and reveal observers only render once scrolled into view
        await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(pause); y += step
        h = await pg.evaluate("document.documentElement.scrollHeight")
    await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(800)


async def run(url, out, name, shots):
    data = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (1440, 390):
            ctx = await b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1, user_agent=UA)
            pg = await ctx.new_page()
            await pg.goto(url, wait_until="domcontentloaded", timeout=90000)
            await pg.wait_for_timeout(2000)
            await scroll_through(pg)
            if shots:
                await pg.screenshot(path=os.path.join(out, f"{name}-{w}.png"), full_page=True)
            if w == 1440:
                data = await pg.evaluate(EXTRACT)
            await ctx.close()
        ctx = await b.new_context(viewport={"width": 390, "height": 664}, device_scale_factor=1, user_agent=UA)
        pg = await ctx.new_page()
        await pg.goto(url, wait_until="domcontentloaded", timeout=90000)
        await pg.wait_for_timeout(2000)
        data.update(await pg.evaluate(FIRST))
        if shots:
            await pg.screenshot(path=os.path.join(out, f"{name}-first-screen.png"))
        await ctx.close()
        await b.close()
    return data


def slice_shots(out, name):
    try:
        from PIL import Image
    except ImportError:
        print("note: Pillow not installed, slices skipped (pip install pillow)"); return
    Image.MAX_IMAGE_PIXELS = None
    for w in (1440, 390):
        im = Image.open(os.path.join(out, f"{name}-{w}.png")); W, H = im.size
        step = 1800 if W > 1000 else 2400
        n = 0
        for i, y in enumerate(range(0, H, step)):
            c = im.crop((0, y, W, min(H, y + step)))
            if W > 1000:
                c = c.resize((W // 2, max(1, c.height // 2)))
            c.save(os.path.join(out, f"{name}-{w}-p{i}.png")); n += 1
        print(f"{w}px: page height {H}, {n} slices")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target"); ap.add_argument("out")
    ap.add_argument("--name", default="ref"); ap.add_argument("--json-only", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    httpd, url = (None, a.target)
    if os.path.exists(a.target):
        httpd, url = serve(a.target)
    try:
        data = asyncio.run(run(url, a.out, a.name, not a.json_only))
    finally:
        if httpd:
            httpd.shutdown()
    data["source"] = a.target if not httpd else os.path.basename(os.path.abspath(a.target))
    with open(os.path.join(a.out, f"{a.name}-recon.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"title: {data.get('title')}")
    print(f"h1: {data.get('h1')}")
    print(f"sections: {len(data.get('sections', []))}")
    for i, s in enumerate(data.get("sections", []), 1):
        head = s["headings"][0] if s["headings"] else "(no heading)"
        m = s["media"]
        print(f"  {i:>2}. {s['tag']:<7} h{s['height']:<5} {head[:60]:<60} img {m['img']} video {m['video']} svg {m['svg']}")
    print(f"first-screen CTAs (390x664): {data.get('first_screen_ctas')}")
    if not a.json_only:
        slice_shots(a.out, a.name)
    print(f"wrote {os.path.join(a.out, a.name + '-recon.json')}")


if __name__ == "__main__":
    main()
