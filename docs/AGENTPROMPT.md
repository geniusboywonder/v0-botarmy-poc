# Instructions for AI Agent

- **Always follow** the **Code Protocol** in `docs/CODEPROTOCOL.md`.  
- Use the **README** to understand project context and structure.  
- Use `https://github.com/geniusboywonder/v0-botarmy-poc` as the code base, working on the local main branch.  
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

**[goal]**  Optimsie the BotArmy application and amke sure the front and back end work seamlessly.

---  
  
`[specific_tasks_placeholder]`
Fix the following issues:

1) when sending a message in the chat window results in this error:
System
15:09:12
❌ An error occurred: _lib_websocket_websocket_service__WEBPACK_IMPORTED_MODULE_4__.websocketService.sendChatMessage is not a function

2) you need to clear the chat window messages on each restart and include a button to do so on the Dashboard page. The message need to stay inside the chat window (and scroll). currently they are pushing out of the chat window and pushing the rest of the features down the page.

3) Finally, since you seem to still be struggling to size the Agent Chat on the Dashboard. Make it the same dimensions as the Process Summary box. In that box you need to fit the chat window (containing a minimum of 2 messages) and the text line and submit button (put the button at the end of the text line instead of under neath it). If you have to redesign and reduce the layout of the messages and the borders/padding to make this happen then do so.
