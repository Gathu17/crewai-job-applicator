"""
Generate Report Agent - compiles analysis, research, and tailoring into a final report.
"""
from typing import Dict, Any
import json
from crewai import Agent, Task
from src.config.prompts import get_agent_prompt, get_task_prompt


class GenerateReportAgent:
    def __init__(self, llm=None, tools=None):
        self.llm = llm
        self.tools = tools or []
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create agent using YAML configuration."""
        config = get_agent_prompt('generate_report')
        return Agent(
            role=config.get('role', 'Generate Report'),
            goal=config.get('goal', 'Create comprehensive reports'),
            backstory=config.get('backstory', 'You produce detailed reports.'),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools,
        )

    def create_report_task(self, analysis: Dict[str, Any], company: Dict[str, Any], tailor: Dict[str, Any], resume: Dict[str, Any]) -> Task:
        """Create a task that returns a JSON report object."""
        # Convert all inputs to JSON strings for the prompt
        job_analysis_str = json.dumps(analysis, indent=2)
        company_research_str = json.dumps(company, indent=2)
        tailor_recommendations_str = json.dumps(tailor, indent=2)
        generated_resume_str = json.dumps(resume, indent=2)

        # Get task configuration from YAML
        task_config = get_task_prompt(
            'generate_report',
            job_analysis=job_analysis_str,
            company_research=company_research_str,
            tailor_recommendations=tailor_recommendations_str,
            generated_resume=generated_resume_str
        )

        return Task(
            description=task_config['description'],
            agent=self.agent,
            expected_output=task_config['expected_output']
        )
