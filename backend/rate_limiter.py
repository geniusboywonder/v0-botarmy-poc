"""
Rate limiter for LLM API calls to prevent hitting quotas and manage costs.
Supports multiple providers with different limits.
"""

import asyncio
import time
import logging
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    tokens_per_minute: int = 90000
    tokens_per_hour: int = 200000
    burst_limit: int = 10  # Allow bursts up to this many requests

@dataclass
class RequestRecord:
    """Record of a single API request"""
    timestamp: float
    tokens: int = 0
    
class TokenBucket:
    """Token bucket algorithm for rate limiting"""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens. Returns True if successful."""
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        """Refill tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

class RateLimiter:
    """
    Advanced rate limiter for LLM APIs with provider-specific limits.
    Tracks requests per minute/hour and token usage.
    """
    
    def __init__(self):
        self.configs: Dict[str, RateLimitConfig] = {
            'openai': RateLimitConfig(
                requests_per_minute=60,
                requests_per_hour=1000, 
                tokens_per_minute=90000,
                tokens_per_hour=200000,
                burst_limit=10
            ),
            'anthropic': RateLimitConfig(
                requests_per_minute=50,
                requests_per_hour=1000,
                tokens_per_minute=100000,
                tokens_per_hour=300000,
                burst_limit=8
            ),
            'google': RateLimitConfig(
                requests_per_minute=100,
                requests_per_hour=2000,
                tokens_per_minute=120000,
                tokens_per_hour=500000,
                burst_limit=15
            )
        }
        
        # Request tracking
        self.request_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.token_buckets: Dict[str, TokenBucket] = {}
        
        # Initialize token buckets
        for provider, config in self.configs.items():
            self.token_buckets[provider] = TokenBucket(
                capacity=config.burst_limit,
                refill_rate=config.requests_per_minute / 60.0
            )
    
    def add_provider_config(self, provider: str, config: RateLimitConfig):
        """Add or update rate limit configuration for a provider"""
        self.configs[provider] = config
        self.token_buckets[provider] = TokenBucket(
            capacity=config.burst_limit,
            refill_rate=config.requests_per_minute / 60.0
        )
        logger.info(f"Updated rate limit config for {provider}")
    
    async def acquire(self, provider: str, estimated_tokens: int = 1000) -> bool:
        """
        Try to acquire permission to make a request.
        Returns True if request is allowed, False if rate limited.
        """
        if provider not in self.configs:
            logger.warning(f"No rate limit config for provider {provider}, allowing request")
            return True
        
        config = self.configs[provider]
        now = time.time()
        
        # Check token bucket (burst protection)
        if not self.token_buckets[provider].consume(1):
            logger.warning(f"Rate limited by burst protection for {provider}")
            return False
        
        # Check request rate limits
        history = self.request_history[provider]
        
        # Remove old requests (older than 1 hour)
        while history and now - history[0].timestamp > 3600:
            history.popleft()
        
        # Count requests in the last minute and hour
        recent_requests = sum(1 for req in history if now - req.timestamp <= 60)
        hourly_requests = len(history)
        
        # Count tokens in the last minute and hour
        recent_tokens = sum(req.tokens for req in history if now - req.timestamp <= 60)
        hourly_tokens = sum(req.tokens for req in history)
        
        # Check limits
        if recent_requests >= config.requests_per_minute:
            logger.warning(f"Rate limited: {recent_requests} requests in last minute for {provider}")
            return False
        
        if hourly_requests >= config.requests_per_hour:
            logger.warning(f"Rate limited: {hourly_requests} requests in last hour for {provider}")
            return False
        
        if recent_tokens + estimated_tokens > config.tokens_per_minute:
            logger.warning(f"Rate limited: {recent_tokens + estimated_tokens} tokens would exceed minute limit for {provider}")
            return False
        
        if hourly_tokens + estimated_tokens > config.tokens_per_hour:
            logger.warning(f"Rate limited: {hourly_tokens + estimated_tokens} tokens would exceed hour limit for {provider}")
            return False
        
        # Record the request
        history.append(RequestRecord(timestamp=now, tokens=estimated_tokens))
        
        logger.debug(f"Rate limit check passed for {provider}: {recent_requests}/min, {hourly_requests}/hour, {recent_tokens} tokens/min")
        return True
    
    async def wait_if_needed(self, provider: str, estimated_tokens: int = 1000, max_wait: float = 60.0) -> bool:
        """
        Wait until a request can be made, up to max_wait seconds.
        Returns True if permission acquired, False if timed out.
        """
        start_time = time.time()
        wait_time = 1.0  # Start with 1 second wait
        
        while time.time() - start_time < max_wait:
            if await self.acquire(provider, estimated_tokens):
                return True
            
            logger.info(f"Rate limited for {provider}, waiting {wait_time:.1f}s...")
            await asyncio.sleep(wait_time)
            
            # Exponential backoff, but cap at 10 seconds
            wait_time = min(wait_time * 1.5, 10.0)
        
        logger.error(f"Rate limit timeout for {provider} after {max_wait}s")
        return False
    
    def update_actual_usage(self, provider: str, actual_tokens: int):
        """Update the last request record with actual token usage"""
        if provider in self.request_history and self.request_history[provider]:
            # Update the most recent request
            last_request = self.request_history[provider][-1]
            last_request.tokens = actual_tokens
            logger.debug(f"Updated actual token usage for {provider}: {actual_tokens}")
    
    def get_status(self, provider: str) -> Dict[str, Any]:
        """Get current rate limit status for a provider"""
        if provider not in self.configs:
            return {"error": f"No config for provider {provider}"}
        
        config = self.configs[provider]
        history = self.request_history[provider]
        now = time.time()
        
        recent_requests = sum(1 for req in history if now - req.timestamp <= 60)
        hourly_requests = len(history)
        recent_tokens = sum(req.tokens for req in history if now - req.timestamp <= 60)
        hourly_tokens = sum(req.tokens for req in history)
        
        return {
            "provider": provider,
            "requests_per_minute": f"{recent_requests}/{config.requests_per_minute}",
            "requests_per_hour": f"{hourly_requests}/{config.requests_per_hour}",
            "tokens_per_minute": f"{recent_tokens}/{config.tokens_per_minute}",
            "tokens_per_hour": f"{hourly_tokens}/{config.tokens_per_hour}",
            "burst_tokens_available": self.token_buckets[provider].tokens,
            "next_refill_in": 60 - (now % 60)  # Rough estimate
        }
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get rate limit status for all providers"""
        return {provider: self.get_status(provider) for provider in self.configs.keys()}

# Global rate limiter instance
rate_limiter = RateLimiter()

# Decorator for automatic rate limiting
def rate_limited(provider: str, estimated_tokens: int = 1000):
    """Decorator to automatically rate limit function calls"""
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            if not await rate_limiter.wait_if_needed(provider, estimated_tokens):
                raise Exception(f"Rate limit exceeded for {provider}")
            
            try:
                result = await func(*args, **kwargs)
                # If the function returns token usage info, update it
                if isinstance(result, dict) and 'usage' in result:
                    actual_tokens = result['usage'].get('total_tokens', estimated_tokens)
                    rate_limiter.update_actual_usage(provider, actual_tokens)
                return result
            except Exception as e:
                logger.error(f"Error in rate limited function: {e}")
                raise
        
        return wrapper
    return decorator