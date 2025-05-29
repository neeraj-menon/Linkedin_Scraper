from bs4 import BeautifulSoup
import json
import os

class EducationScraper:
    def __init__(self, html_file=None, html_content=None):
        """
        Initialize the education scraper.
        
        Args:
            html_file (str, optional): Path to HTML file containing education section
            html_content (str, optional): Raw HTML content string instead of file
        """
        if html_content:
            self.html_content = html_content
        elif html_file:
            with open(html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
        else:
            raise ValueError("Either html_file or html_content must be provided")
            
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def extract_education(self):
        education = []
        
        # Find the main education section
        main_section = self.soup.find('main', attrs={'aria-label': 'Education'})
        if not main_section:
            return education
        
        # Return full text of education
        education_text = main_section.get_text(separator=' | ', strip=True)
        education.append(education_text)
        
        return education

    def scrape_education(self):
        return self.extract_education()

def main():
    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_pages', 'education_expanded_html.txt')
    
    # Create scraper instance
    scraper = EducationScraper(html_file)
    
    # Scrape education
    education = scraper.scrape_education()
    
    # Print the education details
    print(json.dumps(education, indent=2))

if __name__ == '__main__':
    main()
