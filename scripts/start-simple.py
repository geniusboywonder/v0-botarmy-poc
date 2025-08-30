#!/usr/bin/env python3
"""
Simple Replit startup script for BotArmy - No indentation issues
"""
import os
import sys
import subprocess
from pathlib import Path

print("🚀 Starting BotArmy on Replit...")

# Set basic environment
os.environ['REPLIT'] = '1'
os.environ['PYTHONPATH'] = f"{Path.cwd()}:{Path.cwd() / 'backend'}"

# Check for API keys
if not os.getenv('OPENAI_API_KEY'):
    print("❌ OPENAI_API_KEY not found in Secrets")
    print("   Please add it in Replit Secrets tab (🔐)")
    sys.exit(1)

print("✅ Environment variables found")

# Install dependencies
print("📦 Installing Python dependencies...")
try:
    if Path("requirements-replit.txt").exists():
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-replit.txt"], check=True)
    else:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("✅ Dependencies installed")
except:
    print("❌ Failed to install dependencies")
    sys.exit(1)

# Start backend
print("🔧 Starting backend...")
os.chdir(Path.cwd() / 'backend')
port = os.getenv('PORT', '8000')

try:
    subprocess.run([
        sys.executable, "-m", "uvicorn", "main:app",
        "--host", "0.0.0.0", "--port", port, "--reload"
    ])
except KeyboardInterrupt:
    print("👋 Shutdown requested")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)