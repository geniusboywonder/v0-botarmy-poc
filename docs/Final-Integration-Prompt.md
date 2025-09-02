use the backend-engineer role.
use the v0-botarmy-poc project, understand the project and code-base.

help me brainstorm and plan.

the goal is to produce a plan to be implemented by developers to polish and test the final product.
Once a user starts a project, the following flow should happen:

1) User submits prompt on what to build.
2) Analyst should ask questions to clarify requirements by asking one-shot questions in the chat.
    If any questions are not answered, clearly state assumptions and generate the Product Spec Document and make it available under the Plan Stage as a PSD.md artifact. The UI should update and show this in the Plan Stage as the document is created with relevent tasks and progress indicators.
3) Once requirements are clear, Analyst should generate the Execution Plan in the Plan tab, and the Artifacts section. The UI should populate with the scaffolding of each artifact needed for this stage. If known at this stage, other Stage artifacts could also be scaffolded and appear in this Stages in the UI.
4) On confirmation to continue by the User in the chat, the process should continue with the Plan and PSD being passed to the next Stage agent/role as context, and for them to complete their Plan for the appropriate stage and update the UI with the artifacts needed.
5) Once all the Plans are completed for each stage, the user can confirm the project may start in the chat window and the process can flow, with various agents compelting their artifacts and tasks as required.
6) The UI should update as each task, artifact and stage progresses.
7) Once complete the user should be notified that the process has completed.
8) at any stage if any of the agents needs clarification or assistance, the notifications should appear in the notification area, and appropriate messages should show in the chat window for HITL action.
9) At all times the agents must be aware of HITL and stop all tasks if asked to by the User.
10) all artifacts should be available for download in the Stage as single downloads.

Detail what changes are needed to implement this final flow in a FINALTEST.md
