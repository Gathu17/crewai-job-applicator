"""
FastAPI main application for job application automation orchestration.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import jobs, monitoring
from src.core.monitoring.llm_callback import LLMMonitorCallback
from src.core.llm_factory import create_llm
from src.config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# Global LLM Monitoring Setup
# ============================================

# Create global monitor
llm_monitor = LLMMonitorCallback(model=settings.LLM_MODEL)
logger.info(f"✅ LLM Monitor initialized for model: {settings.LLM_MODEL}")

monitoring.set_monitor(llm_monitor)
logger.info("✅ Monitoring API endpoints enabled")

# Create monitored LLM instances
try:
    # Basic LLM for analysis tasks
    monitored_llm_basic = create_llm(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE_FACTUAL,
        provider=settings.LLM_PROVIDER,
        callbacks=[llm_monitor]
    )
    logger.info(f"✅ Basic LLM created: {settings.LLM_PROVIDER}/{settings.LLM_MODEL}")

except Exception as e:
    logger.error(f"❌ Failed to create LLM: {e}")
    logger.error("Please check your .env file and ensure the correct API keys are set")
    logger.error(f"Current provider: {settings.LLM_PROVIDER}")
    logger.error("See docs/ALTERNATIVE_LLM_PROVIDERS.md for setup instructions")
    raise

# ============================================
# FastAPI App with Lifespan
# ============================================

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    logger.info(f"Provider: {settings.LLM_PROVIDER}")
    logger.info(f"Model: {settings.LLM_MODEL}")
    logger.info(f"Monitoring: Enabled")
    logger.info("=" * 70)

    yield

    # Shutdown
    logger.info("=" * 70)
    logger.info("🛑 Job Application Automation API Shutting Down")
    logger.info("=" * 70)


app = FastAPI(
    title="Job Application Automation API",
    description="CrewAI orchestration for automated job applications",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(jobs.router)
app.include_router(monitoring.router)
# app.include_router(resume.router)
# app.include_router(workflow.router)


@app.get("/")
async def root():
    """Root endpoint with system information."""
    return {
        "message": "Job Application Automation API",
        "status": "running",
        "llm_provider": settings.LLM_PROVIDER,
        "llm_model": settings.LLM_MODEL,
        "monitoring_enabled": True,
        "caching_enabled": settings.ENABLE_RESULT_CACHING
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "llm_provider": settings.LLM_PROVIDER,
        "monitoring": {
            "enabled": True,
            "total_calls": llm_monitor.call_count,
            "total_tokens": llm_monitor.total_tokens,
            "total_cost": round(llm_monitor.total_cost, 4)
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


