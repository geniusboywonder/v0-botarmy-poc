"""
Adaptive Architect Agent that works in both development and Replit environments.
"""

import logging
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect

# Get appropriate modules based on environment
cf = get_controlflow()
prefect = get_prefect()

logger = logging.getLogger(__name__)

# Define the persona and instructions for the Architect Agent
ARCHITECT_SYSTEM_PROMPT = """
You are a master AI software architect. Your goal is to take a requirements
document and produce a high-level technical architecture specification.

The specification should include:
1. **Technology Stack:** A list of recommended technologies (e.g., Frontend Framework, Backend Language, Database).
2. **System Components:** A breakdown of the major components of the system (e.g., API Server, Database, Caching Layer, Frontend App).
3. **Data Model:** A simple representation of the core data entities and their relationships.
4. **API Endpoints:** A list of key API endpoints, including the HTTP method, path, and a brief description.

Produce the output in Markdown format. Be concise and clear.
"""

@cf.task
async def run_architect_task(requirements_document: str, status_broadcaster=None, session_id: str = "global") -> str:
    """
    Architect Agent task that adapts to the runtime environment.
    """
    
    run_logger = prefect.get_run_logger()
    run_logger.info("Starting Architect Agent")

    architect_agent = BaseAgent(system_prompt=ARCHITECT_SYSTEM_PROMPT, status_broadcaster=status_broadcaster)
    
    try:
        technical_design = await architect_agent.execute(
            user_prompt=requirements_document, 
            agent_name="Architect",
            session_id=session_id
        )
        
        run_logger.info("Architect Agent completed")
        
        return technical_design
        
    except Exception as e:
        error_msg = f"Architect Agent failed: {str(e)}"
        logger.error(error_msg)
        
        return f"""# Technical Architecture - Error Recovery

## Issue
⚠️ Automated architecture design failed: {str(e)}

## Fallback Architecture
Based on requirements: "{requirements_document[:100]}..."

### Recommended Technology Stack
- Frontend: React/Next.js
- Backend: Python FastAPI
- Database: PostgreSQL
- Deployment: Railway + Replit

### System Components
1. Frontend Application
2. REST API Server
3. Database Layer
4. Authentication Service

### Next Steps
- Manual architecture review required
- Consult with technical team
"""
