#!/usr/bin/env python3
"""Generate the portfolio's index pages from docs/projects.json.

docs/projects.json is the single source of truth for every project: name,
status, description, tech, and links. Before this script existed the same list
was maintained by hand in three places (index.html, ios/index.html, and a
CURATED array in script.js), which had already drifted into conflicting names,
statuses, and descriptions.

Generated files, both fully static so the pages need no JavaScript to render:
  docs/index.html     selected work + the full project table
  docs/ios/index.html the App Store catalogue, grouped by category

Run with `python3 scripts/build_site.py`; CI runs the same file.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = DOCS / "projects.json"

EMAIL = "jackwallner@gmail.com"
GITHUB = "https://github.com/jackwallner"
LINKEDIN = "https://www.linkedin.com/in/wallnerjack/"

SITE = "https://jackwallner.com/"
OG_IMAGE = SITE + "assets/profile.png"
APPLE_PROVIDER_TOKEN = "128748779"
APPLE_DEVELOPER_ID = "1891233967"
APPLE_LOOKUP_URL = "https://itunes.apple.com/lookup"
CONTRIBUTION_CHART = DOCS / "assets" / "github-contributions.svg"
ASSETS = DOCS / "assets"
THUMBS = ASSETS / "thumbs"
# Icons render at 32px and the avatar at 40px; 3x covers every screen density.
THUMB_PX = 120

# Filter chips on the home table: label -> group key in projects.json.
FILTERS = [("All", "all"), ("iOS apps", "ios"), ("Web", "web"), ("Tools", "tools")]

# Order the iOS catalogue's category sections.
CATEGORY_ORDER = [
    "Health & body",
    "Habits & recovery",
    "Card & tile games",
    "Sports",
    "Family & life admin",
    "Play",
]


class ContributionSummaryParser(HTMLParser):
    """Extract the official total and daily levels from GitHub's profile fragment."""

    def __init__(self) -> None:
        super().__init__()
        self.in_summary = False
        self.parts: list[str] = []
        self.days: list[dict[str, str]] = []
        self.tooltips: dict[str, str] = {}
        self.active_tooltip: str | None = None
        self.tooltip_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "h2" and attributes.get("id") == "js-contribution-activity-description":
            self.in_summary = True
        if tag == "td" and "ContributionCalendar-day" in (attributes.get("class") or ""):
            day = attributes.get("data-date")
            level = attributes.get("data-level")
            cell_id = attributes.get("id")
            if day and level and cell_id:
                self.days.append({"date": day, "level": level, "id": cell_id})
        if tag == "tool-tip" and attributes.get("for", "").startswith("contribution-day-component-"):
            self.active_tooltip = attributes["for"]
            self.tooltip_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self.in_summary:
            self.in_summary = False
        if tag == "tool-tip" and self.active_tooltip:
            self.tooltips[self.active_tooltip] = " ".join(" ".join(self.tooltip_parts).split())
            self.active_tooltip = None

    def handle_data(self, data: str) -> None:
        if self.in_summary:
            self.parts.append(data)
        if self.active_tooltip:
            self.tooltip_parts.append(data)


def github_contribution_data() -> tuple[str | None, list[dict[str, str]]]:
    request = Request(
        "https://github.com/users/jackwallner/contributions",
        headers={"User-Agent": "jackwallner-portfolio-build"},
    )
    try:
        with urlopen(request, timeout=10) as response:
            parser = ContributionSummaryParser()
            parser.feed(response.read().decode("utf-8"))
    except (OSError, UnicodeDecodeError):
        return None, []

    summary = " ".join(" ".join(parser.parts).split())
    match = re.search(r"([\d,]+) contributions in the last year", summary, re.IGNORECASE)
    total = None
    if match:
        total = f"{int(match.group(1).replace(',', '')):,} contributions in the last year"

    days = []
    for day in parser.days:
        try:
            parsed_date = date.fromisoformat(day["date"])
        except ValueError:
            continue
        days.append({
            **day,
            "title": parser.tooltips.get(
                day["id"],
                f"{parsed_date.strftime('%A, %B')} {parsed_date.day}, {parsed_date.year}: "
                f"contribution level {day['level']}",
            ),
        })
    return total, days


