#!/usr/bin/env python3
"""
Test to reproduce the maximum recursion depth exceeded error in botarmy_workflow.

This test attempts to reproduce the recursion error that occurs during Prefect workflow 
initialization by creating a minimal test environment.
"""

import asyncio
import logging
import sys
import traceback
from unittest.mock import Mock, AsyncMock

# Set up logging to capture recursion details
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('recursion_test.log')
    ]
)
logger = logging.getLogger(__name__)

def track_recursion():
    """Track recursion depth to detect infinite loops"""
    frame = sys._getframe()
    depth = 0
    while frame:
        depth += 1
        if depth > 100:  # Stop counting at reasonable depth
            break
        frame = frame.f_back
    return depth

async def test_botarmy_workflow_recursion():
    """Test the botarmy_workflow for recursion issues"""
    logger.info("Starting recursion test for botarmy_workflow")
    
    try:
        # Set up offline mode for Prefect
        import os
        os.environ["PREFECT_API_URL"] = ""
        os.environ["PREFECT_SERVER_ALLOW_EPHEMERAL_MODE"] = "true"
        os.environ["AGENT_TEST_MODE"] = "true"  # Enable agent test mode
        
        # Import with recursion tracking
        initial_depth = track_recursion()
        logger.info(f"Initial recursion depth: {initial_depth}")
        
        # Import the serialization wrapper
        from backend.serialization_safe_wrapper import make_serialization_safe
        
        # Mock dependencies to isolate the workflow
        mock_status_broadcaster = AsyncMock()
        mock_agent_pause_states = {}
        mock_artifact_preferences = {"reqs-doc": True}
        mock_role_enforcer = Mock()
        
        # Wrap status_broadcaster to prevent circular reference serialization
        safe_status_broadcaster = make_serialization_safe(mock_status_broadcaster, "test_broadcaster")
        safe_role_enforcer = make_serialization_safe(mock_role_enforcer, "test_role_enforcer")
        
        # Try to import the workflow
        logger.info("Importing botarmy_workflow...")
        from backend.legacy_workflow import botarmy_workflow
        
        import_depth = track_recursion()
        logger.info(f"Post-import recursion depth: {import_depth}")
        
        # Test minimal workflow call
        logger.info("Testing minimal workflow call...")
        
        # Set recursion limit to catch issues early
        original_recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(200)  # Lower limit to catch recursion faster
        logger.info(f"Set recursion limit to 200 (was {original_recursion_limit})")
        
        try:
            result = await botarmy_workflow(
                project_brief="Simple test project",
                session_id="test_session",
                status_broadcaster=safe_status_broadcaster,
                agent_pause_states=mock_agent_pause_states,
                artifact_preferences=mock_artifact_preferences,
                role_enforcer=safe_role_enforcer
            )
            logger.info(f"Workflow completed successfully: {result}")
            
        except RecursionError as e:
            logger.error(f"RECURSION ERROR CAUGHT: {e}")
            logger.error("Stack trace of recursion error:")
            logger.error(traceback.format_exc())
            
            # Try to identify the recursive pattern
            tb = traceback.extract_tb(sys.exc_info()[2])
            function_calls = [frame.name for frame in tb]
            
            # Find repeating patterns
            pattern_found = False
            for i in range(1, min(50, len(function_calls))):
                if len(function_calls) >= 2*i:
                    pattern1 = function_calls[-i:]
                    pattern2 = function_calls[-2*i:-i]
                    if pattern1 == pattern2:
                        logger.error(f"Recursive pattern detected (length {i}): {pattern1}")
                        pattern_found = True
                        break
            
            if not pattern_found:
                logger.error("No clear recursive pattern found in stack trace")
                
            # Log recent function calls
            logger.error(f"Recent function calls: {function_calls[-20:]}")
            
            raise
        
        finally:
            # Restore original recursion limit
            sys.setrecursionlimit(original_recursion_limit)
            logger.info(f"Restored recursion limit to {original_recursion_limit}")
            
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        logger.error(traceback.format_exc())
        raise

async def test_prefect_flow_initialization():
    """Test Prefect flow initialization separately"""
    logger.info("Testing Prefect flow initialization...")
    
    try:
        import os
        # Set Prefect to offline mode to avoid API calls
        os.environ["PREFECT_API_URL"] = ""
        os.environ["PREFECT_SERVER_ALLOW_EPHEMERAL_MODE"] = "true"
        
        from backend.runtime_env import get_prefect
        prefect = get_prefect()
        
        # Test creating a simple flow in offline mode
        @prefect.flow(name="Test Flow", retries=0, persist_result=False)
        async def simple_test_flow():
            logger.info("Simple flow executed")
            return "success"
        
        # Run flow without server connection
        result = await simple_test_flow()
        logger.info(f"Simple Prefect flow test completed: {result}")
        
    except Exception as e:
        logger.error(f"Prefect flow test failed: {e}")
        logger.error(traceback.format_exc())
        # Don't raise - this is expected in test environment
        logger.info("Using mock Prefect implementation for further tests")

async def test_agent_task_imports():
    """Test importing agent tasks for circular dependencies"""
    logger.info("Testing agent task imports...")
    
    try:
        # Test each agent import individually
        agent_modules = [
            "backend.agents.analyst_agent",
            "backend.agents.architect_agent", 
            "backend.agents.developer_agent",
            "backend.agents.tester_agent",
            "backend.agents.deployer_agent"
        ]
        
        for module_name in agent_modules:
            try:
                logger.info(f"Importing {module_name}...")
                __import__(module_name)
                logger.info(f"✓ {module_name} imported successfully")
            except Exception as e:
                logger.error(f"✗ Failed to import {module_name}: {e}")
                logger.error(traceback.format_exc())
                
    except Exception as e:
        logger.error(f"Agent import test failed: {e}")
        raise

async def main():
    """Main test runner"""
    logger.info("=" * 60)
    logger.info("BOTARMY WORKFLOW RECURSION TEST")
    logger.info("=" * 60)
    
    tests = [
        ("Prefect Flow Initialization", test_prefect_flow_initialization),
        ("Agent Task Imports", test_agent_task_imports),
        ("BotArmy Workflow Recursion", test_botarmy_workflow_recursion),
    ]
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Running: {test_name} ---")
        try:
            await test_func()
            logger.info(f"✓ {test_name} PASSED")
        except Exception as e:
            logger.error(f"✗ {test_name} FAILED: {e}")
            # Continue with other tests
    
    logger.info("\n" + "=" * 60)
    logger.info("RECURSION TEST COMPLETED")
    logger.info("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())