import re
from typing import Dict, Any

class MessageRouter:
    def __init__(self):
        self.project_mode_keywords = [
            "start project", "begin working on", "project mode", "enable agents",
            "/project start"
        ]
        self.general_chat_keywords = [
            "general chat", "exit project", "chat mode", "stop project", "/chat",
            "/project exit"
        ]

    def route_message(self, message: Dict[str, Any], current_mode: str) -> str:
        """
        Routes the message to either the general chat service or the project workflow.
        """
        text = message.get("text", "").lower().strip()

        # Check for explicit commands to switch mode
        if any(keyword in text for keyword in self.project_mode_keywords):
            return "switch_to_project"
        if any(keyword in text for keyword in self.general_chat_keywords):
            return "switch_to_general"

        # Route based on current mode
        if current_mode == "project":
            return "project_workflow"
        else:
            return "general_chat"

    def get_project_description(self, message: str) -> str:
        """
        Extracts the project description from a message.
        """
        match = re.search(r"(?:start project|begin working on|/project start)\s*(.*)", message, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return "New Project"
