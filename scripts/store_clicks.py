"""Add the App Store tap counter (docs/clicks.js) to pages with App Store links.

App repos push their own pages here, so build_site.py and sync_ios_pages.py both
run this over what they publish rather than each page generator adding the tag.
"""

from __future__ import annotations

from pathlib import Path

TAG = '<script src="/clicks.js" defer></script>'


def tag(text: str) -> str:
    """The page with the counter script before </body>, if it links to the App Store."""
    if "apps.apple.com" not in text or "/clicks.js" in text or "</body>" not in text:
        return text
    head, _, tail = text.rpartition("</body>")
    return f"{head}{TAG}\n</body>{tail}"


def tag_tree(root: Path) -> int:
    """Tag every HTML page under root; returns how many changed."""
    changed = 0
    for page in root.rglob("*.html"):
        text = page.read_text(encoding="utf-8", errors="replace")
        tagged = tag(text)
        if tagged != text:
            page.write_text(tagged, encoding="utf-8")
            changed += 1
    return changed
