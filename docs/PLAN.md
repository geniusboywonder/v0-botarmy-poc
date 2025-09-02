# BotArmy Project Plan

This document outlines the development plan for implementing the 10-step interactive workflow as specified in Final-Integration-Prompt.md.

---

## 2025-09-02 - Interactive SDLC Workflow Implementation

### **Current Architecture Analysis (Based on CODEPROTOCOL Scan):**

**Discovered Existing Systems:**
- **YAML-Driven Process Configuration**: `/backend/configs/processes/sdlc.yaml` - Defines roles, stages, tasks, artifacts
- **Generic Orchestrator**: `/backend/workflow/generic_orchestrator.py` - Executes YAML-configured workflows  
- **Process Config Loader**: `/backend/services/process_config_loader.py` - Dynamic YAML loading with validation
- **Generic Agent Executor**: `/backend/agents/generic_agent_executor.py` - Role-based agent execution with security
- **JSON Schema Validation**: `/backend/schemas/process_schema.json` - YAML configuration validation

**Frontend Stack:**
- **Next.js 15** with React 19, TypeScript
- **Zustand State Management**: Agent, conversation, log stores
- **WebSocket Service**: Real-time communication
- **shadcn/ui Components**: Complete UI component library

**Backend Stack:**  
- **FastAPI** with async WebSocket support
- **ControlFlow + Prefect** orchestration  
- **Multi-LLM Support**: OpenAI, Anthropic Claude, Google Gemini
- **Security Features**: Input sanitization, rate limiting, YAML validation
- **Connection Pooling**: HTTP optimization for LLM providers

**Mockup Reference:**
```
+------------------------------------------------------------------+
| Process Summary                                                  |
| Building a Hello World page in React                            |
| +---------+    +--------+    +-------+    +------+    +-------+  |
| | Plan    | -> | Design | -> | Build | -> | Test | -> | Deploy|  |
| | Agent   |    | Agent  |    | Agent |    | Agent|    | Agent |  |
| | Status  |    | Status |    | Status|    | Status|   | Status|  |
| +---------+    +--------+    +-------+    +------+    +-------+  |
```

---

### **Task 00: Use Mockup as Reference for Dashboard Process Summary Element**

**Objective:** Implement the mockup design as a working example for the current Dashboard Process Summary element.

**Timestamp:** 2025-01-10 16:05:00 UTC
**What:** Create/update the Process Summary component to match the provided mockup exactly
**Requirements:**
- Horizontal flow layout with 5 stage cards (Plan, Design, Build, Test, Deploy)
- Each card shows: Stage Name, Agent Name, Status
- Clear visual progression with arrows between stages
- Clean, consistent typography and spacing
- Status indicators with appropriate colors/icons
- Integration with existing process store data

**Implementation Steps:**
1. **Enhance SimplifiedProcessSummary Component**
   - Add agent name display in each card
   - Implement status indicators (done, wip, queued, error)
   - Add proper card structure with stage name, agent, status layout
   - Include connecting arrows between stages
   - Ensure responsive design

2. **Update Main Dashboard Integration**
   - Verify component is properly imported and used in main dashboard
   - Ensure proper spacing and layout within dashboard grid
   - Test integration with existing process store

3. **Visual Validation**
   - Capture screenshots to compare with mockup
   - Test responsive behavior across screen sizes
   - Validate status indicators and transitions

**Files to Modify:**
- `components/dashboard/simplified-process-summary.tsx` - Main component enhancement
- `app/page.tsx` - Ensure correct component usage
- Potentially update process store if data structure needs adjustment

**Success Criteria:**
- Visual implementation matches provided mockup exactly
- Component displays stage name, agent name, and status for each stage
- Horizontal flow with connecting arrows
- Responsive design maintains usability
- Integration works with existing process store data

---

### **Subsequent Tasks (To be defined after Task 00 completion):**

Additional tasks related to dynamic process and artifact generation will be planned after the initial mockup implementation is completed and tested.

---

## Implementation Notes

**Key Design Elements:**
- Horizontal card layout with consistent sizing
- Clear visual hierarchy (stage name prominent, agent secondary, status indicator)
- Color-coded status system
- Smooth transitions and responsive behavior

**Data Integration:**
- Use existing `useProcessStore` for stage data
- Maintain compatibility with current WebSocket updates
- Handle loading states appropriately
- Support fallback data when no real process is active

**Testing Requirements:**
- Visual comparison with provided mockup
- Responsive testing (desktop 1440px, tablet 768px, mobile 375px)
- Integration testing with process store
- Status transition testing