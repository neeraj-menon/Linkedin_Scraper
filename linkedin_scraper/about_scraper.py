#!/usr/bin/env python3
"""
Extract company information from LinkedIn company about pages.

This script processes HTML files in the company_about_pages directory and extracts
structured information such as company name, overview, website, industry, etc.
"""

import os
import json
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any


def extract_company_info(html_content: str) -> Dict[str, Any]:
    """
    Extract company information from HTML content.
    
    Args:
        html_content: The HTML content of a company's about page
        
    Returns:
        A dictionary containing the extracted company information
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize result dictionary
    company_info = {
        'name': '',
        'overview': '',
        'website': '',
        'industry': '',
        'company_size': '',
        'headquarters': '',
        'founded': '',
        'specialties': '',
        'verified_date': ''
    }
    
    try:
        # Extract company name
        # Try different selectors for company name as LinkedIn's HTML structure varies
        name_selectors = [
            'h1.org-top-card-summary__title',
            'h1.org-top-card-summary__title.t-24.t-black.t-bold',
            'h1.ember-view.t-24.t-black.t-bold',
            'h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words'
        ]
        
        for selector in name_selectors:
            name_tag = soup.select_one(selector)
            if name_tag:
                company_info['name'] = name_tag.get_text(strip=True)
                break
        
        # Extract overview - try different selectors
        overview_selectors = [
            'p.break-words.white-space-pre-wrap',
            'div.org-about-us-organization-description__text',
            'div.org-about-module__description',
            'div.org-about-module__text',
            'div.org-page-details__description-content'
        ]
        
        for selector in overview_selectors:
            overview_tags = soup.select(selector)
            if overview_tags:
                overview_text = '\n'.join([tag.get_text('\n', strip=True) for tag in overview_tags])
                if overview_text:
                    company_info['overview'] = overview_text
                    break
        
        # Extract details from definition list
        dl_elements = soup.find_all('dl')
        for dl in dl_elements:
            dt_elements = dl.find_all('dt')
            dd_elements = dl.find_all('dd')
            
            for dt, dd in zip(dt_elements, dd_elements):
                label = dt.get_text(strip=True).lower()
                value = dd.get_text('\n', strip=True)
                
                # Map labels to the correct fields
                if 'website' in label:
                    company_info['website'] = value
                elif 'industry' in label:
                    company_info['industry'] = value
                elif 'company size' in label or 'employees' in label:
                    company_info['company_size'] = value
                elif 'headquarters' in label or 'location' in label:
                    company_info['headquarters'] = value
                elif 'founded' in label or 'year founded' in label:
                    company_info['founded'] = value
                elif 'specialties' in label:
                    company_info['specialties'] = value
                elif 'verified' in label:
                    company_info['verified_date'] = value
        
        # If we couldn't find the information in definition lists, try other approaches
        if not any(company_info.values()):
            # Try to find information in sections with labels
            sections = soup.find_all(['section', 'div'], class_=lambda c: c and ('org-about-module' in c or 'org-page-details' in c))
            for section in sections:
                # Look for labeled sections
                heading = section.find(['h2', 'h3'])
                if heading:
                    label = heading.get_text(strip=True).lower()
                    content_div = section.find(['p', 'div'], class_=lambda c: c and ('description' in c or 'text' in c))
                    if content_div:
                        value = content_div.get_text('\n', strip=True)
                        
                        if 'about' in label and not company_info['overview']:
                            company_info['overview'] = value
                        elif 'website' in label:
                            company_info['website'] = value
                        elif 'industry' in label:
                            company_info['industry'] = value
                        elif 'size' in label or 'employees' in label:
                            company_info['company_size'] = value
                        elif 'headquarters' in label or 'location' in label:
                            company_info['headquarters'] = value
                        elif 'founded' in label:
                            company_info['founded'] = value
                        elif 'specialties' in label:
                            company_info['specialties'] = value
    
    except Exception as e:
        print(f"Error extracting company info: {e}")
    
    return company_info


def process_about_file(file_path_or_content) -> Dict[str, Any]:
    """
    Process a company about file or HTML content and extract information.
    
    Args:
        file_path_or_content: Path to the about file or HTML content string
        
    Returns:
        Dictionary containing the extracted company information
    """
    try:
        # Check if input is a file path or HTML content
        if isinstance(file_path_or_content, (str, Path)) and os.path.exists(str(file_path_or_content)):
            # It's a file path
            with open(file_path_or_content, 'r', encoding='utf-8') as f:
                html_content = f.read()
            source_name = os.path.basename(str(file_path_or_content))
        else:
            # It's HTML content
            html_content = file_path_or_content
            source_name = "in_memory_content"
        
        # Make sure we have valid HTML content
        if not html_content or not isinstance(html_content, str):
            print(f"Invalid HTML content provided: {type(html_content)}")
            return None
        
        # Extract company information
        company_info = extract_company_info(html_content)
        
        # Add source information
        company_info['source'] = source_name
        
        # Verify we have at least some basic information
        if not company_info['name'] and not company_info['overview']:
            print("Warning: Could not extract any meaningful company information")
            # Try to extract name from the source if it's a file
            if source_name != "in_memory_content" and '_' in source_name:
                company_name = source_name.split('_')[0].replace('-', ' ').title()
                if company_name:
                    company_info['name'] = company_name
                    print(f"Extracted company name '{company_name}' from filename")
        
        return company_info
    
    except Exception as e:
        print(f"Error processing company content: {e}")
        return None


def process_all_about_files(directory: str) -> List[Dict[str, Any]]:
    """
    Process all about files in the specified directory.
    
    Args:
        directory: Path to the directory containing about files
        
    Returns:
        List of dictionaries containing company information
    """
    about_dir = Path(directory)
    about_files = list(about_dir.glob('*_about.txt'))
    
    all_companies = []
    
    for file_path in about_files:
        print(f"Processing {file_path.name}...")
        company_info = process_about_file(file_path)
        if company_info:
            all_companies.append(company_info)
    
    return all_companies


def save_to_json(data: List[Dict[str, Any]], output_file: str) -> None:
    """
    Save the extracted data to a JSON file.
    
    Args:
        data: List of company information dictionaries
        output_file: Path to the output JSON file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nSaved data to {output_file}")
    except Exception as e:
        print(f"Error saving to {output_file}: {e}")


