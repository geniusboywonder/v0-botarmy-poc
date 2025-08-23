import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from backend.workflow import botarmy_workflow

# Mock the agent tasks
@pytest.fixture
def mock_agent_tasks(monkeypatch):
    monkeypatch.setattr("backend.workflow.run_analyst_task", AsyncMock(return_value="Analyst Result"))
    monkeypatch.setattr("backend.workflow.run_architect_task", AsyncMock(return_value="Architect Result"))
    monkeypatch.setattr("backend.workflow.run_developer_task", AsyncMock(return_value="Developer Result"))
    monkeypatch.setattr("backend.workflow.run_tester_task", AsyncMock(return_value="Tester Result"))
    monkeypatch.setattr("backend.workflow.run_deployer_task", AsyncMock(return_value="Deployer Result"))

# Mock the status broadcaster
@pytest.fixture
def mock_status_broadcaster():
    broadcaster = MagicMock()
    broadcaster.broadcast_agent_status = AsyncMock()
    broadcaster.broadcast_workflow_progress = AsyncMock()
    return broadcaster

@pytest.mark.asyncio
async def test_botarmy_workflow_test_mode(mock_agent_tasks, mock_status_broadcaster):
    """
    Tests that the full workflow runs correctly in test mode.
    """
    project_brief = "Create a simple to-do app."
    session_id = "test_session_123"

    results = await botarmy_workflow(
        project_brief=project_brief,
        session_id=session_id,
        status_broadcaster=mock_status_broadcaster,
        test_mode=True
    )

    # Check that all agents were called
    assert len(results) == 5
    assert "Analyst" in results
    assert "Architect" in results
    assert "Developer" in results
    assert "Tester" in results
    assert "Deployer" in results

    # Check that the status broadcaster was called for each agent
    assert mock_status_broadcaster.broadcast_agent_status.call_count >= 10 # start and complete for each agent

    # Check that workflow progress was broadcast
    assert mock_status_broadcaster.broadcast_workflow_progress.call_count >= 2 # start and end
