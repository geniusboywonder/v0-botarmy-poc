import pytest
from backend.services.role_enforcer import RoleEnforcer

@pytest.fixture
def enforcer():
    return RoleEnforcer()

@pytest.mark.parametrize("agent_role, message, expected", [
    ("Analyst", "I need to gather requirements.", True),
    ("Analyst", "Let's talk about system design.", False),
    ("Architect", "What about the architecture?", True),
    ("Developer", "I will write some code.", True),
    ("Tester", "We need to test this feature.", True),
    ("Deployer", "Time to deploy.", True),
])
def test_validate_topic(enforcer, agent_role, message, expected):
    assert enforcer.validate_topic(agent_role, message) == expected

def test_get_redirect_message(enforcer):
    message = enforcer.get_redirect_message("Analyst")
    assert "This is outside my analysis role" in message
