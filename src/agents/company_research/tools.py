"""
Tools for the Company Research Agent.
"""
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from src.config.settings import settings
# from src.integrations.scraping.firecrawl_client import FirecrawlClient
import asyncio


class ScrapeCompanyWebsiteTool(BaseTool):
    """Tool to scrape company websites using Firecrawl API."""

    name: str = "scrape_company_website"
    description: str = (
        "Scrape a company website to gather information about the company. "
        "Uses Firecrawl API for high-quality content extraction. "
        "Useful for getting company information from their official website, about page, or careers page."
    )

    def _run(self, url: str) -> str:
        """
        Scrape a company website to gather information about the company.

        Args:
            url: URL of the company website or careers page

        Returns:
            Scraped content as markdown string
        """
        if not settings.FIRECRAWL_API_KEY:
            return "Firecrawl API key not configured. Please set FIRECRAWL_API_KEY in environment."

        try:
            firecrawl = FirecrawlClient(api_key=settings.FIRECRAWL_API_KEY)

            # Run async function
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, firecrawl.scrape_url(url))
                    result = future.result()
            else:
                result = loop.run_until_complete(firecrawl.scrape_url(url))

            # Extract markdown content
            content = result.get("markdown", result.get("content", ""))
            if not content:
                return f"No content extracted from {url}"

            return content
        except Exception as e:
            return f"Error scraping company website: {str(e)}"


class SearchCompanyInfoTool(BaseTool):
    """Tool to search for company information using Google search."""

    name: str = "search_company_info"
    description: str = (
        "Search for company information using Google search. "
        "Useful for finding company size, industry, recent news, and culture information. "
        "Returns search results with relevant company details."
    )

    def _run(self, company_name: str) -> str:
        """
        Search for company information using Google search.

        Args:
            company_name: Name of the company to research

        Returns:
            Search results with company information
        """
        if not settings.SERPER_API_KEY:
            return "Serper API key not configured. Please set SERPER_API_KEY in environment."

        try:
            serper = SerperDevTool(api_key=settings.SERPER_API_KEY)
            query = f"{company_name} company size industry culture recent news"
            results = serper._run(query)
            return results
        except Exception as e:
            return f"Error searching for company info: {str(e)}"


def _create_serper_tool():
    """Create SerperDevTool instance with API key from settings."""
    if not settings.SERPER_API_KEY:
        return None
    return SerperDevTool(api_key=settings.SERPER_API_KEY)


def get_company_research_tools():
    """
    Get list of tools for company research agent.
    Includes Firecrawl scraping and Serper search tools.
    """
    tools = []

    # Add scraping tool if Firecrawl is configured
    if settings.FIRECRAWL_API_KEY:
        tools.append(ScrapeCompanyWebsiteTool())

    # Add search tool if Serper is configured
    if settings.SERPER_API_KEY:
        tools.append(SearchCompanyInfoTool())
        # Also add the SerperDevTool for general search
        serper_tool = _create_serper_tool()
        if serper_tool:
            tools.append(serper_tool)

    return tools


# Default tools list (for backward compatibility)
COMPANY_RESEARCH_TOOLS = get_company_research_tools()

