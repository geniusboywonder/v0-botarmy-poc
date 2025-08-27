# BotArmy Process-View Refactoring Implementation Plan

**Date Created**: August 27, 2025 14:30 UTC  
**Project**: Transform BotArmy from agent-focused to process-focused UI  
**Target**: Complete SDLC-based interface while preserving all functionality  
**Developer**: Jules (AI Coding Agent)  

---

## Project Overview

Transform BotArmy from agent-centric to process-centric UI based on mockups in `mockups/ProcessView/`. The goal is to restructure pages around SDLC stages (Requirements, Design, Dev, Test, Deploy) while maintaining all existing functionality including WebSocket communication, HITL controls, and real-time updates.

## Quick Summary Checklist

- [ ] **Phase 1**: Documentation & Planning (30 mins)
- [ ] **Phase 2**: Layout Architecture (2 hours)  
- [ ] **Phase 3**: Dashboard Redesign (3 hours)
- [ ] **Phase 4**: Stage Pages Implementation (6 hours)
- [ ] **Phase 5**: Integration & Testing (2 hours)
- [ ] **Phase 6**: Polish & Optimization (1 hour)

**Total Estimated Time**: 14.5 hours

---

## Phase 1: Documentation & Planning (30 minutes)

### Task 1.1: Create Planning Documents
**File**: `docs/PLAN.md` ✅ **Done** (This file)  
**Action**: Create comprehensive project plan document  
**Status**: Complete  
**Timestamp**: August 27, 2025 14:30 UTC

### Task 1.2: Update Progress Tracking  
**File**: `docs/PROGRESS.md`  
**Action**: Create progress tracking document  
**Status**: ToDo  
**Content**:
- Task completion checklist
- Known issues and blockers
- Testing requirements
- Deployment considerations

### Task 1.3: Document Current State
**Action**: Analyze and document existing components structure  
**Status**: ToDo  
**Files to examine**:
- `app/page.tsx` (current dashboard)
- `components/layout/` (current navigation)
- `lib/stores/` (current state management)
- `app/{analytics,artifacts,logs,settings,tasks}/` (current pages)

---

## Phase 2: Layout Architecture Changes (2 hours)

### Task 2.1: Header Component Enhancement
**File**: `components/layout/header.tsx`  
**Status**: ToDo  
**Requirements**:
- Add global chat icon with modal/drawer functionality
- Integrate user profile and system status
- Ensure responsive design across all breakpoints
- Add search functionality placeholder

**New Features**:
- Global chat access via header button
- System health indicator in header
- User profile dropdown

### Task 2.2: Sidebar Navigation Restructure  
**File**: `components/layout/sidebar.tsx`  
**Status**: ToDo  
**Requirements**:
- Replace current agent-based navigation with SDLC process navigation
- Navigation items: Dashboard, Requirements, Design, Dev, Test, Deploy, Logs, Settings
- Add notification indicators (!) for stages requiring attention
- Add system health and global stats at bottom
- Maintain collapsible functionality

**Navigation Structure**:
```typescript
const processNavigation = [
  { name: 'Dashboard', path: '/', icon: HomeIcon },
  { name: 'Requirements', path: '/requirements', icon: DocumentIcon, alert: true },
  { name: 'Design', path: '/design', icon: CubeIcon },
  { name: 'Dev', path: '/dev', icon: CodeIcon, alert: true },
  { name: 'Test', path: '/test', icon: BeakerIcon },
  { name: 'Deploy', path: '/deploy', icon: RocketIcon },
  { name: 'Logs', path: '/logs', icon: DocumentTextIcon },
  { name: 'Settings', path: '/settings', icon: CogIcon }
]
```

### Task 2.3: Global Chat Component
**File**: `components/chat/global-chat-modal.tsx`  
**Status**: ToDo  
**Requirements**:
- Modal/drawer implementation using shadcn/ui Dialog
- Full chat functionality with agent communication
- Maintain existing WebSocket integration  
- Mobile-responsive design
- Persistent chat history across page navigation

### Task 2.4: Layout Wrapper Updates
**File**: `app/layout.tsx`  
**Status**: ToDo  
**Requirements**:
- Integrate new header with global chat
- Update sidebar with process navigation
- Ensure all pages use consistent layout
- Add proper meta tags and SEO elements

---

## Phase 3: Dashboard Redesign (3 hours)

### Task 3.1: Process Summary Component
**File**: `components/dashboard/process-summary.tsx`  
**Status**: ToDo  
**Requirements**:
- Horizontal layout showing Requirements → Design → Dev → Test → Deploy
- Each stage shows: status icon, agent name, current deliverable, task count
- HITL indicators and pause buttons for each stage
- Status badges (Done ✅, WIP 🟡, Queued ⏸️, Error ❌, Waiting !)
- Mobile responsive with horizontal scroll

