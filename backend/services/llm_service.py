import time
import os
from openai import OpenAI

class LLMService:
    """
    A centralized service to handle all interactions with LLM providers.
    This service is responsible for making API calls, managing API keys,
    and handling rate limiting.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=self.api_key)
        self.last_call_time = 0
        self.rate_limit_delay = 2 # seconds

    def _enforce_rate_limit(self):
        """
        Enforces a simple delay between API calls to prevent hitting rate limits.
        """
        elapsed_time = time.time() - self.last_call_time
        if elapsed_time < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed_time)
        self.last_call_time = time.time()

    def generate_response(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        """
        Generates a response from the LLM.

        Args:
            prompt: The full prompt to send to the LLM.
            model: The model to use for the generation.

        Returns:
            The text content of the LLM's response.
        """
        self._enforce_rate_limit()

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            return content.strip() if content else "Error: Empty response from API."
        except Exception as e:
            # In a real app, this would have more robust error handling
            print(f"An error occurred with the OpenAI API: {e}")
            return f"Error: Could not get a response from the API. Details: {e}"

# Singleton instance to be used across the application
llm_service = LLMService()
