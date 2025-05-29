from bs4 import BeautifulSoup
import json
import os

class SkillsScraper:
    def __init__(self, html_file=None, html_content=None):
        """
        Initialize the skills scraper.
        
        Args:
            html_file (str, optional): Path to HTML file containing skills section
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

    def extract_skills(self):
        skills = []
        
        # Find the main skills section
        main_section = self.soup.find('main', attrs={'aria-label': 'Skills'})
        if not main_section:
            return skills
        
        # Return full text of skills
        skills_text = main_section.get_text(separator=' | ', strip=True)
        skills.append(skills_text)
        
        return skills

    def scrape_skills(self):
        return self.extract_skills()

def main():
    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_pages', 'skills_expanded_html.txt')
    
    # Create scraper instance
    scraper = SkillsScraper(html_file)
    
    # Scrape skills
    skills = scraper.scrape_skills()
    
    # Print the skills
    print(json.dumps(skills, indent=2))

if __name__ == '__main__':
    main()
