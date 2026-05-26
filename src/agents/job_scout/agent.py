"""
Job Scout Agent - Responsible for discovering and scraping job opportunities.
"""
from typing import List, Dict, Any
import json
from crewai import Agent, Task

from src.agents.job_scout.tools import get_job_scout_tools
from src.config.prompts import get_agent_prompt, get_task_prompt


class JobScoutAgent:
    """Agent that scouts for job opportunities using various sources."""

    def __init__(self, llm=None, tools=None):
        """
        Initialize the job scout agent.

        Args:
            llm: LLM instance for the agent
            tools: Optional list of tools. If None, uses default tools from get_job_scout_tools()
        """
        self.llm = llm
        self.tools = tools or get_job_scout_tools()
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with tools using YAML configuration."""
        config = get_agent_prompt('job_scout')
        return Agent(
            role=config.get('role', 'Job Scout'),
            goal=config.get('goal', 'Find relevant job opportunities'),
            backstory=config.get('backstory', 'You are an expert job scout.'),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )

    def create_scout_task(self, search_criteria: Dict[str, Any]) -> Task:
        """Create a task for scouting jobs."""
        # Convert search_criteria to JSON string for the prompt
        search_criteria_str = json.dumps(search_criteria, indent=2)

        # Get task configuration from YAML
        task_config = get_task_prompt('scout_jobs', search_criteria=search_criteria_str)

        return Task(
            description=task_config['description'],
            agent=self.agent,
            expected_output=task_config['expected_output']
        )


