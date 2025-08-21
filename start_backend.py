#!/usr/bin/env python3
"""
BotArmy Backend Startup Script

This script properly sets up the Python path and starts the backend server.
Run this from the project root directory.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path so 'backend' module can be found
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Change to backend directory for relative imports to work
backend_dir = project_root / "backend"
os.chdir(backend_dir)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting BotArmy Backend...")
    print(f"📍 Project root: {project_root}")
    print(f"📍 Backend dir: {backend_dir}")
    print(f"📍 Python path includes: {project_root}")
    print("=" * 50)
    
    # Start the server
    uvicorn.run(
        "backend.main:app",  # Use import string for reload to work
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        reload_dirs=[str(backend_dir)]
    )
