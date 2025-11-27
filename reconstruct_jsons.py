#!/usr/bin/env python3
"""
Reconstruct JSON files from existing HTML files
Creates minimal JSONs with only required fields for the generator
"""

import os
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime

class JSONReconstructor:
    def __init__(self):
        self.sections_dir = "offline_help_center/sections"
        self.articles_dir = "offline_help_center/articles"
        self.categories_dir = "offline_help_center/categories"
        self.output_dir = "zendesk_export_userology"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Data storage
        self.categories = []
        self.sections = []
        self.articles = []
    
    def extract_id_from_filename(self, filename):
        """Extract ID from filename like 'section_25457022454173.html'"""
        match = re.search(r'_(\d+)\.html', filename)
        return int(match.group(1)) if match else None
    
    def normalize_section_name(self, name):
        """Normalize section names to title case for consistency"""
        # Map lowercase variations to correct title case
        name_mapping = {
            'study setup': 'Study Setup',
            'study settings': 'Study Settings',
            'interview plan': 'Interview Plan',
            'launch': 'Launch',
            'responses and recordings': 'Responses and Recordings',
            'settings and admin': 'Settings and Admin',
            'results and reports': 'Results and Reports'
        }
        
        return name_mapping.get(name.lower(), name)
    
    def parse_categories(self):
        """Parse category HTML files"""
        if not os.path.exists(self.categories_dir):
            print(f"Warning: {self.categories_dir} not found")
            return
        
        for filename in os.listdir(self.categories_dir):
            if not filename.endswith('.html'):
                continue
            
            filepath = os.path.join(self.categories_dir, filename)
            category_id = self.extract_id_from_filename(filename)
            
            if not category_id:
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            # Extract category name from h1 in content div (not header)
            content = soup.find('div', class_='content')
            h1 = content.find('h1') if content else soup.find('h1')
            name = h1.text.strip() if h1 else "Unknown"
            
            # Extract description from p after h1 in content div
            description = ""
            if h1:
                p = h1.find_next('p')
                if p:
                    description = p.text.strip()
            
            self.categories.append({
                'id': category_id,
                'name': name,
                'description': description
            })
            
            print(f"Parsed category: {name} (ID: {category_id})")
    
    def parse_sections(self):
        """Parse section HTML files"""
        if not os.path.exists(self.sections_dir):
            print(f"Warning: {self.sections_dir} not found")
            return
        
        for filename in sorted(os.listdir(self.sections_dir)):
            if not filename.endswith('.html'):
                continue
            
            filepath = os.path.join(self.sections_dir, filename)
            section_id = self.extract_id_from_filename(filename)
            
            if not section_id:
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            # Extract section name from h1 in content div (not header)
            content = soup.find('div', class_='content')
            h1 = content.find('h1') if content else soup.find('h1')
            name = h1.text.strip() if h1 else "Unknown"
            
            # Normalize section name to match emoji mappings
            name = self.normalize_section_name(name)
            
            # Find category ID from sidebar link
            category_id = 25457035135005  # Default to "General"
            sidebar = soup.find('aside', class_='sidebar')
            if sidebar:
                category_link = sidebar.find('a', href=re.compile(r'category_(\d+)\.html'))
                if category_link:
                    match = re.search(r'category_(\d+)\.html', category_link['href'])
                    if match:
                        category_id = int(match.group(1))
            
            self.sections.append({
                'id': section_id,
                'name': name,
                'category_id': category_id
            })
            
            print(f"Parsed section: {name} (ID: {section_id})")
    
    def parse_articles(self):
        """Parse article HTML files"""
        if not os.path.exists(self.articles_dir):
            print(f"Warning: {self.articles_dir} not found")
            return
        
        for filename in sorted(os.listdir(self.articles_dir)):
            if not filename.endswith('.html'):
                continue
            
            filepath = os.path.join(self.articles_dir, filename)
            article_id = self.extract_id_from_filename(filename)
            
            if not article_id:
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract article title from h1 in content div (not header)
            content = soup.find('div', class_='content')
            h1 = content.find('h1') if content else soup.find('h1')
            title = h1.text.strip() if h1 else "Unknown"
            
            # Extract updated date from article-meta
            updated_at = "2025-03-17"  # Default
            meta_div = soup.find('div', class_='article-meta')
            if meta_div:
                date_match = re.search(r'Updated:\s*(\d{4}-\d{2}-\d{2})', meta_div.text)
                if date_match:
                    updated_at = date_match.group(1)
            
            # Find section ID from sidebar link
            section_id = None
            sidebar = soup.find('aside', class_='sidebar')
            if sidebar:
                section_link = sidebar.find('a', href=re.compile(r'section_(\d+)\.html'))
                if section_link:
                    match = re.search(r'section_(\d+)\.html', section_link['href'])
                    if match:
                        section_id = int(match.group(1))
            
            # Extract body content from article-content div
            body = ""
            article_content = soup.find('div', class_='article-content')
            if article_content:
                # Get inner HTML content
                body = ''.join(str(child) for child in article_content.children)
                body = body.strip()
            
            if section_id:
                self.articles.append({
                    'id': article_id,
                    'title': title,
                    'body': body,
                    'section_id': section_id,
                    'updated_at': updated_at
                })
                
                print(f"Parsed article: {title[:50]}... (ID: {article_id})")
    
    def save_json(self, data, filename):
        """Save data to JSON file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {filepath}")
    
    def create_manifest(self):
        """Create minimal manifest.json"""
        manifest = {
            "export_date": datetime.now().isoformat(),
            "categories_count": len(self.categories),
            "sections_count": len(self.sections),
            "articles_count": len(self.articles)
        }
        self.save_json(manifest, "manifest.json")
    
    def run(self):
        """Run the reconstruction process"""
        print("Starting JSON reconstruction from HTML files...\n")
        
        print("=" * 60)
        print("Parsing categories...")
        print("=" * 60)
        self.parse_categories()
        
        print("\n" + "=" * 60)
        print("Parsing sections...")
        print("=" * 60)
        self.parse_sections()
        
        print("\n" + "=" * 60)
        print("Parsing articles...")
        print("=" * 60)
        self.parse_articles()
        
        print("\n" + "=" * 60)
        print("Saving JSON files...")
        print("=" * 60)
        
        self.save_json(self.categories, "categories.json")
        self.save_json(self.sections, "sections.json")
        self.save_json(self.articles, "articles.json")
        self.create_manifest()
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Categories: {len(self.categories)}")
        print(f"Sections: {len(self.sections)}")
        print(f"Articles: {len(self.articles)}")
        print(f"\nJSON files saved to: {self.output_dir}/")
        print("=" * 60)

def main():
    reconstructor = JSONReconstructor()
    reconstructor.run()

if __name__ == "__main__":
    main()
