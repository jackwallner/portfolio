# Portfolio UX Audit Report

## Site Structure

```
portfolio/
├── index.html (home - project grid)
├── repos.html (all repositories list)
├── 404.html (error page)
├── home.css (shared styles)
├── e3fit/
│   └── index.html (more info)
├── flight-tracker/
│   └── index.html (more info)
├── statscout/
│   └── index.html (more info)
├── streaks/
│   └── index.html (more info)
├── headaches/
│   └── index.html (more info - UNUSED, links go to external)
└── vitals/
    └── index.html (more info - UNUSED, links go to external)
```

## Critical Issues Found

### 1. PLACEHOLDER LINK - BROKEN
**Location:** Streak Finder App Store link  
**Issue:** `APP_STORE_ID` placeholder still in URL  
**Impact:** Users click → 404 on App Store  
**Fix:** Replace with actual App Store ID when available

### 2. INCONSISTENT NAVIGATION PATTERNS

| Project | Title Link | "Site" Link | "More info" Link | Result |
|---------|-----------|-------------|------------------|--------|
| Total Calories | External landing | External landing | Internal (UNUSED) | Confusing - 2 ways to same place |
| Headache Logger | External landing | External landing | Internal (UNUSED) | Confusing |
| Streak Finder | External landing | External landing | Internal (UNUSED) | Confusing |
| Baseball Savvy StatScout | None (plain text) | None | Internal | Dead end for mobile users |
| e3fit.me | Internal | External | Internal | 2 internal links redundant |
| Flight Tracker | None (plain text) | None | Internal | Dead end for mobile users |

### 3. INACCESSIBLE PROJECT TITLES
**Issue:** StatScout and Flight Tracker titles are NOT clickable  
**Impact:** Mobile users expect to tap the title to learn more  
**Fix:** Make all project titles clickable links

### 4. NAVIGATION TRAPS

#### From Detail Pages:
- All detail pages have "← Back to portfolio" ✓
- But NO link to external site (e3fit has it, others don't)
- Missing: "View on App Store" primary CTA on app detail pages

#### From Portfolio Home:
- Total Calories, Headache Logger, Streak Finder → external landing pages
- But user might expect to stay IN portfolio for consistency

### 5. VISUAL INCONSISTENCY

#### Stamp/Badge Usage:
- "App Store" = green (live)
- "TestFlight" = yellow (wip)  
- "Live" = green (for e3fit, Flight Tracker)

**Issue:** "Live" vs "App Store" ambiguous - both green  
**Clarification needed:** "Live" = web service, "App Store" = iOS app

### 6. LINK TARGET CONFUSION

Users can't tell what opens in new tab vs same tab:
- External sites: target="_blank" (good)
- Internal "More info": same tab (good)
- But visual indication (↗) only on some external links

### 7. MOBILE FRICTION POINTS

#### Project Cards:
- 2-column grid → 1-column at 640px ✓
- But title + stamp wrap awkwardly on small screens
- "More info" links might be too small for touch (44px min?)

#### Detail Pages:
- Specs tables: first column 140px fixed width
- On very small screens (<400px), content may overflow

### 8. EMPTY STATES / DEAD ENDS

#### repos.html:
- Loading state shows "Loading..."
- Error state shows "Error loading repositories"
- No retry button on error
- No fallback if JavaScript fails

#### 404.html:
- "That page isn't here" - helpful ✓
- Links back to portfolio ✓
- But: missing link to home page from detail pages if user lands directly

### 9. MISSING INTERACTION FEEDBACK

- No hover states defined for `project-card` on desktop
- No active/tap states for mobile
- No loading states for external links

### 10. CONTENT DISCOVERY ISSUES

#### GitHub Chart:
- Below the fold on mobile
- Shows "Public repos only" disclaimer
- But: user might not scroll past project grid

#### Footer Links:
- Email, GitHub, LinkedIn only on detail pages
- Home page has them in header ✓
- repos.html footer links?

## User Journey Friction Analysis

### Journey 1: Hiring Manager Scrolling Portfolio
1. Lands on portfolio home ✓
2. Sees 6 projects in grid ✓
3. Wants to see more about Total Calories
4. **FRICTION:** Two options - "Site ↗" or "More info"? Which to click?
5. Clicks "Site ↗" → goes to external landing page
6. **FRICTION:** External page has DIFFERENT design, different nav
7. Wants to come back → browser back button (works) ✓

### Journey 2: Mobile User Tapping Project
1. On mobile, taps "Baseball Savvy StatScout" title
2. **BUG:** Title is plain text, not clickable!
3. Tries "More info" → goes to detail page ✓
4. On detail page, wants to see it on App Store
5. **FRICTION:** Only "Source ↗" link - no App Store link!
6. Has to go back, click external GitHub link

### Journey 3: Direct Landing on Detail Page
1. Gets link to `portfolio/statscout/`
2. Reads about the project ✓
3. Wants to try it
4. **ISSUE:** No direct "View on App Store" or "Visit Site" link!
5. Only options: Back to portfolio, Email, GitHub

## Recommendations

### Immediate Fixes:

1. **Fix broken App Store link:** Replace `APP_STORE_ID` placeholder

2. **Make all project titles clickable:**
   - StatScout title → detail page
   - Flight Tracker title → detail page
   - e3fit title → detail page

3. **Add primary CTA to detail pages:**
   ```html
   <div class="project-links" style="margin-bottom: 2rem;">
       <a href="APP_STORE_URL" class="primary-cta">View on App Store</a>
       <a href="LIVE_SITE_URL">Visit Live Site</a>
   </div>
   ```

4. **Consolidate navigation:**
   - Option A: All projects link to internal detail pages first
   - Option B: Remove "More info" for apps that have external landing pages
   - Recommended: A for consistency

### UX Improvements:

5. **Add hover/active states:**
   ```css
   .project-card:hover { transform: translateY(-2px); }
   .project-card:active { transform: translateY(0); }
   ```

6. **Clarify status badges:**
   - "On App Store" (green)
   - "In TestFlight" (yellow)  
   - "Live Site" (blue - different color!)

7. **Add "Top" link on long detail pages:**
   - Vitals/Headaches/Streaks detail pages are long
   - User scrolls through specs, wants to go back to top

8. **repos.html improvements:**
   - Add retry button on error
   - Show cached results if available
   - Add loading skeleton instead of "Loading..." text

### Navigation Consistency:

| Project | Title | Primary CTA | Secondary |
|---------|-------|-------------|-----------|
| Total Calories | Link to detail | "View on App Store" | "Source ↗" |
| Headache Logger | Link to detail | "View on App Store" | "Source ↗" |
| Streak Finder | Link to detail | "View on App Store" | "Source ↗" |
| StatScout | Link to detail | "Join TestFlight" | "Source ↗" |
| e3fit.me | Link to detail | "Visit Live Site" | "Source ↗" |
| Flight Tracker | Link to detail | "View History" | "Source ↗" |

All detail pages should have:
- Back to portfolio
- Primary CTA (App Store / Live Site / TestFlight)
- Source code link
- Email support
