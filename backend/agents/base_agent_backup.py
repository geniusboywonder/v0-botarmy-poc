"""
Adaptive base agent that works in both development and Replit environments.
Supports multiple LLM providers and ControlFlow integration.
"""

import asyncio
import logging
from typing import Any, Dict, Optional
import google.generativeai as genai
import os

from backend.runtime_env import IS_REPLIT, get_environment_info

logger = logging.getLogger(__name__)

class LightweightAgent:
    """Lightweight agent implementation for fallback scenarios."""
<<<<<<< HEAD
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature/add-test-framework
=======
    
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    def __init__(self, system_prompt: str, agent_name: str = "Agent"):
        self.system_prompt = system_prompt
        self.agent_name = agent_name
        self.model = None
        self._setup_llm()
<<<<<<< HEAD
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature/add-test-framework
=======
    
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    def _setup_llm(self):
        """Setup the LLM client."""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment")
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info(f"Gemini model configured for {self.agent_name}")
            
        except Exception as e:
            logger.error(f"Failed to setup LLM for {self.agent_name}: {e}")
            raise
    
<<<<<<< HEAD
=======

            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info(f"Gemini model configured for {self.agent_name}")

        except Exception as e:
            logger.error(f"Failed to setup LLM for {self.agent_name}: {e}")
            raise

>>>>>>> origin/feature/add-test-framework
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    async def execute(self, user_prompt: str, **kwargs) -> str:
        """Execute the agent task with the given prompt."""
        try:
            # Combine system prompt and user prompt
            full_prompt = f"""System Instructions: {self.system_prompt}

User Request: {user_prompt}

Please provide a detailed response following the system instructions."""

            logger.info(f"{self.agent_name} processing request...")
<<<<<<< HEAD
<<<<<<< HEAD
            
=======

>>>>>>> origin/feature/add-test-framework
=======
            
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            # Generate response using Gemini
            response = await asyncio.to_thread(
                self.model.generate_content, full_prompt
            )
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            
            result = response.text
            logger.info(f"{self.agent_name} completed task")
            
            return result
            
<<<<<<< HEAD
=======

            result = response.text
            logger.info(f"{self.agent_name} completed task")

            return result

>>>>>>> origin/feature/add-test-framework
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
        except Exception as e:
            logger.error(f"{self.agent_name} failed: {e}")
            # Return a fallback response instead of crashing
            return f"⚠️ {self.agent_name} encountered an issue: {str(e)}. Please try again or contact support."

class BaseAgent:
    """
    Adaptive base agent that works in both development and Replit environments.
<<<<<<< HEAD
<<<<<<< HEAD
    
=======

>>>>>>> origin/feature/add-test-framework
=======
    
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    This class is not a ControlFlow agent itself. Instead, it's a tool that
    ControlFlow tasks can use to get structured responses from an LLM based on a
    pre-defined persona or system prompt.
    """
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
    
    def __init__(self, system_prompt: str, status_broadcaster=None):
        """
        Initializes the BaseAgent with a specific system prompt.
        
<<<<<<< HEAD
=======

    def __init__(self, system_prompt: str, status_broadcaster=None):
        """
        Initializes the BaseAgent with a specific system prompt.

>>>>>>> origin/feature/add-test-framework
=======
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
        Args:
            system_prompt: The persona, instructions, or context for the agent.
            status_broadcaster: An instance of AgentStatusBroadcaster to send progress updates.
        """
        self.system_prompt = system_prompt
        self.status_broadcaster = status_broadcaster
        self.is_replit_mode = IS_REPLIT
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> origin/feature/add-test-framework
=======
        
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
        if self.is_replit_mode:
            logger.info("Using Replit-compatible agent implementation")
        else:
            logger.info("Using full-featured agent implementation")

    async def execute(self, user_prompt: str, agent_name: str = "BaseAgent", session_id: str = "global") -> str:
        """
        Executes a query against the LLM with the agent's system prompt.

        Args:
            user_prompt: The specific query or task for this execution.
            agent_name: The name of the calling agent, for logging and fallbacks.
            session_id: Session identifier for status broadcasting.

        Returns:
            The response from the LLM.
        """
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> origin/feature/add-test-framework
=======
        
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
        # Try to get ControlFlow logger first
        try:
            import controlflow as cf
            logger = cf.get_run_logger()
            logger.info(f"Agent '{agent_name}' is thinking...")
        except Exception:
            # If not in a run context, use standard logger
            logger.info(f"Agent '{agent_name}' is thinking... (standard mode)")

        # Broadcast status if available
        if self.status_broadcaster:
            await self.status_broadcaster.broadcast_agent_progress(agent_name, "Initializing", 1, 4, session_id)
            await asyncio.sleep(0.1)

        try:
            # Try to use LLM service if available
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(agent_name, "Querying LLM", 3, 4, session_id)
<<<<<<< HEAD
<<<<<<< HEAD
            
=======

>>>>>>> origin/feature/add-test-framework
=======
            
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            try:
                from backend.services.llm_service import get_llm_service
                full_prompt = f"{self.system_prompt}\n\nUser query: {user_prompt}"
                llm_service = get_llm_service()
                response = await llm_service.generate_response(prompt=full_prompt, agent_name=agent_name)
            except ImportError:
                # Fallback to lightweight agent
                logger.info(f"LLM service not available, using lightweight agent for {agent_name}")
                lightweight_agent = LightweightAgent(self.system_prompt, agent_name)
                response = await lightweight_agent.execute(user_prompt)
<<<<<<< HEAD
<<<<<<< HEAD
            
=======

>>>>>>> origin/feature/add-test-framework
=======
            
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(agent_name, "Processing response", 4, 4, session_id)
                await asyncio.sleep(0.1)

            return response
<<<<<<< HEAD
<<<<<<< HEAD
            
=======

>>>>>>> origin/feature/add-test-framework
=======
            
>>>>>>> 888a13e8888c2a85282e3309ece813befd8c920e
        except Exception as e:
            logger.error(f"Agent {agent_name} failed: {e}")
            # Return a fallback response
            return f"⚠️ Agent {agent_name} encountered an issue: {str(e)}. Using fallback response."