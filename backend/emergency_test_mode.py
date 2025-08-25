"""
Emergency Test Mode Activation Script
This will enable test mode to stop the infinite agent loop.
"""

import os

# Set test mode environment variables
os.environ["AGENT_TEST_MODE"] = "true"
os.environ["ROLE_TEST_MODE"] = "false" 
os.environ["ENABLE_HITL"] = "false"

print("🧪 EMERGENCY TEST MODE ACTIVATED")
print("   - AGENT_TEST_MODE=true (agents return static responses)")
print("   - ROLE_TEST_MODE=false") 
print("   - ENABLE_HITL=false")
print("")
print("This will prevent infinite loops in agent responses.")
print("Restart your backend server to apply these settings.")
print("")
print("To restore normal mode later:")
print('   - Set AGENT_TEST_MODE=false')
print('   - Set ROLE_TEST_MODE=false')
print('   - Set ENABLE_HITL=true')
