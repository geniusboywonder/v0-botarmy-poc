import json
import logging

from backend.agui.protocol import MessageProtocol
from backend.connection_manager import EnhancedConnectionManager

logger = logging.getLogger(__name__)

class AgentStatusBroadcaster:
    def __init__(self, connection_manager: EnhancedConnectionManager):
        self.connection_manager = connection_manager

    async def _broadcast(self, message: dict):
        """Helper method to serialize and broadcast a message."""
        serialized_message = json.dumps(message, default=str)
        await self.connection_manager.broadcast_to_all(serialized_message)

    async def broadcast_agent_started(self, agent_name: str, task_description: str, session_id: str):
        """Broadcasts that an agent has started a task."""
        logger.info(f"Broadcasting AGENT_STARTED for {agent_name}")
        message = MessageProtocol.create_agent_status_update(
            agent_name=agent_name,
            status="started",
            task=task_description,
            session_id=session_id
        )
        await self._broadcast(message)

    async def broadcast_agent_waiting(self, agent_name: str, task_description: str, session_id: str):
        """Broadcasts that the workflow is waiting for human approval for an agent."""
        logger.info(f"Broadcasting AGENT_WAITING for {agent_name}")
        message = MessageProtocol.create_agent_status_update(
            agent_name=agent_name,
            status="waiting_for_approval",
            task=f"Awaiting user approval to start: {task_description}",
            session_id=session_id
        )
        await self._broadcast(message)

    async def broadcast_agent_thinking(self, agent_name: str, session_id: str):
        """Broadcasts that an agent is thinking (e.g., calling an LLM)."""
        logger.info(f"Broadcasting AGENT_THINKING for {agent_name}")
        message = MessageProtocol.create_agent_status_update(
            agent_name=agent_name,
            status="thinking",
            task="Querying Language Model...",
            session_id=session_id
        )
        await self._broadcast(message)

    async def broadcast_agent_completed(self, agent_name: str, result: str, session_id: str):
        """Broadcasts that an agent has completed its task."""
        logger.info(f"Broadcasting AGENT_COMPLETED for {agent_name}")
        # First, send a "completed" status update
        status_message = MessageProtocol.create_agent_status_update(
            agent_name=agent_name,
            status="completed",
            task="Task finished.",
            session_id=session_id
        )
        await self._broadcast(status_message)

        # Then, send the actual result as a separate response message
        response_message = MessageProtocol.create_agent_response(
            agent_name=agent_name,
            content=result,
            session_id=session_id
        )
        await self._broadcast(response_message)


    async def broadcast_agent_error(self, agent_name: str, error: str, session_id: str):
        """Broadcasts that an agent has encountered an error."""
        logger.info(f"Broadcasting AGENT_ERROR for {agent_name}")
        message = MessageProtocol.create_error_message(
            error=error,
            agent_name=agent_name,
            session_id=session_id
        )
        await self._broadcast(message)