def print_company_info(company: Dict[str, Any]) -> None:
    """
    Print company information in a readable format.
    
    Args:
        company: Dictionary containing company information
    """
    print("\n" + "=" * 80)
    print(f"Company: {company.get('name', 'N/A')}")
    print("=" * 80)
    
    print("\nOVERVIEW:")
    print("-" * 40)
    print(company.get('overview', 'No overview available'))
    
    print("\nDETAILS:")
    print("-" * 40)
    details = [
        ("Website", company.get('website', 'N/A')),
        ("Industry", company.get('industry', 'N/A')),
        ("Company Size", company.get('company_size', 'N/A')),
        ("Headquarters", company.get('headquarters', 'N/A')),
        ("Founded", company.get('founded', 'N/A')),
        ("Specialties", company.get('specialties', 'N/A')),
        ("Verified Date", company.get('verified_date', 'N/A')),
    ]
    
    for label, value in details:
        print(f"{label}: {value}")
    
    print("\n" + "=" * 80 + "\n")


def main():
    # Directory containing the about files
    script_dir = Path(__file__).parent
    about_dir = script_dir / 'html_pages' / 'company_about_pages'
    
    # Output file for JSON data
    output_file = script_dir / 'company_data.json'
    
    # Process all about files
    print(f"Processing about files in: {about_dir}")
    companies = process_all_about_files(about_dir)
    
    if not companies:
        print("No company data found. Make sure you have scraped the about pages first.")
        return
    
    # Print information for each company
    for company in companies:
        print_company_info(company)
    
    # Save all data to JSON file
    save_to_json(companies, output_file)


if __name__ == "__main__":
    main()