def contribution_chart_svg(days: list[dict[str, str]]) -> str:
    """Render GitHub's public daily contribution levels as an inline SVG chart."""
    if not days:
        return ""

    palette = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
    cell = 11
    step = 14
    left = 30
    top = 22
    ordered = sorted(days, key=lambda item: item["date"])
    start = date.fromisoformat(ordered[0]["date"])
    start_sunday = start - timedelta(days=(start.weekday() + 1) % 7)
    end = date.fromisoformat(ordered[-1]["date"])
    weeks = (end - start_sunday).days // 7 + 1
    width = left + weeks * step + 36
    height = top + 7 * step + 22

    labels = []
    squares = []
    previous_month = None
    for day in ordered:
        current = date.fromisoformat(day["date"])
        week = (current - start_sunday).days // 7
        weekday = (current.weekday() + 1) % 7
        x = left + week * step
        y = top + weekday * step
        if current.day == 1 and current.month != previous_month:
            labels.append(
                f'<text class="month-label" x="{x}" y="13" fill="#777" font-size="11">'
                f'{current.strftime("%b")}</text>'
            )
        previous_month = current.month
        level = min(max(int(day["level"]), 0), len(palette) - 1)
        squares.append(
            f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" '
            f'fill="{palette[level]}"><title>{e(day["title"])}</title></rect>'
        )

    weekday_labels = "".join(
        f'<text class="weekday-label" x="0" y="{top + row * step + 9}" '
        f'fill="#777" font-size="10">{label}</text>'
        for row, label in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )
    legend_start = max(left, width - 154)
    legend = [
        f'<text class="legend-label" x="{legend_start}" y="{height - 3}" '
        'fill="#777" font-size="10">Less</text>'
    ]
    for level, color in enumerate(palette):
        x = legend_start + 35 + level * step
        legend.append(
            f'<rect class="legend-cell" x="{x}" y="{height - 13}" width="11" height="11" '
            f'rx="2" fill="{color}" />'
        )
    legend.append(
        f'<text class="legend-label" x="{legend_start + 35 + len(palette) * step + 2}" '
        f'y="{height - 3}" '
        'fill="#777" font-size="10">More</text>'
    )

    return (
        f'<svg class="activity-chart" xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" role="img" '
        'aria-label="GitHub contributions over the last year">'
        '<title>GitHub contributions over the last year</title>'
        '<desc>Daily public contributions. Hover a square to see its date and count.</desc>'
        f'{"".join(labels)}{weekday_labels}{"".join(squares)}{"".join(legend)}</svg>'
    )


def app_store_listings() -> dict[str, tuple[str, str | None]] | None:
    """Return (URL, name) of this developer's currently listed US App Store apps."""
    request = Request(
        f"https://itunes.apple.com/lookup?id={APPLE_DEVELOPER_ID}&entity=software&limit=200&country=us",
        headers={"User-Agent": "jackwallner-portfolio-build"},
    )
    try:
        with urlopen(request, timeout=10) as response:
            results = json.load(response).get("results", [])
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None

    return {
        str(item["trackId"]): (item["trackViewUrl"], item.get("trackName"))
        for item in results
        if item.get("trackId") and item.get("trackViewUrl")
    }


def sync_app_store_status(projects: list[dict]) -> bool:
    """Promote entries once Apple lists them, and keep their names current."""
    listings = app_store_listings()
    if listings is None:
        return False

    changed = False
    for project in projects:
        app_id = str(project.get("appStoreId") or "")
        if not app_id:
            m = re.search(r"/id(\d+)", project.get("appStore") or "")
            app_id = m.group(1) if m else ""
        listing = listings.get(app_id)
        if not app_id or not listing:
            continue
        url, name = listing
        updated = {
            "appStore": url,
            "status": "App Store",
            "cls": "live",
        }
        # The listing name is the source of truth (see the naming rule in
        # ~/ios/landing-pages/README.md), so renames reach the site on their own.
        if name:
            updated["name"] = name
        for key, value in updated.items():
            if project.get(key) != value:
                project[key] = value
                changed = True
    return changed


