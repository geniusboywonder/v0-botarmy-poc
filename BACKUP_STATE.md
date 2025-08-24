# BotArmy State Backup - Pre-HITL Merge

**Date:** August 22, 2025
**Current Branch:** main
**Purpose:** Backup before merging origin/feature/human-in-the-loop

## Current Working State

### Backend Structure
```
backend/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── analyst_agent.py
│   ├── architect_agent.py
│   ├── developer_agent.py
│   ├── tester_agent.py
│   └── deployer_agent.py
├── agui/
│   ├── __init__.py
│   └── protocol.py
├── services/
│   └── llm_service.py
├── main.py
├── workflow.py
└── bridge.py
```

### Frontend Structure
```
app/
├── dashboard/
├── components/
├── lib/
│   ├── stores/
│   └── websocket/
└── hooks/
```

### Key Files to Monitor During Merge
- main.py (core application)
- workflow.py (orchestration)
- agents/base_agent.py (agent core)
- lib/websocket/websocket-service.ts (frontend WS)
- lib/stores/ (state management)

### Current Functionality (Baseline)
- [x] Basic agent workflow execution
- [x] WebSocket communication
- [x] Simple UI with dashboard
- [x] Replit deployment working
- [x] Basic state management

### Environment
- Python 3.11+ (Replit environment)
- Node.js for frontend
- Current deployment: Replit

## Rollback Instructions
If merge fails:
1. `git checkout main`
2. `git reset --hard HEAD`
3. Restore from this backup state
4. Test basic functionality with current scripts
