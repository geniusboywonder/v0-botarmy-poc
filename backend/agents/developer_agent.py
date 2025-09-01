"""
Developer Agent with proper logging and 1-LLM-call safety limit.
"""

import asyncio
import logging
import os
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect, IS_REPLIT
from backend.agent_status_broadcaster import AgentStatusBroadcaster

cf = get_controlflow()
prefect = get_prefect()
logger = logging.getLogger(__name__)

_developer_call_count = 0
MAX_LLM_CALLS = 1

DEVELOPER_SYSTEM_PROMPT = """
You are a world-class software developer AI. Your goal is to take technical 
architecture and create implementation plans and code examples.

The document should include:
1. **Implementation Plan:** Step-by-step development approach
2. **Key Components:** Main modules and their responsibilities
3. **Code Examples:** Brief code snippets for critical functionality
4. **Development Notes:** Important implementation considerations

Produce the output in Markdown format. Keep the response under 500 words.
"""

def should_be_interactive() -> bool:
    hitl_enabled = os.getenv("ENABLE_HITL", "true").lower() == "true"
    auto_action = os.getenv("AUTO_ACTION", "none").lower()
    return hitl_enabled and auto_action == "none" and not IS_REPLIT

@cf.task(interactive=should_be_interactive())
async def run_developer_task(architecture_doc: str, status_broadcaster: AgentStatusBroadcaster, session_id: str, artifact_preferences: dict, role_enforcer=None, agent_name="Developer") -> str:
    """Developer Agent task with proper logging and 1-LLM-call safety limit."""
    if role_enforcer and not role_enforcer.validate_topic(agent_name, architecture_doc):
        message = role_enforcer.get_redirect_message(agent_name)
        if status_broadcaster:
            await status_broadcaster.broadcast_agent_response(
                agent_name=agent_name,
                content=message,
                session_id=session_id
            )
        return f"Task skipped due to off-topic input for {agent_name}."
    global _developer_call_count
    
    if IS_REPLIT:
        current_logger = logger
        current_logger.info(f"💻 Starting Developer Agent (Replit mode)")
    else:
        try:
            current_logger = prefect.get_run_logger()
        except:
            current_logger = logger
        current_logger.info(f"💻 Starting Developer Agent (Development mode)")

    input_preview = architecture_doc[:200] + "..." if len(architecture_doc) > 200 else architecture_doc
    current_logger.info(f"📝 INPUT RECEIVED: '{input_preview}'")
    current_logger.info(f"📊 Agent call count: {_developer_call_count}/{MAX_LLM_CALLS}")

    if _developer_call_count >= MAX_LLM_CALLS:
        current_logger.warning(f"🚨 SAFETY LIMIT REACHED: Developer has made {_developer_call_count} LLM calls.")
        return f"""# Implementation Plan - Safety Limit Reached

## Development Overview
⚠️ **Safety Limit Active**: This agent has reached its maximum LLM call limit ({MAX_LLM_CALLS} calls).

## Status
✅ Task completed (safety mode)
🔄 Ready to hand off to Tester Agent

---
*Safety limit: {_developer_call_count}/{MAX_LLM_CALLS} calls made*"""

    _developer_call_count += 1
    current_logger.info(f"🚀 Making LLM call #{_developer_call_count}")

    current_logger.info("🤖 Creating BaseAgent with system prompt...")
    developer_agent = BaseAgent(system_prompt=DEVELOPER_SYSTEM_PROMPT)
    
    try:
        if not artifact_preferences.get("source-code", True):
            logger.info("Skipping source code generation as per user preference.")
            return "Source code generation skipped by user."

        await status_broadcaster.broadcast_agent_response(
            agent_name="Developer",
            content="Querying LLM to create an implementation plan and code examples...",
            session_id=session_id,
        )
        current_logger.info("📡 Calling LLM for implementation plan...")
        implementation_doc = await developer_agent.execute(
            user_prompt=f"Create implementation plan for:\n{architecture_doc}", 
            agent_name="Developer"
        )
        
        output_preview = implementation_doc[:200] + "..." if len(implementation_doc) > 200 else implementation_doc
        current_logger.info(f"✅ LLM RESPONSE RECEIVED (preview): {output_preview}")
        await status_broadcaster.broadcast_agent_response(
            agent_name="Developer",
            content=f"Received implementation plan from LLM. Preview: {output_preview}",
            session_id=session_id,
        )
        current_logger.info(f"📏 Full response length: {len(implementation_doc)} characters")
        current_logger.info("🎯 Developer Agent completed successfully")
        
        return implementation_doc
        
    except Exception as e:
        error_msg = f"Developer Agent failed: {str(e)}"
        current_logger.error(f"❌ LLM CALL FAILED: {error_msg}")
        await status_broadcaster.broadcast_agent_response(
            agent_name="Developer",
            content=f"Error during implementation planning: {error_msg}",
            session_id=session_id,
        )
        
        return f"""# Implementation Plan - Error Recovery

## Development Overview
⚠️ The automated implementation planning encountered an issue: {str(e)}

## Status
❌ LLM call failed
🔄 Ready to hand off to Tester Agent

---
*Error: {str(e)}*"""

def reset_developer_call_count():
    global _developer_call_count
    _developer_call_count = 0
    logger.info(f"🔄 Developer call counter reset to 0")

def get_developer_call_count():
    return _developer_call_count
