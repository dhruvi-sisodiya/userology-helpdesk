# Userology Helpdesk

Offline Help Center with automated JSON-to-HTML regeneration.

## File Organizational Changes

**Folder restructure:**
- All HTML, CSS, JS, videos, and attachments moved to `offline_help_center/` directory
- Created organized subfolders: `sections/`, `articles/`, `categories/`, `videos/`, `attachments/`, `css/`, `js/`
- Updated all internal links and paths to reflect new structure (e.g., `../css/style.css` for articles, `sections/section_*.html` for navigation)

**JSON data re-engineering:**
- `reconstruct_jsons.py` — Extracts minimal JSON from existing HTML files in `offline_help_center/`
  - Parses categories, sections, and articles from HTML content (not headers)
  - Normalizes section names to match presentation layer (emoji mappings)
  - Outputs to `zendesk_export_userology/`: `categories.json`, `sections.json`, `articles.json`, `manifest.json`
  - Only essential fields stored: `id`, `name`, `description` (categories); `id`, `name`, `category_id` (sections); `id`, `title`, `body`, `section_id`, `updated_at` (articles)

- `generate_offline_website.py` — Regenerates static site from minimal JSON
  - Acts as pure template engine (no URL rewriting, no attachment downloading)
  - Reads from `zendesk_export_userology/`, writes to `offline_help_center/`
  - Emojis and descriptions hardcoded in generator (presentation layer, not data layer)
  - Conditionally includes search container and script tags based on page type

**Regeneration:**

```powershell
python reconstruct_jsons.py
python generate_offline_website.py
python build_search_index.py
```

**Note:** Run `build_search_index.py` after regenerating the site to update the search index with latest articles.

## UI Changes

**Color & Theme:**

- Dark purple gradient theme: `#8B7BF7`, `#6366F1`, background `#0A0A0F`
- Card backgrounds: `#16161F` with purple glow on hover
- Section headings: gradient text `linear-gradient(0deg, rgb(96, 91, 255) 0%, rgb(159, 156, 255) 100%)`

**Typography:**

- Body & cards: **Figtree** font, `rgb(215, 212, 255)`, weight 600
- Headings: **Inter** font
- Hero title: solid white (`#FFFFFF`), 3rem, Inter font

**Header:**

- Sticky header with scroll effect: opacity 0.95 → 0.7, blur 12px → 20px
- Logo and "Userology Help Center" are clickable links to homepage
- Reduced padding `var(--space-4)`
- Navigation moves into header on scroll with smooth fade transition

**Homepage Hero:**

- Centered search with purple glow: `box-shadow: 0 0 15px/30px rgba(139, 123, 247, 0.3/0.15)`
- Search button: purple gradient `linear-gradient(135deg, #3e246bcc 33%, #8c40ffcc 100%)`
- Button disabled (opacity 0.5) when input is empty
- Input: autocomplete off, spellcheck off, white X clear button
- Full-width gradient background extending beyond container

**Sections:**

- "Topics" heading added above topic cards (matches "Popular Articles" and "Featured Video Tutorials" style)
- All section headings use gradient text styling

**Topic Cards:**

- Responsive grid: `repeat(auto-fill, minmax(min(280px, 100%), 1fr))`
- Desktop: 3 columns, Tablet: 2 columns, Mobile: 1 column
- Radial gradient backgrounds with purple hover overlay
- Icons: 3.5rem, grayscale filter → full color on hover with scale
- Hover: translateY(-4px), purple border, shadow

**Article Cards:**

- Grid layout: `repeat(auto-fill, minmax(min(300px, 100%), 1fr))`
- Gradient overlay on hover
- All cards have `box-sizing: border-box`, `width: 100%`, `max-width: 100%`

**Video Carousel:**

- Responsive: 3 columns (desktop) → 2 columns (tablet) → 1 column + horizontal scroll (mobile)
- Play overlay: 60px circle, purple background, scales 1.1x on hover
- Navigation arrows: 48px, hidden on mobile (<640px)
- Mobile: touch swipe with scroll-snap

**Footer Links:**

- "View all" links with diagonal arrow SVG (18px, white)
- Text color: rgba(255,255,255,0.9) → 1 on hover
- Arrow appears inline after text

**Navigation Scroll Behavior:**

- Standalone nav initially visible below header
- At 50px scroll: nav fades into header (opacity 0 → 1, translateY -10px → 0)
- Smooth 0.3s transitions
- Works on: home, videos, articles, categories pages
- Mobile (<768px): nav-in-header hidden, standalone nav always visible

**Responsive Design:**

- Container: `max-width: 1200px`, responsive padding `var(--space-6)` → `var(--space-4)` → `var(--space-3)`
- Homepage structure: `.main-home` full-width, `.container` inside for content constraint
- All grids use `min(Xpx, 100%)` pattern to prevent overflow
- Mobile breakpoints: 768px, 640px, 480px
- Hero font: 3rem → 1.75rem → 1.5rem
- Single-column layouts on mobile with reduced spacing

**Search Dropdown:**

- High z-index (10000) to appear above all content
- Positioned absolutely within search container
- `overflow: visible` on hero-content to prevent clipping
- Max-height 500px with scroll

**Cache Busting:**

- CSS: `?v=20251129`

## Search Feature Fix

**Cross-page navigation fix:**

- Fixed search functionality to work from all pages (home, categories, videos, sections, articles)
- Implemented dynamic base path detection for subdirectories
- Search results now clickable and navigable from any page location
- Added proper relative path handling for search-index.json loading
- Fixed URL resolution for search results across different folder depths

**Dropdown improvements:**

- Added support for both header search (`.search-container`) and hero search (`.hero-search`)
- Increased blur delay from 200ms to 300ms for better click detection
- Added mousedown event prevention to keep dropdown visible during clicks
- Dropdown now properly attaches to search container on all page types
- Enhanced positioning with `position: relative` on hero search container
