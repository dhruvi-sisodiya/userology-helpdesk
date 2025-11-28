#!/usr/bin/env python3
"""
Offline Zendesk Help Center Website Generator
Creates a static HTML website from exported Zendesk data
"""

import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse

class OfflineWebsiteGenerator:
    def __init__(self, export_dir="zendesk_export_userology"):
        self.export_dir = export_dir
        self.output_dir = "offline_help_center"
        
        # Load data
        self.categories = self.load_json("categories.json")
        self.sections = self.load_json("sections.json")
        self.articles = self.load_json("articles.json")
        
        # Create output directory with organized structure
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/css", exist_ok=True)
        os.makedirs(f"{self.output_dir}/js", exist_ok=True)
        os.makedirs(f"{self.output_dir}/sections", exist_ok=True)
        os.makedirs(f"{self.output_dir}/articles", exist_ok=True)
        os.makedirs(f"{self.output_dir}/categories", exist_ok=True)
        
        # Create mappings for easy lookup
        self.sections_by_category = {}
        self.articles_by_section = {}
        
        for section in self.sections:
            cat_id = section['category_id']
            if cat_id not in self.sections_by_category:
                self.sections_by_category[cat_id] = []
            self.sections_by_category[cat_id].append(section)
            
            section_id = section['id']
            self.articles_by_section[section_id] = []
        
        for article in self.articles:
            section_id = article['section_id']
            if section_id in self.articles_by_section:
                self.articles_by_section[section_id].append(article)

    def load_json(self, filename):
        """Load JSON data from export directory"""
        with open(f"{self.export_dir}/{filename}", 'r', encoding='utf-8') as f:
            return json.load(f)

    def create_css(self):
        """Create CSS styling for the help center"""
        css_content = """/* Userology Help Center - Clean Professional Design */

:root {
    /* Colors - Clean and Professional */
    --color-primary: #3b82f6;
    --color-primary-dark: #2563eb;
    --color-primary-light: #60a5fa;

    --color-text: #111827;
    --color-text-light: #6b7280;
    --color-text-lighter: #9ca3af;

    --color-bg: #ffffff;
    --color-bg-gray: #f9fafb;
    --color-bg-light: #f3f4f6;

    --color-border: #e5e7eb;
    --color-border-light: #f3f4f6;

    /* Spacing */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-10: 2.5rem;
    --space-12: 3rem;
    --space-16: 4rem;

    /* Typography */
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --font-mono: "SF Mono", Monaco, Consolas, monospace;

    /* Shadows - Subtle */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
    --shadow-hover: 0 8px 16px -4px rgba(0, 0, 0, 0.12);

    /* Radius */
    --radius-sm: 0.375rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-sans);
    font-size: 16px;
    line-height: 1.6;
    color: var(--color-text);
    background: var(--color-bg-gray);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Remove ALL underlines from links globally */
a {
    text-decoration: none;
    color: inherit;
}

/* Container */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-6);
}

/* ========== HEADER ========== */
.header {
    background: var(--color-bg);
    border-bottom: 1px solid var(--color-border);
    padding: var(--space-6) 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: var(--shadow-sm);
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-8);
}

.header-branding {
    display: flex;
    align-items: center;
    gap: var(--space-4);
}

.header-logo {
    width: 40px;
    height: 40px;
    object-fit: contain;
    opacity: 1;
}

.header-text h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-text);
    margin: 0;
    line-height: 1.2;
}

.header-text p {
    font-size: 0.875rem;
    color: var(--color-text-light);
    margin: 0;
}

/* ========== SEARCH ========== */
.search-container {
    flex: 1;
    max-width: 500px;
}

.search-input {
    width: 100%;
    padding: var(--space-3) var(--space-4);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    font-size: 0.9375rem;
    transition: all 0.2s;
    background: var(--color-bg);
}

.search-input:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-input::placeholder {
    color: var(--color-text-lighter);
}

/* ========== NAVIGATION ========== */
.nav {
    background: var(--color-bg);
    border-bottom: 1px solid var(--color-border);
}

.nav ul {
    list-style: none;
    display: flex;
    gap: var(--space-2);
}

.nav a {
    display: block;
    padding: var(--space-4) var(--space-5);
    color: var(--color-text-light);
    font-weight: 500;
    font-size: 0.9375rem;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}

.nav a:hover {
    color: var(--color-primary);
    background: var(--color-bg-light);
}

.nav a.active {
    color: var(--color-primary);
    border-bottom-color: var(--color-primary);
}

/* ========== MAIN LAYOUT ========== */
.main {
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: var(--space-8);
    margin: var(--space-8) 0;
    align-items: start;
}

/* Pages without sidebar (categories, articles) */
.main:not(:has(.sidebar)) {
    grid-template-columns: 1fr;
    max-width: 1400px;
    margin: var(--space-8) auto;
}

/* ========== SIDEBAR ========== */
.sidebar {
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    position: sticky;
    top: 140px;
}

.sidebar h3 {
    font-size: 1rem;
    font-weight: 700;
    color: var(--color-text);
    margin: 0 0 var(--space-4) 0;
}

.sidebar ul {
    list-style: none;
}

.sidebar a {
    display: block;
    padding: var(--space-3) var(--space-4);
    color: var(--color-text-light);
    font-size: 0.9375rem;
    border-radius: var(--radius-md);
    transition: all 0.2s;
}

.sidebar a:hover {
    color: var(--color-primary);
    background: var(--color-bg-light);
}

/* ========== CONTENT AREA ========== */
.content {
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-10);
    min-height: 500px;
}

/* Content without sidebar - more breathing room */
.main:not(:has(.sidebar)) .content {
    padding: var(--space-12);
    border: none;
    background: transparent;
}

.content h1 {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-text);
    margin: 0 0 var(--space-6) 0;
    line-height: 1.2;
}

.content > p {
    font-size: 1.0625rem;
    color: var(--color-text-light);
    margin: 0 0 var(--space-8) 0;
}

.content h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-text);
    margin: var(--space-12) 0 var(--space-6) 0;
}

/* First h2 (like "Popular Articles") */
.content h2:first-of-type {
    margin-top: var(--space-10);
}

.content h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--color-text);
    margin: var(--space-8) 0 var(--space-4) 0;
}

.content h4 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--color-text);
    margin: var(--space-6) 0 var(--space-3) 0;
}

.content p {
    margin: 0 0 var(--space-4) 0;
    line-height: 1.7;
}

.content a {
    color: var(--color-primary);
    font-weight: 500;
}

.content a:hover {
    color: var(--color-primary-dark);
}

.content ul,
.content ol {
    margin: var(--space-4) 0;
    padding-left: var(--space-8);
}

.content li {
    margin-bottom: var(--space-2);
    line-height: 1.7;
}

.content img {
    max-width: 100%;
    height: auto;
    border-radius: var(--radius-md);
    margin: var(--space-6) 0;
}

/* YouTube embeds */
.youtube-container {
    position: relative;
    width: 100%;
    padding-bottom: 56.25%;
    margin: var(--space-8) 0;
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.youtube-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
}

/* ========== ARTICLE GRID - PROPER GRID LAYOUT ========== */
.article-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: var(--space-8);
    margin: var(--space-8) 0 0 0;
}

/* Home page - 2 column max */
.main:has(.sidebar) .article-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

/* Categories/Articles pages - 3 column */
.main:not(:has(.sidebar)) .article-grid {
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: var(--space-6);
}

/* Single category - center it and make it bigger */
.article-grid:has(:only-child) {
    grid-template-columns: 1fr;
    max-width: 600px;
}

.article-grid:has(:only-child) .article-card {
    padding: var(--space-10);
    min-height: 200px;
    text-align: center;
    justify-content: center;
}

/* ========== ARTICLE CARDS - CLEAN & MINIMAL ========== */
.article-card {
    display: flex;
    flex-direction: column;
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-8);
    transition: all 0.2s ease;
    cursor: pointer;
    min-height: 140px;
}

/* Remove any text decoration on card and children */
.article-card,
.article-card *,
.article-card:hover,
.article-card:hover * {
    text-decoration: none !important;
}

.article-card:hover {
    border-color: var(--color-primary);
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}

.article-card h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--color-text);
    line-height: 1.5;
    margin: 0 0 auto 0;
    flex-grow: 1;
    transition: color 0.2s;
}

.article-card:hover h3 {
    color: var(--color-primary);
}

.article-card .article-meta {
    font-size: 0.875rem;
    color: var(--color-text-lighter);
    margin: var(--space-4) 0 0 0;
    padding-top: var(--space-4);
    border-top: 1px solid var(--color-border-light);
}

/* Legacy article items */
.article-list {
    display: grid;
    gap: var(--space-4);
}

.article-item {
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    transition: all 0.2s;
}

.article-item:hover {
    border-color: var(--color-primary);
    box-shadow: var(--shadow-md);
}

.article-item h3 {
    font-size: 1.125rem;
    font-weight: 600;
    margin: 0 0 var(--space-2) 0;
}

.article-item h3 a {
    color: var(--color-text);
}

.article-item h3 a:hover {
    color: var(--color-primary);
}

.article-meta {
    font-size: 0.875rem;
    color: var(--color-text-lighter);
}

.article-excerpt {
    color: var(--color-text-light);
    font-size: 0.9375rem;
    line-height: 1.6;
    margin-top: var(--space-2);
}

/* Breadcrumb */
.breadcrumb {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    font-size: 0.875rem;
    color: var(--color-text-lighter);
    margin-bottom: var(--space-6);
    padding: var(--space-2) var(--space-4);
    background: var(--color-bg-light);
    border-radius: var(--radius-md);
}

.breadcrumb a {
    color: var(--color-primary);
}

.breadcrumb a:hover {
    color: var(--color-primary-dark);
}

/* ========== FOOTER ========== */
.footer {
    background: var(--color-text);
    color: rgba(255, 255, 255, 0.8);
    text-align: center;
    padding: var(--space-12) 0;
    margin-top: var(--space-16);
}

.footer p {
    font-size: 0.875rem;
    margin: 0;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
    .main {
        grid-template-columns: 1fr;
    }

    .sidebar {
        position: static;
        order: 2;
    }

    .content {
        order: 1;
    }

    .article-grid,
    .main:has(.sidebar) .article-grid,
    .main:not(:has(.sidebar)) .article-grid {
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    }
}

@media (max-width: 768px) {
    .container {
        padding: 0 var(--space-4);
    }

    .header-content {
        flex-direction: column;
        align-items: stretch;
        gap: var(--space-4);
    }

    .search-container {
        max-width: none;
    }

    .nav ul {
        flex-direction: column;
        gap: 0;
    }

    .nav a {
        border-bottom: none;
        border-left: 2px solid transparent;
    }

    .nav a.active {
        border-left-color: var(--color-primary);
    }

    .content {
        padding: var(--space-6);
    }

    .content h1 {
        font-size: 1.75rem;
    }

    .article-grid,
    .main:has(.sidebar) .article-grid,
    .main:not(:has(.sidebar)) .article-grid {
        grid-template-columns: 1fr;
        gap: var(--space-5);
    }

    .main:not(:has(.sidebar)) .content {
        padding: var(--space-6);
    }
}

@media (max-width: 480px) {
    .content {
        padding: var(--space-5);
    }

    .content h1 {
        font-size: 1.5rem;
    }
}

/* ========== ACCESSIBILITY ========== */
*:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

/* Print styles */
@media print {
    .nav,
    .sidebar,
    .footer,
    .search-container {
        display: none;
    }

    .main {
        grid-template-columns: 1fr;
    }

    .content {
        border: none;
        box-shadow: none;
    }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}

/* ========== VIDEO GRID & CARDS ========== */
.video-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: var(--space-8);
    margin: var(--space-8) 0 0 0;
}

.video-card {
    display: flex;
    flex-direction: column;
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: all 0.2s ease;
}

.video-card:hover {
    border-color: var(--color-primary);
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}

.video-thumbnail {
    width: 100%;
    aspect-ratio: 16 / 9;
    background: var(--color-bg-light);
    overflow: hidden;
    position: relative;
}

.video-thumbnail video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    background: #000;
}

.video-info {
    padding: var(--space-6);
    flex: 1;
}

.video-info h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--color-text);
    line-height: 1.4;
    margin: 0 0 var(--space-3) 0;
}

.video-description {
    font-size: 0.9375rem;
    color: var(--color-text-light);
    line-height: 1.6;
    margin: 0;
}

/* Video player responsive */
@media (max-width: 768px) {
    .video-grid {
        grid-template-columns: 1fr;
        gap: var(--space-6);
    }
}

/* ========== TOPIC CARDS (for Browse Topics page) ========== */
.topic-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: var(--space-6);
    margin: var(--space-8) 0 var(--space-12) 0;
}

.topic-card {
    display: flex;
    flex-direction: column;
    background: var(--color-bg);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-8);
    transition: all 0.2s ease;
    cursor: pointer;
    text-align: center;
}

.topic-card:hover {
    border-color: var(--color-primary);
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}

.topic-icon {
    font-size: 3rem;
    margin-bottom: var(--space-4);
    line-height: 1;
}

.topic-card h3 {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--color-text);
    margin: 0 0 var(--space-3) 0;
    line-height: 1.3;
}

.topic-description {
    font-size: 0.9375rem;
    color: var(--color-text-light);
    line-height: 1.6;
    margin: 0 0 var(--space-4) 0;
    flex-grow: 1;
}

.topic-meta {
    font-size: 0.875rem;
    color: var(--color-text-lighter);
    font-weight: 500;
    padding-top: var(--space-4);
    border-top: 1px solid var(--color-border-light);
}

/* Topic grid responsive */
@media (max-width: 768px) {
    .topic-grid {
        grid-template-columns: 1fr;
        gap: var(--space-5);
    }
}
"""
        
        with open(f"{self.output_dir}/css/style.css", 'w', encoding='utf-8') as f:
            f.write(css_content)

    def create_javascript(self):
        """Create JavaScript for search and interactivity"""
        js_content = """
// Zendesk Help Center - Search and Interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            if (query.length < 2) return;
            
            // Simple client-side search
            const articles = document.querySelectorAll('.article-item, .article-card');
            articles.forEach(article => {
                const titleElement = article.querySelector('h3 a, h3');
                const metaElement = article.querySelector('.article-meta');
                const excerptElement = article.querySelector('.article-excerpt');
                
                const title = titleElement ? titleElement.textContent.toLowerCase() : '';
                const meta = metaElement ? metaElement.textContent.toLowerCase() : '';
                const excerpt = excerptElement ? excerptElement.textContent.toLowerCase() : '';
                
                if (title.includes(query) || meta.includes(query) || excerpt.includes(query)) {
                    article.style.display = 'block';
                } else {
                    article.style.display = 'none';
                }
            });
        });
    }
    
    // Add active class to current page navigation
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading states for images (exclude header logo)
    const images = document.querySelectorAll('img:not(.header-logo)');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease';
    });
});
"""
        
        with open(f"{self.output_dir}/js/main.js", 'w', encoding='utf-8') as f:
            f.write(js_content)

    def get_header_html(self, title, description="Get help with Userology", is_root=True, include_search=True):
        """Get the common header HTML for all pages"""
        # Adjust paths based on whether we're in root or subdirectory
        path_prefix = "" if is_root else "../"
        
        # Search container only on root pages (index, categories, articles, videos)
        search_html = ""
        if include_search:
            search_html = f"""
                <div class="search-container">
                    <form id="searchForm">
                        <input type="search" class="search-input" placeholder="Search articles..." id="searchInput">
                    </form>
                </div>"""
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Userology Help Center</title>
    <link rel="stylesheet" href="{path_prefix}css/style.css">
    <link rel="icon" type="image/png" href="{path_prefix}logo.png">
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="header-branding">
                    <img src="{path_prefix}logo.png" alt="Userology Logo" class="header-logo">
                    <div class="header-text">
                        <h1>Userology Help Center</h1>
                        <p>{description}</p>
                    </div>
                </div>{search_html}
            </div>
        </div>
    </header>

    <nav class="nav">
        <div class="container">
            <ul>
                <li><a href="{path_prefix}index.html">Home</a></li>
                <li><a href="{path_prefix}categories.html">Browse Topics</a></li>
                <li><a href="{path_prefix}articles.html">All Articles</a></li>
                <li><a href="{path_prefix}videos.html">Videos</a></li>
            </ul>
        </div>
    </nav>"""

    def get_footer_html(self, is_root=True, include_script=False):
        """Get the common footer HTML for all pages"""
        path_prefix = "" if is_root else "../"
        script_tag = f'\n    <script src="{path_prefix}js/main.js"></script>' if include_script else ''
        return f"""
    <footer class="footer">
        <div class="container">
            <p>© 2025 Userology. All rights reserved.</p>
        </div>
    </footer>{script_tag}
