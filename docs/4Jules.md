# Instructions for Jules: WebSocket Stabilization Phase

**Date:** August 20, 2025  
**Architect:** Senior Full-Stack Architect  
**Phase:** WebSocket Reliability & Real-time Communication  
**Timeframe:** 15 tasks over 24 hours  

---

## 🎯 Mission Overview

Jules, you're tasked with stabilizing the WebSocket layer and establishing robust real-time communication between the frontend and backend. The goal is to make the MVP demo-ready with professional error handling and reliable agent communication.

**Success Definition:** A user can start a project, see all 5 agents respond in sequence through OpenAI, with zero technical errors visible to the user.

---

## 🔧 Development Workflow

### Git Branch Strategy
```bash
# Jules will work on feature branches
git checkout -b websocket-stabilization-<task-number>
# Complete task, commit, push
git push origin websocket-stabilization-<task-number>
# I'll review and merge to main
```

### Communication Protocol
- **Progress Updates:** Update `/docs/jules-progress.md` after each task
- **Issues/Blockers:** Log in `/docs/jules-issues.md` 
- **Questions:** Create `/docs/jules-questions.md`
- **Completion:** Update task status in this file

### File Naming Convention
- Work files: `filename_WIP_<timestamp>.ext`
- Final files: `filename.ext` (remove _WIP_timestamp)
- Always check imports don't reference _WIP_ files

---

## 📋 Task Breakdown (15 Tasks)

### Phase 1: Backend Reliability (Tasks 1-8)

#### Task 1: Enhanced Connection Manager 🔴 High Priority - ✅ Implemented
**Estimated Time:** 2 hours  
**Branch:** `websocket-stabilization-1`

**Goal:** Replace basic ConnectionManager with robust connection handling.

**Implementation:**
```python
# File: backend/connection_manager.py
class EnhancedConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_metadata: Dict[str, dict] = {}
        self.message_queue: Dict[str, List[str]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        # Generate unique client ID
        # Store connection with metadata (timestamp, user_agent, etc.)
        # Send welcome message
        # Clear any queued messages for this client
    
    async def disconnect(self, websocket: WebSocket):
        # Clean up connection and metadata
        # Log disconnection reason
    
    async def send_to_client(self, client_id: str, message: dict):
        # Try to send message
        # If client disconnected, queue message
        # Include retry logic
    
    async def broadcast_to_all(self, message: dict):
        # Send to all connected clients
        # Handle individual client failures
    
    def get_connection_stats(self) -> dict:
        # Return connection statistics for monitoring
```

**Files to Modify:**
- Create: `backend/connection_manager.py`
- Update: `backend/main.py` (replace simple ConnectionManager)

**Testing:**
- Test with multiple browser tabs
- Test disconnect/reconnect scenarios
- Verify message queuing works

---

#### Task 2: Centralized Error Handler 🔴 High Priority - ✅ Implemented
**Estimated Time:** 1.5 hours  
**Branch:** `websocket-stabilization-2`

**Goal:** Create unified error handling that converts technical errors to user-friendly messages.

**Implementation:**
```python
# File: backend/error_handler.py
class ErrorHandler:
    @staticmethod
    def handle_llm_error(error: Exception, agent_name: str) -> dict:
        # Convert OpenAI errors to user messages
        # Handle rate limiting, API key issues, etc.
    
    @staticmethod
    def handle_websocket_error(error: Exception, client_id: str) -> dict:
        # Convert WebSocket errors to user messages
    
    @staticmethod
    def handle_workflow_error(error: Exception, session_id: str) -> dict:
        # Convert ControlFlow errors to user messages
    
    @staticmethod
    def create_user_friendly_message(error_type: str, details: str) -> str:
        # Map technical errors to user-friendly messages
```

**Error Message Mapping:**
- `OpenAI API key not found` → "AI service configuration needed. Please check setup."
- `Rate limit exceeded` → "AI service is busy. Retrying in a moment..."
- `Connection timeout` → "Connection lost. Reconnecting automatically..."

**Files to Modify:**
- Create: `backend/error_handler.py`
- Update: `backend/main.py` (integrate error handler)
- Update: `backend/workflow.py` (use error handler)

---

#### Task 3: WebSocket Message Protocol Enhancement 🟡 Medium Priority - ✅ Completed
**Estimated Time:** 2 hours  
**Branch:** `websocket-stabilization-3`

**Goal:** Standardize all WebSocket messages and add message acknowledgment.

