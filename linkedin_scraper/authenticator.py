import asyncio
import random
import logging
import os
from typing import Optional, Tuple

from playwright.async_api import async_playwright, Page, Browser, BrowserContext

class LinkedinAuthenticator:
    @classmethod
    async def login(
        cls, 
        email: Optional[str] = None, 
        password: Optional[str] = None
    ) -> Tuple[Browser, BrowserContext, Page]:
        """
        Advanced LinkedIn login with comprehensive error handling and diagnostics
        """
        # Configure logging
        # Configure console logging only
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

        if not email or not password:
            logger.error("No LinkedIn credentials provided")
            raise ValueError("LinkedIn credentials are required")

        try:
            playwright = await async_playwright().start()
            
            # Launch browser in headless mode
            browser = await playwright.chromium.launch(
                headless=True,  # Run in headless mode
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-infobars',
                    '--disable-extensions',
                    '--no-sandbox',
                    '--disable-setuid-sandbox'
                ],
                timeout=60000
            )

            # Advanced context creation
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                geolocation={'latitude': 40.7128, 'longitude': -74.0060},
                permissions=['geolocation']
            )

            # Sophisticated anti-detection script
            await context.add_init_script("""
                // Prevent webdriver detection
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                
                // Simulate real browser environment
                window.navigator.chrome = {
                    runtime: {},
                    app: {},
                    loadTimes: () => {},
                    csi: () => {}
                };
                
                // Randomize plugins and mimetypes
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [{ name: 'Chrome PDF Plugin' }]
                });
            """)

            page = await context.new_page()

            # Advanced navigation with multiple strategies
            logger.info("Navigating to LinkedIn login")
            try:
                await page.goto('https://www.linkedin.com/login', 
                                wait_until='domcontentloaded', 
                                timeout=45000)
                
                # Additional human-like interactions
                await page.wait_for_timeout(random.uniform(2000, 5000))
                
                # Enter email
                logger.info("Entering email")
                await page.fill('input[name="session_key"]', email)
                await asyncio.sleep(random.uniform(0.5, 1.5))

                # Enter password
                logger.info("Entering password")
                await page.fill('input[name="session_password"]', password)
                await asyncio.sleep(random.uniform(0.5, 1.5))

                # Click login button
                logger.info("Clicking login button")
                await page.click('button[type="submit"]')
                await asyncio.sleep(random.uniform(2, 3))

                # More flexible navigation wait
                await page.wait_for_load_state('load', timeout=45000)
                
                # Verify login by checking current URL
                current_url = page.url
                logger.info(f"Current URL after login: {current_url}")

                # Check for potential login challenges
                if 'checkpoint' in current_url or 'login' in current_url:
                    logger.error("Login challenge detected")
                    raise RuntimeError("Login challenge detected")

                return browser, context, page

            except Exception as nav_error:
                # Error handling without screenshots
                logger.error(f"Navigation error: {nav_error}")
                raise

        except Exception as e:
            logger.error(f"Comprehensive login failure: {e}")
            raise RuntimeError(f"LinkedIn login failed: {e}")

    @staticmethod
    async def _human_type(page: Page, selector: str, text: str):
        """
        Simulate human-like typing with advanced randomization
        """
        await page.focus(selector)
        for char in text:
            # Varied typing speed and small random pauses
            await page.type(selector, char, delay=random.uniform(50, 250))
            await page.wait_for_timeout(random.uniform(20, 100))