"""
Deployer Agent with proper logging and 1-LLM-call safety limit.
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

_deployer_call_count = 0
MAX_LLM_CALLS = 1

DEPLOYER_SYSTEM_PROMPT = """
You are a world-class DevOps engineer AI. Your goal is to take testing strategies 
and create deployment plans and infrastructure recommendations.

The document should include:
1. **Deployment Strategy:** Recommended deployment approach
2. **Infrastructure:** Server and hosting requirements
3. **CI/CD Pipeline:** Automated deployment process
4. **Monitoring:** Health checks and monitoring setup

Produce the output in Markdown format. Keep the response under 500 words.
"""

def should_be_interactive() -> bool:
    hitl_enabled = os.getenv("ENABLE_HITL", "true").lower() == "true"
    auto_action = os.getenv("AUTO_ACTION", "none").lower()
    return hitl_enabled and auto_action == "none" and not IS_REPLIT

@cf.task(interactive=should_be_interactive())
async def run_deployer_task(testing_doc: str, status_broadcaster: AgentStatusBroadcaster, session_id: str, artifact_preferences: dict) -> str:
    """Deployer Agent task with proper logging and 1-LLM-call safety limit."""
    global _deployer_call_count
    
    if IS_REPLIT:
        current_logger = logger
        current_logger.info(f"🚀 Starting Deployer Agent (Replit mode)")
    else:
        try:
            current_logger = prefect.get_run_logger()
        except:
            current_logger = logger
        current_logger.info(f"🚀 Starting Deployer Agent (Development mode)")

    input_preview = testing_doc[:200] + "..." if len(testing_doc) > 200 else testing_doc
    current_logger.info(f"📝 INPUT RECEIVED: '{input_preview}'")
    current_logger.info(f"📊 Agent call count: {_deployer_call_count}/{MAX_LLM_CALLS}")

    if _deployer_call_count >= MAX_LLM_CALLS:
        current_logger.warning(f"🚨 SAFETY LIMIT REACHED: Deployer has made {_deployer_call_count} LLM calls.")
        return f"""# Deployment Plan - Safety Limit Reached

## Deployment Overview
⚠️ **Safety Limit Active**: This agent has reached its maximum LLM call limit ({MAX_LLM_CALLS} calls).

## Status
✅ Task completed (safety mode)
🏁 Workflow complete - all agents finished

---
*Safety limit: {_deployer_call_count}/{MAX_LLM_CALLS} calls made*"""

    _deployer_call_count += 1
    current_logger.info(f"🚀 Making LLM call #{_deployer_call_count}")

    current_logger.info("🤖 Creating BaseAgent with system prompt...")
    deployer_agent = BaseAgent(system_prompt=DEPLOYER_SYSTEM_PROMPT)
    
    try:
        if not artifact_preferences.get("deploy-scripts", True):
            logger.info("Skipping deployment script generation as per user preference.")
            return "Deployment script generation skipped by user."

        await status_broadcaster.broadcast_agent_response(
            agent_name="Deployer",
            content="Querying LLM to create a deployment plan...",
            session_id=session_id,
        )
        current_logger.info("📡 Calling LLM for deployment plan...")
        deployment_doc = await deployer_agent.execute(
            user_prompt=f"Create deployment plan for:\n{testing_doc}", 
            agent_name="Deployer"
        )
        
        output_preview = deployment_doc[:200] + "..." if len(deployment_doc) > 200 else deployment_doc
        current_logger.info(f"✅ LLM RESPONSE RECEIVED (preview): {output_preview}")
        await status_broadcaster.broadcast_agent_response(
            agent_name="Deployer",
            content=f"Received deployment plan from LLM. Preview: {output_preview}",
            session_id=session_id,
        )
        current_logger.info(f"📏 Full response length: {len(deployment_doc)} characters")
        current_logger.info("🎯 Deployer Agent completed successfully")
        current_logger.info("🏁 WORKFLOW COMPLETE - All agents finished!")
        
        return deployment_doc
        
    except Exception as e:
        error_msg = f"Deployer Agent failed: {str(e)}"
        current_logger.error(f"❌ LLM CALL FAILED: {error_msg}")
        await status_broadcaster.broadcast_agent_response(
            agent_name="Deployer",
            content=f"Error during deployment planning: {error_msg}",
            session_id=session_id,
        )
        
        return f"""# Deployment Plan - Error Recovery

## Deployment Overview
⚠️ The automated deployment planning encountered an issue: {str(e)}

## Status
❌ LLM call failed
🏁 Workflow complete - all agents attempted

---
*Error: {str(e)}*"""

def reset_deployer_call_count():
    global _deployer_call_count
    _deployer_call_count = 0
    logger.info(f"🔄 Deployer call counter reset to 0")

def get_deployer_call_count():
    return _deployer_call_count
