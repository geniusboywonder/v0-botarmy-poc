# Human-in-the-Loop (HITL) Design for BotArmy

## Executive Summary

This document presents the design for a seamless Human-in-the-Loop (HITL) experience within the BotArmy POC project. The solution combines **CopilotKit's renderAndWaitForResponse** with **intelligent notification routing** to provide quick resolution of HITL moments without disrupting user flow.

## Current Architecture Analysis

### Existing Components
- **CopilotChat**: Main chat interface with agent status display
- **Agent Store**: Manages agent states, progress tracking, and status updates
- **Notification Store**: Handles alerts with priority levels and stage tracking
- **Enhanced Process Summary**: Visual workflow with stage indicators
- **WebSocket Service**: Real-time communication for agent updates

### HITL Touchpoints Identified

1. **Primary Chat Interface** (`components/chat/copilot-chat.tsx`)
2. **Agent Status Cards** (integrated in CopilotChat)
3. **Process Summary Stages** (`components/mockups/enhanced-process-summary.tsx`)
4. **Alert System** (header notification area)
5. **Artifact Summary Tasks** (tasks requiring HITL response)

## HITL Scenarios Analysis

### Scenario 1: Direct Agent Chat HITL
**Context**: User actively chatting with agent
**Trigger**: Agent requests approval/decision during conversation
**Experience**: Inline approval interface appears in chat

### Scenario 2: Background Task Elevation
**Context**: Agent working in background needs human decision
**User State**: Could be on different page/section
**Experience**: Multi-channel notification with intelligent routing

### Scenario 3: Cross-Agent Coordination
**Context**: Multiple agents need human arbitration
**Experience**: Consolidated decision interface with context from all agents

## Recommended HITL Pattern

### Core Design Philosophy: **Contextual Proximity with Smart Routing**

1. **In-Chat HITL**: Use CopilotKit's `renderAndWaitForResponse` for active conversations
2. **Background HITL**: Smart notification system with one-click resolution
3. **Status Badge Navigation**: Clickable "HITL" badges that route to relevant context
4. **Unified Resolution Interface**: Single chat window handles all HITL interactions

### Key Pattern Decisions

#### ✅ **Recommended**: Single Chat Window with Context Filtering
- **Why**: Maintains conversation continuity and provides full context
- **How**: Agent status badges filter chat to show only relevant agent messages
- **UX**: Click agent status → filter chat → see HITL request → resolve in-place

#### ❌ **Not Recommended**: Separate Chat Windows per Agent
- **Why**: Creates cognitive overhead and context switching friction
- **Problem**: User loses conversation flow and has to manage multiple interfaces

#### ✅ **Recommended**: In-Situ Resolve Buttons with Chat Navigation
- **Why**: Provides immediate action but routes to full context when needed
- **How**: "Resolve" button in notification → jumps to filtered chat view → shows full context

## Technical Approach Comparison

### Option A: CopilotKit renderAndWaitForResponse ⭐ **RECOMMENDED**

#### Strengths
- **Native Integration**: Already integrated into BotArmy via existing CopilotChat
- **Proven Pattern**: Well-tested HITL implementation with TypeScript support
- **Rich UI Components**: Built-in support for forms, buttons, and complex interactions
- **State Management**: Handles approval state automatically
- **Real-time Updates**: Seamless integration with existing WebSocket architecture

#### Architecture Integration
```typescript
// Existing CopilotChat can be enhanced with HITL actions
useCopilotAction({
  name: "requireHumanApproval",
  renderAndWaitForResponse: ({ respond, args, status }) => {
    if (status === "complete") {
      return <div>✅ Approved</div>;
    }
    
    return (
      <HITLApprovalComponent
        agentName={args.agentName}
        decision={args.decision}
        context={args.context}
        onApprove={() => respond?.("APPROVE")}
        onReject={() => respond?.("REJECT")}
        onModify={(feedback) => respond?.(feedback)}
      />
    );
  }
});
```

