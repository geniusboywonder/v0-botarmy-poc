"""
Adaptive workflow that works in both development and Replit environments.
Uses ControlFlow + Prefect with Human-in-the-Loop functionality.
"""

import asyncio
import logging
import os
from typing import Dict, Any

from backend.runtime_env import get_controlflow, get_prefect, IS_REPLIT
from backend.human_input_handler import request_human_approval

# Import the agent tasks
from backend.agents.analyst_agent import run_analyst_task
from backend.agents.architect_agent import run_architect_task  
from backend.agents.developer_agent import run_developer_task
from backend.agents.tester_agent import run_tester_task
from backend.agents.deployer_agent import run_deployer_task

logger = logging.getLogger(__name__)

# Get appropriate modules based on environment
cf = get_controlflow()
prefect = get_prefect()

# Define the sequence of agent tasks with HITL support
AGENT_TASKS = [
    {
        "name": "Analyst", 
        "task_func": run_analyst_task, 
        "description": "Analyzing project brief and creating requirements.",
        "hitl_enabled": True  # Human approval required
    },
    {
        "name": "Architect", 
        "task_func": run_architect_task, 
        "description": "Designing technical architecture.",
        "hitl_enabled": True  # Human approval required
    },
    {
        "name": "Developer", 
        "task_func": run_developer_task, 
        "description": "Writing application code.",
        "hitl_enabled": False  # Auto-proceed for faster development
    },
    {
        "name": "Tester", 
        "task_func": run_tester_task, 
        "description": "Creating a test plan.",
        "hitl_enabled": False  # Auto-proceed for faster development
    },
    {
        "name": "Deployer", 
        "task_func": run_deployer_task, 
        "description": "Generating deployment script.",
        "hitl_enabled": True  # Human approval for deployment
    },
]

from backend.agent_status_broadcaster import AgentStatusBroadcaster

from backend.services.role_enforcer import RoleEnforcer

@prefect.flow(name="BotArmy SDLC Workflow with HITL")
async def botarmy_workflow(project_brief: str, session_id: str, status_broadcaster: AgentStatusBroadcaster, agent_pause_states: Dict[str, bool], artifact_preferences: Dict[str, bool], role_enforcer: RoleEnforcer) -> Dict[str, Any]:
    """
    Adaptive workflow with Human-in-the-Loop functionality.
    Works in both development (with ControlFlow/Prefect) and Replit environments.
    """
    
    mode = "Replit" if IS_REPLIT else "Development"
    logger.info(f"Running workflow with HITL in {mode} mode")
    
    results = {}
    current_input = project_brief

    # Check if HITL is enabled globally using dynamic config
    from backend.dynamic_config import get_dynamic_config
    config = get_dynamic_config()
    hitl_enabled = config.is_hitl_enabled()
    auto_action = config.get_auto_action()
    
    if not hitl_enabled or auto_action == "approve":
        logger.info("HITL disabled or auto-approval enabled - running automatically")

    for i, agent_info in enumerate(AGENT_TASKS):
        agent_name = agent_info["name"]

        # Pause check with safety limit to prevent infinite loops
        pause_check_count = 0
        max_pause_checks = 30  # 30 seconds max wait
        while agent_pause_states.get(agent_name, False):
            logger.info(f"Agent {agent_name} is paused. Waiting... ({pause_check_count + 1}/{max_pause_checks})")
            await asyncio.sleep(1)
            pause_check_count += 1
            if pause_check_count >= max_pause_checks:
                logger.warning(f"Agent {agent_name} pause check timed out - proceeding anyway")
                break

        task_func = agent_info["task_func"]
        description = agent_info["description"]
        requires_approval = agent_info.get("hitl_enabled", False)

        # Broadcast progress update
        if status_broadcaster:
            await status_broadcaster.broadcast_agent_progress(
                agent_name=agent_name,
                stage=f"Starting {agent_name}",
                current=i + 1,
                total=len(AGENT_TASKS),
                session_id=session_id,
            )

        try:
            # Human-in-the-Loop approval step
            if hitl_enabled and requires_approval and auto_action == "none":
                logger.info(f"Requesting human approval for {agent_name}")
                
                approval = await request_human_approval(
                    agent_name=agent_name,
                    description=description,
                    session_id=session_id,
                    status_broadcaster=status_broadcaster
                )

                if approval in ["denied", "denied_error"]:
                    logger.info(f"Human denied {agent_name} - skipping task")
                    results[agent_name] = f"⏭️ {agent_name} task skipped by human decision"
                    await status_broadcaster.broadcast_agent_response(
                        agent_name="System",
                        content=f"Skipping {agent_name} task due to human decision.",
                        session_id=session_id,
                    )
                    current_input = results[agent_name]
                    continue
                elif approval == "approved_timeout":
                    logger.info(f"Human approval timed out for {agent_name} - proceeding automatically")
            
            logger.info(f"Starting {agent_name}: {description}")
            await status_broadcaster.broadcast_agent_response(
                agent_name="System",
                content=f"Starting {agent_name} task: {description}",
                session_id=session_id,
            )
            
            # Execute the agent's task
            result = await task_func(
                current_input,
                status_broadcaster=status_broadcaster,
                session_id=session_id,
                artifact_preferences=artifact_preferences,
                role_enforcer=role_enforcer,
                agent_name=agent_name
            )
            results[agent_name] = result
            current_input = result  # Chain the outputs
            
            logger.info(f"{agent_name} completed successfully")
            await status_broadcaster.broadcast_agent_response(
                agent_name="System",
                content=f"✅ {agent_name} task completed.",
                session_id=session_id,
            )

        except Exception as e:
            # Handle errors gracefully
            error_msg = f"Agent '{agent_name}' encountered an issue: {str(e)}. Continuing with simplified approach."
            logger.error(error_msg)
            await status_broadcaster.broadcast_agent_response(
                agent_name="System",
                content=f"❌ Error in {agent_name} task: {e}",
                session_id=session_id,
            )
            
            results[agent_name] = error_msg
            current_input = results[agent_name]
            continue

    logger.info(f"Workflow completed with {len(results)} agent results")
    return results

async def simple_workflow(project_brief: str, session_id: str) -> Dict[str, Any]:
    """
    Simplified workflow for cases where full workflow isn't available.
    This provides basic functionality as a fallback.
    """
    
    logger.info("Running simplified workflow")
    
    try:
        # Just run a basic analysis using the analyst agent
        result = await run_analyst_task(project_brief)
        
        return {
            "Analyst": result,
            "status": "simplified_workflow_completed",
            "message": "Simplified workflow completed. For full functionality, use local development environment."
        }
        
    except Exception as e:
        logger.error(f"Simplified workflow failed: {e}")
        return {
            "error": str(e),
            "status": "workflow_failed",
            "message": "Workflow execution failed. Please check logs and try again."
        }

# HITL Configuration Functions now use dynamic config service
# Settings are managed through the settings page API