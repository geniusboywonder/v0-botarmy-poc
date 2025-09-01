import pytest
from backend.services.message_router import MessageRouter

@pytest.fixture
def router():
    return MessageRouter()

def test_route_to_general_chat_by_default(router):
    message = {"text": "Hello, how are you?"}
    assert router.route_message(message, "general") == "general_chat"

def test_route_to_project_workflow_in_project_mode(router):
    message = {"text": "Implement this feature."}
    assert router.route_message(message, "project") == "project_workflow"

def test_switch_to_project_mode(router):
    message = {"text": "start project build a website"}
    assert router.route_message(message, "general") == "switch_to_project"

def test_switch_to_general_mode(router):
    message = {"text": "let's go to general chat"}
    assert router.route_message(message, "project") == "switch_to_general"

def test_get_project_description(router):
    message = "start project build a cool new app"
    assert router.get_project_description(message) == "build a cool new app"

def test_get_project_description_no_description(router):
    message = "start project"
    assert router.get_project_description(message) == "New Project"
