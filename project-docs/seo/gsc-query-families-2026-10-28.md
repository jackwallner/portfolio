# Search Console query families (2026-10-28)

Pulled 2026-10-28 through Claude in Chrome. Google: GSC Performance, web search, "3 months", which
only holds Oct 11-26 because the properties were created Oct 12. Bing: Search Performance API
(`/webmasters/api/searchperf/{keyword,page}/stats`, 90 days, data starts Oct 14) and AI Performance.
App Store: ASC dashboard `timeseries` grouped by storefront, Jul 29-Oct 25, 29 live apps.

## Totals

| Source | Impressions | Clicks | Notes |
|---|---|---|---|
| GSC jackwallner.com | 2,262 | 223 | 126 named queries, 61 pages |
| of which /songhero/ | 1,316 | 209 | 94% of clicks |
| of which /ios/ | 964 | 7 | avg position 12.3 |
| GSC jackwallner.github.io | 30 | 0 | support and privacy pages only; the redirect script is working |
| Bing jackwallner.com | 170 | 13 | 84 keywords, 22 pages |
| Bing Copilot citations | 127 | | songhero 76, basketball 12, EPA 11, best triathlon app 11, xG 6, best cribbage app 5, conduit fill 3, triathlon splits 2 |
| GSC AI features (AI Overviews) | 638 songhero | | then mahj/ 17, home 9, best bridge app 9, TS% 8, charleston 8, talk about sports 8, EPA 6, football/ 5 |

Named queries cover only about a fifth of /ios/ impressions; Google hides the rest as rare queries.
For low-volume pages, page impressions are the better signal than the query list.

/ios/ impressions by country (GSC): US 104, Canada 28, UK 18, then 31 countries with 1-5 each.
Non-English search demand is near zero today, which is what an English-only site gets. It says
nothing about demand for localized pages.

## Query families and the page Google picked

Position is GSC average position. "Bing" is Bing impressions, position in brackets.

| # | App | Family (top queries) | Google impr | Pos | Page Google ranks | Bing | Gap |
|---|---|---|---|---|---|---|---|
| 1 | Bridge | best bridge app for beginners, best app to learn bridge, bridge apps for beginners, best bridge app for iphone, learn bridge online free | 141 (page) | 9.2 | bridge/best-bridge-app-for-beginners.html | 0 | Biggest /ios/ page. Edge of page 1 |
| 2 | Football | epa cpoe, epa/play, what is epa per play, epa meaning football, nfl epa per play meaning, what is qb epa | 119 (89 on guide, 30 on index) | 7.7 | football/what-is-epa-per-play.html | 17 (6.6), Copilot 11 | Page already covers CPOE; "epa cpoe" (16) is the top /ios/ query |
| 3 | Mahj | mahjtrainer / mahj trainer (brand), can you call mahjong during the charleston, when can you stop the charleston, soap in mahjong, a quint must have a joker, jokers pairs | 164 (all mahj) | 6.5 index, 11.7 charleston, 7.3 card sections | mahj/ (46), learn/charleston (35), learn/card-sections (27), learn/jokers (20), learn/glossary (17), learn/scoring (13) | 7 (6.4) | Charleston page has no answer to "call mahjong during" or "stop the Charleston" |
| 4 | Basketball | whats a good true shooting percentage, true shooting percentage nba, ts meaning nba, basketball ts meaning | 62 | 9.0 | basketball/true-shooting-percentage-explained.html | 0, Copilot 12 on index | |
| 5 | Sober | sobriety milestones | 42 (page) + 6 index | 10.4 | sober/sobriety-milestones.html | 0 | Index has 2 of the 7 /ios/ clicks (pos 2.7) |
| 6 | Bond | love language examples, 5 acts of love, love in everyday scenarios, five love languages list | 38 | 31.0 | bond/5-love-languages-examples.html | 1 | Page 3-4. Not close |
| 7 | Sports | (hidden queries) | 37 | 6.4 | sports/how-to-talk-about-sports.html | 0 | 1 click |
| 8 | VO2 Max | where to check vo2 max on iphone, where to find vo2 max on iphone, how to check vo2 max on iphone | 31 (index) | 8-11 | vo2max/ (the app page) | 1 | No page owns this how-to. Google stands the app page in |
| 9 | Hockey | hockey scoring app | 27 (index) | 37.6 | hockey/ | xG 8 (6.1), Copilot 6 | Google shows no xG impressions; Bing does |
| 10 | Vitals | how many calories do I burn a day (18 variants), apple watch active vs resting calories (Bing, 9 variants) | 26 + 5 | 66.9 | vitals/how-many-calories-do-i-burn-a-day.html | 10 (6.1) on active-vs-resting | Google: page 7. Bing ranks the active vs resting page on page 1 |
| 11 | Queasy | apple watch motion sickness, apple watch nausea relief, does closing your eyes help | 26 + 12 | 8.3 index, 26.4 road trip | queasy/ | 0 | Health topic: comparison pages here get rejected |
| 12 | Cribbage | how to count a cribbage hand, peg counter app; Bing: best cribbage app for iphone without auto score | 20 + 6 | 7.2 | cribbage/how-to-count-a-cribbage-hand.html | 5 (2.3-8), Copilot 5, 1 click | |
| 13 | Baseball | statcast metrics, what does xwoba mean, mlb percentile rankings | 16 + 8 | 10-13 | baseball/, statcast-metrics-explained.html | 2 | |
| 14 | Posture | desk posture checklist | 13 + 8 | 9.3 | posture/desk-posture-checklist.html | 2 | |
| 15 | Ironman | triathlon splits, what is t1 in ironman | 11 + 3 | 6.5 | ironman/triathlon-splits-explained.html | 2 (3.0), Copilot 11 on best-triathlon-results-app | |
| 16 | Skat | (Bing, German) skat lernen, was bedeutet mit re, welche stiche | 11 | 7.9 | skat/ | 3 (6.7) | Site is already German |
| 17 | Headaches | headache diary, apple watch migraine tracker (pos 1) | 24 index + 4 | 11.3, 55 | headaches/ | 7 (6.7) on diary page | Bing likes the diary page, Google does not |
| 18 | Sheepshead | sheepshead app, sheepshead card game app | 7 | 2-5 | sheepshead/ | 0 | Already top 5 |
| - | SongHero (not an App Store app) | songhero; clone hero chart generator / auto charter / ai chart maker (10 variants); spotify to clone hero (3 variants, 17 impr, pos 2-3.4); clone hero song maker | 1,316 | 3.9 | songhero/ | 95 (7.6), Copilot 76 | Spotify family has no page of its own |

