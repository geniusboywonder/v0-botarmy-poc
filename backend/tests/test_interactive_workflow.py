import pytest
import asyncio
import os
from unittest.mock import MagicMock, AsyncMock, patch
import sys

# Mock modules to prevent circular imports during test collection
sys.modules['backend.error_handler'] = MagicMock()
sys.modules['backend.bridge'] = MagicMock()

from prefect.testing.utilities import prefect_test_harness
from backend.workflow.generic_orchestrator import generic_workflow
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.serialization_safe_wrapper import make_serialization_safe

class MockConnectionManager:
    def __init__(self):
        self.broadcast_messages = []

    async def broadcast_to_all(self, message: str):
        self.broadcast_messages.append(message)
        await asyncio.sleep(0)

@pytest.fixture
def mock_broadcaster():
    """Provides a mock AgentStatusBroadcaster that records messages."""
    manager = MockConnectionManager()
    broadcaster = AgentStatusBroadcaster(manager)
    # Mock the methods that will be called
    broadcaster.broadcast_agent_progress = AsyncMock()
    broadcaster.broadcast_agent_response = AsyncMock()
    return broadcaster

@pytest.mark.asyncio
async def test_generic_workflow_execution(mock_broadcaster):
    """
    Tests the generic_workflow with a mocked LLM backend.
    Verifies that the workflow executes all stages and that progress is broadcast.
    """
    # Mock the LLM Service to return a simple string
    mock_llm_service = MagicMock()
    mock_llm_service.generate_response = AsyncMock(return_value="Mocked LLM Result")

    # Wrap the broadcaster to prevent serialization issues with Prefect
    safe_broadcaster = make_serialization_safe(mock_broadcaster, "MockBroadcaster")

    with prefect_test_harness():
        # Patch the function that gets the LLM service
        with patch('backend.agents.generic_agent_executor.get_llm_service', return_value=mock_llm_service):
            results = await generic_workflow(
                config_name="sdlc",
                initial_input="Test Project",
                session_id="test_session_generic",
                status_broadcaster=safe_broadcaster
            )

    print("Workflow results:", results)

    # 1. Verify the results from the mocked LLM
    assert len(results['results']) == 5
    for task_name, task_result in results['results'].items():
        assert task_result == "Mocked LLM Result"

    # 2. Verify that progress was broadcast for each of the 5 agents
    # The executor broadcasts progress 4 times per task. 5 tasks * 4 broadcasts = 20
    assert mock_broadcaster.broadcast_agent_progress.call_count == 20

    # 3. Verify that stage responses were broadcast
    # One for each of the 5 stages, plus a final "finished" message.
    assert mock_broadcaster.broadcast_agent_response.call_count == 6
