"""
File Upload Rate Limiter

Implements rate limiting for file uploads to prevent abuse and ensure system stability.
Addresses recommendation: Add rate limiting on file uploads in the new modal.
"""

import asyncio
import time
import logging
from typing import Dict, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
import hashlib
import os

logger = logging.getLogger(__name__)

class RateLimitType(Enum):
    """Types of rate limiting strategies"""
    PER_IP = "per_ip"
    PER_USER = "per_user"
    GLOBAL = "global"

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    max_uploads_per_minute: int = 10
    max_uploads_per_hour: int = 100
    max_file_size_mb: int = 1  # 1MB default
    max_total_size_per_hour_mb: int = 100  # 100MB total per hour
    cooldown_seconds: int = 60  # Cooldown after hitting limit

class UploadRateLimiter:
    """
    Advanced rate limiter for file uploads with multiple limiting strategies.
    
    Features:
    - Per-IP and per-user rate limiting
    - File size tracking
    - Total bandwidth limiting
    - Configurable time windows
    - Automatic cleanup of old records
    """
    
    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        
        # Track uploads per identifier (IP/user)
        self._upload_counts: Dict[str, deque] = defaultdict(deque)
        self._upload_sizes: Dict[str, deque] = defaultdict(deque)
        
        # Track global uploads
        self._global_uploads: deque = deque()
        self._global_size: deque = deque()
        
        # Track blocked identifiers and their cooldown
        self._blocked_until: Dict[str, float] = {}
        
        # Metrics for monitoring
        self.metrics = {
            'total_uploads_allowed': 0,
            'total_uploads_blocked': 0,
            'total_size_uploaded_mb': 0,
            'active_rate_limits': 0,
            'peak_uploads_per_minute': 0,
            'created_at': time.time()
        }
        
        # Background cleanup task
        self._cleanup_task = None
        self._start_cleanup_task()
    
    def _start_cleanup_task(self):
        """Start background task to cleanup old records"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_old_records())
    
    async def _cleanup_old_records(self):
        """Cleanup old upload records to prevent memory leaks"""
        while True:
            try:
                await asyncio.sleep(300)  # Cleanup every 5 minutes
                current_time = time.time()
                
                # Clean up upload counts older than 1 hour
                for identifier in list(self._upload_counts.keys()):
                    uploads = self._upload_counts[identifier]
                    while uploads and current_time - uploads[0] > 3600:  # 1 hour
                        uploads.popleft()
                    
                    # Remove empty deques
                    if not uploads:
                        del self._upload_counts[identifier]
                
                # Clean up upload sizes
                for identifier in list(self._upload_sizes.keys()):
                    sizes = self._upload_sizes[identifier]
                    while sizes and current_time - sizes[0][0] > 3600:  # 1 hour
                        sizes.popleft()
                    
                    if not sizes:
                        del self._upload_sizes[identifier]
                
                # Clean up global tracking
                while self._global_uploads and current_time - self._global_uploads[0] > 3600:
                    self._global_uploads.popleft()
                
                while self._global_size and current_time - self._global_size[0][0] > 3600:
                    self._global_size.popleft()
                
                # Clean up expired blocks
                expired_blocks = [
                    identifier for identifier, until_time in self._blocked_until.items()
                    if current_time > until_time
                ]
                for identifier in expired_blocks:
                    del self._blocked_until[identifier]
                    logger.info(f"Rate limit cooldown expired for {self._hash_identifier(identifier)}")
                
                # Update metrics
                self.metrics['active_rate_limits'] = len(self._blocked_until)
                
            except Exception as e:
                logger.error(f"Error during rate limiter cleanup: {e}")
    
    def _hash_identifier(self, identifier: str) -> str:
        """Hash identifier for privacy in logs"""
        return hashlib.sha256(identifier.encode()).hexdigest()[:8]
    
    def _get_upload_count_last_minute(self, identifier: str) -> int:
        """Get upload count in the last minute for identifier"""
        current_time = time.time()
        uploads = self._upload_counts[identifier]
        
        # Remove old entries
        while uploads and current_time - uploads[0] > 60:  # 1 minute
            uploads.popleft()
        
        return len(uploads)
    
    def _get_upload_count_last_hour(self, identifier: str) -> int:
        """Get upload count in the last hour for identifier"""
        current_time = time.time()
        uploads = self._upload_counts[identifier]
        
        # Remove old entries
        while uploads and current_time - uploads[0] > 3600:  # 1 hour
            uploads.popleft()
        
        return len(uploads)
    
    def _get_total_size_last_hour(self, identifier: str) -> float:
        """Get total upload size in MB for the last hour"""
        current_time = time.time()
        sizes = self._upload_sizes[identifier]
        
        # Remove old entries and sum remaining
        total_size = 0
        while sizes and current_time - sizes[0][0] > 3600:  # 1 hour
            sizes.popleft()
        
        for timestamp, size_mb in sizes:
            total_size += size_mb
        
        return total_size
    
    async def check_rate_limit(
        self, 
        identifier: str, 
        file_size_bytes: int,
        limit_type: RateLimitType = RateLimitType.PER_IP
    ) -> Tuple[bool, str]:
        """
        Check if upload is allowed under rate limits.
        
        Args:
            identifier: IP address, user ID, or other identifier
            file_size_bytes: Size of the file being uploaded
            limit_type: Type of rate limiting to apply
            
        Returns:
            Tuple of (is_allowed, reason_if_blocked)
        """
        current_time = time.time()
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        # Check if identifier is currently blocked
        if identifier in self._blocked_until:
            if current_time < self._blocked_until[identifier]:
                remaining = int(self._blocked_until[identifier] - current_time)
                return False, f"Rate limit cooldown active. Try again in {remaining} seconds."
            else:
                del self._blocked_until[identifier]
        
        # Check file size limit
        if file_size_mb > self.config.max_file_size_mb:
            self.metrics['total_uploads_blocked'] += 1
            return False, f"File size ({file_size_mb:.1f}MB) exceeds limit of {self.config.max_file_size_mb}MB"
        
        # Check per-identifier limits
        if limit_type in [RateLimitType.PER_IP, RateLimitType.PER_USER]:
            uploads_last_minute = self._get_upload_count_last_minute(identifier)
            uploads_last_hour = self._get_upload_count_last_hour(identifier)
            total_size_last_hour = self._get_total_size_last_hour(identifier)
            
            # Check rate limits
            if uploads_last_minute >= self.config.max_uploads_per_minute:
                self._blocked_until[identifier] = current_time + self.config.cooldown_seconds
                self.metrics['total_uploads_blocked'] += 1
                logger.warning(f"Rate limit exceeded for {self._hash_identifier(identifier)}: {uploads_last_minute} uploads/minute")
                return False, f"Too many uploads. Limit: {self.config.max_uploads_per_minute} per minute."
            
            if uploads_last_hour >= self.config.max_uploads_per_hour:
                self._blocked_until[identifier] = current_time + self.config.cooldown_seconds
                self.metrics['total_uploads_blocked'] += 1
                logger.warning(f"Hourly rate limit exceeded for {self._hash_identifier(identifier)}: {uploads_last_hour} uploads/hour")
                return False, f"Too many uploads. Limit: {self.config.max_uploads_per_hour} per hour."
            
            if total_size_last_hour + file_size_mb > self.config.max_total_size_per_hour_mb:
                self._blocked_until[identifier] = current_time + self.config.cooldown_seconds
                self.metrics['total_uploads_blocked'] += 1
                logger.warning(f"Size limit exceeded for {self._hash_identifier(identifier)}: {total_size_last_hour + file_size_mb:.1f}MB/hour")
                return False, f"Upload size limit exceeded. Limit: {self.config.max_total_size_per_hour_mb}MB per hour."
        
        # All checks passed - record the upload
        self._upload_counts[identifier].append(current_time)
        self._upload_sizes[identifier].append((current_time, file_size_mb))
        self._global_uploads.append(current_time)
        self._global_size.append((current_time, file_size_mb))
        
        # Update metrics
        self.metrics['total_uploads_allowed'] += 1
        self.metrics['total_size_uploaded_mb'] += file_size_mb
        
        # Update peak uploads per minute
        current_uploads_per_minute = len([
            t for t in self._global_uploads 
            if current_time - t <= 60
        ])
        if current_uploads_per_minute > self.metrics['peak_uploads_per_minute']:
            self.metrics['peak_uploads_per_minute'] = current_uploads_per_minute
        
        logger.info(f"Upload allowed for {self._hash_identifier(identifier)}: {file_size_mb:.1f}MB")
        return True, "Upload allowed"
    
    def get_rate_limit_status(self, identifier: str) -> Dict:
        """Get current rate limit status for an identifier"""
        current_time = time.time()
        
        uploads_last_minute = self._get_upload_count_last_minute(identifier)
        uploads_last_hour = self._get_upload_count_last_hour(identifier)
        total_size_last_hour = self._get_total_size_last_hour(identifier)
        
        is_blocked = identifier in self._blocked_until and current_time < self._blocked_until[identifier]
        cooldown_remaining = 0
        if is_blocked:
            cooldown_remaining = int(self._blocked_until[identifier] - current_time)
        
        return {
            'identifier_hash': self._hash_identifier(identifier),
            'uploads_last_minute': uploads_last_minute,
            'uploads_last_hour': uploads_last_hour,
            'total_size_last_hour_mb': round(total_size_last_hour, 2),
            'is_blocked': is_blocked,
            'cooldown_remaining_seconds': cooldown_remaining,
            'limits': {
                'max_uploads_per_minute': self.config.max_uploads_per_minute,
                'max_uploads_per_hour': self.config.max_uploads_per_hour,
                'max_file_size_mb': self.config.max_file_size_mb,
                'max_total_size_per_hour_mb': self.config.max_total_size_per_hour_mb
            }
        }
    
    def get_global_metrics(self) -> Dict:
        """Get global rate limiter metrics"""
        current_time = time.time()
        uptime = current_time - self.metrics['created_at']
        
        # Calculate current global rates
        uploads_last_minute = len([
            t for t in self._global_uploads 
            if current_time - t <= 60
        ])
        
        uploads_last_hour = len([
            t for t in self._global_uploads 
            if current_time - t <= 3600
        ])
        
        return {
            **self.metrics,
            'uptime_seconds': round(uptime, 2),
            'current_uploads_per_minute': uploads_last_minute,
            'current_uploads_per_hour': uploads_last_hour,
            'active_identifiers': len(self._upload_counts),
            'blocked_identifiers': len(self._blocked_until),
        }
    
    async def cleanup(self):
        """Cleanup resources"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Upload rate limiter cleanup completed")

# Global instance
_upload_rate_limiter = None

def get_upload_rate_limiter(config: Optional[RateLimitConfig] = None) -> UploadRateLimiter:
    """Get singleton upload rate limiter instance"""
    global _upload_rate_limiter
    if _upload_rate_limiter is None:
        _upload_rate_limiter = UploadRateLimiter(config)
    return _upload_rate_limiter