def thumb(name):
    """Return the assets-relative path of a small WebP copy of an image.

    Source icons are 256px+ PNGs (100 to 400 KB each) shown at 32px, which made
    the home page pull about 2.7 MB of images. The copy is regenerated when the
    source is newer; without Pillow (for example in CI) an existing copy is
    reused and a missing one falls back to the original file.
    """
    src = ASSETS / name
    out = THUMBS / (Path(name).stem + ".webp")
    stale = not out.exists() or (src.exists() and src.stat().st_mtime > out.stat().st_mtime)
    if stale and src.exists():
        try:
            from PIL import Image
        except ImportError:
            pass
        else:
            THUMBS.mkdir(exist_ok=True)
            with Image.open(src) as im:
                im = im.convert("RGBA")
                im.thumbnail((THUMB_PX, THUMB_PX), Image.LANCZOS)
                im.save(out, "WEBP", quality=85, method=6)
    return f"thumbs/{out.name}" if out.exists() else name


def e(s):
    return html.escape(s or "", quote=True)


def fmt_date(iso):
    if not iso:
        return ""
    y, m, _ = iso.split("-")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{months[int(m) - 1]} {y}"


def head(title, desc, prefix="", canonical=None, jsonld=None):
    canon = f'\n    <link rel="canonical" href="{canonical}">' if canonical else ""
    social = ""
    if canonical:
        social = f"""
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Jack Wallner">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(desc)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{e(title)}">
    <meta name="twitter:description" content="{e(desc)}">"""
    ld = ""
    if jsonld:
        # "</" can't appear inside a script element; JSON allows the escaped form.
        body = json.dumps(jsonld, indent=2, ensure_ascii=False).replace("</", "<\\/")
        ld = f'\n    <script type="application/ld+json">\n{body}\n    </script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">{canon}{social}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{prefix}home.css?v=9">
    <link rel="icon" type="image/x-icon" href="{prefix}favicon.ico">{ld}
</head>
<body>"""


PERSON = {
    "@type": "Person",
    "@id": SITE + "#person",
    "name": "Jack Wallner",
    "url": SITE,
    "image": OG_IMAGE,
    "jobTitle": "iOS developer",
    "homeLocation": {"@type": "Place", "name": "Vancouver, Washington"},
    "sameAs": [GITHUB, LINKEDIN,
               f"https://apps.apple.com/us/developer/id{APPLE_DEVELOPER_ID}"],
}


def page_url(p):
    """Absolute URL of a project's own page, or None when it lives off-site."""
    page = p.get("page") or ""
    if not page or page.startswith("http"):
        return None
    return SITE + page


