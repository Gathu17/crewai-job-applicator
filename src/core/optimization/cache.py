"""
Result caching to avoid redundant LLM calls.
"""
import hashlib
import json
import logging
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
from functools import wraps

logger = logging.getLogger(__name__)


class ResultCache:
    """
    Simple in-memory cache for LLM results.
    
    Caches results based on input hash to avoid redundant API calls.
    """
    
    def __init__(self, ttl_minutes: int = 60):
        """
        Initialize cache.
        
        Args:
            ttl_minutes: Time-to-live for cache entries in minutes
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = timedelta(minutes=ttl_minutes)
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        # Combine all arguments into a string
        key_data = json.dumps({
            'args': args,
            'kwargs': kwargs
        }, sort_keys=True, default=str)
        
        # Hash it
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        # Check if expired
        if datetime.now() - entry['timestamp'] > self.ttl:
            logger.debug(f"Cache entry expired: {key}")
            del self.cache[key]
            self.misses += 1
            return None
        
        self.hits += 1
        logger.info(f"✅ Cache hit! (hits: {self.hits}, misses: {self.misses}, hit rate: {self.hit_rate:.1%})")
        return entry['value']
    
    def set(self, key: str, value: Any) -> None:
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = {
            'value': value,
            'timestamp': datetime.now()
        }
        logger.debug(f"Cached result: {key}")
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Cache cleared")
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    @property
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': round(self.hit_rate, 3),
            'ttl_minutes': self.ttl.total_seconds() / 60
        }


def cached_result(cache: ResultCache):
    """
    Decorator to cache function results.
    
    Usage:
        cache = ResultCache(ttl_minutes=60)
        
        @cached_result(cache)
        def expensive_function(arg1, arg2):
            # ... expensive operation
            return result
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache._generate_key(*args, **kwargs)
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function
            logger.debug(f"Cache miss, calling {func.__name__}")
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator


# Global cache instance
_global_cache = ResultCache(ttl_minutes=60)


def get_global_cache() -> ResultCache:
    """Get the global cache instance."""
    return _global_cache

