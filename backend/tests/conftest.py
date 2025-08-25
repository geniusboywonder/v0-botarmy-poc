"""
pytest configuration and shared fixtures for BotArmy tests.
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def mock_llm_service():
    """Mock LLM service for testing agents without actual API calls."""
    mock_service = Mock()
    mock_service.generate_response = Mock(return_value="Mock LLM response for testing")
    return mock_service

@pytest.fixture
def mock_websocket():
    """Mock WebSocket connection for testing."""
    mock_ws = AsyncMock()
    mock_ws.send_text = AsyncMock()
    mock_ws.receive_text = AsyncMock()
    return mock_ws

@pytest.fixture
def sample_project_brief():
    """Sample project brief for testing agent workflows."""
    return "Create a simple todo app with React frontend and Python backend"

@pytest.fixture
def sample_agent_response():
    """Sample structured agent response for testing."""
    return {
        "analysis": "Test analysis content",
        "recommendations": ["Test recommendation 1", "Test recommendation 2"],
        "confidence": 0.85,
        "next_steps": ["Step 1", "Step 2"]
    }

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Test environment setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables."""
    os.environ['TESTING'] = 'true'
    os.environ['LLM_PROVIDER'] = 'mock'
    yield
    # Cleanup after tests
    if 'TESTING' in os.environ:
        del os.environ['TESTING']
    if 'LLM_PROVIDER' in os.environ:
        del os.environ['LLM_PROVIDER']