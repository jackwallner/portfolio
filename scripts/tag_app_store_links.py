"""Add App Store campaign tags (pt/ct/mt) to links to our own apps in a docs folder.

Usage: python3 tag_app_store_links.py <app repo>/docs <slug>. Idempotent; leaves
competitor links and JSON-LD URLs alone. Add new app IDs to OURS.
"""
import re
import sys
from pathlib import Path

PT = "128748779"
OURS = set("""6797089337 6820647074 6792930447 6790052126 6821025282 6806112259 6820644691 6761743504
6762074561 6804828001 6763945657 6786780495 6768514450 6787820106 6797089333 6791026407 6796911073
6796913722 6791235742 6784788496 6796913227 6770137909 6804828725 6803727074 6768869215 6796916172
6811133796 6815023447 6762699692 6770138156 6799785786 6768514177 6814953557 6805950103 6762168021
6823808045 6825448110""".split())
LINK = re.compile(r'href="(https://apps\.apple\.com/(?:[a-z]{2}/)?app/(?:[^/"?]+/)?id(\d+))(\?[^"#]*)?(#[^"]*)?"')


def ct_for(slug: str, rel: Path) -> str:
    stem = "-".join(rel.with_suffix("").parts)
    stem = "home" if stem == "index" else stem.replace("index", "").strip("-")
    return re.sub(r"[^a-z0-9-]", "", f"jw-{slug}-{stem}".lower())[:40].rstrip("-")


def tag(root: Path, slug: str) -> int:
    total = 0
    for f in sorted(root.rglob("*.html")):
        ct = ct_for(slug, f.relative_to(root))
        s = f.read_text()

        def sub(m: re.Match) -> str:
            if m.group(2) not in OURS:
                return m.group(0)
            return f'href="{m.group(1)}?pt={PT}&amp;ct={ct}&amp;mt=8{m.group(4) or ""}"'

        new, n = LINK.subn(sub, s)
        changed = sum(1 for a, b in zip(LINK.findall(s), LINK.findall(new)) if a != b)
        if new != s:
            f.write_text(new)
            total += changed
            print(f"  {f.relative_to(root)}: {changed} -> ct={ct}")
    return total


if __name__ == "__main__":
    root, slug = Path(sys.argv[1]), sys.argv[2]
    print(slug, tag(root, slug))
