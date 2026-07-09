"""
Crew Runner Service - Orchestrates CrewAI crews for job application workflows.
"""
import os
import yaml
import logging
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from crewai import Crew, Agent, Task, Process

from src.config.settings import settings
from src.core.llm_factory import create_llm
from src.agents.job_scout.agent import JobScoutAgent
from src.agents.job_analyzer.agent import JobAnalyzerAgent
from src.agents.company_research.agent import CompanyResearchAgent
from src.agents.tailor_optimize.agent import TailorOptimizeAgent
from src.agents.generate_resume.agent import GenerateResumeAgent
from src.agents.generate_report.agent import GenerateReportAgent
# from agents.matcher.agent import MatcherAgent
# from agents.tailor.agent import TailorAgent
# from agents.applicator.agent import ApplicatorAgent
from src.core.rag.vector_store import VectorStore
from src.core.models.schemas import (
    JobSearchCriteria, JobPosting, MatchResult,
    JobAnalysis, CompanyResearch, TailorResult,
    GeneratedResume, WorkflowReport, Resume
)
from crewai.project import CrewBase, agent, crew, task
logger = logging.getLogger(__name__)


class CrewRunner:
    """Service for running CrewAI crews for different job application workflows."""
    
    def __init__(self, llm=None, vector_store: Optional[VectorStore] = None):
        """
        Initialize the crew runner.
        
        Args:
            llm: Optional LLM instance (LangChain LLM). If None, will be initialized from settings.
            vector_store: Optional vector store instance. If None, will be initialized from settings.
        """
        self.llm = llm or self._initialize_llm()
        # self.vector_store = vector_store or self._initialize_vector_store()
        
        # Initialize agents
        self.job_scout_agent = JobScoutAgent(llm=self.llm)
        self.job_analyzer_agent = JobAnalyzerAgent(llm=self.llm)
        self.company_research_agent = CompanyResearchAgent(llm=self.llm)
        self.tailor_optimize_agent = TailorOptimizeAgent(llm=self.llm)
        self.generate_resume_agent = GenerateResumeAgent(llm=self.llm)
        self.generate_report_agent = GenerateReportAgent(llm=self.llm)
        # self.matcher_agent = MatcherAgent(llm=self.llm, vector_store=self.vector_store)
        # self.tailor_agent = TailorAgent(llm=self.llm)
        # self.applicator_agent = ApplicatorAgent(llm=self.llm)
        
        # Load workflow configuration
        self.workflow_config = self._load_workflow_config()
    
    def _initialize_llm(self):
        """Initialize LLM from settings using LLM Factory."""
        return create_llm(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            provider=settings.LLM_PROVIDER
        )
    
    def _load_workflow_config(self) -> Dict[str, Any]:
        """Load workflow configuration from YAML file."""
        config_path = Path(__file__).parent.parent.parent / "config" / "workflows" / "default.yaml"
        if not config_path.exists():
            return {}
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    
    def _parse_job_scout_results(self, result_text: str) -> List[JobPosting]:
        """
        Parse job scout agent JSON output into structured JobPosting objects.
        
        Expects the agent to return a JSON array with job information.
        
        Args:
            result_text: JSON output from job scout agent
            
        Returns:
            List of JobPosting objects with extracted information
        """
        jobs = []
        
        try:
            # Extract JSON from the result (handle cases where there might be extra text)
            result_str = str(result_text).strip()
            

            json_start = result_str.find('[')
            json_end = result_str.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                logger.warning("No JSON array found in scout results")
                return jobs
            
            json_str = result_str[json_start:json_end]
            job_data = json.loads(json_str)
            
            # Ensure it's a list
            if not isinstance(job_data, list):
                job_data = [job_data]
            
            # Convert each job entry to JobPosting
            for idx, job_info in enumerate(job_data):
                try:
                    job = JobPosting(
                        id=f"scout_{idx}",
                        title=job_info.get('title', 'Unknown Job'),
                        company=job_info.get('company', 'Unknown Company'),
                        location=job_info.get('location'),
                        description=job_info.get('description', ''),
                        url=job_info.get('url'),
                        source=job_info.get('source', 'Unknown Source'),
                        metadata={
                            "scout_result": True,
                            "raw_data": job_info
                        }
                    )
                    jobs.append(job)
                    logger.debug(f"Parsed job {idx + 1}: {job.title} from {job.company}")
                except Exception as e:
                    logger.error(f"Error parsing job entry {idx}: {str(e)}")
                    continue
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from scout results: {str(e)}")
            logger.debug(f"Result text: {result_text}")
        except Exception as e:
            logger.error(f"Unexpected error parsing scout results: {str(e)}")
        
        return jobs
    
    def run_job_scout(
        self,
        search_criteria: JobSearchCriteria,
        config: Optional[Dict[str, Any]] = None
    ) -> List[JobPosting]:
        """
        Run the job scout crew to discover job opportunities.
        
        Args:
            search_criteria: Job search criteria
            config: Optional configuration override
            
        Returns:
            List of discovered job postings
        """
        # Get config from workflow or use provided
        workflow_config = self.workflow_config.get("stages", [])
        scout_config = next(
            (stage.get("config", {}) for stage in workflow_config if stage.get("agent") == "job_scout"),
            {}
        )
        if config:
            scout_config.update(config)
        
        # Create search criteria dict
        criteria_dict = {
            "role": search_criteria.role,
            "location": search_criteria.location,
            "remote": search_criteria.remote,
            "experience_level": search_criteria.experience_level.value,
            "skills": search_criteria.skills,
            "salary_min": search_criteria.salary_min,
            "salary_max": search_criteria.salary_max,
            **scout_config
        }
        
        # Create task
        task = self.job_scout_agent.create_scout_task(criteria_dict)
        
        # Create and run crew
        crew = Crew(
            agents=[self.job_scout_agent.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        logger.info(f"Job scout execution completed. Raw result: {result}")
        
        # Parse results into structured JobPosting objects
        jobs = self._parse_job_scout_results(str(result))
        logger.info(f"Parsed {len(jobs)} job postings from scout results")
        
        return jobs
    
    def run_matcher(
        self,
        job_postings: List[JobPosting],
        resume_context: str,
        config: Optional[Dict[str, Any]] = None
    ) -> List[MatchResult]:
        """
        Run the matcher crew to match jobs with resume.
        
        Args:
            job_postings: List of job postings to match
            resume_context: Resume content/context
            config: Optional configuration override
            
        Returns:
            List of match results with compatibility scores
        """
        # Get config from workflow or use provided
        workflow_config = self.workflow_config.get("stages", [])
        matcher_config = next(
            (stage.get("config", {}) for stage in workflow_config if stage.get("agent") == "matcher"),
            {}
        )
        if config:
            matcher_config.update(config)
        
        min_score = matcher_config.get("min_compatibility_score", 75)
        
        # Create tasks for each job posting
        tasks = []
        for job in job_postings:
            task = self.matcher_agent.create_match_task(
                job_description=job.description,
                resume_context=resume_context
            )
            tasks.append(task)
        
        # Create and run crew
        crew = Crew(
            agents=[self.matcher_agent.agent],
            tasks=tasks,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Parse results and filter by min score
        # This would need to be adapted based on actual agent output format
        match_results = []
        # Placeholder - would parse actual results here
        return match_results
    
    def run_tailor(
        self,
        job_posting: JobPosting,
        base_resume: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Run the tailor crew to generate customized resume and cover letter.
        
        Args:
            job_posting: Job posting to tailor for
            base_resume: Base resume content
            config: Optional configuration override
            
        Returns:
            Dictionary with 'resume' and 'cover_letter' keys
        """
        # Get config from workflow or use provided
        workflow_config = self.workflow_config.get("stages", [])
        tailor_config = next(
            (stage.get("config", {}) for stage in workflow_config if stage.get("agent") == "tailor"),
            {}
        )
        if config:
            tailor_config.update(config)
        
        # Create task
        task = self.tailor_agent.create_tailor_task(
            base_resume=base_resume,
            job_description=job_posting.description,
            job_title=job_posting.title,
            company=job_posting.company
        )
        
        # Create and run crew
        crew = Crew(
            agents=[self.tailor_agent.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Parse results (would need to be adapted based on actual output format)
        return {
            "resume": str(result),
            "cover_letter": str(result)
        }
    
    def run_applicator(
        self,
        job_posting: JobPosting,
        tailored_resume: str,
        cover_letter: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run the applicator crew to submit job application.
        
        Args:
            job_posting: Job posting to apply for
            tailored_resume: Tailored resume content
            cover_letter: Cover letter content
            config: Optional configuration override
            
        Returns:
            Dictionary with application status and details
        """
        # Get config from workflow or use provided
        workflow_config = self.workflow_config.get("stages", [])
        applicator_config = next(
            (stage.get("config", {}) for stage in workflow_config if stage.get("agent") == "applicator"),
            {}
        )
        if config:
            applicator_config.update(config)
        
        # Check if auto-submit is enabled
        auto_submit = applicator_config.get("auto_submit", False)
        require_review = applicator_config.get("require_review", True)
        
        if not auto_submit and require_review:
            return {
                "status": "pending_review",
                "message": "Application requires manual review before submission",
                "job": job_posting.dict(),
                "resume": tailored_resume,
                "cover_letter": cover_letter
            }
        
        # Create task
        job_data = {
            "title": job_posting.title,
            "company": job_posting.company,
            "url": str(job_posting.url) if job_posting.url else None
        }
        
        task = self.applicator_agent.create_apply_task(
            job_data=job_data,
            tailored_resume=tailored_resume,
            cover_letter=cover_letter
        )
        
        # Create and run crew
        crew = Crew(
            agents=[self.applicator_agent.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "status": "submitted",
            "message": "Application submitted successfully",
            "result": str(result)
        }
    
    
    def run_job_analyzer(self, job_description: str, job_url: Optional[str] = None) -> JobAnalysis:
        """Run the job analyzer agent on a job description.

        Args:
            job_description: The full job description text (from job_scout or other source)
            job_url: Optional URL of the job posting for reference

        Returns:
            JobAnalysis object with structured job information
        """
        task = self.job_analyzer_agent.create_analysis_task(job_description, job_url)
        crew = Crew(
            agents=[self.job_analyzer_agent.agent],
            tasks=[task],
            verbose=True
        )
        result = crew.kickoff()
        logger.info(f"Job analyzer result type: {type(result)}")

        if hasattr(result, 'json_dict') and result.json_dict:
            logger.info("Extracting json_dict from CrewOutput")
            data = result.json_dict
        elif hasattr(result, 'pydantic') and result.pydantic:
            logger.info("Extracting pydantic model from CrewOutput")
            return result.pydantic
        elif isinstance(result, JobAnalysis):
            logger.info("Result is already JobAnalysis instance")
            return result
        elif isinstance(result, dict):
            logger.info("Result is a dict")
            data = result
        else:
            logger.warning(f"Unexpected result type {type(result)}. Attempting to parse as string...")
            return self._parse_job_analysis(str(result))

        # Convert dict to JobAnalysis model
        try:
            logger.info(f"Converting data to JobAnalysis: {data}")
            return JobAnalysis(**data)
        except Exception as e:
            logger.error(f"Failed to convert to JobAnalysis: {e}")
            logger.error(f"Data: {data}")
            raise
    
    def run_company_research(self, company_name: str) -> CompanyResearch:
        """Run the company research agent."""
        task = self.company_research_agent.create_research_task({"company": company_name})
        crew = Crew(
            agents=[self.company_research_agent.agent],
            tasks=[task],
            verbose=True
        )
        result = crew.kickoff()
        logger.info(f"Company research result type: {type(result)}")

        # CrewAI returns a CrewOutput object when using output_json
        if hasattr(result, 'json_dict') and result.json_dict:
            logger.info("Extracting json_dict from CrewOutput")
            data = result.json_dict
        elif hasattr(result, 'pydantic') and result.pydantic:
            logger.info("Extracting pydantic model from CrewOutput")
            return result.pydantic
        elif isinstance(result, CompanyResearch):
            logger.info("Result is already CompanyResearch instance")
            return result
        elif isinstance(result, dict):
            logger.info("Result is a dict")
            data = result
        else:
            logger.warning(f"Unexpected result type {type(result)}. Attempting to parse as string...")
            return self._parse_company_research(str(result))

        # Convert dict to CompanyResearch model
        try:
            logger.info(f"Converting data to CompanyResearch: {data}")
            return CompanyResearch(**data)
        except Exception as e:
            logger.error(f"Failed to convert to CompanyResearch: {e}")
            logger.error(f"Data: {data}")
            raise
    
    def run_tailor_optimize(self, base_resume: str, job_analysis: JobAnalysis) -> TailorResult:
        """Run the tailor/optimize agent."""
        task = self.tailor_optimize_agent.create_tailor_task(base_resume, job_analysis.dict())
        crew = Crew(
            agents=[self.tailor_optimize_agent.agent],
            tasks=[task],
            verbose=True
        )
        result = crew.kickoff()
        logger.info(f"Tailor optimize result: {result}")
        return self._parse_tailor_result(str(result))
    
    def run_generate_resume(self, optimized_content: Dict[str, Any], output_format: str = "markdown") -> GeneratedResume:
        """Run the generate resume agent."""
        task = self.generate_resume_agent.create_generate_task(optimized_content, output_format)
        crew = Crew(
            agents=[self.generate_resume_agent.agent],
            tasks=[task],
            verbose=True
        )
        result = crew.kickoff()
        logger.info(f"Generate resume result: {result}")
        return self._parse_generated_resume(str(result))
    
    def run_generate_report(self, analysis: JobAnalysis, company: CompanyResearch, tailor: TailorResult, resume: GeneratedResume) -> WorkflowReport:
        """Run the generate report agent."""
        task = self.generate_report_agent.create_report_task(
            analysis.dict(), company.dict(), tailor.dict(), resume.dict()
        )
        crew = Crew(
            agents=[self.generate_report_agent.agent],
            tasks=[task],
            verbose=True
        )
        result = crew.kickoff()
        logger.info(f"Generate report result: {result}")
        return self._parse_workflow_report(str(result), analysis, company, tailor, resume)
    
    # JSON Parsing helpers
    def _parse_job_analysis(self, result_text: str) -> JobAnalysis:
        """Parse JSON output into JobAnalysis model."""
        return self._parse_json_to_model(result_text, JobAnalysis, "JobAnalysis")
    
    def _parse_company_research(self, result_text: str) -> CompanyResearch:
        """Parse JSON output into CompanyResearch model."""
        return self._parse_json_to_model(result_text, CompanyResearch, "CompanyResearch")
    
    def _parse_tailor_result(self, result_text: str) -> TailorResult:
        """Parse JSON output into TailorResult model."""
        return self._parse_json_to_model(result_text, TailorResult, "TailorResult")
    
    def _parse_generated_resume(self, result_text: str) -> GeneratedResume:
        """Parse JSON output into GeneratedResume model."""
        data = self._extract_json(result_text)
        if not data.get("resume_id"):
            data["resume_id"] = f"resume_{int(__import__('time').time())}"
        return GeneratedResume(**data)
    
    def _parse_json_to_model(self, result_text: str, model_class, model_name: str):
        """Generic JSON parsing helper."""
        try:
            data = self._extract_json(result_text)
            if not data:
                raise ValueError(f"No valid JSON data extracted from {model_name} result. Raw result: {result_text[:200]}")
            logger.info(f"Extracted data for {model_name}: {data}")
            return model_class(**data)
        except Exception as e:
            logger.error(f"Error parsing {model_name}: {str(e)}")
            logger.error(f"Raw result text: {result_text[:500]}")
            raise

    def _extract_json(self, result_text: str) -> Dict[str, Any]:
        """Extract JSON object/array from agent result text."""
        try:
            result_str = str(result_text).strip()

            # Try to parse the entire string as JSON first
            try:
                data = json.loads(result_str)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass

            # If that fails, try to extract JSON from the text
            json_start = result_str.find('{')
            json_end = result_str.rfind('}') + 1
            if json_start == -1 or json_end == 0:
                json_start = result_str.find('[')
                json_end = result_str.rfind(']') + 1

            if json_start == -1 or json_end == 0:
                logger.warning(f"No JSON found in result: {result_text[:200]}")
                return {}

            json_str = result_str[json_start:json_end]
            data = json.loads(json_str)
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            logger.error(f"Attempted to parse: {result_text[:200]}")
            return {}



@CrewBase
class ResumeCrew:
    """Crew for processing resumes using CrewBase pattern with YAML configuration."""

    # Path to configuration files
    agents_config = str(Path(__file__).parent.parent / "config" / "agents.yaml")
    tasks_config = str(Path(__file__).parent.parent / "config" / "tasks.yaml")

    def __init__(self, job_input: str = None, base_resume: str = None, company_name: str = None, llm=None):
        """
        Initialize the crew.

        Args:
            job_input: Job URL or job posting text
            base_resume: Base resume content
            company_name: Optional company name (extracted from job if not provided)
            llm: Optional LLM instance (LangChain LLM). If None, will be initialized from settings.
        """
        self.job_input = job_input
        self.base_resume = base_resume
        self.company_name = company_name
        self.llm = llm or self._initialize_llm()

        # Initialize agent instances
        self._job_analyzer = JobAnalyzerAgent(llm=self.llm)
        self._company_research = CompanyResearchAgent(llm=self.llm)
        self._tailor_optimize = TailorOptimizeAgent(llm=self.llm)
        self._generate_resume = GenerateResumeAgent(llm=self.llm)
        self._generate_report = GenerateReportAgent(llm=self.llm)

    def _initialize_llm(self):
        """Initialize LLM from settings using LLM Factory."""
        return create_llm(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            provider=settings.LLM_PROVIDER
        )

    @agent
    def job_analyzer_agent(self) -> Agent:
        """Create the job analyzer agent (loads config from YAML)."""
        return self._job_analyzer.agent

    @agent
    def company_research_agent(self) -> Agent:
        """Create the company research agent (loads config from YAML)."""
        return self._company_research.agent

    @agent
    def tailor_optimize_agent(self) -> Agent:
        """Create the tailor/optimize agent (loads config from YAML)."""
        return self._tailor_optimize.agent

    @agent
    def generate_resume_agent(self) -> Agent:
        """Create the generate resume agent (loads config from YAML)."""
        return self._generate_resume.agent

    @agent
    def generate_report_agent(self) -> Agent:
        """Create the generate report agent (loads config from YAML)."""
        return self._generate_report.agent

    @task
    def analyze_job_task(self) -> Task:
        """Task to analyze the job posting."""
        job_url = None
        job_description = self.job_input

        # Check if it's a URL
        if self.job_input and (self.job_input.startswith('http://') or self.job_input.startswith('https://')):
            job_url = self.job_input

            job_description = f"Job URL: {job_url}\nPlease analyze this job posting."

        return self._job_analyzer.create_analysis_task(job_description, job_url)

    @task
    def research_company_task(self) -> Task:
        """Task to research the company."""
       
        company = self.company_name or "Unknown Company"
        return self._company_research.create_research_task({"company": company})

    @task
    def tailor_resume_task(self) -> Task:
        """Task to tailor the resume."""
        return self._tailor_optimize.create_tailor_task(
            self.base_resume,
            {} 
        )

    @task
    def generate_resume_task(self) -> Task:
        """Task to generate the optimized resume."""
        return self._generate_resume.create_generate_task(
            {},  # Tailor data will be available from context
            "markdown"
        )

    @task
    def generate_report_task(self) -> Task:
        """Task to generate the comprehensive report."""
        return self._generate_report.create_report_task(
            {},  # All previous results will be available from context
            {},
            {},
            {}
        )

    @crew
    def crew(self) -> Crew:
        """Create the crew with all agents and tasks."""
        return Crew(
            agents=[
                self.job_analyzer_agent(),
                self.company_research_agent(),
                self.tailor_optimize_agent(),
                self.generate_resume_agent(),
                self.generate_report_agent()
            ],
            tasks=[
                self.analyze_job_task(),
                self.research_company_task(),
                self.tailor_resume_task(),
                self.generate_resume_task(),
                self.generate_report_task()
            ],
            verbose=True,
            process=Process.sequential  
        )


