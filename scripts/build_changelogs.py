#!/usr/bin/env python3
"""Write docs/ios/<slug>/changelog.html (and its .html.md twin) for every App Store app.

Each page lists the app's live versions, newest first: version, release date,
and that version's What's New text. A page that changes with every release
gives search engines a reason to recrawl the app's folder.

Data lives in data/changelogs.json ({slug: [{version, date, notes}]}, newest
first). It was seeded on 2026-11-18 from App Store Connect (every appStoreVersion
and its en-US whatsNew), with release dates from the public App Store listing.
ASC has no release-date field, and the listing only shows the latest 25
versions, so the ten oldest Vitals versions are dated by the first day each one
appeared in ASC's daily sales report.

New releases arrive without credentials: the iTunes lookup API gives each app's
current version, its release time and its notes, and the public listing fills
any versions a run missed. Both are public, so this runs in the build-site
workflow with no secrets. Known versions are never rewritten or removed.

The layout is taken from each app's own index.html (its head, nav and footer),
which scripts/sync_ios_pages.py mirrors from the app's repo. The sync calls
render() after every mirror, so a page refresh never drops the changelog, and
inject_link() adds the Changelog link to the app page's footer.

Usage:
  python3 scripts/build_changelogs.py            fetch new versions, render all
  python3 scripts/build_changelogs.py --offline  render from data only
  python3 scripts/build_changelogs.py vitals     limit to some slugs
"""

from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PROJECTS = DOCS / "projects.json"
DATA = ROOT / "data" / "changelogs.json"
SITE = "https://jackwallner.com/"
PACIFIC = ZoneInfo("America/Los_Angeles")
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio changelog build)"}
PAGE = "changelog.html"
LINK = f'<a href="{PAGE}">Changelog</a>'
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "source", "track", "wbr"}

STYLE = """    <style>
      .changelog { max-width: 720px; margin: 0 auto; padding: 48px 24px 24px; text-align: left; }
      .changelog h1 { margin: 0 0 32px; }
      .changelog .release { padding: 24px 0; border-top: 1px solid rgba(127, 127, 127, 0.25); }
      .changelog .release h2 { margin: 0; font-size: 1.15em; }
      .changelog .release time { display: block; margin: 4px 0 12px; opacity: 0.7; font-size: 0.9em; }
      .changelog .release p, .changelog .release ul { margin: 0 0 10px; line-height: 1.55; }
      .changelog .release ul { padding-left: 20px; }
    </style>
"""


# ---------------------------------------------------------------- data

def load() -> dict[str, list[dict]]:
    return json.loads(DATA.read_text()) if DATA.is_file() else {}


def save(data: dict[str, list[dict]]) -> None:
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def apps(projects: list[dict]) -> list[tuple[str, str, dict]]:
    """(slug, App Store id, project) for every listed app with a page under ios/."""
    out = []
    for p in projects:
        m = re.search(r"/id(\d+)", p.get("appStore") or "")
        if m and p.get("slug") and (p.get("page") or "").startswith("ios/"):
            out.append((p["slug"], m.group(1), p))
    return out


def short_name(project: dict) -> str:
    """The app name without the App Store subtitle ("Total Calories - Daily Tracker")."""
    return re.split(r":| - ", project["name"])[0].strip()


