"""
Pydantic models and schemas for the job application system.
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ExperienceLevel(str, Enum):
    """Experience level enum."""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"


class ApplicationStatus(str, Enum):
    """Application status enum."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    REVIEWING = "reviewing"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class JobSearchCriteria(BaseModel):
    """Job search criteria model."""
    role: str = Field(..., description="Job role or title")
    location: Optional[str] = Field(None, description="Preferred location")
    remote: bool = Field(False, description="Remote work preference")
    experience_level: ExperienceLevel = Field(ExperienceLevel.MID, description="Experience level")
    skills: List[str] = Field(default_factory=list, description="Required skills")
    salary_min: Optional[int] = Field(None, description="Minimum salary")
    salary_max: Optional[int] = Field(None, description="Maximum salary")


class JobPosting(BaseModel):
    """Job posting model."""
    id: Optional[str] = None
    title: str
    company: str
    location: Optional[str] = None
    description: str
    requirements: List[str] = Field(default_factory=list)
    url: Optional[str] = None  # Changed from HttpUrl to str for JSON serialization
    salary_range: Optional[str] = None
    posted_date: Optional[datetime] = None
    source: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Resume(BaseModel):
    """Resume model."""
    id: Optional[str] = None
    candidate_name: str
    email: str
    phone: Optional[str] = None
    summary: str
    skills: List[str]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    certifications: List[str] = Field(default_factory=list)
    projects: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MatchResult(BaseModel):
    """Job-resume match result."""
    job_id: str
    resume_id: str
    compatibility_score: float = Field(..., ge=0, le=100)
    matching_skills: List[str]
    missing_requirements: List[str]
    strengths: List[str]
    recommendations: List[str]
    created_at: datetime = Field(default_factory=datetime.now)


class TailoredDocument(BaseModel):
    """Tailored resume or cover letter."""
    job_id: str
    resume_id: str
    document_type: str  # 'resume' or 'cover_letter'
    content: str
    format: str = "markdown"
    created_at: datetime = Field(default_factory=datetime.now)


class JobApplication(BaseModel):
    """Job application model."""
    id: Optional[str] = None
    job_id: str
    resume_id: str
    status: ApplicationStatus = ApplicationStatus.PENDING
    tailored_resume_id: Optional[str] = None
    cover_letter_id: Optional[str] = None
    submitted_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


# API Request/Response Models
class JobSearchRequest(BaseModel):
    """Request model for job search."""
    criteria: JobSearchCriteria
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional configuration override")


class JobSearchResponse(BaseModel):
    """Response model for job search."""
    jobs: List[JobPosting] = Field(default_factory=list)
    total: int = 0
    message: str = "Job search completed successfully"


class MatchRequest(BaseModel):
    """Request model for job matching."""
    job_ids: List[str] = Field(..., description="List of job IDs to match")
    resume_context: str = Field(..., description="Resume content or context")
    resume_id: Optional[str] = Field(None, description="Resume ID if stored")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional configuration override")


class MatchResponse(BaseModel):
    """Response model for job matching."""
    matches: List[MatchResult] = Field(default_factory=list)
    total_matched: int = 0
    message: str = "Matching completed successfully"


class TailorRequest(BaseModel):
    """Request model for document tailoring."""
    job_posting: JobPosting = Field(..., description="Job posting to tailor for")
    base_resume: str = Field(..., description="Base resume content")
    resume_id: Optional[str] = Field(None, description="Resume ID if stored")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional configuration override")


class TailorResponse(BaseModel):
    """Response model for document tailoring."""
    job_id: str
    resume: str
    cover_letter: str
    format: str = "markdown"
    message: str = "Documents tailored successfully"


class ApplyRequest(BaseModel):
    """Request model for job application."""
    job_posting: JobPosting = Field(..., description="Job posting to apply for")
    tailored_resume: str = Field(..., description="Tailored resume content")
    cover_letter: str = Field(..., description="Cover letter content")
    resume_id: Optional[str] = Field(None, description="Resume ID if stored")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional configuration override")


class ApplyResponse(BaseModel):
    """Response model for job application."""
    application_id: Optional[str] = None
    status: str
    message: str
    job_id: str
    submitted_at: Optional[datetime] = None


class ResumeUploadRequest(BaseModel):
    """Request model for resume upload."""
    resume: Resume
    index_to_vector_store: bool = Field(True, description="Whether to index resume to vector store")


class ResumeUploadResponse(BaseModel):
    """Response model for resume upload."""
    resume_id: str
    message: str = "Resume uploaded successfully"
    indexed: bool = False


class WorkflowRequest(BaseModel):
    """Request model for full workflow execution."""
    search_criteria: JobSearchCriteria
    resume_context: str = Field(..., description="Resume content for matching")
    base_resume: str = Field(..., description="Base resume for tailoring")
    auto_apply: bool = Field(False, description="Whether to automatically submit applications")
    resume_id: Optional[str] = Field(None, description="Resume ID if stored")


class WorkflowResponse(BaseModel):
    """Response model for full workflow execution."""
    discovered_jobs: List[JobPosting] = Field(default_factory=list)
    matched_jobs: List[MatchResult] = Field(default_factory=list)
    tailored_documents: List[Dict[str, Any]] = Field(default_factory=list)
    applications: List[Dict[str, Any]] = Field(default_factory=list)
    message: str = "Workflow completed successfully"


class JobAnalysis(BaseModel):
    """Structured analysis of a job posting."""
    job_id: Optional[str] = None
    title: str
    summary: Optional[str] = None
    requirements: List[str] = Field(default_factory=list)
    key_skills: List[str] = Field(default_factory=list)
    seniority: Optional[str] = None
    apply_url: Optional[str] = None  # Changed from HttpUrl to str for JSON serialization

    model_config = {"json_schema_extra": {"example": {
        "job_id": "job_123",
        "title": "Senior Software Engineer",
        "summary": "Looking for an experienced engineer to build scalable systems",
        "requirements": ["5+ years Python", "AWS experience", "Microservices"],
        "key_skills": ["Python", "AWS", "Docker", "Kubernetes"],
        "seniority": "Senior",
        "apply_url": "https://example.com/jobs/123"
    }}}


class CompanyResearch(BaseModel):
    """Structured research about a company."""
    company: str
    size: Optional[str] = None
    industry: Optional[str] = None
    culture: Optional[str] = None
    recent_news: List[str] = Field(default_factory=list)
    interview_tips: List[str] = Field(default_factory=list)


class TailorResult(BaseModel):
    """Result of optimizing a resume for a job."""
    highlights: List[str] = Field(default_factory=list)
    changes: List[str] = Field(default_factory=list)
    score_before: Optional[float] = None
    score_after: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GeneratedResume(BaseModel):
    """Generated resume artifact."""
    resume_id: str
    format: str = "markdown"
    content: str
    created_at: datetime = Field(default_factory=datetime.now)


class WorkflowReport(BaseModel):
    """Final workflow report combining all artifacts."""
    job: JobPosting
    analysis: JobAnalysis
    company: CompanyResearch
    tailor: TailorResult
    resume: GeneratedResume
    report_id: Optional[str] = None
    summary: Optional[str] = None
    recommendations: List[str] = Field(default_factory=list)


