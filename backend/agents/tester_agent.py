"""
Tester Agent with proper logging and 1-LLM-call safety limit.
"""

import asyncio
import logging
import os
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect, IS_REPLIT

cf = get_controlflow()
prefect = get_prefect()
logger = logging.getLogger(__name__)

_tester_call_count = 0
MAX_LLM_CALLS = 1

TESTER_SYSTEM_PROMPT = """
You are a world-class QA engineer AI. Your goal is to take implementation plans 
and create comprehensive testing strategies.

The document should include:
1. **Testing Strategy:** Overall approach to quality assurance
2. **Test Cases:** Key test scenarios to validate functionality  
3. **Test Data:** Sample data needed for testing
4. **Quality Metrics:** Success criteria and measurement approaches

Produce the output in Markdown format. Keep the response under 500 words.
"""

def should_be_interactive() -> bool:
    hitl_enabled = os.getenv("ENABLE_HITL", "true").lower() == "true"
    auto_action = os.getenv("AUTO_ACTION", "none").lower()
    return hitl_enabled and auto_action == "none" and not IS_REPLIT

@cf.task(interactive=should_be_interactive())
async def run_tester_task(implementation_doc: str) -> str:
    """Tester Agent task with proper logging and 1-LLM-call safety limit."""
    global _tester_call_count
    
    if IS_REPLIT:
        current_logger = logger
        current_logger.info(f"🧪 Starting Tester Agent (Replit mode)")
    else:
        try:
            current_logger = prefect.get_run_logger()
        except:
            current_logger = logger
        current_logger.info(f"🧪 Starting Tester Agent (Development mode)")

    input_preview = implementation_doc[:200] + "..." if len(implementation_doc) > 200 else implementation_doc
    current_logger.info(f"📝 INPUT RECEIVED: '{input_preview}'")
    current_logger.info(f"📊 Agent call count: {_tester_call_count}/{MAX_LLM_CALLS}")

    if _tester_call_count >= MAX_LLM_CALLS:
        current_logger.warning(f"🚨 SAFETY LIMIT REACHED: Tester has made {_tester_call_count} LLM calls.")
        return f"""# Testing Strategy - Safety Limit Reached

## Quality Assurance Overview
⚠️ **Safety Limit Active**: This agent has reached its maximum LLM call limit ({MAX_LLM_CALLS} calls).

## Status
✅ Task completed (safety mode)
🔄 Ready to hand off to Deployer Agent

---
*Safety limit: {_tester_call_count}/{MAX_LLM_CALLS} calls made*"""

    _tester_call_count += 1
    current_logger.info(f"🚀 Making LLM call #{_tester_call_count}")

    current_logger.info("🤖 Creating BaseAgent with system prompt...")
    tester_agent = BaseAgent(system_prompt=TESTER_SYSTEM_PROMPT)
    
    try:
        current_logger.info("📡 Calling LLM for testing strategy...")
        testing_doc = await tester_agent.execute(
            user_prompt=f"Create testing strategy for:\n{implementation_doc}", 
            agent_name="Tester"
        )
        
        output_preview = testing_doc[:200] + "..." if len(testing_doc) > 200 else testing_doc
        current_logger.info(f"✅ LLM RESPONSE RECEIVED (preview): {output_preview}")
        current_logger.info(f"📏 Full response length: {len(testing_doc)} characters")
        current_logger.info("🎯 Tester Agent completed successfully")
        
        return testing_doc
        
    except Exception as e:
        error_msg = f"Tester Agent failed: {str(e)}"
        current_logger.error(f"❌ LLM CALL FAILED: {error_msg}")
        
        return f"""# Testing Strategy - Error Recovery

## Quality Assurance Overview
⚠️ The automated testing strategy creation encountered an issue: {str(e)}

## Status
❌ LLM call failed
🔄 Ready to hand off to Deployer Agent

---
*Error: {str(e)}*"""

def reset_tester_call_count():
    global _tester_call_count
    _tester_call_count = 0
    logger.info(f"🔄 Tester call counter reset to 0")

def get_tester_call_count():
    return _tester_call_count
