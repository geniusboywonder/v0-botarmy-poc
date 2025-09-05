"use client";

import { useCopilotChat, useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";
import { Role, TextMessage } from "@copilotkit/runtime-client-gql";
import { HITLApprovalComponent } from '../hitl/hitl-approval';
import {
  Bot,
  User,
  CheckCircle,
  ClipboardCheck,
  DraftingCompass,
  Construction,
  TestTube2,
  Rocket,
  Activity,
  Trash2,
  Send,
  Maximize2,
  Minimize2,
  Loader2,
  Circle,
  AlertTriangle,
  X,
  Square
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAgentStore } from "@/lib/stores/agent-store";
import { useChatModeStore } from "@/lib/stores/chat-mode-store";
import { useConversationStore } from "@/lib/stores/conversation-store";
import { useHITLStore } from "@/lib/stores/hitl-store";
import { KillSwitchControls } from '../controls/kill-switch';
import { useState, useRef, useEffect, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Input } from "@/components/ui/input";

interface CustomCopilotMessage {
  id: string;
  role: Role;
  content: string;
  agent?: string;
  timestamp?: Date;
}

// Default agents to always show (the 6 standard BotArmy agents)
const DEFAULT_AGENTS = [
  { name: "Analyst", role: "analyst", status: "idle" },
  { name: "Architect", role: "architect", status: "idle" },
  { name: "Developer", role: "developer", status: "idle" },
  { name: "Tester", role: "tester", status: "idle" },
  { name: "Deployer", role: "deployer", status: "idle" },
  { name: "Project Manager", role: "manager", status: "idle" }
];

// Role-based Icon Mapping
const getRoleIcon = (agent: string = '', role: Role = Role.Assistant) => {
  if (role === Role.User) return <User className="w-4 h-4" />;
  
  const agentLower = agent.toLowerCase();
  if (agentLower.includes('analyst')) return <ClipboardCheck className="w-4 h-4" />;
  if (agentLower.includes('architect')) return <DraftingCompass className="w-4 h-4" />;
  if (agentLower.includes('developer')) return <Construction className="w-4 h-4" />;
  if (agentLower.includes('tester')) return <TestTube2 className="w-4 h-4" />;
  if (agentLower.includes('deployer')) return <Rocket className="w-4 h-4" />;
  if (agentLower.includes('manager') || agentLower.includes('project')) return <Activity className="w-4 h-4" />;
  if (agent === 'System') return <CheckCircle className="w-4 h-4" />;
  return <Bot className="w-4 h-4" />;
};

// Format timestamp
const formatTimestamp = (date: Date) => {
  return date.toLocaleTimeString('en-US', { 
    hour12: false, 
    hour: '2-digit', 
    minute: '2-digit'
  });
};

// Agent Status Component - text-only format matching Process Summary dimensions
const HorizontalAgentStatus = ({ isExpanded, isClient = false, agentFilter, onAgentFilterChange }: { isExpanded: boolean; isClient?: boolean; agentFilter: string | null; onAgentFilterChange: (agent: string | null) => void }) => {
  const { agents } = useAgentStore();
  const { getRequestsByAgent, navigateToRequest } = useHITLStore();

  // Merge live agents with default agents, prioritizing live data
  const displayAgents = DEFAULT_AGENTS.map(defaultAgent => {
    const liveAgent = agents.find(agent => 
      agent.name.toLowerCase().includes(defaultAgent.role.toLowerCase()) ||
      agent.role.toLowerCase().includes(defaultAgent.role.toLowerCase())
    );
    
    const pendingRequests = isClient ? getRequestsByAgent(defaultAgent.name) : [];
    const hasPendingHITL = isClient && pendingRequests.length > 0;

    return {
      name: defaultAgent.name,
      role: defaultAgent.role,
      status: liveAgent?.status || defaultAgent.status,
      hasPendingHITL,
      pendingRequests,
    };
  });

  // Get agent icon color based on role
  const getAgentIconColor = (role: string) => {
    const roleLower = role.toLowerCase();
    if (roleLower.includes('analyst')) return 'text-slate-500';
    if (roleLower.includes('architect')) return 'text-pink-500';
    if (roleLower.includes('developer')) return 'text-lime-600';
    if (roleLower.includes('tester')) return 'text-sky-500';
    if (roleLower.includes('deployer')) return 'text-rose-600';
    if (roleLower.includes('manager')) return 'text-muted-foreground';
    return 'text-muted-foreground';
  };

  // Get status color - different from name/icon color
  const getStatusColor = (status: string) => {
    const statusLower = status.toLowerCase();
    if (['working', 'active', 'busy'].includes(statusLower)) return 'text-green-400';
    if (['waiting', 'pending'].includes(statusLower)) return 'text-yellow-400';
    if (['error', 'failed'].includes(statusLower)) return 'text-red-400';
    return 'text-muted-foreground/60';
  };

  const handleStatusClick = (agent: any) => {
    // Toggle agent filter - clicking the same agent again removes filter
    if (agentFilter === agent.name) {
      onAgentFilterChange(null);
    } else {
      onAgentFilterChange(agent.name);
      
      // If this agent has a pending HITL request, make it the active request
      const agentHITLRequests = getRequestsByAgent(agent.name);
      if (agentHITLRequests.length > 0) {
        // Find the first pending request for this agent
        const pendingRequest = agentHITLRequests.find(req => req.status === 'pending');
        if (pendingRequest) {
          navigateToRequest(pendingRequest.id);
        }
      }
    }
  };

  return (
    <div className="relative flex items-center justify-between gap-1 px-2" style={{height: '92px'}}>
      {displayAgents.map((agent, index) => {
        const iconColor = getAgentIconColor(agent.role);
        const statusColor = getStatusColor(agent.status);
        
        const isActive = agentFilter === agent.name;
        
        return (
          <div key={agent.name} 
            className={cn(
              "flex flex-col items-center justify-center flex-1 space-y-1 cursor-pointer p-2 rounded-lg transition-all",
              isActive 
                ? "bg-teal ring-2 ring-teal/60 text-white" 
                : "hover:bg-secondary"
            )} 
            onClick={() => handleStatusClick(agent)}
          >
            <div className="flex items-center gap-1 justify-center">
              <div className={cn("flex-shrink-0", isActive ? "text-white" : iconColor)}>
                {getRoleIcon(agent.name, "w-5 h-5")}
              </div>
            </div>
            <div className="text-center">
              <div className={cn("font-medium text-sm", isActive ? "text-white" : iconColor)}>
                {agent.name}
              </div>
              <div className={cn("capitalize text-xs", isActive ? "text-white/80" : statusColor)}>
                {agent.status}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// Chat Mode Toggle Component - REMOVED (AI determines mode automatically)

// Message Component - User on left, AI on right, responsive width
const MessageComponent = ({ message, isLoading, isExpanded }: { message: any; isLoading?: boolean; isExpanded?: boolean }) => {
  const { resolveRequest } = useHITLStore();
  const isUser = message.role === Role.User;
  const agent = message.agent || (isUser ? 'User' : 'Assistant');
  const timestamp = message.timestamp || new Date();
  const isHITL = (message as any).isHITL;
  const hitlData = (message as any).hitlData;

  const handleHITLApprove = () => {
    if (hitlData?.requestId) {
      resolveRequest(hitlData.requestId, 'approved', 'Approved from chat');
    }
  };

  const handleHITLReject = () => {
    if (hitlData?.requestId) {
      resolveRequest(hitlData.requestId, 'rejected', 'Rejected from chat');
    }
  };

  const handleHITLModify = (feedback: string) => {
    if (hitlData?.requestId) {
      resolveRequest(hitlData.requestId, 'modified', feedback);
    }
  };

  return (
    <div className={cn(
      "mb-4", // Consistent spacing between ALL messages
      isExpanded ? "px-8" : "px-4" // More padding in expanded view
    )}>
      <div className={cn(
        "p-4 rounded-lg border", // Consistent padding from chat border
        isExpanded ? "max-w-[95%]" : "max-w-[80%]", // Wider messages in expanded view
        isUser 
          ? "bg-primary/10 border-primary/20 mr-auto" // User messages on LEFT
          : isHITL 
            ? "bg-amber-50 border-amber-200 ml-auto" // HITL messages have amber background
            : "bg-muted/30 border-border ml-auto" // AI messages on RIGHT
      )}>
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 mt-1">
            {getRoleIcon(agent, message.role)}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-2">
              <div className="font-semibold text-sm">
                {agent}
              </div>
              <div className="text-xs text-muted-foreground">
                {formatTimestamp(timestamp)}
              </div>
            </div>
            <div className="text-sm text-foreground/90 prose prose-sm max-w-none">
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="text-muted-foreground">Thinking...</span>
                </div>
              ) : isHITL && hitlData ? (
                <div className="space-y-3">
                  <div>{message.content}</div>
                  <HITLApprovalComponent
                    agentName={hitlData.agentName}
                    decision={hitlData.decision}
                    context={hitlData.context}
                    priority={hitlData.priority}
                    onApprove={handleHITLApprove}
                    onReject={handleHITLReject}
                    onModify={handleHITLModify}
                    minimal={true}
                  />
                </div>
              ) : (
                message.content
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Input Component with fixed positioning
const ChatInput = ({ onSend, isLoading, hasActiveHITL = false }: { onSend: (message: string) => void; isLoading: boolean; hasActiveHITL?: boolean }) => {
  const [input, setInput] = useState("");
  const { mode } = useChatModeStore();
  const { agents, resetAgent } = useAgentStore();
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSend(input.trim());
      setInput("");
    }
  };

  const handleStop = () => {
    // Stop all active agents
    agents.forEach(agent => {
      if (agent.status === 'working' || agent.status === 'busy' || agent.status === 'active') {
        resetAgent(agent.name);
      }
    });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getPlaceholder = () => {
    if (hasActiveHITL) {
      return "Type 'accept', 'reject', or 'modify: your feedback' to respond to HITL request...";
    }
    return "Ask me anything or describe your project...";
  };

  const hasActiveAgents = agents.some(agent => 
    agent.status === 'working' || agent.status === 'busy' || agent.status === 'active'
  );

  return (
    <div className="flex-shrink-0 p-4 bg-card">
      <div className="flex gap-2">
        <Input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={getPlaceholder()}
          disabled={isLoading}
          className="flex-1"
        />
        <Button 
          onClick={isLoading || hasActiveAgents ? handleStop : handleSend} 
          disabled={!isLoading && !hasActiveAgents && !input.trim()}
          size="sm"
          className="flex-shrink-0"
          variant={isLoading || hasActiveAgents ? "destructive" : "default"}
          title={isLoading || hasActiveAgents ? "Stop current task" : "Send message"}
        >
          {isLoading || hasActiveAgents ? (
            <Square className="w-4 h-4" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </Button>
      </div>
    </div>
  );
};

// Simple Resize Hook
const useSimpleResize = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  return {
    isExpanded,
    toggleExpanded: () => setIsExpanded(!isExpanded)
  };
};

// Main Component - INTEGRATED (not floating)
const CustomCopilotChat = () => {
  const { agents } = useAgentStore();
  const { mode } = useChatModeStore();
  const { clearMessages } = useConversationStore();
  const { isExpanded, toggleExpanded } = useSimpleResize();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [agentFilter, setAgentFilter] = useState<string | null>(null);
  const [isClient, setIsClient] = useState(false);
  const { activeRequest, resolveRequest } = useHITLStore();

  const {
    visibleMessages,
    appendMessage,
    isLoading,
  } = useCopilotChat();

  // Provide readable context to CopilotKit
  useCopilotReadable({
    description: "The current status of all AI agents in the system.",
    value: agents,
  });

  useCopilotReadable({
    description: "The current chat mode (general or project).",
    value: mode,
  });

  useCopilotAction({
    name: "requireHumanApproval",
    description: "Request human approval for a decision.",
    parameters: [
      { name: "agentName", type: "string", description: "The name of the agent requesting approval." },
      { name: "decision", type: "string", description: "The decision that requires approval." },
      { name: "context", type: "object", description: "Additional context for the decision." },
      { name: "priority", type: "string", description: "The priority of the request." },
    ],
    render: (props) => {
      const { agentName, decision, context, priority } = props.args;
      return (
        <HITLApprovalComponent
          agentName={agentName}
          decision={decision}
          context={context}
          priority={priority as any}
          onApprove={() => props.notify("APPROVE")}
          onReject={() => props.notify("REJECT")}
          onModify={(feedback) => props.notify(feedback)}
        />
      );
    },
    handler: async (args) => {
      // This handler is not used when `render` is defined,
      // but it's good practice to have a fallback.
      console.log("Human approval requested:", args);
    },
  });

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ 
        behavior: "smooth", 
        block: "nearest" 
      });
    }
  }, [visibleMessages, isLoading]);

  // Auto-filter when HITL request is active, but don't override manual selection
  useEffect(() => {
    if (activeRequest && !agentFilter) {
      // Only auto-set if no manual filter is currently active
      setAgentFilter(activeRequest.agentName);
    }
  }, [activeRequest]); // Removed agentFilter from dependency to prevent interference

  // Fix hydration mismatch by only showing HITL data on client
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Filter messages by agent when filter is active
  const filteredMessages = useMemo(() => {
    if (!agentFilter) return visibleMessages;
    return visibleMessages.filter(msg =>
      (msg as any).agent?.toLowerCase().includes(agentFilter.toLowerCase())
    );
  }, [visibleMessages, agentFilter]);

  const handleSendMessage = (content: string) => {
    // Check for HITL commands when there's an active request
    if (activeRequest) {
      const command = content.toLowerCase().trim();
      
      if (command === 'accept' || command === 'approve') {
        resolveRequest(activeRequest.id, 'approved', 'Approved via chat command');
        return; // Don't send as regular message
      }
      
      if (command === 'reject' || command === 'deny') {
        resolveRequest(activeRequest.id, 'rejected', 'Rejected via chat command');
        return; // Don't send as regular message
      }
      
      if (command.startsWith('modify ') || command.startsWith('modify:')) {
        const feedback = content.substring(7).trim(); // Remove "modify " prefix
        if (feedback) {
          resolveRequest(activeRequest.id, 'modified', feedback);
          return; // Don't send as regular message
        }
      }
    }

    // Regular message handling
    const message = new TextMessage({ 
      content, 
      role: Role.User,
    });
    // Add timestamp to message
    (message as any).timestamp = new Date();
    appendMessage(message);
  };

  const handleClearChat = () => {
    clearMessages();
  };

  return (
    <Card className={cn(
      "h-full flex flex-col shadow-sm",
      isExpanded && "fixed inset-4 z-50 shadow-2xl",
      mode === 'project' && "border-primary/30"
    )}>
      <CardHeader className="pb-3 flex-shrink-0">
        <CardTitle className="flex items-center justify-between text-lg">
          <div className="flex items-center gap-2">
            <Bot className="w-5 h-5" />
            BotArmy Chat
          </div>
          <div className="flex items-center gap-2">
            <Button
              onClick={handleClearChat}
              variant="outline"
              size="sm"
              className="h-7 text-xs"
              title="Clear chat history"
            >
              <Trash2 className="w-3 h-3 mr-1" />
              Clear
            </Button>
            <Button
              onClick={toggleExpanded}
              variant="ghost"
              size="sm"
              className="h-7 w-7 p-0"
              title={isExpanded ? "Minimize chat" : "Expand chat"}
            >
              {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            </Button>
          </div>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-4 min-h-0 overflow-hidden space-y-2">
        {/* Agent Status Section - mirrors Process Summary styling */}
        <HorizontalAgentStatus 
          isExpanded={isExpanded} 
          isClient={isClient} 
          agentFilter={agentFilter}
          onAgentFilterChange={setAgentFilter}
        />
        
        {/* Messages Area - With border matching Process Summary */}
        <div className="flex-1 min-h-0 flex flex-col overflow-hidden border rounded-lg p-2">
          <ScrollArea className={cn(
            "flex-1 h-full",
            isExpanded ? "max-h-[calc(100vh-200px)]" : "max-h-[380px]"
          )}>
            <div className="pr-4">
              {filteredMessages.length === 0 && !isLoading && (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <Bot className="w-12 h-12 text-muted-foreground mb-4" />
                  <h3 className="text-lg font-medium mb-2">
                    Hello! I'm your BotArmy assistant.
                  </h3>
                  <p className="text-muted-foreground text-sm">
                    How can I help you today? Describe your project or ask me anything!
                  </p>
                </div>
              )}
              
              {filteredMessages.map((message, index) => (
                <MessageComponent 
                  key={`${message.id || index}`}
                  message={{
                    ...message,
                    timestamp: (message as any).timestamp || new Date()
                  }}
                  isExpanded={isExpanded}
                />
              ))}
              
              {/* Active HITL Request - Show inline only if it matches current agent filter */}
              {activeRequest && isClient && (!agentFilter || activeRequest.agentName === agentFilter) && (
                <div className={cn(
                  "mb-4",
                  isExpanded ? "px-8" : "px-4"
                )}>
                  <div className="p-4 rounded-lg border bg-amber-50 border-amber-200 ml-auto max-w-[95%]">
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 mt-1">
                        {getRoleIcon(activeRequest.agentName, Role.Assistant)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-2">
                          <div className="font-semibold text-sm">
                            {activeRequest.agentName}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            {formatTimestamp(new Date(activeRequest.timestamp))}
                          </div>
                        </div>
                        <div className="text-sm text-foreground/90 prose prose-sm max-w-none">
                          <div className="space-y-3">
                            <div>🤖 {activeRequest.agentName} is requesting human approval</div>
                            <HITLApprovalComponent
                              agentName={activeRequest.agentName}
                              decision={activeRequest.decision}
                              context={activeRequest.context}
                              priority={activeRequest.priority}
                              onApprove={() => {
                                resolveRequest(activeRequest.id, 'approved', 'Approved from chat');
                              }}
                              onReject={() => {
                                resolveRequest(activeRequest.id, 'rejected', 'Rejected from chat');
                              }}
                              onModify={(feedback) => {
                                resolveRequest(activeRequest.id, 'modified', feedback);
                              }}
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {isLoading && (
                <MessageComponent 
                  message={{ 
                    role: Role.Assistant, 
                    content: '', 
                    agent: 'Assistant',
                    timestamp: new Date()
                  }}
                  isLoading={true}
                  isExpanded={isExpanded}
                />
              )}
              
              <div ref={messagesEndRef} className="h-1" />
            </div>
          </ScrollArea>
        </div>
      </CardContent>

      {/* Input Area - Fixed at bottom */}
      <ChatInput onSend={handleSendMessage} isLoading={isLoading} hasActiveHITL={!!activeRequest} />
    </Card>
  );
};

export default CustomCopilotChat;