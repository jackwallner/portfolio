# portfolio

This repository is published via **GitHub Pages** from the `main` branch's `/docs` folder with a custom domain.

## GitHub Pages

- **URL**: `https://jackwallner.com`
- **Source**: `main` / `/docs`

### One-time setup in GitHub

In the repo settings:

- **Settings → Pages → Build and deployment**
  - **Source**: Deploy from a branch
  - **Branch**: `main`
  - **Folder**: `/docs`

## Editing projects

`docs/projects.json` is the single source of truth for every project: name,
status, description, tech, and links. Add an `appStoreId` for an unreleased app
so the build can promote it when Apple lists it in the US App Store. The
generator writes the resulting status and link back to `projects.json`; the
scheduled daily build checks again for new releases.

The homepage's contribution chart is baked into its HTML at build time from
GitHub's public contribution data, so it renders without loading a third-party
widget in the visitor's browser.

To add or change a project, edit that file and rebuild:

```sh
python3 scripts/build_site.py
```

That regenerates two pages, both fully static:

- `docs/index.html` - the full project table
- `docs/ios/index.html` - the App Store catalogue, grouped by category

The homepage lists every project in reverse chronological order. The
`build-site` workflow rebuilds and commits automatically if `projects.json` is
pushed without the generated pages.

## Per-app landing pages

`docs/ios/<slug>/` is mirrored from each app's own repo by
`scripts/sync_ios_pages.py`, not edited here. See the header of that file.

## Changelog pages

`docs/ios/<slug>/changelog.html` lists every live version of each App Store app
with its release date and What's New text. `scripts/build_changelogs.py` writes
them from `data/changelogs.json`, using the app page's own head, nav and footer,
and adds a Changelog link to that page's footer. The daily `build-site` run picks
up new releases from Apple's public lookup API and App Store listing (no
credentials), and the mirror sync re-renders an app's changelog whenever its page
is refreshed. The sitemap dates each changelog by its newest release.
