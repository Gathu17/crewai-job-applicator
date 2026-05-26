"""
Job Analyzer Agent - analyzes a job posting and extracts structured information.
"""
from typing import Optional

from crewai import Agent, Task

from src.config.prompts import get_agent_prompt, get_task_prompt
from src.agents.job_analyzer.tools import get_job_analyzer_tools


class JobAnalyzerAgent:
    def __init__(self, llm=None, tools=None):
        self.llm = llm
        # If no tools are provided, default to the job analyzer scraping tools.
        # This lets the agent decide when to scrape from a URL (LinkedIn vs others).
        self.tools = tools or get_job_analyzer_tools()
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create agent using YAML configuration."""
        config = get_agent_prompt('job_analyzer')
        return Agent(
            role=config.get('role', 'Job Analyzer'),
            goal=config.get('goal', 'Extract structured fields from a job posting'),
            backstory=config.get('backstory', 'You extract key information from job descriptions.'),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools,
        )

    def create_analysis_task(self, job_description: str, job_url: Optional[str] = None) -> Task:
        """Create a task that requests a JSON object with job analysis fields.

        Args:
            job_description: The full job description text (from job_scout or other source)
            job_url: Optional URL of the job posting for reference

        Returns:
            Task configured to analyze the job description and return structured JSON
        """
        # Prepare input text
        input_text = f"Job Description:\n{job_description}"
        if job_url:
            input_text = f"Job URL: {job_url}\n\n{input_text}"

        # Get task configuration from YAML
        task_config = get_task_prompt('analyze_job', job_input=input_text)

        # Define the expected JSON schema
        from src.core.models.schemas import JobAnalysis

        return Task(
            description=task_config['description'],
            agent=self.agent,
            expected_output=task_config['expected_output'],
            output_json=JobAnalysis  # Force JSON output matching the schema
        )