Nothing else on /ios/ passed 10 impressions: Quit Zyn 12, GLP 6, Electrician 3, Shoes On 2,
Baby Docs 2, Elder Hub 2, Baby 1, Pickleball 1.

## App Store downloads by language market (Jul 29-Oct 25)

"Non-English" counts downloads from storefronts mapped to a language (US, UK, Canada, Australia, NZ,
Ireland, India, Philippines, Singapore and South Africa count as English). Ranking = downloads +
impressions/50. Figures: downloads/impressions.

| App | Downloads | Non-English share | Top 10 languages |
|---|---|---|---|
| Total Calories | 1,666 | 56% | de 150/1878, ja 61/5261, fr 125/1060, zh-Hans 49/4315, es 64/1360, pl 52/480, ru 35/1067, it 43/325, pt-BR 31/922, ar 35/717 |
| Mahj | 1,134 | 6% | es 32, vi 11, id 11, nl, ar, ru, fr, de, uk, th (all under 35) |
| Sober | 747 | 42% | uk 67, pl 61, de 43, ru 29, nl 25, es 14, fr 12, zh-Hans 4, vi 7, cs 9 |
| Baseball | 618 | 13% | es 28, ja 17, zh-Hant 12, zh-Hans 3, ko 7, fr 5, pt-BR 3, it 3, ar 1, ru 0 |
| Quit Zyn | 244 | 55% | de 59, ru 11, fi 9, cs 8, sv 6, da 7, nl 5, es 4, sk 5, zh-Hans 1 |
| Bridge | 240 | 76% | tr 46, nl 36, th 17, fr 13, zh-Hant 8, de 12, da 9, ar 0/588, ja 6, ru 8 |
| VO2 Max | 149 | 64% | de 17, ru 11, ar 4, fr 10, ja 6, nl 6, es 6, zh-Hant 5, th 3, cs 4 |
| Dream Cart | 142 | 63% | zh-Hans 16, ar 4, ru 8, th 8, tr 1, pt-BR 8, ja 2, es 2, de 13, id 3 |
| GLP | 134 | 30% | pt-BR 11, tr 7, es 5, ru 3, zh-Hant 2, hu 2, fr 2, de 1, it 1, nl 1 |
| Skat | 131 | 95% | de 121 (site already German) |
| Football | 115 | 50% | es 42 (Mexico 38), de 6, ar 2, tr 1, fr 1, it 2, th, nl 2, ja 1, ko 1 |
| Ironman | 84 | 10% | under 3 per language |
| Headaches | 79 | 51% | de 4, ja 3, ru 3, da 3, fi 3, pl 2, pt-PT 2, nb 2, zh-Hans 0/504, ar 0/215 |
| Cribbage | 78 | 10% | under 3 per language |
| Baby | 74 | 80% | it 15, pt-BR 12, es 6, de 4, vi 2, fr 2, sv 2, ru 1, sr 2, he 2 |
| All others | under 55 each | | under 10 downloads per language |

App UI localizations found in local checkouts (`.xcstrings`): Total Calories 35 languages, Sober 17,
Bridge 11, Baseball 7, Mahj 6, Sheepshead en/es. The other checkouts show none, and local checkouts
lag origin, so confirm per app before localizing its page. Every App Store listing except Elder Hub,
Baby Docs and Sunset carries the full set of store locales.

## Click tracking

Own-app App Store links already carry `pt=128748779&ct=jw-<app>-<page>`. As of 2026-10-25 the ASC
campaign report returned no rows for any `ct=jw-` tag: /ios/ pages sent 7 Google clicks in 16 days,
under Apple's reporting threshold. Per-page App Store click-through is not measurable yet.