#### Implementation Complexity: **Low**
- Leverages existing CopilotKit infrastructure
- Minimal additional dependencies
- TypeScript support out of the box

### Option B: HumanLayer Integration

#### Strengths
- **Specialized HITL Platform**: Purpose-built for human-in-the-loop workflows
- **Multi-Channel Support**: Slack, email, and custom channel notifications
- **Advanced Approval Flows**: Complex approval chains and role-based access
- **External Integration**: Can notify users outside the application

#### Architecture Integration Challenges
```python
# Requires significant backend integration
from humanlayer import HumanLayer

hl = HumanLayer(
    contact_channel=ContactChannel(
        slack=SlackContactChannel(channel_or_user_id="C123456")
    )
)

@hl.require_approval()
def agent_action(params):
    # Agent action that requires approval
    pass
```

#### Implementation Complexity: **High**
- Requires new backend service integration
- Additional infrastructure for approval management
- Complex state synchronization between HumanLayer and existing stores
- Need to build UI components for approval display

## Recommended Implementation Strategy

### Phase 1: Enhanced CopilotKit HITL (Immediate Implementation)

#### 1. HITL Action Components
```typescript
// /components/hitl/hitl-approval.tsx
interface HITLApprovalProps {
  agentName: string;
  decision: string;
  context: any;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  onApprove: () => void;
  onReject: () => void;
  onModify: (feedback: string) => void;
}

export const HITLApprovalComponent: React.FC<HITLApprovalProps> = ({
  agentName,
  decision,
  context,
  priority,
  onApprove,
  onReject,
  onModify
}) => {
  return (
    <div className="border-l-4 border-amber-500 bg-amber-50 p-4 rounded-lg">
      <div className="flex items-center justify-between mb-3">
        <Badge variant="outline" className="bg-amber-100 text-amber-800">
          🤖 {agentName} Needs Approval
        </Badge>
        <Badge variant={priority === 'urgent' ? 'destructive' : 'secondary'}>
          {priority.toUpperCase()}
        </Badge>
      </div>
      
      <div className="mb-4">
        <h4 className="font-semibold mb-2">Decision Required:</h4>
        <p className="text-sm">{decision}</p>
        {context && (
          <details className="mt-2">
            <summary className="cursor-pointer text-sm text-muted-foreground">
              View Context
            </summary>
            <pre className="text-xs bg-muted p-2 rounded mt-2">
              {JSON.stringify(context, null, 2)}
            </pre>
          </details>
        )}
      </div>
      
      <div className="flex gap-2">
        <Button onClick={onApprove} className="bg-green-600 hover:bg-green-700">
          ✓ Approve
        </Button>
        <Button onClick={onReject} variant="destructive">
          ✗ Reject
        </Button>
        <HITLModifyDialog onModify={onModify} />
      </div>
    </div>
  );
};
```

#### 2. Enhanced Notification System
```typescript
// /lib/stores/hitl-store.ts
interface HITLRequest {
  id: string;
  agentName: string;
  decision: string;
  context: any;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  timestamp: Date;
  status: 'pending' | 'approved' | 'rejected' | 'modified';
  response?: string;
}

interface HITLStore {
  requests: HITLRequest[];
  activeRequest: HITLRequest | null;
  
  addRequest: (request: Omit<HITLRequest, 'id' | 'timestamp' | 'status'>) => void;
  resolveRequest: (id: string, status: 'approved' | 'rejected' | 'modified', response?: string) => void;
  getRequestsByAgent: (agentName: string) => HITLRequest[];
  getPendingCount: () => number;
  
  // Navigation helpers
  navigateToRequest: (id: string) => void;
  filterChatByAgent: (agentName: string) => void;
}
```

