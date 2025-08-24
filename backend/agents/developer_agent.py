"""
Adaptive Developer Agent that works in both development and Replit environments.
"""

import logging
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect

# Get appropriate modules based on environment
cf = get_controlflow()
prefect = get_prefect()

logger = logging.getLogger(__name__)

# Define the persona and instructions for the Developer Agent
DEVELOPER_SYSTEM_PROMPT = """
You are an expert AI software developer. Your goal is to take a technical
architecture specification and write the main application code.

You should:
1. **Choose a language and framework** appropriate for the task (default to Python with FastAPI if not specified).
2. **Write the code** for the main application logic.
3. **Structure the code** logically in a single file for this POC.
4. **Include comments** to explain key parts of the code.

Produce only the raw code as your output, enclosed in a single markdown code block.
"""

@cf.task
async def run_developer_task(architecture_document: str) -> str:
    """
    Developer Agent task that adapts to the runtime environment.
    """
    
    run_logger = prefect.get_run_logger()
    run_logger.info("Starting Developer Agent")

    developer_agent = BaseAgent(system_prompt=DEVELOPER_SYSTEM_PROMPT)
    
    try:
        generated_code = await developer_agent.execute(
            user_prompt=architecture_document, 
            agent_name="Developer"
        )
        
        run_logger.info("Developer Agent completed")
        
        return generated_code
        
    except Exception as e:
        error_msg = f"Developer Agent failed: {str(e)}"
        logger.error(error_msg)
        
        return f"""# Code Generation - Error Recovery

## Issue
⚠️ Automated code generation failed: {str(e)}

## Fallback Code Template

```python
# Basic FastAPI application template
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Generated Application")

class Item(BaseModel):
    name: str
    description: str

@app.get("/")
async def root():
    return {{"message": "Application generated with fallback template"}}

@app.get("/health")
async def health():
    return {{"status": "healthy"}}

# TODO: Implement specific functionality based on:
# {architecture_document[:200]}...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Next Steps
- Manual code review and implementation required
- Add business logic based on architecture document
"""