**Implementation:**
```python
# File: backend/agui/message_protocol.py
class MessageProtocol:
    @staticmethod
    def create_agent_status_update(agent_name: str, status: str, task: str = None) -> dict:
        # Standardized agent status message
    
    @staticmethod
    def create_agent_response(agent_name: str, content: str, metadata: dict = None) -> dict:
        # Standardized agent response message
    
    @staticmethod
    def create_error_message(error: str, error_type: str = "general") -> dict:
        # Standardized error message
    
    @staticmethod
    def create_system_message(content: str, message_type: str = "info") -> dict:
        # Standardized system message
    
    @staticmethod
    def create_heartbeat_message() -> dict:
        # Heartbeat for connection monitoring
```

**Message Format:**
```json
{
    "id": "uuid",
    "type": "agent_status|agent_response|error|system|heartbeat",
    "timestamp": "ISO-8601",
    "agent_name": "string",
    "content": "string", 
    "metadata": {},
    "requires_ack": boolean
}
```

**Files to Modify:**
- Create: `backend/agui/message_protocol.py`
- Update: `backend/agui/protocol.py` (use new protocol)
- Update: `backend/main.py` (use standardized messages)

---

#### Task 4: Rate Limiter for OpenAI 🟡 Medium Priority - ✅ Implemented
**Estimated Time:** 1.5 hours  
**Branch:** `websocket-stabilization-4`

**Goal:** Prevent OpenAI API rate limit violations with intelligent queuing.

**Implementation:**
```python
# File: backend/rate_limiter.py
class OpenAIRateLimiter:
    def __init__(self):
        self.requests_per_minute = 20  # Conservative limit
        self.tokens_per_minute = 40000
        self.request_timestamps = []
        self.token_usage = []
    
    async def can_make_request(self, estimated_tokens: int = 1000) -> bool:
        # Check if request is within rate limits
    
    async def wait_if_needed(self, estimated_tokens: int = 1000):
        # Wait if necessary to respect rate limits
    
    def record_request(self, tokens_used: int):
        # Record successful request for tracking
    
    def get_rate_limit_status(self) -> dict:
        # Return current rate limit status
```

**Files to Modify:**
- Create: `backend/rate_limiter.py`
- Update: `backend/services/llm_service.py` (integrate rate limiter)
- Update: `backend/agents/base_agent.py` (use rate limiter)

---

#### Task 5: Enhanced LLM Service with Retries 🔴 High Priority - ✅ Implemented
**Estimated Time:** 2 hours  
**Branch:** `websocket-stabilization-5`

**Goal:** Make LLM service robust with retries, timeouts, and graceful degradation.

**Implementation:**
```python
# File: backend/services/llm_service.py (enhanced)
class EnhancedLLMService:
    def __init__(self):
        self.rate_limiter = OpenAIRateLimiter()
        self.max_retries = 3
        self.timeout_seconds = 30
    
    async def generate_response(self, prompt: str, agent_name: str) -> str:
        for attempt in range(self.max_retries):
            try:
                await self.rate_limiter.wait_if_needed()
                # Make OpenAI call with timeout
                # Track token usage
                # Return response
            except OpenAIError as e:
                # Handle specific OpenAI errors
                if attempt == self.max_retries - 1:
                    return self.get_fallback_response(agent_name, str(e))
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                # Handle other errors
                return self.get_fallback_response(agent_name, str(e))
    
    def get_fallback_response(self, agent_name: str, error: str) -> str:
        # Return agent-appropriate fallback message
```

**Fallback Messages:**
- Analyst: "I'm analyzing your requirements. Please give me a moment to gather more information."
- Architect: "I'm designing the system architecture. This may take a moment to ensure quality."
- Developer: "I'm implementing the solution. Please be patient while I write the code."

**Files to Modify:**
- Update: `backend/services/llm_service.py`
- Update: `backend/agents/base_agent.py` (use enhanced service)

---

#### Task 6: Heartbeat and Health Monitoring 🟡 Medium Priority - ✅ Implemented
**Estimated Time:** 1 hour  
**Branch:** `websocket-stabilization-6`

**Goal:** Add heartbeat mechanism to detect dead connections and monitor system health.

**Implementation:**
```python
# File: backend/heartbeat_monitor.py
class HeartbeatMonitor:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
        self.heartbeat_interval = 30  # seconds
        self.client_timeouts = {}
    
    async def start_heartbeat_loop(self):
        while True:
            await self.send_heartbeat_to_all()
            await self.check_client_timeouts()
            await asyncio.sleep(self.heartbeat_interval)
    
    async def send_heartbeat_to_all(self):
        # Send heartbeat to all clients
    
    async def handle_heartbeat_response(self, client_id: str):
        # Update client last seen timestamp
    
    async def check_client_timeouts(self):
        # Disconnect clients that haven't responded
```

