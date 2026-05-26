"""
Unified web scraping interface supporting multiple backends.
"""
from typing import Optional, Dict, Any, Literal
import asyncio
from src.config.settings import settings


ScraperBackend = Literal["firecrawl", "playwright", "puppeteer", "auto"]


class WebScraper:
    """Unified web scraper that can use different backends."""
    
    def __init__(self, backend: ScraperBackend = "playwright"):
        """
        Initialize web scraper.

        Args:
            backend: Scraping backend to use ("firecrawl", "playwright", "puppeteer", or "auto")
        """
        self.backend = backend
        self._firecrawl_client = None
        self._playwright_client = None
        self._puppeteer_client = None
    
    


def scrape_url_sync(url: str, backend: ScraperBackend = "playwright") -> str:
    """
    Synchronous wrapper for scraping a URL.

    Args:
        url: URL to scrape
        backend: Scraping backend to use ("firecrawl", "playwright", "puppeteer", or "auto")

    Returns:
        Scraped text content
    """
    scraper = WebScraper(backend=backend)
    
    try:
        # Get or create event loop
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, use a new thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, scraper.scrape_url(url))
                    return future.result()
            else:
                return loop.run_until_complete(scraper.scrape_url(url))
        except RuntimeError:
            # No event loop, create a new one
            return asyncio.run(scraper.scrape_url(url))
    finally:
        # Clean up
        try:
            loop = asyncio.get_event_loop()
            if not loop.is_running():
                loop.run_until_complete(scraper.close())
        except:
            pass

