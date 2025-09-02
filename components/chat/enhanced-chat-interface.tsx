"use client"

import { useState, useEffect, useRef, memo, useMemo, useCallback } from "react"
import { useConversationStore } from "@/lib/stores/conversation-store"
import { useAgentStore } from "@/lib/stores/agent-store"
import { useChatModeStore } from "@/lib/stores/chat-mode-store"
import { websocketService } from "@/lib/websocket/websocket-service"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TypingIndicator } from "@/components/ui/typing-indicator"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import { 
  Send, 
  Loader2, 
  Bot, 
  User, 
  AlertCircle, 
  CheckCircle, 
  Clock, 
  Activity, 
  Wifi, 
  WifiOff,
  ChevronDown,
  ChevronsRightLeft,
  X,
  ClipboardCheck,
  DraftingCompass,
  Construction,
  TestTube2,
  Rocket,
  Square
} from "lucide-react"
import { cn } from "@/lib/utils"

export interface ChatMessage {
  id: string
  type: 'user' | 'agent' | 'system' | 'error'
  agent?: string
  content: string
  timestamp: Date
  metadata?: Record<string, any>
  collapsed?: boolean
}

// Multi-Corner Resizable Hook
const useMultiResizable = (initialWidth = 400, initialHeight = 400) => {
  const getInitialDimensions = () => {
    if (typeof window === 'undefined') return { width: initialWidth, height: initialHeight, x: 0, y: 0 }
    const isMobile = window.innerWidth < 768
    return { 
      width: isMobile ? 300 : initialWidth,
      height: isMobile ? 300 : initialHeight,
      x: 0,
      y: 0
    }
  }
  
  const [dimensions, setDimensions] = useState(getInitialDimensions)
  const [isResizable, setIsResizable] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  const createResizeHandler = useCallback((corner: 'nw' | 'ne' | 'sw' | 'se') => {
    return (e: React.MouseEvent) => {
      e.preventDefault()
      e.stopPropagation()
      
      const startX = e.clientX
      const startY = e.clientY
      const startWidth = dimensions.width
      const startHeight = dimensions.height
      const startPosX = dimensions.x
      const startPosY = dimensions.y

      const handleMouseMove = (moveEvent: MouseEvent) => {
        moveEvent.preventDefault()
        
        const deltaX = moveEvent.clientX - startX
        const deltaY = moveEvent.clientY - startY
        
        let newWidth = startWidth
        let newHeight = startHeight
        let newX = startPosX
        let newY = startPosY

        // Handle resizing based on corner
        if (corner === 'nw') {
          newWidth = startWidth - deltaX
          newHeight = startHeight - deltaY
          newX = startPosX + deltaX
          newY = startPosY + deltaY
        } else if (corner === 'ne') {
          newWidth = startWidth + deltaX
          newHeight = startHeight - deltaY
          newY = startPosY + deltaY
        } else if (corner === 'sw') {
          newWidth = startWidth - deltaX
          newHeight = startHeight + deltaY
          newX = startPosX + deltaX
        } else if (corner === 'se') {
          newWidth = startWidth + deltaX
          newHeight = startHeight + deltaY
        }

        // Apply constraints
        const maxWidth = Math.min(window.innerWidth - 40, 800)
        const maxHeight = Math.min(window.innerHeight - 120, 600)
        const minWidth = 300
        const minHeight = 200

        if (newWidth < minWidth) {
          if (corner.includes('w')) {
            newX = newX - (minWidth - newWidth)
          }
          newWidth = minWidth
        }
        if (newWidth > maxWidth) {
          if (corner.includes('w')) {
            newX = newX + (newWidth - maxWidth)
          }
          newWidth = maxWidth
        }

        if (newHeight < minHeight) {
          if (corner.includes('n')) {
            newY = newY - (minHeight - newHeight)
          }
          newHeight = minHeight
        }
        if (newHeight > maxHeight) {
          if (corner.includes('n')) {
            newY = newY + (newHeight - maxHeight)
          }
          newHeight = maxHeight
        }

        requestAnimationFrame(() => {
          setDimensions({ width: newWidth, height: newHeight, x: newX, y: newY })
        })
      }

      const handleMouseUp = () => {
        document.removeEventListener("mousemove", handleMouseMove)
        document.removeEventListener("mouseup", handleMouseUp)
      }

      document.addEventListener("mousemove", handleMouseMove)
      document.addEventListener("mouseup", handleMouseUp)
    }
  }, [dimensions])

  return { 
    dimensions, 
    containerRef,
    createResizeHandler,
    isResizable,
    setIsResizable
  }
}

