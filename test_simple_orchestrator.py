#!/usr/bin/env python3
"""
Direct test of the simple orchestrator to verify it works independently
"""
import asyncio
import logging
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.workflow.simple_orchestrator import create_simple_workflow
from backend.services.llm_service import get_llm_service
from backend.agent_status_broadcaster import AgentStatusBroadcaster

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_simple_orchestrator():
    """Test the simple orchestrator directly"""
    logger.info("Starting direct test of simple orchestrator")
    
    try:
        # Initialize services
        llm_service = get_llm_service()
        status_broadcaster = AgentStatusBroadcaster(None)  # No connection manager needed for test
        
        # Create simple workflow
        simple_workflow = create_simple_workflow(llm_service, status_broadcaster)
        
        # Test project brief
        project_brief = "Create a simple calculator app with React frontend and Express backend"
        session_id = "test_session"
        
        logger.info(f"Testing with project: {project_brief}")
        
        # Execute workflow
        result = await simple_workflow.execute_workflow(project_brief, session_id)
        
        logger.info(f"Workflow completed successfully!")
        logger.info(f"Result summary: {result}")
        
        # Check if artifacts were created
        import os
        artifacts_dir = "artifacts"
        if os.path.exists(artifacts_dir):
            artifact_files = [f for f in os.listdir(artifacts_dir) if f.endswith('.md')]
            logger.info(f"Artifacts created: {artifact_files}")
            
            # Read and display first artifact
            if artifact_files:
                with open(os.path.join(artifacts_dir, artifact_files[0]), 'r') as f:
                    content = f.read()[:500]  # First 500 chars
                logger.info(f"Sample artifact content:\n{content}...")
        else:
            logger.warning("No artifacts directory found")
        
        return result
        
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    asyncio.run(test_simple_orchestrator())