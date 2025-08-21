import controlflow as cf
from backend.agents.base_agent import BaseAgent

# Define the persona and instructions for the Developer Agent
DEVELOPER_SYSTEM_PROMPT = """
You are an expert AI software developer. Your goal is to take a technical
architecture specification and write the main application code.

You should:
1.  **Choose a language and framework** appropriate for the task (default to Python with FastAPI if not specified).
2.  **Write the code** for the main application logic.
3.  **Structure the code** logically in a single file for this POC.
4.  **Include comments** to explain key parts of the code.

Produce only the raw code as your output, enclosed in a single markdown code block.
"""

@cf.task
async def run_developer_task(architecture_document: str) -> str:
    """
    This ControlFlow task runs the Developer Agent to write code from a
    technical design document.

    Args:
        architecture_document: A string containing the technical design.

    Returns:
        A string containing the generated code.
    """
    logger = cf.get_run_logger()
    logger.info(f"Starting Developer Agent task...")

    # Create an instance of our BaseAgent with the developer persona
    developer_agent = BaseAgent(system_prompt=DEVELOPER_SYSTEM_PROMPT)

    # Execute the code generation
    generated_code = await developer_agent.execute(user_prompt=architecture_document, agent_name="Developer")

    logger.info("Developer Agent task completed.")

    return generated_code
