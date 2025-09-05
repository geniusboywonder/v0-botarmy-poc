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

---  

## Goal  

**[goal]**  Optimsie the BotArmy application and make sure the front and back end work seamlessly.

---  
  
`[specific_tasks_placeholder]`
 review and simplify the HITL system logic. Include  appearance of HITL prompts in the chat, HITL filtering, HITL alerting and HITL badges. The system to function like this:

1) whenever an  agent requires HITL, an HITL is created for tracking and action and logged to the appropriate stores.
2) each HITL prompt must be linked to an agent.
3) whenever an HITL is created:

- an HITL alert is shown in the Alert Bar.
- an HITL badge is shown in the Artifact Summary, against the Artifact that requires the HITL.
- an HITL prompt is visible in the chat window WHEN USING THE CORRECT AGENT FILTER.

4) no hitl prompt should appear in the general chat window.
5) only hitl prompts related to that specific agent should show when that agent filter is selected in the chat window.
6) when toggling an agent filter, the relevent HITLs should show or hide as approppriate.
7) when clicking on a HITL alert:

- navigate to the chat window, select the appropriate agent filter (and the HITL prompt should then show)

8) when clicking on a HITL badge:

- navigate to the chat window, select the appropriate agent filter (and the HITL prompt should then show)

9) once the HITL is actioned:

- the appropriate Alert is removed from the alert bar
- the appropriate HITL badge is removed from the Artifact Summary, if there was more than one HITL, then the count in the HITL badge are updated.

10) the action taken by the HITL is logged correctly in the appropriate stores.

Current issue remains that when in general chat, and then clicking on an HITL alert or HITL badge, the correct behaviour occurs with the correct agent filter being highlighted in the chat. However the HITL prompt does not show. If clicking on the same alert a second time, then the HITL prompt shows.
