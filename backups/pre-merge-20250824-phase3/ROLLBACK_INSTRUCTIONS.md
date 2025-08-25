# BotArmy Rollback Instructions

## Pre-Merge State Backup - August 24, 2025

### Current State When Backup Created:
- **Branch:** `feature/enhanced-hitl-integration-final` (Jules' completed work)
- **Status:** A+ EXCEPTIONAL integration ready for testing
- **Safety Brakes:** FULLY ENGAGED (TEST_MODE=true)
- **Components:** Frontend + Backend fully integrated

---

## 🚨 Emergency Rollback Procedure

### 1. Immediate Rollback to Current State
If something goes wrong during merge/integration:

```bash
# Navigate to project directory
cd "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

# Switch back to Jules' working branch
git checkout feature/enhanced-hitl-integration-final

# Reset any uncommitted changes
git reset --hard HEAD
git clean -fd

# Verify you're back to known good state
git branch --show-current  # Should show: feature/enhanced-hitl-integration-final
```

### 2. Restore Configuration Files
```bash
# Restore environment file (if needed)
cp "backups/pre-merge-20250824-phase3/env-backup.txt" .env

# Restore package.json (if corrupted)
cp "backups/pre-merge-20250824-phase3/package-json-backup.txt" package.json

# Restore requirements.txt (if corrupted)  
cp "backups/pre-merge-20250824-phase3/requirements-backup.txt" requirements.txt
```

### 3. Reinstall Dependencies
```bash
# Reinstall Node.js dependencies
npm install

# Reinstall Python dependencies (if virtual env active)
pip install -r requirements.txt
```

### 4. Verify Rollback Success

#### Test Backend:
```bash
cd backend
python main.py
# Should start without errors and show safety brake messages
```

#### Test Frontend:
```bash
npm run dev
# Should start on http://localhost:3000
```

#### Test WebSocket Connection:
- Open frontend at localhost:3000
- Check connection status - should show "Connected"
- Try sending a test message
- Should see safety brake confirmations

### 5. Confirm Working State
✅ Backend starts on port 8000  
✅ Frontend starts on port 3000  
✅ WebSocket connection established  
✅ Safety brakes engaged (TEST_MODE=true)  
✅ Chat interface responds with test confirmations  
✅ No errors in console logs  

---

## 📋 State Information at Backup

### Environment Configuration:
- **TEST_MODE:** true (Safety brakes ON)
- **AGENT_TEST_MODE:** true (Mock responses)
- **ENABLE_HITL:** true (Human-in-the-loop enabled)
- **AUTO_ACTION:** none (Manual approval required)

### Key Files Present:
✅ `backend/main.py` - Backend server  
✅ `app/page.tsx` - Main dashboard  
✅ `lib/websocket/websocket-service.ts` - WebSocket service  
✅ `lib/stores/` - State management stores  
✅ `package.json` - Frontend dependencies  
✅ `requirements.txt` - Backend dependencies  

### Integration Status:
- **Frontend-Backend:** Fully integrated
- **WebSocket:** Professional implementation with auto-reconnect  
- **State Management:** Zustand stores working with real-time updates
- **UI Components:** shadcn/ui professional implementation
- **Safety Systems:** Comprehensive error handling and test mode

---

## 🆘 If Rollback Fails

### Last Resort Manual Recovery:
1. **Check backup files** in `backups/pre-merge-20250824-phase3/`
2. **Manually copy configuration** from backup files
3. **Reinstall from scratch** if needed:
   ```bash
   # Remove node_modules and reinstall
   rm -rf node_modules
   npm install
   
   # Remove Python cache and reinstall
   pip freeze > temp-requirements.txt
   pip uninstall -y -r temp-requirements.txt
   pip install -r requirements.txt
   ```

### Contact Information:
- **Backup Created:** Phase 3 - Pre-Merge Validation
- **Purpose:** Ensure rollback capability before integration testing
- **Status:** Jules' A+ work ready for merge to main

---

## ✅ Success Indicators After Rollback

You know rollback worked when:
- No error messages during startup
- Backend shows safety brake confirmations
- Frontend loads without hydration errors
- WebSocket connects successfully
- Chat interface responds with test messages
- All navigation pages load correctly

**Emergency resolved when you see the familiar safety brake messages and test mode confirmations.**
