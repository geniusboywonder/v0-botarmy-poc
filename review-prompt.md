you are a senior full-stack architect. 

critically perform a code review of the codebase in [@v0-botarmy-poc](file:///Users/neill/Documents/AI%20Code/Projects/v0-botarmy-poc/).

there are ongoing issues with the application: 
1) websocket disconnect issues
2) heartbeat issues
3) websocket issues to general chat
4) websocket issues with Copilotkit
5) the state of stages and artifacts not being updated
6) the HITL workflow not triggering
7) breakpoints in the code are not being triggered 

Redesign or simplfy the websockets architecture so that chat works with Copilotkit and appears in the chat window and is capable for each agent.

Ensure that back-end states are reflected correctly and imediately on changes, in the front-end.

Identify other issues that are preventing the application from running smoothly between the front and back end.

Create a FIX.md document with a detailed plan on how to fix each issue.