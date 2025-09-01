import logging
import asyncio
from backend.services.llm_service import get_llm_service
from backend.dynamic_config import get_dynamic_config

logger = logging.getLogger(__name__)

class GenericAgentExecutor:
    """
    A generic agent executor that can take on any role defined in a process configuration.
    """
    def __init__(self, role_config: dict, status_broadcaster=None):
        """
        Initializes the GenericAgentExecutor.

        Args:
            role_config (dict): A dictionary containing the role's configuration
                                (name, description, capabilities, etc.).
            status_broadcaster: An instance of AgentStatusBroadcaster for progress updates.
        """
        if not isinstance(role_config, dict) or 'name' not in role_config or 'description' not in role_config:
            raise ValueError("Invalid role_config provided. Must be a dict with 'name' and 'description'.")

        self.role_config = role_config
        self.agent_name = self.role_config['name']
        self.system_prompt = self.role_config['description']
        self.llm_service = get_llm_service()
        self.status_broadcaster = status_broadcaster
        # In the future, a tools_registry could be initialized here
        # self.capabilities = tools_registry.get_tools(self.role_config.get('capabilities', []))

    async def execute_task(self, context: str, session_id: str = "global") -> str:
        """
        Executes a task based on the provided context and the agent's role.
        This method is analogous to the `execute` method in the old BaseAgent.

        Args:
            context (str): The input or user prompt for the task.
            session_id (str): The session ID for broadcasting status updates.

        Returns:
            A string containing the result from the LLM.
        """
        config = get_dynamic_config()

        # Handle test modes similarly to BaseAgent for consistency
        if config.is_agent_test_mode():
            logger.info(f"🧪 {self.agent_name} in AGENT_TEST_MODE - returning static role confirmation")
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(self.agent_name, "Test mode", 1, 1, session_id)
            return f"🤖 **{self.agent_name} Agent - Test Mode**\n\n✅ **Role Confirmed**: {self.agent_name}"

        if config.is_role_test_mode():
            logger.info(f"🎯 {self.agent_name} in ROLE_TEST_MODE - performing role confirmation")
            # This mode could be simplified or adapted for the generic executor.
            # For now, we'll return a message indicating the mode.
            return f"🎯 **{self.agent_name} Agent - Role Test Mode**\n\n✅ Role confirmed via configuration."

        # Normal execution
        logger.info(f"🔥 {self.agent_name} in NORMAL_MODE - processing task.")
        if self.status_broadcaster:
            await self.status_broadcaster.broadcast_agent_progress(self.agent_name, "Initializing", 1, 3, session_id)

        try:
            full_prompt = f"{self.system_prompt}\n\nUser query: {context}"

            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(self.agent_name, "Querying LLM", 2, 3, session_id)

            response = await self.llm_service.generate_response(
                prompt=full_prompt,
                agent_name=self.agent_name
            )

            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_progress(self.agent_name, "Processing response", 3, 3, session_id)

            logger.info(f"✅ {self.agent_name} completed task successfully.")
            return response

        except Exception as e:
            logger.error(f"❌ Agent {self.agent_name} failed during task execution: {e}")
            if self.status_broadcaster:
                await self.status_broadcaster.broadcast_agent_response(
                    agent_name=self.agent_name,
                    content=f"Error during execution: {e}",
                    session_id=session_id,
                )
            # Provide a fallback response to prevent crashing the workflow
            return f"⚠️ Agent {self.agent_name} encountered an issue: {str(e)}. The workflow may be affected."
