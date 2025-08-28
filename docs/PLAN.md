# BotArmy Frontend Fixes Plan: Dashboard & UI Issues

**Date Created**: August 28, 2025 - 3:00 PM  
**Objective**: Fix specific front-end issues with Dashboard, Stage Pages, Header, and Logs functionality
**Branch**: `fix/frontend-component-build`

## Issues to Fix

### 1. Dashboard - Process Summary Stage Blocks
- [x] **Analysis Complete** - Issues identified in ProcessSummary component
- [ ] **Fix Consistent Sizing** - All stage blocks should be uniform height and width
- [ ] **Remove Duplicate Pause Button** - Only one pause icon needed per stage
- [ ] **Reduce Border Spacing** - Minimize top/bottom border of stage boxes
- [ ] **Fix Text Truncation** - Prevent text wrapping, cut off text at edge

### 2. Stage Pages - Config Tabs  
- [x] **Analysis Complete** - StageConfig component exists and has 3 sections
- [ ] **Verify Config Tabs** - Ensure all stage pages show Config tab correctly
- [ ] **Test Config Content** - Verify Config tab content loads properly

### 3. Header Layout
- [x] **Analysis Complete** - Header component has layout issues 
- [ ] **Fix Search Bar Layout** - Proper positioning and spacing
- [ ] **Fix Icon Positioning** - Prevent overlapping of icons/menus
- [ ] **Improve Responsive Design** - Better mobile/desktop layout

### 4. Logs Page - Test Buttons
- [x] **Analysis Complete** - Test methods exist in WebSocket service
- [ ] **Debug Test Backend** - Fix backend test logging
- [ ] **Debug Test OpenAI** - Fix OpenAI test logging  
- [ ] **Verify Log Display** - Ensure messages appear in JSONL viewer

## Implementation Plan

### Phase 1: Dashboard Process Summary Fixes (30 minutes)
**Task 1.1: Fix Stage Block Layout**
- Standardize block heights and widths
- Remove duplicate pause button
- Implement proper text truncation
- Reduce excessive padding/borders

### Phase 2: Header Layout Fixes (20 minutes)  
**Task 2.1: Fix Header Responsive Layout**
- Improve flexbox spacing
- Fix search bar width and positioning
- Ensure icons don't overlap
- Test on different screen sizes

### Phase 3: Stage Pages Config Tabs (15 minutes)
**Task 3.1: Verify Config Tab Implementation** 
- Test all 5 stage pages (Requirements, Design, Dev, Test, Deploy)
- Ensure Config tab appears and loads content
- Verify StageConfig component functionality

### Phase 4: Logs Page Test Button Functionality (15 minutes)
**Task 4.1: Fix Test Button Log Display**
- Debug WebSocket test methods
- Ensure logs appear in JSONL viewer
- Test both "Test Backend" and "Test OpenAI" buttons

## Dependencies & Risk Mitigation
- Keep development server running for real-time testing
- Test each fix immediately before moving to next
- Maintain existing functionality while fixing issues
- Document any breaking changes

## Success Criteria  
- [ ] Dashboard Process Summary has uniform, properly-sized blocks
- [ ] Only one pause button per stage block
- [ ] Text truncates properly without wrapping
- [ ] Header layout is clean with proper spacing
- [ ] All stage pages show working Config tabs
- [ ] Test buttons on Logs page show messages in viewer

## Time Estimate: 80 minutes total
**Priority**: High - These are visual and functional bugs affecting user experience
