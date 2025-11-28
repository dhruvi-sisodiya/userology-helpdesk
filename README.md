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

**Dark theme matching Userology brand:**
- Implemented dark color scheme with purple/blue gradient accents (`#8B7BF7`, `#6366F1`)
- Changed background from white to dark navy (`#0A0A0F`)
- Updated all card backgrounds to dark theme (`#16161F`) with hover states
- Added Inter font from Google Fonts for modern typography
- Enhanced shadows with purple glow effects on hover
- Gradient text effects on headings (purple-to-blue gradient)

**Homepage redesign:**
- Centered hero section with large search bar
- Search bar moved from header to center of page on homepage
- Simplified header on homepage (removed duplicate search)
- Added gradient background to hero section
- Hero title with gradient text effect: "How can we help you today?"

**Topic cards layout:**
- Creative pyramid arrangement: 3 cards in first row, 4 cards in second row
- Larger icons (3.5rem) with grayscale filter and scale effect on hover
- Compact card design (180px min-height) with thinner borders
- Removed article counts, replaced with action-oriented text:
  - "Get started with your first study"
  - "Design your research questions"
  - "Customize your study experience"
  - "Go live with your research"
  - "Access and organize your data"
  - "Manage team & permissions"
  - "View insights & analytics"
- Responsive grid: 3+4 on desktop, 2-3-2 on tablet, 2 columns on small tablet, single column on mobile
- Cards have gradient overlay on hover for visual depth

**Popular articles section:**
- Separated with border-top and extra spacing
- Centered gradient heading
- Clean card-based layout with hover effects

**Visual enhancements:**
- Smooth 0.3s transitions for all hover effects
- Cards lift 4px on hover for depth perception
- Purple glow shadows on interactive elements
- Backdrop blur effect on header
- Reduced hero section spacing for tighter layout

**Header logo visibility:**
- Changed CSS `opacity` from `0` to `1` for `.header-logo` class
- Logo now properly visible on all pages

**Enhanced search functionality:**
- Built comprehensive search system with live dropdown results
- Created `build_search_index.py` to generate searchable JSON index from articles
- Added fuzzy matching, relevance scoring, and keyword highlighting
- Implemented keyboard navigation (arrow keys, Enter, Escape) in search dropdown
- Created dedicated `search.html` page for full search results
- Search now indexes article titles, content, and section names
- Features: instant dropdown results (top 10), full results page, query highlighting

**How to use search:**
1. Run `python build_search_index.py` to generate search index (after updating articles)
2. Type in search bar - dropdown shows live results as you type
3. Press Enter or click "See all results" for full search results page
4. Use arrow keys to navigate dropdown, Enter to select, Escape to close

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
