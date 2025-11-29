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

- Dark theme with purple gradients: `#8B7BF7`, `#6366F1`, background `#0A0A0F`
- Card backgrounds: `#16161F` with purple glow on hover
- Gradient text: `linear-gradient(0deg, rgb(96, 91, 255) 0%, rgb(159, 156, 255) 100%)`

**Typography:**

- **Figtree**: body text, card titles (`rgb(215, 212, 255)`, weight 600)
- **Inter**: headings with gradient (except hero title: solid white)
- Hero title: 3rem, white, Inter font

**Header:**

- Text: white, reduced padding (`var(--space-4)`)
- Scroll effect: opacity 0.95 → 0.7, blur 12px → 20px
- Navigation: moves into header on scroll (smooth fade transition)
- Logo: visible at 32px

**Homepage Hero:**

- Centered search with purple glow: `box-shadow: 0 0 15px/30px rgba(139, 123, 247, 0.3/0.15)`
- Search button: gradient `linear-gradient(135deg, #3e246bcc 33%, #8c40ffcc 100%)`, disabled state when empty
- Input: autocomplete off, white X button, no purple border highlight
- Placeholder: "Search for help articles, guides, and tutorials..."
- Background gradient: `linear-gradient(180deg, #0A0A0F 0%, #0F0F1A 15%, #1A1A2E 40%, #252545 70%, #2D2D5A 100%)`

**Topic Cards (7):**

- Layout: 3+4 pyramid (8-column grid)
- Radial gradient backgrounds with hover overlay
- Titles: Figtree, `rgb(215, 212, 255)`, 1.125rem
- Icons: 3.5rem, grayscale filter, scale on hover
- Hover: translateY(-4px), purple glow shadow

**Video Carousel:**

- 6 videos, responsive (3-2-1 columns)
- Play button: 60px circle, purple background, scales on hover
- Navigation arrows: 48px circular, scale on hover
- Titles: Figtree, `rgb(215, 212, 255)`, 1.0625rem

**Footer Links:**

- "View all" links: white text (rgba 0.9 → 1), 1.125rem, SVG arrow icon (18px)
- Arrow: diagonal up-right, white fill, appears after text

**Navigation:**

- Standalone nav below header initially
- On scroll (>50px): fades out (opacity 0, translateY -10px), appears in header with smooth transition
- Header nav: fades in between logo and search, margin-right spacing
- Works on: home, videos, articles, categories pages

**Mobile Responsive:**

- Breakpoints: 768px (tablets), 480px (phones)
- Hero: 3rem → 1.75rem font size
- Cards: single column, reduced padding
- Nav: horizontal scroll on mobile

**Cache Busting:**

- CSS links: `?v=20251129` parameter for deployment updates

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
