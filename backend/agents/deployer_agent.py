import controlflow as cf
from backend.agents.base_agent import BaseAgent

# Define the persona and instructions for the Deployer Agent
DEPLOYER_SYSTEM_PROMPT = """
You are a DevOps specialist AI. Your goal is to take a test plan and a piece of
code and create a simple deployment script.

You should:
1.  **Assume the tests have passed.**
2.  **Write a simple shell script** that would deploy the application (e.g., echo "Deploying...", copy files, restart server).
3.  **Keep the script very simple** for this POC.

Produce only the raw shell script as your output, enclosed in a single markdown code block.
"""

@cf.task
def run_deployer_task(test_plan: str) -> str:
    """
    This ControlFlow task runs the Deployer Agent to create a deployment script.

    Args:
        test_plan: A string containing the test plan.

    Returns:
        A string containing the deployment script.
    """
    logger = cf.get_run_logger()
    logger.info(f"Starting Deployer Agent task...")

    # Create an instance of our BaseAgent with the deployer persona
    deployer_agent = BaseAgent(system_prompt=DEPLOYER_SYSTEM_PROMPT)

    # Execute the script generation
    deployment_script = deployer_agent.execute(user_prompt=test_plan)

    logger.info("Deployer Agent task completed.")

    return deployment_script
