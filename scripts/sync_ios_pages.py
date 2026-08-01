#!/usr/bin/env python3
"""Mirror every app's GitHub Pages landing page into portfolio/docs/ios/<slug>/.

The app pages are authored in their own repos (see ~/ios/landing-pages/README.md).
GitHub Pages cannot proxy or rewrite paths, so serving them at
https://jackwallner.com/ios/<slug>/ means the files have to physically live in
this repo. This script clones each source repo shallowly and copies index.html
plus the transitive closure of the relative assets it references -- never the
whole repo, since some of these are full Xcode projects.

The pages already declare https://jackwallner.com/ios/<slug>/ as their canonical
URL, so nothing is rewritten here; the copy is byte-identical to the source.

Run locally with `python3 scripts/sync_ios_pages.py`; CI runs the same file.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# slug -> (repo, path inside the repo holding index.html)
# The slug is the public URL segment: https://jackwallner.com/ios/<slug>/
APPS = {
    "vitals": ("vitals", "docs"),
    "headaches": ("headaches", "docs"),
    "fitness-streaks": ("fitness-streaks", "docs"),
    "sober": ("sober", "docs"),
    "quitzyn": ("quitzyn", "docs"),
    "bond": ("bond", "docs"),
    "simpleglp": ("simpleglp", "docs"),
    "sports": ("sports", "docs"),
    "baseball": ("baseball", "docs"),
    "posture": ("posture", "docs"),
    "bridge": ("bridge", "docs"),
    "mahj": ("mahj", "docs"),
    "cribbage": ("cribbage", "docs"),
    "vo2max": ("vo2max", "docs"),
    "dreamcart": ("dreamcart", "docs"),
    "football": ("football", "docs"),
    # queasy publishes from its repo root, not /docs
    "queasy": ("queasy", "."),
}

ROOT = Path(__file__).resolve().parent.parent
DEST_ROOT = ROOT / "docs" / "ios"
ASSET_RE = re.compile(r'(?:href|src|content)="([^"]+)"')
SKIP_SCHEMES = ("http://", "https://", "//", "mailto:", "tel:", "data:", "#")
# `content="..."` is mostly meta-tag prose, so only values that look like a file
# with one of these extensions are treated as an asset to copy.
ASSET_EXT = (".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg",
             ".webp", ".ico", ".webmanifest", ".json", ".mp4", ".xml", ".txt")


def referenced(html: str) -> set[str]:
    """Relative asset paths referenced by an HTML document."""
    out = set()
    for raw in ASSET_RE.findall(html):
        if raw.startswith(SKIP_SCHEMES) or not raw.strip():
            continue
        path = raw.split("#")[0].split("?")[0].lstrip("./")
        if not path or ".." in path or " " in path:
            continue
        if path.lower().endswith(ASSET_EXT):
            out.add(path)
    return out


def copy_closure(src: Path, dest: Path) -> int:
    """Copy index.html and everything it (transitively) links to."""
    pending = ["index.html"]
    seen: set[str] = set()
    copied = 0
    while pending:
        rel = pending.pop()
        if rel in seen:
            continue
        seen.add(rel)
        source = src / rel
        if not source.is_file():
            print(f"    missing asset, skipped: {rel}")
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied += 1
        if rel.endswith(".html"):
            pending.extend(referenced(source.read_text(encoding="utf-8", errors="replace")))
    return copied


def main() -> int:
    only = sys.argv[1:]
    with tempfile.TemporaryDirectory() as tmp:
        for slug, (repo, sub) in APPS.items():
            if only and slug not in only:
                continue
            clone = Path(tmp) / repo
            subprocess.run(
                ["git", "clone", "--depth", "1", "--quiet",
                 f"https://github.com/jackwallner/{repo}.git", str(clone)],
                check=True,
            )
            src = clone / sub
            if not (src / "index.html").is_file():
                print(f"!! {slug}: no index.html in {repo}/{sub}")
                return 1
            dest = DEST_ROOT / slug
            if dest.exists():
                shutil.rmtree(dest)
            dest.mkdir(parents=True)
            n = copy_closure(src, dest)
            print(f"{slug:16} <- {repo}/{sub}  ({n} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