</body>
</html>"""

    def create_homepage(self):
        """Create the main homepage with Browse by Topic section"""
        html_content = self.get_header_html("Home", "Get help with Userology", is_root=True)
        
        html_content += """
    <div class="container">
        <main class="main">
            <div class="content">
                <h1>Welcome to Userology Help Center</h1>
                <p>Find comprehensive guides, tutorials, and answers to help you get the most out of Userology.</p>

                <h2>Browse by Topic</h2>
                <div class="topic-grid">
"""
        
        # Create topic cards for sections
        section_icons = {
            'Study Setup': '📝',
            'Interview Plan': '💬',
            'Study Settings': '⚙️',
            'Launch': '🚀',
            'Responses and Recordings': '🎥',
            'Settings and Admin': '👥',
            'Results and Reports': '📊'
        }
        
        section_descriptions = {
            'Study Setup': 'Learn how to create and configure your research studies',
            'Interview Plan': 'Set up discussion guides and interview sections',
            'Study Settings': 'Configure AI moderator, devices, permissions, and more',
            'Launch': 'Recruit participants and preview your study',
            'Responses and Recordings': 'Manage recordings, clips, and participant responses',
            'Settings and Admin': 'Manage your team and organization settings',
            'Results and Reports': 'Analyze qualitative and quantitative research data'
        }
        
        for section in self.sections:
            articles_count = len(self.articles_by_section.get(section['id'], []))
            icon = section_icons.get(section['name'], '📄')
            description = section_descriptions.get(section['name'], section.get('description', ''))
            
            html_content += f"""
                    <a href="sections/section_{section['id']}.html" class="topic-card">
                        <div class="topic-icon">{icon}</div>
                        <h3>{section['name']}</h3>
                        <p class="topic-description">{description}</p>
                        <div class="topic-meta">{articles_count} {'article' if articles_count == 1 else 'articles'}</div>
                    </a>
