import controlflow as cf
import prefect
from backend.agents.base_agent import BaseAgent

# Define the persona and instructions for the Tester Agent
TESTER_SYSTEM_PROMPT = """
You are a meticulous AI QA engineer. Your goal is to take a piece of code
and a set of requirements, and write a brief test plan.

You should:
1.  **Review the code** for obvious errors.
2.  **Write a short test plan** in markdown format, including a few key test cases.
3.  **Do not execute the tests.** Simply formulate the plan.

Conclude by stating if you believe the code is ready for deployment based on your plan.
"""

@cf.task
async def run_tester_task(code: str) -> str:
    """
    This ControlFlow task runs the Tester Agent to create a test plan for a
    piece of code.

    Args:
        code: A string containing the code to be tested.

    Returns:
        A string containing the test plan.
    """
    logger = prefect.get_run_logger()
    logger.info(f"Starting Tester Agent task...")

    # Create an instance of our BaseAgent with the tester persona
    tester_agent = BaseAgent(system_prompt=TESTER_SYSTEM_PROMPT)

    # Execute the test planning
    test_plan = await tester_agent.execute(user_prompt=code, agent_name="Tester")

    logger.info("Tester Agent task completed.")

    return test_plan