**Component Structure**:
```typescript
interface ProcessStage {
  name: string;
  status: 'done' | 'wip' | 'queued' | 'error' | 'waiting';
  agent: string;
  deliverable: string;
  taskProgress: { completed: number; total: number };
  hitlRequired: boolean;
  onPause: () => void;
}
```

### Task 3.2: Dashboard Layout Restructure
**File**: `app/page.tsx`  
**Status**: ToDo  
**Requirements**:
- Move process summary to top (above fold)
- Remove individual agent status cards
- Remove current chat window (now in header)
- Add global stats section below process summary
- Ensure above-fold content is optimized

### Task 3.3: Global Statistics Component
**File**: `components/dashboard/global-statistics.tsx`  
**Status**: ToDo  
**Requirements**:
- Total tasks, status breakdown (Queued, WIP, Done, Error)
- Visual charts (pie chart for status distribution)
- System health indicators
- Performance metrics display
- Compact design for dashboard integration

---

## Phase 4: Stage Pages Implementation (6 hours)

### Task 4.1: Base Stage Page Template
**File**: `components/stages/base-stage-page.tsx`  
**Status**: ToDo  
**Requirements**:
- Reusable template for all stage pages
- Tab system (Progress, Config)
- Current stage banner with HITL indicators
- Consistent styling and responsive design

**Template Structure**:
```typescript
interface BaseStagePageProps {
  stageName: string;
  currentTask: string;
  agent: string;
  hitlRequired: boolean;
  artifacts: Artifact[];
  tasks: Task[];
  onPause: () => void;
  children?: React.ReactNode;
}
```

### Task 4.2: Requirements Stage Page
**File**: `app/requirements/page.tsx`  
**Status**: ToDo  
**Requirements**:
- Implement using base template
- Artifacts: Project Plan, SRS Document, Use Case Diagrams, Risk Analysis
- Tasks specific to requirements gathering phase
- Agent configuration for Business Analyst
- Stage-specific chat context

### Task 4.3: Design Stage Page
**File**: `app/design/page.tsx`  
**Status**: ToDo  
**Requirements**:
- Implement using base template
- Artifacts: System Design Doc, UI/UX Prototypes, Database Schema, API Specifications
- Tasks specific to design phase
- Agent configuration for Architect
- Design-specific tools integration

### Task 4.4: Development Stage Page
**File**: `app/dev/page.tsx`  
**Status**: ToDo  
**Requirements**:
- Implement using base template
- Artifacts: Source Code (with accordion for file tree), Unit Tests, Documentation
- Tasks specific to development phase
- Agent configuration for Developer
- Code review and version control integration

### Task 4.5: Testing Stage Page
**File**: `app/test/page.tsx`  
**Status**: ToDo  
**Requirements**:
- Implement using base template
- Artifacts: Test Plan, Test Cases, Test Logs, Defect Reports
- Tasks specific to testing phase
- Agent configuration for QA Tester
- Test execution and reporting tools

### Task 4.6: Deploy Stage Page
**File**: `app/deploy/page.tsx`  
**Status**: ToDo  
**Requirements**:
- Implement using base template
- Artifacts: Build/Executable, Deployment Scripts, User Manual, Installation Guide
- Tasks specific to deployment phase
- Agent configuration for System Administrator
- Deployment monitoring and rollback capabilities

### Task 4.7: Shared Components for Stage Pages

#### Artifacts List Component
**File**: `components/stages/artifacts-list.tsx`  
**Status**: ToDo  
**Requirements**:
- Table format for most artifacts
- Accordion functionality for multi-file artifacts (especially Development)
- Download, open, and share actions
- Status indicators (WIP, Done, Queued)
- File type specific icons

#### Tasks List Component  
**File**: `components/stages/tasks-list.tsx`  
**Status**: ToDo  
**Requirements**:
- Chronological task ordering
- Status badges with proper coloring
- Agent assignment display
- Timestamp tracking
- HITL task highlighting

#### Stage Configuration Component
**File**: `components/stages/stage-config.tsx`  
**Status**: ToDo  
**Requirements**:
- Agent role configuration (upload .md files)
- Artifact selection/configuration
- Stage-specific settings
- Validation and error handling

---

## Phase 5: Integration & Testing (2 hours)

### Task 5.1: State Management Updates
**Files**: `lib/stores/*.ts`  
**Status**: ToDo  
**Requirements**:
- Update agent store for process-centric data
- Add stage-specific state management
- Ensure WebSocket integration works with new components
- Add global chat state management

### Task 5.2: WebSocket Integration
**File**: `lib/websocket/websocket-service.ts`  
**Status**: ToDo  
**Requirements**:
- Ensure all process view components receive real-time updates
- Add stage-specific message routing
- Update message types for process-centric data
- Test HITL functionality across all stages

### Task 5.3: Navigation & Routing
**File**: Next.js routing  
**Status**: ToDo  
**Requirements**:
- Test all page transitions
- Ensure proper active states in navigation
- Validate deep linking works correctly
- Test responsive behavior across devices

