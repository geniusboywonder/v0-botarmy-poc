import pytest
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

# Add project root to path to allow absolute imports from backend
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest file
    after command line options have been parsed.
    """
    print("Setting up test environment in conftest.py...")
    # Set a dummy OpenAI API key for all tests
    os.environ["OPENAI_API_KEY"] = "dummy_key"
    # Set the LLM to test mode
    os.environ["TEST_MODE"] = "true"

# We still need these mocks for the test collection phase
mock_error_handler = MagicMock()
mock_error_handler.handle_workflow_error = AsyncMock(return_value={"data": {"error": "Mocked Error"}})
sys.modules['backend.error_handler'] = MagicMock(ErrorHandler=mock_error_handler)
sys.modules['backend.bridge'] = MagicMock()

# We also need a mock broadcaster fixture, but it can't be in the same file as pytest_configure
# if other fixtures depend on it. For simplicity, we'll keep it here for now.
# This can be moved to a separate file if needed.
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.connection_manager import EnhancedConnectionManager

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
    broadcaster.broadcast_agent_waiting = AsyncMock(wraps=broadcaster.broadcast_agent_waiting)
    broadcaster.broadcast_agent_started = AsyncMock(wraps=broadcaster.broadcast_agent_started)
    broadcaster.broadcast_agent_completed = AsyncMock(wraps=broadcaster.broadcast_agent_completed)
    broadcaster.broadcast_agent_waiting.reset_mock()
    broadcaster.broadcast_agent_started.reset_mock()
    broadcaster.broadcast_agent_completed.reset_mock()
    return broadcaster
