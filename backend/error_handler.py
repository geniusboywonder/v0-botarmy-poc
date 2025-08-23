"""
Enhanced error handling system with status broadcasting integration.
Provides centralized error management and real-time error notifications.
"""

import logging
import traceback
import asyncio
from typing import Optional, Dict, Any, Callable
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories for better classification."""
    NETWORK = "network"
    LLM_API = "llm_api"
    RATE_LIMIT = "rate_limit"
    AGENT = "agent"
    WORKFLOW = "workflow"
    WEBSOCKET = "websocket"
    VALIDATION = "validation"
    SYSTEM = "system"

# Custom Exception Classes
class AgentException(Exception):
    """Base class for agent-related exceptions."""
    pass

class APIRateLimitError(AgentException):
    """Raised when an API rate limit is exceeded."""
    pass

class NetworkError(AgentException):
    """Raised for network-related issues during an API call."""
    pass

class ValidationError(AgentException):
    """Raised when the input to an agent is invalid."""
    pass

class AgentExecutionError(AgentException):
    """Raised for general errors during agent execution."""
    pass

class ErrorHandler:
    """
    Enhanced error handler with status broadcasting and recovery strategies.
    """
    
    # Class variable to hold the status broadcaster
    _status_broadcaster = None

    def __init__(self):
        self.error_history: list = []
        self.recovery_strategies: Dict[ErrorCategory, Callable] = {}
        self.error_count_by_category: Dict[ErrorCategory, int] = {cat: 0 for cat in ErrorCategory}
        logger.info("Enhanced Error Handler initialized")

    @classmethod
    def set_status_broadcaster(cls, status_broadcaster):
        """Set the status broadcaster for the class."""
        cls._status_broadcaster = status_broadcaster
        logger.info("Status broadcaster set in Error Handler")

    async def handle_error(
        self,
        error: Exception,
        context: str,
        agent_name: Optional[str] = None,
        session_id: str = "global_session",
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle an error with comprehensive logging and broadcasting.

        Args:
            error: The exception that occurred
            context: Context where the error occurred
            agent_name: Name of the agent if applicable
            session_id: Session identifier
            severity: Error severity level
            category: Error category
            metadata: Additional error metadata

        Returns:
            Error handling result with recovery suggestions
        """

        error_details = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "agent_name": agent_name,
            "session_id": session_id,
            "severity": severity.value,
            "category": category.value,
            "timestamp": datetime.now().isoformat(),
            "traceback": traceback.format_exc(),
            "metadata": metadata or {}
        }

        # Update error statistics
        self.error_count_by_category[category] += 1

        # Add to error history (keep last 100 errors)
        self.error_history.append(error_details)
        if len(self.error_history) > 100:
            self.error_history.pop(0)

        # Log the error based on severity
        log_message = f"[{category.value.upper()}] {context}: {str(error)}"
        if agent_name:
            log_message = f"[{agent_name}] {log_message}"

        if severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message, exc_info=True)
        elif severity == ErrorSeverity.HIGH:
            logger.error(log_message, exc_info=True)
        elif severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        # Broadcast error if agent-related and status broadcaster is available
        if agent_name and self._status_broadcaster:
            try:
                await self._status_broadcaster.broadcast_agent_status(
                    agent_name=agent_name,
                    status="error",
                    error_message=f"[{category.value}] {str(error)}",
                    session_id=session_id,
                    current_task=context,
                    metadata={
                        "severity": severity.value,
                        "category": category.value,
                        "context": context,
                        **(metadata or {})
                    }
                )
            except Exception as broadcast_error:
                logger.error(f"Failed to broadcast error: {broadcast_error}")

        return {
            "error_id": len(self.error_history),
            "handled": True,
            "suggested_actions": self._get_suggested_actions(category, severity),
            "error_details": error_details
        }

    def _get_suggested_actions(self, category: ErrorCategory, severity: ErrorSeverity) -> list:
        """Get suggested actions based on error category and severity."""
        suggestions = []

        if category == ErrorCategory.RATE_LIMIT:
            suggestions.extend([
                "Wait before retrying the request",
                "Consider using a different LLM provider",
                "Reduce request frequency"
            ])
        elif category == ErrorCategory.LLM_API:
            suggestions.extend([
                "Check API key validity",
                "Verify network connectivity",
                "Try with a different model or provider"
            ])
        elif category == ErrorCategory.AGENT:
            suggestions.extend([
                "Review agent configuration",
                "Check input parameters",
                "Consider simpler task breakdown"
            ])

        if severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            suggestions.append("Consider stopping current operations")
            suggestions.append("Review system logs for related issues")

        return suggestions

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics and recent error history."""
        return {
            "total_errors": len(self.error_history),
            "errors_by_category": {cat.value: count for cat, count in self.error_count_by_category.items()},
            "recent_errors": self.error_history[-10:],  # Last 10 errors
        }

# Global error handler instance
error_handler = ErrorHandler()

# Convenience functions for common error scenarios
async def handle_llm_error(error: Exception, agent_name: str, context: str = "LLM API call", session_id: str = "global_session"):
    """Convenience function for handling LLM-related errors."""
    return await error_handler.handle_error(
        error=error,
        context=context,
        agent_name=agent_name,
        session_id=session_id,
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.LLM_API
    )

async def handle_agent_error(error: Exception, agent_name: str, task: str, session_id: str = "global_session"):
    """Convenience function for handling agent execution errors."""
    return await error_handler.handle_error(
        error=error,
        context=f"Agent task execution: {task}",
        agent_name=agent_name,
        session_id=session_id,
        severity=ErrorSeverity.MEDIUM,
        category=ErrorCategory.AGENT,
        metadata={"task": task}
    )