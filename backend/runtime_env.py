"""
Runtime environment detection and conditional imports.
This allows the same codebase to work in both development (with full dependencies)
and production (Vercel) with lightweight alternatives.
"""

import os
import sys
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Detect if we're running in Vercel
IS_VERCEL = os.getenv('VERCEL') == '1'
IS_PRODUCTION = os.getenv('VERCEL_ENV') == 'production'

class MockFlow:
    """Mock implementation of Prefect flow for Vercel deployment."""
    
    def __init__(self, name: str = "mock_flow", **kwargs):
        self.name = name
        self.kwargs = kwargs
    
    def __call__(self, func):
        # Return the function unchanged in Vercel
        return func

class MockTask:
    """Mock implementation of ControlFlow task for Vercel deployment."""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    def __call__(self, func):
        # Return the function unchanged in Vercel
        return func

class MockControlFlow:
    """Mock ControlFlow module for Vercel deployment."""
    
    @staticmethod
    def task(**kwargs):
        return MockTask(**kwargs)

class MockPrefect:
    """Mock Prefect module for Vercel deployment."""
    
    @staticmethod
    def flow(**kwargs):
        return MockFlow(**kwargs)
    
    @staticmethod
    def get_run_logger():
        return logging.getLogger("mock_prefect")

def get_controlflow():
    """Get ControlFlow module or mock for Vercel."""
    if IS_VERCEL:
        logger.info("Using mock ControlFlow for Vercel deployment")
        return MockControlFlow()
    
    try:
        import controlflow as cf
        return cf
    except ImportError:
        logger.warning("ControlFlow not available, using mock")
        return MockControlFlow()

def get_prefect():
    """Get Prefect module or mock for Vercel."""
    if IS_VERCEL:
        logger.info("Using mock Prefect for Vercel deployment")
        return MockPrefect()
    
    try:
        import prefect
        return prefect
    except ImportError:
        logger.warning("Prefect not available, using mock")
        return MockPrefect()

def get_prefect_client():
    """Get Prefect client or mock for Vercel."""
    if IS_VERCEL:
        logger.info("Prefect client not available in Vercel")
        return None
    
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
        "is_vercel": IS_VERCEL,
        "is_production": IS_PRODUCTION,
        "python_version": sys.version,
        "platform": sys.platform,
        "vercel_env": os.getenv('VERCEL_ENV'),
        "vercel_url": os.getenv('VERCEL_URL'),
        "vercel_region": os.getenv('VERCEL_REGION'),
    }
