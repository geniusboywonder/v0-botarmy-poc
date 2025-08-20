import logging
from typing import Dict

# Assuming agui_handler is a singleton or accessible this way
from backend.agui.protocol import agui_handler
from backend.main import status_broadcaster

logger = logging.getLogger(__name__)

class ErrorHandler:
    """
    A centralized handler for converting technical exceptions into user-friendly
    and machine-readable messages for the AG-UI protocol.
    """

    _error_map = {
        "APIKeyNotFound": "AI service configuration needed. Please check your setup.",
        "RateLimitError": "AI service is busy. Retrying in a moment...",
        "ConnectionTimeout": "Connection to a service has been lost. Reconnecting automatically...",
        "WebSocketDisconnect": "Real-time connection lost. Attempting to reconnect...",
        "WorkflowFailed": "The project task failed unexpectedly. Our team is looking into it.",
        "Default": "An unexpected error occurred. We are working to resolve it."
    }

    @staticmethod
    def _create_user_friendly_message(error_type: str, details: str) -> str:
        """Maps a technical error type to a user-friendly message."""
        return ErrorHandler._error_map.get(error_type, ErrorHandler._error_map["Default"])

    @staticmethod
    async def handle_llm_error(error: Exception, agent_name: str, session_id: str) -> Dict:
        """
        Converts OpenAI and other LLM-related errors into user-friendly messages.
        """
        logger.error(f"[ErrorHandler] Handling LLM error for agent {agent_name}: {error}", exc_info=True)

        error_type = "Default"
        # This requires knowledge of the specific exceptions the llm_service can raise.
        # We'll use string matching for this example, but checking `isinstance` is better.
        error_str = str(error).lower()
        if "api key" in error_str:
            error_type = "APIKeyNotFound"
        elif "rate limit" in error_str:
            error_type = "RateLimitError"
        elif "timeout" in error_str:
            error_type = "ConnectionTimeout"

        user_message = ErrorHandler._create_user_friendly_message(error_type, str(error))

        # Broadcast the error status
        await status_broadcaster.broadcast_agent_error(agent_name, user_message, session_id)

        return agui_handler.create_error_message(
            error=user_message,
            agent_name=agent_name,
            session_id=session_id,
            details=str(error) # Include technical details for debugging
        )

    @staticmethod
    def handle_websocket_error(error: Exception, client_id: str) -> Dict:
        """
        Converts WebSocket errors into user-friendly messages.
        Note: The message may not be deliverable if the socket is already closed.
        """
        logger.error(f"[ErrorHandler] Handling WebSocket error for client {client_id}: {error}", exc_info=True)

        error_type = "WebSocketDisconnect"
        user_message = ErrorHandler._create_user_friendly_message(error_type, str(error))

        # This message is intended more for logging or potential reconnection logic
        # as it's unlikely to be successfully sent to the disconnected client.
        return agui_handler.create_error_message(
            error=user_message,
            session_id=client_id, # Assuming client_id can stand in for session_id here
            details=str(error)
        )


    @staticmethod
    async def handle_workflow_error(error: Exception, session_id: str) -> Dict:
        """
        Converts ControlFlow/Prefect workflow errors into user-friendly messages.
        """
        logger.error(f"[ErrorHandler] Handling workflow error for session {session_id}: {error}", exc_info=True)

        error_type = "WorkflowFailed"
        # We could add more specific checks here if we knew more about workflow exceptions
        user_message = ErrorHandler._create_user_friendly_message(error_type, str(error))

        # Broadcast the error status
        # We don't have a specific agent name here, so we use "System"
        await status_broadcaster.broadcast_agent_error("System", user_message, session_id)

        return agui_handler.create_error_message(
            error=user_message,
            session_id=session_id,
            details=str(error)
        )
