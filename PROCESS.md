# Rebuilding the Userology Help Center
## A Documentation of My Problem-Solving Process

---

## Where This Started

I had a static Zendesk export—24 articles, 27 videos, basic HTML pages. My goal was simple: turn this into a functional help center that users could actually navigate and use.

This document walks through how I approached the problem, what I built, and the reasoning behind each decision.

---

## Navigation Map

**Discovery & Analysis**
- [Initial User Testing](#initial-user-testing)
- [Problems I Identified](#problems-i-identified)

**Building Solutions**
- [Making Search Work](#making-search-work)
- [Creating a Workflow Visualization](#creating-a-workflow-visualization)
- [Applying Brand Consistency](#applying-brand-consistency)
- [Fixing Mobile Experience](#fixing-mobile-experience)
- [Adding Engagement Tools](#adding-engagement-tools)

**Reflection & Results**
- [Technical Decisions](#technical-decisions)
- [What Failed & Why](#what-failed--why)
- [Success Metrics](#success-metrics)
- [Key Files & Features](#key-files--features)

---

## Initial User Testing

Before writing any code, I needed to understand what was actually broken. I opened the site locally and used it like a regular user would.

I asked myself basic questions:
- Can I find information about setting up my first study?
- If I have a specific question, can I search for it?
- Can I browse videos easily?
- Do I understand where to start?

The experience revealed multiple friction points that I documented for later fixing.

---

## Problems I Identified

After testing, I grouped issues into categories:

**Search Functionality**
The search bar existed but was completely non-functional. When users typed queries, nothing happened. This was misleading—it looked like a feature but did nothing.

**Content Discovery**
Articles and videos were presented as long, flat lists. No filtering, no categorization, no way to narrow down content by topic. Users had to scan every single title.

**Information Architecture**
No clear indication of where articles fit in the Userology workflow. A new user seeing 24 article titles wouldn't know where to begin or what order made sense.

**User Engagement**
No feedback mechanisms. No way to know if articles were helpful. No related content suggestions. Users would read one article and leave.

**Visual Consistency**
The default theme didn't match Userology's actual branding—different colors, different feel. This created a disconnect between the main product and its documentation.

**Mobile Usability**
Testing on actual devices revealed broken layouts, unreadable text sizes, and touch targets that were too small.

### My Prioritization Approach

I couldn't fix everything at once, so I prioritized based on:
- **User impact**: How many people does this affect?
- **Foundation vs. polish**: Does this need to work before I can build other features?
- **Entry points**: Where do users first interact with the site?

This led me to tackle search first, then information architecture, then visual consistency, then engagement features.

---

## Making Search Work

## Making Search Work

The broken search bar was the first thing I fixed.

**The Build Process:**

I wrote a Python script to extract content from all HTML files:
- Article titles
- Section headings
- Body text

This data went into a JSON file that JavaScript could search through in real-time.

For the search interface, I built:
- A scoring algorithm (title matches scored highest, then sections, then body content)
- Live dropdown results as users type
- Keyboard navigation (arrow keys + Enter)
- 300ms debounce to prevent lag
- Category tags showing which section each result belongs to

**The Path Problem:**

Search worked on the homepage but broke on article pages. The issue was relative paths—`../search-index.json` failed when pages were in different directory depths.

Solution: A `getBasePath()` function that detects the current page's location and constructs the correct path to the search index.

**Research I Did:**

I looked at how Intercom and Zendesk implement help center search. The pattern was clear: instant, inline results. No "press Enter and wait" experience. I applied this pattern.

---

## Creating a Workflow Visualization

The homepage had all 24 articles in alphabetical order. Functional, but not helpful for someone who's never used Userology before.

**The Problem:**
Users don't think in alphabetical terms. They think in workflows: "First I set up a study, then I configure it, then I launch it."

**Options I Considered:**
- Tabbed categories (hides content, forces clicking)
- Accordion menus (same issue)
- Keep the flat list (boring, unhelpful)

**What I Built:**

A tree-line roadmap showing the actual Userology workflow:

```
Study Setup → Interview Plan → Study Settings → Launch → 
Responses & Recordings → Results & Reports
```

Visual design:
- Vertical spine with numbered nodes (1-6)
- Connecting lines showing progression
- Each node contains relevant topic cards
- Smooth animations (fade-in, subtle pulse)

This gives users immediate context. They can see the entire product journey and click into whichever stage is relevant.

---

## Applying Brand Consistency

The default theme was generic blue/white. Userology's actual site uses dark purple tones and space-black backgrounds.

**What I Did:**

I grabbed screenshots of the Userology website and color-picked exact values:
- Background: `#0A0A0F`
- Primary purple: `#8B7BF7`
- Card backgrounds: `#1A1625`
- Borders: `#2A2538`

Added glass-morphism effects:
- Backdrop blur on cards
- Semi-transparent overlays
- Purple glow on hover states

Matched typography:
- Figtree for body text
- Inter for headings

**Deployment Issue:**

GitHub Pages aggressively cached the old CSS. I had to add cache-busting query parameters to force browsers to reload stylesheets.

**Text Readability Problem:**

The dark theme made some text nearly invisible. White text on gradient backgrounds had poor contrast.

I tried multiple fixes:
1. Force white color → didn't work, gradient still interfered
2. Add text shadow → better, but still blurry
3. Remove all gradient properties entirely → finally fixed it

Applied this to roadmap titles, video cards, article headings, and related article sections.

---

## Fixing Mobile Experience
```css
/* BEFORE (broken) */
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));

/* AFTER (fixed) */
grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
```

That `min(280px, 100%)` means "use 280px, but never exceed 100% of viewport width."

I also had to add:
```css
* {
  box-sizing: border-box;
  min-width: 0;  /* Stops grid children from blowing up */
}
```

## Fixing Mobile Experience

**The Testing Gap:**

Chrome DevTools showed everything working perfectly on mobile viewports. Then I tested on my actual phone and discovered the truth—broken layouts, tiny text, touch targets under 44px.

**The Core Issue:**

CSS grid using `minmax(280px, 1fr)` forced 280px cards even when the viewport was narrower. Result: horizontal overflow.

The fix:
```css
/* Changed from */
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));

/* To */
grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
```

Also added:
```css
* {
  box-sizing: border-box;
  min-width: 0;
}
```

Set up responsive breakpoints:
- 768px: 2-column grids
- 640px: 1 column, larger text
- 480px: simplified navigation

For video carousel:
- 85% width cards (so next card peeks out)
- `scroll-snap-type: x mandatory` for smooth scrolling

**Takeaway:** Browser simulators can't replace real device testing.

---

## Adding Engagement Tools

After the foundation was solid, I added four features to improve user engagement:

**1. Article Feedback System**

Thumbs up/down buttons on every article. "Not helpful" triggers a comment box. LocalStorage prevents duplicate votes. Analytics hooks included for future tracking.

Data structure:
```javascript
{
  articleId: "article_25456988151453",
  vote: "helpful" | "not-helpful",
  comment: "Could use more screenshots",
  timestamp: "2025-12-05T10:30:00Z"
}
```

**2. Related Articles**

Three curated suggestions at the bottom of each article. Manually mapped all 72 relationships (24 articles × 3 suggestions each).

Example:
```python
"article_25456988151453": [
    ("article_25561782334749", "Interview Plan", "Discussion Guide"),
    ("article_25562045316637", "Study Settings", "AI Moderator"),
    ("article_25562330763805", "Launch", "Previewing Study")
]
```

**3. Breadcrumb Navigation**

Simple path showing: `Home > Browse Topics > Section > Article`

Clickable except for current page. Uses `aria-current="page"` for accessibility.

**4. Enhanced Search Results**

Added category tags to search dropdown. Shows "View all X results →" footer. Better visual hierarchy.

**The Automation Script:**

Python script to apply all four features to 24 articles automatically. Checks for existing enhancements to avoid duplicates.

```python
def enhance_article(filepath):
    # 1. Add breadcrumb
    # 2. Inject feedback widget
    # 3. Generate related articles
    # 4. Write back to file
```

---

## Technical Decisions

**Why Plain HTML/CSS/JS:**

I could've used React, Algolia, or a CMS. Instead:
- GitHub Pages hosting (free forever)
- Instant load times (no bundle)
- Simple deployment (git push)
- SEO-friendly (static HTML)
- Offline capability

Trade-offs:
- Manual content updates (acceptable for documentation)
- No real-time analytics dashboard (can add later)
- But: zero hosting costs, 100% uptime

**Benchmarking Strategy:**

Studied Intercom, Zendesk, Linear, Maze, and Dovetail. Looked for patterns that multiple successful products use—those are proven solutions worth borrowing.

**Design Consistency:**

Same card styles, hover effects, and spacing throughout. Users learn the pattern once and apply it everywhere.

---

## What Failed & Why

**Edge Case Testing:**

First search version broke with special characters and unusual article titles. Lesson: test weird inputs from the start, not just happy paths.

**Simulator Reliance:**

DevTools looked perfect. Real iPhone showed multiple issues. Lesson: always test on actual devices.

**Scope Creep:**

Tried fixing search, roadmap, and theme simultaneously. Got confused, made mistakes. Lesson: tackle one problem at a time.

---

## Success Metrics

How I'd measure if this actually worked:

**Usage Metrics:**
- Search usage rate: % of sessions using search (target: >40%)
- Search success rate: % of searches leading to article clicks (target: >60%)
- Pages per session: how much users explore (target: >2.5)
- Time to first article: how fast users find content (target: <30s)

**Outcome Metrics:**
- Support ticket volume: fewer "how do I..." questions (target: ↓20%)
- Helpfulness votes: article quality signals
- Bounce rate: users leaving immediately (target: lower)

**User Journey Changes:**

Before:
1. Land on homepage → see alphabetical list → feel lost
2. Try search → nothing happens
3. Read one article → leave

After:
1. Land on homepage → see workflow roadmap → understand context
2. Use search → instant results with categories
3. Read article → vote on helpfulness → click related article → continue learning

Estimated impact: pages per session should increase from ~1.2 to ~2.8.

---

## Key Files & Features

**Modified Files:**
- Core pages (4): index.html, categories.html, articles.html, videos.html
- Article pages (24): all article_*.html files
- Section pages (7): all section_*.html files
- Styles: css/style.css (~500 lines added)
- JavaScript: js/main.js (~250 lines added)

**Features Shipped:**
- Working search with keyboard navigation
- Tree-line workflow roadmap  
- Brand-consistent dark theme
- Article feedback system
- Related articles (72 mappings)
- Breadcrumb navigation
- Enhanced search with category tags
- Full mobile responsiveness
- Python automation for bulk updates

**Live Site:** https://dhruvi-sisodiya.github.io/userology-helpdesk/

---

*This documentation reflects my actual build process—problems identified, solutions implemented, and lessons learned along the way.*
