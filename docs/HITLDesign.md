use the frontend-engineer role.
use the v0-botarmy-poc project and scan to understand the project and code-base.
comply with docs/CODEPROTOCOL.md
comply with docs/STYLEGUIDE.md     .
DO NOT WRITE ANY CODE. STOP AFTER GENERATING AN HITL.md FILE

The goal: To design a seamless and efficient HITL experience within the botarmy-poc project, ensuring quick resolution of HITL moments without disrupting the user flow. We first need to decide on a pattern and then evaluate the technical options.

Context:
There are 2 HITL scenarios i can see, but add any others I may have missed.
1) while chatting with the agent directly
2) after the agent has started working and has to elevate a background task for an information/decision point. The user could be on a diffent Stage or part of the page (like Setting etc).

The 3 areas where notifications of HITL attention is need in the interface are:
1) the expanded alert in the HITL messages below the Header
2) the current task in the Artifacts Summary that requires HITL response
3) any response in the iteractive chat

The Tasks:
Understand the points of HITL within botarmy based on the above and suggest a pattern based on these questions:
- Would it make things easier if the chat with each agent could be filtered by clicking on the "Agent Status" and only seeing messages relevent to that context?
- Having a seperate chat window for each agent seems like a confusing option for the user?
- Would a standard "resolve" button in situ make sense to redirect the user back to the chat and the relevent response/message required?
- Or would it be easier to just use the "HITL" and "Waiting" status tag to jump to the right context in the chat window?  The tag could flash/glow to indicate action is required.

The pattern might be impacted by the functionality available, so
- Evaluate https://github.com/humanlayer/humanlayer and determine whether it is a suitable option for this project, and include how it would integrate into the existing chat and process.
- Use the mcp  <https://docs.copilotkit.ai/direct-to-llm/guides/generative-ui?gen-ui-type=renderAndWaitForResponse+%28HITL%> to see what the existing copilotkit offers.

Identify any differences in functionality between the two options as well as technical considerations of both. Recommend an option.

- initialise agents
- clear chat doesnt work