### Task 5.4: Data Flow Testing
**Status**: ToDo  
**Requirements**:
- Test agent status updates across all components
- Verify artifact management works correctly
- Confirm task progression updates properly
- Validate HITL pause/resume functionality

---

## Phase 6: Polish & Optimization (1 hour)

### Task 6.1: Responsive Design Review
**Status**: ToDo  
**Requirements**:
- Test all components on mobile, tablet, desktop
- Ensure horizontal process summary scrolls properly on mobile
- Verify accordion functionality works on touch devices
- Optimize loading states and transitions

### Task 6.2: Performance Optimization
**Status**: ToDo  
**Requirements**:
- Implement lazy loading for stage pages
- Optimize WebSocket message handling
- Add proper error boundaries
- Ensure smooth animations and transitions

### Task 6.3: Accessibility & UX
**Status**: ToDo  
**Requirements**:
- Add proper ARIA labels and keyboard navigation
- Ensure color contrast meets accessibility standards
- Add loading states and empty states
- Implement proper focus management

---

## Technical Architecture Details

### State Management Changes
**Current**: Agent-centric stores (agent status, individual agent data)  
**New**: Process-centric stores (stage status, stage-specific data, global process state)

### Component Architecture Standards
- Use shadcn/ui components consistently
- Implement proper TypeScript interfaces
- Follow existing naming conventions
- Maintain responsive design patterns
- Ensure WebSocket integration in all components

### Data Flow Preservation
- All existing WebSocket functionality must be maintained
- Agent orchestration backend remains unchanged
- Real-time updates must work across all new components  
- HITL functionality must be preserved and enhanced

### New Features Required

1. **Global Chat Modal**: Header-accessible chat with persistent history
2. **Stage Notifications**: Alert indicators in sidebar navigation
3. **Process Summary**: Horizontal stage flow with status indicators
4. **Artifact Accordions**: Expandable file lists (especially for Development)
5. **Stage Configuration**: Role upload and artifact selection per stage
6. **Responsive Process View**: Mobile-optimized horizontal process summary

---

## File Structure Changes

### New Files to Create:
```
components/
├── layout/
│   └── header.tsx (enhanced)
├── chat/
│   └── global-chat-modal.tsx (new)
├── dashboard/
│   ├── process-summary.tsx (new)
│   └── global-statistics.tsx (new)
└── stages/
    ├── base-stage-page.tsx (new)
    ├── artifacts-list.tsx (new)
    ├── tasks-list.tsx (new)
    └── stage-config.tsx (new)

app/
├── requirements/page.tsx (new)
├── design/page.tsx (new)
├── dev/page.tsx (new)
├── test/page.tsx (new)
└── deploy/page.tsx (new)
```

### Files to Modify:
```
app/
├── layout.tsx (header integration)
└── page.tsx (dashboard redesign)

components/layout/
└── sidebar.tsx (navigation restructure)

lib/stores/
└── *.ts (process-centric state management)
```

---

## Critical Success Factors

1. **No Functionality Loss**: All existing features must work in new interface
2. **Performance Maintained**: WebSocket updates must remain real-time
3. **Mobile Responsive**: All new components must work on mobile devices
4. **Consistent Styling**: Maintain shadcn/ui design system throughout
5. **Accessible Design**: Proper ARIA labels and keyboard navigation

---

## Dependencies & Risk Management

### Dependencies
- Existing WebSocket service must be compatible with new components
- Agent state management needs refactoring for process-centric view
- Global chat requires new modal/drawer implementation

### Risks
- Process summary horizontal layout may be complex on mobile
- Stage page file accordions may impact performance with many files
- Global chat state management could interfere with existing chat functionality

### Mitigation Strategies
- Implement mobile-first design for process summary  
- Use virtual scrolling or pagination for large file lists
- Create isolated state management for global chat

---

## Testing Strategy

### Unit Testing
- Test all new components with React Testing Library
- Mock WebSocket connections for component testing
- Test state management updates with proper mocking

### Integration Testing
- Test complete user workflows from dashboard to stage pages
- Verify WebSocket message handling across all components
- Test responsive behavior on multiple screen sizes

### User Acceptance Testing
- Compare functionality with existing agent-centric interface
- Verify all HITL controls work properly
- Test complete SDLC workflow end-to-end

---

## Deployment Considerations

### Development
- Use feature branch for all changes
- Regular commits with descriptive messages
- Test locally before pushing to remote

### Production
- Ensure backward compatibility during transition
- Plan for rollback if issues arise
- Monitor performance after deployment

### Post-Deployment
- Gather user feedback on new interface
- Monitor for any performance regressions
- Plan iterative improvements based on usage patterns

---

**Next Steps**: Jules should start with Task 1.2 (creating PROGRESS.md) and then Task 1.3 (analyzing current state) before beginning implementation.

**Success Metric**: User can navigate entire SDLC process from dashboard, drill into any stage for detailed view, and maintain all existing agent communication and HITL functionality.
