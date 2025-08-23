"""
Adaptive Deployer Agent that works in both development and Replit environments.
"""

import logging
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect

# Get appropriate modules based on environment
cf = get_controlflow()
prefect = get_prefect()

logger = logging.getLogger(__name__)

# Define the persona and instructions for the Deployer Agent
DEPLOYER_SYSTEM_PROMPT = """
You are a DevOps specialist AI. Your goal is to take a test plan and a piece of
code and create a simple deployment script.

You should:
1. **Assume the tests have passed.**
2. **Write a simple shell script** that would deploy the application (e.g., echo "Deploying...", copy files, restart server).
3. **Keep the script very simple** for this POC.

Produce only the raw shell script as your output, enclosed in a single markdown code block.
"""

@cf.task
async def run_deployer_task(test_plan: str, status_broadcaster=None, session_id: str = "global") -> str:
    """
    Deployer Agent task that adapts to the runtime environment.
    """
    
    run_logger = prefect.get_run_logger()
    run_logger.info("Starting Deployer Agent")

    deployer_agent = BaseAgent(system_prompt=DEPLOYER_SYSTEM_PROMPT, status_broadcaster=status_broadcaster)
    
    try:
        deployment_script = await deployer_agent.execute(
            user_prompt=test_plan, 
            agent_name="Deployer",
            session_id=session_id
        )
        
        run_logger.info("Deployer Agent completed")
        
        return deployment_script
        
    except Exception as e:
        error_msg = f"Deployer Agent failed: {str(e)}"
        logger.error(error_msg)
        
        return f"""# Deployment Script - Error Recovery

## Issue
⚠️ Automated deployment script generation failed: {str(e)}

## Fallback Deployment Script

```bash
#!/bin/bash

# Basic deployment script template
echo "🚀 Starting deployment process..."

# Environment check
echo "📋 Checking environment..."
if [ -z "$REPLIT_DEPLOYMENT" ]; then
    echo "Local deployment mode"
else
    echo "Replit deployment mode: $REPLIT_DEPLOYMENT"
fi

# Build application
echo "🔨 Building application..."
npm run build

# Deploy to Replit/Railway
echo "☁️ Deploying to cloud platform..."
echo "TODO: Add platform-specific deployment commands"

echo "✅ Deployment process completed"
echo "🌐 Application should be available at your deployment URL"

# Post-deployment checks
echo "🔍 Running post-deployment health checks..."
echo "TODO: Add health check endpoints verification"

echo "📝 Manual verification required:"
echo "1. Check application URL"
echo "2. Verify API endpoints"
echo "3. Test core functionality"
```

## Next Steps
- Manual deployment verification required
- Update script based on specific needs: "{test_plan[:100]}..."
"""
