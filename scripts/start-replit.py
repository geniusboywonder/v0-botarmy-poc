#!/usr/bin/env python3
"""
Fixed Replit startup script for BotArmy
Handles environment detection and stable dependency management
"""

import os
import sys
import subprocess
import logging
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup the Replit environment for BotArmy."""
    logger.info("🚀 Setting up BotArmy for Replit...")
    
    # Set environment variables for proper Python path
    os.environ['REPLIT'] = '1'
    os.environ['PYTHONPATH'] = f"{Path.cwd()}:{Path.cwd() / 'backend'}"
    
    # Auto-detect Replit URL if possible
    if 'REPL_SLUG' in os.environ and 'REPL_OWNER' in os.environ:
        repl_url = f"https://{os.environ['REPL_SLUG']}.{os.environ['REPL_OWNER']}.repl.co"
        os.environ['BACKEND_URL'] = repl_url
        os.environ['NEXT_PUBLIC_BACKEND_URL'] = repl_url
        os.environ['WEBSOCKET_URL'] = f"wss://{os.environ['REPL_SLUG']}.{os.environ['REPL_OWNER']}.repl.co/api/ws"
        os.environ['NEXT_PUBLIC_WEBSOCKET_URL'] = f"wss://{os.environ['REPL_SLUG']}.{os.environ['REPL_OWNER']}.repl.co/api/ws"
        logger.info(f"✅ Auto-detected Replit URL: {repl_url}")
    else:
        logger.warning("⚠️  Could not auto-detect Replit URL - using localhost fallback")
        os.environ.setdefault('BACKEND_URL', 'http://localhost:8000')
        os.environ.setdefault('WEBSOCKET_URL', 'ws://localhost:8000/api/ws')
    
    # Verify Python version
    python_version = sys.version_info
    logger.info(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 13):
        logger.warning("⚠️  Python 3.13+ recommended for best compatibility")
    
    # Check environment variables
    required_vars = ['OPENAI_API_KEY', 'GOOGLE_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        logger.error("   Please set these in Replit Secrets tab (🔐)")
        return False
    else:
        logger.info("✅ Required environment variables found")
    
    return True

def install_dependencies():
    """Install Python dependencies with Replit-optimized requirements."""
    logger.info("📦 Installing Python dependencies...")
    
    try:
        # Use Replit-specific requirements if available, otherwise fall back
        if Path("requirements-replit.txt").exists():
            requirements_file = "requirements-replit.txt"
            logger.info("   Using Replit-optimized requirements")
        else:
            requirements_file = "requirements.txt" 
            logger.warning("   Using full requirements.txt (may cause issues)")
        
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", requirements_file,
            "--no-cache-dir",  # Save disk space
            "--disable-pip-version-check"  # Reduce output noise
        ], check=True, capture_output=True, text=True, timeout=300)
        
        logger.info("✅ Python dependencies installed successfully")
        
        # Log any warnings
        if result.stderr and "warning" in result.stderr.lower():
            logger.warning(f"   Installation warnings: {result.stderr}")
            
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("❌ Dependency installation timed out after 5 minutes")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        logger.error(f"   stdout: {e.stdout}")
        logger.error(f"   stderr: {e.stderr}")
        return False

def verify_imports():
    """Verify critical imports work before starting server."""
    logger.info("🔍 Verifying critical imports...")
    
    critical_imports = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn web server'),
        ('websockets', 'WebSocket support'),
        ('pydantic', 'Data validation'),
        ('openai', 'OpenAI client'),
        ('google.generativeai', 'Google AI')
    ]
    
    failed_imports = []
    
    for module_name, description in critical_imports:
        try:
            __import__(module_name)
            logger.info(f"   ✅ {description}")
        except ImportError as e:
            logger.error(f"   ❌ {description}: {e}")
            failed_imports.append(module_name)
    
    if failed_imports:
        logger.error(f"❌ Failed to import: {failed_imports}")
        return False
    
    # Test backend imports specifically
    try:
        sys.path.insert(0, str(Path.cwd() / 'backend'))
        from main import app
        logger.info("   ✅ Backend main module")
        return True
    except ImportError as e:
        logger.error(f"   ❌ Backend main module: {e}")
        return False

def start_backend():
    """Start the FastAPI backend with proper Replit configuration."""
    logger.info("🔧 Starting BotArmy backend...")
    
    # Change to backend directory
    backend_dir = Path.cwd() / 'backend'
    if not backend_dir.exists():
        logger.error("❌ Backend directory not found")
        return False
        
    os.chdir(backend_dir)
    logger.info(f"   Working directory: {backend_dir}")
    
    # Get port from Replit environment
    port = os.getenv('PORT', '8000')
    host = "0.0.0.0"  # Required for Replit external access
    
    logger.info(f"   Starting server on {host}:{port}")
    
    try:
        # Start uvicorn with Replit-optimized settings
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app",
            "--host", host,
            "--port", str(port),
            "--reload",
            "--access-log",
            "--log-level", "info",
            "--timeout-keep-alive", "65",  # For WebSocket stability
            "--timeout-graceful-shutdown", "30"
        ]
        
        logger.info(f"   Command: {' '.join(cmd)}")
        logger.info("=" * 60)
        logger.info("🟢 Backend starting... (Ctrl+C to stop)")
        logger.info("=" * 60)
        
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to start backend: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("👋 Backend shutdown requested by user")
        return True

def main():
    """Main startup function for Replit deployment."""
    logger.info("=" * 60)
    logger.info("🤖 BotArmy POC - Replit Deployment (Fixed)")
    logger.info("=" * 60)
    
    # Phase 1: Environment Setup
    if not setup_environment():
        logger.error("❌ Environment setup failed")
        logger.error("   Check Replit Secrets tab for API keys")
        return 1
    
    # Phase 2: Install Dependencies
    if not install_dependencies():
        logger.error("❌ Dependency installation failed")
        logger.error("   Try switching to requirements-replit.txt")
        return 1
    
    # Phase 3: Verify Imports
    if not verify_imports():
        logger.error("❌ Import verification failed")
        logger.error("   Some required packages may not be installed")
        return 1
    
    # Phase 4: Start Backend
    logger.info("🚀 All checks passed - starting backend server...")
    start_backend()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        logger.error("   Please check the Replit console for details")
        sys.exit(1)