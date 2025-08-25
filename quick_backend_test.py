#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Set test mode
os.environ["AGENT_TEST_MODE"] = "true"

print("🧪 Quick Backend Test")
print("=" * 30)

# Test results
results = []

# Test 1: FastAPI
try:
    from fastapi import FastAPI
    results.append("✅ FastAPI")
except Exception as e:
    results.append(f"❌ FastAPI: {e}")

# Test 2: Backend runtime
try:
    from backend.runtime_env import IS_REPLIT, get_environment_info
    results.append("✅ Runtime Environment")
except Exception as e:
    results.append(f"❌ Runtime Environment: {e}")

# Test 3: AGUI protocol
try:
    from backend.agui.protocol import agui_handler
    results.append("✅ AGUI Protocol")
except Exception as e:
    results.append(f"❌ AGUI Protocol: {e}")

# Test 4: Connection Manager
try:
    from backend.connection_manager import EnhancedConnectionManager
    results.append("✅ Connection Manager")
except Exception as e:
    results.append(f"❌ Connection Manager: {e}")

# Test 5: Status Broadcaster
try:
    from backend.agent_status_broadcaster import AgentStatusBroadcaster
    results.append("✅ Status Broadcaster")
except Exception as e:
    results.append(f"❌ Status Broadcaster: {e}")

# Test 6: Workflow
try:
    from backend.workflow import botarmy_workflow
    results.append("✅ Workflow")
except Exception as e:
    results.append(f"❌ Workflow: {e}")

# Test 7: main_simple
try:
    from backend.main_simple import app
    results.append("✅ main_simple")
except Exception as e:
    results.append(f"❌ main_simple: {e}")

# Write results to file
with open("test_results.txt", "w") as f:
    for result in results:
        print(result)
        f.write(result + "\n")

print("\nTest completed!")
