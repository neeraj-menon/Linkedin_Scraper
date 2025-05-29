import random
import asyncio
from typing import Tuple

from playwright.async_api import Page

class RandomBehavior:
    """Utility class for simulating human-like browser interactions"""
    
    @staticmethod
    async def human_type(page: Page, selector: str, text: str):
        """
        Simulate human-like typing with random delays
        
        Args:
            page (Page): Playwright page object
            selector (str): CSS selector for input
            text (str): Text to type
        """
        await page.focus(selector)
        for char in text:
            await page.type(selector, char, delay=random.uniform(50, 200))
            await page.wait_for_timeout(random.uniform(50, 200))

    @staticmethod
    async def simulate_scroll(page: Page):
        """
        Simulate natural page scrolling
        
        Args:
            page (Page): Playwright page object
        """
        await page.evaluate("""
            () => {
                return new Promise((resolve) => {
                    let totalHeight = 0;
                    let distance = 100;
                    let timer = setInterval(() => {
                        let scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;

                        if(totalHeight >= scrollHeight){
                            clearInterval(timer);
                            resolve();
                        }
                    }, 200);
                });
            }
        """)

    @staticmethod
    def generate_random_wait() -> Tuple[float, float]:
        """
        Generate random wait times for more natural behavior
        
        Returns:
            Tuple of (min_wait, max_wait) in seconds
        """
        return (random.uniform(0.5, 2), random.uniform(2, 5))
