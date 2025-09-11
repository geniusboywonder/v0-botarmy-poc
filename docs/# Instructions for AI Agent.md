# Instructions for AI Agent

- **Always follow** the **Code Protocol** in `docs/CODEPROTOCOL.md`.
- **Always follow** the **Style Guide** in `docs/STYLEGUIDE.md`  
- Use the **README** to understand project context and structure.  
- Use `https://github.com/geniusboywonder/v0-botarmy-poc` as the code base.
- Document plans with detailed, **timestamped steps** in `docs/PLAN.md`.  
- Track progress with **timestamped updates** in `docs/PROGRESS.md`.
  
- **Review and understand** existing requirements, codebase, structure, and functions **before starting**.  
- **Update plan and progress files incrementally** after each step to avoid loss or token limits.  
  
- You are senior full-stack `test-writer-fixer`, experienced in architecture, coding standards, modularization, current UX & UI trends, and best practices.  
  
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

---    ## Goal    Fix the BotArmy application and make sure the front and back end work seamlessly with comprehensive testing suite and pupeteer visual checks.  

---      [specific_tasks_placeholder]  
Insert breakpoints at relevent points so we can run and test and correct as we go.
Start the front end and backend.
Run a full test using pupeteer. Ensure that all settings in .env are correct to allow the full test:

- enter "start project to build a "Hello World" html page"
expected flow:

1) project specific workflow will initialise
2) Analyst Agent will start and either ask clarifying questions, or kciking off task.
3) Process Summary UI will update to show:

- Create Analysis Execution Plan change from QUEUED to WIP
- Analysis Execution Plan change from QUEUED to WIP
- Artifact Summary change from QUEUED to WIP
- Analyze Stage change from QUEUED to WIP

4) Analyst creates Analysis Execution Plan.md
5) Analyst pauses for HITL approval and:

- HITL message appears in chat window
- HITL alert appears in HITL Alert bar
- HITL badge appears in task "Create Analysis Execution Plan"

6) Process pauses until HITL ocurs

IF ANY OF THE EXPECTED ITEMS DO NOT OCCUR IN THE NECESSARY ORDER, PAUSE THE PROCESS.
Understand what has ocured. Report on the last successful step, and investigate why the step failed.
Take instruction to correct it before continuing.
