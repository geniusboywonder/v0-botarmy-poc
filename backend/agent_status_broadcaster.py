"""
Agent Status Broadcasting system for real-time progress updates.
Integrates with the WebSocket system to broadcast agent status changes.
"""

import asyncio
import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentStatusBroadcaster:
    """
    Broadcasts agent status updates to connected WebSocket clients.
    Provides real-time progress tracking and agent state management.
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
        Broadcast a comprehensive agent status update.

        Args:
            agent_name: Name of the agent
            status: Current status (e.g., "working", "completed", "error", "idle")
            current_task: Description of the current task
            progress_percentage: Task completion percentage (0-100)
            estimated_completion: Estimated time to completion (e.g., "2 minutes")
            error_message: Error message if status is "error"
            session_id: Session identifier
            metadata: Additional status metadata
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

        # Create status message
        status_message = {
            "type": "agent_status",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "agent_name": agent_name,
                "status": status,
                "current_task": current_task,
                "progress_percentage": progress_percentage,
                "estimated_completion": estimated_completion,
                "error_message": error_message,
                "session_id": session_id,
                "metadata": metadata or {}
            }
        }

        logger.info(f"Broadcasting status for {agent_name}: {status} - {current_task}")

        # Broadcast to all connected clients
        if self.connection_manager:
            await self.connection_manager.broadcast_to_all(json.dumps(status_message))
        else:
            logger.warning("No connection manager available for broadcasting")

    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get current status for a specific agent."""
        return self.agent_states.get(agent_name)

    def get_all_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get current status for all agents."""
        return self.agent_states.copy()

    async def broadcast_workflow_progress(
        self,
        current_step: int,
        total_steps: int,
        current_task: str,
        session_id: str = "global_session"
    ):
        progress_percentage = (current_step / total_steps) * 100 if total_steps > 0 else 0

        message = {
            "type": "workflow_progress",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "current_step_index": current_step,
                "total_steps": total_steps,
                "current_task": current_task,
                "overall_progress": progress_percentage,
                "session_id": session_id
            }
        }

        logger.info(f"Broadcasting workflow progress: Step {current_step}/{total_steps}")

        if self.connection_manager:
            await self.connection_manager.broadcast_to_all(json.dumps(message))

# Convenience functions for easier integration
async def broadcast_agent_thinking(broadcaster: AgentStatusBroadcaster, agent_name: str, task: str, session_id: str = "global_session"):
    """Convenience function to broadcast that an agent is thinking."""
    await broadcaster.broadcast_agent_status(
        agent_name=agent_name,
        status="thinking",
        current_task=f"Thinking about: {task}",
        session_id=session_id
    )

async def broadcast_agent_working(broadcaster: AgentStatusBroadcaster, agent_name: str, task: str, progress: float, session_id: str = "global_session"):
    """Convenience function to broadcast that an agent is working."""
    await broadcaster.broadcast_agent_status(
        agent_name=agent_name,
        status="working",
        current_task=task,
        progress_percentage=progress,
        session_id=session_id
    )

async def broadcast_agent_complete(broadcaster: AgentStatusBroadcaster, agent_name: str, result: str, session_id: str = "global_session"):
    """Convenience function to broadcast that an agent has completed work."""
    await broadcaster.broadcast_agent_status(
        agent_name=agent_name,
        status="completed",
        current_task=f"Completed: {result}",
        progress_percentage=100,
        session_id=session_id
    )

async def broadcast_agent_error(broadcaster: AgentStatusBroadcaster, agent_name: str, error: str, session_id: str = "global_session"):
    """Convenience function to broadcast that an agent has encountered an error."""
    await broadcaster.broadcast_agent_status(
        agent_name=agent_name,
        status="error",
        error_message=error,
        session_id=session_id
    )