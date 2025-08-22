"""
Runtime environment detection and conditional imports.
This allows the same codebase to work in both development and Replit environments.
"""

import os
import sys
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Detect if we're running in Replit
IS_REPLIT = os.getenv('REPLIT') == '1' or 'replit' in os.getenv('HOSTNAME', '').lower()
IS_PRODUCTION = os.getenv('REPLIT_DEPLOYMENT') == '1'

class MockFlow:
    """Mock implementation of Prefect flow for fallback."""
    
    def __init__(self, name: str = "mock_flow", **kwargs):
        self.name = name
        self.kwargs = kwargs
    
    def __call__(self, func):
        # Return the function unchanged
        return func

class MockTask:
    """Mock implementation of ControlFlow task for fallback."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    def __call__(self, func):
        # Return the function unchanged
        return func

class MockControlFlow:
    """Mock ControlFlow module for fallback."""
    
    @staticmethod
    def task(**kwargs):
        return MockTask(**kwargs)

class MockPrefect:
    """Mock Prefect module for fallback."""
    
    @staticmethod
    def flow(**kwargs):
        return MockFlow(**kwargs)
    
    @staticmethod
    def get_run_logger():
        return logging.getLogger("mock_prefect")

def get_controlflow():
    """Get ControlFlow module or mock for fallback."""
    try:
        import controlflow as cf
        logger.info("ControlFlow successfully imported")
        return cf
    except ImportError as e:
        logger.warning(f"ControlFlow not available: {e}, using mock")
        return MockControlFlow()

def get_prefect():
    """Get Prefect module or mock for fallback."""
    try:
        import prefect
        logger.info("Prefect successfully imported")
        return prefect
    except ImportError as e:
        logger.warning(f"Prefect not available: {e}, using mock")
        return MockPrefect()

def get_prefect_client():
    """Get Prefect client or mock for fallback."""
    try:
        from prefect.client.orchestration import get_client
        return get_client()
    except ImportError:
        logger.warning("Prefect client not available")
        return None

# Environment info for debugging
def get_environment_info():
    """Get information about the current runtime environment."""
    return {
        "is_replit": IS_REPLIT,
        "is_production": IS_PRODUCTION,
        "python_version": sys.version,
        "platform": sys.platform,
        "replit_deployment": os.getenv('REPLIT_DEPLOYMENT'),
        "hostname": os.getenv('HOSTNAME'),
        "port": os.getenv('PORT'),
        "replit_db_url": os.getenv('REPLIT_DB_URL'),
    }