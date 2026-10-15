# Search results baseline and competitor read (2026-10-13)

Google US, logged-in Chrome with `pws=0`, top organic results (about 8 per page) for the target
query of each guide and comparison page. 52 of 63 queries ran before Google showed a CAPTCHA; the
11 not run: EPA per play, xG in hockey, true shooting, triathlon splits, 5 love languages
examples, medication list for aging parent, newborn paperwork checklist, newborn diapers by day,
starting a task with ADHD, conduit fill, third shot drop. Bing returned bot-filtered junk
(dictionary pages for every "best ..." query), so it has no usable baseline; use Bing Webmaster
Tools data instead.

## Where we stand
- jackwallner.com: on page 1 for 0 of 52. Expected: most pages were published or first submitted
  on Oct 12-13, and Search Console still shows "Processing data" for page indexing.
- Our App Store listings: Baseball Savvy StatScout is #2 for "best baseball savant app". No other
  listing of ours made page 1.
- Search Console Performance (data to Oct 11): 63 impressions, 11 clicks, all from SongHero
  queries ("songhero", "clone hero ai chart generator", "clone hero auto charter").

## What ranks for "best X app" queries
- A rival app maker's own comparison article is on page 1 for 15 of 22 queries (sobrmate,
  shotsyapp, meagain, peakvo2trainer, playsheepshead, baseballnut, quitzynapp, getvelm,
  journeymaniq, loomi, routinery, reassign, mindoryapp, dizzout, carsick.app, habi, habitbox,
  habitpocket, habitdoom, babydaybook, betteroo, bamgoodtime, mahjong4friends, connectedcouples,
  postureletics). Our format is the one that wins these SERPs.
- Reddit is on page 1 for about 15 of 22. App Store and Google Play listings fill most of the rest.
- Ranking rival pages vs ours: they run 1,500 to 4,800 words (ours 1,000 to 1,400), one H2 per app
  (ours use H3), FAQPage schema on most, and most were updated within the last 6 weeks (Dizzout
  updated its page today).

## Winnability
Weak page 1 (forums, social posts, small shop blogs, few results). Most likely to rank first:
- Mah jongg guides: "charleston mah jongg" (only 4 organic results), "how to read the mah jongg
  card", "how to play american mah jongg", "mah jongg joker rules", "american mah jongg scoring",
  "mah jongg glossary".
- Comparisons: best american mahjong app, best sheepshead app, best cribbage app, best baseball
  savant app, best quit zyn app, streaks app alternative, best app for time blindness, best
  journeyman electrician test prep app, best motion sickness app.
- Guides: apple watch streak broken, how to talk about sports, how to play sheepshead.

Held by health systems, government or big calculator sites (Cleveland Clinic, Mayo, Healthline,
calculator.net, OSHA, NIH, MLB). Long shots for a new domain: bmr calculator, tdee calculator, how
many calories do i burn a day, caffeine half life, barometric pressure headaches, migraine
triggers, headache diary, vo2 max chart, motion sickness road trip, sobriety milestones, how to
quit zyn, what is xwoba, desk posture checklist.

## Gaps found
- People Also Ask questions per query were captured and are being added to each page's FAQ (with
  FAQPage schema).
- Apps on Google page 1 that our comparison does not mention: Snusless and Quit Pouches (quit zyn),
  Posture AI (posture), Carsick and KineStop (motion sickness), NEC Journeyman Electrician and
  Electrician Test Prep 2026 (electrician), MyTherapy (medication), theScore (NFL stats), Ultimate
  Cribbage Classic (cribbage), MyFitnessPal and FatSecret (calories burned; food loggers, worth a
  FAQ explaining the difference).

## Re-check
Re-run these queries around 2026-11-10, after Google has indexed the pages. Pace about 40 searches
per session to avoid the CAPTCHA.

## Done the same day
- People Also Ask questions answered on 38 pages (visible FAQ + FAQPage schema). Skipped: the
  mahjong "1/4/7 rule" and "Move streak not updating" (no reliable source).
- "Other apps you will see" sections added for the page-1 apps listed under Gaps (8 comparison
  pages; Cribbage Pro Classic noted as the Mac version of Cribbage Pro). MyFitnessPal covered by a
  calories-page FAQ instead.
- SongHero title and description retargeted to "clone hero chart generator" and "auto charter".

## Removed 2026-10-14
Protein Tracker and Daylight came off the site (both removed from App Store Connect), including
the "time in daylight apple watch" and "track protein apple watch" guides. Skip those queries in
the re-check.

## Indexing submitted 2026-10-14
- Bing URL Submission: 96 main pages (all priority 0.7+ sitemap URLs), quota 100 to 4.
- Google Request Indexing: 10 pages (baseball, streaks alternative, quit zyn, vo2 max, nfl stats, bridge, cribbage, baby tracker, time blindness x2). 5 were "URL is unknown to Google" though listed in sitemap.xml since Oct 13 (Google has not re-read it yet). Next: guides/ hub and the remaining comparison pages on Oct 15.

## Install attribution (2026-10-14)
- Every link to our own apps on jackwallner.com now carries `pt=128748779&ct=jw-<app>-<page>&mt=8` (182 links on 75 pages; apps index uses `ct=jw-apps-index`). JSON-LD URLs stay untagged. Run `scripts/tag_app_store_links.py <repo>/docs <slug>` after adding a page or app.
- Read installs per page in App Store Connect > app > Analytics > Acquisition > Campaigns. Apple hides values under 5 devices.
- Baseline before tags (Aug 15 to Oct 12, Web Referrer by domain, all apps): google.com 347 product page views and 149 downloads (Mahj, Total Calories, Sober, Baseball lead); chatgpt.com 10 views and 9 downloads (Total Calories); jackwallner.com 0, below Apple threshold.

