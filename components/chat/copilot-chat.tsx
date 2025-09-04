"use client";

import { useCopilotChat, useCopilotReadable } from "@copilotkit/react-core";
import { Role, TextMessage } from "@copilotkit/runtime-client-gql";
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
  AlertTriangle
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAgentStore } from "@/lib/stores/agent-store";
import { useChatModeStore } from "@/lib/stores/chat-mode-store";
import { useConversationStore } from "@/lib/stores/conversation-store";
import { useState, useRef, useEffect } from "react";
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
const HorizontalAgentStatus = ({ isExpanded }: { isExpanded: boolean }) => {
  const { agents } = useAgentStore();

  // Merge live agents with default agents, prioritizing live data
  const displayAgents = DEFAULT_AGENTS.map(defaultAgent => {
    const liveAgent = agents.find(agent => 
      agent.name.toLowerCase().includes(defaultAgent.role.toLowerCase()) ||
      agent.role.toLowerCase().includes(defaultAgent.role.toLowerCase())
    );
    
    return {
      name: defaultAgent.name,
      role: defaultAgent.role,
      status: liveAgent?.status || defaultAgent.status
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

  return (
    <div className="relative flex items-center justify-between gap-1 px-2" style={{height: '92px'}}>
      {displayAgents.map((agent, index) => {
        const iconColor = getAgentIconColor(agent.role);
        const statusColor = getStatusColor(agent.status);
        
        return (
          <div key={agent.name} className="flex flex-col items-center justify-center flex-1 space-y-1">
            <div className="flex items-center gap-1 justify-center">
              <div className={cn("flex-shrink-0", iconColor)}>
                {getRoleIcon(agent.name, "w-5 h-5")}
              </div>
            </div>
            <div className="text-center">
              <div className={cn("font-medium text-sm", iconColor)}>
                {agent.name}
              </div>
              <div className={cn("capitalize text-xs", statusColor)}>
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
  const isUser = message.role === Role.User;
  const agent = message.agent || (isUser ? 'User' : 'Assistant');
  const timestamp = message.timestamp || new Date();

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
const ChatInput = ({ onSend, isLoading }: { onSend: (message: string) => void; isLoading: boolean }) => {
  const [input, setInput] = useState("");
  const { mode } = useChatModeStore();
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSend(input.trim());
      setInput("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getPlaceholder = () => {
    return "Ask me anything or describe your project...";
  };

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
          onClick={handleSend} 
          disabled={!input.trim() || isLoading}
          size="sm"
          className="flex-shrink-0"
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
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

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ 
        behavior: "smooth", 
        block: "nearest" 
      });
    }
  }, [visibleMessages, isLoading]);

  const handleSendMessage = (content: string) => {
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
        <HorizontalAgentStatus isExpanded={isExpanded} />
        
        {/* Messages Area - With border matching Process Summary */}
        <div className="flex-1 min-h-0 flex flex-col overflow-hidden border rounded-lg p-2">
          <ScrollArea className={cn(
            "flex-1 h-full",
            isExpanded ? "max-h-[calc(100vh-200px)]" : "max-h-[380px]"
          )}>
            <div className="pr-4">
              {visibleMessages.length === 0 && !isLoading && (
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
              
              {visibleMessages.map((message, index) => (
                <MessageComponent 
                  key={`${message.id || index}`}
                  message={{
                    ...message,
                    timestamp: (message as any).timestamp || new Date()
                  }}
                  isExpanded={isExpanded}
                />
              ))}
              
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
      <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
    </Card>
  );
};

export default CustomCopilotChat;