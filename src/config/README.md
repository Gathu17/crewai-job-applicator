# Configuration Files

This directory contains YAML configuration files for agents and tasks used in the job application automation system.

## Files

### `agents.yaml`
Defines the configuration for all AI agents including their:
- **role**: The agent's job title/role
- **goal**: What the agent aims to accomplish
- **backstory**: Context and expertise that shapes the agent's behavior

### `tasks.yaml`
Defines the configuration for all tasks including:
- **description**: Detailed instructions for what the task should accomplish
- **expected_output**: What format and content the task should return

### `prompts.py`
Python module that provides utilities to load and use the YAML configurations programmatically.

## Usage

### Using the PromptConfig class

```python
from src.config.prompts import PromptConfig

# Initialize the config loader
config = PromptConfig()

# Get agent configuration
job_analyzer_config = config.get_agent_config('job_analyzer')
print(job_analyzer_config['role'])
print(job_analyzer_config['goal'])
print(job_analyzer_config['backstory'])

# Get task configuration
analyze_job_config = config.get_task_config('analyze_job')
print(analyze_job_config['description'])
print(analyze_job_config['expected_output'])

# Format task description with variables
formatted_desc = config.format_task_description(
    'analyze_job',
    job_input='https://example.com/job-posting'
)
```

### Using convenience functions

```python
from src.config.prompts import get_agent_prompt, get_task_prompt

# Get agent configuration
agent_config = get_agent_prompt('company_research')

# Get task configuration with formatted description
task_config = get_task_prompt(
    'research_company',
    company_name='Acme Corp'
)
```

### Using in CrewAI agents

```python
from crewai import Agent, Task
from src.config.prompts import get_agent_prompt, get_task_prompt

# Create an agent from YAML config
config = get_agent_prompt('job_analyzer')
agent = Agent(
    role=config['role'],
    goal=config['goal'],
    backstory=config['backstory'],
    verbose=True,
    llm=llm
)

# Create a task from YAML config
task_config = get_task_prompt(
    'analyze_job',
    job_input='https://example.com/job'
)
task = Task(
    description=task_config['description'],
    expected_output=task_config['expected_output'],
    agent=agent
)
```

## Available Agents

- `job_analyzer` - Analyzes job postings and extracts structured information
- `company_research` - Researches companies and gathers relevant information
- `tailor_optimize` - Optimizes resumes for specific job postings
- `generate_resume` - Generates professionally formatted resumes
- `generate_report` - Creates comprehensive application reports
- `job_scout` - Discovers job opportunities from multiple sources

## Available Tasks

- `analyze_job` - Analyze a job posting
  - Variables: `{job_input}`
- `research_company` - Research a company
  - Variables: `{company_name}`
- `tailor_resume` - Tailor a resume for a job
  - Variables: `{base_resume}`, `{job_analysis}`
- `generate_resume` - Generate a formatted resume
  - Variables: `{optimized_content}`, `{output_format}`
- `generate_report` - Generate a comprehensive report
  - Variables: `{job_analysis}`, `{company_research}`, `{tailor_recommendations}`, `{generated_resume}`
- `scout_jobs` - Search for job opportunities
  - Variables: `{search_criteria}`

## Customization

You can customize the prompts by editing the YAML files directly. The changes will be automatically picked up when the configuration is reloaded.

### Tips for writing effective prompts:

1. **Be specific**: Clearly define what you want the agent to do
2. **Provide context**: Give the agent background information about its role
3. **Define output format**: Specify exactly what format you expect (JSON, text, etc.)
4. **Use examples**: Include examples in the description when helpful
5. **Set expectations**: Clearly state what constitutes success

## Example: Adding a new agent

```yaml
# In agents.yaml
new_agent_name:
  role: >
    Agent Role Title
  goal: >
    What this agent aims to accomplish
  backstory: >
    Background and expertise that shapes behavior
```

## Example: Adding a new task

```yaml
# In tasks.yaml
new_task_name:
  description: >
    Detailed instructions for the task.
    
    Input: {variable_name}
    
    Steps:
    1. First step
    2. Second step
    
    Return format: JSON object with specific fields
  expected_output: >
    Description of what the output should contain
```

