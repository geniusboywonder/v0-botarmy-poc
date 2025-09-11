import pytest
import asyncio
import os
import sys
from unittest.mock import MagicMock, AsyncMock, patch

# --- Forceful mocking to prevent ANY real code from running ---

# Mock ErrorHandler to prevent circular imports during test collection
mock_error_handler = MagicMock()
mock_error_handler.handle_workflow_error = AsyncMock(return_value={"data": {"error": "Mocked Error"}})
sys.modules['backend.error_handler'] = MagicMock(ErrorHandler=mock_error_handler)

# Mock AGUI_Handler/bridge to be safe and prevent other circular imports
sys.modules['backend.bridge'] = MagicMock()

# Now that the problematic modules are mocked, we can import the rest
from prefect.testing.utilities import prefect_test_harness
from backend.workflow import generic_workflow
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.connection_manager import EnhancedConnectionManager

# --- Mocks ---

class MockConnectionManager:
    def __init__(self):
        self.broadcast_messages = []

    async def broadcast_to_all(self, message: str):
        self.broadcast_messages.append(message)
        await asyncio.sleep(0) # yield control

@pytest.fixture
def mock_broadcaster():
    """Provides a mock AgentStatusBroadcaster that records messages."""
    manager = MockConnectionManager()
    broadcaster = AgentStatusBroadcaster(manager)
    broadcaster.broadcast_agent_status = AsyncMock(wraps=broadcaster.broadcast_agent_status)
    
    broadcaster.broadcast_agent_completed = AsyncMock(wraps=broadcaster.broadcast_agent_completed)
    broadcaster.broadcast_agent_status.reset_mock()
    
    broadcaster.broadcast_agent_completed.reset_mock()
    return broadcaster


# --- Tests ---

@pytest.mark.asyncio
async def test_workflow_auto_approve(mock_broadcaster):
    """
    Tests the workflow with AUTO_ACTION=approve.
    Verifies that all agents are approved and executed.
    """
    os.environ["AUTO_ACTION"] = "approve"

    with prefect_test_harness():
        with patch('backend.workflow.handle_agent_run', new_callable=AsyncMock) as mock_handle_agent_run:
            mock_handle_agent_run.return_value = {"approval_status": "approved", "result": {"content": "Mocked LLM Result"}}
            results = await generic_workflow(
                project_brief="Test Project",
                session_id="test_session_approve",
                status_broadcaster=mock_broadcaster
            )

    print("Workflow results:", results)


    # 1. Verify approval status in results
    for agent_name, agent_result in results.items():
        assert agent_result["approval_status"] == "approved"
        # The LLM is now mocked directly in the service
        # The result is now nested in the 'result' key
        assert agent_result["result"].get("content") == "Mocked LLM Result"

    # 2. Verify that progress updates and completion were called for each agent
    assert mock_broadcaster.broadcast_agent_progress.call_count == 20
    assert mock_broadcaster.broadcast_agent_completed.call_count == 5


@pytest.mark.asyncio
async def test_workflow_auto_deny(mock_broadcaster):
    """
    Tests the workflow with AUTO_ACTION=deny.
    Verifies that all agents are denied and their tasks are skipped.
    """
    os.environ["AUTO_ACTION"] = "deny"

    with prefect_test_harness():
        with patch('backend.workflow.handle_agent_run', new_callable=AsyncMock) as mock_handle_agent_run:
            mock_handle_agent_run.return_value = {"approval_status": "denied", "output": "Task skipped because it was denied by the user."}
            results = await generic_workflow(
                project_brief="Test Project",
                session_id="test_session_deny",
                status_broadcaster=mock_broadcaster
            )

    # 1. Verify approval status in results
    for agent_name, agent_result in results.items():
        assert agent_result["approval_status"] == "denied"
        assert "denied by the user" in agent_result["output"]

    # 2. Verify that no progress updates or completion were called
    assert mock_broadcaster.broadcast_agent_progress.call_count == 0
    assert mock_broadcaster.broadcast_agent_completed.call_count == 0
