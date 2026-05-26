# Astro ASO setup — Bond (US)

> Process: [`astro-setup-process.md`](astro-setup-process.md)

Last curated: **2026-05-25** — competitor research + pop/difficulty + live search intent

## App

| Field | Value |
|-------|-------|
| App Store name | Husband & Wife Reminder - Bond |
| Astro app | **Bond** (temporary) — ID `101` |
| Bundle ID | `com.jackwallner.bond` |
| Store | `us` |
| Status | Pre-launch — rankings N/A until live |

## Recommended ASC copy (in repo)

All three fields are optimized and **within Apple limits** (verified by char count).

| Field | Limit | Chars | Value |
|-------|-------|-------|-------|
| **Name** | 30 | 29 | `Bond: Love Language Reminders` |
| **Subtitle** | 30 | 29 | `Couples · Watch · Anniversary` |
| **Keywords** | 100 | 100 | `relationship,tracker,anniversary,partner,widget,watch,spouse,distance,milestone,nudge,counter,paired` |

**Keyword field rules:** comma-separated, no spaces (`KEY,WORD,CYX`). Do not repeat words from name/subtitle — Apple ignores duplicates, so those slots are wasted. Name/subtitle carry: bond, love, language, reminders, couples, watch, anniversary.

**Name change note:** replaced `Husband & Wife Reminder - Bond` (bad search intent — prayer apps / wife games) with brand-first love-language positioning.

Files: `fastlane/metadata/en-US/{name,subtitle,keywords}.txt` — upload with `./scripts/upload-appstore-metadata.sh` when ready.

## Research summary

### What we removed (wrong SERP or noise)

- **Prayer / wife games:** `husband wife reminder`, `wife reminder`, `remind my husband/wife`
- **Too generic / wrong category:** `bond`, `daily check in`, `milestone tracker` (CDC app), `marriage app` (Muzz), `words of affirmation` (I am app), `acts of service` (unrelated)
- **Ultra-low volume:** most multi-word phrases with pop ≈ 5 and no couples intent in top 10

### Tier 1 — prioritize (high intent + best metrics)

| Keyword / phrase | Pop | Diff | Why |
|------------------|-----|------|-----|
| `couples app` | 54 | 72 | Top ratio; SERP = Cozy Couples, Couple Joy |
| `relationship reminder` | — | — | **#1 Vera: Relationship Reminders** — closest competitor niche |
| `relationship tracker` | 57 | 62 | My Love, Paired rank |
| `love language app` | — | — | **#1 Love Nudge** — category anchor |
| `couple check in` | — | — | **#1 Paired** |
| `five love languages` | — | — | **#1 Love Nudge** |
| `love counter` | — | — | My Love counter apps |
| `long distance relationship` | 36 | 70 | Strong couples SERP |
| `relationship app` | 25 | 72 | My Love, counters |
| `anniversary tracker` | 33 | 60 | My Love ranks |

### Tier 2 — track in Astro, secondary ASC focus

`partner app`, `couples widget`, `love language`, `love nudge`, `paired app couples`, `anniversary countdown`, `partner reminder`, `couples reminder`, `love app`, `cozy couples`, `apple watch couples`, `free couples app`, `widget couple`

### Tier 3 — brand / love-language taxonomy (low volume, high relevance)

`acts of service`, `words of affirmation`, `quality time`, `physical touch`, `receiving gifts` — keep for positioning; don’t expect rank until established.

### ASC keyword field strategy

16 single tokens (99 chars) covering the highest-volume **roots** Astro can combine: couple, relationship, love, language, reminder, tracker, anniversary, partner, widget, watch, spouse, distance, milestone, nudge, counter, paired.

Apple indexes combinations; phrases above are tracked separately in Astro for research.

## Astro tracking

| Artifact | Path |
|----------|------|
| Curated phrase list | `scripts/astro_curate_keywords.py` |
| Full track list (58) | `scripts/astro-keywords-us.json` |
| Research dumps | `scripts/astro-research-*.json` |
| Resync script | `./scripts/astro-resync-curated.sh` |
| Config | `scripts/.astro-app.json` |

Competitors researched: Paired, Between, Cupla, Love Nudge, Couple Joy, Evergreen.

## Re-sync

```bash
./scripts/astro-resync-curated.sh
```

## After App Store launch

1. Replace temporary Astro app `101` with real App Store ID.
2. `./scripts/astro-setup.sh --skip-pull`
3. Weekly: sort by rank change; drop phrases stuck at 1000 for 3+ weeks.

## Next ASC experiments

1. **Description** — lead with love languages + reminders + Watch/widgets; mirror Tier 1 phrases in first 3 lines.
2. **Name** — consider shortening; “Husband & Wife” pulls non-couples-app SERP.
3. **Screenshots** — show couple pairing + reminder notification + love-language tags.
