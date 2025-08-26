#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Setup environment
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

# Load environment
from dotenv import load_dotenv
load_dotenv()

results = []

# Test critical backend imports
print("Testing Jules' Backend Components...")

try:
    from fastapi import FastAPI
    results.append("✅ FastAPI")
except:
    results.append("❌ FastAPI")

try:
    from backend.runtime_env import IS_REPLIT
    results.append("✅ Runtime Environment")
except:
    results.append("❌ Runtime Environment")

try:
    from backend.connection_manager import EnhancedConnectionManager
    results.append("✅ Connection Manager")
except:
    results.append("❌ Connection Manager")

try:
    from backend.agent_status_broadcaster import AgentStatusBroadcaster
    results.append("✅ Status Broadcaster")
except:
    results.append("❌ Status Broadcaster")

try:
    from backend.services.llm_service import get_llm_service
    results.append("✅ LLM Service")
except:
    results.append("❌ LLM Service")

try:
    from backend.agents.base_agent import BaseAgent
    results.append("✅ Base Agent")
except:
    results.append("❌ Base Agent")

try:
    from backend.agui.protocol import agui_handler
    results.append("✅ AGUI Protocol")
except:
    results.append("❌ AGUI Protocol")

try:
    from backend.workflow import botarmy_workflow
    results.append("✅ Workflow")
except:
    results.append("❌ Workflow")

try:
    from backend.main_simple import app
    results.append("✅ Simple Backend")
except:
    results.append("❌ Simple Backend")

try:
    from backend.main import app
    results.append("✅ Full Backend")
except:
    results.append("❌ Full Backend")

# Output results
for result in results:
    print(result)

passed = sum(1 for r in results if "✅" in r)
total = len(results)
rate = (passed/total)*100

print(f"\nResults: {passed}/{total} ({rate:.1f}%)")

# Brake verification
print(f"\nBrake Status:")
print(f"AGENT_TEST_MODE: {os.getenv('AGENT_TEST_MODE')}")
print(f"TEST_MODE: {os.getenv('TEST_MODE')}")

# Write results to file
with open("testing_logs/manual_import_test.txt", "w") as f:
    f.write("Manual Backend Import Test Results\n")
    f.write("=" * 40 + "\n")
    for result in results:
        f.write(result + "\n")
    f.write(f"\nSuccess Rate: {rate:.1f}% ({passed}/{total})\n")
    f.write(f"AGENT_TEST_MODE: {os.getenv('AGENT_TEST_MODE')}\n")
    f.write(f"TEST_MODE: {os.getenv('TEST_MODE')}\n")

print("Results saved to testing_logs/manual_import_test.txt")
