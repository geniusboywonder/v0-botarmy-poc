# Instructions for Jules - Phase 2: Human-in-the-Loop Integration

**Project:** BotArmy MVP  
**Phase:** Human-in-the-Loop Integration  
**Target:** Complete MVP with interactive agent workflow  
**Timeline:** 15 tasks over 2-3 days  

---

## 🎉 Excellent Work on Phase 1!

Jules, your WebSocket Stabilization work was **EXCEPTIONAL**. All 15 tasks completed with A+ quality. Your implementations of the connection manager, error handler, rate limiter, and enhanced WebSocket service exceed production standards.

**Your work has been APPROVED and MERGED to main branch.**

---

## 🎯 Phase 2 Objectives

With your solid foundation, we can now implement the final MVP feature: **Human-in-the-Loop integration**. This will allow users to control and interact with agents throughout the workflow.

### Core Requirements:
1. **Agent Pause/Resume Controls** - Individual agent control
2. **Decision Point Interfaces** - User approval for major decisions  
3. **Interactive Agent Communication** - Agents explain work and ask permission
4. **Enhanced UX** - Progress indicators and task descriptions

---

## 📋 Phase 2 Tasks (15 Tasks)

### **Backend Tasks (Tasks 1-8)**

#### **Task 1: Enhanced ControlFlow Workflow with Human Checkpoints** (2h)
**Priority:** High  
**File:** `backend/workflow.py`

**Requirements:**
- Modify the `botarmy_workflow` to include human approval checkpoints before each agent
- Use ControlFlow's `cf.input()` functionality for user prompts
- Add pause/resume functionality using ControlFlow's flow state management
- Ensure each agent waits for human approval before proceeding

**Technical Details:**
- Wrap each agent task with a human approval step
- Add timeout handling for approval requests (default: 5 minutes)
- Store approval status in workflow state
- Add bypass option for fully automated mode

**Dependencies:** None

**Communication Files:** Update `jules-progress.md` with implementation notes and any blocking questions in `jules-questions.md`

---

#### **Task 2: Agent Communication Protocol Enhancement** (1.5h)
**Priority:** High  
**File:** `backend/agui/message_protocol.py`

**Requirements:**
- Add new message types: `agent_question`, `approval_request`, `workflow_paused`, `workflow_resumed`
- Enhance existing message format to include `requires_approval` and `approval_timeout` fields
- Add message acknowledgment system for critical user interactions

**Technical Details:**
```python
# New message types to add
class ApprovalRequest(BaseModel):
    agent_name: str
    question: str
    context: str
    options: List[str]  # e.g., ["approve", "reject", "modify"]
    timeout_seconds: int = 300
    
class AgentQuestion(BaseModel):
    agent_name: str
    question: str
    context: str
    requires_response: bool = True
```

**Dependencies:** Task 1 completion

---

#### **Task 3: Workflow State Manager** (2h)
**Priority:** High  
**File:** `backend/workflow_state_manager.py` (new file)

**Requirements:**
- Create a centralized workflow state manager to track agent progress and user interactions
- Implement pause/resume functionality for individual agents and entire workflow
- Add state persistence for workflow recovery after disconnection
- Track pending approvals and timeouts

**Technical Details:**
- Use async state management with proper locking
- Store state in memory (for MVP) with option to extend to Redis later
- Implement state broadcasting to all connected clients
- Add state validation and recovery mechanisms

**Dependencies:** Task 2 completion

---

#### **Task 4: Human Input Handler** (1.5h)
**Priority:** High  
**File:** `backend/human_input_handler.py` (new file)

**Requirements:**
- Create handler for processing user responses to agent questions and approval requests
- Implement timeout handling for unanswered prompts
- Add validation for user inputs and responses
- Queue pending questions when user is not available

**Technical Details:**
- Async handling of multiple concurrent approval requests
- Input validation based on question type
- Automatic timeout handling with default responses
- Integration with workflow state manager

**Dependencies:** Task 3 completion

---

#### **Task 5: Enhanced Agent Base Class** (1.5h)
**Priority:** Medium  
**File:** `backend/agents/base_agent.py`

**Requirements:**
- Add human interaction methods to base agent class
- Implement `ask_human()` method for agent questions
- Add `request_approval()` method for major decisions
- Include progress reporting and task description updates

**Technical Details:**
```python
async def ask_human(self, question: str, context: str, timeout: int = 300) -> str:
    # Send question to human via AG-UI protocol
    # Wait for response or timeout
    # Return human response or default

async def request_approval(self, action: str, context: str) -> bool:
    # Request human approval for specific action
    # Show context and implications
    # Return approval status
```

