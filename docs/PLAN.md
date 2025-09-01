# Dual Chat Mode Implementation Plan

**Date:** September 1, 2025  
**Priority:** High - Enhanced user experience with general chat + focused project mode
**Status:** PLANNING - Ready for Implementation

---

## Overview
Implement a dual-mode chat system where users can engage in general LLM conversation or switch to project-focused agent mode with role-specific behavior enforcement.

## Current State Analysis

### Existing Components
- **Chat Interface**: `components/chat/enhanced-chat-interface.tsx` - handles UI and message display
- **Conversation Store**: `lib/stores/conversation-store.ts` - manages chat messages and state
- **WebSocket Service**: `lib/websocket/websocket-service.ts` - handles real-time communication
- **Agent System**: `backend/agents/` - role-specific agents (Analyst, Architect, Developer, etc.)
- **Workflow Engine**: `backend/workflow.py` - orchestrates agent interactions

### Current Issues
1. No distinction between general chat and project mode
2. All messages currently route through the agent system
3. No native LLM chat capability for general conversation
4. Agents not restricted to their specific roles/domains

## Proposed Solution Architecture

### 1. Chat Mode Management

#### Frontend State
```typescript
interface ChatMode {
  mode: 'general' | 'project'
  projectContext?: {
    id: string
    description: string
    activeAgents: string[]
    artifacts: any[]
  }
}
```

#### Mode Indicators
- Visual mode indicator in chat header
- Different styling/colors for each mode
- Clear transition messages when switching modes

### 2. Message Routing System

#### Backend Message Router
Create `backend/services/message_router.py`:
- Analyze incoming messages for mode switching keywords
- Route to appropriate handler (LLM service vs Agent workflow)
- Maintain context awareness across mode switches

#### Mode Detection Logic
- **Enter Project Mode**: Keywords like "start project", "begin working on", "project mode", "enable agents"
- **Exit Project Mode**: Keywords like "general chat", "exit project", "chat mode", "stop project"
- **Explicit Commands**: `/project start [description]`, `/chat`, `/project exit`

### 3. General Chat Mode

#### Direct LLM Integration
- Create `backend/services/general_chat_service.py`
- Direct connection to LLM providers (OpenAI, Claude, Gemini)
- No agent workflow involvement
- Maintains conversation history
- Supports all general topics and questions

#### Features
- Natural conversation flow
- Context retention within chat session
- Support for creative writing, coding help, general Q&A
- No restrictions on topic scope

### 4. Project Mode Enhancement

#### Agent Role Enforcement
Create `backend/services/role_enforcer.py`:
- Define strict role boundaries for each agent type
- Implement topic filtering and validation
- Redirect off-topic questions to appropriate agent or general mode

#### Role Definitions
```python
AGENT_ROLES = {
    'Analyst': {
        'focus': ['requirements', 'analysis', 'user stories', 'specifications'],
        'off_topic_redirect': 'This is outside my analysis role. Consider asking the {appropriate_agent} or switch to general chat.'
    },
    'Architect': {
        'focus': ['system design', 'architecture', 'technical decisions', 'patterns'],
        'off_topic_redirect': 'This is outside my architectural role. Consider asking the {appropriate_agent} or switch to general chat.'
    },
    # ... other agents
}
```

#### Project Context Management
- Maintain active project state
- Track artifacts, tasks, and progress
- Enable agent-to-agent handoffs
- Provide project-specific context to all agents

### 5. Implementation Steps

#### Phase 1: Backend Infrastructure
1. **Message Router Service**
   - Create message routing logic
   - Implement mode detection
   - Add routing configuration

2. **General Chat Service**
   - Direct LLM integration
   - Context management
   - Response formatting

3. **Role Enforcer Service**
   - Agent role definitions
   - Topic validation logic
   - Redirect mechanisms

#### Phase 2: Mode Management
1. **Chat Mode Store**
   - Extend conversation store with mode state
   - Add mode switching methods
   - Implement context persistence

2. **Backend Mode Handler**
   - Create mode switching endpoints
   - Project context management
   - State synchronization

#### Phase 3: Frontend Integration
1. **Mode UI Components**
   - Mode indicator widget
   - Switch mode buttons/commands
   - Visual mode differentiation

2. **Chat Interface Updates**
   - Mode-specific styling
   - Command recognition
   - Context display

#### Phase 4: Agent System Enhancement
1. **Role Boundaries**
   - Implement role enforcement in each agent
   - Add topic validation
   - Create redirect responses

2. **Agent Coordination**
   - Cross-agent communication protocols
   - Task handoff mechanisms
   - Context sharing

### 6. User Experience Flow

#### Starting General Chat
```
User: "Hello, can you help me understand quantum computing?"
System: [GENERAL CHAT MODE] 
LLM: "I'd be happy to explain quantum computing! Quantum computing is..."
```

#### Switching to Project Mode
```
User: "Let's start a project to build a task management app"
System: [SWITCHING TO PROJECT MODE]
System: [PROJECT MODE ACTIVE] - Task Management App
Analyst: "I'll help analyze the requirements for your task management app. What are the core features you need?"
```

#### Role-Focused Responses in Project Mode
```
User: "What's the weather like today?"
Analyst: "That's outside my analysis role. I focus on requirements, user stories, and project specifications. For general questions, try switching to chat mode with '/chat' or ask about project requirements."
```

#### Switching Back to General Chat
```
User: "Switch to general chat mode"
System: [SWITCHING TO GENERAL CHAT MODE]
System: [GENERAL CHAT MODE]
LLM: "I'm now in general chat mode. How can I help you with any topic?"
```

### 7. Technical Considerations

#### State Management
- Persist mode state across sessions
- Handle mode switches gracefully
- Maintain project context when switching modes

#### Performance
- Cache LLM responses for general chat
- Optimize agent routing
- Minimize unnecessary workflow triggers

#### Error Handling
- Graceful mode switch failures
- Agent unavailability scenarios
- Context recovery mechanisms

#### Security
- Validate mode switch permissions
- Sanitize project context data
- Protect agent role boundaries

### 8. Configuration Options

#### Environment Variables
```bash
# Chat mode settings
ENABLE_GENERAL_CHAT=true
DEFAULT_CHAT_MODE=general
PROJECT_MODE_TIMEOUT=3600  # Auto-exit after 1 hour of inactivity

# Agent role enforcement
STRICT_ROLE_ENFORCEMENT=true
ALLOW_ROLE_FLEXIBILITY=false

# LLM provider for general chat
GENERAL_CHAT_PROVIDER=openai
GENERAL_CHAT_MODEL=gpt-4
```

#### User Preferences
- Default mode on startup
- Auto-switch sensitivity
- Preferred LLM for general chat
- Agent notification preferences

### 9. Testing Strategy

#### Unit Tests
- Mode detection logic
- Role enforcement rules
- Message routing accuracy
- Context management

#### Integration Tests
- End-to-end mode switching
- Agent coordination
- WebSocket communication
- State persistence

#### User Acceptance Tests
- Natural conversation flow
- Smooth mode transitions
- Agent role adherence
- Context preservation

### 10. Future Enhancements

#### Advanced Features
- Multi-project support
- Custom agent roles
- Agent learning from interactions
- Advanced context sharing

#### Analytics
- Mode usage patterns
- Agent effectiveness metrics
- User satisfaction tracking
- Performance monitoring

This plan provides a comprehensive roadmap for implementing the dual-mode chat system while maintaining the existing agent functionality and adding robust general conversation capabilities.