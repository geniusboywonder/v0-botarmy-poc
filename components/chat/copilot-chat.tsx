
import React, { useState, useEffect, useMemo, useRef, useLayoutEffect } from 'react';
import { Bot, User, Expand } from 'lucide-react';
import { cn } from '@/lib/utils';
import { AGENT_DEFINITIONS } from '@/lib/agents/agent-definitions';
import { useAgentStore } from '@/lib/stores/agent-store';
import { useConversationStore } from '@/lib/stores/conversation-store';
import { useHITLStore } from '@/lib/stores/hitl-store';
// Local Role enum since it's not exported from lib/types
enum Role {
  User = 'User',
  Assistant = 'Assistant'
}

// Local timestamp formatting function
const formatTimestamp = (timestamp: Date | string): string => {
  const date = timestamp instanceof Date ? timestamp : new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};
import { Card, CardContent } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import ChatInput from './chat-input';
import MessageComponent from './message';
import { HITLApprovalComponent } from '../hitl/hitl-approval';

const CustomCopilotChat: React.FC = () => {
  const { agent, agentFilter, setAgentFilter } = useAgentStore();
  const { messages, addMessage, clearMessages } = useConversationStore();
  const { activeRequest, resolveRequest } = useHITLStore();

  // Safety check for store hydration issues
  if (!setAgentFilter) {
    console.warn('setAgentFilter function not available, store may not be hydrated');
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground">
        <div className="text-center">
          <div className="animate-spin w-6 h-6 border-2 border-primary border-t-transparent rounded-full mx-auto mb-2"></div>
          <p>Loading chat interface...</p>
        </div>
      </div>
    );
  }
  const [isLoading, setIsLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [forceShowHITL, setForceShowHITL] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  useLayoutEffect(() => {
    if (activeRequest && setAgentFilter) {
      setAgentFilter(activeRequest.agentName);
      setForceShowHITL(true); // Force immediate display
    } else {
      setForceShowHITL(false);
    }
  }, [activeRequest, setAgentFilter]);

  useEffect(() => {
    if (forceShowHITL && agentFilter && activeRequest && agentFilter === activeRequest.agentName) {
      const timer = setTimeout(() => {
        setForceShowHITL(false);
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [forceShowHITL, agentFilter, activeRequest]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages, isLoading]);

  const handleSendMessage = async (content: string) => {
    const userMessage = {
      role: Role.User,
      content,
      agent: 'User',
      timestamp: new Date(),
    };
    addMessage(userMessage);
    setIsLoading(true);

    // Simulate API call
    setTimeout(() => {
      const botMessage = {
        role: Role.Assistant,
        content: `This is a simulated response to "${content}"`,
        agent: agent?.name || 'Assistant',
        timestamp: new Date(),
      };
      addMessage(botMessage);
      setIsLoading(false);
    }, 1000);
  };

  const filteredMessages = useMemo(() => {
    if (!agentFilter) return messages;
    return messages.filter(
      (msg) =>
        msg.agent === agentFilter ||
        msg.agent === 'User' ||
        msg.role === Role.User
    );
  }, [messages, agentFilter]);

  const shouldShowHITL = useMemo(() => {
    if (!isClient) return false;
    if (forceShowHITL && activeRequest) return true; // Bypass timing issues
    return activeRequest && agentFilter && activeRequest.agentName === agentFilter;
  }, [activeRequest, isClient, agentFilter, forceShowHITL]);

  return (
    <Card className={cn(
      "flex flex-col transition-all duration-300",
      isExpanded 
        ? "fixed inset-4 z-50 h-auto max-h-[calc(100vh-2rem)] shadow-2xl" 
        : "h-full"
    )}>
      {/* Agent Status Bar */}
      <div className="border-b border-border p-4 bg-card/50">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Bot className="w-4 h-4" />
            <h3 className="font-semibold text-sm">BotArmy Chat</h3>
          </div>
          <div className="flex items-center gap-2">
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => clearMessages && clearMessages()}
              title="Clear all chat messages"
            >
              Clear Chat
            </Button>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => setAgentFilter && setAgentFilter('')}
              title="Clear agent filter"
            >
              Clear Filter
            </Button>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => setIsExpanded(!isExpanded)}
              title={isExpanded ? "Collapse chat" : "Expand chat"}
            >
              <Expand className={cn("w-4 h-4", isExpanded && "rotate-180")} />
            </Button>
          </div>
        </div>
        
        {/* Agent Cards Grid */}
        <div className="grid grid-cols-6 gap-3">
          {AGENT_DEFINITIONS.map((agent) => {
            const isSelected = agentFilter === agent.name;
            
            // Use semantic color classes from style guide
            const getAgentClasses = (agentName: string) => {
              switch (agentName) {
                case 'Analyst':
                  return {
                    bg: 'bg-slate-500/5 hover:bg-slate-500/10 border-slate-500/20',
                    selectedBg: 'bg-slate-500 border-slate-500',
                    text: 'text-slate-500',
                    selectedText: 'text-white'
                  };
                case 'Architect':
                  return {
                    bg: 'bg-pink-500/5 hover:bg-pink-500/10 border-pink-500/20',
                    selectedBg: 'bg-pink-500 border-pink-500',
                    text: 'text-pink-500',
                    selectedText: 'text-white'
                  };
                case 'Developer':
                  return {
                    bg: 'bg-lime-600/5 hover:bg-lime-600/10 border-lime-600/20',
                    selectedBg: 'bg-lime-600 border-lime-600',
                    text: 'text-lime-600',
                    selectedText: 'text-white'
                  };
                case 'Tester':
                  return {
                    bg: 'bg-sky-500/5 hover:bg-sky-500/10 border-sky-500/20',
                    selectedBg: 'bg-sky-500 border-sky-500',
                    text: 'text-sky-500',
                    selectedText: 'text-white'
                  };
                case 'Deployer':
                  return {
                    bg: 'bg-rose-600/5 hover:bg-rose-600/10 border-rose-600/20',
                    selectedBg: 'bg-rose-600 border-rose-600',
                    text: 'text-rose-600',
                    selectedText: 'text-white'
                  };
                case 'Project Manager':
                  return {
                    bg: 'bg-secondary hover:bg-secondary/80 border-border',
                    selectedBg: 'bg-muted-foreground border-muted-foreground',
                    text: 'text-muted-foreground',
                    selectedText: 'text-white'
                  };
                default:
                  return {
                    bg: 'bg-secondary hover:bg-secondary/80 border-border',
                    selectedBg: 'bg-muted-foreground border-muted-foreground',
                    text: 'text-muted-foreground',
                    selectedText: 'text-white'
                  };
              }
            };
            
            const classes = getAgentClasses(agent.name);
            
            return (
              <button
                key={agent.name}
                onClick={() => setAgentFilter && setAgentFilter(agentFilter === agent.name ? '' : agent.name)}
                className={cn(
                  "flex flex-col items-center p-3 rounded-lg border transition-all text-center",
                  isSelected 
                    ? `${classes.selectedBg} shadow-md` 
                    : classes.bg
                )}
              >
                <div className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center mb-2",
                  isSelected 
                    ? "bg-white/20" 
                    : "bg-background/80"
                )}>
                  <agent.icon className={cn(
                    "w-4 h-4",
                    isSelected ? classes.selectedText : classes.text
                  )} />
                </div>
                <div className={cn(
                  "text-xs font-medium",
                  isSelected ? classes.selectedText : classes.text
                )}>
                  {agent.name}
                </div>
                <div className={cn(
                  "text-xs mt-1",
                  isSelected ? "text-white/80" : "text-muted-foreground"
                )}>
                  {agent.status === 'idle' ? 'Idle' : agent.status}
                </div>
              </button>
            );
          })}
        </div>
      </div>
      
      <CardContent className="flex-grow p-0 overflow-hidden">
        <div className="flex flex-col h-full">
          <ScrollArea className="flex-grow h-0">
            <div className="p-4 space-y-4">
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
              
              {/* Active HITL Request - Show when conditions are met */}
              {shouldShowHITL && (
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

// Helper to get agent icon
const getRoleIcon = (agentName: string, role: Role) => {
  const agent = AGENT_DEFINITIONS.find(a => a.name === agentName);
  if (agent) {
    const Icon = agent.icon;
    return <Icon className="w-5 h-5" />;
  }
  return role === Role.User ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />;
};