#### 3. Smart Badge Navigation
```typescript
// Enhanced Agent Status Card with HITL routing
const AgentStatusCard = ({ agent }: { agent: Agent }) => {
  const { getRequestsByAgent, navigateToRequest } = useHITLStore();
  const pendingRequests = getRequestsByAgent(agent.name);
  const hasPendingHITL = pendingRequests.length > 0;

  const handleStatusClick = () => {
    if (hasPendingHITL) {
      // Route to chat with agent filter applied
      navigateToRequest(pendingRequests[0].id);
    }
  };

  return (
    <Card className="cursor-pointer" onClick={handleStatusClick}>
      <div className="flex items-center justify-between">
        <span>{agent.name}</span>
        {hasPendingHITL ? (
          <Badge 
            variant="destructive" 
            className="animate-pulse cursor-pointer"
            title="Click to resolve HITL request"
          >
            HITL ({pendingRequests.length})
          </Badge>
        ) : (
          <Badge variant="secondary">{agent.status}</Badge>
        )}
      </div>
    </Card>
  );
};
```

#### 4. Header Alert Integration
```typescript
// Enhanced header alerts with HITL routing
const HITLAlerts = () => {
  const { requests } = useHITLStore();
  const { navigateToRequest } = useHITLStore();
  const pendingRequests = requests.filter(r => r.status === 'pending');

  return (
    <div className="flex items-center gap-2">
      {pendingRequests.slice(0, 2).map((request) => (
        <Alert 
          key={request.id}
          className="bg-amber-50 border-amber-200 cursor-pointer hover:bg-amber-100"
          onClick={() => navigateToRequest(request.id)}
        >
          <AlertTriangle className="h-4 w-4 text-amber-600" />
          <AlertDescription className="text-amber-800">
            {request.agentName} needs approval
            <ChevronRight className="h-3 w-3 ml-1 inline" />
          </AlertDescription>
        </Alert>
      ))}
      
      {pendingRequests.length > 2 && (
        <Badge variant="outline" className="cursor-pointer">
          +{pendingRequests.length - 2} more
        </Badge>
      )}
    </div>
  );
};
```

### Phase 2: Advanced Features

#### 1. Kill Switch/Pause Controls
```typescript
// /components/controls/kill-switch.tsx
const KillSwitchControls = ({ agentName }: { agentName: string }) => {
  const { pauseAgent, resumeAgent, resetAgent } = useAgentStore();
  
  return (
    <div className="flex items-center gap-2">
      <Button
        variant="outline"
        size="sm"
        onClick={() => pauseAgent(agentName)}
        title="Pause agent execution"
      >
        <Pause className="w-3 h-3" />
        Pause
      </Button>
      
      <Button
        variant="destructive"
        size="sm"
        onClick={() => resetAgent(agentName)}
        title="Stop and reset agent"
      >
        <Square className="w-3 h-3" />
        Stop
      </Button>
    </div>
  );
};
```

#### 2. Context-Aware Chat Filtering
```typescript
// Enhanced CopilotChat with agent filtering
const CopilotChatWithHITL = () => {
  const [agentFilter, setAgentFilter] = useState<string | null>(null);
  const { activeRequest } = useHITLStore();

  // Auto-filter when HITL request is active
  useEffect(() => {
    if (activeRequest) {
      setAgentFilter(activeRequest.agentName);
    }
  }, [activeRequest]);

  // Filter messages by agent when filter is active
  const filteredMessages = useMemo(() => {
    if (!agentFilter) return visibleMessages;
    return visibleMessages.filter(msg => 
      msg.agent?.toLowerCase().includes(agentFilter.toLowerCase())
    );
  }, [visibleMessages, agentFilter]);

  return (
    <div className="flex flex-col h-full">
      {agentFilter && (
        <div className="bg-blue-50 border-b border-blue-200 p-2 flex items-center justify-between">
          <span className="text-sm text-blue-800">
            Showing messages from: <strong>{agentFilter}</strong>
          </span>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setAgentFilter(null)}
          >
            Show All <X className="w-3 h-3 ml-1" />
          </Button>
        </div>
      )}
      
      {/* Enhanced CopilotChat with HITL actions */}
      <CopilotChatComponent 
        messages={filteredMessages}
        hitlActions={getHITLActionsForAgent(agentFilter)}
      />
    </div>
  );
};
```

