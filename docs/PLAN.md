# BotArmy Frontend Refactor Plan: Agent to Process-Based Focus

**Date Created**: December 18, 2024 - 10:30 AM  
**Objective**: Refactor frontend from agent-based to process-based focus while maintaining all existing functionality

## Phase 1: Analysis & Structure (30 minutes)
### Task 1.1: Codebase Analysis
- [ ] Review existing components and identify unused code
- [ ] Map current agent-based structure to new process-based structure  
- [ ] Document component dependencies and data flows
- [ ] Identify reusable components vs components needing refactor

### Task 1.2: Process Stage Mapping
- [ ] Map 5 process stages to existing agent workflow
- [ ] Define data models for process-based state management
- [ ] Plan integration points for real API data

## Phase 2: Dashboard Refactor (45 minutes)
### Task 2.1: Process Summary Fix
- [ ] Reduce Process Summary block heights by 50%+ 
- [ ] Make all 5 blocks uniform height
- [ ] Adjust widths to fit all 5 blocks on page width
- [ ] Ensure responsive design for different screen sizes

### Task 2.2: Dashboard Chat Integration
- [ ] Add chat component above the fold, below Process Summary
- [ ] Integrate with existing WebSocket service
- [ ] Adjust dashboard proportions to accommodate chat
- [ ] Implement real-time message display

### Task 2.3: Button Migration & Header Cleanup
- [ ] Move Clear Log, Test Backend, Test OpenAI buttons to Logs page
- [ ] Remove Metric button from dashboard
- [ ] Fix header row layout issues (overlapping icons/menus)
- [ ] Clean up search bar area positioning

## Phase 3: Stage Pages Enhancement (30 minutes)
### Task 3.1: Add Missing Navigation
- [ ] Add header component to all stage pages
- [ ] Add sidebar component to all stage pages  
- [ ] Ensure consistent navigation experience
- [ ] Test routing between stage pages

## Phase 4: Configuration Pages Redesign (45 minutes)
### Task 4.1: Stage Configuration Page
- [ ] Create bordered box layout with clear heading
- [ ] Reorganize controls for better UX
- [ ] Apply consistent site styling

### Task 4.2: Artifact Generation Page  
- [ ] Create bordered box layout with clear heading
- [ ] Reorganize controls for better UX
- [ ] Apply consistent site styling

### Task 4.3: Stage Settings Page
- [ ] Create bordered box layout with clear heading
- [ ] Reorganize controls for better UX  
- [ ] Apply consistent site styling

## Phase 5: Sidebar Enhancement (15 minutes)
### Task 5.1: System Health & Service Repositioning
- [ ] Move System Health section above the fold
- [ ] Move Service section above the fold
- [ ] Position directly under last menu item
- [ ] Ensure visibility and accessibility

## Phase 6: Real Data Integration (60 minutes)
### Task 6.1: API Integration
- [ ] Connect process stages to real backend APIs
- [ ] Replace dummy data in all components
- [ ] Implement error handling for API calls
- [ ] Add loading states for data fetching

### Task 6.2: State Management Update
- [ ] Update Zustand stores for process-based data
- [ ] Implement real-time data updates via WebSocket
- [ ] Add data persistence where needed
- [ ] Test all data flows end-to-end

## Phase 7: Code Cleanup & Optimization (30 minutes)  
### Task 7.1: Remove Unused Code
- [ ] Identify and remove unused components
- [ ] Clean up unused imports and dependencies
- [ ] Remove redundant state management
- [ ] Update routing and navigation

### Task 7.2: Testing & Validation
- [ ] Test all pages and functionality
- [ ] Validate responsive design
- [ ] Test real API integrations
- [ ] Document any remaining issues

## Dependencies & Interdependencies

### Critical Path Dependencies:
1. Dashboard chat requires Process Summary resize (Tasks 2.1 → 2.2)
2. Real data integration requires API analysis (Tasks 1.1 → 6.1) 
3. Stage pages navigation requires consistent header/sidebar (Tasks 3.1 → 4.x)

### Technical Interdependencies:
- WebSocket service integration affects chat and real-time updates
- State management changes impact all data-driven components  
- Styling consistency requires coordinated CSS/Tailwind updates

## Risk Mitigation:
- Checkpoint code after each major task completion
- Test functionality after each phase before moving to next
- Maintain backup of current working state before major changes
- Document any breaking changes for rollback capability

## Success Criteria:
- [ ] All 5 process stages fit uniformly on dashboard width
- [ ] Chat functionality working with real-time updates
- [ ] All stage pages have proper navigation
- [ ] Configuration pages follow consistent design patterns
- [ ] System health visible above the fold
- [ ] All dummy data replaced with real API data
- [ ] No unused code remains in codebase
