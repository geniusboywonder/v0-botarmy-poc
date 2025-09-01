import pytest
from backend.services.general_chat_service import GeneralChatService

@pytest.fixture
def chat_service():
    return GeneralChatService()

def test_handle_message(chat_service):
    response = chat_service.handle_message("Hello")
    assert "You said: 'Hello'" in response
    assert len(chat_service.get_history()) == 2  # User and assistant message

def test_history_clears(chat_service):
    chat_service.handle_message("First message")
    assert len(chat_service.get_history()) == 2
    chat_service.clear_history()
    assert len(chat_service.get_history()) == 0
