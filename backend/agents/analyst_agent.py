import controlflow as cf
from backend.agents.base_agent import BaseAgent

# Define the persona and instructions for the Analyst Agent
ANALYST_SYSTEM_PROMPT = """
You are a world-class business analyst AI. Your goal is to take a high-level
project brief and transform it into a detailed, structured requirements document.

The document should include:
1.  **Executive Summary:** A brief overview of the project.
2.  **User Stories:** A list of user stories in the format "As a [user type], I want [an action] so that [a benefit]."
3.  **Functional Requirements:** A numbered list of specific, testable functional requirements.
4.  **Non-Functional Requirements:** A numbered list of non-functional requirements (e.g., performance, security, scalability).

Produce the output in Markdown format.
"""

@cf.task(interactive=True)
async def run_analyst_task(project_brief: str) -> str:
    """
    This ControlFlow task runs the Analyst Agent to generate a requirements
    document from a project brief.

    Args:
        project_brief: A string containing the high-level project description.

    Returns:
        A string containing the formatted requirements document.
    """
    logger = cf.get_run_logger()
    logger.info(f"Starting Analyst Agent task for brief: '{project_brief[:50]}...'")

    # Create an instance of our BaseAgent with the analyst persona
    analyst_agent = BaseAgent(system_prompt=ANALYST_SYSTEM_PROMPT)

    # Execute the analysis
    requirements_document = await analyst_agent.execute(user_prompt=project_brief, agent_name="Analyst")

    logger.info("Analyst Agent task completed.")

    return requirements_document
