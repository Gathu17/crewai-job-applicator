"""
Application settings and configuration.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Job Application Automation"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, description="Debug mode")
    ENVIRONMENT: str = Field(default="development", description="Environment (development, staging, production)")
    
    # API Configuration
    API_HOST: str = Field(default="0.0.0.0", description="API host")
    API_PORT: int = Field(default=8000, description="API port")
    API_WORKERS: int = Field(default=4, description="Number of API workers")
    
    # LLM Configuration
    # Provider: openai, anthropic, google, groq, ollama, openrouter, huggingface
    LLM_PROVIDER: str = Field(default="openai", description="LLM provider to use")

    # API Keys
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, description="Anthropic API key")
    GOOGLE_API_KEY: Optional[str] = Field(default=None, description="Google API key")
    GROQ_API_KEY: Optional[str] = Field(default=None, description="Groq API key")
    OPENROUTER_API_KEY: Optional[str] = Field(default=None, description="OpenRouter API key")
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, description="Hugging Face API token (HF_TOKEN)")

    # Ollama configuration
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434", description="Ollama base URL")

    # Model selection
    LLM_MODEL: str = Field(default="gpt-4o-mini", description="Default LLM model for most tasks")
    LLM_MODEL_PREMIUM: str = Field(default="gpt-4o", description="Premium model for complex/creative tasks")

    # Temperature settings
    LLM_TEMPERATURE: float = Field(default=0.7, description="Default LLM temperature")
    LLM_TEMPERATURE_FACTUAL: float = Field(default=0.3, description="Temperature for factual/extraction tasks")
    LLM_TEMPERATURE_CREATIVE: float = Field(default=0.9, description="Temperature for creative tasks")

    # Cost optimization
    ENABLE_RESULT_CACHING: bool = Field(default=True, description="Enable caching of LLM results")
    CACHE_TTL_MINUTES: int = Field(default=60, description="Cache time-to-live in minutes")
    CREW_VERBOSE: bool = Field(default=False, description="Enable verbose mode for CrewAI (increases token usage)")
    
    # RAG Configuration
    EMBEDDING_MODEL: str = Field(default="all-MiniLM-L6-v2", description="Embedding model name")
    VECTOR_DB_PATH: str = Field(default="./data/lancedb", description="Vector database path")
    
    # Job APIs
    JOOBLE_API_KEY: Optional[str] = Field(default=None, description="Jooble API key")
    LINKEDIN_API_KEY: Optional[str] = Field(default=None, description="LinkedIn API key")
    SERPER_API_KEY: Optional[str] = Field(default=None, description="Serper API key for Google Search")
    
    # Scraping
    FIRECRAWL_API_KEY: Optional[str] = Field(default=None, description="Firecrawl API key")
    PLAYWRIGHT_HEADLESS: bool = Field(default=True, description="Run Playwright in headless mode")
    
    # Storage
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="AWS access key")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="AWS secret key")
    AWS_REGION: str = Field(default="us-east-1", description="AWS region")
    S3_BUCKET: Optional[str] = Field(default=None, description="S3 bucket name")
    
    GOOGLE_SHEETS_CREDENTIALS: Optional[str] = Field(default=None, description="Path to Google Sheets credentials")
    
    # Notifications
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None, description="Telegram bot token")
    TELEGRAM_CHAT_ID: Optional[str] = Field(default=None, description="Telegram chat ID")
    SMTP_HOST: Optional[str] = Field(default=None, description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USER: Optional[str] = Field(default=None, description="SMTP username")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="SMTP password")
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./data/jobs.db", description="Database URL")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_DIR: str = Field(default="./logs", description="Log directory")
    
    # Feature Flags
    ENABLE_AUTO_APPLY: bool = Field(default=False, description="Enable automatic job application")
    ENABLE_NOTIFICATIONS: bool = Field(default=True, description="Enable notifications")
    ENABLE_SCRAPING: bool = Field(default=True, description="Enable web scraping")

    # Job Search Tool Configuration
    USE_JOBSPY: bool = Field(default=True, description="Use JobSpy for job searching (LinkedIn, Indeed, etc.)")
    USE_SERPER_FOR_JOBS: bool = Field(default=False, description="Use Serper Dev for job searching (general web search)")
    JOBSPY_DEFAULT_RESULTS: int = Field(default=20, description="Default number of results from JobSpy")
    JOBSPY_HOURS_OLD: int = Field(default=168, description="Only return jobs posted within this many hours (default: 168 = 1 week)")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


