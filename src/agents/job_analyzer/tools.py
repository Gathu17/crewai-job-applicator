"""
Scraping tools that can be used by the JobAnalyzerAgent.

Historically, job descriptions were passed directly into the analyzer.
This module re‑introduces a simple, explicit scraping tool for cases where
you have only a job URL (for example a LinkedIn job link) and want the
agent to fetch the full description first.
"""

from crewai.tools import BaseTool

from src.integrations.scraping.linkedin_client import scrape_linkedin_job
from src.integrations.scraping.scraper import scrape_url_sync


class ScrapeJobPostingTool(BaseTool):
    """
    Generic tool to scrape job posting URLs using the unified scraper.

    Uses Playwright / Firecrawl / Puppeteer depending on configuration.
    Prefer this when you want robust scraping across many sites.
    """

    name: str = "scrape_job_posting"
    description: str = (
        "Scrape a job posting URL to get full job details as plain text. "
        "Use when you have a job URL and need the full job description for analysis. "
        "Uses the unified scraper (Firecrawl / Playwright / Puppeteer)."
    )

    def _run(self, url: str) -> str:
        try:
            # For non-LinkedIn job postings we prefer the Playwright-based
            # scraper, which is more robust for interactive job boards.
            content = scrape_url_sync(url, backend="playwright")
            if not content or not content.strip():
                return (
                    "No content found at URL. Please provide the job description text directly."
                )
            return content
        except ImportError as e:
            return (
                f"Scraping dependencies not installed: {e}. "
                "Install with: pip install playwright && playwright install chromium. "
                "Otherwise, paste the job description text directly."
            )
        except Exception as e:
            return (
                f"Error scraping URL: {e}. "
                "Please provide the job description text directly."
            )


class LinkedInJobScraperTool(BaseTool):
    """
    Specialized tool to scrape LinkedIn job posting pages using requests + BeautifulSoup.

    Use this when the job URL is a LinkedIn job link and you want a clean,
    analyzer‑ready text blob containing title, company, location, and description.
    """

    name: str = "linkedin_job_scraper"
    description: str = (
        "Scrape a LinkedIn job URL and return a clean job description string "
        "containing title, company, location, and full description text."
    )

    def _run(self, url: str) -> str:
        if "linkedin.com" not in url:
            return (
                "This tool is intended for LinkedIn job URLs only. "
                "For other sites, use the scrape_job_posting tool instead."
            )

        return scrape_linkedin_job(url)


def get_job_analyzer_tools():
    """
    Tools that can be attached to the JobAnalyzerAgent when you want it
    to be able to scrape job URLs on its own.

    Returns:
        List of tools:
        - scrape_job_posting: generic scraper via unified scraping backend
        - linkedin_job_scraper: LinkedIn‑optimized scraper using requests + BeautifulSoup
    """
    return [
        ScrapeJobPostingTool(),
        LinkedInJobScraperTool(),
    ]