"""
        
        html_content += """
                </div>

                <h2>Popular Articles</h2>
                <div class="article-grid">
"""
        
        # Show recent articles (last 6)
        recent_articles = sorted(self.articles, key=lambda x: x['updated_at'], reverse=True)[:6]
        for article in recent_articles:
            section = next((s for s in self.sections if s['id'] == article['section_id']), None)
            
            html_content += f"""
                    <a href="articles/article_{article['id']}.html" class="article-card">
                        <h3>{article['title']}</h3>
                        <div class="article-meta">
                            {section['name'] if section else 'Unknown'}
                        </div>
                    </a>
"""
        
        html_content += """
                </div>
            </div>
        </main>
    </div>

    <footer class="footer">
        <div class="container">
            <p>© 2025 Userology. All rights reserved.</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""
        
        with open(f"{self.output_dir}/index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

    def create_category_page(self, category):
        """Create a category page in categories folder"""
        sections = self.sections_by_category.get(category['id'], [])
        
        html_content = self.get_header_html(category['name'], "Browse help topics organized by category", is_root=False)
        
        html_content += f"""
    <div class="container">
        <main class="main">
            <aside class="sidebar">
                <h3>Sections in {category['name']}</h3>
                <ul>
"""
        
        for section in sections:
            html_content += f'                    <li><a href="../sections/section_{section["id"]}.html">{section["name"]}</a></li>\n'
        
        html_content += f"""
                </ul>
            </aside>

            <div class="content">
                <h1>{category['name']}</h1>
                <p>{category.get('description', '')}</p>
                
                <h2>Sections</h2>
                <div class="article-list">
"""
        
        for section in sections:
            articles = self.articles_by_section.get(section['id'], [])
            html_content += f"""
                    <div class="article-item">
                        <h3><a href="../sections/section_{section['id']}.html">{section['name']}</a></h3>
                        <div class="article-meta">
                            {len(articles)} articles
                        </div>
                    </div>
"""
        
        html_content += """
                </div>
            </div>
        </main>
    </div>
"""
        
        html_content += self.get_footer_html(is_root=False)
        
        with open(f"{self.output_dir}/categories/category_{category['id']}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

    def create_section_page(self, section):
        """Create a section page in sections folder"""
        articles = self.articles_by_section.get(section['id'], [])
        category = next((c for c in self.categories if c['id'] == section['category_id']), None)
        
        html_content = self.get_header_html(section['name'], "Your complete guide to using Userology", is_root=False, include_search=False)
        
        html_content += f"""
    <div class="container">
        <main class="main">
            <aside class="sidebar">
                <h3>Articles in {section['name']}</h3>
                <ul>
"""
        
        for article in articles:
            html_content += f'                    <li><a href="../articles/article_{article["id"]}.html">{article["title"]}</a></li>\n'
        
        html_content += f"""
                </ul>
            </aside>

            <div class="content">
                <h1>{section['name']}</h1>
                
                
                <h2>Articles</h2>
                <div class="article-list">
"""
        
        for article in articles:
            html_content += f"""
                    <div class="article-item">
                        <h3><a href="../articles/article_{article['id']}.html">{article['title']}</a></h3>
                        <div class="article-meta">
                            Updated: {article['updated_at'][:10]}
                        </div>
                    </div>
"""
        
        html_content += """
                </div>
            </div>
        </main>
    </div>

    <footer class="footer">
        <div class="container">
            <p>© 2025 Userology. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""
        
        with open(f"{self.output_dir}/sections/section_{section['id']}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

    def create_article_page(self, article):
        """Create an article page in articles folder"""
        section = next((s for s in self.sections if s['id'] == article['section_id']), None)
        category = next((c for c in self.categories if c['id'] == section['category_id']), None) if section else None
        
        # Use article body directly - it's already properly formatted from the HTML
        article_body = article.get('body', '')
        
        html_content = self.get_header_html(article['title'], "Your complete guide to using Userology", is_root=False, include_search=False)
        
        html_content += f"""
    <div class="container">
        <main class="main">
            <aside class="sidebar">
                <h3>Navigation</h3>
                <ul>
                    <li><a href="../index.html">← Back to Home</a></li>
"""
        
        if category:
            html_content += f'                    <li><a href="../categories/category_{category["id"]}.html">← {category["name"]}</a></li>\n'
        if section:
            html_content += f'                    <li><a href="../sections/section_{section["id"]}.html">← {section["name"]}</a></li>\n'
        
        html_content += f"""
                </ul>
            </aside>

            <div class="content">
                <h1>{article['title']}</h1>
                <div class="article-meta">
                    {category['name'] if category else 'Unknown'} → {section['name'] if section else 'Unknown'} | 
                    Updated: {article['updated_at'][:10]}
                </div>
                
                <div class="article-content">
                    {article_body}
                </div>
            </div>
        </main>
    </div>

    <footer class="footer">
        <div class="container">
            <p>© 2025 Userology. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""
        
        with open(f"{self.output_dir}/articles/article_{article['id']}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

    def create_all_pages(self):
        """Create all pages"""
        print("Creating CSS...")
        self.create_css()
        
        print("Creating JavaScript...")
        self.create_javascript()
        
        print("Creating homepage...")
        self.create_homepage()
        
        print("Creating category pages...")
        for category in self.categories:
            self.create_category_page(category)
        
        print("Creating section pages...")
        for section in self.sections:
            self.create_section_page(section)
        
        print("Creating article pages...")
        for article in self.articles:
            self.create_article_page(article)
        
        print("Creating index pages...")
        self.create_categories_index()
        self.create_articles_index()
        self.create_videos_page()

    def create_videos_page(self):
        """Create videos.html page with all video tutorials"""
        import os
        
        # Get all video files from videos folder
        videos_dir = "videos"
        videos = []
        
        if os.path.exists(videos_dir):
            video_files = [f for f in os.listdir(videos_dir) if f.endswith('.mp4')]
            
            # Video descriptions mapping
            video_descriptions = {
                'Creating your study on Userology.mp4': 'Learn how to create and set up a new study on the Userology platform.',
                'AI Discussion Guides.mp4': 'Understand how AI-powered discussion guides enhance your usability testing.',
                'AI Moderator Configuration.mp4': 'Configure the AI moderator settings for your research sessions.',
                'AI Transcript.mp4': 'Learn how to access and utilize AI-generated transcripts from your sessions.',
                'Ask AI Feature.mp4': 'Discover how to use the Ask AI feature to get insights from your research data.',
                'Configuring Devices and Browsers.mp4': 'Set up device and browser requirements for your study participants.',
                'Downloading and Creating Clips.mp4': 'Learn how to download recordings and create clips from your research sessions.',
                'Duplicating a study on userology.mp4': 'Quickly duplicate an existing study to save time on setup.',
                'External Recruitment.mp4': 'Learn how to recruit participants from external sources for your studies.',
                'Launching Your Study and Recruiting Participants.mp4': 'Complete guide to launching your study and recruiting participants.',
                'Live Product Section.mp4': 'Set up and configure the live product testing section in your study.',
                'Managing Team and Inviting Members.mp4': 'Add and manage team members in your Userology organization.',
                'Organization settings.mp4': 'Configure your organization settings and preferences.',
                'Personalizing Your Study.mp4': 'Customize your study with branding and personalization options.',
                'Preview Session.mp4': 'Preview how your study will appear to participants before launching.',
                'Prototype Section.mp4': 'Set up prototype testing sections for your design research.',
                'QnA results.mp4': 'Analyze and interpret Q&A results from your research sessions.',
                'Recording permission settings.mp4': 'Configure recording permissions and privacy settings for your studies.',
                'Recordings page.mp4': 'Navigate and manage all your session recordings in one place.',
                'Recruit Participant Yourself.mp4': 'Learn how to recruit and invite your own participants to studies.',
                'Sign In Feature.mp4': 'Set up sign-in requirements for your study participants.',
                'Time estimation feature.mp4': 'Use the time estimation feature to plan your study duration.',
                'Types of responses .mp4': 'Understand the different types of responses you can collect in your studies.',
                'Understanding Quantitative Results .mp4': 'Learn how to analyze and interpret quantitative data from your research.',
                'Uploading a Legal Document to Your Study.mp4': 'Add consent forms and legal documents to your study setup.',
                'Usability score.mp4': 'Understand and interpret usability scores from your testing sessions.',
                'Voice Interview Section.mp4': 'Set up and conduct voice interviews as part of your research studies.'
            }
            
            for video_file in sorted(video_files):
                video_name = os.path.splitext(video_file)[0]
                videos.append({
                    'filename': video_file,
                    'title': video_name,
                    'description': video_descriptions.get(video_file, '')
                })
        
        html_content = self.get_header_html("Video Tutorials", "Watch video tutorials to learn how to use Userology", is_root=True)
        
        html_content += """
    <div class="container">
        <main class="main">
            <div class="content">
                <h1>Video Tutorials</h1>
                <p>Watch step-by-step video guides to help you master Userology features. Click on any video to watch.</p>

                <div class="video-grid">
"""
        
        for video in videos:
            html_content += f"""
                    <div class="video-card">
                        <div class="video-thumbnail">
                            <video controls preload="metadata">
                                <source src="videos/{video['filename']}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div class="video-info">
                            <h3>{video['title']}</h3>
                            <p class="video-description">{video['description']}</p>
                        </div>
                    </div>
"""
        
        html_content += """
                </div>
            </div>
        </main>
    </div>
"""
        
        html_content += self.get_footer_html(is_root=True, include_script=True)
        
        with open(f"{self.output_dir}/videos.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

    def create_categories_index(self):
        """Create Browse Topics index page with topic grid"""
        html_content = self.get_header_html("Browse Topics", "Browse help topics organized by category", is_root=True)
        
        html_content += """
    <div class="container">
        <main class="main">
            <div class="content">
                <h1>Browse Topics</h1>
                <p>Find articles organized by topic to help you get started quickly.</p>

                <div class="topic-grid">
"""
        
        # Create topic cards for sections
        section_icons = {
            'Study Setup': '📝',
            'Interview Plan': '💬',
            'Study Settings': '⚙️',
            'Launch': '🚀',
            'Responses and Recordings': '🎥',
            'Settings and Admin': '👥',
            'Results and Reports': '📊'
        }
        
        section_descriptions = {
            'Study Setup': 'Learn how to create and configure your research studies',
            'Interview Plan': 'Set up discussion guides and interview sections',
            'Study Settings': 'Configure AI moderator, devices, permissions, and more',
            'Launch': 'Recruit participants and preview your study',
            'Responses and Recordings': 'Manage recordings, clips, and participant responses',
            'Settings and Admin': 'Manage your team and organization settings',
            'Results and Reports': 'Analyze qualitative and quantitative research data'
        }
        
        for section in self.sections:
            articles_count = len(self.articles_by_section.get(section['id'], []))
            icon = section_icons.get(section['name'], '📄')
            description = section_descriptions.get(section['name'], section.get('description', ''))
            
            html_content += f"""
                    <a href="sections/section_{section['id']}.html" class="topic-card">
                        <div class="topic-icon">{icon}</div>
                        <h3>{section['name']}</h3>
                        <p class="topic-description">{description}</p>
                        <div class="topic-meta">{articles_count} {'article' if articles_count == 1 else 'articles'}</div>
                    </a>
"""
        
        html_content += """
                </div>
            </div>
        </main>
    </div>
"""
        
        html_content += self.get_footer_html(is_root=True, include_script=True)
        
        with open(f"{self.output_dir}/categories.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

    def create_articles_index(self):
        """Create articles index page"""
        html_content = self.get_header_html("All Articles", "Browse all help articles", is_root=True)
        
        html_content += """
    <div class="container">
        <main class="main">
            <div class="content">
                <h1>All Articles</h1>
                <div class="article-grid">
"""
        
        for article in sorted(self.articles, key=lambda x: x['title']):
            section = next((s for s in self.sections if s['id'] == article['section_id']), None)
            category = next((c for c in self.categories if c['id'] == section['category_id']), None) if section else None
            
            html_content += f"""
                    <a href="articles/article_{article['id']}.html" class="article-card">
                        <h3>{article['title']}</h3>
                        <div class="article-meta">
                            {category['name'] if category else 'Unknown'} → {section['name'] if section else 'Unknown'}
                        </div>
                    </a>
"""
        
        html_content += """
                </div>
            </div>
        </main>
    </div>

    <footer class="footer">
        <div class="container">
            <p>Offline Help Center - Generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""
        
        with open(f"{self.output_dir}/articles.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    print("🚀 Generating offline help center website...")
    generator = OfflineWebsiteGenerator()
    generator.create_all_pages()
    print(f"✅ Website generated successfully!")
    print(f"📁 Open {generator.output_dir}/index.html in your browser to view the offline help center")

if __name__ == "__main__":
    main()
