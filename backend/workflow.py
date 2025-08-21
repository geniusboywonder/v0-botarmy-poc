import asyncio
from prefect import flow, task
from backend.human_input_handler import request_human_approval
from backend.agent_status_broadcaster import AgentStatusBroadcaster
from backend.agents.analyst_agent import run_analyst_task
from backend.agents.architect_agent import run_architect_task
from backend.agents.developer_agent import run_developer_task
from backend.agents.tester_agent import run_tester_task
from backend.agents.deployer_agent import run_deployer_task

async def handle_agent_run(agent_name, agent_task, status_broadcaster, *args, **kwargs):
    """
    Handles running an agent task, including getting human approval.
    """
    approval_status, human_input = await request_human_approval(agent_name, status_broadcaster)

    if approval_status == "approved":
        await status_broadcaster.broadcast_agent_started(agent_name)
        result = await agent_task.submit(*args, **kwargs)
        await status_broadcaster.broadcast_agent_completed(agent_name)
        return {"approval_status": "approved", "result": result.result()}
    else:
        return {"approval_status": "denied", "output": "Task skipped because it was denied by the user."}

@flow(name="BotArmy Workflow")
async def botarmy_workflow(project_brief: str, session_id: str, status_broadcaster: AgentStatusBroadcaster):
    """
    The main workflow for the BotArmy application.
    """
    previous_results = {}

    # Analyst
    analyst_result = await handle_agent_run("Analyst", run_analyst_task, status_broadcaster, project_brief, previous_results)
    previous_results["analyst"] = analyst_result

    # Architect
    architect_result = await handle_agent_run("Architect", run_architect_task, status_broadcaster, project_brief, previous_results)
    previous_results["architect"] = architect_result

    # Developer
    developer_result = await handle_agent_run("Developer", run_developer_task, status_broadcaster, project_brief, previous_results)
    previous_results["developer"] = developer_result

    # Tester
    tester_result = await handle_agent_run("Tester", run_tester_task, status_broadcaster, project_brief, previous_results)
    previous_results["tester"] = tester_result

    # Deployer
    deployer_result = await handle_agent_run("Deployer", run_deployer_task, status_broadcaster, project_brief, previous_results)
    previous_results["deployer"] = deployer_result

    return previous_results
