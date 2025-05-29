from bs4 import BeautifulSoup
import json
import os

class ProjectScraper:
    def __init__(self, html_file=None, html_content=None):
        """
        Initialize the project scraper.
        
        Args:
            html_file (str, optional): Path to HTML file containing project section
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

    def extract_projects(self):
        projects = []
        
        # Find the main projects section
        main_section = self.soup.find('main', attrs={'aria-label': 'Projects'})
        if not main_section:
            return projects
        
        # Return full text of projects
        projects_text = main_section.get_text(separator=' | ', strip=True)
        projects.append(projects_text)
        
        return projects

    def scrape_projects(self):
        return self.extract_projects()

def main():
    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_pages', 'projects_expanded_html.txt')
    
    # Create scraper instance
    scraper = ProjectScraper(html_file)
    
    # Scrape projects
    projects = scraper.scrape_projects()
    
    # Print the projects
    print(json.dumps(projects, indent=2))

if __name__ == '__main__':
    main()
