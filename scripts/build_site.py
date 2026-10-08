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

APPLE_DEVELOPER_ID = "1891233967"
APPLE_LOOKUP_URL = "https://itunes.apple.com/lookup"
CONTRIBUTION_CHART = DOCS / "assets" / "github-contributions.svg"

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


def app_store_listings() -> dict[str, str] | None:
    """Return public US App Store URLs for this developer's currently listed apps."""
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
        str(item["trackId"]): item["trackViewUrl"]
        for item in results
        if item.get("trackId") and item.get("trackViewUrl")
    }


def sync_app_store_status(projects: list[dict]) -> bool:
    """Promote entries with appStoreId values once Apple lists them."""
    listings = app_store_listings()
    if listings is None:
        return False

    changed = False
    for project in projects:
        app_id = str(project.get("appStoreId") or "")
        listing = listings.get(app_id)
        if not app_id or not listing:
            continue
        updated = {
            "appStore": listing,
            "status": "App Store",
            "cls": "live",
        }
        for key, value in updated.items():
            if project.get(key) != value:
                project[key] = value
                changed = True
    return changed


def e(s):
    return html.escape(s or "", quote=True)


def fmt_date(iso):
    if not iso:
        return ""
    y, m, _ = iso.split("-")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{months[int(m) - 1]} {y}"


def head(title, desc, prefix="", canonical=None):
    canon = f'\n    <link rel="canonical" href="{canonical}">' if canonical else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">{canon}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{prefix}home.css?v=9">
    <link rel="icon" type="image/x-icon" href="{prefix}favicon.ico">
</head>
<body>"""


def site_header(subtitle, prefix="", home_link=False):
    title = f'<a href="{prefix or "./"}">Jack Wallner</a>' if home_link else "Jack Wallner"
    return f"""
    <header class="site-header container">
        <img src="{prefix}assets/profile.png" alt="Jack Wallner" class="profile-img">
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
        f'<br><a class="project-store-link" href="{e(p["googlePlay"])}" '
        'target="_blank" rel="noopener">Google Play &#8599;</a>'
        if p.get("googlePlay") else ""
    )
    icon = (f'<img src="assets/{e(p["icon"])}" alt="" class="proj-icon">'
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
        head("Jack Wallner - Work",
             f"{shipped} apps on the App Store and {len(projects)} projects by Jack Wallner.",
             canonical="https://jackwallner.com/"),
        site_header("Vancouver, Washington"),
        f"""
    <main class="container">
        <section class="activity-section" aria-labelledby="activity-title">
            <div class="activity-head">
                <div class="activity-title-wrap">
                    <h1 id="activity-title" class="section-title">Activity</h1>
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
                <a href="{GITHUB}?tab=repositories" target="_blank" rel="noopener">GitHub profile &#8599;</a>
            </p>
        </section>

    </main>
""",
        site_footer(),
    ]).replace("</body>", '    <script src="script.js?v=5"></script>\n</body>')


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
                f'<a href="{e(p[key])}" target="_blank" rel="noopener">{label} &#8599;</a>'
                for key, label in (("appStore", "App Store"), ("googlePlay", "Google Play"))
                if p.get(key)
            ]
            store = (" ".join(store_links) if store_links else
                     f'<span class="project-stamp {e(p["cls"])}">{e(p["status"])}</span>')
            # A pre-release app can be listed before it has an icon.
            icon = (f'<img src="../assets/{e(p["icon"])}" alt="" class="proj-icon">'
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
        head("iOS Apps - Jack Wallner",
             f"Every iOS and watchOS app Jack Wallner has shipped: {live} on the App Store, "
             "each with its own page.",
             prefix="../", canonical="https://jackwallner.com/ios/"),
        site_header("iOS and watchOS apps", prefix="../", home_link=True),
        f"""
    <main class="container">
        <section class="apps-index">
            <h1 class="intro-title">iOS apps</h1>
            <p class="intro-text">{live} apps on the App Store, {len(apps) - live} in the pipeline. Every one has its own page here with screenshots, privacy policy, and support.</p>
{chr(10).join(sections)}
        </section>
    </main>
""",
        site_footer(prefix="../", back=True),
    ]).replace('    <script src="script.js?v=5"></script>\n', "")


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
    shipped = sum(1 for project in projects if project.get("appStore"))
    print(f"built index pages from {len(projects)} projects, {shipped} on the App Store "
          f"({date.today().isoformat()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
