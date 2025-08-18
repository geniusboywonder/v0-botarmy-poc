"""
LLM Integration for BotArmy Agents
Provides standardized LLM access and configuration
"""

import openai
import os
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMConfig:
    """Configuration for LLM integration"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("LLM_MODEL", "gpt-4")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2000"))
        
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
    
    def get_client(self) -> openai.OpenAI:
        """Get configured OpenAI client"""
        return openai.OpenAI(api_key=self.openai_api_key)

class LLMService:
    """Service for LLM interactions"""
    
    def __init__(self, config: LLMConfig = None):
        self.config = config or LLMConfig()
        self.client = self.config.get_client() if self.config.openai_api_key else None
    
    async def generate_response(self, prompt: str, system_message: str = None, 
                              context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response using LLM"""
        if not self.client:
            return {
                "success": False,
                "error": "LLM client not configured - missing API key",
                "mock_response": f"Mock response for: {prompt[:100]}..."
            }
        
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            if context:
                context_str = f"Context: {context}\n\n"
                prompt = context_str + prompt
            
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.acreate(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "model": self.config.model,
                "timestamp": datetime.now().isoformat(),
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "mock_response": f"Error occurred, mock response for: {prompt[:100]}..."
            }
    
    async def stream_response(self, prompt: str, system_message: str = None) -> Any:
        """Stream response from LLM"""
        if not self.client:
            yield {"error": "LLM client not configured"}
            return
        
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            stream = await self.client.chat.completions.acreate(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield {
                        "content": chunk.choices[0].delta.content,
                        "timestamp": datetime.now().isoformat()
                    }
                    
        except Exception as e:
            logger.error(f"LLM streaming error: {e}")
            yield {"error": str(e)}

# Global LLM service instance
llm_service = LLMService()
