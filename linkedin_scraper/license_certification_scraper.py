from bs4 import BeautifulSoup
import json
import os

class LicenseCertificationScraper:
    def __init__(self, html_file=None, html_content=None):
        """
        Initialize the license and certification scraper.
        
        Args:
            html_file (str, optional): Path to HTML file containing license/certification section
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

    def extract_licenses_certifications(self):
        """
        Extract licenses and certifications from the HTML content.
        Returns a list with a single string containing all certifications.
        """
        certifications = []
        
        # Find the main certifications section
        main_section = self.soup.find('main', attrs={'aria-label': 'Licenses & certifications'})
        if not main_section:
            # Try alternative section names
            main_section = self.soup.find('main', attrs={'aria-label': 'Licenses & Certifications'})
            if not main_section:
                main_section = self.soup.find('main', attrs={'aria-label': 'Licenses'})
                if not main_section:
                    print("Warning: No Licenses & Certifications section found")
                    return certifications
        
        # Return full text of certifications
        certs_text = main_section.get_text(separator=' | ', strip=True)
        certifications.append(certs_text)
        
        return certifications

def main():
    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_pages', 'licenses_and_certifications_expanded_html.txt')
    
    try:
        # Create scraper instance
        scraper = LicenseCertificationScraper(html_file)
        
        # Scrape licenses & certifications
        certifications = scraper.extract_licenses_certifications()
        
        # Print the certifications as JSON
        print(json.dumps(certifications, indent=2))
        
    except FileNotFoundError:
        print(f"Error: The file {html_file} was not found.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
        
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