**Dependencies:** Tasks 2, 4 completion

---

#### **Task 6: Agent Task Description Broadcasting** (1h)
**Priority:** Medium  
**File:** `backend/agent_task_broadcaster.py` (new file)

**Requirements:**
- Create system to broadcast detailed agent task descriptions and progress
- Send real-time updates about what each agent is currently doing
- Include progress percentages and estimated completion times
- Integration with existing agent status broadcaster

**Technical Details:**
- Extend existing status broadcasting system
- Add progress calculation based on task complexity
- Include detailed task descriptions for user understanding
- Real-time progress updates during long-running tasks

**Dependencies:** Task 5 completion

---

#### **Task 7: Workflow Command Handler** (1.5h)
**Priority:** Medium  
**File:** `backend/workflow_command_handler.py` (new file)

**Requirements:**
- Handle user commands for workflow control: pause, resume, skip, retry
- Implement individual agent control (pause specific agent)
- Add workflow step navigation (next, previous, jump to step)
- Validate command permissions and workflow state

**Technical Details:**
- Command validation based on current workflow state
- Safe state transitions with rollback capability
- Command queuing for execution at appropriate times
- Integration with ControlFlow's workflow control

**Dependencies:** Task 3 completion

---

#### **Task 8: Main.py Integration** (1h)
**Priority:** High  
**File:** `backend/main.py`

**Requirements:**
- Integrate all new human-in-the-loop components with existing main.py
- Add new WebSocket message handlers for approval requests and workflow commands
- Update error handling for human interaction scenarios
- Add health checks for human interaction systems

**Technical Details:**
- Add new message type handlers in `handle_websocket_message()`
- Initialize new components in application startup
- Update error broadcasting for human interaction failures
- Add logging for human interaction events

**Dependencies:** All previous backend tasks completion

---

### **Frontend Tasks (Tasks 9-15)**

#### **Task 9: Enhanced Chat Interface with Approval System** (2h)
**Priority:** High  
**File:** `components/chat/approval-chat-interface.tsx` (new file)

**Requirements:**
- Create enhanced chat interface that handles approval requests from agents
- Add approval buttons and interactive response options
- Implement timeout indicators for pending approvals
- Show agent questions with context and response options

**Technical Details:**
- Support for different approval types (yes/no, multiple choice, text input)
- Visual distinction between regular messages and approval requests
- Timeout countdown timers for pending approvals
- Response validation and confirmation

**Dependencies:** Backend Task 2 completion

---

#### **Task 10: Agent Control Panel** (2h)
**Priority:** High  
**File:** `components/agent-control-panel.tsx` (new file)

**Requirements:**
- Create control panel with pause/resume buttons for each agent
- Add workflow-level controls (pause all, resume all, emergency stop)
- Show current agent status and pending actions
- Implement progress bars and task descriptions

**Technical Details:**
- Real-time agent status updates
- Control button state management (enabled/disabled based on workflow state)
- Progress visualization with task breakdown
- Emergency controls with confirmation dialogs

**Dependencies:** Backend Task 3 completion

---

#### **Task 11: Approval Queue Component** (1.5h)
**Priority:** High  
**File:** `components/approval-queue.tsx` (new file)

**Requirements:**
- Create queue component showing all pending approval requests
- Prioritize approvals by urgency and timeout
- Show approval context and implications
- Batch approval options for similar requests

**Technical Details:**
- Sortable approval list by priority and time remaining
- Expandable approval details with full context
- Quick approval options for common scenarios
- Visual timeout indicators

**Dependencies:** Frontend Task 9 completion

---

#### **Task 12: Workflow Progress Visualization** (1.5h)
**Priority:** Medium  
**File:** `components/workflow-progress.tsx` (new file)

**Requirements:**
- Create visual workflow progress indicator showing all 5 agents
- Display current step, completed steps, and upcoming steps
- Show waiting states for human approval
- Include estimated completion times

**Technical Details:**
- Step-by-step progress visualization
- Agent-specific progress indicators
- Human interaction indicators (waiting for approval)
- Time estimates and progress percentages

**Dependencies:** Backend Task 6 completion

---

#### **Task 13: WebSocket Service Enhancement for Human Interaction** (1.5h)
**Priority:** High  
**File:** `lib/websocket/websocket-service.ts`

