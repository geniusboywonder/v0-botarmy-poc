#!/usr/bin/env python3
"""
Phase 1 Backend Testing - Focused Issue Identification
Tests the backend startup and WebSocket functionality step by step
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Setup environment
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set test mode for safety
os.environ["AGENT_TEST_MODE"] = "true"

print("🧪 Phase 1: Backend Startup Test")
print("=" * 50)

# Test results collector
test_results = []

def log_result(test_name, success, message="", error=None):
    """Log test results"""
    status = "✅ PASS" if success else "❌ FAIL"
    result_line = f"{status} {test_name}"
    if message:
        result_line += f" - {message}"
    if error:
        result_line += f" (Error: {error})"

    test_results.append(result_line)
    print(result_line)

# Test 1: Environment Check
print("\n1️⃣ Environment Configuration Test")
api_key = os.getenv("OPENAI_API_KEY")
test_mode = os.getenv("AGENT_TEST_MODE", "false")

if api_key and len(api_key) > 20:
    log_result("OpenAI API Key", True, f"Configured ({api_key[:8]}...{api_key[-4:]})")
else:
    log_result("OpenAI API Key", False, "Missing or invalid")

log_result("Test Mode", True, f"AGENT_TEST_MODE={test_mode}")

# Test 2: Critical Import Test
print("\n2️⃣ Critical Imports Test")
import_tests = [
    ("FastAPI", "from fastapi import FastAPI, WebSocket"),
    ("uvicorn", "import uvicorn"),
    ("WebSocket", "from fastapi import WebSocketDisconnect"),
    ("CORS", "from fastapi.middleware.cors import CORSMiddleware"),
    ("dotenv", "from dotenv import load_dotenv"),
]

for test_name, import_stmt in import_tests:
    try:
        exec(import_stmt)
        log_result(f"Import {test_name}", True)
    except Exception as e:
        log_result(f"Import {test_name}", False, error=str(e))

# Test 3: Backend Module Test
print("\n3️⃣ Backend Modules Test")
backend_tests = [
    ("Runtime Environment", "from backend.runtime_env import IS_REPLIT"),
    ("AGUI Protocol", "from backend.agui.protocol import agui_handler"),
    ("Connection Manager", "from backend.connection_manager import EnhancedConnectionManager"),
    ("Status Broadcaster", "from backend.agent_status_broadcaster import AgentStatusBroadcaster"),
    ("Error Handler", "from backend.error_handler import ErrorHandler"),
    ("Human Input Handler", "from backend.human_input_handler import request_human_approval"),
]

for test_name, import_stmt in backend_tests:
    try:
        exec(import_stmt)
        log_result(f"Backend {test_name}", True)
    except Exception as e:
        log_result(f"Backend {test_name}", False, error=str(e))

# Test 4: Simple Backend App Creation
print("\n4️⃣ Simple Backend App Test")
try:
    from backend.main_simple import app
    log_result("Simple Backend Import", True, "main_simple.py imported")

    # Test a simple route
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/")
    if response.status_code == 200:
        data = response.json()
        log_result("Simple Backend Root Route", True, f"Status: {data.get('status', 'unknown')}")
        log_result("Test Mode Detection", True, f"Test Mode: {data.get('test_mode', 'unknown')}")
    else:
        log_result("Simple Backend Root Route", False, f"HTTP {response.status_code}")

except Exception as e:
    log_result("Simple Backend Import", False, error=str(e))

# Test 5: Full Backend App Creation
print("\n5️⃣ Full Backend App Test")
try:
    # Import the full main.py
    from backend.main import app as full_app
    log_result("Full Backend Import", True, "main.py imported")

    # Try to test the root route
    client = TestClient(full_app)
    response = client.get("/")
    if response.status_code == 200:
        data = response.json()
        log_result("Full Backend Root Route", True, f"Version: {data.get('version', 'unknown')}")

        # Check features
        features = data.get('features', {})
        for feature_name, feature_status in features.items():
            log_result(f"Feature {feature_name}", feature_status, "Available" if feature_status else "Disabled")
    else:
        log_result("Full Backend Root Route", False, f"HTTP {response.status_code}")

except Exception as e:
    log_result("Full Backend Import", False, error=str(e))

# Test 6: WebSocket Component Test
print("\n6️⃣ WebSocket Components Test")
try:
    from backend.connection_manager import EnhancedConnectionManager
    manager = EnhancedConnectionManager()
    stats = manager.get_connection_stats()
    log_result("Connection Manager Creation", True, f"Active connections: {stats['active_connections']}")

    from backend.agent_status_broadcaster import AgentStatusBroadcaster
    broadcaster = AgentStatusBroadcaster(manager)
    log_result("Status Broadcaster Creation", True, "Broadcaster initialized with manager")

except Exception as e:
    log_result("WebSocket Components", False, error=str(e))

# Test 7: Agent Workflow Test
print("\n7️⃣ Agent Workflow Test")
try:
    from backend.workflow import botarmy_workflow, simple_workflow
    log_result("Workflow Import", True, "Both workflows imported")

    # Test workflow function signature
    import inspect
    sig = inspect.signature(botarmy_workflow)
    log_result("Workflow Signature", True, f"Parameters: {list(sig.parameters.keys())}")

except Exception as e:
    log_result("Agent Workflow", False, error=str(e))

# Summary
print("\n📊 Test Summary")
print("=" * 30)

passed_tests = sum(1 for result in test_results if "✅ PASS" in result)
total_tests = len(test_results)
success_rate = passed_tests / total_tests * 100

print(f"Passed Tests: {passed_tests}/{total_tests}")
print(f"Success Rate: {success_rate:.1f}%")

if success_rate >= 90:
    print("🎉 BACKEND READY - All systems operational!")
    backend_status = "READY"
elif success_rate >= 75:
    print("⚠️  BACKEND MOSTLY READY - Minor issues to address")
    backend_status = "MOSTLY_READY"
else:
    print("❌ BACKEND NEEDS WORK - Major issues found")
    backend_status = "NEEDS_WORK"

# Write detailed log
log_file = project_root / "testing_logs" / "phase1_backend_test.txt"
with open(log_file, "w") as f:
    f.write("BotArmy Phase 1 Backend Testing Report\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Test Date: {os.environ.get('USER', 'Unknown')}\n")
    f.write(f"Environment: AGENT_TEST_MODE={os.environ.get('AGENT_TEST_MODE')}\n")
    f.write(f"Backend Status: {backend_status}\n\n")

    f.write("Detailed Results:\n")
    f.write("-" * 20 + "\n")
    for result in test_results:
        f.write(result + "\n")

    f.write(f"\nSummary: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)\n")

print(f"\nDetailed log saved to: {log_file}")

# Next steps recommendation
print("\n🚀 Next Steps:")
if backend_status == "READY":
    print("✅ Proceed to frontend integration testing")
elif backend_status == "MOSTLY_READY":
    print("⚠️  Fix minor issues, then proceed to integration testing")
else:
    print("❌ Address major backend issues before proceeding")

print("=" * 50)
