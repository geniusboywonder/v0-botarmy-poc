"""
Agent Status Broadcasting system for real-time progress updates.
Integrates with the WebSocket system to broadcast a unified agent status.
"""

import asyncio
import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentStatusBroadcaster:
    """
    Broadcasts unified agent status updates to connected WebSocket clients.
    """

    def __init__(self, connection_manager=None):
        """
        Initialize the status broadcaster.

        Args:
            connection_manager: WebSocket connection manager instance
        """
        self.connection_manager = connection_manager
        self.agent_states: Dict[str, Dict[str, Any]] = {}
        logger.info("Agent Status Broadcaster initialized")

    def set_connection_manager(self, connection_manager):
        """Set or update the connection manager."""
        self.connection_manager = connection_manager
        logger.info("Connection manager updated in status broadcaster")

    async def broadcast_agent_status(
        self,
        agent_name: str,
        status: str,
        current_task: Optional[str] = None,
        progress_percentage: Optional[float] = None,
        estimated_completion: Optional[str] = None,
        error_message: Optional[str] = None,
        session_id: str = "global_session",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Broadcast a unified agent status update.

        Args:
            agent_name: Name of the agent
            status: Current status (e.g., 'starting', 'working', 'completed', 'error', 'idle')
            current_task: Description of the current task.
            progress_percentage: Task completion percentage (0-100).
            estimated_completion: Estimated time to completion (e.g., "2 minutes").
            error_message: A description of the error if status is 'error'.
            session_id: Session identifier.
            metadata: Additional status metadata.
        """

        # Update internal state
        self.agent_states[agent_name] = {
            "name": agent_name,
            "status": status,
            "current_task": current_task,
            "progress_percentage": progress_percentage,
            "estimated_completion": estimated_completion,
            "error_message": error_message,
            "last_update": datetime.now().isoformat(),
            "session_id": session_id,
            "metadata": metadata or {}
        }

        # Create status message payload
        data_payload = {
            "agent_name": agent_name,
            "status": status,
            "current_task": current_task,
            "progress_percentage": progress_percentage,
            "estimated_completion": estimated_completion,
            "error_message": error_message,
            "session_id": session_id,
            "metadata": metadata or {}
        }

        # Create the full WebSocket message
        status_message = {
            "type": "agent_status",
            "timestamp": datetime.now().isoformat(),
            "data": data_payload
        }

        log_message = f"Broadcasting status for {agent_name}: {status}"
        if current_task:
            log_message += f" - Task: {current_task}"
        if progress_percentage is not None:
            log_message += f" - Progress: {progress_percentage}%"
        if error_message:
            log_message += f" - Error: {error_message}"

        logger.info(log_message)

        # Broadcast to all connected clients
        if self.connection_manager:
            await self.connection_manager.broadcast_to_all(json.dumps(status_message))
        else:
            logger.warning("No connection manager available for broadcasting")

    async def broadcast_workflow_progress(
        self,
        progress_percentage: float,
        current_step: str,
        steps: list,
        session_id: str = "global_session"
    ):
        """
        Broadcast the overall workflow progress.

        Args:
            progress_percentage: Overall progress percentage (0-100).
            current_step: The name of the currently active step.
            steps: A list of all steps with their statuses.
            session_id: Session identifier.
        """

        progress_message = {
            "type": "workflow_progress",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "progress_percentage": progress_percentage,
                "current_step": current_step,
                "steps": steps,
                "session_id": session_id,
            }
        }

        logger.info(f"Broadcasting workflow progress: {progress_percentage}% - Current step: {current_step}")

        if self.connection_manager:
            await self.connection_manager.broadcast_to_all(json.dumps(progress_message))
        else:
            logger.warning("No connection manager available for broadcasting")

    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get current status for a specific agent."""
        return self.agent_states.get(agent_name)

    def get_all_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get current status for all agents."""
        return self.agent_states.copy()