// Role-based Icon Mapping
const getRoleIcon = (agent: string = '') => {
  const agentLower = agent.toLowerCase()
  if (agentLower.includes('analyst')) return <ClipboardCheck className="w-3 h-3" />
  if (agentLower.includes('architect')) return <DraftingCompass className="w-3 h-3" />
  if (agentLower.includes('developer')) return <Construction className="w-3 h-3" />
  if (agentLower.includes('tester')) return <TestTube2 className="w-3 h-3" />
  if (agentLower.includes('deployer')) return <Rocket className="w-3 h-3" />
  
  if (agent === 'User') return <User className="w-3 h-3" />
  if (agent === 'System') return <CheckCircle className="w-3 h-3" />
  return <Bot className="w-3 h-3" />
}

const placeholders = [
  "e.g., Create a Python script to scrape weather data from a website.",
  "e.g., Build a simple todo app with React and a Flask backend.",
  "e.g., Design a database schema for a social media platform.",
  "e.g., Write unit tests for an existing Django application.",
  "e.g., Create a REST API for managing user accounts.",
  "e.g., Build a real-time chat application with WebSockets.",
]

const getMessageIcon = (message: ChatMessage) => {
  if (message.type === "user") return <User className="w-3 h-3 text-user" />
  if (message.type === "system") return <CheckCircle className="w-3 h-3 text-system" />
  return getRoleIcon(message.agent || '') // Use role-based icon for agents
}

const getMessageSeverityColor = (type: ChatMessage['type']) => {
  if (type === "user") return 'bg-user/10 border-user/20 text-user'
  if (type === "system") return 'bg-system/10 border-system/20 text-system'
  return 'bg-secondary border-border text-foreground'
}

