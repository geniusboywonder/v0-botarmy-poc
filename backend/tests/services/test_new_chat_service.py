import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path to allow absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Mock the LLMService to prevent actual API calls during testing
class MockLLMService:
    def __init__(self):
        self.generate_response = AsyncMock(return_value="Mocked LLM Response")

# Patch the get_llm_service function to return our mock
@pytest.fixture(autouse=True)
def mock_get_llm_service():
    with patch('backend.services.general_chat_service.get_llm_service') as mock_get:
        mock_get.return_value = MockLLMService()
        yield mock_get

from backend.services.general_chat_service import GeneralChatService

@pytest.fixture
def chat_service():
    return GeneralChatService()

@pytest.mark.asyncio
async def test_chat_service_init(chat_service):
    assert chat_service.provider == "openai"
    assert chat_service.model == "gpt-4"
    assert chat_service.history == []
    assert chat_service.llm_service is not None

@pytest.mark.asyncio
async def test_handle_message(chat_service):
    message = "Hello, chat service!"
    response = await chat_service.handle_message(message)

    assert response == "Mocked LLM Response"
    assert len(chat_service.history) == 2
    assert chat_service.history[0] == {"role": "user", "content": message}
    assert chat_service.history[1] == {"role": "assistant", "content": "Mocked LLM Response"}
    chat_service.llm_service.generate_response.assert_called_once_with(
        prompt=message,
        agent_name="GeneralChat"
    )

@pytest.mark.asyncio
async def test_get_history(chat_service):
    await chat_service.handle_message("Test message 1")
    await chat_service.handle_message("Test message 2")
    history = chat_service.get_history()
    assert len(history) == 4
    assert history[0]["content"] == "Test message 1"
    assert history[2]["content"] == "Test message 2"

@pytest.mark.asyncio
async def test_clear_history(chat_service):
    await chat_service.handle_message("Message to clear")
    assert len(chat_service.history) == 2
    chat_service.clear_history()
    assert chat_service.history == []
