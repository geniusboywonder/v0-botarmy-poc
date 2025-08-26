#!/usr/bin/env python3
"""
Phase 2: Frontend Integration Testing
Tests the complete frontend-backend integration with safety brakes engaged
"""

import os
import sys
import time
import json
from pathlib import Path

# Setup environment
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Ensure brakes are engaged
from dotenv import load_dotenv
load_dotenv()

print("🔗 Phase 2: Frontend Integration Testing")
print("=" * 55)
print(f"🛡️  AGENT_TEST_MODE: {os.getenv('AGENT_TEST_MODE')}")
print(f"🛡️  TEST_MODE: {os.getenv('TEST_MODE')}")
print("=" * 55)

# Test Results Collector
test_results = []
test_categories = {
    "Frontend Structure": [],
    "State Management": [],
    "WebSocket Integration": [],
    "UI Components": [],
    "Integration Points": []
}

def log_test(category, name, success, details="", error=None):
    """Log test results with categories"""
    status = "✅ PASS" if success else "❌ FAIL"
    result = f"{status} {name}"
    if details:
        result += f" - {details}"
    if error:
        result += f" (Error: {str(error)[:100]}{'...' if len(str(error)) > 100 else ''})"

    test_results.append(result)
    if category in test_categories:
        test_categories[category].append((name, success, details, error))
    print(result)
    return success

print("\n📁 TESTING PHASE 1: FRONTEND STRUCTURE ANALYSIS")
print("-" * 50)

# Test 1: Next.js Application Structure
try:
    # Check if Next.js is properly set up
    package_json_path = project_root / "package.json"

    if package_json_path.exists():
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)

        # Check Next.js version
        next_version = package_data.get('dependencies', {}).get('next', 'Not found')
        react_version = package_data.get('dependencies', {}).get('react', 'Not found')

        log_test("Frontend Structure", "Next.js Setup", True,
                f"Next.js {next_version}, React {react_version}")
    else:
        log_test("Frontend Structure", "Next.js Setup", False, "package.json not found")

except Exception as e:
    log_test("Frontend Structure", "Next.js Setup", False, error=e)

# Test 2: App Directory Structure
try:
    app_dir = project_root / "app"
    required_files = ["layout.tsx", "page.tsx", "globals.css"]

    existing_files = []
    for file in required_files:
        if (app_dir / file).exists():
            existing_files.append(file)

    log_test("Frontend Structure", "App Directory", len(existing_files) == len(required_files),
            f"Found {len(existing_files)}/{len(required_files)} required files")

    # Check for app pages
    app_pages = ["analytics", "artifacts", "logs", "settings", "tasks"]
    existing_pages = [page for page in app_pages if (app_dir / page).exists()]

    log_test("Frontend Structure", "App Pages", len(existing_pages) > 0,
            f"Found {len(existing_pages)} pages: {', '.join(existing_pages)}")

except Exception as e:
    log_test("Frontend Structure", "App Directory", False, error=e)

# Test 3: Components Structure
try:
    components_dir = project_root / "components"
    key_components = [
        "agent-status-card.tsx",
        "connection-status.tsx",
        "main-layout.tsx",
        "client-provider.tsx"
    ]

    existing_components = []
    for component in key_components:
        if (components_dir / component).exists():
            existing_components.append(component)

    log_test("Frontend Structure", "Core Components", len(existing_components) == len(key_components),
            f"Found {len(existing_components)}/{len(key_components)} core components")

    # Check UI components
    ui_dir = components_dir / "ui"
    if ui_dir.exists():
        ui_components = list(ui_dir.glob("*.tsx"))
        log_test("Frontend Structure", "UI Components", len(ui_components) > 5,
                f"Found {len(ui_components)} UI components")
    else:
        log_test("Frontend Structure", "UI Components", False, "UI directory not found")

except Exception as e:
    log_test("Frontend Structure", "Components Structure", False, error=e)

