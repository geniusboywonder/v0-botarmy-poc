# AI Coding Agent Protocol

This protocol provides a clear, structured guide for AI coding agents to follow when working on projects. It emphasizes **respect for the existing codebase**, **precision**, and **avoidance of assumptions or inventions**. Agents must adhere to these rules sequentially where applicable, documenting deviations or issues immediately. Rules have been consolidated to reduce redundancy (e.g., combining similar checks for new files/functions) and eliminate potential contradictions (e.g., ensuring no overlap between scanning and creation rules). Follow this protocol **step-by-step** for every task to prevent confusion or errors.

## 1. **Understand and Respect the Existing Project**

   Before any action, **always prioritize scanning and respecting the current state** to avoid duplication or disruption.

- **Never make up things that aren’t part of the actual project**, skip or ignore the existing system, or deviate from it.
- **Be precise and respectful of the current codebase**: Adhere strictly to existing architecture diagrams, patterns, and standards without deviation.
- **Read README.md first**, then run `git ls-files | grep -v -f (sed 's|^|^|; s|$|/|' .cursorignore | psub)` to understand the project's context and files (ignoring any specified in .cursorignore).
- **Always scan the entire project structure** before making changes to avoid duplication. **Request a modular breakdown of the codebase** to understand its components, **map dependencies between components**, and **list dependencies for each component** to ensure clarity on interactions and requirements.
- **Don't create new files, structures, or functions** without checking if they already exist by another name or folder structure.
- **Reuse existing utilities or libraries** instead of reinventing functionality.

## 2. **Plan and Break Down Work**

   Before coding, **create a clear plan** by breaking the task into manageable, well-defined steps to ensure clarity and efficiency.

- **Analyze the task requirements** and identify key components, dependencies, and potential challenges.
- **Break the task into smaller, logical steps** (e.g., functions, modules, or features) to simplify implementation and testing.
- **Document the plan** in the designated progress file (e.g., ClaudeProgress.md) with a clear outline of steps, expected outcomes, and any assumptions.
- **Validate the plan** by cross-referencing with the existing codebase and project requirements to ensure alignment.
- **Seek human input (HITL)** if the plan reveals ambiguities or requires clarification before proceeding.

## 3. **Coding and Implementation Practices**

   Focus on **modular, secure, and maintainable code** that aligns with project standards. **Prioritize readability** with meaningful variable names and concise functions.

- **Use consistent naming conventions** matching the current codebase (e.g., camelCase, snake_case).
- **Ensure all new code is modular, reusable, and follows DRY (Don't Repeat Yourself) principles**.
- **Replace mock functions or data with real implementations** only after verifying necessities.
- **Handle errors and edge cases explicitly**, logging them for traceability.
- **Avoid hardcoding values**: Use configuration files or environment variables instead.
- **Review code for security best practices**, like input validation and dependency checks.
- **Optimize performance only if bottlenecks are identified through profiling**, not prematurely.
- **Ensure cross-compatibility** with existing dependencies and versions.
- **Test new code in isolation** before integration to prevent breaking existing functionality.

## 4. **Version Control and Change Management**

   **Isolate and track changes** to maintain project integrity. Use branching strategies (e.g., feature branches) to isolate changes.

- **Commit changes frequently** with clear, descriptive messages referencing the task or issue.
- **Regularly pull from the main branch** to stay in sync and avoid merge conflicts.
- **Archive or version old code** instead of deleting to preserve history.
- **Enforce code linting and formatting tools** to match project standards before commits.

## 5. **Documentation and Communication**

   **Document everything** to ensure transparency and traceability. Maintain chronological task tracking to show clear progress without gaps.

- **Document every step, decision, and change** in the designated progress file (e.g., ClaudeProgress.md).
- **Update documentation** (e.g., README, inline comments) alongside code modifications.
- **Communicate progress, blockers, or clarifications needed** before proceeding to next steps.
- **Pause and seek human input (HITL)** for ambiguous requirements to prevent drift.
- **Limit scope to assigned tasks**: Don't expand without explicit approval.

## Key Enforcement Rules

- **Review your execution**: After any change, check for errors, failures, or delays, and fix them immediately.
- **Apply learnings**: Note insights from each task for future improvements, but document them in the progress file without altering this protocol.
