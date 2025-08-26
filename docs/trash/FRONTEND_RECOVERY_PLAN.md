# BotArmy Frontend Recovery Plan

**Date**: August 23, 2025
**Issue**: Main codebase corrupted, build failures, UI broken
**Goal**: Restore working frontend from 2 days ago

---

## 🎯 RECOVERY STRATEGY

### **Phase 1: Diagnostic and Backup** ⏱️ 15 minutes

**Objective**: Understand what's broken and create safety nets

#### Step 1.1: Create Emergency Backup
```bash
# Create backup of current broken state
cp -r /Users/neill/Documents/AI Code/Projects/v0-botarmy-poc /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc-BROKEN-BACKUP

# Note: Keep this for analysis of what went wrong
```

#### Step 1.2: Identify Last Working Commit
```bash
cd /Users/neill/Documents/AI Code/Projects/v0-botarmy-poc

# Check git log for commit from 2 days ago (Aug 21)
git log --oneline --since="2025-08-21" --until="2025-08-22"

# Find the commit ID that represents working state
```

#### Step 1.3: Analyze Build Errors
```bash
# Run build to capture exact error messages
npm run build > build_errors.log 2>&1

# Check for specific import/TypeScript issues
npx tsc --noEmit > typescript_errors.log 2>&1
```

**Expected Issues to Find**:
- Missing workflow-store import
- TypeScript compilation errors
- Component import chain failures
- Theme provider configuration broken

---

### **Phase 2: Strategic Restoration** ⏱️ 30 minutes

**Objective**: Restore to last known working state using git

#### Option A: Git Reset (RECOMMENDED)
```bash
# Hard reset to last working commit
git log --oneline -20  # Find working commit from Aug 21
git reset --hard <WORKING_COMMIT_ID>

# Force push to update remote (CAUTION)
git push --force-with-lease origin main
```

#### Option B: Selective File Restoration
```bash
# If git reset too dangerous, restore key files only
git checkout <WORKING_COMMIT_ID> -- package.json
git checkout <WORKING_COMMIT_ID> -- package-lock.json
git checkout <WORKING_COMMIT_ID> -- app/
git checkout <WORKING_COMMIT_ID> -- components/
git checkout <WORKING_COMMIT_ID> -- lib/
git checkout <WORKING_COMMIT_ID> -- styles/
```

#### Option C: Branch Merge Recovery
```bash
# Check if working code exists in branches
git branch -a
git log origin/feature/human-in-the-loop --oneline -5

# Merge specific working branch if available
git checkout main
git merge origin/<WORKING_BRANCH>
```

---

### **Phase 3: Validation and Testing** ⏱️ 15 minutes

**Objective**: Ensure restored codebase works correctly

#### Step 3.1: Clean Installation
```bash
# Remove corrupted node_modules
rm -rf node_modules package-lock.json

# Fresh install
npm install

# Verify no peer dependency issues
npm ls --depth=0
```

#### Step 3.2: Build Validation
```bash
# Test TypeScript compilation
npx tsc --noEmit

# Test production build
npm run build

# Both should succeed without errors
```

#### Step 3.3: Development Testing
```bash
# Test development mode
npm run dev

# Verify:
# - UI loads with green theme (like Replit)
# - WebSocket connects to ws://localhost:8000
# - Agent status cards display properly
# - No console errors
```

#### Step 3.4: Backend Integration Test
```bash
# Test with simple backend
cd backend && python main_simple.py &
# Frontend should connect and work

# Test with full backend (if time permits)
cd backend && python main.py &
# Should see agent workflow functionality
```

---

## 🎯 SUCCESS CRITERIA

**Recovery Complete When**:
- [ ] `npm run build` succeeds without errors
- [ ] `npm run dev` shows green UI theme (matches Replit)
- [ ] WebSocket connects to localhost:8000 correctly
- [ ] Agent status cards display with proper styling
- [ ] No TypeScript compilation errors
- [ ] Theme provider working (dark theme displays)
- [ ] All navigation and components functional

**Verification Tests**:
1. **Build Test**: `npm run build` → Success
2. **Theme Test**: UI shows proper dark theme with green accents
3. **Connection Test**: WebSocket status shows "Connected"
4. **Component Test**: All sidebar navigation works
5. **Integration Test**: Backend communication functional

---

## 🚨 CONTINGENCY PLANS

### If Git Reset Fails:
1. **Manual Restoration**: Copy working files from Replit codebase
2. **Fresh Start**: Create new Next.js project and migrate components
3. **Branch Recovery**: Use backup branches if available

### If Dependencies Broken:
1. **Package Reset**: Delete package.json, reinstall from scratch
2. **Version Downgrade**: Use React 18 instead of React 19
3. **Dependency Audit**: Remove problematic packages

### If Theme/Styling Broken:
1. **Tailwind Reset**: Reinstall Tailwind CSS completely
2. **Component Library Reset**: Reinstall shadcn/ui components
3. **Manual CSS**: Add custom CSS overrides

---

## 📝 POST-RECOVERY ACTIONS

### Immediate (After Recovery):
1. **Test Full Workflow**: Verify both frontend and backend work together
2. **Document Issues**: Record what caused the corruption
3. **Create Safe Branch**: `git checkout -b frontend-stable`
4. **Backup Working State**: Create clean backup

### Short-term (Next Day):
1. **Branch Strategy**: Establish proper development branches
2. **CI/CD Setup**: Add build checks to prevent future breaks
3. **Testing**: Add automated tests for critical components
4. **Documentation**: Update setup/development docs

### Long-term Prevention:
1. **Regular Backups**: Daily backups of working states
2. **Staged Development**: Use feature branches for all changes
3. **Build Validation**: Require successful builds before merges
4. **Environment Parity**: Keep local and Replit codebases synced

---

## 🔧 TECHNICAL DETAILS

### Likely Root Causes:
1. **Incomplete Merge**: Human-in-the-loop branch merged with conflicts
2. **Dependency Conflicts**: React 19 + component library version mismatches
3. **Import Chain Breaks**: Missing workflow-store or similar component
4. **Environment Variables**: Local .env issues vs Replit configuration
5. **Node Modules Corruption**: npm install issues or cache problems

### Recovery Priorities:
1. **Get builds working** (highest priority)
2. **Restore UI theme/styling** (user visible)
3. **Fix WebSocket connection** (functionality)
4. **Ensure backend integration** (core features)

---

*This plan prioritizes getting back to a working state quickly while preserving the ability to understand and prevent future issues.*

**Estimated Total Time**: 60-90 minutes
**Risk Level**: Low (multiple fallback options)
**Success Probability**: High (git history should contain working state)
