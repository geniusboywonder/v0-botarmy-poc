"""
Adaptive Tester Agent that works in both development and Vercel environments.
"""

import logging
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect, IS_VERCEL

# Get appropriate modules based on environment
cf = get_controlflow()
prefect = get_prefect()

logger = logging.getLogger(__name__)

# Define the persona and instructions for the Tester Agent
TESTER_SYSTEM_PROMPT = """
You are a meticulous AI QA engineer. Your goal is to take a piece of code
and a set of requirements, and write a brief test plan.

You should:
1. **Review the code** for obvious errors.
2. **Write a short test plan** in markdown format, including a few key test cases.
3. **Do not execute the tests.** Simply formulate the plan.

Conclude by stating if you believe the code is ready for deployment based on your plan.
"""

@cf.task
async def run_tester_task(code: str) -> str:
    """
    Tester Agent task that adapts to the runtime environment.
    """
    
    if IS_VERCEL:
        logger.info("Starting Tester Agent (Vercel mode)")
    else:
        run_logger = prefect.get_run_logger()
        run_logger.info("Starting Tester Agent (Development mode)")

    tester_agent = BaseAgent(system_prompt=TESTER_SYSTEM_PROMPT)
    
    try:
        test_plan = await tester_agent.execute(
            user_prompt=code, 
            agent_name="Tester"
        )
        
        if IS_VERCEL:
            logger.info("Tester Agent (Vercel mode) completed")
        else:
            run_logger.info("Tester Agent (Development mode) completed")
        
        return test_plan
        
    except Exception as e:
        error_msg = f"Tester Agent failed: {str(e)}"
        logger.error(error_msg)
        
        return f"""# Test Plan - Error Recovery

## Issue
⚠️ Automated test planning failed: {str(e)}

## Manual Test Plan Required

### Code Analysis
Code to be tested: "{code[:200]}..."

### Recommended Test Categories
1. **Unit Tests**
   - Test individual functions
   - Validate input/output behavior
   - Check error handling

2. **Integration Tests**
   - Test API endpoints
   - Verify database connections
   - Check external service integration

3. **End-to-End Tests**
   - Test complete user workflows
   - Validate UI functionality
   - Check performance under load

### Next Steps
- Manual code review required
- Create specific test cases
- Set up testing framework
- Execute tests before deployment

## Deployment Readiness
❌ Manual review required before deployment
"""
