import logging
from typing import Dict, Any
import asyncio

from backend.runtime_env import get_prefect
from backend.services.process_config_loader import get_process_config_loader
from backend.agents.generic_agent_executor import GenericAgentExecutor
from backend.agent_status_broadcaster import AgentStatusBroadcaster

prefect = get_prefect()
logger = logging.getLogger(__name__)

@prefect.flow(name="Generic BotArmy Workflow", persist_result=False, validate_parameters=False)
async def generic_workflow(
    config_name: str,
    initial_input: str,
    session_id: str,
    status_broadcaster: AgentStatusBroadcaster
) -> Dict[str, Any]:
    """
    A generic workflow orchestrator that executes processes based on a YAML configuration.

    Args:
        config_name (str): The name of the process configuration to load.
        initial_input (str): The initial input for the first task (e.g., a project brief).
        session_id (str): The session ID for the workflow.
        status_broadcaster (AgentStatusBroadcaster): The broadcaster for sending status updates.

    Returns:
        A dictionary containing the results and artifacts from the workflow execution.
    """
    logger.info(f"🚀 Starting generic workflow for process '{config_name}' with session ID '{session_id}'.")
    
    # Unwrap status_broadcaster if it's wrapped to prevent circular reference serialization
    if hasattr(status_broadcaster, 'get_wrapped_object'):
        status_broadcaster = status_broadcaster.get_wrapped_object()
        logger.info("Unwrapped status_broadcaster from serialization-safe wrapper")

    # 1. Load the process configuration
    config_loader = get_process_config_loader()
    try:
        config = config_loader.get_config(config_name)
        logger.info(f"Successfully loaded configuration for '{config['process_name']}'.")
    except Exception as e:
        logger.error(f"Failed to load process configuration '{config_name}': {e}")
        await status_broadcaster.broadcast_agent_response("System", f"Error: Could not load process config '{config_name}'.", session_id)
        return {"error": f"Failed to load process configuration: {e}"}

    # Workflow execution state
    artifacts = {"Project Brief": initial_input}
    results = {}

    # 2. Iterate through the defined stages in order
    # The order of stages is fixed for now, as in the original workflow.
    stage_order = ["Analyze", "Design", "Build", "Validate", "Launch"]

    for stage_name in stage_order:
        if stage_name not in config.get('stages', {}):
            continue

        stage_config = config['stages'][stage_name]
        logger.info(f"--- Entering Stage: {stage_name} ---")
        await status_broadcaster.broadcast_agent_response("System", f"Entering stage: {stage_name}", session_id)

        # This is a simplified linear execution of tasks within a stage.
        # A more advanced implementation would handle the dependency graph properly.
        for task_config in stage_config.get('tasks', []):
            task_name = task_config['name']
            role_name = task_config['role']

            logger.info(f"  - Starting Task: '{task_name}' with Role: '{role_name}'")

            # Find the full role configuration from the 'roles' list
            role_details = next((r for r in config['roles'] if r['name'] == role_name), None)
            if not role_details:
                logger.error(f"Role '{role_name}' not found in configuration. Skipping task '{task_name}'.")
                continue

            # 3. Instantiate the Generic Agent Executor
            agent_executor = GenericAgentExecutor(role_details, status_broadcaster)

            # 4. Prepare the context for the agent
            # This is a simplified context preparation. A real implementation would
            # load the content of all input_artifacts.
            input_artifacts = task_config.get('input_artifacts', [])
            context = "\n".join([artifacts.get(art, "") for art in input_artifacts])

            if not context:
                 logger.warning(f"Task '{task_name}' has no input context. The initial input will be used if it is the first task.")
                 if not artifacts: # if no artifacts produced yet.
                    context = initial_input


            # 5. Execute the task
            try:
                result = await agent_executor.execute_task(context, session_id)
                results[task_name] = result

                # 6. Store the output artifacts
                output_artifacts = task_config.get('output_artifacts', [])
                if output_artifacts:
                    # For simplicity, we'll store the entire result as the content of the first output artifact.
                    # Convert result to string to ensure it can be joined later.
                    artifacts[output_artifacts[0]] = str(result)
                    logger.info(f"    -> Produced artifact: '{output_artifacts[0]}'")

            except Exception as e:
                error_msg = f"Task '{task_name}' failed: {e}"
                logger.error(error_msg)
                results[task_name] = {"error": error_msg}
                # Decide if the workflow should continue or halt on error
                # For now, we'll just log and continue

    logger.info(f"🏁 Workflow '{config_name}' completed.")
    await status_broadcaster.broadcast_agent_response("System", f"Workflow '{config_name}' finished.", session_id)

    return {
        "results": results,
        "artifacts": artifacts
    }
