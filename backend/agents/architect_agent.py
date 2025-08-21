import controlflow as cf
from backend.agents.base_agent import BaseAgent

# Define the persona and instructions for the Architect Agent
ARCHITECT_SYSTEM_PROMPT = """
You are a master AI software architect. Your goal is to take a requirements
document and produce a high-level technical architecture specification.

The specification should include:
1.  **Technology Stack:** A list of recommended technologies (e.g., Frontend Framework, Backend Language, Database).
2.  **System Components:** A breakdown of the major components of the system (e.g., API Server, Database, Caching Layer, Frontend App).
3.  **Data Model:** A simple representation of the core data entities and their relationships.
4.  **API Endpoints:** A list of key API endpoints, including the HTTP method, path, and a brief description.

Produce the output in Markdown format. Be concise and clear.
"""

@cf.task
async def run_architect_task(requirements_document: str) -> str:
    """
    This ControlFlow task runs the Architect Agent to generate a technical
    design from a requirements document.

    Args:
        requirements_document: A string containing the requirements.

    Returns:
        A string containing the formatted technical design document.
    """
    logger = cf.get_run_logger()
    logger.info(f"Starting Architect Agent task...")

    # Create an instance of our BaseAgent with the architect persona
    architect_agent = BaseAgent(system_prompt=ARCHITECT_SYSTEM_PROMPT)

    # Execute the analysis
    technical_design = await architect_agent.execute(user_prompt=requirements_document, agent_name="Architect")

    logger.info("Architect Agent task completed.")

    return technical_design
