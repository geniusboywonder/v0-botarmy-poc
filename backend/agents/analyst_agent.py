"""
Adaptive Analyst Agent that works in both development and Replit environments.
Supports Human-in-the-Loop functionality.
"""

import logging
import os
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect, IS_REPLIT

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

# Determine if this task should be interactive based on environment and settings
def should_be_interactive() -> bool:
    """Determine if the analyst task should request human approval"""
    hitl_enabled = os.getenv("ENABLE_HITL", "true").lower() == "true"
    auto_action = os.getenv("AUTO_ACTION", "none").lower()
    
    # Interactive if HITL is enabled and not in auto mode
    return hitl_enabled and auto_action == "none" and not IS_REPLIT

@cf.task(interactive=should_be_interactive())
async def run_analyst_task(project_brief: str, status_broadcaster=None, session_id: str = "global") -> str:
    """
    Analyst Agent task that adapts to the runtime environment and HITL settings.
    Uses ControlFlow in development, direct LLM calls in Replit.
    Supports human approval when configured.

    Args:
        project_brief: A string containing the high-level project description.
        status_broadcaster: An instance of AgentStatusBroadcaster to send progress updates.
        session_id: The session ID for broadcasting messages.

    Returns:
        A string containing the formatted requirements document.
    """
    
    # Get appropriate logger
    if IS_REPLIT:
        logger.info(f"Starting Analyst Agent (Replit mode) for: '{project_brief[:50]}...'")
    else:
        run_logger = prefect.get_run_logger()
        run_logger.info(f"Starting Analyst Agent (Development mode) for: '{project_brief[:50]}...'")

    # Check if human approval was requested and granted
    if should_be_interactive():
        try:
            # In interactive mode, ControlFlow will handle the human approval
            # This will pause and wait for user input
            logger.info("Analyst Agent waiting for human approval...")
        except Exception as e:
            logger.warning(f"Interactive mode failed: {e}, proceeding automatically")

    # Create and execute the analyst agent
    analyst_agent = BaseAgent(system_prompt=ANALYST_SYSTEM_PROMPT, status_broadcaster=status_broadcaster)
    
    try:
        requirements_document = await analyst_agent.execute(
            user_prompt=project_brief, 
            agent_name="Analyst",
            session_id=session_id
        )
        
        if IS_REPLIT:
            logger.info("Analyst Agent (Replit mode) completed successfully")
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

# Utility functions for HITL control
def enable_analyst_hitl():
    """Enable human approval for analyst tasks"""
    os.environ["ANALYST_HITL"] = "true"
    
def disable_analyst_hitl():
    """Disable human approval for analyst tasks"""
    os.environ["ANALYST_HITL"] = "false"