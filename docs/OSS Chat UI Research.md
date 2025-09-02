use the backend-engineer role.
use the v0-botarmy-poc project, understand the project and code-base.

Rather than use the existing custom-built agent chat, investigate switching to an existing well established but lightweight version from opensource sources like and advise on one that offers the best fit.
It would need to be customisable to remove unwanted features (like tools, prompts, agents etc):
<https://gittodoc.com/agno-agi/agent-ui>
<https://gittodoc.com/agno-agi/agent-ui>
<https://gittodoc.com/fingerthief/minimal-chat>
<https://gittodoc.com/CopilotKit/CopilotKit>
<https://gittodoc.com/mckaywrigley/chatbot-ui>

<https://github.com/agno-agi/agent-ui>
<https://github.com/agno-agi/agent-ui>
<https://github.com/fingerthief/minimal-chat>
<https://github.com/CopilotKit/CopilotKit>
<https://github.com/mckaywrigley/chatbot-ui>

Consider any other suitable open source projects that offer a web-based agentic chat ui.

## OSS Chat UI Comparison

| **Chat UI Library** | **Pros** | **Cons** | **Integration Complexity** | **Recommendation** |
|-------------------|----------|----------|-------------------------|-------------------|
| **CopilotKit** | ✅ Purpose-built for AI agents<br/>✅ React/TypeScript native<br/>✅ Built-in WebSocket support<br/>✅ Handles streaming responses<br/>✅ Agent-aware UI components<br/>✅ Customizable themes<br/>✅ Active development | ❌ Newer project (less mature)<br/>❌ Larger bundle size<br/>❌ Opinionated architecture | **Medium** (2-3 weeks)<br/>- React component integration<br/>- WebSocket adapter needed<br/>- Agent status mapping required | **RECOMMENDED** for v0-botarmy-poc<br/>Best fit for multi-agent workflows |
| **assistant-ui** | ✅ Most popular (8.2k stars)<br/>✅ TypeScript/React focused<br/>✅ Lightweight and performant<br/>✅ Well-documented<br/>✅ Flexible theming<br/>✅ Active community | ❌ Generic chat (not agent-specific)<br/>❌ No built-in WebSocket handling<br/>❌ Requires custom agent integration | **Low-Medium** (1-2 weeks)<br/>- Drop-in React components<br/>- Custom WebSocket service<br/>- Agent status overlay needed | **STRONG ALTERNATIVE**<br/>Good balance of features/simplicity |
| **chatbot-ui** | ✅ Full-featured Next.js app<br/>✅ Multiple AI model support<br/>✅ Supabase integration<br/>✅ File upload handling<br/>✅ Conversation management<br/>✅ Production-ready | ❌ Full application (not library)<br/>❌ Supabase dependency<br/>❌ Not designed for agents<br/>❌ Would require major modifications | **High** (4-6 weeks)<br/>- Extract components from full app<br/>- Replace Supabase with current backend<br/>- Rebuild agent integration<br/>- Significant architectural changes | **NOT RECOMMENDED**<br/>Too complex for component needs |
| **agent-ui** | ✅ Specifically for AI agents<br/>✅ Modern tech stack<br/>✅ Clean, professional design<br/>✅ TypeScript support | ❌ Limited documentation<br/>❌ Small community<br/>❌ Unclear maintenance status<br/>❌ May lack advanced features | **Medium-High** (3-4 weeks)<br/>- Agent-specific but less mature<br/>- Custom integration required<br/>- Limited community support | **CAUTION**<br/>Good concept but risky choice |
| **minimal-chat** | ✅ Very lightweight<br/>✅ Simple integration<br/>✅ Multiple LLM support<br/>✅ Vue.js based (good architecture) | ❌ Vue.js (different framework)<br/>❌ Too minimal for agent features<br/>❌ No agent-specific UI<br/>❌ Would need extensive customization | **High** (4-5 weeks)<br/>- Framework conversion needed<br/>- Rebuild in React/TypeScript<br/>- Add all agent-specific features | **NOT RECOMMENDED**<br/>Framework mismatch |

## Final Recommendation: CopilotKit

**Why CopilotKit is the best choice for v0-botarmy-poc:**

1. **Purpose-Built for Agents**: Designed specifically for AI copilot/agent interfaces, unlike generic chat libraries
2. **Technical Alignment**: React/TypeScript/Next.js stack matches your current architecture perfectly
3. **WebSocket Support**: Built-in streaming and real-time communication features
4. **Agent-Aware Components**: UI components designed for multi-agent workflows
5. **Reasonable Integration Effort**: 2-3 week timeline vs 4-6 weeks for alternatives

## Implementation Strategy:

- Replace `components/chat/enhanced-chat-interface.tsx` with CopilotKit components
- Adapt WebSocket service to CopilotKit's streaming interface
- Map agent status updates to CopilotKit's UI patterns
- Maintain existing Zustand stores for conversation history