def vkey(version: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", version))


def ordered(versions: list[dict]) -> list[dict]:
    return sorted(versions, key=lambda v: (v["date"], vkey(v["version"])), reverse=True)


def pacific_day(stamp: str) -> str:
    """ISO 8601 ("2026-11-05T16:07:37Z") or JS ("Tue Nov 17 2026 22:38:52 GMT+0000")."""
    m = re.match(r"\w{3} (\w{3} \d{1,2} \d{4} \d\d:\d\d:\d\d) GMT", stamp)
    if m:
        moment = datetime.strptime(m.group(1), "%b %d %Y %H:%M:%S").replace(tzinfo=timezone.utc)
    else:
        moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    return moment.astimezone(PACIFIC).date().isoformat()


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
        return r.read()


def lookup(ids: list[str]) -> dict[str, dict]:
    url = f"https://itunes.apple.com/lookup?id={','.join(ids)}&country=us&entity=software"
    results = json.loads(fetch(url)).get("results", [])
    return {str(r["trackId"]): r for r in results if r.get("trackId")}


def listing_history(app_id: str) -> list[dict]:
    """Versions on the public App Store listing (Apple shows the latest 25)."""
    page = fetch(f"https://apps.apple.com/us/app/id{app_id}").decode("utf-8", "replace")
    m = re.search(r'id="serialized-server-data">(.*?)</script>', page, re.S)
    if not m:
        return []

    def walk(node):
        if isinstance(node, dict):
            if node.get("page") == "versionHistory" and isinstance(node.get("pageData"), dict):
                yield node["pageData"]
            for value in node.values():
                yield from walk(value)
        elif isinstance(node, list):
            for value in node:
                yield from walk(value)

    for data in walk(json.loads(m.group(1))):
        items = [i for shelf in data.get("shelves", []) for i in shelf.get("items", [])]
        return [{"version": i["primarySubtitle"].removeprefix("Version ").strip(),
                 "date": pacific_day(i["secondarySubtitle"]),
                 "notes": (i.get("text") or "").strip()}
                for i in items if i.get("primarySubtitle") and i.get("secondarySubtitle")]
    return []


def update(data: dict[str, list[dict]], projects: list[dict], only: list[str]) -> list[str]:
    """Add versions released since the last run. Returns "slug version" for each."""
    targets = [a for a in apps(projects) if not only or a[0] in only]
    try:
        current = lookup([app_id for _, app_id, _ in targets])
    except (OSError, ValueError) as err:
        print(f"lookup failed, keeping known versions: {err}")
        return []
    added = []
    for slug, app_id, _ in targets:
        versions = data.setdefault(slug, [])
        known = {v["version"] for v in versions}
        live = current.get(app_id)
        if versions and (not live or live.get("version") in known):
            continue
        try:
            found = listing_history(app_id)
        except (OSError, ValueError) as err:
            print(f"  {slug}: listing unreadable ({err})")
            found = []
        if live and live.get("version") and live.get("currentVersionReleaseDate"):
            found.append({"version": live["version"],
                          "date": pacific_day(live["currentVersionReleaseDate"]),
                          "notes": (live.get("releaseNotes") or "").strip()})
        for v in found:
            if v["version"] not in known:
                versions.append(v)
                known.add(v["version"])
                added.append(f"{slug} {v['version']}")
        data[slug] = ordered(versions)
    return added


# ---------------------------------------------------------------- page layout

class Outline(HTMLParser):
    """Element spans of an HTML document: tag, attrs, start, end of open tag, end."""

    def __init__(self, text: str) -> None:
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = [0]
        for line in text.splitlines(keepends=True):
            self.lines.append(self.lines[-1] + len(line))
        self.elements: list[dict] = []
        self.stack: list[dict] = []
        self.feed(text)
        self.close()
        for el in self.stack:
            el["end"] = len(text)

    def pos(self) -> int:
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        start = self.pos()
        el = {"tag": tag, "attrs": dict(attrs), "start": start,
              "open_end": start + len(self.get_starttag_text() or ""),
              "end": None, "parent": self.stack[-1] if self.stack else None}
        self.elements.append(el)
        if tag in VOID:
            el["end"] = el["open_end"]
        else:
            self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1]["tag"] == tag and self.stack[-1]["end"] is None:
            el = self.stack.pop()
            el["end"] = el["open_end"]

    def handle_endtag(self, tag):
        if not any(el["tag"] == tag for el in self.stack):
            return
        end = self.text.find(">", self.pos()) + 1
        while self.stack:
            el = self.stack.pop()
            el["end"] = end
            if el["tag"] == tag:
                break


