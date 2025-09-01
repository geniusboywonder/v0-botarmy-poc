from typing import Dict, List

class RoleEnforcer:
    def __init__(self):
        self.agent_roles = {
            'Analyst': {
                'focus': ['requirements', 'analysis', 'user stories', 'specifications'],
                'off_topic_redirect': 'This is outside my analysis role. Consider asking the {appropriate_agent} or switch to general chat.'
            },
            'Architect': {
                'focus': ['system design', 'architecture', 'technical decisions', 'patterns'],
                'off_topic_redirect': 'This is outside my architectural role. Consider asking the {appropriate_agent} or switch to general chat.'
            },
            'Developer': {
                'focus': ['code', 'implementation', 'programming', 'debugging'],
                'off_topic_redirect': 'This is outside my development role. Consider asking the {appropriate_agent} or switch to general chat.'
            },
            'Tester': {
                'focus': ['testing', 'quality assurance', 'test cases', 'bug reports'],
                'off_topic_redirect': 'This is outside my testing role. Consider asking the {appropriate_agent} or switch to general chat.'
            },
            'Deployer': {
                'focus': ['deployment', 'release', 'infrastructure', 'monitoring'],
                'off_topic_redirect': 'This is outside my deployment role. Consider asking the {appropriate_agent} or switch to general chat.'
            }
        }

    def validate_topic(self, agent_role: str, message: str) -> bool:
        """
        Validates if the message topic is within the agent's focus.
        """
        if agent_role not in self.agent_roles:
            return False

        focus_keywords = self.agent_roles[agent_role]['focus']
        message_lower = message.lower()

        return any(keyword in message_lower for keyword in focus_keywords)

    def get_redirect_message(self, agent_role: str) -> str:
        """
        Gets the off-topic redirect message for a given agent role.
        """
        if agent_role in self.agent_roles:
            # A more sophisticated implementation would suggest an appropriate agent.
            return self.agent_roles[agent_role]['off_topic_redirect'].format(appropriate_agent="another agent")
        return "This is off-topic. Please try another agent or switch to general chat."
