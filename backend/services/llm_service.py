import os
import asyncio
import logging
from openai import OpenAI, APIError
from backend.rate_limiter import OpenAIRateLimiter

logger = logging.getLogger(__name__)

class LLMService:
    """
    A centralized service to handle all interactions with LLM providers.
    This service is responsible for making API calls, managing API keys,
    and handling async rate limiting, retries, and fallbacks.
    """
    def __init__(self):
        self.is_test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key and not self.is_test_mode:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None # No client in test mode without key
        self.rate_limiter = OpenAIRateLimiter()
        self.max_retries = 3
        self.timeout_seconds = 30

    def get_fallback_response(self, agent_name: str, error: str) -> str:
        """Returns an agent-appropriate fallback message."""
        logger.warning(f"Providing fallback response for agent {agent_name} due to error: {error}")
        fallbacks = {
            "Analyst": "I'm analyzing your requirements. Please give me a moment to gather more information.",
            "Architect": "I'm designing the system architecture. This may take a moment to ensure quality.",
            "Developer": "I'm implementing the solution. Please be patient while I write the code.",
            "Tester": "I am preparing the test plan. This requires careful consideration.",
            "Deployer": "I am creating the deployment script. I am ensuring it is robust."
        }
        return fallbacks.get(agent_name, "I am currently processing your request. Please wait.")

    async def generate_response(self, prompt: str, agent_name: str, model: str = "gpt-3.5-turbo") -> str:
        """
        Asynchronously generates a response from the LLM, with retries and fallbacks.
        """
        if self.is_test_mode:
            return "Mocked LLM Result"

        estimated_tokens = len(prompt.split()) + 500

        for attempt in range(self.max_retries):
            try:
                await self.rate_limiter.wait_if_needed(estimated_tokens)

                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=self.timeout_seconds
                )

                if response.usage:
                    self.rate_limiter.record_request(response.usage.total_tokens)

                content = response.choices[0].message.content
                return content.strip() if content else self.get_fallback_response(agent_name, "Empty response from API")

            except APIError as e:
                logger.warning(f"OpenAI API error on attempt {attempt + 1} for {agent_name}: {e}")
                if attempt == self.max_retries - 1:
                    return self.get_fallback_response(agent_name, str(e))
                await asyncio.sleep(2 ** attempt) # Exponential backoff
            except Exception as e:
                logger.error(f"An unexpected error occurred in LLM service for {agent_name}: {e}", exc_info=True)
                return self.get_fallback_response(agent_name, str(e))

        # This line should ideally not be reached if the loop handles all cases
        return self.get_fallback_response(agent_name, "Max retries exceeded without specific error.")

# Singleton instance to be used across the application
llm_service = None

def get_llm_service():
    """
    Returns the singleton instance of the LLMService, creating it if necessary.
    """
    global llm_service
    if llm_service is None:
        llm_service = LLMService()
    return llm_service
