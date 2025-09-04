# ClaudeProgress.md - HITL Implementation Plan

## Task: Implement Human-in-the-Loop (HITL) patterns for BotArmy

### Status: Planning Phase

---

## Modules to Implement

| Status | Module | Path | Description |
|--------|--------|------|-------------|
| **ToDo** | HITL Manager | `/lib/hitl/manager.ts` | Core HITL orchestration manager |
| **ToDo** | HITL Store | `/lib/stores/hitl-store.ts` | Zustand store for HITL state management |
| **ToDo** | HITL Alert Component | `/components/hitl/hitl-alert.tsx` | Expandable alert component for HITL messages |
| **ToDo** | HITL Badge Component | `/components/hitl/hitl-badge.tsx` | Badge with glow effect for HITL status |
| **ToDo** | Agent Context Filter | `/components/chat/agent-context-filter.tsx` | Filter chat by agent context |
| **ToDo** | Resolve Button Component | `/components/hitl/resolve-button.tsx` | In-situ resolve button for HITL actions |
| **ToDo** | HITL Chat Enhancement | `/components/chat/copilot-chat-hitl.tsx` | Enhanced chat with HITL support |
| **ToDo** | Kill Switch Component | `/components/controls/kill-switch.tsx` | Agent pause/cancel controls |
| **ToDo** | Project Brief Detection | `/lib/utils/project-detection.ts` | Detect and initialize project from brief |
| **ToDo** | HITL Types | `/lib/types/hitl.ts` | TypeScript types for HITL system |

---

## Implementation Plan

### Phase 1: Core HITL Infrastructure
1. Create HITL type definitions
2. Implement HITL store with Zustand
3. Create HITL manager for orchestration
4. Set up project detection utilities

### Phase 2: UI Components
1. Build HITL alert component with expandable state
2. Create HITL badge with glow animation
3. Implement resolve button component
4. Build kill switch controls

### Phase 3: Chat Integration
1. Enhance CopilotChat with HITL support
2. Add agent context filtering
3. Implement project brief detection
4. Integrate kill switch functionality

### Phase 4: Testing & Polish
1. Test all HITL scenarios
2. Ensure proper state management
3. Verify CopilotKit integration
4. Add animations and transitions

---

## Scenarios to Support

### Scenario 1: Direct Agent Chat HITL
- Agent requests approval/decision during conversation
- UI shows inline approval buttons
- User can approve/reject/modify

### Scenario 2: Background Task Elevation
- Agent working in background needs decision
- Alert appears in header area
- User can click to resolve in chat
- Badge glows to indicate attention needed

### Scenario 3: Project Initialization
- User provides project brief in general chat
- System detects and initializes agents
- Workflow begins with proper orchestration

---

## Progress Log
- Started: Planning phase initiated
- Next: Begin implementation with HITL types
