import asyncio
import time
from collections import deque
from typing import Dict, Deque, Tuple

class OpenAIRateLimiter:
    """
    A class to handle rate limiting for OpenAI API calls based on requests
    per minute (RPM) and tokens per minute (TPM).
    """
    def __init__(self, requests_per_minute: int = 20, tokens_per_minute: int = 40000):
        """
        Initializes the rate limiter.

        Args:
            requests_per_minute: The maximum number of requests allowed per minute.
            tokens_per_minute: The maximum number of tokens allowed per minute.
        """
        self.requests_per_minute = requests_per_minute
        self.tokens_per_minute = tokens_per_minute

        # Using deques for efficient sliding window implementation
        self.request_timestamps: Deque[float] = deque()
        self.token_usage: Deque[Tuple[float, int]] = deque()

    def _cleanup_old_entries(self, current_time: float):
        """Removes entries older than 60 seconds from the deques."""
        # Cleanup request timestamps
        while self.request_timestamps and self.request_timestamps[0] <= current_time - 60:
            self.request_timestamps.popleft()

        # Cleanup token usage
        while self.token_usage and self.token_usage[0][0] <= current_time - 60:
            self.token_usage.popleft()

    async def wait_if_needed(self, estimated_tokens: int = 1000):
        """
        Asynchronously waits if the next request might exceed rate limits.

        Args:
            estimated_tokens: An estimate of tokens for the upcoming request.
        """
        while True:
            current_time = time.time()
            self._cleanup_old_entries(current_time)

            # Check requests per minute
            if len(self.request_timestamps) >= self.requests_per_minute:
                wait_time = self.request_timestamps[0] - (current_time - 60)
                await asyncio.sleep(wait_time)
                continue # Re-evaluate after waiting

            # Check tokens per minute
            current_tokens = sum(tokens for _, tokens in self.token_usage)
            if current_tokens + estimated_tokens > self.tokens_per_minute:
                # This is a simplification. A more complex implementation would
                # wait until the oldest token usage entry expires.
                wait_time = self.token_usage[0][0] - (current_time - 60)
                await asyncio.sleep(wait_time)
                continue # Re-evaluate after waiting

            # If both checks pass, we can proceed
            break

    def record_request(self, tokens_used: int):
        """
        Records a successful request and its token usage.

        Args:
            tokens_used: The number of tokens consumed by the request.
        """
        current_time = time.time()
        self.request_timestamps.append(current_time)
        self.token_usage.append((current_time, tokens_used))
        self._cleanup_old_entries(current_time)

    def get_rate_limit_status(self) -> dict:
        """
        Returns a dictionary with the current rate limit status.
        """
        current_time = time.time()
        self._cleanup_old_entries(current_time)

        return {
            "current_rpm": len(self.request_timestamps),
            "max_rpm": self.requests_per_minute,
            "current_tpm": sum(tokens for _, tokens in self.token_usage),
            "max_tpm": self.tokens_per_minute,
        }