def frame(index: str) -> tuple[str, str, str]:
    """Split an app page into (head, body up to the content, footer to the end)."""
    outline = Outline(index)
    els = outline.elements
    body = next(el for el in els if el["tag"] == "body")
    footer = [el for el in els if el["tag"] == "footer"][-1]
    cursor = body["open_end"]
    parent = body
    while True:
        children = [el for el in els if el["parent"] is parent and el["start"] >= cursor]
        if not children:
            break
        child = children[0]
        inner = index[child["start"]:child["end"]]
        if child["tag"] in ("script", "noscript", "style") or (
                child["tag"] in ("nav", "header") and "<h1" not in inner):
            cursor = child["end"]
            continue
        if child["tag"] in ("div", "main") and child["end"] > footer["start"]:
            cursor = child["open_end"]
            parent = child
            continue
        break
    head_end = index.index("</head>")
    return index[:head_end], index[body["start"]:cursor], index[footer["start"]:]


def set_attr(text: str, pattern: str, value: str) -> str:
    """Replace the content/href of the first tag matching `pattern`."""
    def swap(m):
        return re.sub(r'(content|href)="[^"]*"', lambda a: f'{a.group(1)}="{value}"', m.group(0), count=1)
    return re.sub(pattern, swap, text, count=1)


def human(day: str) -> str:
    d = date.fromisoformat(day)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def clean(notes: str) -> str:
    """House style drops em dashes, including in quoted What's New copy."""
    return re.sub(r"\s*\u2014\s*", ", ", notes).strip()


BULLET = re.compile(r"^\s*(?:[-*\u2022\u2013]|\d+\.)\s+")


def notes_html(notes: str) -> str:
    notes = clean(notes)
    if not notes:
        return "        <p>First release on the App Store.</p>\n"
    out = []
    for block in re.split(r"\n\s*\n", notes):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        para: list[str] = []
        items: list[str] = []

        def flush():
            if para:
                out.append("        <p>" + "<br>".join(html.escape(x) for x in para) + "</p>")
                para.clear()
            if items:
                out.append("        <ul>\n" + "\n".join(
                    f"          <li>{html.escape(x)}</li>" for x in items) + "\n        </ul>")
                items.clear()

        for line in lines:
            if BULLET.match(line):
                if para:
                    flush()
                items.append(BULLET.sub("", line))
            else:
                if items:
                    flush()
                para.append(line)
        flush()
    return "\n".join(out) + "\n"


def page(project: dict, slug: str, versions: list[dict], index: str) -> str:
    name = short_name(project)
    url = f"{SITE}ios/{slug}/{PAGE}"
    app_url = f"{SITE}ios/{slug}/"
    latest = versions[0]
    title = f"{name} Changelog: Every Update and Release Date"
    desc = (f"Every {name} update, newest first. Version {latest['version']} "
            f"was released {human(latest['date'])}.")
    head, opening, closing = frame(index)

    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", head, count=1, flags=re.S)
    head = re.sub(r'[ \t]*<script type="application/ld\+json">.*?</script>\n?', "", head, flags=re.S)
    head = re.sub(r'[ \t]*<link rel="(?:alternate|preload)"[^>]*>\n?', "", head)
    head = re.sub(r'[ \t]*<meta property="og:video[^>]*>\n?', "", head)
    e = html.escape
    head = set_attr(head, r'<meta\s+name="description"[^>]*>', e(desc))
    head = set_attr(head, r'<link\s+rel="canonical"[^>]*>', url)
    head = set_attr(head, r'<meta\s+property="og:url"[^>]*>', url)
    head = set_attr(head, r'<meta\s+property="og:title"[^>]*>', e(title))
    head = set_attr(head, r'<meta\s+property="og:description"[^>]*>', e(desc))
    head = set_attr(head, r'<meta\s+name="twitter:title"[^>]*>', e(title))
    head = set_attr(head, r'<meta\s+name="twitter:description"[^>]*>', e(desc))
    jsonld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": url,
        "dateModified": latest["date"],
        "about": {"@type": "MobileApplication", "name": project["name"], "url": app_url,
                  "operatingSystem": "iOS", "softwareVersion": latest["version"],
                  "installUrl": project["appStore"]},
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": name, "item": app_url},
            {"@type": "ListItem", "position": 2, "name": "Changelog", "item": url}]},
    }
    ld = json.dumps(jsonld, indent=2, ensure_ascii=False).replace("</", "<\\/")
    head += f'    <script type="application/ld+json">\n{ld}\n    </script>\n{STYLE}'

    closing = re.sub(r'<time datetime="[^"]*" data-updated>[^<]*</time>',
                     f'<time datetime="{latest["date"]}" data-updated>{human(latest["date"])}</time>',
                     closing, count=1)
    tag = "section" if "<main" in opening else "main"
    back = "" if 'href="./"' in opening else f'      <p><a href="./">{e(name)}</a></p>\n'
    releases = "".join(
        f'      <article class="release" id="v{e(v["version"])}">\n'
        f'        <h2>Version {e(v["version"])}</h2>\n'
        f'        <time datetime="{v["date"]}">{human(v["date"])}</time>\n'
        f'{notes_html(v["notes"])}'
        f'      </article>\n'
        for v in versions)
    content = (f'\n    <{tag} class="changelog">\n{back}'
               f'      <h1>{e(name)} changelog</h1>\n{releases}    </{tag}>\n\n    ')
    return head + "</head>\n" + opening.rstrip() + "\n" + content + closing


