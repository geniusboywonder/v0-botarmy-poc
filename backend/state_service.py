import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class StateService:
    """
    Manages the application's state, acting as a single source of truth.
    This implementation stores state in memory.
    """

    def __init__(self):
        self._state: Dict[str, Any] = {
            "agents": {},
            "workflows": {},
            "artifacts": {},
        }
        logger.info("StateService initialized with in-memory storage.")

    def get_full_state(self) -> Dict[str, Any]:
        """Returns a copy of the entire application state."""
        return self._state.copy()

    def update_agent_status(self, agent_name: str, status: str, task: Optional[str] = None):
        """Updates the status of a specific agent."""
        if agent_name not in self._state["agents"]:
            self._state["agents"][agent_name] = {}
        self._state["agents"][agent_name]["status"] = status
        if task:
            self._state["agents"][agent_name]["task"] = task
        logger.debug(f"Updated agent {agent_name} status to {status}")

    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves the status of a specific agent."""
        return self._state["agents"].get(agent_name)

    def update_workflow_status(self, session_id: str, status: str):
        """Updates the status of a workflow."""
        if session_id not in self._state["workflows"]:
            self._state["workflows"][session_id] = {}
        self._state["workflows"][session_id]["status"] = status
        logger.debug(f"Updated workflow {session_id} status to {status}")

    def get_workflow_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the status of a workflow."""
        return self._state["workflows"].get(session_id)

    def add_artifact(self, artifact_id: str, artifact_data: Dict[str, Any]):
        """Adds an artifact to the state."""
        self._state["artifacts"][artifact_id] = artifact_data
        logger.debug(f"Added artifact {artifact_id}")

    def get_artifact(self, artifact_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a specific artifact."""
        return self._state["artifacts"].get(artifact_id)

state_service = StateService()

def get_state_service() -> StateService:
    """Returns the singleton instance of the StateService."""
    return state_service
