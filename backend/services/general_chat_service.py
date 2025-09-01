from typing import Dict, Any
from backend.services.llm_service import get_llm_service

class GeneralChatService:
    def __init__(self, provider: str = "openai", model: str = "gpt-4"):
        self.provider = provider
        self.model = model
        self.history = []
        self.llm_service = get_llm_service()

    async def handle_message(self, message: str) -> str:
        """
        Handles a message in general chat mode by calling the LLM service.
        """
        self.history.append({"role": "user", "content": message})

        # In a real implementation, this would call an LLM provider.
        response_text = await self.llm_service.generate_response(
            prompt=message,
            agent_name="GeneralChat"
        )

        self.history.append({"role": "assistant", "content": response_text})
        return response_text

    def get_history(self):
        """
        Returns the conversation history.
        """
        return self.history

    def clear_history(self):
        """
        Clears the conversation history.
        """
        self.history = []
