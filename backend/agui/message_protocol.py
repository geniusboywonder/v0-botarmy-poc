import uuid
from datetime import datetime, timezone
from typing import Optional

class MessageProtocol:
    """
    A class to create standardized WebSocket messages for the AG-UI protocol.
    """

    @staticmethod
    def _create_base_message(
        msg_type: str,
        session_id: str,
        content: str = "",
        agent_name: str = "System",
        metadata: Optional[dict] = None
    ) -> dict:
        """Helper to create the base structure for all messages."""
        return {
            "id": str(uuid.uuid4()),
            "type": msg_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "agent_name": agent_name,
            "content": content,
            "metadata": metadata or {},
            "requires_ack": False
        }

    @staticmethod
    def create_agent_status_update(agent_name: str, status: str, session_id: str, task: str = None) -> dict:
        """Creates a standardized agent status message."""
        content = f"Agent '{agent_name}' is now {status}."
        if task:
            content += f" Current task: {task}"

        metadata = {"status": status, "task": task}

        return MessageProtocol._create_base_message(
            msg_type="agent_status",
            session_id=session_id,
            content=content,
            agent_name=agent_name,
            metadata=metadata
        )

    @staticmethod
    def create_agent_progress_update(agent_name: str, stage: str, current: int, total: int, session_id: str, estimated_time_remaining: float = None) -> dict:
        """Creates a standardized agent progress message."""
        content = f"Agent '{agent_name}' is at stage '{stage}' ({current}/{total})."
        metadata = {
            "stage": stage,
            "current": current,
            "total": total,
            "estimated_time_remaining": estimated_time_remaining
        }
        return MessageProtocol._create_base_message(
            msg_type="agent_progress",
            session_id=session_id,
            content=content,
            agent_name=agent_name,
            metadata=metadata
        )

    @staticmethod
    def create_agent_response(agent_name: str, content: str, session_id: str, metadata: Optional[dict] = None) -> dict:
        """Creates a standardized agent response message."""
        return MessageProtocol._create_base_message(
            msg_type="agent_response",
            session_id=session_id,
            content=content,
            agent_name=agent_name,
            metadata=metadata
        )

    @staticmethod
    def create_error_message(error: str, session_id: str, error_type: str = "general", agent_name: str = "System") -> dict:
        """Creates a standardized error message."""
        metadata = {"error_type": error_type}

        return MessageProtocol._create_base_message(
            msg_type="error",
            session_id=session_id,
            content=error,
            agent_name=agent_name,
            metadata=metadata
        )

    @staticmethod
    def create_system_message(content: str, session_id: str, message_type: str = "info", metadata: Optional[dict] = None) -> dict:
        """Creates a standardized system message."""
        # Combine provided metadata with the message_type
        final_metadata = metadata or {}
        final_metadata["message_type"] = message_type

        return MessageProtocol._create_base_message(
            msg_type="system",
            session_id=session_id,
            content=content,
            agent_name="System",
            metadata=final_metadata
        )

    @staticmethod
    def create_heartbeat_message() -> dict:
        """Creates a heartbeat message for connection monitoring. It does not have a session_id."""
        return {
            "id": str(uuid.uuid4()),
            "type": "heartbeat",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_name": "System",
            "content": "ping",
            "metadata": {},
            "requires_ack": False
        }
