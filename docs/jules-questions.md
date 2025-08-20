# Jules Questions

**Phase:** WebSocket Stabilization  
**Date:** August 20, 2025  

---

## ❓ Current Questions

### Question #1 - `session_id` in New Message Protocol
**Date:** 2025-08-20 06:33
**Task:** Task 3 - WebSocket Message Protocol Enhancement
**Urgency:** High

### Question:
Should the new standardized message format include a `session_id`?

### Context:
I am working on Task 3. The new message format specified in the task description does not include a `session_id` field. The existing system, however, relies heavily on `session_id` to associate messages with the correct workflow and user session (e.g., in `run_and_track_workflow` in `main.py`). Removing this field would break session tracking.

### What I've Tried:
- I have analyzed `backend/agui/protocol.py` and see that `session_id` is a key part of the existing Pydantic models and message creation functions.
- I have reviewed `backend/main.py` and confirmed that `session_id` is used to manage the `active_workflows` dictionary.

### Potential Solutions I'm Considering:
1.  **Add a top-level `session_id` field** to the new message format. This seems like the cleanest solution and aligns with the existing architecture.
2.  **Include `session_id` in the `metadata` field** of the new message format. This is a workable alternative that doesn't alter the specified top-level keys. I will proceed with this option while awaiting an answer to avoid being blocked.

### Impact if Unresolved:
I cannot correctly implement the new message protocol without knowing how to handle session tracking. My implementation will be based on an assumption that might need to be reworked.

### Status:
Answered ✅

### Answer:
**Go with Option 1 - Add `session_id` as a top-level field.**

The updated message format should be:
```json
{
    "id": "uuid",
    "type": "agent_status|agent_response|error|system|heartbeat",
    "timestamp": "ISO-8601",
    "session_id": "string",
    "agent_name": "string",
    "content": "string", 
    "metadata": {},
    "requires_ack": boolean
}
```

**Reasoning:**
1. Session tracking is critical for multi-user scenarios and workflow isolation
2. Top-level placement makes it easily accessible without parsing metadata
3. Maintains backward compatibility with existing system
4. Follows the principle of making important fields explicit rather than buried

**Additional Requirements:**
- Make `session_id` required for all message types except `heartbeat`
- Use "global_session" as default for single-user MVP scenarios
- Ensure all message creation functions include session_id parameter

**Priority:** This is the correct architectural decision. Please implement with the updated format.

---

## 🤔 Question Log

### Question Template
```markdown
## Question #X - [Brief Topic]
**Date:** YYYY-MM-DD HH:MM
**Task:** Task X - [Task Name]
**Urgency:** High/Medium/Low

### Question:
[Clear, specific question]

### Context:
[What I'm trying to accomplish and why this question came up]

### What I've Tried:
- [Research/attempts made]
- [Documentation checked]
- [Code experiments]

### Potential Solutions I'm Considering:
1. Option A: [Description and pros/cons]
2. Option B: [Description and pros/cons]

### Impact if Unresolved:
[How this affects progress/timeline]

### Status:
[Open/Answered/Resolved]

### Answer:
[Architect's response - to be filled by Neill]
```

---

## 💡 Answered Questions

*Resolved questions will be moved here for reference.*

---

## 🔍 Quick Reference

### When to Ask Questions
- **Immediately:** Architecture decisions affecting multiple components
- **After 30 minutes:** Technical blockers preventing progress
- **Before starting:** If task requirements are unclear
- **During integration:** Cross-component compatibility issues

### Architecture Contact
- **Senior Architect:** Neill
- **Response Time:** Within 2-4 hours during business hours
- **Urgent Issues:** Mark as "High" urgency

### Self-Help Resources
1. Check existing codebase for patterns
2. Review TypeScript types for expected interfaces
3. Check console/logs for error details
4. Test in isolation before integration

---

*Jules: Don't hesitate to ask questions! Better to clarify early than fix issues later.*
