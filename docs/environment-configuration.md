# BotArmy Environment Configuration Guide

## 📁 **Environment Files Overview**

BotArmy uses two separate environment files with different purposes:

| File | Purpose | Read By | Contains |
|------|---------|---------|----------|
| **`backend/.env`** | Backend configuration | Python backend | API keys, agent modes, HITL settings |
| **`.env.local`** | Frontend configuration | Next.js frontend | Connection URLs, UI settings |

## 🔧 **Backend Configuration (`backend/.env`)**

### **Agent Operation Modes** (Choose One)

#### **1. FULL TEST MODE** 
```bash
AGENT_TEST_MODE=true
ROLE_TEST_MODE=false
```
- **Purpose**: UI/workflow testing without API costs
- **Behavior**: Static role confirmations, no LLM calls
- **Cost**: $0
- **Use Case**: Testing UI, workflow logic, debugging

#### **2. ROLE CONFIRMATION MODE** ⭐ **Recommended for Testing**
```bash
AGENT_TEST_MODE=false
ROLE_TEST_MODE=true
```
- **Purpose**: Safe LLM integration testing
- **Behavior**: Real LLM calls for role confirmation only
- **Cost**: ~$0.01-0.05 per workflow (5 agents × 1 call each)
- **Use Case**: Testing LLM connectivity, validating API keys

#### **3. NORMAL MODE** 
```bash
AGENT_TEST_MODE=false
ROLE_TEST_MODE=false
```
- **Purpose**: Full production workflows
- **Behavior**: Complete SDLC processing with many LLM calls
- **Cost**: $0.50-5.00+ per workflow (hundreds of LLM calls)
- **Use Case**: Production use, full agent functionality

### **Human-in-the-Loop (HITL) Settings**

Only applies in **NORMAL MODE**:

#### **Fully Automatic** (Default)
```bash
ENABLE_HITL=false
AUTO_ACTION=none
```
- Agents run without human interaction
- Fastest execution, no interruptions

#### **Manual Approval**
```bash
ENABLE_HITL=true
AUTO_ACTION=none
```
- Agents pause and wait for human approval at each step
- Maximum control, slower execution
- Requires UI interaction to approve/reject

#### **Simulated Approval** (Testing)
```bash
ENABLE_HITL=true
AUTO_ACTION=approve
```
- Agents simulate human approval automatically
- Tests HITL workflow without manual interaction

## 🌐 **Frontend Configuration (`.env.local`)**

### **Connection Settings**
```bash
# Backend connection URLs - update these if backend runs on different port
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/api/ws
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### **Development Settings**
```bash
# Enable development features and detailed logging
NEXT_DEV=true
NEXT_PUBLIC_DEBUG=true
NEXT_PUBLIC_ENVIRONMENT=development
```

## 🎯 **Common Configuration Scenarios**

### **Scenario 1: First-Time Setup Testing**
*Goal: Test that everything works without spending money*

**Backend (.env):**
```bash
AGENT_TEST_MODE=true
ROLE_TEST_MODE=false
ENABLE_HITL=false
```
**Result**: Static responses, no API calls, $0 cost

### **Scenario 2: LLM Integration Testing**
*Goal: Test OpenAI connectivity safely*

**Backend (.env):**
```bash
AGENT_TEST_MODE=false
ROLE_TEST_MODE=true
ENABLE_HITL=false
```
**Result**: Real LLM role confirmations, minimal cost (~$0.05)

### **Scenario 3: Full Workflow with Human Oversight**
*Goal: Production use with human approval*

**Backend (.env):**
```bash
AGENT_TEST_MODE=false
ROLE_TEST_MODE=false
ENABLE_HITL=true
AUTO_ACTION=none
```
**Result**: Full SDLC processing, pauses for approval, high cost

### **Scenario 4: Full Automatic Production**
*Goal: Production use without human interaction*

**Backend (.env):**
```bash
AGENT_TEST_MODE=false
ROLE_TEST_MODE=false
ENABLE_HITL=false
AUTO_ACTION=none
```
**Result**: Full SDLC processing, no pauses, high cost

## ⚠️ **Important Notes**

### **API Key Security**
- **Never** put API keys in `.env.local` (frontend file)
- **Always** put API keys in `backend/.env` (backend file)
- Frontend variables with `NEXT_PUBLIC_` are visible to users

### **Cost Management**
- **ROLE_TEST_MODE**: ~$0.01-0.05 per workflow (safe for testing)
- **NORMAL_MODE**: $0.50-5.00+ per workflow (expensive, use carefully)
- **TEST_MODE**: $0 (no API calls)

### **File Locations**
```
botarmy/
├── backend/
│   └── .env          ← Backend configuration (API keys, agent modes)
├── .env.local        ← Frontend configuration (URLs, UI settings)
└── README.md
```

### **Environment Loading**
- Backend reads `backend/.env` on startup
- Frontend reads `.env.local` during build/runtime
- Both files must exist for proper operation

## 🔄 **Changing Modes**

To switch between modes:

1. **Edit the appropriate `.env` file**
2. **Restart the backend**: `python backend/start_backend.py`
3. **Check startup logs** for mode confirmation:
   - `🧪 TEST_MODE enabled...`
   - `🎯 ROLE_TEST_MODE enabled...`
   - `🔥 NORMAL_MODE active...`

## 🆘 **Troubleshooting**

### **Backend won't start / wrong mode**
- Check `backend/.env` exists and has correct values
- Restart backend after changing variables
- Look for mode confirmation in startup logs

### **Frontend can't connect**
- Check `.env.local` has correct WebSocket URL
- Ensure backend is running on specified port
- Verify no firewall blocking connections

### **No LLM responses**
- Check `OPENAI_API_KEY` is set in `backend/.env`
- Verify API key is valid and has credits
- Check if in TEST_MODE (no LLM calls by design)

### **Unexpected behavior**
- Compare your settings with the scenarios above
- Ensure only one agent mode is enabled at a time
- Check both environment files for conflicts