**Files to Modify:**
- Create: `backend/heartbeat_monitor.py`
- Update: `backend/main.py` (start heartbeat loop)
- Update: `backend/connection_manager.py` (handle heartbeat responses)

---

#### Task 7: Agent Status Broadcasting 🔴 High Priority - ✅ Implemented
**Estimated Time:** 1.5 hours  
**Branch:** `websocket-stabilization-7`

**Goal:** Real-time agent status updates sent to frontend during workflow execution.

**Implementation:**
```python
# File: backend/agent_status_broadcaster.py
class AgentStatusBroadcaster:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
    
    async def broadcast_agent_started(self, agent_name: str, task: str):
        # Send agent started message
    
    async def broadcast_agent_thinking(self, agent_name: str):
        # Send agent thinking/working message
    
    async def broadcast_agent_completed(self, agent_name: str, result: str):
        # Send agent completed message
    
    async def broadcast_agent_error(self, agent_name: str, error: str):
        # Send agent error message
```

**Integration Points:**
- ControlFlow task start/complete hooks
- LLM service before/after calls
- Error handler integration

**Files to Modify:**
- Create: `backend/agent_status_broadcaster.py`
- Update: `backend/workflow.py` (add status broadcasts)
- Update: `backend/bridge.py` (integrate broadcaster)

---

#### Task 8: Improved Error Recovery in Workflow 🔴 High Priority - ✅ Implemented
**Estimated Time:** 1.5 hours  
**Branch:** `websocket-stabilization-8`

**Goal:** Make workflow continue gracefully when individual agents fail.

**Implementation:**
```python
# File: backend/workflow.py (enhanced)
@cf.flow
def enhanced_botarmy_workflow(project_brief: str):
    results = {}
    
    # Define agent tasks with error handling
    for agent_name, agent_task in AGENT_TASKS.items():
        try:
            broadcaster.broadcast_agent_started(agent_name, agent_task.description)
            result = agent_task(project_brief, previous_results=results)
            results[agent_name] = result
            broadcaster.broadcast_agent_completed(agent_name, result)
        except Exception as e:
            error_msg = error_handler.handle_workflow_error(e, agent_name)
            broadcaster.broadcast_agent_error(agent_name, error_msg)
            # Continue with next agent instead of failing entire workflow
            results[agent_name] = f"Agent {agent_name} encountered an issue. Continuing with workflow..."
    
    return results
```

**Files to Modify:**
- Update: `backend/workflow.py`
- Update: `backend/agents/` (all agent files for better error handling)

---

### Phase 2: Frontend Reliability (Tasks 9-15)

#### Task 9: Enhanced WebSocket Service 🔴 High Priority
**Estimated Time:** 2 hours  
**Branch:** `websocket-stabilization-9`

**Goal:** Make frontend WebSocket service robust with proper reconnection and error handling.

**Implementation:**
```typescript
// File: lib/websocket/websocket-service.ts (enhanced)
class EnhancedWebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 10
  private messageQueue: any[] = []
  private heartbeatInterval: number | null = null
  private connectionStatus: ConnectionStatus
  
  connect() {
    // Enhanced connection logic
    // Setup heartbeat
    // Queue message processing
  }
  
  private setupHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.send({ type: 'heartbeat' })
      }
    }, 30000)
  }
  
  private processMessageQueue() {
    // Process queued messages when connection restored
  }
  
  private handleMessage(message: WebSocketMessage) {
    // Enhanced message handling
    // Update agent stores in real-time
    // Handle different message types
  }
}
```

**Key Improvements:**
- Message queuing during disconnection
- Heartbeat mechanism
- Better error classification
- Real-time store updates

**Files to Modify:**
- Update: `lib/websocket/websocket-service.ts`

---

#### Task 10: Connection Status Component 🟡 Medium Priority
**Estimated Time:** 1 hour  
**Branch:** `websocket-stabilization-10`

**Goal:** Visual connection status indicator in the UI.

**Implementation:**
```typescript
// File: components/connection-status.tsx
export function ConnectionStatus() {
  const [status, setStatus] = useState<ConnectionStatus>()
  
  useEffect(() => {
    const unsubscribe = websocketService.onStatusChange(setStatus)
    return unsubscribe
  }, [])
  
  return (
    <div className={`flex items-center space-x-2 ${getStatusColor(status?.connected)}`}>
      <StatusIcon status={status} />
      <span className="text-sm">{getStatusText(status)}</span>
    </div>
  )
}
```

