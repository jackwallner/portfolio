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

import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = DOCS / "projects.json"

EMAIL = "jackwallner@gmail.com"
GITHUB = "https://github.com/jackwallner"
LINKEDIN = "https://www.linkedin.com/in/wallnerjack/"

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
    <link rel="stylesheet" href="{prefix}home.css?v=5">
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
                            <td class="col-status"><span class="project-stamp {e(p['cls'])}">{e(p['status'])}</span></td>
                            <td class="col-updated"><span class="proj-when">{fmt_date(p.get('updated'))}</span></td>
                        </tr>"""


def build_home(projects):
    by_date = sorted(projects, key=lambda p: p.get("start") or "", reverse=True)

    counts = {"all": len(projects)}
    for _, key in FILTERS[1:]:
        counts[key] = sum(1 for p in projects if p["group"] == key)
    shipped = sum(1 for p in projects if p.get("appStore"))

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
                <h1 id="activity-title" class="section-title">Activity</h1>
                <div class="activity-stats mono" aria-label="Portfolio stats">
                    <span><strong>{shipped}</strong> on the App Store</span>
                    <span><strong>{len(projects)}</strong> projects</span>
                </div>
            </div>
            <a class="activity-chart-link" href="{GITHUB}" target="_blank" rel="noopener" aria-label="View Jack Wallner's GitHub activity">
                <img src="https://ghchart.rshah.org/39d353/jackwallner" alt="GitHub contribution graph" class="activity-chart">
            </a>
            <div class="activity-chart-note">Public contributions only</div>
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
            store = (f'<a href="{e(p["appStore"])}" target="_blank" rel="noopener">App Store &#8599;</a>'
                     if p.get("appStore") else
                     f'<span class="project-stamp {e(p["cls"])}">{e(p["status"])}</span>')
            rows.append(f"""                    <li class="app-row">
                        <a class="app-link" href="{e(p['slug'])}/">
                            <img src="../assets/{e(p['icon'])}" alt="" class="proj-icon">
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
    (DOCS / "index.html").write_text(build_home(projects))
    (DOCS / "ios" / "index.html").write_text(build_ios(projects))
    print(f"built index.html and ios/index.html from {len(projects)} projects "
          f"({date.today().isoformat()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
