import asyncio
import os
import random
import logging
from typing import Optional, List, Dict, Tuple

from playwright.async_api import Page, Browser, BrowserContext

from .authenticator import LinkedinAuthenticator
# from .extractors import ProfileExtractor
# from .models import Profile
from .extract_current_companies import extract_current_companies

# Setup logger for this module
logger = logging.getLogger(__name__)

class LinkedinProfileScraper:
    def __init__(self, debug_mode=False):
        """
        Initialize the LinkedIn profile scraper.
        
        Args:
            debug_mode (bool): If True, HTML content will be saved to disk for debugging
        """
        self.debug_mode = debug_mode
        
        # Store HTML content in memory
        self.html_content = {}
        
        # Only create debug directory if in debug mode
        if self.debug_mode:
            # Define the html_pages directory path relative to this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.html_pages_dir = os.path.join(script_dir, 'html_pages')
            
            # Ensure html_pages directory exists
            os.makedirs(self.html_pages_dir, exist_ok=True)
    
    async def scrape_profile(
        self, 
        profile_url: str, 
        email: Optional[str] = None, 
        password: Optional[str] = None,
        scrape_companies: bool = True
    ) -> Tuple[bool, Dict[str, str]]:
        """
        Comprehensive LinkedIn profile scraping method
        
        Returns:
            Tuple[bool, Dict[str, str]]: (success, html_content_dict)
        """
        # Setup basic console logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        logger = logging.getLogger(__name__)

        # Retrieve credentials from environment if not provided
        if not email:
            email = os.environ.get('LINKEDIN_EMAIL')
        if not password:
            password = os.environ.get('LINKEDIN_PASSWORD')
        
        # Validate credentials
        if not email or not password:
            logger.error("No LinkedIn credentials provided")
            raise ValueError(
                "LinkedIn credentials must be provided either as arguments "
                "or through LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables"
            )
        
        # Launch browser and authenticate
        browser, context, page = await LinkedinAuthenticator.login(email, password)
        
        try:
            logger.info(f"Navigating to profile: {profile_url}")
            
            # Navigate to profile with advanced waiting
            await page.goto(profile_url, wait_until='domcontentloaded', timeout=45000)
            
            # Random wait to simulate human behavior
            await page.wait_for_timeout(random.uniform(2000, 5000))
            
            # Extract page HTML
            profile_html = await page.content()
            
            # Store HTML in memory
            self.html_content['profile_html'] = profile_html
            
            # Save HTML to file only in debug mode
            if self.debug_mode:
                profile_html_path = os.path.join(self.html_pages_dir, 'profile_html.txt')
                with open(profile_html_path, 'w', encoding='utf-8') as f:
                    f.write(profile_html)
            
            # Attempt to expand and capture additional sections
            await self._expand_and_capture_section(page, 'experiences')
            await self._expand_and_capture_section(page, 'skills')
            await self._expand_and_capture_section(page, 'education')
            await self._expand_and_capture_section(page, 'languages')
            await self._expand_and_capture_section(page, 'projects')
            await self._expand_and_capture_section(page, 'licenses_and_certifications')
            
            logger.info("Profile HTML captured successfully")

            # Extract full profile
            logger.info("Extracting profile information")
            
            # Scrape company about pages if requested
            if scrape_companies:
                logger.info("Scraping company about pages")
                await self.scrape_company_about_pages(browser, context, page)
            
            # Close browser resources
            await context.close()
            await browser.close()
            
            return True, self.html_content
        
        except Exception as e:
            logger.error(f"Profile scraping failed: {e}")
            raise
        
    async def _expand_and_capture_section(self, page: Page, section: str):
        try:
            # Wait for the page to be visually stable
            await page.wait_for_load_state('domcontentloaded', timeout=10000)
            
            # Wait a bit longer to ensure dynamic content is loaded
            await page.wait_for_timeout(random.uniform(3000, 5000))
            
            # Define selectors for different sections with exact IDs when possible
            section_selectors = {
                'experiences': [
                    '#navigation-index-see-all-experiences',
                    '//span[text()[contains(., "Show all") and contains(., "experiences")]]/ancestor::a'
                ],
                'skills': [
                    'a[id*="navigation-index-Show-all"][id*="-skills"]',
                    '//span[text()[contains(., "Show all") and contains(., "skills")]]/ancestor::a'
                ],
                'education': [
                    '#navigation-index-see-all-education',
                    '//span[text()[contains(., "Show all") and contains(., "educations")]]/ancestor::a'
                ],
                'languages': [
                    '#navigation-index-see-all-languages',
                    '//span[text()[contains(., "Show all") and contains(., "languages")]]/ancestor::a',
                    '//a[contains(@href, "/details/languages")]'
                ],
                'projects': [
                    '#navigation-index-see-all-projects',
                    '//span[text()[contains(., "Show all") and contains(., "projects")]]/ancestor::a',
                    '//a[contains(@href, "/details/projects")]'
                ],
                'licenses_and_certifications': [
                    '#navigation-index-see-all-licenses-and-certifications',
                    '//span[text()[contains(., "Show all") and (contains(., "licenses") or contains(., "certifications"))]]/ancestor::a',
                    '//a[contains(@href, "/details/certifications")]',
                    '//a[contains(@href, "/details/licenses")]'
                ]
            }
            
            # Check if section selector exists
            selectors = section_selectors.get(section, [])
            
            # Try each selector
            for selector in selectors:
                # Log the exact selector being used
                logger.info(f"Attempting to find '{section}' expansion button with selector: {selector}")
                
                try:
                    # Wait for the selector to be visible with a timeout
                    await page.wait_for_selector(selector, state='visible', timeout=5000)
                    logger.info(f"Found '{section}' expansion button with selector: {selector}")
                    
                    # Get the button and its href
                    button = page.locator(selector).first
                    href = await button.get_attribute('href')
                    
                    if href:
                        # Navigate to the full section page
                        logger.info(f"Navigating to full {section} section: {href}")
                        await page.goto(href, wait_until='domcontentloaded', timeout=30000)
                        
                        # Wait for the page to be visually stable
                        await page.wait_for_load_state('domcontentloaded', timeout=10000)
                        await page.wait_for_timeout(random.uniform(3000, 5000))
                        
                        # Capture expanded section HTML
                        expanded_html = await page.content()
                        
                        # Store HTML in memory
                        self.html_content[f'{section}_expanded_html'] = expanded_html
                        
                        # Save expanded section HTML only in debug mode
                        if self.debug_mode:
                            section_html_path = os.path.join(self.html_pages_dir, f'{section}_expanded_html.txt')
                            with open(section_html_path, 'w', encoding='utf-8') as f:
                                f.write(expanded_html)
                        
                        # Go back to the original profile page
                        await page.go_back(wait_until='domcontentloaded', timeout=30000)
                        await page.wait_for_timeout(random.uniform(3000, 5000))
                        
                        logger.info(f"Expanded {section} section HTML captured")
                        return
                    else:
                        logger.info(f"Found '{section}' button but no href attribute")
                        
                except Exception as e:
                    logger.info(f"Selector '{selector}' not found or timed out: {e}")
                    continue
            
            # If no buttons found after trying all selectors
            logger.info(f"No '{section}' expansion button found")
        
        except Exception as e:
            logger.error(f"Error with '{section}' expansion button: {e}")
        
        except Exception as ex:
            logger.error(f"Error expanding {section} section: {ex}")
            
    async def scrape_company_about_pages(self, browser: Browser, context: BrowserContext, page: Page):
        """
        Scrape about pages for companies listed in the profile's experience section
        """
        try:
            # Extract current companies from the profile
            # Check if we have experiences_expanded_html in memory
            if 'experiences_expanded_html' in self.html_content:
                company_urls = extract_current_companies(self.html_content.get('experiences_expanded_html', ''))
            else:
                # Fall back to profile HTML if experiences section isn't expanded
                company_urls = extract_current_companies(self.html_content.get('profile_html', ''))
            
            if not company_urls:
                logger.info("No company URLs found to scrape")
                return
            
            logger.info(f"Found {len(company_urls)} company URLs to scrape")
            
            # Create a directory for company about pages if in debug mode
            company_pages_dir = None
            if self.debug_mode:
                company_pages_dir = os.path.join(self.html_pages_dir, 'company_about_pages')
                os.makedirs(company_pages_dir, exist_ok=True)
            
            # Visit each company page and extract the about page
            for i, company_url in enumerate(company_urls):
                try:
                    logger.info(f"Processing company {i+1}/{len(company_urls)}: {company_url}")
                    
                    # Extract company name from URL for better identification
                    company_name = "unknown_company"
                    if '/company/' in company_url:
                        company_name = company_url.split('/company/')[1].split('/')[0]
                    
                    # Navigate to the company page
                    await page.goto(company_url, wait_until='domcontentloaded', timeout=45000)
                    await page.wait_for_timeout(random.uniform(3000, 5000))
                    
                    # First get the main company page HTML
                    main_company_html = await page.content()
                    
                    # Store main company page HTML in memory
                    self.html_content[f'company_{i}_main_html'] = main_company_html
                    
                    # Save main company page HTML only in debug mode
                    if self.debug_mode and company_pages_dir:
                        main_html_path = os.path.join(company_pages_dir, f'{company_name}_main.txt')
                        with open(main_html_path, 'w', encoding='utf-8') as f:
                            f.write(main_company_html)
                    
                    # Try to find and navigate to the About page using multiple selectors
                    about_url = None
                    about_selectors = [
                        'a.org-page-navigation__item-anchor:has-text("About")',
                        'a[href*="/about/"]:has-text("About")',
                        'a[href*="/about"]',
                        '//a[contains(@href, "/about") and contains(text(), "About")]',
                        'a.ember-view[href*="about"]'
                    ]
                    
                    for selector in about_selectors:
                        try:
                            logger.info(f"Looking for About link with selector: {selector}")
                            about_element = None
                            
                            # Try different methods to find the element
                            if selector.startswith('//'):
                                # XPath selector
                                about_element = await page.query_selector_all(f"xpath={selector}")
                                if about_element and len(about_element) > 0:
                                    about_element = about_element[0]
                            else:
                                # CSS selector
                                about_element = await page.query_selector(selector)
                            
                            if about_element:
                                about_href = await about_element.get_attribute('href')
                                if about_href:
                                    if not about_href.startswith('http'):
                                        about_url = f"https://www.linkedin.com{about_href}"
                                    else:
                                        about_url = about_href
                                    logger.info(f"Found About link: {about_url}")
                                    break
                        except Exception as e:
                            logger.debug(f"Selector '{selector}' not found or error: {e}")
                    
                    # If we couldn't find the about link, try to construct it
                    if not about_url and '/company/' in company_url:
                        # Construct the about URL by appending /about to the company URL
                        base_url = company_url.split('?')[0].rstrip('/')
                        about_url = f"{base_url}/about/"
                        logger.info(f"Constructed About URL: {about_url}")
                    
                    # Navigate to the about page if we have a URL
                    about_html = None
                    if about_url:
                        try:
                            logger.info(f"Navigating to About page: {about_url}")
                            await page.goto(about_url, wait_until='domcontentloaded', timeout=45000)
                            await page.wait_for_timeout(random.uniform(3000, 5000))
                            
                            # Get the about page HTML
                            about_html = await page.content()
                            
                            # Store about page HTML in memory
                            self.html_content[f'company_{i}_about_html'] = about_html
                            
                            # Save about page HTML only in debug mode
                            if self.debug_mode and company_pages_dir:
                                about_html_path = os.path.join(company_pages_dir, f'{company_name}_about.txt')
                                with open(about_html_path, 'w', encoding='utf-8') as f:
                                    f.write(about_html)
                        except Exception as e:
                            logger.warning(f"Error navigating to About page: {e}")
                    
                    # Store the best HTML content for company info extraction
                    # Prioritize about page HTML if available, otherwise use main page
                    if about_html:
                        self.html_content[f'company_{i}_html'] = about_html
                    else:
                        self.html_content[f'company_{i}_html'] = main_company_html
                        logger.warning(f"Using main company page for {company_name} as About page not available")
                    
                    logger.info(f"Company {i+1} HTML captured successfully")
                    
                    # Add a delay between company scrapes to avoid rate limiting
                    await page.wait_for_timeout(random.uniform(2000, 4000))
                    
                except Exception as e:
                    logger.error(f"Error scraping company {i+1}: {e}")
            
            logger.info("Finished scraping company about pages")
            
        except Exception as e:
            logger.error(f"Error in scrape_company_about_pages: {e}")
            
        except Exception as e:
            logger.error(f"Error in scrape_company_about_pages: {e}")
    
    def get_html_content(self) -> Dict[str, str]:
        """
        Get the HTML content stored in memory.
        
        Returns:
            Dict[str, str]: Dictionary of HTML content with keys like 'profile_html', 
                           '{section}_expanded_html', etc.
        """
        return self.html_content