import sys
import os
from pathlib import Path

# Add paths
project_root = Path("/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc")
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Set test mode
os.environ["AGENT_TEST_MODE"] = "true"

test_results = []

# Test 1: Basic imports
try:
    from fastapi import FastAPI
    test_results.append("PASS: FastAPI import")
except Exception as e:
    test_results.append(f"FAIL: FastAPI - {e}")

try:
    import uvicorn
    test_results.append("PASS: uvicorn import")
except Exception as e:
    test_results.append(f"FAIL: uvicorn - {e}")

# Test 2: Backend modules
try:
    from backend.runtime_env import IS_REPLIT, get_environment_info
    env_info = get_environment_info()
    test_results.append(f"PASS: Runtime env - IS_REPLIT={IS_REPLIT}")
except Exception as e:
    test_results.append(f"FAIL: Runtime env - {e}")

try:
    from backend.connection_manager import EnhancedConnectionManager
    test_results.append("PASS: Connection Manager")
except Exception as e:
    test_results.append(f"FAIL: Connection Manager - {e}")

try:
    from backend.agent_status_broadcaster import AgentStatusBroadcaster
    test_results.append("PASS: Status Broadcaster")
except Exception as e:
    test_results.append(f"FAIL: Status Broadcaster - {e}")

try:
    from backend.agui.protocol import agui_handler
    test_results.append("PASS: AGUI Protocol")
except Exception as e:
    test_results.append(f"FAIL: AGUI Protocol - {e}")

try:
    from backend.workflow import botarmy_workflow
    test_results.append("PASS: Workflow")
except Exception as e:
    test_results.append(f"FAIL: Workflow - {e}")

# Test simple backend
try:
    from backend.main_simple import app
    test_results.append("PASS: main_simple app")
except Exception as e:
    test_results.append(f"FAIL: main_simple - {e}")

# Write results
with open("/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc/testing_logs/import_test_results.txt", "w") as f:
    f.write("Backend Import Test Results\n")
    f.write("="*40 + "\n\n")
    for result in test_results:
        f.write(result + "\n")

print("Test completed - results written to testing_logs/import_test_results.txt")
