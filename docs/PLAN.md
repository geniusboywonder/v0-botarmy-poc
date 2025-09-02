# BotArmy Project Plan

This document outlines the development plan for updating the app with changes to dynamic process and artifact generation.

---

## 2025-01-10 16:00:00 UTC - Dynamic Process and Artifact Generation Update

**Goal:** Update the app with changes to the dynamic process and artifact generation using the provided mockup as a reference for the current Dashboard Process Summary element.

**Current Architecture Analysis:**
- **Frontend**: Next.js with React 19, TypeScript, Zustand state management
- **Backend**: FastAPI with ControlFlow + Prefect orchestration  
- **Agent System**: Specialist agents (Analyst, Architect, Developer, Tester, Deployer)
- **Workflow**: 5-stage process (Analyze/Plan, Design, Build, Test, Deploy)
- **Communication**: WebSocket-based real-time messaging
- **UI Components**: Existing ProcessSummary and EnhancedProcessSummary components

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