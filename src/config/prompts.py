"""
Prompt configuration loader for agents and tasks.
Provides utilities to load and format prompts from YAML files.
"""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class PromptConfig:
    """Manages loading and accessing prompt configurations from YAML files."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the prompt configuration loader.
        
        Args:
            config_dir: Path to the config directory. If None, uses default location.
        """
        if config_dir is None:
            config_dir = Path(__file__).parent
        
        self.config_dir = config_dir
        self.agents_config_path = config_dir / "agents.yaml"
        self.tasks_config_path = config_dir / "tasks.yaml"
        
        self._agents_data: Optional[Dict[str, Any]] = None
        self._tasks_data: Optional[Dict[str, Any]] = None
    
    @property
    def agents(self) -> Dict[str, Any]:
        """Load and cache agents configuration."""
        if self._agents_data is None:
            with open(self.agents_config_path, 'r') as f:
                self._agents_data = yaml.safe_load(f) or {}
        return self._agents_data
    
    @property
    def tasks(self) -> Dict[str, Any]:
        """Load and cache tasks configuration."""
        if self._tasks_data is None:
            with open(self.tasks_config_path, 'r') as f:
                self._tasks_data = yaml.safe_load(f) or {}
        return self._tasks_data
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific agent.
        
        Args:
            agent_name: Name of the agent (e.g., 'job_analyzer')
            
        Returns:
            Dictionary with agent configuration (role, goal, backstory)
        """
        return self.agents.get(agent_name, {})
    
    def get_task_config(self, task_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific task.
        
        Args:
            task_name: Name of the task (e.g., 'analyze_job')
            
        Returns:
            Dictionary with task configuration (description, expected_output)
        """
        return self.tasks.get(task_name, {})
    
    def format_task_description(self, task_name: str, **kwargs) -> str:
        """
        Get and format a task description with provided variables.
        
        Args:
            task_name: Name of the task
            **kwargs: Variables to format into the description
            
        Returns:
            Formatted task description
        """
        config = self.get_task_config(task_name)
        description = config.get('description', '')
        
        try:
            return description.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable for task '{task_name}': {e}")
    
    def reload(self):
        """Reload configurations from YAML files."""
        self._agents_data = None
        self._tasks_data = None


# Global instance for easy access
prompt_config = PromptConfig()


def get_agent_prompt(agent_name: str) -> Dict[str, Any]:
    """
    Convenience function to get agent configuration.
    
    Args:
        agent_name: Name of the agent
        
    Returns:
        Agent configuration dictionary
    """
    return prompt_config.get_agent_config(agent_name)


def get_task_prompt(task_name: str, **kwargs) -> Dict[str, str]:
    """
    Convenience function to get task configuration with formatted description.
    
    Args:
        task_name: Name of the task
        **kwargs: Variables to format into the description
        
    Returns:
        Dictionary with 'description' and 'expected_output' keys
    """
    config = prompt_config.get_task_config(task_name)
    
    description = config.get('description', '')
    if kwargs:
        try:
            description = description.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable for task '{task_name}': {e}")
    
    return {
        'description': description,
        'expected_output': config.get('expected_output', '')
    }

