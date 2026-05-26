"""
LLM Factory - Create LLM instances from different providers.

Supports: OpenAI, Anthropic, Google, Groq, Ollama, OpenRouter, Hugging Face

Note: Returns CrewAI LLM objects (not LangChain) for compatibility with CrewAI agents.
"""
import logging
from typing import Optional, List, Any

from src.config.settings import settings

logger = logging.getLogger(__name__)


def create_llm(
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    provider: Optional[str] = None,
    callbacks: Optional[List] = None
):
    """
    Create a CrewAI LLM instance based on the configured provider.

    Args:
        model: Model name (uses settings.LLM_MODEL if not provided)
        temperature: Temperature (uses settings.LLM_TEMPERATURE if not provided)
        provider: Provider name (uses settings.LLM_PROVIDER if not provided)
        callbacks: Optional callbacks for monitoring (Note: CrewAI LLM may not support all callback types)

    Returns:
        CrewAI LLM instance compatible with CrewAI agents

    Raises:
        ValueError: If provider is not supported or API key is missing
    """
    from crewai import LLM

    provider = provider or settings.LLM_PROVIDER
    model = model or settings.LLM_MODEL
    temperature = temperature if temperature is not None else settings.LLM_TEMPERATURE

    logger.info(f"Creating CrewAI LLM: provider={provider}, model={model}, temperature={temperature}")

    try:
        if provider == "openai":
            return _create_openai_llm(model, temperature)
        elif provider == "anthropic":
            return _create_anthropic_llm(model, temperature)
        elif provider == "google":
            return _create_google_llm(model, temperature)
        elif provider == "groq":
            return _create_groq_llm(model, temperature)
        elif provider == "ollama":
            return _create_ollama_llm(model, temperature)
        elif provider == "openrouter":
            return _create_openrouter_llm(model, temperature)
        elif provider == "huggingface":
            return _create_huggingface_llm(model, temperature)
        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider}. "
                f"Supported: openai, anthropic, google, groq, ollama, openrouter, huggingface"
            )
    except Exception as e:
        logger.error(f"Failed to create LLM: {e}")
        raise


def _create_openai_llm(model: str, temperature: float):
    """Create OpenAI LLM using CrewAI's LLM class."""
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set in environment")

    from crewai import LLM

    return LLM(
        model=f"openai/{model}",
        temperature=temperature,
        api_key=settings.OPENAI_API_KEY
    )


def _create_anthropic_llm(model: str, temperature: float):
    """Create Anthropic Claude LLM using CrewAI's LLM class."""
    if not settings.ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    from crewai import LLM

    return LLM(
        model=f"anthropic/{model}",
        temperature=temperature,
        api_key=settings.ANTHROPIC_API_KEY
    )


def _create_google_llm(model: str, temperature: float):
    """Create Google Gemini LLM using CrewAI's LLM class."""
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in environment")

    from crewai import LLM

    return LLM(
        model=f"gemini/{model}",
        temperature=temperature,
        api_key=settings.GOOGLE_API_KEY
    )


def _create_groq_llm(model: str, temperature: float):
    """Create Groq LLM using CrewAI's LLM class."""
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in environment")

    from crewai import LLM

    return LLM(
        model=f"groq/{model}",
        temperature=temperature,
        api_key=settings.GROQ_API_KEY
    )


def _create_ollama_llm(model: str, temperature: float):
    """Create Ollama LLM using CrewAI's LLM class."""
    from crewai import LLM

    return LLM(
        model=f"ollama/{model}",
        temperature=temperature,
        base_url=settings.OLLAMA_BASE_URL
    )


def _create_openrouter_llm(model: str, temperature: float):
    """Create OpenRouter LLM using CrewAI's LLM class.

    OpenRouter requires the 'openrouter/' prefix for LiteLLM to route correctly.
    """
    if not settings.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in environment")

    from crewai import LLM

    # LiteLLM expects 'openrouter/' prefix for OpenRouter models
    model_name = f"openrouter/{model}" if not model.startswith("openrouter/") else model

    return LLM(
        model=model_name,
        temperature=temperature,
        api_key=settings.OPENROUTER_API_KEY
    )


def _create_huggingface_llm(model: str, temperature: float):
    """Create Hugging Face LLM using CrewAI's LLM class.

    Note: CrewAI/LiteLLM may not natively support Hugging Face Inference API.
    Consider using OpenRouter or Google Gemini instead for better compatibility.
    """
    if not settings.HUGGINGFACE_API_KEY:
        raise ValueError("HUGGINGFACE_API_KEY not set in environment")

    from crewai import LLM

    # Try using huggingface/ prefix for LiteLLM
    # This may require additional LiteLLM configuration
    model_name = f"huggingface/{model}" if not model.startswith("huggingface/") else model

    return LLM(
        model=model_name,
        temperature=temperature,
        api_key=settings.HUGGINGFACE_API_KEY
    )

