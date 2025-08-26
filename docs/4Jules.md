# Instructions for Jules - BotArmy MVP Completion

**Project**: BotArmy POC  
**Phase**: Core Agent Workflow Completion  
**Target**: Polished production ready solution  

Before starting any coding, scan the files and folder structure to make sure you fully understand the project and how it functions.
Do not create new code without first checking and understadning what has already been written.

## 🛠️ Technical Implementation Guidelines

### **Architecture Principles**

- **Keep existing patterns** - Don't reinvent what's already working well
- **Progressive enhancement** - Build on the solid foundation
- **Error resilience** - Every component should handle failures gracefully
- **Real-time updates** - Users should see immediate feedback for all actions
- **Clean separation** - Keep backend logic separate from frontend concerns

### **Code Quality Standards**

- Follow the same high-quality patterns established
- Add proper error handling at every level
- Include logging for debugging and monitoring
- Write tests for critical functionality
- Keep code clean and well-commented

### **Frontend State Management**

- Use Zustand stores for application state
- Update state from WebSocket messages
- Keep UI reactive to state changes
- Handle loading and error states properly

## 📋 Workflow and Communication

### **Branch Management**

1. **Create a new branch** for this work
2. **Make incremental commits** after each task completion
3. **Push regularly** to GitHub for backup
4. **Create merge request** when all tasks are complete

### **Progress Reporting**

Update these files after each task:

- `docs/jules-progress.md` - Overall progress and task completion
- `ClaudeProgress.md` - Module status updates
- `docs/jules-questions.md` - Any questions or clarifications needed
- `docs/jules-issues.md` - Any problems encountered and solutions

### **Communication Protocol**

- **Questions**: Use `jules-questions.md` for architectural clarifications
- **Issues**: Use `jules-issues.md` for problems that need help
- **Progress**: Update progress files after each task completion
- **Code Review**: Push to GitHub branch for review before merging

### **Testing Protocol**

After each major change:

1. Test the backend: `cd backend && python main.py`
2. Test the frontend: `npm run dev`
3. Test WebSocket connection in browser console
4. Test both test mode and full mode (if safe)
5. Document any issues encountered

1. **Complete the tasks** - This is the heart of BotArmy
2. **Make status updates visible** - Users need to see progress
3. **Handle errors gracefully** - System should be robust
4. **Test thoroughly** - Ensure reliability for demonstrations

**Key Success Factors**:

- Build incrementally - complete one task fully before moving to the next
- Test frequently - catch issues early
- Ask questions - clarify anything unclear
- Document progress - keep detailed notes of changes
