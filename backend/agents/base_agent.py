"""
Lightweight agent implementation for Vercel deployment.
Uses direct LLM calls instead of ControlFlow when heavy dependencies aren't available.
"""

import asyncio
import logging
from typing import Any, Dict, Optional
import google.generativeai as genai
import os

from backend.runtime_env import IS_VERCEL, get_environment_info

logger = logging.getLogger(__name__)

class VercelAgent:
    """Lightweight agent implementation for Vercel deployment."""
    
    def __init__(self, system_prompt: str, agent_name: str = "Agent"):
        self.system_prompt = system_prompt
        self.agent_name = agent_name
        self.model = None
        self._setup_llm()
    
    def _setup_llm(self):
        """Setup the LLM client."""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info(f"Gemini model configured for {self.agent_name}")
            
        except Exception as e:
            logger.error(f"Failed to setup LLM for {self.agent_name}: {e}")
            raise
    
    async def execute(self, user_prompt: str, **kwargs) -> str:
        """Execute the agent task with the given prompt."""
        try:
            # Combine system prompt and user prompt
            full_prompt = f"""System Instructions: {self.system_prompt}

User Request: {user_prompt}

Please provide a detailed response following the system instructions."""

            logger.info(f"{self.agent_name} processing request...")
            
            # Generate response using Gemini
            response = await asyncio.to_thread(
                self.model.generate_content, full_prompt
            )
            
            result = response.text
            logger.info(f"{self.agent_name} completed task")
            
            return result
            
        except Exception as e:
            logger.error(f"{self.agent_name} failed: {e}")
            # Return a fallback response instead of crashing
            return f"⚠️ {self.agent_name} encountered an issue: {str(e)}. Please try again or contact support."

class BaseAgent:
    """Adaptive base agent that works in both development and Vercel environments."""
    
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.is_vercel_mode = IS_VERCEL
        
        if self.is_vercel_mode:
            logger.info("Using Vercel-compatible agent implementation")
        else:
            logger.info("Using full-featured agent implementation")
    
    async def execute(self, user_prompt: str, agent_name: str = "Agent", **kwargs) -> str:
        """Execute the agent task, adapting to the current environment."""
        
        if self.is_vercel_mode:
            # Use lightweight Vercel implementation
            vercel_agent = VercelAgent(self.system_prompt, agent_name)
            return await vercel_agent.execute(user_prompt, **kwargs)
        else:
            # Use full ControlFlow implementation in development
            try:
                import controlflow as cf
                
                # Create ControlFlow agent
                agent = cf.Agent(
                    name=agent_name,
                    instructions=self.system_prompt
                )
                
                # Run the task
                result = await cf.run_async(
                    f"Process this request: {user_prompt}",
                    agents=[agent]
                )
                
                return str(result)
                
            except ImportError:
                logger.warning("ControlFlow not available, falling back to Vercel mode")
                # Fallback to Vercel implementation
                vercel_agent = VercelAgent(self.system_prompt, agent_name)
                return await vercel_agent.execute(user_prompt, **kwargs)
