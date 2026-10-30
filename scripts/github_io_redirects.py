#!/usr/bin/env python3
"""Add a crawler-visible redirect to the github.io copies of mirrored app pages.

Each app page is served twice: by its own repo's GitHub Pages at
jackwallner.github.io/<repo>/ and by the mirror at jackwallner.com/ios/<slug>/.
GitHub Pages cannot send a 301, and the existing JavaScript redirect is invisible
to crawlers that do not run scripts (Bing and ChatGPT search kept citing the
github.io copies). A 0-second meta refresh is the closest static equivalent; Bing
and Google treat it as a permanent redirect.

For every .html file under the given folders whose canonical points at
https://jackwallner.com/ and whose canonical URL is live, this inserts
`<meta http-equiv="refresh" content="0; url=<canonical>">` right after the
canonical tag. sync_ios_pages.py strips that line from the jackwallner.com
mirror, so only github.io redirects. Idempotent.

Usage: python3 scripts/github_io_redirects.py [--dry-run] <repo>/docs [...]
"""

import re
import sys
import urllib.request
from pathlib import Path

CANON_RE = re.compile(r'^([ \t]*)<link rel="canonical" href="(https://jackwallner\.com/[^"]*)">[^\n]*\n', re.M)
REFRESH_RE = re.compile(r'<meta http-equiv="refresh"')
SKIP_PARTS = {"build", "node_modules", "archive", ".build", "DerivedData"}


def is_live(url: str) -> bool:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "github-io-redirects"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status == 200
    except Exception:
        return False


def add_refresh(path: Path, dry_run: bool) -> str:
    text = path.read_text(encoding="utf-8")
    if REFRESH_RE.search(text):
        return "has refresh"
    m = CANON_RE.search(text)
    if not m:
        return "no jackwallner.com canonical"
    indent, url = m.group(1), m.group(2)
    if not is_live(url):
        return f"canonical not live: {url}"
    if not dry_run:
        line = f'{indent}<meta http-equiv="refresh" content="0; url={url}">\n'
        path.write_text(text[: m.end()] + line + text[m.end():], encoding="utf-8")
    return "added"


def main() -> int:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    folders = [Path(a) for a in args if a != "--dry-run"]
    if not folders:
        print(__doc__)
        return 2
    added = 0
    for folder in folders:
        for path in sorted(folder.rglob("*.html")):
            if SKIP_PARTS & set(path.relative_to(folder).parts):
                continue
            result = add_refresh(path, dry_run)
            added += result == "added"
            print(f"{result:30} {path}")
    print(f"{'would add' if dry_run else 'added'}: {added}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