def markdown(project: dict, slug: str, versions: list[dict]) -> str:
    name = short_name(project)
    lines = [f"# {name} changelog", "",
             f"> Every {name} update, newest first.", "",
             f"Web page: {SITE}ios/{slug}/{PAGE}", ""]
    for v in versions:
        lines += [f"## Version {v['version']} ({human(v['date'])})", "",
                  clean(v["notes"]) or "First release on the App Store.", ""]
    return "\n".join(lines)


def inject_link(index: str) -> str:
    """Add a Changelog link to the app page's footer, beside Support or Privacy."""
    if f'href="{PAGE}"' in index:
        return index
    start = index.rfind("<footer")
    end = index.find("</footer>", start)
    if start < 0 or end < 0:
        return index
    footer = index[start:end]
    anchors = list(re.finditer(r"<a\b[^>]*>.*?</a>", footer, re.S))
    if not anchors:
        return index
    pick = next((a for key in ("support", "privacy", "terms") for a in anchors
                 if key in a.group(0).lower()), anchors[-1])
    i = anchors.index(pick)
    if i + 1 < len(anchors):
        sep = footer[pick.end():anchors[i + 1].start()]
        insert = f"{sep}{LINK}"
    elif i > 0:
        insert = f"{footer[anchors[i - 1].end():pick.start()]}{LINK}"
    else:
        insert = f" {LINK}"
    pos = start + pick.end()
    return index[:pos] + insert + index[pos:]


def latest_date(slug: str, data: dict | None = None) -> str | None:
    versions = (data or load()).get(slug) or []
    return versions[0]["date"] if versions else None


def render(slug: str, data: dict | None = None, projects: list[dict] | None = None) -> bool:
    """Write one app's changelog pages and footer link. False when there is no data."""
    data = data if data is not None else load()
    projects = projects if projects is not None else json.loads(PROJECTS.read_text())
    project = next((p for s, _, p in apps(projects) if s == slug), None)
    versions = data.get(slug)
    folder = DOCS / "ios" / slug
    if not project or not versions or not (folder / "index.html").is_file():
        return False
    index_path = folder / "index.html"
    index = index_path.read_text(encoding="utf-8")
    linked = inject_link(index)
    if linked != index:
        index_path.write_text(linked, encoding="utf-8")
    write(folder / PAGE, page(project, slug, versions, linked))
    write(folder / f"{PAGE}.md", markdown(project, slug, versions))
    return True


def write(path: Path, text: str) -> None:
    if not path.is_file() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")


def refresh(projects: list[dict] | None = None, offline: bool = False,
            only: list[str] | None = None) -> int:
    """Fetch new versions (unless offline) and render every page. Returns pages written."""
    projects = projects if projects is not None else json.loads(PROJECTS.read_text())
    data = load()
    if not offline:
        added = update(data, projects, only or [])
        if added:
            save(data)
            print("new versions: " + ", ".join(added))
    slugs = [s for s, _, _ in apps(projects) if not only or s in only]
    return sum(render(s, data, projects) for s in slugs)


def main() -> int:
    args = sys.argv[1:]
    offline = "--offline" in args
    only = [a for a in args if not a.startswith("--")]
    n = refresh(offline=offline, only=only)
    print(f"wrote {n} changelog pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
