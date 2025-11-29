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
- Enhanced shadows with purple glow effects on hover
- Gradient text effects on headings (purple-to-blue gradient: `rgb(96, 91, 255)` to `rgb(159, 156, 255)`)
- Seamless page design: removed body margins/padding and footer border for continuous flow

**Typography system:**
- **Figtree** font for all body text and card titles (imported from Google Fonts)
- **Inter** font for main headings with gradient effects
- Card titles: `rgb(215, 212, 255)` color, font-weight: 600, using Figtree
- Hero title "How can we help you today?": solid white (`#FFFFFF`) with Inter font
- All other headings: purple gradient text effect using Inter font
- Gradient formula: `linear-gradient(0deg, rgb(96, 91, 255) 0%, rgb(159, 156, 255) 100%)`
- Added `!important` overrides to card h3 styles to prevent `.content h3` gradient from affecting cards

**Header styling:**
- Header title "Userology Help Center": solid white (`#FFFFFF`) with Inter font
- Reduced header padding from `var(--space-6)` to `var(--space-4)`
- Logo visibility: changed opacity from 0 to 1 (32px size)
- Transparent scroll effect: `rgba(10, 10, 15, 0.95)` becomes `0.7` on scroll
- Glassmorphism: backdrop-filter blur increases from 12px to 20px when scrolled
- Font size: 1.25rem (down from larger sizes)

**Homepage redesign:**
- Centered hero section with large search bar
- Search bar moved from header to center of page on homepage
- Simplified header on homepage (removed duplicate search)
- Hero search box with purple glow effect: `box-shadow: 0 0 15px rgba(139, 123, 247, 0.3), 0 0 30px rgba(139, 123, 247, 0.15)`
- Focus state intensifies glow: `box-shadow: 0 0 15px rgba(139, 123, 247, 0.5), 0 0 30px rgba(139, 123, 247, 0.25), 0 0 0 3px rgba(139, 123, 247, 0.2)`
- Search placeholder text: "Search for help articles, guides, and tutorials..."
- Hero title: 3rem font size, white color, Inter font
- Hero description: 1.0625rem, light gray color
- Hero section padding: `var(--space-16)` top, `var(--space-12)` bottom

**Topic cards (7 cards):**
- Creative pyramid arrangement: 3 cards in first row, 4 cards in second row (8-column grid system)
- Card gradient backgrounds: `radial-gradient(ellipse at top, rgba(45, 45, 90, 0.3) 0%, rgba(26, 26, 46, 0.4) 50%, var(--color-bg-card) 100%)`
- Hover overlay: `radial-gradient(circle at 50% 0%, rgba(139, 123, 247, 0.08) 0%, transparent 60%)`
- Card size: 180px min-height
- Icons: 3.5rem font size, grayscale filter (0.3), scale(1.1) on hover
- Card titles (h3): Figtree font, `rgb(215, 212, 255)` color, 1.125rem, font-weight: 600
- Topic description: hidden on homepage for cleaner look
- Border radius: `var(--radius-lg)` (0.75rem)
- Padding: `var(--space-6)` (1.5rem)
- Hover effect: border-color changes to `var(--color-primary)`, translateY(-4px), purple shadow

**Popular articles section:**
- Section heading (h2): 2rem font size, purple gradient text, Inter font, centered
- Cards use same styling as topic cards but with different content structure
- Card hover: lift 4px, purple glow shadow, border color changes to primary
- Article meta: 0.875rem font size, lighter gray color, top border separator
- Removed top border from section for seamless integration with gradient background

**Video carousel:**
- 6 featured videos with navigation arrows
- Responsive columns: 3 videos on desktop (33.333%), 2 on tablet (50%), 1 on mobile (100%)
- Video card thumbnails: 16:9 aspect ratio with play overlay (60px circle)
- Play button: `rgba(139, 123, 247, 0.9)` background, scales to 1.1 on hover
- Video titles (h4): Figtree font, `rgb(215, 212, 255)` color, 1.0625rem, font-weight: 600
- Description text: 0.875rem, lighter gray
- Navigation arrows: 48px circular buttons, background `var(--color-bg-card)`, hover scales to 1.1
- Disabled state: 0.3 opacity, no hover effects
- Section heading: 2rem font size, purple gradient, centered
- Gap between cards: `var(--space-6)`

**Background effects:**
- Hero section: radial gradient overlay `radial-gradient(ellipse at center top, rgba(139, 123, 247, 0.15) 0%, transparent 60%)`
- Card backgrounds: subtle radial gradients with low opacity purple tones
- Smooth 0.3s transitions for all hover effects

**Footer styling:**
- Background matches page background (`var(--color-bg)`) for seamless blend
- Removed border-top and margin-top for continuous design
- Padding: `var(--space-12)` (3rem) top and bottom
- Text: 0.875rem font size, light gray color, centered

**Visual enhancements:**
- Smooth 0.3s transitions for all interactive elements
- Cards lift 4px on hover for depth perception
- Purple glow shadows on hover: `var(--shadow-hover)` with `rgba(139, 123, 247, 0.3)`
- Border radius consistency: cards use `var(--radius-lg)` (0.75rem)
- Responsive grid systems with auto-fill and minmax for fluid layouts


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
