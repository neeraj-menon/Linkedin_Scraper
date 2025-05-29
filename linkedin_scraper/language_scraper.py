from bs4 import BeautifulSoup
import json
import os

class LanguageScraper:
    def __init__(self, html_file=None, html_content=None):
        """
        Initialize the language scraper.
        
        Args:
            html_file (str, optional): Path to HTML file containing language section
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

    def extract_languages(self):
        languages = []
        
        # Find the main languages section
        main_section = self.soup.find('main', attrs={'aria-label': 'Languages'})
        if not main_section:
            # Try alternative section name
            main_section = self.soup.find('main', attrs={'aria-label': 'Language'})
            if not main_section:
                print("Warning: No Languages section found")
                return languages
                
        # Return full text of languages
        language_text = main_section.get_text(separator=' | ', strip=True)
        languages.append(language_text)
        
        return languages

    def scrape_languages(self) -> list:
        """Scrape and return languages as a list of dictionaries."""
        return self.extract_languages()

def main():
    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_pages', 'languages_expanded_html.txt')
    
    try:
        # Create scraper instance
        scraper = LanguageScraper(html_file)
        
        # Scrape languages
        languages = scraper.extract_languages()
        
        # Print the language details
        print(json.dumps(languages, indent=2))
        
    except FileNotFoundError:
        print(f"Error: File not found at {html_file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
        
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
