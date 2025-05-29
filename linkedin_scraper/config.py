import os
from typing import Optional, Dict, Any

class ScraperConfig:
    """Configuration management for LinkedIn scraper"""
    
    @staticmethod
    def get_credentials() -> Dict[str, Optional[str]]:
        """
        Retrieve LinkedIn credentials from environment variables
        
        Returns:
            Dict containing email and password
        """
        return {
            'email': os.environ.get('LINKEDIN_EMAIL'),
            'password': os.environ.get('LINKEDIN_PASSWORD')
        }
    
    @staticmethod
    def get_browser_config() -> Dict[str, Any]:
        """
        Get browser configuration settings
        
        Returns:
            Dict with browser launch and context settings
        """
        return {
            'launch_options': {
                'headless': False,
                'args': [
                    '--disable-blink-features=AutomationControlled',
                    '--disable-infobars',
                    '--window-size=1920,1080'
                ]
            },
            'context_options': {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
                'viewport': {'width': 1920, 'height': 1080}
            }
        }
    
    @staticmethod
    def get_scraping_config() -> Dict[str, Any]:
        """
        Get scraping-specific configuration
        
        Returns:
            Dict with scraping settings
        """
        return {
            'scroll_delay': (0.1, 0.5),  # Random delay between scroll steps
            'type_delay': (50, 200),      # Random delay between keystrokes
            'wait_timeout': 10,           # Default timeout for page loads
            'max_retries': 3              # Maximum number of retries for failed operations
        }