**Status States:**
- 🟢 Connected - "Connected to BotArmy"
- 🟡 Connecting - "Connecting..."
- 🔴 Disconnected - "Connection lost. Retrying..."
- ⚠️ Error - "Connection error. Check backend."

**Files to Modify:**
- Create: `components/connection-status.tsx`
- Update: `app/dashboard/page.tsx` (add connection status)

---

#### Task 11: Real-time Agent Store Integration 🔴 High Priority  
**Estimated Time:** 1.5 hours  
**Branch:** `websocket-stabilization-11`

**Goal:** Agent store updates in real-time from WebSocket messages.

**Implementation:**
```typescript
// File: lib/stores/agent-store.ts (enhanced)
export const useAgentStore = create<AgentStore>()(
  subscribeWithSelector((set, get) => ({
    // ... existing code ...
    
    updateAgentFromMessage: (message: WebSocketMessage) => {
      const { agent_name, type, content, metadata } = message
      
      if (type === 'agent_status') {
        set((state) => ({
          agents: state.agents.map(agent => 
            agent.name === agent_name 
              ? { 
                  ...agent, 
                  status: metadata?.status || agent.status,
                  currentTask: metadata?.task || agent.currentTask,
                  progress: metadata?.progress || agent.progress,
                  lastActivity: new Date()
                }
              : agent
          )
        }))
      }
    },
    
    handleAgentError: (agentName: string, error: string) => {
      set((state) => ({
        agents: state.agents.map(agent =>
          agent.name === agentName
            ? { ...agent, status: 'error', currentTask: error }
            : agent
        )
      }))
    }
  }))
)
```

**Files to Modify:**
- Update: `lib/stores/agent-store.ts`
- Update: `lib/websocket/websocket-service.ts` (call store methods)

---

#### Task 12: Error Boundary Components 🟡 Medium Priority
**Estimated Time:** 1 hour  
**Branch:** `websocket-stabilization-12`

**Goal:** React error boundaries to prevent UI crashes.

**Implementation:**
```typescript
// File: components/error-boundary.tsx
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false, error: null }
  }
  
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error Boundary caught an error:', error, errorInfo)
    // Log to monitoring service
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} onReset={() => this.setState({ hasError: false, error: null })} />
    }
    
    return this.props.children
  }
}
```

**Files to Modify:**
- Create: `components/error-boundary.tsx` 
- Create: `components/error-fallback.tsx`
- Update: `app/layout.tsx` (wrap app in error boundary)

---

#### Task 13: Enhanced Chat Interface 🔴 High Priority
**Estimated Time:** 2 hours  
**Branch:** `websocket-stabilization-13`

**Goal:** Improved chat interface with typing indicators and better error display.

**Implementation:**
```typescript
// File: components/chat/enhanced-chat-interface.tsx
export function EnhancedChatInterface() {
  const [message, setMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const logs = useLogStore(state => state.logs)
  const connectionStatus = useConnectionStatus()
  
  const handleSendMessage = async () => {
    if (!message.trim() || isLoading || !connectionStatus.connected) return
    
    try {
      setIsLoading(true)
      await websocketService.startProject(message)
      setMessage("")
    } catch (error) {
      // Error handling
    } finally {
      setIsLoading(false)
    }
  }
  
  return (
    <div className="flex flex-col h-full">
      <ConnectionStatus />
      <ChatMessageList logs={logs} />
      <ChatInput 
        message={message}
        onChange={setMessage}
        onSend={handleSendMessage}
        disabled={isLoading || !connectionStatus.connected}
        loading={isLoading}
      />
    </div>
  )
}
```

**Features:**
- Connection status integration
- Disabled state when disconnected
- Loading states
- Better error messaging

**Files to Modify:**
- Create: `components/chat/enhanced-chat-interface.tsx`
- Update: `app/dashboard/page.tsx` (use enhanced chat)

---

#### Task 14: Agent Status Cards with Real-time Updates 🔴 High Priority
**Estimated Time:** 1.5 hours  
**Branch:** `websocket-stabilization-14`

**Goal:** Agent cards that update in real-time with smooth animations.

**Implementation:**
```typescript
// File: components/agent-status-card.tsx (enhanced)
export function EnhancedAgentStatusCard({ agent }: { agent: Agent }) {
  return (
    <Card className={cn(
      "p-4 transition-all duration-300",
      agent.status === 'active' && "ring-2 ring-blue-500",
      agent.status === 'error' && "ring-2 ring-red-500"
    )}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <AgentAvatar agent={agent} />
          <div>
            <h3 className="font-semibold">{agent.name}</h3>
            <p className="text-sm text-muted-foreground">{agent.role}</p>
          </div>
        </div>
        <AgentStatusBadge status={agent.status} />
      </div>
      
      {agent.status === 'active' && agent.currentTask && (
        <div className="mt-2 flex items-center space-x-2">
          <TypingIndicator />
          <span className="text-sm text-muted-foreground">{agent.currentTask}</span>
        </div>
      )}
      
      {agent.progress && (
        <Progress value={agent.progress} className="mt-2" />
      )}
    </Card>
  )
}

// Typing indicator component
const TypingIndicator = () => (
  <div className="flex space-x-1">
    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
  </div>
)
```

