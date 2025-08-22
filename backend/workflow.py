"""
Adaptive workflow that works in both development and Vercel environments.
Uses ControlFlow + Prefect in development, lightweight alternatives in Vercel.
"""

import asyncio
import logging
from typing import Dict, Any

from backend.runtime_env import get_controlflow, get_prefect, IS_VERCEL

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

# Define the sequence of agent tasks
AGENT_TASKS = [
    {"name": "Analyst", "task_func": run_analyst_task, "description": "Analyzing project brief and creating requirements."},
    {"name": "Architect", "task_func": run_architect_task, "description": "Designing technical architecture."},
    {"name": "Developer", "task_func": run_developer_task, "description": "Writing application code."},
    {"name": "Tester", "task_func": run_tester_task, "description": "Creating a test plan."},
    {"name": "Deployer", "task_func": run_deployer_task, "description": "Generating deployment script."},
]

@prefect.flow(name="BotArmy SDLC Workflow")
async def botarmy_workflow(project_brief: str, session_id: str) -> Dict[str, Any]:
    """
    Adaptive workflow that runs the full agent pipeline.
    Works in both development (with ControlFlow/Prefect) and Vercel (lightweight).
    """
    
    if IS_VERCEL:
        logger.info("Running workflow in Vercel mode (lightweight)")
    else:
        logger.info("Running workflow in development mode (full featured)")
    
    results = {}
    current_input = project_brief

    for agent_info in AGENT_TASKS:
        agent_name = agent_info["name"]
        task_func = agent_info["task_func"]
        description = agent_info["description"]

        try:
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
