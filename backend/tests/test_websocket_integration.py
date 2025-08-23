import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from backend.main import handle_websocket_message

@pytest.fixture
def mock_manager():
    return AsyncMock()

@pytest.fixture
def mock_heartbeat_monitor():
    return MagicMock()

@pytest.fixture
def mock_status_broadcaster():
    return AsyncMock()

@pytest.mark.asyncio
async def test_handle_start_project_command(mock_manager, mock_heartbeat_monitor, mock_status_broadcaster, monkeypatch):
    """
    Tests that the 'start_project' command is handled correctly.
    """
    # Mock the run_and_track_workflow function to avoid running the full workflow
    mock_run_workflow = AsyncMock()
    monkeypatch.setattr("backend.main.run_and_track_workflow", mock_run_workflow)

    client_id = "test_client"
    message = {
        "type": "user_command",
        "data": {
            "command": "start_project",
            "brief": "Test project brief",
            "test_mode": True
        },
        "session_id": "test_session"
    }

    await handle_websocket_message(
        client_id,
        message,
        mock_manager,
        mock_heartbeat_monitor,
        mock_status_broadcaster
    )

    # Check that run_and_track_workflow was called with the correct arguments
    mock_run_workflow.assert_called_once_with(
        "Test project brief",
        "test_session",
        mock_manager,
        mock_status_broadcaster,
        True
    )
