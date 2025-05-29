import asyncio
import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from . import LinkedinProfileScraper
from .profile_builder import LinkedInProfileScraper as ProfileBuilder
from .config import ScraperConfig

async def scrape_linkedin_profile(
    profile_url: str, 
    email: Optional[str] = None, 
    password: Optional[str] = None, 
    debug_mode: bool = False
) -> Optional[Dict]:
    """
    Scrape a LinkedIn profile and return the parsed data.
    
    Args:
        profile_url (str): The URL of the LinkedIn profile to scrape
        email (str, optional): LinkedIn login email. Defaults to environment variable LINKEDIN_EMAIL.
        password (str, optional): LinkedIn login password. Defaults to environment variable LINKEDIN_PASSWORD.
        debug_mode (bool, optional): If True, save HTML files to disk for debugging
        
    Returns:
        dict: The scraped and parsed profile data or None if scraping failed
        
    Example:
        >>> import asyncio
        >>> from linkedin_scraper import scrape_linkedin_profile
        >>> 
        >>> # Set credentials via environment variables
        >>> import os
        >>> os.environ['LINKEDIN_EMAIL'] = 'your_email@example.com'
        >>> os.environ['LINKEDIN_PASSWORD'] = 'your_password'
        >>> 
        >>> # Or pass credentials directly
        >>> profile_data = asyncio.run(scrape_linkedin_profile(
        >>>     'https://www.linkedin.com/in/username/',
        >>>     email='your_email@example.com',
        >>>     password='your_password'
        >>> ))
    """
    try:
        # Create scraper instance with debug mode setting
        scraper = LinkedinProfileScraper(debug_mode=debug_mode)
        
        # Scrape single profile
        success, html_content = await scraper.scrape_profile(
            profile_url, 
            email=email, 
            password=password
        )
        
        if success:
            # Initialize the profile builder with the HTML content dictionary
            profile_builder = ProfileBuilder(html_content_dict=html_content)
            
            # Build the profile data
            profile_data = profile_builder.scrape_profile()
            
            return profile_data
        else:
            logger.error("Failed to scrape LinkedIn profile")
            return None
    except Exception as e:
        logger.error(f"Error in scrape_linkedin_profile: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

async def save_profile_to_json(
    profile_url: str, 
    output_file: str = 'linkedin_profile.json',
    email: Optional[str] = None,
    password: Optional[str] = None,
    debug_mode: bool = False
) -> bool:
    """
    Scrape a LinkedIn profile and save the data to a JSON file.
    
    Args:
        profile_url (str): The URL of the LinkedIn profile to scrape
        output_file (str): Path to save the JSON output
        email (str, optional): LinkedIn login email
        password (str, optional): LinkedIn login password
        debug_mode (bool, optional): If True, save HTML files to disk for debugging
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Scrape LinkedIn profile
        profile_data = await scrape_linkedin_profile(
            profile_url,
            email=email,
            password=password,
            debug_mode=debug_mode
        )
        
        if profile_data:
            # Save the profile data to a JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Profile data has been saved to {os.path.abspath(output_file)}")
            return True
        else:
            logger.error("Failed to scrape LinkedIn profile")
            return False
    
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

async def main():
    """
    Example usage when running the module directly
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape LinkedIn profiles')
    parser.add_argument('profile_url', help='LinkedIn profile URL to scrape')
    parser.add_argument('--email', help='LinkedIn login email')
    parser.add_argument('--password', help='LinkedIn login password')
    parser.add_argument('--output', default='linkedin_profile.json', help='Output JSON file path')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    return await save_profile_to_json(
        args.profile_url,
        output_file=args.output,
        email=args.email,
        password=args.password,
        debug_mode=args.debug
    )

if __name__ == '__main__':
    asyncio.run(main())