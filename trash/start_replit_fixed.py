#!/usr/bin/env python3
"""
Replit startup script with pip installation fix
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

# Try to ensure pip is available
print("🔧 Setting up pip...")
try:
    # Try to ensure pip is installed
    subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], 
                  check=False, capture_output=True)
    print("✅ pip setup complete")
except:
    print("⚠️  pip setup had issues, continuing anyway...")

# Install dependencies with multiple fallback methods
print("📦 Installing Python dependencies...")

# Method 1: Try with python -m pip
try:
    if Path("requirements-replit.txt").exists():
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements-replit.txt",
            "--user", "--no-cache-dir"
        ], check=True, capture_output=True, text=True)
    else:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", 
            "--user", "--no-cache-dir"
        ], check=True, capture_output=True, text=True)
    print("✅ Dependencies installed via pip")
except subprocess.CalledProcessError as e:
    print(f"⚠️  pip install failed: {e}")
    
    # Method 2: Try essential packages only
    print("📦 Trying minimal package installation...")
    essential_packages = [
        "fastapi==0.116.1",
        "uvicorn[standard]==0.24.0", 
        "websockets==12.0",
        "python-dotenv",
        "pydantic",
        "openai",
        "google-generativeai"
    ]
    
    failed_packages = []
    for package in essential_packages:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", package, "--user"
            ], check=True, capture_output=True)
            print(f"   ✅ {package}")
        except:
            print(f"   ❌ {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"⚠️  Failed to install: {failed_packages}")
        print("   Try installing these via Replit Packages tab (📦)")
        print("   Or continue - some functionality may be limited")

# Test imports
print("🔍 Testing critical imports...")
critical_imports = ['fastapi', 'uvicorn', 'websockets', 'pydantic', 'openai']
working_imports = []

for module in critical_imports:
    try:
        __import__(module)
        working_imports.append(module)
        print(f"   ✅ {module}")
    except ImportError:
        print(f"   ❌ {module}")

if len(working_imports) < 3:
    print("❌ Too many missing imports. Please install packages via Replit UI.")
    print("   Go to Packages tab (📦) and install: fastapi, uvicorn, websockets")
    sys.exit(1)

print(f"✅ {len(working_imports)}/{len(critical_imports)} critical imports working")

# Start backend
print("🔧 Starting backend...")
backend_dir = Path.cwd() / 'backend'
if not backend_dir.exists():
    print("❌ Backend directory not found")
    sys.exit(1)

os.chdir(backend_dir)
port = os.getenv('PORT', '8000')

print(f"🟢 Starting server on 0.0.0.0:{port}")
print("=" * 50)

try:
    subprocess.run([
        sys.executable, "-m", "uvicorn", "main:app",
        "--host", "0.0.0.0", 
        "--port", port, 
        "--reload"
    ])
except KeyboardInterrupt:
    print("👋 Shutdown requested")
except Exception as e:
    print(f"❌ Server error: {e}")
    print("   Check that all required packages are installed")
    sys.exit(1)