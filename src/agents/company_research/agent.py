"""
Company Research Agent - gathers company information and interview tips.
"""
from typing import Dict, Any
from crewai import Agent, Task
from src.config.prompts import get_agent_prompt, get_task_prompt
from src.agents.company_research.tools import get_company_research_tools


class CompanyResearchAgent:
    def __init__(self, llm=None, tools=None):
        self.llm = llm
        self.tools = tools or get_company_research_tools()
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create agent using YAML configuration."""
        config = get_agent_prompt('company_research')
        return Agent(
            role=config.get('role', 'Company Research'),
            goal=config.get('goal', 'Collect company profile information'),
            backstory=config.get('backstory', 'You research companies.'),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools,
        )

    def create_research_task(self, company_input: Dict[str, Any] | str) -> Task:
        """Create a task that requests a JSON object with company research fields.

        Uses Firecrawl to scrape company website and Serper to search for company information.
        """
        # Extract company name from input
        if isinstance(company_input, str):
            company_name = company_input
        else:
            company_name = company_input.get('company', str(company_input))

        # Get task configuration from YAML
        task_config = get_task_prompt('research_company', company_name=company_name)

        
        from src.core.models.schemas import CompanyResearch

        return Task(
            description=task_config['description'],
            agent=self.agent,
            expected_output=task_config['expected_output'],
            output_json=CompanyResearch  # Force JSON output matching the schema
        )
