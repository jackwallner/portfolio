# Google Request Indexing queue

Search Console allows 10 Request Indexing calls per rolling 24 hours (per Google account). The
`google-index-daily` scheduled task works down this list once a day: it requests the first 10
unchecked URLs, ticks each one with the date and the inspection status it saw, and stops on
"Quota exceeded". URLs are relative to `https://jackwallner.com/`. Pages already requested
(Oct 12-15) are logged in [indexing-2026-10-12.md](indexing-2026-10-12.md); do not re-request
"Crawled - currently not indexed" pages, it does not change Google's verdict.

## Mahj learn guides
- [ ] ios/mahj/learn/jokers.html
- [ ] ios/mahj/learn/card-sections.html
- [ ] ios/mahj/learn/scoring-and-table-rules.html
- [ ] ios/mahj/learn/glossary.html

## App pages not yet requested
- [ ] ios/skat/
- [ ] ios/sheepshead/
- [ ] ios/electrician/
- [ ] ios/ironman/
- [ ] ios/babydocs/
- [ ] ios/elderhub/
- [ ] ios/posture/
- [ ] ios/sports/
- [ ] ios/bond/
- [ ] ios/baby/
- [ ] ios/fitness-streaks/
- [ ] ios/vo2max/
- [ ] ios/queasy/
- [ ] ios/time/
- [ ] ios/adhd/
- [ ] ios/caffeine/
- [ ] ios/pickleball/
- [ ] ios/hockey/
- [ ] ios/basketball/
- [ ] ios/dreamcart/
- [ ] (home page, https://jackwallner.com/)

## Guides
- [ ] ios/sober/sobriety-milestones.html
- [ ] ios/simpleglp/glp-1-injection-site-rotation.html
- [ ] ios/baseball/statcast-metrics-explained.html
- [ ] ios/babydocs/newborn-paperwork-checklist.html
- [ ] ios/caffeine/caffeine-half-life.html
- [ ] ios/bridge/bridge-bidding-for-beginners.html
- [ ] ios/sheepshead/how-to-play-sheepshead.html
- [ ] ios/skat/skat-regeln-einfach-erklaert.html
- [ ] ios/electrician/how-to-calculate-conduit-fill.html
- [ ] ios/headaches/how-to-keep-a-headache-diary.html
- [ ] ios/football/what-is-epa-per-play.html
- [ ] ios/ironman/triathlon-splits-explained.html
- [ ] ios/baby/newborn-wet-dirty-diapers-first-week.html
- [ ] ios/bond/5-love-languages-examples.html
- [ ] ios/fitness-streaks/apple-watch-streak-broken.html
- [ ] ios/vitals/tdee-calculator.html
- [ ] ios/vitals/bmr-calculator.html
- [ ] ios/vitals/apple-watch-active-vs-resting-calories.html
- [ ] ios/vitals/guides.html
- [ ] ios/headaches/barometric-pressure-headaches.html
- [ ] ios/headaches/migraine-trigger-tracking.html
- [ ] ios/posture/desk-posture-checklist.html
- [ ] ios/sports/how-to-talk-about-sports.html
- [ ] ios/queasy/motion-sickness-road-trip.html
- [ ] ios/hockey/what-is-xg-in-hockey.html
- [ ] ios/basketball/true-shooting-percentage-explained.html
- [ ] ios/elderhub/medication-list-for-aging-parent.html
- [ ] ios/adhd/how-to-start-a-task-with-adhd.html
- [ ] ios/time/time-blindness-always-late.html
- [ ] ios/pickleball/third-shot-drop-vs-drive.html
- [ ] ios/pelojack/apple-watch-heart-rate-peloton-bike-plus.html

## Side projects
- [ ] ios/pelojack/
- [ ] e3fit/
- [ ] flight-tracker/
- [ ] spotify-bot/
