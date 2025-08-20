import uuid
from datetime import datetime, timezone

class MessageProtocol:
    """
    A class to create standardized WebSocket messages for the AG-UI protocol.
    """

    @staticmethod
    def _create_base_message(msg_type: str, content: str = "", agent_name: str = "System", metadata: dict = None) -> dict:
        """Helper to create the base structure for all messages."""
        return {
            "id": str(uuid.uuid4()),
            "type": msg_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_name": agent_name,
            "content": content,
            "metadata": metadata or {},
            "requires_ack": False  # Defaulting to False as per initial requirements
        }

    @staticmethod
    def create_agent_status_update(agent_name: str, status: str, task: str = None, session_id: str = None) -> dict:
        """Creates a standardized agent status message."""
        content = f"Agent '{agent_name}' is now {status}."
        if task:
            content += f" Current task: {task}"

        metadata = {"status": status, "task": task}
        if session_id:
            metadata["session_id"] = session_id

        return MessageProtocol._create_base_message(
            msg_type="agent_status",
            content=content,
            agent_name=agent_name,
            metadata=metadata
        )

    @staticmethod
    def create_agent_response(agent_name: str, content: str, metadata: dict = None, session_id: str = None) -> dict:
        """Creates a standardized agent response message."""
        if metadata is None:
            metadata = {}
        if session_id:
            metadata["session_id"] = session_id

        return MessageProtocol._create_base_message(
            msg_type="agent_response",
            content=content,
            agent_name=agent_name,
            metadata=metadata
        )

    @staticmethod
    def create_error_message(error: str, error_type: str = "general", agent_name: str = "System", session_id: str = None) -> dict:
        """Creates a standardized error message."""
        metadata = {"error_type": error_type}
        if session_id:
            metadata["session_id"] = session_id

        return MessageProtocol._create_base_message(
            msg_type="error",
            content=error,
            agent_name=agent_name,
            metadata=metadata
        )

    @staticmethod
    def create_system_message(content: str, message_type: str = "info", session_id: str = None) -> dict:
        """Creates a standardized system message."""
        metadata = {"message_type": message_type}
        if session_id:
            metadata["session_id"] = session_id

        return MessageProtocol._create_base_message(
            msg_type="system",
            content=content,
            agent_name="System",
            metadata=metadata
        )

    @staticmethod
    def create_heartbeat_message() -> dict:
        """Creates a heartbeat message for connection monitoring."""
        return MessageProtocol._create_base_message(
            msg_type="heartbeat",
            content="ping",
            agent_name="System"
        )
