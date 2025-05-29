# Import key classes and functions for easy access
from .profile_scraper import LinkedinProfileScraper
from .authenticator import LinkedinAuthenticator
from .config import ScraperConfig

# Import and expose main functions directly at the package level
from .main import scrape_linkedin_profile, save_profile_to_json

# Version information
__version__ = "0.1.0"

# Expose key components
__all__ = [
    'LinkedinProfileScraper',
    'LinkedinAuthenticator',
    'ScraperConfig',
    'scrape_linkedin_profile',
    'save_profile_to_json'
]