## Impact check (2026-10-14 evening)
- Google Search Console (data through Oct 12): 17 clicks, 131 impressions, all clicks to SongHero. App pages: 1 to 2 impressions each (mahj, sheepshead, elderhub, babydocs, bridge, dreamcart, apps index). Page indexing report still "processing data".
- Bing Webmaster Tools: no search performance data yet.
- App Store web referrals by week, all apps (views/downloads), June to Oct 13: google.com grew from 3/1 (week of Jun 1) to about 40/15 a week and has been flat since mid-September (Sep 14: 47/21, Sep 21: 43/14, Sep 28: 36/12, Oct 5: 43/18). chatgpt.com peaked at 3/3 (week of Aug 24) and was 0 in 3 of the last 4 weeks; nearly all of it is Total Calories. These are clicks from Google or ChatGPT straight to the App Store listing, not via jackwallner.com, so they predate this work and are the baseline it should lift.
- Google Play links now carry `referrer=utm_source=jackwallner.com&utm_campaign=jw-<page>` (Tri Locker page, homepage, apps index).
- Next read: about Oct 28 (GSC impressions per app page, ASC Campaigns report, weekly google.com and chatgpt.com referrals vs the 40/15 baseline).

## Indexing submitted 2026-10-15 (about 1:15 PM PT)
- Google Request Indexing, 10 accepted: guides/, mahj/learn/charleston, and the 8 remaining comparison pages (posture, bond love language, queasy motion sickness, ironman triathlon results, sheepshead, beste-skat-app, elderhub medication tracker, electrician journeyman). The 11th (mahj/learn/jokers) hit Quota Exceeded. Most showed "Discovered - currently not indexed"; queasy, ironman and electrician were still "URL is unknown to Google".
- Every comparison page has now been requested once. Next Google batch (Oct 16 after about 1:15 PM PT): mahj/learn/jokers, card-sections, scoring-and-table-rules, glossary, then app pages not yet requested (skat, sheepshead, electrician, ironman, babydocs, elderhub, posture, sports, bond, baby, fitness-streaks, vo2max, queasy).
- IndexNow (Bing, Yandex): 98 pages changed since Oct 14 evening (campaign-tagged links).

## Indexing outcome check (2026-10-15 afternoon, live URL Inspection)
20 of the 31 URLs requested Oct 12-14 are indexed. Google crawled each within minutes of the request.
- Oct 12 app pages: 10 of 11 indexed (mahj, /ios/, vitals, headaches, simpleglp, baseball, football,
  quitzyn, cribbage, bridge). sober/ is "Crawled - currently not indexed".
- Oct 13: 4 of 10 indexed (mahj how-to-play, vitals calories-a-day, cribbage hand count, vo2 max chart).
  Crawled, not indexed: mahj best-american-mahjong-app, sober i-am-sober-alternative,
  headaches best-headache-tracker-app, quitzyn how-to-quit-zyn, simpleglp best-glp-1-tracker-app.
  Never crawled ("Discovered"): vitals best-app-to-track-calories-burned-apple-watch.
- Oct 14: 6 of 10 indexed (guides/, baseball best-baseball-savant-app, football best-nfl-stats-app,
  bridge best-bridge-app-for-beginners, baby best-baby-tracker-app, time best-app-for-time-blindness).
  Crawled, not indexed: cribbage best-cribbage-app, quitzyn best-quit-zyn-app,
  fitness-streaks streaks-app-alternative. Never crawled: vo2max best-vo2-max-app-for-apple-watch.
- Pattern: app pages and guides index; comparison pages are about half "crawled, not indexed"
  (Google judged them not worth indexing yet). Re-requesting does not change that verdict; inbound
  links and time do.
- GSC Performance still ends 2026-10-13 (7 days: SongHero 203 of 215 impressions, mahj 5, others
  1 each). Pages report last updated 2026-10-11 (26 indexed), so it predates all requests.
- Bing Search Performance: "check back in 48 hours", no data yet.

## Install outcome check (2026-10-15, RevenueCat + ASC web dashboard, data through Oct 14)
Baseline = Sep 14 to Oct 11 (28 days), post = Oct 12 to 14 (3 days), per day.
- RevenueCat new customers, fleet: 73.4 to 90.7 a day (+24%). Mahj 14.4 to 22.3 (all iOS), trials
  4.1 to 6.3. Others within noise (Total Calories 22.4 to 21.3, Sober 8.4 to 9.7).
- ASC Web Referrer by domain, all apps: google.com 6.0 views / 2.3 downloads a day before, 4.3 / 3.0
  after. Flat. chatgpt.com 0 after. jackwallner.com still below Apple's threshold. Campaigns (ct=jw-*)
  return no rows for any app yet (under 5 devices each, or no tagged installs).
- Mahj downloads by source (ASC): App Store Search 11.5 to 16.3 a day; App Referrer 1.3 to 5.7 a day
  (WhatsApp page views 3 in 28 days, then 12 in 3 days, so someone shared it in a group chat); Web
  Referrer 1.2 to 1.0. The Mahj lift is search plus a WhatsApp share, not Google or the site.
- Verdict: no measurable install impact from indexing yet. Expected, since GSC shows almost no
  impressions on app pages. Re-read on Oct 28 as planned.
