"""
API endpoints for monitoring LLM usage and performance.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


class TokenUsage(BaseModel):
    """Token usage statistics."""
    total_calls: int
    successful_calls: int
    failed_calls: int
    total_tokens: int
    total_prompt_tokens: int
    total_completion_tokens: int
    total_cost: float
    average_tokens_per_call: float
    average_cost_per_call: float


class LLMCallDetail(BaseModel):
    """Details of a single LLM call."""
    call_number: int
    timestamp: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    latency: float = 0.0
    success: bool = True
    error: str = None


class MonitoringSummary(BaseModel):
    """Complete monitoring summary."""
    model: str
    total_calls: int
    successful_calls: int
    failed_calls: int
    total_tokens: int
    total_prompt_tokens: int
    total_completion_tokens: int
    total_cost: float
    average_tokens_per_call: float
    average_cost_per_call: float
    calls: List[LLMCallDetail]


# Global monitor instance (will be set by main.py)
_monitor = None


def set_monitor(monitor):
    """Set the global monitor instance."""
    global _monitor
    _monitor = monitor


@router.get("/usage", response_model=TokenUsage)
async def get_token_usage():
    """
    Get current token usage statistics.
    
    Returns:
        Token usage summary including costs and call counts
    """
    if not _monitor:
        raise HTTPException(
            status_code=503,
            detail="Monitoring not enabled. Set up LLMMonitorCallback in main.py"
        )
    
    summary = _monitor.get_summary()
    
    return TokenUsage(
        total_calls=summary['total_calls'],
        successful_calls=summary['successful_calls'],
        failed_calls=summary['failed_calls'],
        total_tokens=summary['total_tokens'],
        total_prompt_tokens=summary['total_prompt_tokens'],
        total_completion_tokens=summary['total_completion_tokens'],
        total_cost=summary['total_cost'],
        average_tokens_per_call=summary['average_tokens_per_call'],
        average_cost_per_call=summary['average_cost_per_call']
    )


@router.get("/summary", response_model=MonitoringSummary)
async def get_monitoring_summary():
    """
    Get complete monitoring summary including all call details.
    
    Returns:
        Full monitoring summary with individual call information
    """
    if not _monitor:
        raise HTTPException(
            status_code=503,
            detail="Monitoring not enabled. Set up LLMMonitorCallback in main.py"
        )
    
    return _monitor.get_summary()


@router.get("/calls", response_model=List[LLMCallDetail])
async def get_llm_calls(
    limit: int = 100,
    successful_only: bool = False
):
    """
    Get list of LLM calls.
    
    Args:
        limit: Maximum number of calls to return (default: 100)
        successful_only: Only return successful calls (default: False)
    
    Returns:
        List of LLM call details
    """
    if not _monitor:
        raise HTTPException(
            status_code=503,
            detail="Monitoring not enabled. Set up LLMMonitorCallback in main.py"
        )
    
    summary = _monitor.get_summary()
    calls = summary['calls']
    
    if successful_only:
        calls = [c for c in calls if c.get('success', True)]
    
    return calls[-limit:]


@router.post("/reset")
async def reset_monitoring():
    """
    Reset monitoring statistics.
    
    Returns:
        Confirmation message
    """
    if not _monitor:
        raise HTTPException(
            status_code=503,
            detail="Monitoring not enabled. Set up LLMMonitorCallback in main.py"
        )
    
    # Reset counters
    _monitor.total_tokens = 0
    _monitor.total_prompt_tokens = 0
    _monitor.total_completion_tokens = 0
    _monitor.total_cost = 0.0
    _monitor.call_count = 0
    _monitor.error_count = 0
    _monitor.calls = []
    
    return {
        "message": "Monitoring statistics reset successfully",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/health")
async def monitoring_health():
    """
    Check if monitoring is enabled and working.
    
    Returns:
        Health status
    """
    return {
        "monitoring_enabled": _monitor is not None,
        "model": _monitor.model if _monitor else None,
        "timestamp": datetime.now().isoformat()
    }

