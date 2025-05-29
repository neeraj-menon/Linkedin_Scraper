from bs4 import BeautifulSoup
import json
import re
import os
from .skills_scraper import SkillsScraper
from .language_scraper import LanguageScraper
from .license_certification_scraper import LicenseCertificationScraper
from .project_scraper import ProjectScraper
from .education_scraper import EducationScraper
from .experience_scraper import ExperienceScraper
from .about_scraper import process_about_file
from pathlib import Path
# from skills_scraper import SkillsScraper
# from language_scraper import LanguageScraper
# from license_certification_scraper import LicenseCertificationScraper

class LinkedInProfileScraper:
    def __init__(self, html_file=None, session_dir=None, html_content=None, html_content_dict=None):
        """
        Initialize the LinkedIn profile scraper.
        
        Args:
            html_file (str, optional): Path to HTML file containing profile HTML
            session_dir (str, optional): Directory containing expanded section HTML files
            html_content (str, optional): Raw HTML content string instead of file
            html_content_dict (dict, optional): Dictionary of HTML content for all sections
        """
        # Store the HTML content dictionary if provided
        self.html_content_dict = html_content_dict or {}
        
        # Load HTML content either from file or directly
        if html_content:
            self.html_content = html_content
        elif html_file:
            with open(html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            # Store in dictionary if not already there
            if 'profile_html' not in self.html_content_dict:
                self.html_content_dict['profile_html'] = self.html_content
        elif 'profile_html' in self.html_content_dict:
            self.html_content = self.html_content_dict['profile_html']
        else:
            raise ValueError("Either html_file, html_content, or html_content_dict with 'profile_html' key must be provided")
            
        # Parse the HTML content
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
        
        # Store the session directory if provided
        self.session_dir = session_dir

    def extract_name(self):
        """Extract the profile name."""
        # Try multiple methods to extract name
        name_elem = self.soup.find('title')
        if name_elem:
            # Extract name from title, removing " | LinkedIn"
            name = name_elem.text.replace(' | LinkedIn', '').strip()
            # Remove leading number if present
            name = re.sub(r'^\(\d+\)\s*', '', name).strip()
            return name
        
        # Fallback to other potential name locations
        name_elem = self.soup.find('h1', class_=re.compile(r'.*text-heading-xlarge.*'))
        if name_elem:
            return name_elem.text.strip()
        
        return None

    def extract_headline(self):
        """Extract the professional headline."""
        headline_elem = self.soup.find('div', class_=re.compile(r'.*text-body-medium.*'))
        if headline_elem:
            return headline_elem.text.strip()
        return None

    def extract_experiences(self):
        """Extract work experiences from LinkedIn profile."""
        experiences = []
        
        # Find all sections with profile card class
        all_sections = self.soup.find_all('section', class_=re.compile(r'.*pv-profile-card.*'))
        
        for section in all_sections:
            # Extract section header if exists
            header = section.find(['h2', 'h1'], class_=re.compile(r'.*heading.*'))
            
            # If this is the Experience section
            if header and 'Experience' in header.get_text(strip=True):
                full_text = section.get_text(separator=' | ', strip=True)
                
                # Check if we need to expand experiences (Show all)
                if 'Show all' in full_text:
                    try:
                        # Try to get from memory first
                        if self.html_content_dict and 'experiences_expanded_html' in self.html_content_dict:
                            scraper = ExperienceScraper(html_content=self.html_content_dict['experiences_expanded_html'])
                            experiences = scraper.extract_experience()
                            return experiences
                        # Fall back to file if session directory is provided
                        elif self.session_dir:
                            exp_file = os.path.join(self.session_dir, 'experiences_expanded_html.txt')
                            if os.path.exists(exp_file):
                                scraper = ExperienceScraper(exp_file)
                                experiences = scraper.extract_experience()
                                return experiences
                    except Exception as e:
                        print(f"Error expanding experiences: {e}")
                
                # If we couldn't expand or no need to expand, return basic experiences
                experiences.append(full_text)
        
        return experiences

    def extract_education(self):
        """Extract education details from LinkedIn profile."""
        education = []
        
        # Find all sections with profile card class
        all_sections = self.soup.find_all('section', class_=re.compile(r'.*pv-profile-card.*'))
        
        for section in all_sections:
            # Extract section header if exists
            header = section.find(['h2', 'h1'], class_=re.compile(r'.*heading.*'))
            
            # If this is the Education section
            if header and 'Education' in header.get_text(strip=True):
                full_text = section.get_text(separator=' | ', strip=True)
                
                # Check if we need to expand education (Show all)
                if 'Show all' in full_text:
                    try:
                        # Try to get from memory first
                        if self.html_content_dict and 'education_expanded_html' in self.html_content_dict:
                            scraper = EducationScraper(html_content=self.html_content_dict['education_expanded_html'])
                            education = scraper.scrape_education()
                            return education
                        # Fall back to file if session directory is provided
                        elif self.session_dir:
                            edu_file = os.path.join(self.session_dir, 'education_expanded_html.txt')
                            if os.path.exists(edu_file):
                                scraper = EducationScraper(edu_file)
                                education = scraper.scrape_education()
                                return education
                    except Exception as e:
                        print(f"Error expanding education: {e}")
                
                # If we couldn't expand or no need to expand, return basic education
                education.append(full_text)
        
        return education

    def extract_skills(self):
        """Extract skills from LinkedIn profile."""
        skills = []
        
        # Find all sections with profile card class
        all_sections = self.soup.find_all('section', class_=re.compile(r'.*pv-profile-card.*'))
        
        for section in all_sections:
            # Extract section header if exists
            header = section.find(['h2', 'h1'], class_=re.compile(r'.*heading.*'))
            
            # If this is the Skills section
            if header and 'Skills' in header.get_text(strip=True):
                full_text = section.get_text(separator=' | ', strip=True)
                
                # Check if we need to expand skills (Show all)
                if 'Show all' in full_text:
                    try:
                        # Try to get from memory first
                        if self.html_content_dict and 'skills_expanded_html' in self.html_content_dict:
                            scraper = SkillsScraper(html_content=self.html_content_dict['skills_expanded_html'])
                            skills = scraper.scrape_skills()
                            return skills
                        # Fall back to file if session directory is provided
                        elif self.session_dir:
                            skills_file = os.path.join(self.session_dir, 'skills_expanded_html.txt')
                            if os.path.exists(skills_file):
                                scraper = SkillsScraper(skills_file)
                                skills = scraper.scrape_skills()
                                return skills
                    except Exception as e:
                        print(f"Error expanding skills: {e}")
                
                # Return the full text of the skills section
                skills.append(full_text)
                return skills
        
        return skills

    def extract_languages(self):
        """Extract languages from LinkedIn profile."""
        languages = []
        
        # Find all sections with profile card class
        all_sections = self.soup.find_all('section', class_=re.compile(r'.*pv-profile-card.*'))
        
        for section in all_sections:
            # Extract section header if exists
            header = section.find(['h2', 'h1'], class_=re.compile(r'.*heading.*'))
            
            # If this is the Languages section
            if header and 'Languages' in header.get_text(strip=True):
                full_text = section.get_text(separator=' | ', strip=True)
                
                # Check if we need to expand languages (Show all)
                if 'Show all' in full_text:
                    try:
                        # Try to get from memory first
                        if self.html_content_dict and 'languages_expanded_html' in self.html_content_dict:
                            scraper = LanguageScraper(html_content=self.html_content_dict['languages_expanded_html'])
                            languages = scraper.scrape_languages()
                            return languages
                        # Fall back to file if session directory is provided
                        elif self.session_dir:
                            lang_file = os.path.join(self.session_dir, 'languages_expanded_html.txt')
                            if os.path.exists(lang_file):
                                scraper = LanguageScraper(lang_file)
                                languages = scraper.scrape_languages()
                                return languages
                    except Exception as e:
                        print(f"Error expanding languages: {e}")
                
                # Return the full text of the languages section
                languages.append(full_text)
                return languages
        
        return languages

    def extract_licenses_certifications(self):
        """Extract licenses and certifications from LinkedIn profile."""
        licenses = []
        
        # Find all sections with profile card class
        all_sections = self.soup.find_all('section', class_=re.compile(r'.*pv-profile-card.*'))
        
        for section in all_sections:
            # Extract section header if exists
            header = section.find(['h2', 'h1'], class_=re.compile(r'.*heading.*'))
            
            # If this is the Licenses & certifications section
            if header and any(x in header.get_text(strip=True) for x in ['Licenses', 'Certifications']):
                full_text = section.get_text(separator=' | ', strip=True)
                
                # Check if we need to expand licenses (Show all)
                if 'Show all' in full_text:
                    try:
                        # Try to get from memory first
                        if self.html_content_dict and 'licenses_and_certifications_expanded_html' in self.html_content_dict:
                            scraper = LicenseCertificationScraper(html_content=self.html_content_dict['licenses_and_certifications_expanded_html'])
                            licenses = scraper.extract_licenses_certifications()
                            return licenses
                        # Fall back to file if session directory is provided
                        elif self.session_dir:
                            lic_file = os.path.join(self.session_dir, 'licenses_and_certifications_expanded_html.txt')
                            if os.path.exists(lic_file):
                                scraper = LicenseCertificationScraper(lic_file)
                                licenses = scraper.extract_licenses_certifications()
                                return licenses
                    except Exception as e:
                        print(f"Error expanding licenses: {e}")
                
                # Return the full text of the licenses section
                licenses.append(full_text)
                return licenses
        
        return licenses

    def extract_projects(self):
        """Extract projects from LinkedIn profile."""
        projects = []
        
        # Find all sections with profile card class
        all_sections = self.soup.find_all('section', class_=re.compile(r'.*pv-profile-card.*'))
        
        for section in all_sections:
            # Extract section header if exists
            header = section.find(['h2', 'h1'], class_=re.compile(r'.*heading.*'))
            
            # If this is the Projects section
            if header and 'Projects' in header.get_text(strip=True):
                full_text = section.get_text(separator=' | ', strip=True)
                
                # Check if we need to expand projects (Show all)
                if 'Show all' in full_text:
                    try:
                        # Try to get from memory first
                        if self.html_content_dict and 'projects_expanded_html' in self.html_content_dict:
                            scraper = ProjectScraper(html_content=self.html_content_dict['projects_expanded_html'])
                            projects = scraper.scrape_projects()
                            return projects
                        # Fall back to file if session directory is provided
                        elif self.session_dir:
                            proj_file = os.path.join(self.session_dir, 'projects_expanded_html.txt')
                            if os.path.exists(proj_file):
                                scraper = ProjectScraper(proj_file)
                                projects = scraper.scrape_projects()
                                return projects
                    except Exception as e:
                        print(f"Error expanding projects: {e}")
                
                # If we couldn't expand or no need to expand, return the full text
                projects.append(full_text)
                return projects
        
        return projects
        
    def extract_companies(self):
        """Extract company information from the about pages."""
        try:
            companies = []
            
            # First check if we have company HTML content in memory
            if self.html_content_dict:
                # Look only for the 'best' company HTML content (not *_main_html or *_about_html)
                company_keys = [k for k in self.html_content_dict.keys() 
                               if k.startswith('company_') and k.endswith('_html') 
                               and not k.endswith('_main_html') and not k.endswith('_about_html')]
                
                if company_keys:
                    # Process each unique company only once
                    processed_companies = set()
                    
                    for key in company_keys:
                        try:
                            # Process the company HTML content
                            company_info = process_about_file(self.html_content_dict[key])
                            
                            if company_info and company_info['name'] and company_info['name'] not in processed_companies:
                                companies.append(company_info)
                                processed_companies.add(company_info['name'])
                        except Exception as e:
                            print(f"Error processing company content from {key}: {e}")
                    
                    return companies
            
            # Fall back to file-based approach if no in-memory content
            if self.session_dir:
                company_dir = os.path.join(self.session_dir, 'company_about_pages')
                if os.path.exists(company_dir):
                    about_files = [f for f in os.listdir(company_dir) if f.endswith('_about.txt')]
                    for file_name in about_files:
                        try:
                            file_path = os.path.join(company_dir, file_name)
                            company_info = process_about_file(file_path)
                            if company_info:
                                companies.append(company_info)
                        except Exception as e:
                            print(f"Error processing company file {file_name}: {e}")
                    return companies
            
            # Legacy path as last resort
            about_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'html_pages' / 'company_about_pages'
            if about_dir.exists():
                about_files = list(about_dir.glob('*_about.txt'))
                for file_path in about_files:
                    try:
                        company_info = process_about_file(file_path)
                        if company_info:
                            companies.append(company_info)
                    except Exception as e:
                        print(f"Error processing company file {file_path}: {e}")
            
            return companies
            
        except Exception as e:
            print(f"Error extracting companies: {e}")
            return []
            
    def extract_about(self):
        """Extract the 'About' section from LinkedIn profile."""
        # Find the div with id="about" which is the anchor for the About section
        about_anchor = self.soup.find('div', id='about')
        if not about_anchor:
            return None
            
        # Find the parent container that has the actual content
        parent_container = about_anchor.find_next_sibling('div', class_=re.compile(r'.*escTwakvXlHtkbumLjULwyNILFHqFbANpitf'))
        if not parent_container:
            return None
            
        # Find the content div with the about text - it's in a sibling div of the parent container
        content_div = parent_container.find_next_sibling('div', class_='display-flex ph5 pv3')
        if not content_div:
            return None
            
        # Find the div with the actual text content
        text_div = content_div.find('div', class_=re.compile(r'.*inline-show-more-text.*'))
        if not text_div:
            return None
            
        # Extract text from both visible and hidden spans
        visible_text = ''
        hidden_text = ''
        
        # Get visible text (aria-hidden="true")
        visible_span = text_div.find('span', {'aria-hidden': 'true'})
        if visible_span:
            # Clean up the text by removing HTML comments and extra whitespace
            visible_text = ' '.join(visible_span.stripped_strings)
        
        # Get hidden text (visually-hidden)
        hidden_span = text_div.find('span', class_='visually-hidden')
        if hidden_span:
            hidden_text = ' '.join(hidden_span.stripped_strings)
        
        # Clean up any HTML entities and extra whitespace
        def clean_text(text):
            if not text:
                return None
            # Replace HTML entities and clean up whitespace
            text = text.replace('&amp;', '&')
            text = ' '.join(text.split())
            return text.strip()
        
        # Return the non-empty text, preferring visible text if both exist
        result = clean_text(visible_text) or clean_text(hidden_text)
        return result if result else None

    def scrape_profile(self):
        """Compile all profile information."""
        profile = {
            'name': self.extract_name(),
            'headline': self.extract_headline(),
            'about': self.extract_about(),
            'experiences': self.extract_experiences(),
            'education': self.extract_education(),
            'skills': self.extract_skills(),
            'languages': self.extract_languages(),
            'licenses-certifications': self.extract_licenses_certifications(),
            'projects': self.extract_projects(),
            'current_companies': self.extract_companies()
        }
        return profile

def main():
    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_pages', 'profile_html.txt')

    
    # Create scraper instance
    scraper = LinkedInProfileScraper(html_file)
    
    # Scrape profile
    profile = scraper.scrape_profile()
    
    # Print or save the profile
    print(json.dumps(profile, indent=2))
    
    # Optionally, save to a JSON file
    with open('/Users/neerajmenon/Documents/Projects/3R/MCP/sales_mcp/linkedin_profile.json', 'w') as f:
        json.dump(profile, f, indent=2)

if __name__ == '__main__':
    main()
