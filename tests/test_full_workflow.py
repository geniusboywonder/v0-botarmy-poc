import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

# Add project root to path to allow imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from backend.workflow import run_complete_workflow

@pytest.mark.asyncio
async def test_full_workflow_in_test_mode():
    """
    Tests that the full agent workflow runs successfully in test mode.
    """
    # Mock the status broadcaster
    mock_broadcaster = AsyncMock()

    # Project brief for the test
    project_brief = "Create a simple todo application."

    # Run the workflow in test mode
    results = await run_complete_workflow(
        project_brief=project_brief,
        session_id="test_session",
        status_broadcaster=mock_broadcaster,
        test_mode=True
    )

    # Assertions
    assert results is not None
    assert isinstance(results, dict)

    # Check that all 5 agents produced a result
    expected_agents = ["Analyst", "Architect", "Developer", "Tester", "Deployer"]
    assert len(results) == len(expected_agents)
    for agent_name in expected_agents:
        assert agent_name in results
        assert "error" not in results[agent_name]
        # In test mode, the result should be a confirmation string
        assert "Test Mode" in results[agent_name]

    # Check that the status broadcaster was called
    assert mock_broadcaster.broadcast_agent_status.call_count >= len(expected_agents) * 2 # start and complete
    assert mock_broadcaster.broadcast_workflow_progress.call_count >= len(expected_agents)
