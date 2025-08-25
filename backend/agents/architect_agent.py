"""
Architect Agent with proper logging and 1-LLM-call safety limit.
"""

import asyncio
import logging
import os
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect, IS_REPLIT

# Get appropriate modules based on environment
cf = get_controlflow()
prefect = get_prefect()

logger = logging.getLogger(__name__)

# Safety counter to prevent infinite loops
_architect_call_count = 0
MAX_LLM_CALLS = 1

ARCHITECT_SYSTEM_PROMPT = """
You are a world-class technical architect AI. Your goal is to take requirements 
and create a clear technical architecture and design approach.

The document should include:
1. **Technical Stack:** Recommended technologies and frameworks
2. **System Architecture:** High-level system design  
3. **Data Design:** Database and data storage approach
4. **API Design:** Key endpoints and interfaces
5. **Security Considerations:** Basic security requirements

Produce the output in Markdown format. Keep the response under 500 words.
"""

def should_be_interactive() -> bool:
    """Determine if the architect task should request human approval"""
    hitl_enabled = os.getenv("ENABLE_HITL", "true").lower() == "true"
    auto_action = os.getenv("AUTO_ACTION", "none").lower()
    return hitl_enabled and auto_action == "none" and not IS_REPLIT

@cf.task(interactive=should_be_interactive())
async def run_architect_task(requirements_doc: str) -> str:
    """
    Architect Agent task with proper logging and 1-LLM-call safety limit.
    """
    global _architect_call_count
    
    # Get appropriate logger
    if IS_REPLIT:
        current_logger = logger
        current_logger.info(f"🏗️ Starting Architect Agent (Replit mode)")
    else:
        try:
            current_logger = prefect.get_run_logger()
        except:
            current_logger = logger
        current_logger.info(f"🏗️ Starting Architect Agent (Development mode)")

    # Log the input
    input_preview = requirements_doc[:200] + "..." if len(requirements_doc) > 200 else requirements_doc
    current_logger.info(f"📝 INPUT RECEIVED: '{input_preview}'")
    current_logger.info(f"📊 Agent call count: {_architect_call_count}/{MAX_LLM_CALLS}")

    # Safety check - prevent infinite loops
    if _architect_call_count >= MAX_LLM_CALLS:
        current_logger.warning(f"🚨 SAFETY LIMIT REACHED: Architect has made {_architect_call_count} LLM calls. Returning fallback.")
        return f"""# Technical Architecture - Safety Limit Reached

## System Overview
⚠️ **Safety Limit Active**: This agent has reached its maximum LLM call limit ({MAX_LLM_CALLS} calls) to prevent infinite loops.

## Architecture Response
The architect agent acknowledges the requirements and is ready to proceed to the development phase.

## Status
✅ Task completed (safety mode)
🔄 Ready to hand off to Developer Agent

---
*Safety limit: {_architect_call_count}/{MAX_LLM_CALLS} calls made*"""

    # Increment call counter
    _architect_call_count += 1
    current_logger.info(f"🚀 Making LLM call #{_architect_call_count}")

    # Create and execute the architect agent
    current_logger.info("🤖 Creating BaseAgent with system prompt...")
    architect_agent = BaseAgent(system_prompt=ARCHITECT_SYSTEM_PROMPT)
    
    try:
        current_logger.info("📡 Calling LLM for architecture design...")
        architecture_doc = await architect_agent.execute(
            user_prompt=f"Create technical architecture for:\n{requirements_doc}", 
            agent_name="Architect"
        )
        
        # Log the output (truncated for readability)
        output_preview = architecture_doc[:200] + "..." if len(architecture_doc) > 200 else architecture_doc
        current_logger.info(f"✅ LLM RESPONSE RECEIVED (preview): {output_preview}")
        current_logger.info(f"📏 Full response length: {len(architecture_doc)} characters")
        current_logger.info("🎯 Architect Agent completed successfully")
        
        return architecture_doc
        
    except Exception as e:
        error_msg = f"Architect Agent failed: {str(e)}"
        current_logger.error(f"❌ LLM CALL FAILED: {error_msg}")
        
        return f"""# Technical Architecture - Error Recovery

## System Overview
⚠️ The automated architecture design encountered an issue: {str(e)}

## Status
❌ LLM call failed
🔄 Ready to hand off to Developer Agent

---
*Error: {str(e)}*"""

def reset_architect_call_count():
    """Reset the call counter (for testing)"""
    global _architect_call_count
    _architect_call_count = 0
    logger.info(f"🔄 Architect call counter reset to 0")

def get_architect_call_count():
    """Get current call count"""
    return _architect_call_count
