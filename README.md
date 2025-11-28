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
