# CODING PROTOCOL

## **Core Rules (Follow in Order, step-by-step for every task**

### 1. **Scan First**

- Read README.md and scan project structure with `git ls-files | grep -v -f (sed 's|^|^|; s|$|/|' .cursorignore | psub)` to understand the project's context and files
- Review before any changes
- Never create what already exists - check thoroughly first
- Respect existing patterns, architecture, and naming conventions

### 2. **Plan & Track**

- Read and update all plans in `docs/PLAN.md`
- Read and update all progress in `docs/PROGRESS.md`
- **Avoid writing actual code during planning**, except sample scaffolding to clarify new points
- Break work into logical steps (3-7 items max)
- Seek clarification for ambiguities before coding
- Always state assumptions

### 3. **Code Standards**

- Follow existing project conventions (naming, structure, dependencies)
- Write modular, reusable code with proper error handling and follows DRY (Don't Repeat Yourself) principles
- Test changes in isolation before integration
- Follow the style guide in `docs/STYLEGUIDE.md`

### 4. **Save & Document**

- **Isolate and track changes** to maintain project integrity and use branching strategies (e.g., feature branches) to isolate changes.
- **Regularly pull from the main branch** to stay in sync and avoid merge conflicts.
- **Archive or version old code** instead of deleting to preserve history.
- **Enforce code linting and formatting tools** to match project standards before commits.
- Commit code after each feature is completed with clear messages
- Update documentation alongside code changes with chronological task tracking
- Record decisions and blockers in progress file
- clearly state if code has not been tested

## **Checkpoint Protocol**

If approaching token or window limits :

1. Save current work to versioned files: `filename_WIP_timestamp.ext`
2. Update `docs/PROGRESS.md` with current status
3. Provide clear resume instructions

## **Enforcement**

- **Stay in scope** - don't expand tasks without approval
- **No assumptions** - ask rather than guess
- **Fix immediately** - address errors before proceeding

---
*This protocol replaces all previous coding instructions. Follow sequentially for every coding task.*
