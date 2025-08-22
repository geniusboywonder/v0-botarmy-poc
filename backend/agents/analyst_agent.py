"""
Adaptive Analyst Agent that works in both development and Vercel environments.
"""

import logging
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect, IS_VERCEL

# Get appropriate modules based on environment
cf = get_controlflow()
prefect = get_prefect()

logger = logging.getLogger(__name__)

# Define the persona and instructions for the Analyst Agent
ANALYST_SYSTEM_PROMPT = """
You are a world-class business analyst AI. Your goal is to take a high-level
project brief and transform it into a detailed, structured requirements document.

The document should include:
1. **Executive Summary:** A brief overview of the project.
2. **User Stories:** A list of user stories in the format "As a [user type], I want [an action] so that [a benefit]."
3. **Functional Requirements:** A numbered list of specific, testable functional requirements.
4. **Non-Functional Requirements:** A numbered list of non-functional requirements (e.g., performance, security, scalability).

Produce the output in Markdown format.
"""

@cf.task(interactive=True)
async def run_analyst_task(project_brief: str) -> str:
    """
    Analyst Agent task that adapts to the runtime environment.
    Uses ControlFlow in development, direct LLM calls in Vercel.

    Args:
        project_brief: A string containing the high-level project description.

    Returns:
        A string containing the formatted requirements document.
    """
    
    # Get appropriate logger
    if IS_VERCEL:
        logger.info(f"Starting Analyst Agent (Vercel mode) for: '{project_brief[:50]}...'")
    else:
        run_logger = prefect.get_run_logger()
        run_logger.info(f"Starting Analyst Agent (Development mode) for: '{project_brief[:50]}...'")

    # Create and execute the analyst agent
    analyst_agent = BaseAgent(system_prompt=ANALYST_SYSTEM_PROMPT)
    
    try:
        requirements_document = await analyst_agent.execute(
            user_prompt=project_brief, 
            agent_name="Analyst"
        )
        
        if IS_VERCEL:
            logger.info("Analyst Agent (Vercel mode) completed successfully")
        else:
            run_logger.info("Analyst Agent (Development mode) completed successfully")
        
        return requirements_document
        
    except Exception as e:
        error_msg = f"Analyst Agent failed: {str(e)}"
        logger.error(error_msg)
        
        # Return a fallback response instead of crashing
        return f"""# Requirements Analysis - Error Recovery

## Executive Summary
⚠️ The automated analysis encountered an issue: {str(e)}

## Manual Analysis Required
Based on the project brief: "{project_brief[:100]}..."

Please provide:
1. Detailed user stories
2. Functional requirements
3. Non-functional requirements
4. Technical constraints

## Next Steps
- Review the project brief manually
- Consult with stakeholders
- Create detailed requirements document
"""