// Fixed: Use client-side only timestamp formatting to prevent hydration issues
const formatTimestamp = (timestamp: Date | string, mounted: boolean = true) => {
  if (!mounted) return "00:00:00" // Default during SSR
  
  try {
    const date = timestamp instanceof Date ? timestamp : new Date(timestamp)
    if (isNaN(date.getTime())) return "00:00:00" // Invalid date
    
    return date.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch {
    return "00:00:00"
  }
}

interface MessageItemProps {
  message: ChatMessage
  mounted: boolean
  onToggleCollapse?: (id: string) => void
}

const MessageItem = memo(({ message, mounted, onToggleCollapse }: MessageItemProps) => {
  // Safely handle timestamp - ensure it's always a valid Date object
  const safeTimestamp = useMemo(() => {
    try {
      if (message.timestamp instanceof Date) {
        return message.timestamp;
      }
      if (typeof message.timestamp === 'string') {
        const date = new Date(message.timestamp);
        if (!isNaN(date.getTime())) {
          return date;
        }
      }
      // Fallback to current time if timestamp is invalid
      return new Date();
    } catch (error) {
      console.warn('Invalid timestamp in message:', message.timestamp, error);
      return new Date();
    }
  }, [message.timestamp]);

  return (
    <div className="px-2 py-1">
      <div
        className={cn(
          "p-2 rounded border transition-all duration-200 hover:shadow-sm",
          getMessageSeverityColor(message.type)
        )}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 flex-1 min-w-0">
            {getMessageIcon(message)}
            <span className="font-semibold text-xs">
              {message.agent}
              {message.collapsed && message.content && (
                <span className="font-normal opacity-70">
                  : {message.content.length > 50 
                    ? `${message.content.substring(0, 50)}...` 
                    : message.content
                  }
                </span>
              )}
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-xs opacity-70">
              {formatTimestamp(safeTimestamp, mounted)}
            </span>
            {onToggleCollapse && (
              <Button 
                size="icon" 
                variant="ghost" 
                className="h-4 w-4 p-0" 
                onClick={() => onToggleCollapse(message.id)}
              >
                <ChevronDown className={cn("w-3 h-3 transition-transform", !message.collapsed && "rotate-180")} />
              </Button>
            )}
          </div>
        </div>
{!message.collapsed && (
          <div className="pt-2 pl-5 text-xs whitespace-pre-wrap leading-relaxed">
            {message.content}
          </div>
        )}
      </div>
    </div>
  )
})

MessageItem.displayName = "MessageItem"

interface EnhancedChatInterfaceProps {
  initialMessage?: string
}

export function EnhancedChatInterface({ initialMessage = "" }: EnhancedChatInterfaceProps) {
  const [message, setMessage] = useState(initialMessage)
  const [isLoading, setIsLoading] = useState(false)
  const [placeholder, setPlaceholder] = useState(placeholders[0])
  const { mode, projectContext, awaitingBrief, setAwaitingBrief, switchToProjectMode, switchToGeneralMode } = useChatModeStore();
  const [mounted, setMounted] = useState(false) // Fix hydration issues
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const { messages, addMessage, clearMessages, toggleMessageCollapse } = useConversationStore()
  const { agents } = useAgentStore()

  const handleModeSwitch = () => {
    if (mode === 'project') {
      websocketService.sendChatMessage('/chat');
      switchToGeneralMode();
    } else {
      addMessage({
        agent: "System",
        type: "system",
        content: "Please provide a detailed description of the project you want to build.",
      });
      setAwaitingBrief(true);
    }
  };

  const handleStopAgents = () => {
    websocketService.send({
      type: "user_command",
      data: {
        command: "stop_all_agents"
      }
    });
    addMessage({
      agent: "System",
      type: "system",
      content: "🛑 Stopping all agent activities...",
    });
  };
  
  // Add resizable functionality
  const { 
    dimensions, 
    containerRef,
    createResizeHandler,
    isResizable,
    setIsResizable
  } = useMultiResizable(500, 400)

  const isAgentThinking = agents.some(agent => agent.status === 'thinking' || agent.status === 'active')
  const [connectionStatus, setConnectionStatus] = useState('disconnected')

  // Clean up any corrupted messages on mount
  useEffect(() => {
    try {
      // Check if any messages have invalid timestamps and clear if so
      const hasCorruptedMessages = messages.some(msg => {
        try {
          if (msg.timestamp instanceof Date) return false;
          if (typeof msg.timestamp === 'string') {
            const date = new Date(msg.timestamp);
            return isNaN(date.getTime());
          }
          return true; // timestamp is neither Date nor valid string
        } catch {
          return true;
        }
      });

      if (hasCorruptedMessages) {
        console.warn('Found corrupted message timestamps, clearing conversation store...');
        clearMessages();
      }
    } catch (error) {
      console.error('Error checking message integrity:', error);
      clearMessages(); // Clear on any error
    }
  }, []); // Run once on mount

  // Fix hydration - only render after mount
  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    setMessage(initialMessage)
  }, [initialMessage])

  useEffect(() => {
    if (!mounted) return
    const interval = setInterval(() => {
      setPlaceholder(placeholders[Math.floor(Math.random() * placeholders.length)])
    }, 5000)
    return () => clearInterval(interval)
  }, [mounted])

  // Monitor WebSocket connection status
  useEffect(() => {
    if (!mounted) return
    
    const checkConnection = () => {
      try {
        const status = websocketService.getConnectionStatus()
        setConnectionStatus(status.connected ? 'connected' : status.reconnecting ? 'connecting' : 'disconnected')
      } catch (error) {
        setConnectionStatus('disconnected')
      }
    }

    checkConnection()
    const interval = setInterval(checkConnection, 1000)
    return () => clearInterval(interval)
  }, [mounted])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollContainer = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]')
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight
      }
    }
  }, [messages])

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading) return;
    if (connectionStatus !== 'connected') {
      addMessage({
        agent: "System",
        type: "system",
        content: "❌ Cannot send message: Not connected to server",
      });
      return;
    }

    const userMessage = message.trim();
    setMessage("");
    setIsLoading(true);

    addMessage({
      agent: "User",
      type: "user",
      content: userMessage,
    });

    try {
      if (awaitingBrief) {
        if (userMessage.length < 10 || userMessage.length > 1000) {
          addMessage({
            agent: "System",
            type: "error",
            content: "Project brief must be between 10 and 1000 characters.",
          });
          setAwaitingBrief(false); // Reset
          return;
        }

        websocketService.sendChatMessage(`start project ${userMessage}`);
        setAwaitingBrief(false);

      } else if (userMessage.toLowerCase().startsWith('start project') || userMessage.toLowerCase().startsWith('/project start')) {
        const brief = userMessage.split(' ').slice(2).join(' ');
        if (brief) {
          websocketService.sendChatMessage(userMessage);
        } else {
          addMessage({
            agent: "System",
            type: "system",
            content: "Please provide a detailed description of the project you want to build.",
          });
          setAwaitingBrief(true);
        }
      } else if (userMessage.toLowerCase() === '/chat' || userMessage.toLowerCase() === '/general') {
          websocketService.sendChatMessage(userMessage);
          switchToGeneralMode();
      } else {
        websocketService.sendChatMessage(userMessage);
      }
    } catch (error: any) {
      console.error("Failed to send message:", error);
      addMessage({
        agent: "System",
        type: "system",
        content: `❌ An error occurred: ${error.message || 'Unknown error'}`,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const getConnectionStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return <Wifi className="w-3 h-3 text-tester" />
      case 'connecting':
        return <Loader2 className="w-3 h-3 text-amber animate-spin" />
      default:
        return <WifiOff className="w-3 h-3 text-destructive" />
    }
  }

  const getConnectionStatusText = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'Connected'
      case 'connecting':
        return 'Connecting...'
      default:
        return 'Disconnected'
    }
  }

  const isInputDisabled = isLoading || connectionStatus !== 'connected'

  const canSend = useMemo(() => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage || isInputDisabled) return false;
    if (awaitingBrief) {
      return trimmedMessage.length >= 10 && trimmedMessage.length <= 1000;
    }
    return true;
  }, [message, isInputDisabled, awaitingBrief]);

  // Toggle collapse functionality for messages
  const toggleCollapse = (id: string) => {
    toggleMessageCollapse(id)
  }


  // Don't render time-dependent content until mounted
  if (!mounted) {
    return (
      <Card className="h-[240px] flex flex-col">
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <Bot className="w-4 h-4" />
              Agent Chat
            </div>
            <div className="flex items-center gap-1 text-xs font-normal">
              <WifiOff className="w-3 h-3 text-gray-500" />
              <span className="text-xs text-gray-500">Loading...</span>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col p-0">
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center text-muted-foreground">
              <Bot className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p className="text-xs">Loading chat interface...</p>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card 
      ref={containerRef}
      style={isResizable ? { 
        width: `${dimensions.width}px`,
        height: `${dimensions.height}px`,
        transform: `translate(${dimensions.x}px, ${dimensions.y}px)`,
        position: 'relative',
        zIndex: isResizable ? 10 : 'auto'
      } : {}}
      className={cn(
        "h-full flex flex-col transition-all duration-200",
        isResizable && "border-2 shadow-lg",
        mode === 'project' && "border-primary/50"
      )}
    >
      <CardHeader className="pb-2 flex-shrink-0">
        <CardTitle className="flex items-center justify-between text-lg">
          <div className="flex items-center gap-2">
            <Bot className="w-5 h-5" />
            Agent Chat
            <Button
              onClick={() => setIsResizable(!isResizable)}
              variant="ghost"
              size="sm"
              className="h-6 w-6 p-0"
              title={isResizable ? "Lock position" : "Make resizable"}
            >
              <ChevronsRightLeft className="w-3 h-3" />
            </Button>
          </div>
          <div className="flex-1 flex justify-center">
            {isAgentThinking ? (
              <div className="flex items-center space-x-2 bg-user/10 border-user/20 text-user px-3 py-1 rounded-full">
                <Bot className="w-4 h-4 animate-pulse text-user" />
                <span className="text-sm font-medium">Agents are working...</span>
                <Button 
                  onClick={handleStopAgents}
                  size="sm" 
                  variant="destructive" 
                  className="h-5 w-5 p-0 ml-2"
                  title="Stop all agents"
                >
                  <Square className="w-3 h-3" />
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Badge variant={mode === 'project' ? 'default' : 'secondary'}>
                  {mode === 'project' ? `Project: ${projectContext?.description.slice(0,20)}...` : 'General Chat'}
                </Badge>
                <Button onClick={handleModeSwitch} size="sm" variant="outline" className="h-6 px-2 text-xs">
                  <ChevronsRightLeft className="w-3 h-3 mr-1" />
                  Switch
                </Button>
              </div>
            )}
          </div>
          <div className="flex items-center gap-1 text-sm font-normal">
            {getConnectionStatusIcon()}
            <span className={cn(
              "text-sm",
              connectionStatus === 'connected' ? 'text-tester' :
              connectionStatus === 'connecting' ? 'text-amber' : 'text-destructive'
            )}>{getConnectionStatusText()}</span>
          </div>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-0">
        {/* Chat Messages Area - Fixed height scrolling container */}
        <div className={cn(
          "overflow-hidden flex-1",
          !isResizable && "h-80"
        )}>
          {messages.length === 0 ? (
            <div className="text-center text-muted-foreground py-2 px-4 h-full flex flex-col items-center justify-center">
              <Bot className="w-6 h-6 mx-auto mb-1 opacity-50" />
              <p className="text-xs font-medium mb-1">Welcome to BotArmy!</p>
              <p className="text-xs">Create New Project to Start</p>
            </div>
          ) : (
            <ScrollArea className="h-full" ref={scrollAreaRef}>
              <div className="space-y-1 p-2">
                {messages.map((message) => (
                  <MessageItem 
                    key={message.id} 
                    message={message} 
                    mounted={mounted} 
                    onToggleCollapse={toggleCollapse}
                  />
                ))}
              </div>
            </ScrollArea>
          )}
        </div>
        
        <Separator />
        
        {/* Message Input Area - Inline Button Design */}
        <div className="p-2 flex-shrink-0">
          <div className="flex items-center space-x-2">
            {/* Input Field */}
            <div className="flex-1 relative">
              <Input
                placeholder={
                  connectionStatus !== 'connected'
                    ? "Connect to server..."
                    : awaitingBrief
                    ? "Enter project brief..."
                    : mode === 'project'
                    ? `Message project: ${projectContext?.description.slice(0, 30)}...`
                    : "Type a message or 'start project'..."
                }
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isInputDisabled}
                className={cn(
                  "text-xs h-8 pr-16 ring-2 ring-teal/60 focus:ring-teal/80 border-teal/20",
                  connectionStatus !== 'connected' && "opacity-50"
                )}
                maxLength={1000}
              />
              {/* Character Counter */}
              <div className="absolute inset-y-0 right-2 flex items-center">
                <span className={cn(
                  "text-xs",
                  message.length > 900 ? "text-destructive" : 
                  message.length > 700 ? "text-amber" : "text-muted-foreground"
                )}>{message.length}</span>
              </div>
            </div>
            
            {/* Send Button - Inline */}
            <Button
              onClick={handleSendMessage}
              disabled={!canSend}
              size="sm"
              className={cn(
                "h-8 px-3 flex-shrink-0 bg-teal hover:bg-teal/90 text-white",
                !canSend && "opacity-50 cursor-not-allowed"
              )}
            >
              {isLoading ? (
                <Loader2 className="w-3 h-3 animate-spin" />
              ) : (
                <Send className="w-3 h-3 mr-1" />
              )}
              Send
            </Button>
          </div>
          
          {/* Status/Helper Text */}
          {connectionStatus !== 'connected' && (
            <div className="mt-1 p-1 bg-amber/10 border-amber/20 rounded text-xs text-amber">
              ⚠️ Waiting for server connection...
            </div>
          )}
          {awaitingBrief && message.length > 0 && message.length < 10 && (
            <div className="mt-1 text-xs text-amber">
              Minimum 10 characters required
            </div>
          )}
        </div>
      </CardContent>

      {/* Corner Resize Handles - Only shown when resizable */}
      {isResizable && (
        <>
          {/* Top-left corner */}
          <div
            onMouseDown={createResizeHandler('nw')}
            className="absolute top-0 left-0 w-4 h-4 cursor-nw-resize bg-user/30 hover:bg-user/50 border border-user transition-colors z-30"
            style={{ transform: 'translate(-2px, -2px)' }}
          >
            <div className="absolute top-0.5 left-0.5 w-2 h-2 border-l border-t border-user"></div>
          </div>
          
          {/* Top-right corner */}
          <div
            onMouseDown={createResizeHandler('ne')}
            className="absolute top-0 right-0 w-4 h-4 cursor-ne-resize bg-user/30 hover:bg-user/50 border border-user transition-colors z-30"
            style={{ transform: 'translate(2px, -2px)' }}
          >
            <div className="absolute top-0.5 right-0.5 w-2 h-2 border-r border-t border-user"></div>
          </div>
          
          {/* Bottom-left corner */}
          <div
            onMouseDown={createResizeHandler('sw')}
            className="absolute bottom-0 left-0 w-4 h-4 cursor-sw-resize bg-user/30 hover:bg-user/50 border border-user transition-colors z-30"
            style={{ transform: 'translate(-2px, 2px)' }}
          >
            <div className="absolute bottom-0.5 left-0.5 w-2 h-2 border-l border-b border-user"></div>
          </div>
          
          {/* Bottom-right corner */}
          <div
            onMouseDown={createResizeHandler('se')}
            className="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize bg-user/30 hover:bg-user/50 border border-user transition-colors z-30"
            style={{ transform: 'translate(2px, 2px)' }}
          >
            <div className="absolute bottom-0.5 right-0.5 w-2 h-2 border-r border-b border-user"></div>
            <ChevronsRightLeft className="w-2 h-2 absolute bottom-0 right-0 text-user" />
          </div>
        </>
      )}
    </Card>
  )
}
