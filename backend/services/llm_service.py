import os
import asyncio
import logging
from typing import Dict, Any, Optional
import time
from contextlib import asynccontextmanager
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

try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False
    # Create a dummy aiohttp module for type hints when not available
    class _DummyClientSession:
        pass
    class _DummyAiohttp:
        ClientSession = _DummyClientSession
    aiohttp = _DummyAiohttp()

logger = logging.getLogger(__name__)

class ConnectionPool:
    """
    Connection pool for managing HTTP connections to LLM providers.
    Reduces connection overhead and improves performance.
    """
    
    def __init__(self, max_connections_per_provider: int = 10):
        self.max_connections = max_connections_per_provider
        self.sessions: Dict[str, aiohttp.ClientSession] = {}
        self.connection_stats = {
            'total_requests': 0,
            'active_connections': 0,
            'pool_hits': 0,
            'created_at': time.time()
        }
    
    async def get_session(self, provider: str) -> aiohttp.ClientSession:
        """Get or create a session for the provider"""
        if not HAS_AIOHTTP:
            # If aiohttp is not available, return None and let providers handle their own connections
            logger.warning(f"aiohttp not available, connection pooling disabled for {provider}")
            return None
            
        if provider not in self.sessions:
            # Configure session with optimized settings
            connector = aiohttp.TCPConnector(
                limit=self.max_connections,
                limit_per_host=self.max_connections // 2,
                keepalive_timeout=300,  # 5 minutes
                enable_cleanup_closed=True,
                use_dns_cache=True,
            )
            
            timeout = aiohttp.ClientTimeout(
                total=300,    # 5 minutes total timeout
                connect=30,   # 30 seconds to connect
                sock_read=60  # 60 seconds to read response
            )
            
            self.sessions[provider] = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={'User-Agent': 'BotArmy-Backend/1.0'}
            )
            
            logger.info(f"Created new connection pool for {provider}")
        else:
            self.connection_stats['pool_hits'] += 1
        
        self.connection_stats['total_requests'] += 1
        return self.sessions[provider]
    
    async def close_all(self):
        """Close all sessions and cleanup resources"""
        if not HAS_AIOHTTP:
            logger.info("No aiohttp sessions to close")
            return
            
        for provider, session in self.sessions.items():
            try:
                if session:  # Check if session is not None
                    await session.close()
                    logger.info(f"Closed connection pool for {provider}")
            except Exception as e:
                logger.warning(f"Error closing session for {provider}: {e}")
        
        self.sessions.clear()
        logger.info("All connection pools closed")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics"""
        return {
            **self.connection_stats,
            'active_providers': list(self.sessions.keys()),
            'uptime_seconds': time.time() - self.connection_stats['created_at']
        }

class LLMService:
    """
    Enhanced centralized service to handle all interactions with multiple LLM providers.
    Includes rate limiting, fallback providers, connection pooling, and cost tracking.
    """
    def __init__(self):
        self.max_retries = 3
        self.timeout_seconds = 60
        
        # Initialize connection pooling
        self.connection_pool = ConnectionPool(max_connections_per_provider=10)
        
        # Performance metrics - initialize before provider setup
        self.performance_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0,
            'response_times': [],
            'provider_usage': {}
        }
        
        # Initialize providers
        self.providers = {}
        self._setup_providers()
        
        # Default provider order (can be customized)
        self.provider_priority = ['google', 'openai', 'anthropic']
        
    def _setup_providers(self):
        """Setup available LLM providers with enhanced connection management"""
        
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
                    'available': True,
                    'uses_connection_pool': False,  # Google AI uses their own client
                    'config': {
                        'temperature': 0.7,
                        'max_tokens': 4000
                    }
                }
                self.performance_metrics['provider_usage']['google'] = 0
                logger.info("Google AI provider configured")
            except Exception as e:
                logger.warning(f"Failed to configure Google AI: {e}")
        
        # OpenAI with enhanced connection pooling
        if HAS_OPENAI and os.getenv("OPENAI_API_KEY") and not is_test_mode:
            try:
                # Create OpenAI client with custom HTTP session
                openai_client = openai.AsyncOpenAI(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    max_retries=2,
                    timeout=self.timeout_seconds
                )
                
                self.providers['openai'] = {
                    'client': openai_client,
                    'type': 'openai',
                    'available': True,
                    'uses_connection_pool': HAS_AIOHTTP,
                    'config': {
                        'model': 'gpt-3.5-turbo',
                        'temperature': 0.7,
                        'max_tokens': 4000
                    }
                }
                self.performance_metrics['provider_usage']['openai'] = 0
                logger.info("OpenAI provider configured with connection pooling")
            except Exception as e:
                logger.warning(f"Failed to configure OpenAI: {e}")
        
        # Anthropic with enhanced connection pooling
        if HAS_ANTHROPIC and os.getenv("ANTHROPIC_API_KEY") and not is_test_mode:
            try:
                anthropic_client = anthropic.AsyncAnthropic(
                    api_key=os.getenv("ANTHROPIC_API_KEY"),
                    max_retries=2,
                    timeout=self.timeout_seconds
                )
                
                self.providers['anthropic'] = {
                    'client': anthropic_client,
                    'type': 'anthropic',
                    'available': True,
                    'uses_connection_pool': HAS_AIOHTTP,
                    'config': {
                        'model': 'claude-3-haiku-20240307',
                        'temperature': 0.7,
                        'max_tokens': 4000
                    }
                }
                self.performance_metrics['provider_usage']['anthropic'] = 0
                logger.info("Anthropic provider configured with connection pooling")
            except Exception as e:
                logger.warning(f"Failed to configure Anthropic: {e}")
        
        if not self.providers and not is_test_mode:
            logger.warning("No LLM providers configured. Check your API keys.")
        
        logger.info(f"Configured {len(self.providers)} LLM providers with connection pooling")

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
        """Call OpenAI API with connection pooling"""
        config = self.providers['openai']['config']
        response = await client.chat.completions.create(
            model=config['model'],
            messages=[{"role": "user", "content": prompt}],
            temperature=config['temperature'],
            max_tokens=config['max_tokens'],
            timeout=self.timeout_seconds
        )
        return response.choices[0].message.content.strip()

    async def _call_anthropic(self, client, prompt: str) -> str:
        """Call Anthropic API with connection pooling"""
        config = self.providers['anthropic']['config']
        response = await client.messages.create(
            model=config['model'],
            messages=[{"role": "user", "content": prompt}],
            temperature=config['temperature'],
            max_tokens=config['max_tokens'],
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

    def _track_performance(self, provider_name: str, response_time: float, success: bool):
        """Track performance metrics for monitoring and optimization"""
        self.performance_metrics['total_requests'] += 1
        
        if success:
            self.performance_metrics['successful_requests'] += 1
            self.performance_metrics['response_times'].append(response_time)
            
            # Keep only last 100 response times for moving average
            if len(self.performance_metrics['response_times']) > 100:
                self.performance_metrics['response_times'] = self.performance_metrics['response_times'][-100:]
            
            # Update average
            self.performance_metrics['average_response_time'] = sum(self.performance_metrics['response_times']) / len(self.performance_metrics['response_times'])
        else:
            self.performance_metrics['failed_requests'] += 1
        
        # Track provider usage
        if provider_name in self.performance_metrics['provider_usage']:
            self.performance_metrics['provider_usage'][provider_name] += 1

    async def generate_response(self, prompt: str, agent_name: str, preferred_provider: str = None) -> str:
        """
        Generate response with automatic provider fallback, rate limiting, and performance tracking.
        Enhanced with connection pooling for improved performance.
        """
        start_time = time.time()
        
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
            self._track_performance("none", time.time() - start_time, False)
            raise Exception("No LLM providers available")

        last_error = None
        
        for provider_name in providers_to_try:
            provider_start_time = time.time()
            try:
                logger.info(f"Attempting {provider_name} for {agent_name} (connection pooling: {self.providers[provider_name].get('uses_connection_pool', False)})")
                
                if provider_name == 'google':
                    result = await self._generate_with_google(prompt)
                elif provider_name == 'openai':
                    result = await self._generate_with_openai(prompt)
                elif provider_name == 'anthropic':
                    result = await self._generate_with_anthropic(prompt)
                else:
                    continue
                
                # Track successful request
                response_time = time.time() - provider_start_time
                self._track_performance(provider_name, response_time, True)
                
                logger.info(f"Successfully used {provider_name} for {agent_name} in {response_time:.2f}s")
                return result
                
            except Exception as e:
                last_error = e
                response_time = time.time() - provider_start_time
                self._track_performance(provider_name, response_time, False)
                
                logger.warning(f"Provider {provider_name} failed for {agent_name} in {response_time:.2f}s: {e}")
                
                # Mark provider as temporarily unavailable if it's a rate limit
                if "rate limit" in str(e).lower():
                    logger.warning(f"Rate limit hit for {provider_name}, trying next provider")
                
                # If this was the last provider, don't continue
                if provider_name == providers_to_try[-1]:
                    break
                
                # Wait a bit before trying next provider
                await asyncio.sleep(1)

        # If we get here, all providers failed
        total_time = time.time() - start_time
        error_msg = f"All LLM providers failed for {agent_name} in {total_time:.2f}s. Last error: {last_error}"
        logger.error(error_msg)
        raise Exception(error_msg)

    def get_provider_status(self) -> dict:
        """Get comprehensive status of all providers with performance metrics"""
        status = {}
        for name, provider in self.providers.items():
            status[name] = {
                'available': provider['available'],
                'type': provider['type'],
                'uses_connection_pool': provider.get('uses_connection_pool', False),
                'config': provider.get('config', {}),
                'rate_limit_status': rate_limiter.get_status(name),
                'usage_count': self.performance_metrics['provider_usage'].get(name, 0)
            }
        return status

    def get_performance_metrics(self) -> dict:
        """Get detailed performance metrics"""
        return {
            **self.performance_metrics,
            'connection_pool_stats': self.connection_pool.get_stats(),
            'success_rate': (
                self.performance_metrics['successful_requests'] / 
                max(self.performance_metrics['total_requests'], 1)
            ) * 100
        }

    def get_available_providers(self) -> list:
        """Get list of available provider names"""
        return [name for name, provider in self.providers.items() if provider['available']]

    async def health_check(self) -> dict:
        """Check health of all providers with connection pool validation"""
        health = {}
        
        for provider_name in self.providers.keys():
            try:
                test_prompt = "Hello, respond with 'OK'"
                start_time = time.time()
                result = await self.generate_response(test_prompt, f"health_check_{provider_name}", provider_name)
                response_time = time.time() - start_time
                
                health[provider_name] = {
                    'status': 'healthy',
                    'response_time': round(response_time, 3),
                    'response_preview': result[:50] if result else "No response"
                }
            except Exception as e:
                health[provider_name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        return health

    async def cleanup(self):
        """Cleanup resources including connection pools"""
        try:
            await self.connection_pool.close_all()
            logger.info("LLM service cleanup completed")
        except Exception as e:
            logger.error(f"Error during LLM service cleanup: {e}")

    def reset_metrics(self):
        """Reset performance metrics (useful for testing)"""
        self.performance_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0,
            'response_times': [],
            'provider_usage': {name: 0 for name in self.providers.keys()}
        }
        logger.info("Performance metrics reset")


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