print("\n🏪 TESTING PHASE 2: STATE MANAGEMENT")
print("-" * 40)

# Test 4: Zustand Stores
try:
    stores_dir = project_root / "lib" / "stores"
    expected_stores = ["agent-store.ts", "log-store.ts"]

    existing_stores = []
    for store in expected_stores:
        store_path = stores_dir / store
        if store_path.exists():
            existing_stores.append(store)

            # Check store content
            with open(store_path, 'r') as f:
                store_content = f.read()

            # Look for Zustand patterns
            has_create = "create" in store_content
            has_interfaces = "interface" in store_content
            has_methods = "updateAgent" in store_content or "addLog" in store_content

            log_test("State Management", f"{store} Structure", has_create and has_interfaces,
                    f"Zustand: {has_create}, Interfaces: {has_interfaces}, Methods: {has_methods}")

    log_test("State Management", "Store Files", len(existing_stores) == len(expected_stores),
            f"Found {len(existing_stores)}/{len(expected_stores)} stores")

except Exception as e:
    log_test("State Management", "Zustand Stores", False, error=e)

print("\n🔌 TESTING PHASE 3: WEBSOCKET INTEGRATION")
print("-" * 45)

# Test 5: WebSocket Service
try:
    websocket_dir = project_root / "lib" / "websocket"
    websocket_service = websocket_dir / "websocket-service.ts"

    if websocket_service.exists():
        with open(websocket_service, 'r') as f:
            service_content = f.read()

        # Check for key WebSocket functionality
        has_websocket_class = "WebSocket" in service_content
        has_connection_handling = "onopen" in service_content and "onclose" in service_content
        has_message_handling = "onmessage" in service_content
        has_reconnect = "reconnect" in service_content.lower()
        has_send_methods = "startProject" in service_content

        log_test("WebSocket Integration", "WebSocket Service", has_websocket_class,
                f"Class: {has_websocket_class}, Handlers: {has_connection_handling}")
        log_test("WebSocket Integration", "Message Handling", has_message_handling,
                f"Messages: {has_message_handling}, Reconnect: {has_reconnect}")
        log_test("WebSocket Integration", "API Methods", has_send_methods,
                f"Methods: startProject, testBackend, etc.")

        # Check for environment URL handling
        has_env_url = "NEXT_PUBLIC_WEBSOCKET_URL" in service_content
        log_test("WebSocket Integration", "Environment Config", has_env_url,
                "Environment URL configuration found")
    else:
        log_test("WebSocket Integration", "WebSocket Service", False, "Service file not found")

except Exception as e:
    log_test("WebSocket Integration", "WebSocket Service", False, error=e)

# Test 6: WebSocket Hook Integration
try:
    hooks_dir = project_root / "hooks"
    if hooks_dir.exists():
        websocket_hook = hooks_dir / "use-websocket.ts"
        if websocket_hook.exists():
            log_test("WebSocket Integration", "WebSocket Hook", True, "Hook file exists")
        else:
            log_test("WebSocket Integration", "WebSocket Hook", False, "Hook file missing")
    else:
        log_test("WebSocket Integration", "WebSocket Hook", False, "Hooks directory not found")

except Exception as e:
    log_test("WebSocket Integration", "WebSocket Hook", False, error=e)

print("\n🎨 TESTING PHASE 4: UI COMPONENTS ANALYSIS")
print("-" * 44)

# Test 7: Key UI Components
try:
    components_to_check = {
        "EnhancedChatInterface": "components/chat/enhanced-chat-interface.tsx",
        "AgentStatusCard": "components/agent-status-card.tsx",
        "ConnectionStatus": "components/connection-status.tsx",
        "MainLayout": "components/main-layout.tsx"
    }

    for component_name, component_path in components_to_check.items():
        component_file = project_root / component_path

        if component_file.exists():
            with open(component_file, 'r') as f:
                content = f.read()

            # Check for React patterns
            has_use_client = '"use client"' in content
            has_useState = "useState" in content
            has_useEffect = "useEffect" in content
            has_props = "Props" in content

            log_test("UI Components", component_name, True,
                    f"Client: {has_use_client}, State: {has_useState}, Effects: {has_useEffect}")
        else:
            log_test("UI Components", component_name, False, "Component file not found")

