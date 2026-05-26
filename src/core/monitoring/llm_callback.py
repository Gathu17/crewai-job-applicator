"""
Custom callback handler for monitoring LLM calls.
"""
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List, Optional
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class LLMMonitorCallback(BaseCallbackHandler):
    """
    Custom callback to monitor and track LLM calls.
    
    Tracks:
    - Number of calls
    - Token usage
    - Estimated costs
    - Latency
    - Errors
    """
    
    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        'gpt-4o': {'input': 2.50, 'output': 10.00},
        'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
        'gpt-4-turbo': {'input': 10.00, 'output': 30.00},
        'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50},
    }
    
    def __init__(self, model: str = 'gpt-4o-mini'):
        """
        Initialize the monitor.
        
        Args:
            model: The LLM model being used (for cost estimation)
        """
        super().__init__()
        self.model = model
        self.total_tokens = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0
        self.error_count = 0
        self.calls = []
        self.current_call_start = None
    
    def on_llm_start(
        self, 
        serialized: Dict[str, Any], 
        prompts: List[str], 
        **kwargs: Any
    ) -> None:
        """Called when LLM starts."""
        self.call_count += 1
        self.current_call_start = time.time()
        
        logger.info(f"🤖 LLM Call #{self.call_count} started")
        logger.debug(f"   Model: {self.model}")
        logger.debug(f"   Prompt preview: {prompts[0][:150]}...")
    
    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """Called when LLM ends successfully."""
        latency = time.time() - self.current_call_start if self.current_call_start else 0
        
        # Extract token usage
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        
        if hasattr(response, 'llm_output') and response.llm_output:
            token_usage = response.llm_output.get('token_usage', {})
            prompt_tokens = token_usage.get('prompt_tokens', 0)
            completion_tokens = token_usage.get('completion_tokens', 0)
            total_tokens = token_usage.get('total_tokens', 0)
        
        # Update totals
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_tokens += total_tokens
        
        # Calculate cost
        cost = self._calculate_cost(prompt_tokens, completion_tokens)
        self.total_cost += cost
        
        # Log details
        logger.info(f"✅ LLM Call #{self.call_count} completed")
        logger.info(f"   Tokens: {total_tokens:,} (prompt: {prompt_tokens:,}, completion: {completion_tokens:,})")
        logger.info(f"   Cost: ${cost:.4f}")
        logger.info(f"   Latency: {latency:.2f}s")
        logger.info(f"   📊 Running totals - Tokens: {self.total_tokens:,} | Cost: ${self.total_cost:.4f}")
        
        # Store call details
        self.calls.append({
            'call_number': self.call_count,
            'timestamp': datetime.now().isoformat(),
            'model': self.model,
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': total_tokens,
            'cost': cost,
            'latency': latency,
            'success': True
        })
    
    def on_llm_error(
        self, 
        error: Exception, 
        **kwargs: Any
    ) -> None:
        """Called when LLM errors."""
        self.error_count += 1
        latency = time.time() - self.current_call_start if self.current_call_start else 0
        
        logger.error(f"❌ LLM Call #{self.call_count} failed")
        logger.error(f"   Error: {error}")
        logger.error(f"   Latency: {latency:.2f}s")
        
        # Store error details
        self.calls.append({
            'call_number': self.call_count,
            'timestamp': datetime.now().isoformat(),
            'model': self.model,
            'error': str(error),
            'latency': latency,
            'success': False
        })
    
    def _calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost based on token usage."""
        pricing = self.PRICING.get(self.model, self.PRICING['gpt-4o-mini'])
        
        prompt_cost = (prompt_tokens / 1_000_000) * pricing['input']
        completion_cost = (completion_tokens / 1_000_000) * pricing['output']
        
        return prompt_cost + completion_cost
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get monitoring summary.
        
        Returns:
            Dictionary with monitoring statistics
        """
        return {
            'model': self.model,
            'total_calls': self.call_count,
            'successful_calls': self.call_count - self.error_count,
            'failed_calls': self.error_count,
            'total_tokens': self.total_tokens,
            'total_prompt_tokens': self.total_prompt_tokens,
            'total_completion_tokens': self.total_completion_tokens,
            'total_cost': round(self.total_cost, 4),
            'average_tokens_per_call': round(self.total_tokens / max(self.call_count, 1), 2),
            'average_cost_per_call': round(self.total_cost / max(self.call_count, 1), 4),
            'calls': self.calls
        }
    
    def print_summary(self) -> None:
        """Print a formatted summary to console."""
        summary = self.get_summary()
        
        print("\n" + "=" * 70)
        print("📊 LLM MONITORING SUMMARY")
        print("=" * 70)
        print(f"Model: {summary['model']}")
        print(f"Total Calls: {summary['total_calls']} ({summary['successful_calls']} successful, {summary['failed_calls']} failed)")
        print(f"Total Tokens: {summary['total_tokens']:,}")
        print(f"  - Prompt: {summary['total_prompt_tokens']:,}")
        print(f"  - Completion: {summary['total_completion_tokens']:,}")
        print(f"Total Cost: ${summary['total_cost']:.4f}")
        print(f"Average per Call: {summary['average_tokens_per_call']:.0f} tokens, ${summary['average_cost_per_call']:.4f}")
        print("=" * 70 + "\n")

