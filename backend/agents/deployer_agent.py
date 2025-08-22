"""
Adaptive Deployer Agent that works in both development and Vercel environments.
"""

import logging
from backend.agents.base_agent import BaseAgent
from backend.runtime_env import get_controlflow, get_prefect, IS_VERCEL

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
async def run_deployer_task(test_plan: str) -> str:
    """
    Deployer Agent task that adapts to the runtime environment.
    """
    
    if IS_VERCEL:
        logger.info("Starting Deployer Agent (Vercel mode)")
    else:
        run_logger = prefect.get_run_logger()
        run_logger.info("Starting Deployer Agent (Development mode)")

    deployer_agent = BaseAgent(system_prompt=DEPLOYER_SYSTEM_PROMPT)
    
    try:
        deployment_script = await deployer_agent.execute(
            user_prompt=test_plan, 
            agent_name="Deployer"
        )
        
        if IS_VERCEL:
            logger.info("Deployer Agent (Vercel mode) completed")
        else:
            run_logger.info("Deployer Agent (Development mode) completed")
        
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
if [ -z "$VERCEL_ENV" ]; then
    echo "Local deployment mode"
else
    echo "Vercel deployment mode: $VERCEL_ENV"
fi

# Build application
echo "🔨 Building application..."
npm run build

# Deploy to Vercel
echo "☁️ Deploying to Vercel..."
vercel --prod

echo "✅ Deployment process completed"
echo "🌐 Application should be available at your Vercel URL"

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