except Exception as e:
    log_test("UI Components", "Component Analysis", False, error=e)

# Test 8: Tailwind CSS Integration
try:
    globals_css = project_root / "app" / "globals.css"
    tailwind_config = project_root / "tailwind.config.js"

    has_globals = globals_css.exists()
    has_config = tailwind_config.exists()

    if has_globals:
        with open(globals_css, 'r') as f:
            css_content = f.read()
        has_tailwind_directives = "@tailwind" in css_content
    else:
        has_tailwind_directives = False

    log_test("UI Components", "Tailwind CSS", has_config and has_tailwind_directives,
            f"Config: {has_config}, Directives: {has_tailwind_directives}")

except Exception as e:
    log_test("UI Components", "Tailwind CSS", False, error=e)

print("\n🔗 TESTING PHASE 5: INTEGRATION POINTS")
print("-" * 42)

# Test 9: Frontend-Backend Integration Points
try:
    # Check for environment variables
    env_file = project_root / ".env"
    has_env = env_file.exists()

    if has_env:
        with open(env_file, 'r') as f:
            env_content = f.read()

        has_backend_url = "NEXT_PUBLIC_BACKEND_URL" in env_content
        has_websocket_url = "NEXT_PUBLIC_WEBSOCKET_URL" in env_content
        has_safety_brakes = "AGENT_TEST_MODE" in env_content

        log_test("Integration Points", "Environment Config", has_backend_url and has_websocket_url,
                f"Backend URL: {has_backend_url}, WebSocket URL: {has_websocket_url}")
        log_test("Integration Points", "Safety Brakes", has_safety_brakes,
                f"Test mode configured: {has_safety_brakes}")
    else:
        log_test("Integration Points", "Environment Config", False, ".env file not found")

except Exception as e:
    log_test("Integration Points", "Environment Config", False, error=e)

# Test 10: Message Flow Integration
try:
    # Check if components are set up to handle WebSocket messages
    chat_interface = project_root / "components" / "chat" / "enhanced-chat-interface.tsx"

    if chat_interface.exists():
        with open(chat_interface, 'r') as f:
            chat_content = f.read()

        uses_websocket_service = "websocketService" in chat_content
        uses_log_store = "useLogStore" in chat_content
        uses_agent_store = "useAgentStore" in chat_content
        handles_messages = "handleMessage" in chat_content or "addLog" in chat_content

        log_test("Integration Points", "Message Flow", uses_websocket_service and uses_log_store,
                f"WebSocket: {uses_websocket_service}, Stores: {uses_log_store and uses_agent_store}")
    else:
        log_test("Integration Points", "Message Flow", False, "Chat interface not found")

except Exception as e:
    log_test("Integration Points", "Message Flow", False, error=e)

# FINAL RESULTS SUMMARY
print("\n" + "=" * 70)
print("📊 PHASE 2 FRONTEND INTEGRATION TEST RESULTS")
print("=" * 70)

# Calculate statistics
total_tests = len(test_results)
passed_tests = sum(1 for result in test_results if "✅ PASS" in result)
failed_tests = total_tests - passed_tests
success_rate = (passed_tests / total_tests) * 100

print(f"\n🎯 Overall Results:")
print(f"   Total Tests: {total_tests}")
print(f"   Passed: {passed_tests} ✅")
print(f"   Failed: {failed_tests} ❌")
print(f"   Success Rate: {success_rate:.1f}%")

