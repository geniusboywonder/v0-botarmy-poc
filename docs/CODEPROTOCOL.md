# Frontend Transition Plan: Agent-based to Process-based

**Date**: 2025-08-28 15:59 SAST

## Objective

Restructure website frontend to emphasize process-based views per `mockups/ProcessView`, preserving existing functionality and styling.

## Steps

1. **Scan Codebase** (2025-08-28)
   - Run `git ls-files | grep -v -f .cursorignore` to list files.
   - Review `README.md` for tech stack and architecture.
   - Map dependencies (e.g., npm packages, components).
   - Outcome: List of existing pages (e.g., `src/pages/*`), components, and styles.

2. **Analyze Mockups** (2025-08-28)
   - Read `mockups/ProcessView/*.txt` for new page layouts or components.
   - Identify gaps (e.g., new `ProcessTimeline` component).
   - Outcome: List of required pages (e.g., `/process-view`), components, and interdependencies.

3. **Restructure Navigation** (2025-08-29)
   - Update `src/routes.js` to add process-based routes (e.g., `/process-view`).
   - Reuse existing menu components; adjust for new navigation.
   - Interdependency: Check for backend API support.

4. **Create New Components** (2025-08-29)
   - If needed, create `src/components/ProcessTimeline.jsx` for process visualization.
   - Use existing styles (e.g., `src/styles/global.css`).
   - Outcome: Modular, reusable component with error handling.

5. **Test Changes** (2025-08-30)
   - Run unit tests for new components/routes.
   - Test browser compatibility and functionality.
   - Fix errors before merging.

6. **Document Updates** (2025-08-30)
   - Update `README.md` with new routes/components.
   - Log progress in `docs/PROGRESS.md`.

## Assumptions

- Codebase uses React and CSS/Tailwind.
- Mockups describe new page layouts and navigation.
- No backend changes needed unless mockups specify new data.

## Clarifications Needed

- Specific `.txt` files in `mockups/ProcessView`.
- Definition of “Process-based” focus.
- Existing component inventory.
