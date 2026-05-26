"""
Tools for the Job Scout Agent.
"""
from typing import List, Dict, Any, Optional, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from src.core.models.schemas import JobSearchCriteria, JobPosting
from src.config.settings import settings
import json
import logging

logger = logging.getLogger(__name__)


# @tool
# def search_jooble_jobs(role: str, location: Optional[str] = None, remote: bool = False) -> str:
#     """
#     Search for jobs using the Jooble API.
    
#     Args:
#         role: Job role or title to search for
#         location: Location to search in (optional)
#         remote: Whether to search for remote jobs
    
#     Returns:
#         JSON string of job postings
#     """
#     if not settings.JOOBLE_API_KEY:
#         return "Jooble API key not configured"
    
#     try:
#         jooble = JoobleAPI(api_key=settings.JOOBLE_API_KEY)
#         criteria = JobSearchCriteria(
#             role=role,
#             location=location,
#             remote=remote
#         )
        
#         # Run async function
#         loop = asyncio.get_event_loop()
#         if loop.is_running():
#             # If loop is already running, create a new task
#             import concurrent.futures
#             with concurrent.futures.ThreadPoolExecutor() as executor:
#                 future = executor.submit(asyncio.run, jooble.search_jobs(criteria))
#                 jobs = future.result()
#         else:
#             jobs = loop.run_until_complete(jooble.search_jobs(criteria))
        
#         # Convert to JSON string
#         import json
#         jobs_dict = [job.dict() for job in jobs]
#         return json.dumps(jobs_dict, default=str)
#     except Exception as e:
#         return f"Error searching Jooble: {str(e)}"



# Input schemas for tools
class JobSearchInput(BaseModel):
    """Input schema for job search."""
    role: str = Field(..., description="Job role or title to search for (e.g., 'software engineer', 'data scientist')")
    location: str = Field(default="", description="Location to search in (e.g., 'San Francisco, CA', 'Remote')")
    site_name: str = Field(default="linkedin", description="Job sites: 'linkedin', 'indeed', 'zip_recruiter', 'google'")


class JobSpySearchTool(BaseTool):
    name: str = "Search Jobs with JobSpy"
    description: str = "Search for jobs using JobSpy - supports LinkedIn, Indeed, ZipRecruiter, and Google"
    args_schema: Type[BaseModel] = JobSearchInput

    def _run(self, role: str, location: str = "", site_name: str = "linkedin") -> str:
        """Execute job search with JobSpy."""
        try:
            from jobspy import scrape_jobs

            # Use settings defaults
            results_wanted = settings.JOBSPY_DEFAULT_RESULTS
            hours_old = settings.JOBSPY_HOURS_OLD

            # Parse site_name input - can be comma-separated
            sites = [s.strip() for s in site_name.split(",")] if "," in site_name else [site_name]

            logger.info(f"JobSpy: Searching {sites} for '{role}' in '{location or 'any location'}'")

            # Build search parameters
            search_params = {
                "site_name": sites,
                "search_term": role,
                "results_wanted": results_wanted,
                "hours_old": hours_old,
                "linkedin_fetch_description": True,
            }

            # Add location if specified
            if location and location.lower() != "remote":
                search_params["location"] = location

            # Scrape jobs
            jobs_df = scrape_jobs(**search_params)

            if jobs_df is None or len(jobs_df) == 0:
                logger.warning(f"JobSpy: No jobs found")
                return json.dumps({"jobs": [], "total": 0, "message": "No jobs found"})

            logger.info(f"JobSpy: Found {len(jobs_df)} jobs")

            # Convert DataFrame to list of dicts
            jobs_list = jobs_df.to_dict('records')

            # Format the output
            formatted_jobs = []
            for job in jobs_list:
                formatted_job = {
                    "title": job.get("title", ""),
                    "company": job.get("company", ""),
                    "location": job.get("location", ""),
                    "description": job.get("description", "")[:500],  # Truncate
                    "job_url": job.get("job_url", ""),
                    "date_posted": str(job.get("date_posted", "")),
                    "is_remote": job.get("is_remote", False),
                    "site": job.get("site", ""),
                }
                formatted_jobs.append(formatted_job)

            result = {
                "jobs": formatted_jobs[:10],  # Limit to 10
                "total": len(formatted_jobs),
                "message": f"Found {len(formatted_jobs)} jobs, showing first 10"
            }

            return json.dumps(result, indent=2, default=str)

        except ImportError:
            error_msg = "JobSpy not installed. Install with: pip install python-jobspy"
            logger.error(error_msg)
            return json.dumps({"error": error_msg, "jobs": [], "total": 0})
        except Exception as e:
            error_msg = f"Error searching jobs: {str(e)}"
            logger.error(error_msg)
            return json.dumps({"error": error_msg, "jobs": [], "total": 0})


class LinkedInSearchInput(BaseModel):
    """Input schema for LinkedIn job search."""
    role: str = Field(..., description="Job role or title")
    location: str = Field(default="", description="Location to search")


class LinkedInJobsTool(BaseTool):
    name: str = "Search LinkedIn Jobs"
    description: str = "Search for jobs specifically on LinkedIn using JobSpy"
    args_schema: Type[BaseModel] = LinkedInSearchInput

    def _run(self, role: str, location: str = "") -> str:
        """Execute LinkedIn-specific job search."""
        tool = JobSpySearchTool()
        return tool._run(role=role, location=location, site_name="linkedin")


# List of all available tools for job scout
def get_job_scout_tools(use_jobspy: bool = True, use_serper: bool = False):
    """
    Get list of tools for job scout agent.

    Args:
        use_jobspy: Include JobSpy tool for job searching (default: True)
        use_serper: Include SerperDevTool for web search (default: False)

    Returns:
        List of tools for the job scout agent

    Recommended configuration:
        - use_jobspy=True, use_serper=False: Best for job searching (JobSpy is purpose-built)
        - use_jobspy=False, use_serper=True: Fallback to general web search
        - use_jobspy=True, use_serper=True: Both tools available (agent chooses)
    """
    tools = []

    # Add JobSpy tool (primary job search tool)
    if use_jobspy:
        tools.append(JobSpySearchTool())
        # tools.append(LinkedInJobsTool())
        logger.info("Job Scout Tools: JobSpy enabled (LinkedIn, Indeed, ZipRecruiter, Google)")

    # Add Serper tool (general web search, can find jobs but less structured)
    if use_serper:
        # Note: Serper requires crewai-tools package
        try:
            from crewai_tools import SerperDevTool
            if settings.SERPER_API_KEY:
                tools.append(SerperDevTool(api_key=settings.SERPER_API_KEY))
                logger.info("Job Scout Tools: Serper Dev enabled (general web search)")
            else:
                logger.warning("Job Scout Tools: SERPER_API_KEY not configured")
        except ImportError:
            logger.warning("Job Scout Tools: crewai-tools not installed, Serper unavailable")

    # Fallback: if no tools are available, add at least one
    if not tools:
        logger.warning("Job Scout Tools: No tools configured, adding JobSpy as fallback")
        tools.append(JobSpySearchTool())
        tools.append(LinkedInJobsTool())

    logger.info(f"Job Scout Tools: {len(tools)} tools loaded")
    return tools


# Default tool configuration: Use settings from .env
JOB_SCOUT_TOOLS = get_job_scout_tools(
    use_jobspy=settings.USE_JOBSPY,
    use_serper=settings.USE_SERPER_FOR_JOBS
)

