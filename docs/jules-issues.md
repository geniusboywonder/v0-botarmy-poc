# Jules Issues & Blockers

**Phase:** WebSocket Stabilization  
**Date:** August 20, 2025  

---

## 🚨 Current Blockers

*No current blockers. Jules will log any issues here.*

---

## ⚠️ Issue Log

*Jules will add issues using the template below:*

### Issue Template
```markdown
## Issue #X - [Brief Description]
**Date:** YYYY-MM-DD HH:MM
**Task:** Task X - [Task Name]
**Severity:** High/Medium/Low
**Type:** Bug/Question/Enhancement/Blocker

### Description:
[Clear description of the issue]

### Steps to Reproduce:
1. Step 1
2. Step 2
3. Step 3

### Expected vs Actual:
**Expected:** [What should happen]
**Actual:** [What actually happens]

### Environment:
- OS: [macOS/Windows/Linux]
- Node.js: [Version]
- Python: [Version]
- Browser: [Browser and version]

### Attempted Solutions:
- [What I tried]
- [Results of each attempt]

### Potential Solutions:
[Ideas for solving this]

### Status:
[Open/In Progress/Resolved]

### Resolution:
[How it was resolved - to be filled when complete]
```

---

## 🔍 Common Issues & Solutions

### WebSocket Connection Issues
- **Problem:** Connection fails to localhost:8000
- **Solution:** Ensure backend is running: `cd backend && python main.py`

### Import/Module Issues  
- **Problem:** Module not found errors
- **Solution:** Check Python virtual environment is activated: `source venv/bin/activate`

### TypeScript Errors
- **Problem:** Type errors in frontend
- **Solution:** Run `npm run type-check` and fix type issues

### Git Branch Issues
- **Problem:** Merge conflicts or branch issues
- **Solution:** Create new branch: `git checkout -b websocket-stabilization-X-retry`

---

*Jules: Please log all issues here, no matter how small. This helps track patterns and solutions.*
