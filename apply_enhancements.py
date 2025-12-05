"""
Apply new features to all article pages:
1. Article feedback system
2. Related articles section
3. Breadcrumb navigation
"""

import os
import re
from pathlib import Path

# Article metadata for related articles
ARTICLE_SECTIONS = {
    "25457022454173": "Study Setup",
    "25457032309917": "Interview Plan",
    "25456987366429": "Study Settings",
    "25457005624349": "Launch",
    "25457015415453": "Responses and Recordings",
    "25457032160541": "Results and Reports",
    "25562911720605": "Settings and Admin"
}

# Related articles mapping (article_id -> [related1, related2, related3])
RELATED_ARTICLES = {
    "article_25456988151453": [
        ("article_25561782334749", "Interview Plan", "What Is a Discussion Guide on Userology"),
        ("article_25562045316637", "Study Settings", "Configuring the AI Moderator"),
        ("article_25562330763805", "Launch", "Previewing Your Study")
    ],
    "article_25561782334749": [
        ("article_25456988151453", "Study Setup", "Creating your study on Userology"),
        ("article_25562292368669", "Interview Plan", "Adding sections to your discussion guide"),
        ("article_25562045316637", "Study Settings", "Configuring the AI Moderator")
    ],
    # Add mappings for all 24 articles...
}

FEEDBACK_HTML = '''
                <!-- Article Feedback Section -->
                <div class="article-feedback">
                    <h3>Was this article helpful?</h3>
                    <div class="feedback-buttons">
                        <button class="feedback-btn feedback-yes" data-vote="helpful" aria-label="Yes, this was helpful">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
                            </svg>
                            <span>Yes</span>
                        </button>
                        <button class="feedback-btn feedback-no" data-vote="not-helpful" aria-label="No, this was not helpful">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"></path>
                            </svg>
                            <span>No</span>
                        </button>
                    </div>
                    <div class="feedback-response" style="display: none;">
                        <p class="feedback-message"></p>
                        <div class="feedback-details" style="display: none;">
                            <p>What could we improve?</p>
                            <textarea class="feedback-textarea" placeholder="Your feedback helps us improve our documentation..." maxlength="500"></textarea>
                            <button class="feedback-submit-btn">Submit Feedback</button>
                            <button class="feedback-skip-btn">Skip</button>
                        </div>
                    </div>
                </div>
'''

def get_related_articles_html(article_id):
    """Generate related articles HTML for a specific article"""
    related = RELATED_ARTICLES.get(article_id, [])
    if not related:
        # Default related articles
        related = [
            ("article_25561782334749", "Interview Plan", "What Is a Discussion Guide on Userology"),
            ("article_25916497212701", "Results and Reports", "Understanding Quantitative Results in Userology"),
            ("article_25562407594781", "Responses and Recordings", "Types of responses in Userology")
        ]
    
    html = '''
                <!-- Related Articles Section -->
                <div class="related-articles-section">
                    <h3>Related Articles</h3>
                    <div class="related-articles-grid">
'''
    
    for related_id, category, title in related:
        html += f'''                        <a href="{related_id}.html" class="related-article-card">
                            <div class="related-card-category">{category}</div>
                            <h4>{title}</h4>
                            <p>Learn more about this topic</p>
                        </a>
'''
    
    html += '''                    </div>
                </div>
'''
    return html

def add_breadcrumb(content, article_id):
    """Add breadcrumb navigation"""
    breadcrumb = '''            <!-- Breadcrumb Navigation -->
            <nav class="breadcrumb" aria-label="Breadcrumb">
                <ol>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../categories.html">Browse Topics</a></li>
                    <li><a href="../sections/section_25457022454173.html">Study Setup</a></li>
                    <li aria-current="page">Article</li>
                </ol>
            </nav>

'''
    
    # Insert breadcrumb after <main class="main">
    content = content.replace(
        '<main class="main">',
        '<main class="main">\n' + breadcrumb
    )
    
    return content

def enhance_article(filepath):
    """Add all enhancements to an article page"""
    print(f"Processing: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already enhanced
    if 'article-feedback' in content:
        print(f"  ✓ Already enhanced, skipping")
        return
    
    article_id = filepath.stem
    
    # 1. Add breadcrumb
    content = add_breadcrumb(content, article_id)
    
    # 2. Add feedback and related articles before closing </div> of content
    # Find the last </div> before </main>
    pattern = r'(</div>\s*</div>\s*</main>)'
    
    enhancements = FEEDBACK_HTML + get_related_articles_html(article_id)
    replacement = enhancements + r'\1'
    
    content = re.sub(pattern, replacement, content)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Enhanced successfully")

def main():
    """Process all article pages"""
    articles_dir = Path('docs/articles')
    
    if not articles_dir.exists():
        print("❌ docs/articles directory not found")
        return
    
    article_files = list(articles_dir.glob('article_*.html'))
    print(f"Found {len(article_files)} article files\n")
    
    for filepath in article_files:
        try:
            enhance_article(filepath)
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n✅ Processed {len(article_files)} articles")

if __name__ == '__main__':
    main()
