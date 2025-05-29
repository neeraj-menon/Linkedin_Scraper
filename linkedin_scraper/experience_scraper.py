from bs4 import BeautifulSoup
import json
import os

class ExperienceScraper:
    def __init__(self, html_file=None, html_content=None):
        """
        Initialize the experience scraper.
        
        Args:
            html_file (str, optional): Path to HTML file containing experience section
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

    def extract_experience(self):
        experiences = []
        
        # Debug: Print all main sections
        print("Available sections in HTML:")
        for section in self.soup.find_all('main'):
            if 'aria-label' in section.attrs:
                print(f"- {section['aria-label']}")
        
        # Find the main experience section
        main_section = self.soup.find('main', attrs={'aria-label': 'Experience'})
        if not main_section:
            print("Warning: No Experience section found with aria-label='Experience'")
            return experiences
            
        # Return full text of experiences
        experience_text = main_section.get_text(separator=' | ', strip=True)
        experiences.append(experience_text)
        
        return experiences

def main():
    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_pages', 'experiences_expanded_html.txt')
    
    # Create scraper instance
    scraper = ExperienceScraper(html_file)
    
    # Scrape experience
    experiences = scraper.extract_experience()
    
    # Print the experience details
    print(json.dumps(experiences, indent=2))

if __name__ == '__main__':
    main()