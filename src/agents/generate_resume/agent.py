"""
Generate Resume Agent - creates a formatted resume from optimized content.
"""
from typing import Dict, Any
import json
from crewai import Agent, Task
from src.config.prompts import get_agent_prompt, get_task_prompt


class GenerateResumeAgent:
    def __init__(self, llm=None, tools=None):
        self.llm = llm
        self.tools = tools or []
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create agent using YAML configuration."""
        config = get_agent_prompt('generate_resume')
        return Agent(
            role=config.get('role', 'Generate Resume'),
            goal=config.get('goal', 'Produce formatted resumes'),
            backstory=config.get('backstory', 'You create professional resumes.'),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools,
        )

    def create_generate_task(self, optimized_content: Dict[str, Any], output_format: str = "markdown") -> Task:
        """Create a task that returns a JSON object with the generated resume content."""
        optimized_content_str = json.dumps(optimized_content, indent=2)

        task_config = get_task_prompt(
            'generate_resume',
            optimized_content=optimized_content_str,
            output_format=output_format
        )

        return Task(
            description=task_config['description'],
            agent=self.agent,
            expected_output=task_config['expected_output']
        )
