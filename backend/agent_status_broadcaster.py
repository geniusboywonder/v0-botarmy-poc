"""
Agent Status Broadcasting system for real-time progress updates.
Integrates with the WebSocket system to broadcast agent status changes.
"""

import asyncio
import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime

from backend.agui.protocol import agui_handler, MessageType

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
        task: Optional[str] = None,
        session_id: str = "global_session",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Broadcast agent status update.
        
        Args:
            agent_name: Name of the agent
            status: Current status (idle, thinking, working, complete, error)
            task: Current task description
            session_id: Session identifier
            metadata: Additional status metadata
        """
        
        # Update internal state
        self.agent_states[agent_name] = {
            "name": agent_name,
            "status": status,
            "task": task,
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
                "task": task,
                "session_id": session_id,
                "metadata": metadata or {}
            }
        }
        
        logger.info(f"Broadcasting status update for {agent_name}: {status}")
        
        # Broadcast to all connected clients
        if self.connection_manager:
            await self.connection_manager.broadcast_to_all(json.dumps(status_message))
        else:
            logger.warning("No connection manager available for broadcasting")
    
    async def broadcast_agent_completed(
        self,
        agent_name: str,
        result: str,
        session_id: str = "global_session",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Broadcast agent completion status.
        
        Args:
            agent_name: Name of the agent
            result: Completion result or summary
            session_id: Session identifier
            metadata: Additional completion metadata
        """
        
        # Update internal state
        self.agent_states[agent_name] = {
            "name": agent_name,
            "status": "completed",
            "task": f"Completed: {result[:100]}...",  # Truncate long results
            "result": result,
            "last_update": datetime.now().isoformat(),
            "session_id": session_id,
            "metadata": metadata or {}
        }
        
        # Create completion message
        completion_message = {
            "type": "agent_completed",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "agent_name": agent_name,
                "result": result,
                "status": "completed",
                "session_id": session_id,
                "metadata": metadata or {}
            }
        }
        
        logger.info(f"Broadcasting completion for {agent_name}: Task completed")
        
        # Broadcast to all connected clients
        if self.connection_manager:
            await self.connection_manager.broadcast_to_all(json.dumps(completion_message))
        else:
            logger.warning("No connection manager available for completion broadcasting")
    
    async def broadcast_agent_progress(
        self,
        agent_name: str,
        stage: str,
        current: int,
        total: int,
        session_id: str = "global_session",
        estimated_time_remaining: Optional[float] = None
    ):
        """
        Broadcast agent progress update with detailed progress information.
        
        Args:
            agent_name: Name of the agent
            stage: Current stage description
            current: Current progress value
            total: Total progress value
            session_id: Session identifier
            estimated_time_remaining: Estimated time remaining in seconds
        """
        
        progress_percentage = (current / total * 100) if total > 0 else 0
        
        # Update agent state with progress
        if agent_name not in self.agent_states:
            self.agent_states[agent_name] = {}
            
        self.agent_states[agent_name].update({
            "progress_stage": stage,
            "progress_current": current,
            "progress_total": total,
            "progress_percentage": progress_percentage,
            "estimated_time_remaining": estimated_time_remaining,
            "last_progress_update": datetime.now().isoformat()
        })
        
        # Create progress message
        progress_message = {
            "type": "agent_progress",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "agent_name": agent_name,
                "stage": stage,
                "current": current,
                "total": total,
                "percentage": progress_percentage,
                "estimated_time_remaining": estimated_time_remaining,
                "session_id": session_id
            }
        }
        
        logger.info(f"Broadcasting progress for {agent_name}: {stage} ({current}/{total})")
        
        # Broadcast to all connected clients
        if self.connection_manager:
            await self.connection_manager.broadcast_to_all(json.dumps(progress_message))
        else:
            logger.warning("No connection manager available for progress broadcasting")
    
    async def broadcast_agent_error(
        self,
        agent_name: str,
        error_message: str,
        session_id: str = "global_session",
        error_details: Optional[Dict[str, Any]] = None
    ):
        """
        Broadcast agent error status.
        
        Args:
            agent_name: Name of the agent
            error_message: Error description
            session_id: Session identifier
            error_details: Additional error details
        """
        
        # Update agent state with error
        self.agent_states[agent_name] = {
            "name": agent_name,
            "status": "error",
            "error_message": error_message,
            "error_details": error_details or {},
            "last_update": datetime.now().isoformat(),
            "session_id": session_id
        }
        
        # Create error message
        error_message_data = {
            "type": "agent_error",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "agent_name": agent_name,
                "error_message": error_message,
                "error_details": error_details or {},
                "session_id": session_id
            }
        }
        
        logger.error(f"Broadcasting error for {agent_name}: {error_message}")
        
        # Broadcast to all connected clients
        if self.connection_manager:
            await self.connection_manager.broadcast_to_all(json.dumps(error_message_data))
        else:
            logger.warning("No connection manager available for error broadcasting")
    
    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get current status for a specific agent."""
        return self.agent_states.get(agent_name)
    
    def get_all_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get current status for all agents."""
        return self.agent_states.copy()

    async def broadcast_agent_response(
        self,
        agent_name: str,
        content: str,
        session_id: str = "global_session",
    ):
        """Broadcasts a message from an agent to the main chat window."""
        if not self.connection_manager:
            logger.warning("No connection manager available for broadcasting agent response")
            return

        message = agui_handler.create_agent_message(
            content=content,
            agent_name=agent_name,
            session_id=session_id,
            message_type=MessageType.AGENT_MESSAGE,
        )
        await self.connection_manager.broadcast_to_all(
            agui_handler.serialize_message(message)
        )
        logger.info(f"Broadcasted agent response from {agent_name}")

# Convenience functions for easier integration
async def broadcast_agent_thinking(broadcaster, agent_name: str, task: str, session_id: str = "global_session"):
    """Convenience function to broadcast that an agent is thinking."""
    await broadcaster.broadcast_agent_status(
        agent_name=agent_name,
        status="thinking",
        task=f"Thinking about: {task}",
        session_id=session_id
    )

async def broadcast_agent_working(broadcaster, agent_name: str, task: str, session_id: str = "global_session"):
    """Convenience function to broadcast that an agent is working."""
    await broadcaster.broadcast_agent_status(
        agent_name=agent_name,
        status="working",
        task=task,
        session_id=session_id
    )

async def broadcast_agent_complete(broadcaster, agent_name: str, result: str, session_id: str = "global_session"):
    """Convenience function to broadcast that an agent has completed work."""
    await broadcaster.broadcast_agent_completed(
        agent_name=agent_name,
        result=result,
        session_id=session_id
    )
