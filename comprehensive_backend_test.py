#!/usr/bin/env python3
"""
Backend Issues Identification Script
Creates a detailed log of what works and what doesn't
"""

import os
import sys
from pathlib import Path
import traceback

# Setup paths and environment
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Set safe testing environment
os.environ["AGENT_TEST_MODE"] = "true"  # Enable test mode for safe testing

# Initialize results log
results_log = []

def test_and_log(test_name, test_func):
    """Test a function and log results"""
    try:
        result = test_func()
        results_log.append(f"✅ {test_name}: PASS - {result}")
        return True
    except Exception as e:
        results_log.append(f"❌ {test_name}: FAIL - {str(e)}")
        results_log.append(f"   Traceback: {traceback.format_exc().split(chr(10))[-2].strip()}")
        return False

def test_basic_imports():
    """Test basic Python imports"""
    from fastapi import FastAPI
    import uvicorn
    from dotenv import load_dotenv
    return "Basic imports working"

def test_backend_runtime():
    """Test backend runtime environment detection"""
    from backend.runtime_env import IS_REPLIT, get_environment_info
    env_info = get_environment_info()
    return f"Environment: {env_info.get('is_replit', 'unknown')}"

def test_agui_protocol():
    """Test AGUI protocol functionality"""
    from backend.agui.protocol import agui_handler
    test_msg = agui_handler.create_agent_message(
        content="Test message",
        agent_name="TestAgent",
        session_id="test_session"
    )
    return "AGUI message creation works"

def test_connection_manager():
    """Test connection manager initialization"""
    from backend.connection_manager import EnhancedConnectionManager
    manager = EnhancedConnectionManager()
    stats = manager.get_connection_stats()
    return f"Manager initialized, {stats['active_connections']} connections"

def test_status_broadcaster():
    """Test status broadcaster functionality"""
    from backend.agent_status_broadcaster import AgentStatusBroadcaster
    broadcaster = AgentStatusBroadcaster()
    return "Status broadcaster initialized"

def test_workflow_import():
    """Test workflow module import"""
    from backend.workflow import botarmy_workflow, simple_workflow
    return "Workflow functions imported"

def test_error_handler():
    """Test error handler functionality"""
    from backend.error_handler import ErrorHandler, error_handler
    stats = error_handler.get_error_statistics()
    return f"Error handler working, {stats['total_errors']} total errors logged"

def test_human_input_handler():
    """Test human input handler import"""
    from backend.human_input_handler import request_human_approval
    return "Human input handler imported"

def test_main_simple():
    """Test main_simple backend import"""
    from backend.main_simple import app
    return "Simple backend app imported"

def test_main_full():
    """Test main backend import"""
    from backend.main import app
    return "Full backend app imported"

# Run all tests
results_log.append("BotArmy Backend Testing Report")
results_log.append("=" * 50)
results_log.append(f"Test Date: {os.environ.get('USER', 'Unknown User')}")
results_log.append(f"Environment: AGENT_TEST_MODE={os.environ.get('AGENT_TEST_MODE', 'not_set')}")
results_log.append("")

tests = [
    ("Basic Python Imports", test_basic_imports),
    ("Backend Runtime Environment", test_backend_runtime),
    ("AGUI Protocol", test_agui_protocol),
    ("Connection Manager", test_connection_manager),
    ("Status Broadcaster", test_status_broadcaster),
    ("Workflow Import", test_workflow_import),
    ("Error Handler", test_error_handler),
    ("Human Input Handler", test_human_input_handler),
    ("Main Simple Backend", test_main_simple),
    ("Main Full Backend", test_main_full),
]

# Execute tests
passed_tests = 0
total_tests = len(tests)

for test_name, test_func in tests:
    if test_and_log(test_name, test_func):
        passed_tests += 1

# Summary
results_log.append("")
results_log.append("Test Summary:")
results_log.append(f"Passed: {passed_tests}/{total_tests}")
results_log.append(f"Success Rate: {passed_tests/total_tests*100:.1f}%")

if passed_tests == total_tests:
    results_log.append("")
    results_log.append("🎉 ALL TESTS PASSED - Backend is ready for startup!")
elif passed_tests >= total_tests * 0.8:
    results_log.append("")
    results_log.append("⚠️  MOSTLY WORKING - Minor issues to fix")
else:
    results_log.append("")
    results_log.append("❌ MAJOR ISSUES FOUND - Needs attention")

# Write results to file
output_file = project_root / "testing_logs" / "backend_test_report.txt"
with open(output_file, "w") as f:
    for line in results_log:
        print(line)  # Also print to console
        f.write(line + "\n")

print(f"\nFull report saved to: {output_file}")
