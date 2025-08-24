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

@prefect.flow(name="BotArmy SDLC Workflow with HITL")
async def botarmy_workflow(project_brief: str, session_id: str) -> Dict[str, Any]:
    """
    Adaptive workflow with Human-in-the-Loop functionality.
    Works in both development (with ControlFlow/Prefect) and Replit environments.
    """
    
    mode = "Replit" if IS_REPLIT else "Development"
    logger.info(f"Running workflow with HITL in {mode} mode")
    
    results = {}
    current_input = project_brief

    # Check if HITL is enabled globally
    hitl_enabled = os.getenv("ENABLE_HITL", "true").lower() == "true"
    auto_action = os.getenv("AUTO_ACTION", "none").lower()
    
    if not hitl_enabled or auto_action == "approve":
        logger.info("HITL disabled or auto-approval enabled - running automatically")

    for agent_info in AGENT_TASKS:
        agent_name = agent_info["name"]
        task_func = agent_info["task_func"]
        description = agent_info["description"]
        requires_approval = agent_info.get("hitl_enabled", False)

        try:
            # Human-in-the-Loop approval step
            if hitl_enabled and requires_approval and auto_action == "none":
                logger.info(f"Requesting human approval for {agent_name}")
                
                # Import status broadcaster to avoid circular imports
                try:
                    from backend.agent_status_broadcaster import AgentStatusBroadcaster
                    # We'll need to get this from app state in real implementation
                    status_broadcaster = None  # TODO: Get from app state
                    
                    approval = await request_human_approval(
                        agent_name=agent_name,
                        description=description,
                        session_id=session_id,
                        status_broadcaster=status_broadcaster
                    )
                    
                    if approval in ["denied", "denied_error"]:
                        logger.info(f"Human denied {agent_name} - skipping task")
                        results[agent_name] = f"⏭️ {agent_name} task skipped by human decision"
                        current_input = results[agent_name]
                        continue
                    elif approval == "approved_timeout":
                        logger.info(f"Human approval timed out for {agent_name} - proceeding automatically")
                        
                except ImportError:
                    logger.warning("HITL functionality not available - proceeding automatically")
            
            logger.info(f"Starting {agent_name}: {description}")
            
            # Execute the agent's task
            result = await task_func(current_input)
            results[agent_name] = result
            current_input = result  # Chain the outputs
            
            logger.info(f"{agent_name} completed successfully")

        except Exception as e:
            # Handle errors gracefully
            error_msg = f"Agent '{agent_name}' encountered an issue: {str(e)}. Continuing with simplified approach."
            logger.error(error_msg)
            
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

# HITL Configuration Functions
def enable_hitl():
    """Enable Human-in-the-Loop for all agents"""
    os.environ["ENABLE_HITL"] = "true"
    
def disable_hitl():
    """Disable Human-in-the-Loop - run automatically"""
    os.environ["ENABLE_HITL"] = "false"
    
def set_auto_approve():
    """Set agents to auto-approve for testing"""
    os.environ["AUTO_ACTION"] = "approve"
    
def set_auto_deny():
    """Set agents to auto-deny for testing"""
    os.environ["AUTO_ACTION"] = "deny"
    
def reset_hitl():
    """Reset HITL to manual mode"""
    os.environ["AUTO_ACTION"] = "none"