**Requirements:**
- Add support for new message types: approval_request, agent_question, workflow_paused
- Implement approval response sending
- Add workflow command sending (pause, resume, skip)
- Handle approval timeouts on frontend

**Technical Details:**
```typescript
// New methods to add
sendApprovalResponse(approvalId: string, response: string): void
sendWorkflowCommand(command: 'pause' | 'resume' | 'skip', agentName?: string): void
handleApprovalRequest(request: ApprovalRequest): void
```

**Dependencies:** Backend Task 2 completion

---

#### **Task 14: Enhanced Agent Store for Human Interaction** (1h)
**Priority:** Medium  
**File:** `lib/stores/agent-store.ts`

**Requirements:**
- Add state management for pending approvals and workflow control
- Store approval queue and timeout information
- Track individual agent control states (paused, waiting, etc.)
- Add actions for approval responses and workflow commands

**Technical Details:**
- New store sections for approvals and workflow state
- Action creators for human interaction
- State persistence for approval context
- Integration with WebSocket service

**Dependencies:** Frontend Task 13 completion

---

#### **Task 15: Main Page Integration and Testing** (1.5h)
**Priority:** High  
**File:** `app/page.tsx`

**Requirements:**
- Integrate all new human-in-the-loop components into main page
- Add responsive layout for approval queue and control panels
- Implement keyboard shortcuts for common approvals
- Add comprehensive testing and polish

**Technical Details:**
- Layout management for new components
- Responsive design for mobile and desktop
- Keyboard navigation and shortcuts
- Error handling for human interaction components
- Integration testing with backend

**Dependencies:** All previous frontend tasks completion

---

## 🔧 Technical Architecture Notes

### **Human-in-the-Loop Flow:**
```
User Input → Agent Starts → Agent Asks Question → UI Shows Approval → User Responds → Agent Continues
```

### **Key Integration Points:**
1. **ControlFlow Integration**: Use `cf.input()` for human prompts
2. **AG-UI Protocol**: Extend for approval messages
3. **WebSocket Service**: Handle bi-directional approval communication
4. **State Management**: Track workflow and approval state

### **Error Handling:**
- Timeout handling for unanswered approvals
- Graceful degradation when human is unavailable
- Retry mechanisms for failed human interactions
- Fallback to automated mode when appropriate

---

## 📝 Communication Protocol

### **Progress Tracking:**
- Update `docs/jules-progress.md` after each task completion
- Include implementation notes and any challenges encountered
- Estimate time remaining for phase completion

### **Questions and Blockers:**
- Use `docs/jules-questions.md` for architecture questions
- Mark urgency level for time-sensitive blockers
- Provide context and attempted solutions

### **Testing Notes:**
- Update `docs/testing-checklist.md` with human interaction tests
- Include approval scenarios and timeout testing
- Document edge cases and error conditions

---

## 🎯 Success Criteria

### **MVP Demo Ready When:**
- [x] ✅ **Reliable WebSocket communication** (Completed in Phase 1)
- [ ] **Human can pause/resume individual agents**
- [ ] **Agents ask permission before major actions**
- [ ] **Approval queue shows pending decisions**
- [ ] **Workflow continues after human input**
- [ ] **Error handling for human interaction scenarios**

### **Technical Requirements:**
- All agents wait for human approval before proceeding
- Timeout handling prevents workflow from hanging indefinitely
- UI clearly shows what each agent is doing and waiting for
- User can control workflow progression manually
- Graceful handling of disconnection during approval process

---

## 🚀 Getting Started

### **Immediate Next Steps:**
1. **Review this document thoroughly**
2. **Start with Task 1** (Enhanced ControlFlow Workflow)
3. **Create feature branch**: `human-in-the-loop-integration`
4. **Update progress file** after each task completion
5. **Ask questions early** if any requirements are unclear

### **Expected Timeline:**
- **Tasks 1-4:** Day 1 (Backend foundation)
- **Tasks 5-8:** Day 2 (Backend integration)
- **Tasks 9-12:** Day 3 (Frontend components)
- **Tasks 13-15:** Day 4 (Frontend integration and testing)

Jules, your Phase 1 work was outstanding. With this solid foundation, Phase 2 should be smooth sailing. Focus on user experience and make the human-agent interaction feel natural and intuitive.

**Good luck with Phase 2! 🚀**

---

*Instructions prepared by Senior Architect Neill*  
*Phase 2 Start Date: August 21, 2025*  
*Expected Completion: August 24, 2025*
