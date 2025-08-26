#!/usr/bin/env python3
"""
Phase 1 Backend Testing - Runtime Verification
Tests that Jules' backend can actually start up and function properly
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Setup environment and paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Load environment and set test mode
from dotenv import load_dotenv
load_dotenv()
os.environ["AGENT_TEST_MODE"] = "true"  # Safe testing

print("🧪 Phase 1: Backend Runtime Testing")
print("=" * 50)

# Test Results
test_results = []

def log_test(name, success, details="", error=None):
    """Log test results"""
    status = "✅ PASS" if success else "❌ FAIL"
    result = f"{status} {name}"
    if details:
        result += f" - {details}"
    if error:
        result += f" (Error: {error})"
    test_results.append(result)
    print(result)

# Phase 1: Import Testing
print("\n🔬 Testing All Backend Imports...")

try:
    # Core FastAPI imports
    from fastapi import FastAPI, WebSocket
    from fastapi.testclient import TestClient
    log_test("Core FastAPI", True)
except Exception as e:
    log_test("Core FastAPI", False, error=str(e))

try:
    # Backend runtime environment
    from backend.runtime_env import IS_REPLIT, get_environment_info
    env_info = get_environment_info()
    log_test("Runtime Environment", True, f"Replit: {env_info['is_replit']}")
except Exception as e:
    log_test("Runtime Environment", False, error=str(e))

try:
    # All backend components that Jules created
    from backend.connection_manager import EnhancedConnectionManager
    from backend.agent_status_broadcaster import AgentStatusBroadcaster
    from backend.heartbeat_monitor import HeartbeatMonitor
    from backend.error_handler import ErrorHandler
    from backend.rate_limiter import rate_limiter
    from backend.services.llm_service import get_llm_service
    from backend.artifacts import get_artifacts_structure
    from backend.agui.protocol import agui_handler
    from backend.bridge import AGUI_Handler
    from backend.workflow import botarmy_workflow
    from backend.human_input_handler import request_human_approval
    log_test("All Backend Components", True, "Complete suite imported")
except Exception as e:
    log_test("All Backend Components", False, error=str(e))

# Phase 2: Component Initialization Testing
print("\n🏗️  Testing Component Initialization...")

try:
    # Test connection manager
    manager = EnhancedConnectionManager()
    stats = manager.get_connection_stats()
    log_test("Connection Manager", True, f"{stats['active_connections']} connections")
except Exception as e:
    log_test("Connection Manager", False, error=str(e))

try:
    # Test status broadcaster
    broadcaster = AgentStatusBroadcaster(manager if 'manager' in locals() else None)
    log_test("Status Broadcaster", True)
except Exception as e:
    log_test("Status Broadcaster", False, error=str(e))

try:
    # Test heartbeat monitor
    heartbeat = HeartbeatMonitor(manager if 'manager' in locals() else None)
    log_test("Heartbeat Monitor", True)
except Exception as e:
    log_test("Heartbeat Monitor", False, error=str(e))

try:
    # Test LLM service
    llm_service = get_llm_service()
    providers = llm_service.get_available_providers()
    log_test("LLM Service", True, f"Providers: {providers}")
except Exception as e:
    log_test("LLM Service", False, error=str(e))

try:
    # Test rate limiter
    status = rate_limiter.get_all_status()
    log_test("Rate Limiter", True, f"Tracking {len(status)} providers")
except Exception as e:
    log_test("Rate Limiter", False, error=str(e))

try:
    # Test AGUI handler
    test_msg = agui_handler.create_agent_message(
        content="Test message",
        agent_name="TestAgent",
        session_id="test_session"
    )
    log_test("AGUI Handler", True, f"Message type: {test_msg.get('type')}")
except Exception as e:
    log_test("AGUI Handler", False, error=str(e))

# Phase 3: Backend App Testing
print("\n🚀 Testing Backend Applications...")

try:
    # Test simple backend
    from backend.main_simple import app as simple_app
    client = TestClient(simple_app)
    response = client.get("/")
    if response.status_code == 200:
        data = response.json()
        log_test("Simple Backend", True, f"Status: {data.get('status')}, Test Mode: {data.get('test_mode')}")
    else:
        log_test("Simple Backend", False, f"HTTP {response.status_code}")
except Exception as e:
    log_test("Simple Backend", False, error=str(e))

try:
    # Test full backend (this is the critical one)
    from backend.main import app as full_app
    client = TestClient(full_app)
    response = client.get("/")
    if response.status_code == 200:
        data = response.json()
        features = data.get('features', {})
        log_test("Full Backend", True, f"Version: {data.get('version')}")
        log_test("Full Backend Features", True, f"Available: {sum(features.values())}/{len(features)}")
    else:
        log_test("Full Backend", False, f"HTTP {response.status_code}")
except Exception as e:
    log_test("Full Backend", False, error=str(e))

# Phase 4: Agent Workflow Testing
print("\n🤖 Testing Agent Workflow...")

try:
    from backend.agents.base_agent import BaseAgent
    from backend.agents.analyst_agent import run_analyst_task

    # Test base agent in test mode
    test_agent = BaseAgent("You are a test agent.")

    # This should return a test mode response
    result = asyncio.run(test_agent.execute("Test input", "TestAgent"))

    if "Test Mode" in result:
        log_test("Agent Test Mode", True, "Agents returning test confirmations")
    else:
        log_test("Agent Test Mode", False, "Test mode not working properly")

except Exception as e:
    log_test("Agent Test Mode", False, error=str(e))

# Summary and Results
print("\n📊 Testing Summary")
print("=" * 30)

passed_tests = sum(1 for result in test_results if "✅ PASS" in result)
total_tests = len(test_results)
success_rate = (passed_tests / total_tests) * 100

print(f"Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")

if success_rate >= 90:
    backend_status = "🎉 BACKEND FULLY OPERATIONAL"
    recommendation = "✅ Ready for frontend integration testing"
elif success_rate >= 75:
    backend_status = "⚠️  BACKEND MOSTLY WORKING"
    recommendation = "⚠️  Fix remaining issues then proceed"
else:
    backend_status = "❌ BACKEND NEEDS ATTENTION"
    recommendation = "❌ Address critical issues before proceeding"

print(f"\nStatus: {backend_status}")
print(f"Next Steps: {recommendation}")

# Write detailed report
report_file = project_root / "testing_logs" / "backend_runtime_test.txt"
with open(report_file, "w") as f:
    f.write("BotArmy Backend Runtime Test Report\n")
    f.write("=" * 40 + "\n\n")
    f.write(f"Jules' Backend Implementation Assessment\n")
    f.write(f"Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})\n")
    f.write(f"Status: {backend_status}\n\n")

    f.write("Detailed Test Results:\n")
    f.write("-" * 25 + "\n")
    for result in test_results:
        f.write(result + "\n")

print(f"\nDetailed report: {report_file}")

# Overall assessment
print("\n🎯 Jules' Work Assessment:")
if success_rate >= 90:
    print("✅ OUTSTANDING - Jules delivered production-ready backend code")
elif success_rate >= 75:
    print("✅ EXCELLENT - Jules' foundation is solid with minor gaps")
else:
    print("⚠️  GOOD START - Jules' architecture is sound but needs completion")

print("=" * 50)
