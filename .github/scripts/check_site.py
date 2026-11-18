"""Check every page of the site before a recruiter finds a problem.

Two passes:
  1. Links (standard library only): every internal link, image and
     same-page anchor in every HTML file must point at something real.
  2. Browser (--browser, needs Playwright): every page is opened at phone
     and desktop widths. It must load, every image must render, the page
     must not scroll sideways, and the browser console must stay clean.

Run locally:  python3 .github/scripts/check_site.py
With browser: python3 .github/scripts/check_site.py --browser
"""
import argparse
import functools
import http.server
import socketserver
import sys
import threading
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".github", "node_modules"}
WIDTHS = {"phone": 390, "desktop": 1280}


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.refs.append((tag, attrs[key]))


def pages():
    return sorted(p for p in ROOT.rglob("*.html")
                  if not SKIP_DIRS & set(p.relative_to(ROOT).parts))


def parse(path):
    parser = Refs()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def check_links():
    problems = []
    for page in pages():
        found = parse(page)
        for tag, ref in found.refs:
            parts = urlsplit(ref)
            if parts.scheme or ref.startswith(("//", "mailto:", "tel:", "javascript:")):
                continue  # outside links are not checked (they rate-limit bots)
            where = f"{page.relative_to(ROOT)}: <{tag}> {ref}"
            if not parts.path:
                if parts.fragment and parts.fragment not in found.ids:
                    problems.append(f"{where} -> no element with that id")
                continue
            target = (ROOT / parts.path.lstrip("/") if parts.path.startswith("/")
                      else page.parent / unquote(parts.path)).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                problems.append(f"{where} -> file not found")
            elif parts.fragment and target.suffix == ".html":
                if parts.fragment not in parse(target).ids:
                    problems.append(f"{where} -> no element with that id")
    return problems


def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *a: None
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def check_browser(shots):
    from playwright.sync_api import sync_playwright

    problems = []
    server = serve()
    base = f"http://127.0.0.1:{server.server_address[1]}/"
    if shots:
        shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for name, width in WIDTHS.items():
            context = browser.new_context(viewport={"width": width, "height": 900})
            for page_path in pages():
                rel = page_path.relative_to(ROOT).as_posix()
                url = base + rel.removesuffix("index.html")
                tab = context.new_page()
                errors = []
                tab.on("pageerror", lambda e: errors.append(str(e)))
                tab.on("console", lambda m: m.type == "error" and errors.append(m.text))
                where = f"{rel} ({name}, {width}px)"
                response = tab.goto(url, wait_until="networkidle")
                if not response or not response.ok:
                    problems.append(f"{where}: page did not load")
                    tab.close()
                    continue
                tab.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                tab.wait_for_timeout(300)
                broken = tab.evaluate("""() => [...document.images]
                    .filter(i => !i.complete || i.naturalWidth === 0)
                    .map(i => i.getAttribute('src'))""")
                problems += [f"{where}: image did not render: {src}" for src in broken]
                overflow = tab.evaluate(
                    "() => document.documentElement.scrollWidth - window.innerWidth")
                if overflow > 1:
                    problems.append(f"{where}: page scrolls sideways by {overflow}px")
                problems += [f"{where}: console error: {e}" for e in errors]
                if shots:
                    tab.screenshot(path=str(shots / f"{name}-{rel.replace('/', '_')}.png"),
                                   full_page=True)
                tab.close()
            context.close()
        browser.close()
    server.shutdown()
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--browser", action="store_true", help="also open every page in Chromium")
    ap.add_argument("--screenshots", type=Path, help="folder for full-page screenshots")
    args = ap.parse_args()

    print(f"Checking {len(pages())} pages")
    problems = check_links()
    if args.browser:
        problems += check_browser(args.screenshots)
    for p in problems:
        print(f"  FAIL  {p}")
    print("All checks passed" if not problems else f"{len(problems)} problem(s) found")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
