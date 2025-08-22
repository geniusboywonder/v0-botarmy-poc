from backend.services.llm_service import get_llm_service
import controlflow as cf
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.connection_manager import EnhancedConnectionManager
import asyncio

class BaseAgent:
    """
    A helper class for agents to interact with the LLM.
    
    This class is not a ControlFlow agent itself. Instead, it's a tool that
    ControlFlow tasks can use to get structured responses from an LLM based on a
    pre-defined persona or system prompt.
    """
    def __init__(self, system_prompt: str, status_broadcaster: AgentStatusBroadcaster = None):
        """
        Initializes the BaseAgent with a specific system prompt.
        
        Args:
            system_prompt: The persona, instructions, or context for the agent.
            status_broadcaster: An instance of AgentStatusBroadcaster to send progress updates.
        """
        self.system_prompt = system_prompt
        self.status_broadcaster = status_broadcaster

    async def execute(self, user_prompt: str, agent_name: str = "BaseAgent", session_id: str = "global") -> str:
        """
        Executes a query against the LLM with the agent's system prompt.

        Args:
            user_prompt: The specific query or task for this execution.
            agent_name: The name of the calling agent, for logging and fallbacks.

        Returns:
            The response from the LLM.
        """
        # The logger should be retrieved from the context where the task is running
        try:
            logger = cf.get_run_logger()
            logger.info(f"Agent '{agent_name}' is thinking...")
        except Exception:
            # If not in a run context, just print
            print("Logger not found. Not in a ControlFlow run context.")


        if self.status_broadcaster:
            await self.status_broadcaster.broadcast_agent_progress(agent_name, "Initializing", 1, 4, session_id)
            await asyncio.sleep(0.1)

        # In the future, we can construct a more complex prompt with message history
        if self.status_broadcaster:
            await self.status_broadcaster.broadcast_agent_progress(agent_name, "Generating prompt", 2, 4, session_id)
            await asyncio.sleep(0.1)
        full_prompt = f"{self.system_prompt}\n\nUser query: {user_prompt}"
        
        if self.status_broadcaster:
            await self.status_broadcaster.broadcast_agent_progress(agent_name, "Querying LLM", 3, 4, session_id)
        llm_service = get_llm_service()
        response = await llm_service.generate_response(prompt=full_prompt, agent_name=agent_name)
        
        if self.status_broadcaster:
            await self.status_broadcaster.broadcast_agent_progress(agent_name, "Processing response", 4, 4, session_id)
            await asyncio.sleep(0.1)

        return response