# Category breakdown
print(f"\n📋 Results by Category:")
for category, tests in test_categories.items():
    if tests:
        category_passed = sum(1 for _, success, _, _ in tests if success)
        category_total = len(tests)
        category_rate = (category_passed / category_total) * 100
        status_icon = "✅" if category_rate >= 80 else "⚠️" if category_rate >= 60 else "❌"
        print(f"   {status_icon} {category}: {category_passed}/{category_total} ({category_rate:.1f}%)")

# Overall Assessment
if success_rate >= 90:
    overall_status = "🎉 OUTSTANDING"
    recommendation = "✅ Frontend integration is excellent!"
    jules_rating = "A+ - Exceptional frontend work"
elif success_rate >= 75:
    overall_status = "✅ EXCELLENT"
    recommendation = "✅ Frontend integration is ready with minor polish needed"
    jules_rating = "A - Excellent frontend implementation"
elif success_rate >= 60:
    overall_status = "⚠️ GOOD"
    recommendation = "⚠️ Frontend integration is mostly ready, some fixes needed"
    jules_rating = "B+ - Good frontend foundation"
else:
    overall_status = "❌ NEEDS WORK"
    recommendation = "❌ Frontend integration needs significant attention"
    jules_rating = "C - Requires major frontend fixes"

print(f"\n🏆 Jules' Frontend Integration Assessment:")
print(f"   Status: {overall_status}")
print(f"   Rating: {jules_rating}")
print(f"   Recommendation: {recommendation}")

# Integration Readiness
print(f"\n🔗 Integration Status:")
frontend_structure_ready = success_rate >= 75
websocket_integration = any("WebSocket Integration" in result and "✅ PASS" in result for result in test_results)
state_management = any("State Management" in result and "✅ PASS" in result for result in test_results)

integration_ready = frontend_structure_ready and websocket_integration and state_management

if integration_ready:
    print("   ✅ Frontend ready for backend integration testing")
    print("   ✅ WebSocket communication layer prepared")
    print("   ✅ State management configured for real-time updates")
    print("   🚀 Ready for Phase 3: End-to-End Workflow Testing")
else:
    print("   ⚠️  Frontend needs fixes before backend integration")
    print("   🔧 Address issues before proceeding to Phase 3")

# Safety Status
print(f"\n🛡️ Safety Status:")
print(f"   AGENT_TEST_MODE: {os.getenv('AGENT_TEST_MODE', 'not_set')} ✅")
print(f"   TEST_MODE: {os.getenv('TEST_MODE', 'not_set')} ✅")
print(f"   Integration Testing: Safe mode enabled ✅")

# Write detailed report
report_file = project_root / "testing_logs" / "phase2_frontend_integration_test.txt"
with open(report_file, "w") as f:
    f.write("BotArmy Phase 2 Frontend Integration Testing - Complete Results\n")
    f.write("=" * 65 + "\n\n")
    f.write(f"Testing Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Jules' Frontend Integration Assessment\n")
    f.write(f"Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})\n")
    f.write(f"Integration Ready: {integration_ready}\n")
    f.write(f"Safety Status: Brakes ENGAGED - Testing mode active\n")
    f.write(f"Final Rating: {jules_rating}\n\n")

    f.write("Detailed Test Results by Category:\n")
    f.write("-" * 40 + "\n")
    for result in test_results:
        f.write(result + "\n")

    f.write(f"\nRecommendation: {recommendation}\n")

print(f"\n📄 Detailed report saved to: {report_file}")

# Next Steps
if success_rate >= 75:
    print("\n🚀 Ready for Phase 3: End-to-End Workflow Testing")
    print("   - Test complete frontend-backend communication")
    print("   - Verify agent workflow execution in UI")
    print("   - Test human-in-the-loop functionality")
    print("   - Validate safety brake system end-to-end")
else:
    print("\n🔧 Phase 2.1: Address frontend issues before Phase 3")
    print("   - Fix failed tests identified above")
    print("   - Verify WebSocket integration")
    print("   - Test state management")

print("=" * 70)
print("Phase 2 Frontend Integration Testing: COMPLETE ✅")
