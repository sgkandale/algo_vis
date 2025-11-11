#!/usr/bin/env python3

import os
import re
from bs4 import BeautifulSoup
import json

# Algorithm categories and keywords for meta tags
ALGORITHM_CATEGORIES = {
    "sorting": {
        "keywords": "sorting algorithm, sort, bubble sort, merge sort, quick sort, heap sort, insertion sort, selection sort, radix sort, counting sort",
        "description": "Learn about sorting algorithms and their implementations with interactive visualizations"
    },
    "hashing": {
        "keywords": "hashing algorithm, hash function, cryptographic hash, md5, sha, bcrypt, ripemd, blake",
        "description": "Explore hashing algorithms and their applications in cryptography and data structures"
    },
    "distributed": {
        "keywords": "distributed consensus, consensus algorithm, raft, paxos, epaxos, zab, 2pc, 3pc, bft, vsr",
        "description": "Understand distributed consensus algorithms used in distributed systems and databases"
    },
    "garbage": {
        "keywords": "garbage collection, gc algorithm, mark and sweep, generational gc, reference counting",
        "description": "Learn about garbage collection algorithms used in programming language runtimes"
    },
    "page": {
        "keywords": "page replacement algorithm, fifo, lru, lfu, mru, nru, second chance",
        "description": "Study page replacement algorithms used in operating systems memory management"
    },
    "probabilistic": {
        "keywords": "probabilistic data structure, bloom filter, count-min sketch, hyperloglog, flajolet-martin",
        "description": "Discover probabilistic data structures for approximate computing and big data"
    },
    "quantum": {
        "keywords": "quantum computing, quantum algorithm, shor code, quantum error correction",
        "description": "Explore quantum computing algorithms and error correction techniques"
    },
    "cryptography": {
        "keywords": "cryptography, encryption, rsa, diffie-hellman, elgamal, merkle tree, homomorphic encryption",
        "description": "Learn about cryptographic algorithms and their applications in security"
    },
    "machine": {
        "keywords": "machine learning algorithm, linear regression, logistic regression, decision tree, random forest, svm, knn, naive bayes, clustering, pca",
        "description": "Study machine learning algorithms and their practical applications"
    },
    "btree": {
        "keywords": "b-tree, b+ tree, data structure, tree algorithm, database index",
        "description": "Understand B-tree data structures and their use in database indexing"
    }
}

# Default fallback
DEFAULT_CATEGORY = {
    "keywords": "algorithm, data structure, computer science, visualization, interactive",
    "description": "Interactive algorithm visualization platform for learning computer science concepts"
}

def get_category_info(filename):
    """Determine category based on filename and return appropriate SEO info"""
    filename_lower = filename.lower()
    
    for category, info in ALGORITHM_CATEGORIES.items():
        if category in filename_lower:
            return info
    
    return DEFAULT_CATEGORY

def generate_structured_data(title, description, url):
    """Generate JSON-LD structured data"""
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "author": {
            "@type": "Person",
            "name": "Shantanu Kandale"
        },
        "publisher": {
            "@type": "Organization",
            "name": "AlgoViz Hub",
            "logo": {
                "@type": "ImageObject",
                "url": "https://sgkandale.github.io/favicon.ico"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://sgkandale.github.io/{url}"
        }
    }
    return json.dumps(structured_data, indent=2)

def improve_seo(html_content, filename):
    """Add SEO improvements to HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get page title
    title_tag = soup.find('title')
    page_title = title_tag.get_text() if title_tag else "Algorithm Visualization"
    
    # Get category-specific SEO info
    seo_info = get_category_info(filename)
    
    # Add meta description if not present
    if not soup.find('meta', attrs={'name': 'description'}):
        meta_desc = soup.new_tag('meta', attrs={
            'name': 'description',
            'content': seo_info['description']
        })
        soup.head.insert(0, meta_desc)
    
    # Add meta keywords if not present
    if not soup.find('meta', attrs={'name': 'keywords'}):
        meta_keywords = soup.new_tag('meta', attrs={
            'name': 'keywords',
            'content': seo_info['keywords']
        })
        soup.head.insert(1, meta_keywords)
    
    # Add Open Graph tags
    og_tags = [
        ('og:title', page_title),
        ('og:description', seo_info['description']),
        ('og:type', 'article'),
        ('og:url', f'https://sgkandale.github.io/{filename}'),
        ('og:site_name', 'AlgoViz Hub')
    ]
    
    for prop, content in og_tags:
        if not soup.find('meta', attrs={'property': prop}):
            og_tag = soup.new_tag('meta', attrs={
                'property': prop,
                'content': content
            })
            soup.head.append(og_tag)
    
    # Add Twitter Card tags
    twitter_tags = [
        ('twitter:card', 'summary'),
        ('twitter:title', page_title),
        ('twitter:description', seo_info['description']),
        ('twitter:site', '@sgkandale')
    ]
    
    for name, content in twitter_tags:
        if not soup.find('meta', attrs={'name': name}):
            twitter_tag = soup.new_tag('meta', attrs={
                'name': name,
                'content': content
            })
            soup.head.append(twitter_tag)
    
    # Add canonical URL
    if not soup.find('link', attrs={'rel': 'canonical'}):
        canonical = soup.new_tag('link', attrs={
            'rel': 'canonical',
            'href': f'https://sgkandale.github.io/{filename}'
        })
        soup.head.append(canonical)
    
    # Add structured data
    if not soup.find('script', attrs={'type': 'application/ld+json'}):
        structured_data = generate_structured_data(
            page_title,
            seo_info['description'],
            filename
        )
        script_tag = soup.new_tag('script', attrs={'type': 'application/ld+json'})
        script_tag.string = structured_data
        soup.head.append(script_tag)
    
    # Add lang attribute to html tag if missing
    if not soup.html.has_attr('lang'):
        soup.html['lang'] = 'en'
    
    return str(soup)

def process_html_files():
    """Process all HTML files in the directory"""
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    print(f"Processing {len(html_files)} HTML files...")
    
    for filename in html_files:
        try:
            # Backup original file
            with open(filename, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Save backup
            with open(f'/tmp/seo_backup/{filename}', 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Improve SEO
            improved_content = improve_seo(original_content, filename)
            
            # Write improved content back to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(improved_content)
            
            print(f"✓ Processed {filename}")
            
        except Exception as e:
            print(f"✗ Error processing {filename}: {str(e)}")
    
    print("SEO improvement process completed!")

if __name__ == "__main__":
    process_html_files()