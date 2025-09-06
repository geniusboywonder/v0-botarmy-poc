# Instructions for AI Agent

- **Always follow** the **Code Protocol** in `docs/CODEPROTOCOL.md`.
- **Always follow** the **Style Guide** in `docs/STYLEGUIDE.md`  
- Use the **README** to understand project context and structure.  
- Use `https://github.com/geniusboywonder/v0-botarmy-poc` as the code base.
- Document plans with detailed, **timestamped steps** in `docs/PLAN.md`.  
- Track progress with **timestamped updates** in `docs/PROGRESS.md`.
  
- **Review and understand** existing requirements, codebase, structure, and functions **before starting**.  
- **Update plan and progress files incrementally** after each step to avoid loss or token limits.  
  
- You are `senior full-stack developer`, experienced in architecture, coding standards, modularization, current UX & UI trends, and best practices.  
  
## Planning  

- **Break tasks into small, manageable steps**.  
- For each step, state:  
  - What code is needed  
  - How it must be written (standards, modularity, interdependencies)  
- **Avoid writing actual code**, except sample scaffolding to clarify new points.  
- Note any **new functions or features** if gaps exist between requirements and code.  
  
- Communicate all plans and progress **in the respective files** for team transparency.  
  
- **Ask clarifying questions** before starting to remove ambiguity.  
- **State all assumptions** clearly.  

---    ## Goal    Fix the BotArmy HITL features and make sure the front and back end work seamlessly with comprehensive testing suite and pupeteer visual checks.  

---      [specific_tasks_placeholder]  
Use pupeteer to thoroughly check each sceanrio works. the backend and frontend are currently up and running. Current issues:

1) the screen "recenters" when clicking into the chat text-inpt box. the screen should not scroll or move when clicking into the text-input
2) the outcome of clicking on a HITL action is still not recorded and showing in the chat window. it needs to show as a message as if sent by the User.
