"""
Configuration utilities and helpers.
"""
import os
from typing import Any, Optional
from pathlib import Path


def get_env(key: str, default: Any = None, required: bool = False) -> Any:
    """
    Get environment variable with optional default and required check.
    
    Args:
        key: Environment variable key
        default: Default value if not found
        required: Raise error if not found and no default
    
    Returns:
        Environment variable value or default
    """
    value = os.getenv(key, default)
    
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' not set")
    
    return value


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def ensure_dir(path: str) -> Path:
    """Ensure directory exists, create if it doesn't."""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def load_env_file(env_file: str = ".env"):
    """Load environment variables from .env file."""
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        print("python-dotenv not installed. Install with: pip install python-dotenv")



