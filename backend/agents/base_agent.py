"""
Adaptive base agent with TEST_MODE and ROLE_TEST_MODE brake functionality.
"""

import asyncio
import logging
from typing import Any, Dict, Optional
import google.generativeai as genai
import os

from backend.runtime_env import IS_REPLIT, get_environment_info

logger = logging.getLogger(__name__)

# Import dynamic config service
from backend.dynamic_config import get_dynamic_config

# Get config instance for dynamic reading
def get_current_test_modes():
    """Get current test modes dynamically."""
    config = get_dynamic_config()
    return {
        "agent_test_mode": config.is_agent_test_mode(),
        "role_test_mode": config.is_role_test_mode(),
        "any_test_mode": config.is_test_mode()
    }

class LightweightAgent:
    """Lightweight agent implementation for fallback scenarios."""
    
    def __init__(self, system_prompt: str, agent_name: str = "Agent"):
        self.system_prompt = system_prompt
        self.agent_name = agent_name
        self.model = None
        
        # Check test mode dynamically
        config = get_dynamic_config()
        if not config.is_test_mode():
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
        
        # Check test mode dynamically
        config = get_dynamic_config()
        
        # TEST MODE: Just return role confirmation
        if config.is_agent_test_mode():
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
    Adaptive base agent with TEST_MODE and ROLE_TEST_MODE brake functionality.
    
    - TEST_MODE: No LLM calls, returns static confirmations
    - ROLE_TEST_MODE: LLM calls only for role confirmation
    - Normal mode: Full LLM processing
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

    def _get_role_confirmation_prompt(self, agent_name: str, user_prompt: str) -> str:
        """Generate a role confirmation prompt for the LLM."""
        return f"""You are a {agent_name} agent. Please confirm your understanding of your role and acknowledge the instruction you've received.

Your role: {agent_name}
Instruction received: {user_prompt[:200]}{'...' if len(user_prompt) > 200 else ''}

Please respond in this exact format:
"I am the {agent_name} agent. I understand my role is to {self._get_role_description(agent_name)}. I acknowledge receiving the instruction about: [brief summary]. I am ready to proceed to the next agent."

Keep your response under 100 words."""

    def _get_role_description(self, agent_name: str) -> str:
        """Get a brief role description for each agent."""
        role_descriptions = {
            "Analyst": "gather requirements and analyze project needs",
            "Architect": "design system architecture and technical approach", 
            "Developer": "implement code and build the application",
            "Tester": "create tests and validate functionality",
            "Deployer": "handle deployment and infrastructure setup"
        }
        return role_descriptions.get(agent_name, "perform my assigned tasks")

    async def execute(self, user_prompt: str, agent_name: str = "BaseAgent", session_id: str = "global") -> str:
        """
        Executes a query against the LLM with the agent's system prompt.
        Behavior depends on current mode:
        - AGENT_TEST_MODE: Returns static confirmation
        - ROLE_TEST_MODE: Sends role confirmation to LLM
        - Normal: Full LLM processing
        """
        
        # Get dynamic configuration
        config = get_dynamic_config()
        
        # TEST MODE: Return simple static confirmation
        if config.is_agent_test_mode():
            logger.info(f"🧪 {agent_name} in AGENT_TEST_MODE - returning static role confirmation")
            
            # Still broadcast status for UI testing
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(agent_name, "Test mode", 1, 1, session_id)
                await asyncio.sleep(0.5)  # Brief pause for UI testing
            
            return f"""🤖 **{agent_name} Agent - Test Mode**

✅ **Role Confirmed**: {agent_name}
📝 **Instruction Received**: {user_prompt[:150]}{'...' if len(user_prompt) > 150 else ''}

⚙️ **Status**: Test mode active - no LLM processing
🧪 **Purpose**: Testing workflow and UI without LLM calls

To enable role confirmation with LLM:
- Set environment variable: `ROLE_TEST_MODE=true` and `AGENT_TEST_MODE=false`
- Restart the backend

---
*Agent role and instruction successfully received and acknowledged.*"""

        # ROLE TEST MODE: Send role confirmation to LLM
        if config.is_role_test_mode():
            logger.info(f"🎯 {agent_name} in ROLE_TEST_MODE - sending role confirmation to LLM")
            
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(agent_name, "Confirming role with LLM", 1, 2, session_id)

            try:
                # Use LLM service for role confirmation
                from backend.services.llm_service import get_llm_service
                role_prompt = self._get_role_confirmation_prompt(agent_name, user_prompt)
                llm_service = get_llm_service()
                
                if self.status_broadcaster:
                    await self.status_broadcaster.broadcast_agent_progress(agent_name, "Querying LLM", 2, 2, session_id)
                
                llm_response = await llm_service.generate_response(
                    prompt=role_prompt, 
                    agent_name=agent_name
                )
                
                logger.info(f"✅ {agent_name} received LLM role confirmation")
                
                return f"""🎯 **{agent_name} Agent - Role Test Mode**

🤖 **LLM Response**: 
{llm_response}

⚙️ **Status**: Role confirmed with real LLM - workflow can proceed
🔄 **Next**: Ready to hand off to next agent

To enable full agent functionality:
- Set environment variable: `AGENT_TEST_MODE=false` and `ROLE_TEST_MODE=false`
- Restart the backend

---
*Role confirmed via LLM - agent ready for next step.*"""
                
            except Exception as e:
                logger.error(f"🎯 {agent_name} role confirmation failed: {e}")
                return f"""🎯 **{agent_name} Agent - Role Test Mode (Error)**

❌ **LLM Role Confirmation Failed**: {str(e)}

📝 **Instruction Received**: {user_prompt[:150]}{'...' if len(user_prompt) > 150 else ''}

⚙️ **Status**: Could not confirm role with LLM
🔧 **Suggestion**: Check API keys and network connectivity

---
*Role confirmation failed - please check configuration.*"""
        
        # NORMAL MODE: Full LLM processing
        logger.info(f"🔥 {agent_name} in NORMAL_MODE - full LLM processing")
        
        # Try to get ControlFlow logger first
        try:
            import controlflow as cf
            run_logger = cf.get_run_logger()
            run_logger.info(f"Agent '{agent_name}' is thinking...")
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
    def get_current_mode():
        """Get the current agent mode"""
        config = get_dynamic_config()
        if config.is_agent_test_mode():
            return "AGENT_TEST_MODE"
        elif config.is_role_test_mode():
            return "ROLE_TEST_MODE" 
        else:
            return "NORMAL_MODE"
    
    @staticmethod
    def is_test_mode():
        """Check if any test mode is currently enabled"""
        config = get_dynamic_config()
        return config.is_test_mode()