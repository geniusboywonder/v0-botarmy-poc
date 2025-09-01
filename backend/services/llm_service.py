import os
import asyncio
import logging
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError
from backend.rate_limiter import rate_limiter, rate_limited

# Optional imports for multi-provider support
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

logger = logging.getLogger(__name__)

class LLMService:
    """
    Enhanced centralized service to handle all interactions with multiple LLM providers.
    Includes rate limiting, fallback providers, and cost tracking.
    """
    def __init__(self):
        self.max_retries = 3
        self.timeout_seconds = 60
        
        # Initialize providers
        self.providers = {}
        self._setup_providers()
        
        # Default provider order (can be customized)
        self.provider_priority = ['google', 'openai', 'anthropic']
        
    def _setup_providers(self):
        """Setup available LLM providers"""
        
        # Import dynamic config for test mode check
        from backend.dynamic_config import get_dynamic_config
        config = get_dynamic_config()
        is_test_mode = config.get("TEST_MODE", False, "boolean")
        
        # Google AI (Gemini)
        google_key = os.getenv("GOOGLE_AI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if google_key and not is_test_mode:
            try:
                genai.configure(api_key=google_key)
                self.providers['google'] = {
                    'client': genai.GenerativeModel('gemini-pro'),
                    'type': 'google',
                    'available': True
                }
                logger.info("Google AI provider configured")
            except Exception as e:
                logger.warning(f"Failed to configure Google AI: {e}")
        
        # OpenAI
        if HAS_OPENAI and os.getenv("OPENAI_API_KEY") and not is_test_mode:
            try:
                self.providers['openai'] = {
                    'client': openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")),
                    'type': 'openai',
                    'available': True
                }
                logger.info("OpenAI provider configured")
            except Exception as e:
                logger.warning(f"Failed to configure OpenAI: {e}")
        
        # Anthropic
        if HAS_ANTHROPIC and os.getenv("ANTHROPIC_API_KEY") and not is_test_mode:
            try:
                self.providers['anthropic'] = {
                    'client': anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY")),
                    'type': 'anthropic',
                    'available': True
                }
                logger.info("Anthropic provider configured")
            except Exception as e:
                logger.warning(f"Failed to configure Anthropic: {e}")
        
        if not self.providers and not is_test_mode:
            logger.warning("No LLM providers configured. Check your API keys.")

    def estimate_tokens(self, prompt: str) -> int:
        """Rough estimation of tokens (4 chars = 1 token)"""
        return len(prompt) // 4 + 100  # Add buffer for response

    async def _call_google(self, client, prompt: str) -> str:
        """Call Google AI API"""
        response = await asyncio.to_thread(
            client.generate_content,
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
            ),
        )
        
        if response.parts:
            return response.text.strip()
        else:
            raise GoogleAPICallError("Empty response from Google AI")

    async def _call_openai(self, client, prompt: str) -> str:
        """Call OpenAI API"""
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            timeout=self.timeout_seconds
        )
        return response.choices[0].message.content.strip()

    async def _call_anthropic(self, client, prompt: str) -> str:
        """Call Anthropic API"""
        response = await client.messages.create(
            model="claude-3-haiku-20240307",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            timeout=self.timeout_seconds
        )
        return response.content[0].text.strip()

    @rate_limited("google", estimated_tokens=1500)
    async def _generate_with_google(self, prompt: str) -> str:
        """Generate response using Google AI with rate limiting"""
        provider = self.providers['google']
        return await self._call_google(provider['client'], prompt)

    @rate_limited("openai", estimated_tokens=1500)
    async def _generate_with_openai(self, prompt: str) -> str:
        """Generate response using OpenAI with rate limiting"""
        provider = self.providers['openai']
        return await self._call_openai(provider['client'], prompt)

    @rate_limited("anthropic", estimated_tokens=1500)
    async def _generate_with_anthropic(self, prompt: str) -> str:
        """Generate response using Anthropic with rate limiting"""
        provider = self.providers['anthropic']
        return await self._call_anthropic(provider['client'], prompt)

    async def generate_response(self, prompt: str, agent_name: str, preferred_provider: str = None) -> str:
        """
        Generate response with automatic provider fallback and rate limiting.
        """
        # Check test mode dynamically
        from backend.dynamic_config import get_dynamic_config
        config = get_dynamic_config()
        if config.get("TEST_MODE", False, "boolean"):
            return f"Mocked LLM Result for {agent_name}"

        # Determine provider order
        if preferred_provider and preferred_provider in self.providers:
            providers_to_try = [preferred_provider] + [p for p in self.provider_priority if p != preferred_provider]
        else:
            providers_to_try = self.provider_priority

        # Filter to only available providers
        providers_to_try = [p for p in providers_to_try if p in self.providers and self.providers[p]['available']]

        if not providers_to_try:
            raise Exception("No LLM providers available")

        last_error = None
        
        for provider_name in providers_to_try:
            try:
                logger.info(f"Attempting {provider_name} for {agent_name}")
                
                if provider_name == 'google':
                    result = await self._generate_with_google(prompt)
                elif provider_name == 'openai':
                    result = await self._generate_with_openai(prompt)
                elif provider_name == 'anthropic':
                    result = await self._generate_with_anthropic(prompt)
                else:
                    continue
                
                logger.info(f"Successfully used {provider_name} for {agent_name}")
                return result
                
            except Exception as e:
                last_error = e
                logger.warning(f"Provider {provider_name} failed for {agent_name}: {e}")
                
                # Mark provider as temporarily unavailable if it's a rate limit
                if "rate limit" in str(e).lower():
                    logger.warning(f"Rate limit hit for {provider_name}, trying next provider")
                
                # If this was the last provider, don't continue
                if provider_name == providers_to_try[-1]:
                    break
                
                # Wait a bit before trying next provider
                await asyncio.sleep(1)

        # If we get here, all providers failed
        error_msg = f"All LLM providers failed for {agent_name}. Last error: {last_error}"
        logger.error(error_msg)
        raise Exception(error_msg)

    def get_provider_status(self) -> dict:
        """Get status of all providers"""
        status = {}
        for name, provider in self.providers.items():
            status[name] = {
                'available': provider['available'],
                'type': provider['type'],
                'rate_limit_status': rate_limiter.get_status(name)
            }
        return status

    def get_available_providers(self) -> list:
        """Get list of available provider names"""
        return [name for name, provider in self.providers.items() if provider['available']]

    async def health_check(self) -> dict:
        """Check health of all providers"""
        health = {}
        
        for provider_name in self.providers.keys():
            try:
                test_prompt = "Hello, respond with 'OK'"
                await self.generate_response(test_prompt, f"health_check_{provider_name}", provider_name)
                health[provider_name] = "healthy"
            except Exception as e:
                health[provider_name] = f"unhealthy: {str(e)}"
        
        return health


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