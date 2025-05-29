#!/usr/bin/env python3
"""
Extract company profile links from LinkedIn experiences where the duration includes 'present'.
Returns a list of company profile URLs.
"""

import os
from bs4 import BeautifulSoup


def extract_current_companies(html_source) -> list:
    """
    Extract company profile links from LinkedIn experiences HTML where duration is 'present'.
    
    Args:
        html_source: Either a path to an HTML file or a string containing HTML content
        
    Returns:
        List of company profile URLs
    """
    try:
        # Check if html_source is a file path or HTML content
        if isinstance(html_source, str):
            if os.path.exists(html_source):
                # It's a file path
                with open(html_source, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            else:
                # It's HTML content
                html_content = html_source
        else:
            raise ValueError("html_source must be a file path or HTML content string")
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        company_urls = []
        
        # Find all experience items
        experience_items = soup.select('li.pvs-list__paged-list-item')
        
        for item in experience_items:
            # Look for date range containing 'present'
            date_el = item.select_one('span.pvs-entity__caption-wrapper')
            if not date_el or 'present' not in date_el.get_text(strip=True).lower():
                continue
                
            # Find company link
            link = item.find('a', href=lambda x: x and '/company/' in x)
            if link and link.get('href'):
                url = link['href']
                if not url.startswith('http'):
                    url = f"https://www.linkedin.com{url}"
                company_urls.append(url)
        
        return set(company_urls)
        
    except Exception as e:
        print(f"Error: {e}")
        return []


def main():
    # Path to the experiences HTML file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(script_dir, 'html_pages', 'experiences_expanded_html.txt')
    
    if not os.path.exists(html_file):
        print(f"Error: File not found: {html_file}")
        return
    
    # Get company URLs
    company_urls = extract_current_companies(html_file)
    
    # Print the list of URLs
    print(set(company_urls))
    return set(company_urls)


if __name__ == '__main__':
    main()
