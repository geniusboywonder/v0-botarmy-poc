"""
Utility script to reset all agent call counters and manage safety limits.
"""

import logging
from backend.agents.analyst_agent import reset_analyst_call_count, get_analyst_call_count
from backend.agents.architect_agent import reset_architect_call_count, get_architect_call_count  
from backend.agents.developer_agent import reset_developer_call_count, get_developer_call_count
from backend.agents.tester_agent import reset_tester_call_count, get_tester_call_count
from backend.agents.deployer_agent import reset_deployer_call_count, get_deployer_call_count

logger = logging.getLogger(__name__)

def reset_all_agent_counters():
    """Reset all agent call counters to 0"""
    logger.info("🔄 Resetting all agent call counters...")
    
    reset_analyst_call_count()
    reset_architect_call_count() 
    reset_developer_call_count()
    reset_tester_call_count()
    reset_deployer_call_count()
    
    logger.info("✅ All agent call counters reset to 0")

def get_all_call_counts():
    """Get current call counts for all agents"""
    counts = {
        "analyst": get_analyst_call_count(),
        "architect": get_architect_call_count(),
        "developer": get_developer_call_count(),
        "tester": get_tester_call_count(),
        "deployer": get_deployer_call_count()
    }
    
    total_calls = sum(counts.values())
    logger.info(f"📊 Current call counts: {counts} (Total: {total_calls})")
    
    return counts

if __name__ == "__main__":
    print("🔄 Agent Call Counter Management")
    print("=" * 40)
    
    # Show current counts
    print("Current call counts:")
    counts = get_all_call_counts()
    for agent, count in counts.items():
        print(f"  {agent.capitalize()}: {count}")
    
    print()
    
    # Reset all counters
    print("Resetting all counters...")
    reset_all_agent_counters()
    
    # Show new counts
    print("New call counts:")
    new_counts = get_all_call_counts()
    for agent, count in new_counts.items():
        print(f"  {agent.capitalize()}: {count}")
