#!/usr/bin/env python3
"""QA screenshots of a local landing page at 1440 and 390, with the checks a person forgets.

Usage:
  python3 shot.py <site_root> <page.html[,page2.html]> <out_dir> [--overflow] [--no-shots]

Serves <site_root> on 127.0.0.1 (free port), opens each page with reduced motion, scrolls through it
so lazy images and reveal animations run, then reports per page and width:
  scrollWidth      OK, or OVERFLOW with the elements that stick out (always listed on overflow,
                   --overflow lists them every time)
  console errors   and failed requests (a missing font or image shows here)
  blank images     <img> that never loaded (naturalWidth 0), the usual cause is loading="lazy"
                   or a wrong path
Then saves full-page PNGs and slices (1800 px steps at 1440 downscaled by half, 2400 px at 390).
Exit 1 when any page overflows, logs an error, or has a blank image.

Needs Playwright and Pillow:  pip install playwright pillow && python -m playwright install chromium
"""
import argparse, asyncio, http.server, os, socket, sys, threading
from functools import partial

try:
    from playwright.async_api import async_playwright
except ImportError:
    sys.exit("shot.py needs Playwright: pip install playwright pillow && python -m playwright install chromium")

WIDE = """() => { const o = []; document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect();
  if (r.right > innerWidth + 2 && r.width > 0) o.push(e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\\s+/).join('.') : '') + ' width ' + Math.round(r.width) + ' right ' + Math.round(r.right)); });
  return o.slice(0, 12); }"""
BLANK = """() => [...document.images].filter(i => i.complete && i.naturalWidth === 0 || !i.complete).map(i => i.getAttribute('src'))"""



class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

def serve(root):
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    handler = partial(Quiet, directory=root)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


async def run(port, pages, out, over, shots):
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (1440, 390):
            ctx = await b.new_context(viewport={"width": w, "height": 900}, reduced_motion="reduce", device_scale_factor=1)
            pg = await ctx.new_page(); errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("requestfailed", lambda r: errs.append("request failed " + r.url.split(f":{port}", 1)[-1]))
            pg.on("response", lambda r: errs.append(f"HTTP {r.status} " + r.url.split(f':{port}', 1)[-1]) if r.status >= 400 else None)
            for name in pages:
                await pg.goto(f"http://127.0.0.1:{port}/{name}"); await pg.wait_for_timeout(800)
                h = await pg.evaluate("document.documentElement.scrollHeight"); y = 0
                while y < h:
                    await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(120); y += 700
                await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(400)
                sw = await pg.evaluate("document.documentElement.scrollWidth")
                blank = await pg.evaluate(BLANK)
                ok = sw <= w and not errs and not blank
                bad += 0 if ok else 1
                print(f"{name} {w}px  scrollWidth {sw} {'OK' if sw <= w else 'OVERFLOW'}  "
                      f"errors {len(errs)}  blank images {len(blank)}  {'PASS' if ok else 'FAIL'}")
                for e in errs[:6]:
                    print("    error:", e)
                for s in blank[:6]:
                    print("    blank image:", s)
                if over or sw > w:
                    for line in await pg.evaluate(WIDE):
                        print("    wide:", line)
                errs.clear()
                if shots:
                    fn = os.path.join(out, name.replace("/", "_").replace(".html", "") + f"-{w}.png")
                    await pg.screenshot(path=fn, full_page=True)
            await ctx.close()
        await b.close()
    return bad


def slice_all(out, pages):
    try:
        from PIL import Image
    except ImportError:
        print("note: Pillow not installed, slices skipped (pip install pillow)"); return
    Image.MAX_IMAGE_PIXELS = None
    for name in pages:
        for w in (1440, 390):
            n = os.path.join(out, name.replace("/", "_").replace(".html", "") + f"-{w}")
            im = Image.open(n + ".png"); W, H = im.size
            step = 1800 if W > 1000 else 2400
            for i, y in enumerate(range(0, H, step)):
                c = im.crop((0, y, W, min(H, y + step)))
                if W > 1000:
                    c = c.resize((W // 2, max(1, c.height // 2)))
                c.save(f"{n}-p{i}.png")
            print(f"{name} {w}px: {(H + step - 1) // step} slices, read every one")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root"); ap.add_argument("pages"); ap.add_argument("out")
    ap.add_argument("--overflow", action="store_true"); ap.add_argument("--no-shots", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    pages = [p.strip() for p in a.pages.split(",") if p.strip()]
    httpd, port = serve(a.root)
    try:
        bad = asyncio.run(run(port, pages, a.out, a.overflow, not a.no_shots))
    finally:
        httpd.shutdown()
    if not a.no_shots:
        slice_all(a.out, pages)
    print("shot: all green" if not bad else f"shot: {bad} page/width combination(s) failed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
