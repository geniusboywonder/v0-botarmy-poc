import os
import asyncio
import logging
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError

logger = logging.getLogger(__name__)

class LLMService:
    """
    A centralized service to handle all interactions with LLM providers.
    This service is responsible for making API calls and managing API keys.
    """
    def __init__(self):
        self.is_test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key and not self.is_test_mode:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None # No model in test mode without key
        self.max_retries = 3
        self.timeout_seconds = 60

    async def generate_response(self, prompt: str, agent_name: str) -> str:
        """
        Asynchronously generates a response from the LLM, with retries.
        """
        if self.is_test_mode:
            return "Mocked LLM Result"

        for attempt in range(self.max_retries):
            try:
                # Note: The Google AI Python SDK does not currently support async operations out-of-the-box.
                # We run the synchronous SDK call in a separate thread to avoid blocking the asyncio event loop.
                response = await asyncio.to_thread(
                    self.model.generate_content,
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        # candidate_count=1, # Only one candidate is supported
                        # stop_sequences=['...'],
                        # max_output_tokens=2048,
                        temperature=0.7,
                    ),
                    # request_options={'timeout': self.timeout_seconds} # Specify timeout
                )

                if response.parts:
                    return response.text.strip()
                else:
                    # Handle cases where the response is empty or blocked
                    # See: https://ai.google.dev/docs/troubleshooting#safety-settings
                    logger.warning(f"Gemini API returned an empty response for {agent_name}. This could be due to safety settings or other content filters.")
                    # Re-raising as a specific error to be handled by the workflow
                    raise GoogleAPICallError("The LLM API returned an empty or blocked response. Please check the prompt or safety settings.")


            except GoogleAPICallError as e:
                logger.warning(f"Google AI API error on attempt {attempt + 1} for {agent_name}: {e}")
                if attempt == self.max_retries - 1:
                    # After the last retry, re-raise the exception to be caught by the global error handler
                    raise e
                await asyncio.sleep(2 ** attempt) # Exponential backoff
            except Exception as e:
                logger.error(f"An unexpected error occurred in LLM service for {agent_name}: {e}", exc_info=True)
                # Re-raise the exception to be caught by the global error handler
                raise e

        # This part should not be reached if the loop is correct
        raise Exception("Max retries exceeded without a successful response.")


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