**Files to Modify:**
- Update: `components/agent-status-card.tsx`
- Create: `components/typing-indicator.tsx`

---

#### Task 15: Integration Testing & Polish 🔴 High Priority
**Estimated Time:** 1.5 hours  
**Branch:** `websocket-stabilization-15`

**Goal:** End-to-end testing and final polish for MVP demo.

**Implementation:**
1. **Test Complete User Flow:**
   - Start backend server
   - Open frontend
   - Verify connection status shows "Connected"
   - Send test project brief
   - Verify all 5 agents respond
   - Test error scenarios

2. **Error Scenario Testing:**
   - Disconnect backend during workflow
   - Invalid OpenAI API key
   - Malformed project brief
   - Network interruptions

3. **Performance Testing:**
   - Multiple browser tabs
   - Long-running workflows
   - Memory usage monitoring

4. **UI Polish:**
   - Smooth animations
   - Consistent spacing
   - Professional error messages
   - Loading states

**Files to Modify:**
- Create: `docs/testing-checklist.md`
- Update: `README.md` (demo instructions)
- Fix any remaining issues found during testing

---

## 🔧 Communication Templates

### Progress Update Template
```markdown
## Task X Progress Update
**Task:** [Task Name]
**Status:** [In Progress/Completed/Blocked]
**Time Spent:** [X hours]
**Completion:** [X%]

### What I Completed:
- [ ] Item 1
- [ ] Item 2

### Current Blockers:
- None / [Describe blocker]

### Next Steps:
- [What's next]

### Notes:
[Any additional context]
```

### Issue Template
```markdown
## Issue Report
**Task:** [Task Number]
**Severity:** [High/Medium/Low]
**Type:** [Bug/Question/Enhancement]

### Description:
[Clear description of the issue]

### Steps to Reproduce:
1. Step 1
2. Step 2

### Expected vs Actual:
**Expected:** [What should happen]
**Actual:** [What actually happens]

### Potential Solutions:
[Your ideas for solving this]
```

---

## 🎯 Success Criteria

### Technical Requirements
- [ ] WebSocket connection uptime > 95% during testing
- [ ] All backend errors surface as user-friendly messages in UI
- [ ] Agent status updates in real-time within 1 second
- [ ] No technical error messages visible to end users
- [ ] Graceful handling of all connection failure scenarios

### User Experience Requirements
- [ ] Connection status always visible and accurate
- [ ] Loading states for all async operations
- [ ] Professional error messages with actionable guidance
- [ ] Smooth animations and transitions
- [ ] Disabled states when appropriate

### Demo Requirements
- [ ] Complete workflow: Project brief → 5 agent responses
- [ ] Error scenarios handled gracefully
- [ ] Professional appearance suitable for stakeholder demo
- [ ] Consistent behavior across multiple test runs

---

## 🚨 Important Notes

### Critical Success Factors
1. **Error Handling First:** Every failure scenario must be handled gracefully
2. **User Experience:** No technical jargon visible to users
3. **Real-time Updates:** Agent status must update immediately
4. **Professional Polish:** UI must feel production-ready

### Common Pitfalls to Avoid
- Don't leave console.error() messages in production code
- Don't show raw API errors to users
- Don't forget to handle WebSocket reconnection scenarios
- Don't leave hardcoded values (use environment variables)

### Code Quality Standards
- TypeScript strict mode enabled
- No `any` types without justification
- Proper error boundaries around all async operations
- Consistent naming conventions
- Clear comments for complex logic

---

## 📞 Getting Help

### When to Ask Questions
- Unclear requirements or specifications
- Technical blockers that prevent progress > 30 minutes
- Architecture decisions that affect multiple components
- Integration issues between frontend/backend

### How to Ask Questions
1. Create `/docs/jules-questions.md`
2. Include specific context and what you've tried
3. Suggest potential solutions if you have ideas
4. Mark urgency level (High/Medium/Low)

---

**Start with Task 1 and work sequentially. Update progress after each task completion.**

**Good luck, Jules! You've got this! 🚀**

---

*End of Instructions Document*
