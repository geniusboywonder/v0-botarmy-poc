import controlflow as cf
from prefect import flow

# Import the real agent tasks
from backend.agents.analyst_agent import run_analyst_task
from backend.agents.architect_agent import run_architect_task
from backend.agents.developer_agent import run_developer_task
from backend.agents.tester_agent import run_tester_task
from backend.agents.deployer_agent import run_deployer_task

@flow(name="BotArmy SDLC Workflow")
def botarmy_workflow(project_brief: str):
    """
    Defines the main end-to-end workflow for the BotArmy product generation.
    """
    # Chain the tasks together to define the sequence of operations.
    # The output of one task becomes the input for the next.
    requirements = run_analyst_task(project_brief)
    architecture = run_architect_task(requirements)
    code = run_developer_task(architecture)
    test_plan = run_tester_task(code)
    deployment_script = run_deployer_task(test_plan) # The input should be the tested code, but for now we pass the plan

    return deployment_script
