"""
Adaptive base agent with TEST_MODE brake functionality.
"""

import asyncio
import logging
from typing import Any, Dict, Optional
import google.generativeai as genai
import os

from backend.runtime_env import IS_REPLIT, get_environment_info

logger = logging.getLogger(__name__)

# Test mode flag - when enabled, agents only return role confirmations
TEST_MODE = os.getenv("AGENT_TEST_MODE", "false").lower() == "true"

class LightweightAgent:
    """Lightweight agent implementation for fallback scenarios."""
    
    def __init__(self, system_prompt: str, agent_name: str = "Agent"):
        self.system_prompt = system_prompt
        self.agent_name = agent_name
        self.model = None
        if not TEST_MODE:
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
        
        # TEST MODE: Just return role confirmation
        if TEST_MODE:
            return f"🤖 **{self.agent_name} Agent Test Mode**\n\n✅ Role confirmed: {self.agent_name}\n\n📝 Instruction received: {user_prompt[:100]}{'...' if len(user_prompt) > 100 else ''}\n\n⚙️ TEST_MODE: This agent is working in test mode. Real LLM processing is disabled.\n\nTo enable full agent functionality, set AGENT_TEST_MODE=false in your environment."
        
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
    """
    Adaptive base agent with TEST_MODE brake functionality.
    
    When TEST_MODE is enabled, agents return simple role confirmations instead of full LLM responses.
    This allows testing the workflow without consuming tokens or processing full responses.
    """
    
    def __init__(self, system_prompt: str, status_broadcaster=None):
        """
        Initializes the BaseAgent with a specific system prompt.
        
        Args:
            system_prompt: The persona, instructions, or context for the agent.
            status_broadcaster: An instance of AgentStatusBroadcaster to send progress updates.
        """
        self.system_prompt = system_prompt
        self.status_broadcaster = status_broadcaster
        self.is_replit_mode = IS_REPLIT
        
        if TEST_MODE:
            logger.info("🧪 TEST_MODE enabled - agents will return role confirmations only")
        elif self.is_replit_mode:
            logger.info("Using Replit-compatible agent implementation")
        else:
            logger.info("Using full-featured agent implementation")

    async def execute(self, user_prompt: str, agent_name: str = "BaseAgent", session_id: str = "global") -> str:
        """
        Executes a query against the LLM with the agent's system prompt.
        In TEST_MODE, returns a simple role confirmation instead.

        Args:
            user_prompt: The specific query or task for this execution.
            agent_name: The name of the calling agent, for logging and fallbacks.
            session_id: Session identifier for status broadcasting.

        Returns:
            The response from the LLM or a test confirmation.
        """
        
        # TEST MODE: Return simple role confirmation
        if TEST_MODE:
            logger.info(f"🧪 {agent_name} in TEST_MODE - returning role confirmation")
            
            # Still broadcast status for UI testing
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(agent_name, "Test mode", 1, 1, session_id)
                await asyncio.sleep(0.5)  # Brief pause for UI testing
            
            return f"""🤖 **{agent_name} Agent - Test Mode**

✅ **Role Confirmed**: {agent_name}
📝 **Instruction Received**: {user_prompt[:150]}{'...' if len(user_prompt) > 150 else ''}

⚙️ **Status**: Test mode active - no real LLM processing
🧪 **Purpose**: Testing workflow and UI without consuming tokens

To enable full functionality:
- Set environment variable: `AGENT_TEST_MODE=false`
- Restart the backend

---
*Agent role and instruction successfully received and acknowledged.*"""
        
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
            
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(agent_name, "Processing response", 4, 4, session_id)
                await asyncio.sleep(0.1)

            return response
            
        except Exception as e:
            logger.error(f"Agent {agent_name} failed: {e}")
            # Return a fallback response
            return f"⚠️ Agent {agent_name} encountered an issue: {str(e)}. Using fallback response."
    
    @staticmethod 
    def enable_test_mode():
        """Enable test mode for all agents"""
        os.environ["AGENT_TEST_MODE"] = "true"
        logger.info("🧪 Test mode ENABLED - agents will return role confirmations only")
    
    @staticmethod
    def disable_test_mode():
        """Disable test mode for all agents"""
        os.environ["AGENT_TEST_MODE"] = "false"
        logger.info("🔥 Test mode DISABLED - agents will use full LLM processing")
    
    @staticmethod
    def is_test_mode():
        """Check if test mode is currently enabled"""
        return TEST_MODE
