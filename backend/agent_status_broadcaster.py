"""
Agent Status Broadcasting system for real-time progress updates.
This version is refactored to be stateless and use the StateService.
"""

import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

from backend.simple_connection_manager import SimpleConnectionManager
from backend.state_service import get_state_service

logger = logging.getLogger(__name__)

class AgentStatusBroadcaster:
    """
    Broadcasts agent status updates to connected WebSocket clients.
    This class is now stateless and uses the StateService to manage agent states.
    """
    
    def __init__(self, connection_manager: SimpleConnectionManager):
        """
        Initialize the status broadcaster.
        
        Args:
            connection_manager: WebSocket connection manager instance
        """
        self.connection_manager = connection_manager
        self.state_service = get_state_service()
        logger.info("Stateless Agent Status Broadcaster initialized.")

    async def broadcast_agent_status(
        self, 
        agent_name: str, 
        status: str, 
        task: Optional[str] = None,
        session_id: str = "global_session",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Broadcast agent status update and update state via StateService."""
        self.state_service.update_agent_status(agent_name, status, task)
        
        status_message = {
            "type": "agent_status",
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "status": status,
            "task": task,
            "session_id": session_id,
            "metadata": metadata or {}
        }
        
        logger.info(f"Broadcasting status update for {agent_name}: {status}")
        await self.connection_manager.broadcast(json.dumps(status_message))

    async def broadcast_agent_error(
        self,
        agent_name: str,
        error_message: str,
        session_id: str = "global_session",
        error_details: Optional[Dict[str, Any]] = None
    ):
        """Broadcast agent error status and update state via StateService."""
        self.state_service.update_agent_status(agent_name, "error", error_message)

        error_message_data = {
            "type": "agent_error",
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "error_message": error_message,
            "error_details": error_details or {},
            "session_id": session_id
        }
        
        logger.error(f"Broadcasting error for {agent_name}: {error_message}")
        await self.connection_manager.broadcast(json.dumps(error_message_data))

    async def broadcast_agent_response(
        self,
        agent_name: str,
        content: str,
        session_id: str = "global_session",
    ):
        """Broadcasts a message from an agent to the main chat window."""
        message = {
            "type": "agent_response",
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "content": content,
            "session_id": session_id
        }
        logger.info(f"[DEBUG] Broadcasting agent response: {message}")
        await self.connection_manager.broadcast(json.dumps(message))
        logger.info(f"Broadcasted agent response from {agent_name}")

    async def broadcast_agent_completed(
        self,
        agent_name: str,
        session_id: str = "global_session",
        final_output: Optional[str] = None
    ):
        """Broadcasts agent completion status and updates state via StateService."""
        self.state_service.update_agent_status(agent_name, "completed", final_output or "Task completed")

        completion_message = {
            "type": "agent_status",
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "status": "completed",
            "task": final_output or "Task completed",
            "session_id": session_id
        }

        logger.info(f"Broadcasting completion status for {agent_name}")
        await self.connection_manager.broadcast(json.dumps(completion_message))