def app_list(apps):
    """ItemList of app pages, so crawlers see every app from one document."""
    items = []
    for i, p in enumerate(apps, 1):
        app = {
            "@type": "MobileApplication",
            "name": p["name"],
            "url": page_url(p),
            "description": p["desc"],
            "operatingSystem": "iOS",
            "author": {"@id": SITE + "#person"},
        }
        if p.get("appStore"):
            app["installUrl"] = p["appStore"]
        items.append({"@type": "ListItem", "position": i, "item": app})
    return {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": items}


def site_header(subtitle, prefix="", home_link=False):
    title = f'<a href="{prefix or "./"}">Jack Wallner</a>' if home_link else "Jack Wallner"
    return f"""
    <header class="site-header container">
        <img src="{prefix}assets/{thumb('profile.png')}" alt="Jack Wallner" class="profile-img" width="40" height="40">
        <div class="site-title-wrap">
            <div class="site-title">{title}</div>
            <div class="site-subtitle">{e(subtitle)}</div>
        </div>
        <nav class="header-links">
            <a href="mailto:{EMAIL}">Email</a>
            <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
            <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
        </nav>
    </header>
"""


def site_footer(prefix="", back=False):
    back_link = f'<a href="{prefix or "./"}">Back to portfolio</a> · ' if back else ""
    return f"""
    <footer>
        <div class="container footer-inner">
            <div>Jack Wallner · Vancouver, Washington</div>
            <div>
                {back_link}<a href="mailto:{EMAIL}">Email</a> ·
                <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a> ·
                <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""


def table_row(p):
    ext = ' target="_blank" rel="noopener"' if p.get("ext") else ""
    status = f'<span class="project-stamp {e(p["cls"])}">{e(p["status"])}</span>'
    play_link = (
        f'<br><a class="project-store-link" href="{e(play_url(p["googlePlay"], "jw-home"))}" '
        'target="_blank" rel="noopener">Google Play</a>'
        if p.get("googlePlay") else ""
    )
    icon = (f'<img src="assets/{e(thumb(p["icon"]))}" alt="" class="proj-icon" '
            'width="32" height="32" loading="lazy" decoding="async">'
            if p.get("icon") else
            f'<span class="proj-icon ph">{e(p["name"][0].upper())}</span>')
    return f"""                        <tr class="proj-tr" data-group="{e(p['group'])}">
                            <td class="col-proj">
                                <div class="proj-cell">
                                    {icon}
                                    <div class="proj-body">
                                        <a class="proj-name" href="{e(p['page'])}"{ext}>{e(p["name"])}</a>
                                        <span class="proj-desc">{e(p['desc'])}</span>
                                    </div>
                                </div>
                            </td>
                            <td class="col-type"><span class="proj-type">{e(p['type'])}</span></td>
                            <td class="col-status">{status}{play_link}</td>
                            <td class="col-updated"><span class="proj-when">{fmt_date(p.get('updated'))}</span></td>
                        </tr>"""


def build_home(projects, contribution_summary, contribution_svg):
    by_date = sorted(projects, key=lambda p: p.get("start") or "", reverse=True)

    counts = {"all": len(projects)}
    for _, key in FILTERS[1:]:
        counts[key] = sum(1 for p in projects if p["group"] == key)
    shipped = sum(1 for p in projects if p.get("appStore"))
    contribution_summary = contribution_summary or "GitHub activity"

    chips = "\n".join(
        f'                    <button class="chip{" active" if key == "all" else ""}" '
        f'data-filter="{key}">{e(label)} <span class="chip-n">{counts[key]}</span></button>'
        for label, key in FILTERS
    )

    return "".join([
        head("Jack Wallner - iPhone and Apple Watch Apps",
             f"Jack Wallner builds simple iPhone and Apple Watch apps: {shipped} on the App "
             "Store for health tracking, sports stats, card game practice, and family life.",
             canonical=SITE,
             jsonld={"@context": "https://schema.org", "@graph": [
                 PERSON,
                 {"@type": "WebSite", "@id": SITE + "#site", "url": SITE,
                  "name": "Jack Wallner", "publisher": {"@id": SITE + "#person"}},
                 {"@type": "ProfilePage", "url": SITE, "name": "Jack Wallner",
                  "mainEntity": {"@id": SITE + "#person"}},
             ]}),
        site_header("Vancouver, Washington"),
        f"""
    <main class="container">
        <section class="intro">
            <h1 class="intro-title">Simple iPhone and Apple Watch apps</h1>
            <p class="intro-text">Jack Wallner is an independent developer in Vancouver, Washington who makes simple iPhone and Apple Watch apps: {shipped} on the App Store for health tracking, sports stats, card game practice, and family life. Browse them all on the <a href="ios/">iOS apps</a> page, or read the <a href="guides/">guides and comparisons</a>.</p>
        </section>

        <section class="activity-section" aria-labelledby="activity-title">
            <div class="activity-head">
                <div class="activity-title-wrap">
                    <h2 id="activity-title" class="section-title">Activity</h2>
                </div>
                <div class="activity-stats mono" aria-label="Portfolio stats">
                    <span><strong>{shipped}</strong> on the App Store</span>
                    <span><strong>{len(projects)}</strong> projects</span>
                </div>
            </div>
            <div class="github-activity">
                <p class="activity-summary">{e(contribution_summary)}</p>
                <a class="activity-chart-link" href="{GITHUB}" target="_blank" rel="noopener" aria-label="View Jack Wallner's GitHub activity">
{contribution_svg}
                </a>
                <div class="activity-chart-note">Public contributions only</div>
            </div>
        </section>

        <section class="all-projects" id="all">
            <div class="section-head">
                <h2 class="section-title">All projects</h2>
                <div class="filters" role="group" aria-label="Filter projects by type">
{chips}
                </div>
            </div>

            <div class="proj-table-wrap">
                <table class="proj-table">
                    <thead>
                        <tr>
                            <th class="col-proj">Project</th>
                            <th class="col-type">Type</th>
                            <th class="col-status">Status</th>
                            <th class="col-updated">Updated</th>
                        </tr>
                    </thead>
                    <tbody id="proj-rows">
{chr(10).join(table_row(p) for p in by_date)}
                    </tbody>
                </table>
            </div>

            <p class="all-foot mono">
                <a href="ios/">All {counts['ios']} iOS apps &rarr;</a>
                <a href="guides/">Guides and comparisons &rarr;</a>
                <a href="{GITHUB}?tab=repositories" target="_blank" rel="noopener">GitHub profile</a>
            </p>
        </section>

    </main>
""",
        site_footer(),
    ]).replace("</body>", '    <script src="script.js?v=5"></script>\n</body>')


def store_url(p, key):
    """Store link for the apps index; App Store links carry a campaign tag so
    App Store Connect can attribute installs to this page."""
    url = p[key]
    if key == "googlePlay":
        return play_url(url, "jw-apps-index")
    return f"{url.split('?')[0]}?pt={APPLE_PROVIDER_TOKEN}&ct=jw-apps-index&mt=8"


def play_url(url, campaign):
    """Google Play link with a UTM referrer, reported in Play Console acquisition."""
    return (f"{url}&referrer=utm_source%3Djackwallner.com%26utm_medium%3Dweb"
            f"%26utm_campaign%3D{campaign}")


def build_ios(projects):
    apps = [p for p in projects if p["group"] == "ios"]
    live = sum(1 for p in apps if p.get("appStore"))
    sections = []
    for cat in CATEGORY_ORDER:
        members = [p for p in apps if p.get("category") == cat]
        if not members:
            continue
        rows = []
        for p in members:
            store_links = [
                f'<a href="{e(store_url(p, key))}" target="_blank" rel="noopener">{label}</a>'
                for key, label in (("appStore", "App Store"), ("googlePlay", "Google Play"))
                if p.get(key)
            ]
            store = (" ".join(store_links) if store_links else
                     f'<span class="project-stamp {e(p["cls"])}">{e(p["status"])}</span>')
            # A pre-release app can be listed before it has an icon.
            icon = (f'<img src="../assets/{e(thumb(p["icon"]))}" alt="" class="proj-icon" '
                    'width="32" height="32" loading="lazy" decoding="async">'
                    if p.get("icon") else
                    f'<span class="proj-icon ph">{e(p["name"][0].upper())}</span>')
            rows.append(f"""                    <li class="app-row">
                        <a class="app-link" href="{e(p['slug'])}/">
                            {icon}
                            <span class="app-body">
                                <span class="app-name">{e(p["name"])}</span>
                                <span class="app-desc">{e(p['desc'])}</span>
                            </span>
                        </a>
                        <span class="app-store">{store}</span>
                    </li>""")
        sections.append(f"""            <section class="app-group">
                <h2 class="group-title mono">{e(cat)} <span class="group-n">{len(members)}</span></h2>
                <ul class="app-list">
{chr(10).join(rows)}
                </ul>
            </section>""")

    return "".join([
        head("iPhone and Apple Watch Apps by Jack Wallner",
             f"{live} iPhone and Apple Watch apps by Jack Wallner: calorie, migraine, sobriety "
             "and GLP-1 trackers, advanced sports stats, and card game trainers.",
             prefix="../", canonical=SITE + "ios/",
             jsonld={"@context": "https://schema.org", "@graph": [
                 PERSON,
                 {"@type": "CollectionPage", "url": SITE + "ios/",
                  "name": "iPhone and Apple Watch Apps by Jack Wallner",
                  "author": {"@id": SITE + "#person"},
                  "mainEntity": app_list([p for c in CATEGORY_ORDER for p in apps
                                          if p.get("category") == c])},
                 {"@type": "BreadcrumbList", "itemListElement": [
                     {"@type": "ListItem", "position": 1, "name": "Jack Wallner", "item": SITE},
                     {"@type": "ListItem", "position": 2, "name": "iOS apps",
                      "item": SITE + "ios/"}]},
             ]}),
        site_header("iOS and watchOS apps", prefix="../", home_link=True),
        f"""
    <main class="container">
        <section class="apps-index">
            <h1 class="intro-title">iOS apps</h1>
            <p class="intro-text">{live} apps on the App Store, {len(apps) - live} in the pipeline. Every one has its own page here with screenshots, privacy policy, and support. <a href="../guides/">Guides and comparisons</a> for each app are collected on one page.</p>
{chr(10).join(sections)}
        </section>
    </main>
""",
        site_footer(prefix="../", back=True),
    ]).replace('    <script src="script.js?v=5"></script>\n', "")


def guide_title(title):
    """Page title without the trailing "| App name" brand suffix."""
    return title.split(" | ")[0].strip()


def build_guides(projects):
    """One page linking every guide and comparison, so each sits a click from the home page."""
    apps = [p for p in projects if p["group"] == "ios"]
    total = 0
    sections = []
    items = []
    for cat in CATEGORY_ORDER:
        rows = []
        for p in (a for a in apps if a.get("category") == cat):
            for url, title, desc in guides(p):
                total += 1
                items.append({"@type": "ListItem", "position": total, "url": url,
                              "name": guide_title(title)})
                rows.append(f"""                    <li class="app-row">
                        <a class="app-link" href="{e(url.replace(SITE, '../'))}">
                            <span class="app-body">
                                <span class="app-name">{e(guide_title(title))}</span>
                                <span class="app-desc">{e(desc)}</span>
                            </span>
                        </a>
                        <span class="app-store"><a href="../{e(p['page'])}">{e(p['name'].split(':')[0].split(' - ')[0])}</a></span>
                    </li>""")
        if rows:
            sections.append(f"""            <section class="app-group">
                <h2 class="group-title mono">{e(cat)} <span class="group-n">{len(rows)}</span></h2>
                <ul class="app-list">
{chr(10).join(rows)}
                </ul>
            </section>""")

    title = "Guides and App Comparisons by Jack Wallner"
    desc = (f"{total} plain guides and app comparisons: calorie burn and VO2 max on Apple Watch, "
            "GLP-1 and sobriety tracking, Statcast and NFL stats, and card game rules.")
    return "".join([
        head(title, desc, prefix="../", canonical=SITE + "guides/",
             jsonld={"@context": "https://schema.org", "@graph": [
                 PERSON,
                 {"@type": "CollectionPage", "url": SITE + "guides/", "name": title,
                  "author": {"@id": SITE + "#person"},
                  "mainEntity": {"@type": "ItemList", "numberOfItems": total,
                                 "itemListElement": items}},
                 {"@type": "BreadcrumbList", "itemListElement": [
                     {"@type": "ListItem", "position": 1, "name": "Jack Wallner", "item": SITE},
                     {"@type": "ListItem", "position": 2, "name": "Guides",
                      "item": SITE + "guides/"}]},
             ]}),
        site_header("Guides and comparisons", prefix="../", home_link=True),
        f"""
    <main class="container">
        <section class="apps-index">
            <h1 class="intro-title">Guides</h1>
            <p class="intro-text">{total} guides and comparisons, each written alongside one of my <a href="../ios/">iOS apps</a> and sourced at the bottom. Comparisons cover the main alternatives, not only my app.</p>
{chr(10).join(sections)}
        </section>
    </main>
""",
        site_footer(prefix="../", back=True),
    ])


AI_CRAWLERS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
               "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended",
               "Applebot-Extended", "Bingbot", "DuckAssistBot"]


def last_modified(path):
    """Date of the last commit touching a published file, falling back to today."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        out = ""
    return out.strip() or date.today().isoformat()


LEGAL_PAGE = re.compile(r"(privacy|terms|support|community|consumer-health|join)[^/]*\.html$")


def indexable(path):
    """True unless the page opts out of search or points its canonical elsewhere."""
    head = path.read_text(encoding="utf-8", errors="replace")[:6000]
    if re.search(r'name="robots"[^>]*noindex', head):
        return False
    canon = re.search(r'rel="canonical"\s+href="([^"]+)"', head)
    rel = path.relative_to(DOCS).as_posix()
    own = SITE + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
    return not canon or canon.group(1) == own


def build_sitemap(projects):
    """Every indexable page under each project's folder, not just its front page.

    The guides, calculators and support pages inside an app folder are what match
    long-tail searches, so they belong in the sitemap too.
    """
    pages = [("", 1.0), ("ios/", 0.9), ("guides/", 0.9)]
    for p in projects:
        if not page_url(p) or not (DOCS / p["page"] / "index.html").exists():
            continue
        root = DOCS / p["page"]
        for f in sorted(root.rglob("*.html")):
            if not indexable(f):
                continue
            rel = f.relative_to(DOCS).as_posix()
            path = rel[: -len("index.html")] if rel.endswith("index.html") else rel
            if f.parent == root and f.name == "index.html":
                prio = 0.8 if p["group"] == "ios" else 0.5
            else:
                prio = 0.3 if LEGAL_PAGE.search(rel) else 0.7
            pages.append((path, prio))
    rows = "\n".join(
        f"  <url><loc>{SITE}{path}</loc>"
        f"<lastmod>{last_modified(DOCS / (path + 'index.html' if path.endswith('/') or not path else path))}</lastmod>"
        f"<priority>{prio}</priority></url>"
        for path, prio in pages
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{rows}\n</urlset>\n")


def build_robots():
    named = "\n\n".join(f"User-agent: {bot}\nAllow: /" for bot in AI_CRAWLERS)
    return (f"# Search engines and AI answer engines are welcome.\n\n{named}\n\n"
            f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")


def guides(p):
    """(url, title, description) for an app's indexable guide pages, legal pages excluded."""
    root = DOCS / (p.get("page") or "")
    if not page_url(p) or not root.is_dir():
        return []
    out = []
    for f in sorted(root.rglob("*.html")):
        rel = f.relative_to(DOCS).as_posix()
        if f.parent == root and f.name == "index.html" or LEGAL_PAGE.search(rel) or not indexable(f):
            continue
        h = f.read_text(encoding="utf-8", errors="replace")
        t = re.search(r"<title[^>]*>(.*?)</title>", h, re.S)
        d = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', h)
        if not (t and d):
            continue
        url = SITE + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
        out.append((url, html.unescape(t.group(1).strip()), html.unescape(d.group(1))))
    return out


def markdown_url(url):
    """The page's markdown twin (<page>.html.md) when the app ships one, else the page."""
    rel = url[len(SITE):]
    twin = rel + "index.html.md" if rel.endswith("/") or not rel else rel + ".md"
    return SITE + twin if (DOCS / twin).is_file() else url


def build_llms(projects):
    """llms.txt: a plain index of every app page for AI answer engines."""
    apps = [p for c in CATEGORY_ORDER for p in projects
            if p["group"] == "ios" and p.get("category") == c]
    lines = ["# Jack Wallner", "",
             "> Independent iOS developer in Vancouver, Washington. Simple iPhone and "
             "Apple Watch apps, each with its own page, privacy policy and support.", ""]
    for cat in CATEGORY_ORDER:
        members = [p for p in apps if p.get("category") == cat]
        if not members:
            continue
        lines += [f"## {cat}", ""]
        for p in members:
            store = "App Store" if p.get("appStore") else p["status"]
            lines.append(f"- [{p['name']}]({markdown_url(page_url(p))}): {p['desc']} ({store})")
            lines += [f"  - [{t}]({markdown_url(u)}): {d}" for u, t, d in guides(p)]
        lines.append("")
    others = [p for p in projects if p["group"] != "ios" and page_url(p)
              and p.get("status") != "Retired"]
    if others:
        lines += ["## Other projects", ""]
        lines += [f"- [{p['name']}]({page_url(p)}): {p['desc']}" for p in others]
        lines.append("")
    lines += ["## Contact", "", f"- Email: {EMAIL}", f"- GitHub: {GITHUB}", ""]
    return "\n".join(lines)


def main():
    projects = json.loads(DATA.read_text())
    if sync_app_store_status(projects):
        DATA.write_text(json.dumps(projects, indent=2, ensure_ascii=False) + "\n")

    contribution_summary, contribution_days = github_contribution_data()
    contribution_svg = contribution_chart_svg(contribution_days)
    if contribution_svg:
        CONTRIBUTION_CHART.write_text(contribution_svg)
    elif CONTRIBUTION_CHART.exists():
        contribution_svg = CONTRIBUTION_CHART.read_text()

    (DOCS / "index.html").write_text(
        build_home(projects, contribution_summary, contribution_svg)
    )
    (DOCS / "ios" / "index.html").write_text(build_ios(projects))
    (DOCS / "guides").mkdir(exist_ok=True)
    (DOCS / "guides" / "index.html").write_text(build_guides(projects))
    (DOCS / "sitemap.xml").write_text(build_sitemap(projects))
    (DOCS / "robots.txt").write_text(build_robots())
    (DOCS / "llms.txt").write_text(build_llms(projects))
    shipped = sum(1 for project in projects if project.get("appStore"))
    print(f"built index pages from {len(projects)} projects, {shipped} on the App Store "
          f"({date.today().isoformat()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
