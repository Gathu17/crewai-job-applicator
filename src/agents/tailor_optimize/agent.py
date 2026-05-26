"""
Tailor/Optimize Agent - suggests resume optimizations for a target job.
"""
from typing import Dict, Any
import json
from crewai import Agent, Task
from src.config.prompts import get_agent_prompt, get_task_prompt


class TailorOptimizeAgent:
    def __init__(self, llm=None, tools=None):
        self.llm = llm
        self.tools = tools or []
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create agent using YAML configuration."""
        config = get_agent_prompt('tailor_optimize')
        return Agent(
            role=config.get('role', 'Tailor Optimizer'),
            goal=config.get('goal', 'Provide tailored resume improvements'),
            backstory=config.get('backstory', 'You optimize resumes for specific jobs.'),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools,
        )

    def create_tailor_task(self, base_resume: str, job_analysis: Dict[str, Any]) -> Task:
        """Create a task that returns JSON with tailoring recommendations and scores."""
        # Convert job_analysis to JSON string for the prompt
        job_analysis_str = json.dumps(job_analysis, indent=2)

        # Get task configuration from YAML
        task_config = get_task_prompt(
            'tailor_resume',
            base_resume=base_resume,
            job_analysis=job_analysis_str
        )

        return Task(
            description=task_config['description'],
            agent=self.agent,
            expected_output=task_config['expected_output']
        )