## User Experience Flows

### Flow 1: Direct Chat HITL
```
User chatting with Agent
↓
Agent requests approval via renderAndWaitForResponse
↓
HITL component renders inline in chat
↓
User sees context, approves/rejects/modifies
↓
Agent receives response and continues
```

### Flow 2: Background Task HITL
```
Agent working in background
↓
Agent needs human input
↓
HITL request added to store
↓
Header alert appears + Agent status badge glows
↓
User clicks badge or alert
↓
Chat auto-filters to show agent context
↓
User sees HITL request and resolves
↓
Agent receives response and continues
```

### Flow 3: Cross-Navigation HITL
```
User on different page (Settings, Logs, etc.)
↓
Agent needs approval
↓
Header alert notification appears
↓
User clicks "Resolve" in notification
↓
Redirected to main dashboard
↓
Chat auto-filtered to relevant agent
↓
HITL interface displayed
↓
User resolves and can return to previous page
```

## Implementation Priority

### Phase 1 (Week 1): Core HITL Infrastructure
1. ✅ **HITLStore**: Zustand store for managing HITL requests
2. ✅ **HITL Components**: Approval UI components with CopilotKit integration
3. ✅ **Badge Navigation**: Clickable status badges with HITL routing
4. ✅ **Enhanced Chat**: Agent filtering and HITL action rendering

### Phase 2 (Week 2): User Experience Polish
1. ✅ **Header Alerts**: Smart notification system with routing
2. ✅ **Kill Switch**: Pause/resume/stop controls for agents
3. ✅ **Context Display**: Rich context visualization for decisions
4. ✅ **Response History**: Track and display HITL decision history

### Phase 3 (Week 3): Advanced Features
1. 🔄 **Multi-Agent HITL**: Coordinated decisions across multiple agents
2. 🔄 **Approval Workflows**: Complex multi-step approval processes
3. 🔄 **External Notifications**: Optional integration with external channels
4. 🔄 **Analytics**: HITL performance metrics and insights

## Technical Considerations

### Performance
- **Lightweight State**: HITL store only holds active/recent requests
- **Efficient Filtering**: Chat filtering uses React.useMemo for performance
- **WebSocket Optimization**: HITL events use existing WebSocket infrastructure

### Accessibility
- **Keyboard Navigation**: All HITL components support keyboard interaction
- **Screen Readers**: ARIA labels and semantic markup for approval interfaces
- **Color Blind Support**: Status indicators use icons + text, not just colors

### Error Handling
- **Timeout Handling**: HITL requests auto-expire after configured timeout
- **Offline Support**: Graceful degradation when WebSocket disconnected
- **State Recovery**: HITL store persisted to handle page refreshes

### Security
- **Context Sanitization**: All context data sanitized before display
- **Action Validation**: Server-side validation of HITL responses
- **Audit Trail**: All HITL decisions logged with timestamps and user info

## Conclusion

The recommended approach leverages **CopilotKit's renderAndWaitForResponse** as the core HITL mechanism, enhanced with intelligent notification routing and context-aware navigation. This provides:

1. **Seamless Integration**: Builds on existing CopilotKit infrastructure
2. **Minimal Disruption**: Users can resolve HITL requests without losing context
3. **Smart Routing**: Notifications intelligently guide users to relevant context
4. **Unified Experience**: Single chat interface handles all HITL interactions
5. **Extensible Design**: Architecture supports future advanced features

The solution balances **simplicity of implementation** with **sophistication of user experience**, ensuring rapid deployment while maintaining the flexibility to evolve into more complex workflows as BotArmy matures.

---

**Next Steps**: Begin implementation of Phase 1 components, starting with the HITLStore and basic approval components, then integrate with existing CopilotChat infrastructure.
