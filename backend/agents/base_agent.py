from backend.services.llm_service import llm_service
import controlflow as cf

class BaseAgent:
    """
    A helper class for agents to interact with the LLM.
    
    This class is not a ControlFlow agent itself. Instead, it's a tool that
    ControlFlow tasks can use to get structured responses from an LLM based on a
    pre-defined persona or system prompt.
    """
    def __init__(self, system_prompt: str):
        """
        Initializes the BaseAgent with a specific system prompt.
        
        Args:
            system_prompt: The persona, instructions, or context for the agent.
        """
        self.system_prompt = system_prompt
        # The logger is now retrieved from the ControlFlow context within the task
        # self.logger = cf.get_run_logger()

    def execute(self, user_prompt: str) -> str:
        """
        Executes a query against the LLM with the agent's system prompt.

        Args:
            user_prompt: The specific query or task for this execution.

        Returns:
            The response from the LLM.
        """
        # The logger should be retrieved from the context where the task is running
        try:
            logger = cf.get_run_logger()
            logger.info(f"Executing with system prompt: '{self.system_prompt[:50]}...'")
            logger.info(f"User prompt: '{user_prompt[:50]}...'")
        except Exception:
            # If not in a run context, just print
            print("Logger not found. Not in a ControlFlow run context.")


        # In the future, we can construct a more complex prompt with message history
        full_prompt = f"{self.system_prompt}\n\nUser query: {user_prompt}"
        
        response = llm_service.generate_response(prompt=full_prompt)
        
        return response
