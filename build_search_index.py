#!/usr/bin/env python3
"""
Build search index from JSON data
Creates a searchable index with article content, titles, and metadata
"""

import json
import re
from html.parser import HTMLParser

class HTMLTextExtractor(HTMLParser):
    """Extract plain text from HTML"""
    def __init__(self):
        super().__init__()
        self.text = []
    
    def handle_data(self, data):
        self.text.append(data)
    
    def get_text(self):
        return ' '.join(self.text)

def strip_html(html):
    """Convert HTML to plain text"""
    extractor = HTMLTextExtractor()
    extractor.feed(html)
    return extractor.get_text()

def build_search_index():
    """Build searchable index from articles and sections"""
    
    # Load data
    with open('zendesk_export_userology/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    with open('zendesk_export_userology/sections.json', 'r', encoding='utf-8') as f:
        sections = json.load(f)
    
    # Create section lookup
    section_map = {s['id']: s['name'] for s in sections}
    
    # Build search index
    search_index = []
    
    for article in articles:
        # Extract plain text from HTML body
        body_text = strip_html(article.get('body', ''))
        
        # Create search entry
        search_entry = {
            'id': article['id'],
            'title': article['title'],
            'section': section_map.get(article['section_id'], 'Unknown'),
            'section_id': article['section_id'],
            'url': f'articles/article_{article["id"]}.html',
            'content': body_text[:500],  # First 500 chars for preview
            'updated': article.get('updated_at', ''),
            # Searchable text (combined for indexing)
            'searchText': f"{article['title']} {section_map.get(article['section_id'], '')} {body_text}".lower()
        }
        
        search_index.append(search_entry)
    
    # Save search index to docs directory
    with open('docs/search-index.json', 'w', encoding='utf-8') as f:
        json.dump(search_index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Search index created with {len(search_index)} articles")
    print(f"📁 Saved to: docs/search-index.json")

if __name__ == "__main__":
    build_search_index()
