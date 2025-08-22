#!/usr/bin/env python3
"""
Replit startup script for BotArmy
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup the Replit environment for BotArmy."""
    logger.info("🚀 Setting up BotArmy for Replit...")
    
    # Set environment variables
    os.environ['REPLIT'] = '1'
    os.environ['PYTHONPATH'] = f"{Path.cwd()}:{Path.cwd() / 'backend'}"
    
    # Verify Python version
    python_version = sys.version_info
    logger.info(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 11):
        logger.warning("Python 3.11+ recommended for best compatibility")
    
    return True

def install_dependencies():
    """Install Python dependencies."""
    logger.info("📦 Installing Python dependencies...")
    
    try:
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        
        logger.info("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        logger.error(f"Output: {e.stdout}")
        logger.error(f"Error: {e.stderr}")
        return False

def start_backend():
    """Start the FastAPI backend."""
    logger.info("🔧 Starting BotArmy backend...")
    
    # Change to backend directory
    backend_dir = Path.cwd() / 'backend'
    os.chdir(backend_dir)
    
    # Get port from environment (Replit sets this)
    port = os.getenv('PORT', '8000')
    
    try:
        # Start uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", str(port),
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to start backend: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("👋 Backend shutdown requested")
        return True

def main():
    """Main startup function."""
    logger.info("=" * 60)
    logger.info("🤖 BotArmy POC - Replit Deployment")
    logger.info("=" * 60)
    
    # Setup environment
    if not setup_environment():
        logger.error("❌ Environment setup failed")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        logger.error("❌ Dependency installation failed")
        return 1
    
    # Start backend
    start_backend()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())