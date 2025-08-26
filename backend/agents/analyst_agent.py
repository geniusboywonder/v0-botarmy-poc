"""
Analyst Agent with proper logging and 1-LLM-call safety limit.
"""

import asyncio
import logging
import os
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect, IS_REPLIT
from backend.agent_status_broadcaster import AgentStatusBroadcaster

# Get appropriate modules based on environment
cf = get_controlflow()
prefect = get_prefect()

logger = logging.getLogger(__name__)

# Safety counter to prevent infinite loops
_analyst_call_count = 0
MAX_LLM_CALLS = 1

# Define the persona and instructions for the Analyst Agent
ANALYST_SYSTEM_PROMPT = """
You are a world-class business analyst AI. Your goal is to take a high-level
project brief and transform it into a detailed, structured requirements document.

The document should include:
1. **Executive Summary:** A brief overview of the project.
2. **User Stories:** A list of user stories in the format "As a [user type], I want [an action] so that [a benefit]."
3. **Functional Requirements:** A numbered list of specific, testable functional requirements.
4. **Non-Functional Requirements:** A numbered list of non-functional requirements (e.g., performance, security, scalability).

Produce the output in Markdown format. Keep the response under 500 words.
"""

# Determine if this task should be interactive based on environment and settings
def should_be_interactive() -> bool:
    """Determine if the analyst task should request human approval"""
    hitl_enabled = os.getenv("ENABLE_HITL", "true").lower() == "true"
    auto_action = os.getenv("AUTO_ACTION", "none").lower()
    
    # Interactive if HITL is enabled and not in auto mode
    return hitl_enabled and auto_action == "none" and not IS_REPLIT

@cf.task(interactive=should_be_interactive())
async def run_analyst_task(project_brief: str, status_broadcaster: AgentStatusBroadcaster, session_id: str, artifact_preferences: dict) -> str:
    """
    Analyst Agent task with proper logging and 1-LLM-call safety limit.

    Args:
        project_brief: A string containing the high-level project description.
        status_broadcaster: The broadcaster for sending status updates.
        session_id: The session ID for the current workflow.
        artifact_preferences: A dictionary of user preferences for artifacts.

    Returns:
        A string containing the formatted requirements document.
    """
    global _analyst_call_count
    
    # Get appropriate logger
    if IS_REPLIT:
        current_logger = logger
        current_logger.info(f"🔍 Starting Analyst Agent (Replit mode)")
    else:
        try:
            current_logger = prefect.get_run_logger()
        except:
            current_logger = logger
        current_logger.info(f"🔍 Starting Analyst Agent (Development mode)")

    # Log the input
    current_logger.info(f"📝 INPUT RECEIVED: '{project_brief}'")
    current_logger.info(f"📊 Agent call count: {_analyst_call_count}/{MAX_LLM_CALLS}")

    # Safety check - prevent infinite loops
    if _analyst_call_count >= MAX_LLM_CALLS:
        current_logger.warning(f"🚨 SAFETY LIMIT REACHED: Analyst has made {_analyst_call_count} LLM calls. Returning fallback.")
        return f"""# Requirements Analysis - Safety Limit Reached

## Executive Summary
⚠️ **Safety Limit Active**: This agent has reached its maximum LLM call limit ({MAX_LLM_CALLS} calls) to prevent infinite loops.

## Analysis Request
**Project Brief**: {project_brief}

## Safety Response
The analyst agent acknowledges the request and is ready to proceed to the architecture phase.

## Status
✅ Task completed (safety mode)
🔄 Ready to hand off to Architect Agent

---
*Safety limit: {_analyst_call_count}/{MAX_LLM_CALLS} calls made*"""

    # Increment call counter
    _analyst_call_count += 1
    current_logger.info(f"🚀 Making LLM call #{_analyst_call_count}")

    # Check if human approval was requested and granted
    if should_be_interactive():
        try:
            current_logger.info("👤 Analyst Agent waiting for human approval...")
        except Exception as e:
            current_logger.warning(f"Interactive mode failed: {e}, proceeding automatically")

    # Create and execute the analyst agent
    current_logger.info("🤖 Creating BaseAgent with system prompt...")
    analyst_agent = BaseAgent(system_prompt=ANALYST_SYSTEM_PROMPT)
    
    try:
        if not artifact_preferences.get("reqs-doc", True):
            logger.info("Skipping requirements document generation as per user preference.")
            return "Requirements document generation skipped by user."

        await status_broadcaster.broadcast_agent_response(
            agent_name="Analyst",
            content="Querying LLM to analyze project brief and create requirements document...",
            session_id=session_id,
        )
        current_logger.info("📡 Calling LLM for analysis...")
        requirements_document = await analyst_agent.execute(
            user_prompt=project_brief, 
            agent_name="Analyst"
        )
        
        # Log the output (truncated for readability)
        output_preview = requirements_document[:200] + "..." if len(requirements_document) > 200 else requirements_document
        current_logger.info(f"✅ LLM RESPONSE RECEIVED (preview): {output_preview}")
        await status_broadcaster.broadcast_agent_response(
            agent_name="Analyst",
            content=f"Received analysis from LLM. Preview: {output_preview}",
            session_id=session_id,
        )
        current_logger.info(f"📏 Full response length: {len(requirements_document)} characters")
        current_logger.info("🎯 Analyst Agent completed successfully")
        
        return requirements_document
        
    except Exception as e:
        error_msg = f"Analyst Agent failed: {str(e)}"
        current_logger.error(f"❌ LLM CALL FAILED: {error_msg}")
        await status_broadcaster.broadcast_agent_response(
            agent_name="Analyst",
            content=f"Error during analysis: {error_msg}",
            session_id=session_id,
        )
        
        # Return a fallback response instead of crashing
        return f"""# Requirements Analysis - Error Recovery

## Executive Summary
⚠️ The automated analysis encountered an issue: {str(e)}

## Analysis Request  
**Project Brief**: {project_brief}

## Manual Analysis Required
Based on the project brief, please provide:
1. Detailed user stories
2. Functional requirements
3. Non-functional requirements
4. Technical constraints

## Status
❌ LLM call failed
🔄 Ready to hand off to Architect Agent

---
*Error: {str(e)}*"""

# Utility functions for HITL control
def enable_analyst_hitl():
    """Enable human approval for analyst tasks"""
    os.environ["ANALYST_HITL"] = "true"
    
def disable_analyst_hitl():
    """Disable human approval for analyst tasks"""
    os.environ["ANALYST_HITL"] = "false"

def reset_analyst_call_count():
    """Reset the call counter (for testing)"""
    global _analyst_call_count
    _analyst_call_count = 0
    logger.info(f"🔄 Analyst call counter reset to 0")

def get_analyst_call_count():
    """Get current call count"""
    return _analyst_call_count
