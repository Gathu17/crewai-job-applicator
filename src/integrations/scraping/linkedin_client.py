"""
LinkedIn job scraping helper using requests and BeautifulSoup.

This module is intended for scenarios where you have a direct LinkedIn job URL
and need to extract a clean job description string for job analysis.
"""

from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def scrape_linkedin_job(url: str, headers: Optional[Dict[str, str]] = None) -> str:
    """
    Scrape a LinkedIn job posting URL and return a text blob suitable
    to feed into the job analyzer.

    Args:
        url: LinkedIn job URL (e.g. https://www.linkedin.com/jobs/view/123456789/)
        headers: Optional extra/override headers for the HTTP request.

    Returns:
        A single string containing job title, company, location, and description.
        On failure, returns a short error message string.
    """
    merged_headers = {**DEFAULT_HEADERS, **(headers or {})}

    try:
        resp = requests.get(url, headers=merged_headers, timeout=20)
        if resp.status_code != 200:
            return f"Failed to scrape LinkedIn job. HTTP {resp.status_code}."

        soup = BeautifulSoup(resp.content, "html.parser")

        # These selectors may need adjustment over time as LinkedIn changes.
        title_el = soup.find("h1", class_="top-card-layout__title")
        company_el = soup.find("a", class_="topcard__org-name-link")
        if company_el is None:
            # Some variants use a span instead of a link
            company_el = soup.find("span", class_="topcard__flavor")
        location_el = soup.find("span", class_="topcard__flavor--bullet")
        description_el = soup.find("div", class_="description__text")
        if description_el is None:
            # Fallback selector used in some layouts
            description_el = soup.find("div", class_="show-more-less-html__markup")

        title = title_el.get_text(strip=True) if title_el else ""
        company = company_el.get_text(strip=True) if company_el else ""
        location = location_el.get_text(strip=True) if location_el else ""
        # get_text with separator keeps line breaks more readable
        description = (
            description_el.get_text(separator="\n", strip=True) if description_el else ""
        )

        if not any([title, company, location, description]):
            return (
                "Could not extract job fields from LinkedIn HTML. "
                "The page structure may have changed."
            )

        parts = []
        if title:
            parts.append(f"Job Title: {title}")
        if company:
            parts.append(f"Company: {company}")
        if location:
            parts.append(f"Location: {location}")
        if description:
            parts.append("Description:")
            parts.append(description)

        return "\n\n".join(parts)

    except Exception as exc:
        return f"Error scraping LinkedIn job: {exc}"

