#!/usr/bin/env python3
"""Submit every URL in docs/sitemap.xml to IndexNow (Bing, Yandex, Seznam, Naver).

Bing's index feeds ChatGPT search and Copilot, so this is the fastest way to get
a changed page in front of AI answer engines. Google ignores IndexNow; use
Search Console for it. The key file docs/<key>.txt must already be live.

Run after a deploy: `python3 scripts/indexnow.py [--dry-run] [url ...]` (default: whole
sitemap). --dry-run checks the live key file and prints what would be sent.
"""

import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

DOCS = Path(__file__).resolve().parent.parent / "docs"
HOST = "jackwallner.com"


def key() -> str:
    for f in DOCS.glob("*.txt"):
        text = f.read_text().strip()
        if re.fullmatch(r"[0-9a-f]{32}", f.stem) and text == f.stem:
            return text
    raise SystemExit("no IndexNow key file in docs/")


def main() -> int:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    urls = [a for a in args if a != "--dry-run"]
    urls = urls or re.findall(r"<loc>(.*?)</loc>", (DOCS / "sitemap.xml").read_text())
    k = key()
    if dry_run:
        with urlopen(f"https://{HOST}/{k}.txt", timeout=20) as r:
            live = r.read().decode().strip()
        print(f"key file {'live and matching' if live == k else 'MISMATCH: ' + live}")
        print(f"would submit {len(urls)} urls, first: {urls[:3]}")
        return 0 if live == k else 1
    body = json.dumps({"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt",
                       "urlList": urls}).encode()
    req = Request("https://api.indexnow.org/indexnow", data=body,
                  headers={"Content-Type": "application/json; charset=utf-8"})
    with urlopen(req, timeout=20) as r:
        print(f"IndexNow {r.status}: submitted {len(urls)} urls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
