"use client"

import { useState, useEffect, useRef, memo, useMemo } from "react"
import { useConversationStore } from "@/lib/stores/conversation-store"
import { useAgentStore } from "@/lib/stores/agent-store"
import { websocketService } from "@/lib/websocket/websocket-service"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TypingIndicator } from "@/components/ui/typing-indicator"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Send, Loader2, Bot, User, AlertCircle, CheckCircle, Clock, Activity, Wifi, WifiOff } from "lucide-react"
import { cn } from "@/lib/utils"

export interface ChatMessage {
  id: string
  type: 'user' | 'agent' | 'system' | 'error'
  agent?: string
  content: string
  timestamp: Date
  metadata?: Record<string, any>
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
  if (message.type === "user") return <User className="w-3 h-3 text-blue-600" />
  if (message.type === "system") return <CheckCircle className="w-3 h-3 text-green-500" />
  return <Bot className="w-3 h-3 text-purple-600" />
}

const getMessageSeverityColor = (type: ChatMessage['type']) => {
  if (type === "user") return 'bg-blue-50 border-blue-200 text-blue-900'
  if (type === "system") return 'bg-green-50 border-green-200 text-green-900'
  return 'bg-gray-50 border-gray-200 text-gray-900'
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
}

const MessageItem = memo(({ message, mounted }: MessageItemProps) => {
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
          "flex items-start space-x-2 p-1.5 rounded border transition-all duration-200 hover:shadow-sm",
          getMessageSeverityColor(message.type)
        )}
      >
        {/* Message Icon - Smaller */}
        <div className="flex-shrink-0 mt-0.5">
          {getMessageIcon(message)}
        </div>

        {/* Message Content - Compact */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-0.5">
            <div className="flex items-center space-x-1">
              <span className="font-semibold text-xs">{message.agent}</span>
            </div>
            <span className="text-xs opacity-70">
              {formatTimestamp(safeTimestamp, mounted)}
            </span>
          </div>

          <div className="text-xs whitespace-pre-wrap leading-relaxed">
            {message.content}
          </div>
        </div>
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
  const [mode, setMode] = useState<'chat' | 'awaiting_brief'>('chat');
  const [mounted, setMounted] = useState(false) // Fix hydration issues
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const { messages, addMessage, clearMessages } = useConversationStore()
  const { agents } = useAgentStore()

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
    if (!message.trim() || isLoading) return
    if (connectionStatus !== 'connected') {
      addMessage({
        agent: "System",
        type: "system",
        content: "❌ Cannot send message: Not connected to server",
      })
      return
    }

    const userMessage = message.trim()
    setMessage("")
    setIsLoading(true)

    addMessage({
      agent: "User",
      type: "user",
      content: userMessage,
    })

    try {
      if (mode === 'awaiting_brief') {
        if (userMessage.length < 10 || userMessage.length > 1000) {
            addMessage({
                agent: "System",
                type: "error",
                content: "Project brief must be between 10 and 1000 characters.",
            });
            setMode('chat'); // Reset mode even on error
            return;
        }
        addMessage({
            agent: "System",
            type: "system",
            content: "Initializing agents...",
        });
        websocketService.startProject(userMessage);
        setMode('chat'); // Reset after sending
      } else if (userMessage.toLowerCase() === 'start project') {
        addMessage({
            agent: "System",
            type: "system",
            content: "Please provide a detailed description of the project you want to build.",
        });
        setMode('awaiting_brief');
      } else {
        // This is a general chat message.
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
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const getConnectionStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return <Wifi className="w-3 h-3 text-green-500" />
      case 'connecting':
        return <Loader2 className="w-3 h-3 text-yellow-500 animate-spin" />
      default:
        return <WifiOff className="w-3 h-3 text-red-500" />
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
    if (mode === 'awaiting_brief') {
      return trimmedMessage.length >= 10 && trimmedMessage.length <= 1000;
    }
    return true;
  }, [message, isInputDisabled, mode]);


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
    <Card className="h-[240px] flex flex-col">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2">
            <Bot className="w-4 h-4" />
            Agent Chat
          </div>
          <div className="flex items-center gap-1 text-xs font-normal">
            {getConnectionStatusIcon()}
            <span className={cn(
              "text-xs",
              connectionStatus === 'connected' ? 'text-green-600' :
              connectionStatus === 'connecting' ? 'text-yellow-600' : 'text-red-600'
            )}>
              {getConnectionStatusText()}
            </span>
          </div>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-0 overflow-hidden">
        {/* Chat Messages Area - Fixed scrolling container */}
        <div className="flex-1 min-h-0">
          {messages.length === 0 ? (
            <div className="text-center text-muted-foreground py-2 px-4">
              <Bot className="w-6 h-6 mx-auto mb-1 opacity-50" />
              <p className="text-xs font-medium mb-1">Welcome to BotArmy!</p>
              <p className="text-xs">Create New Project to Start</p>
            </div>
          ) : (
            <ScrollArea className="h-full" ref={scrollAreaRef}>
              <div className="space-y-1">
                {messages.map((message) => (
                  <MessageItem key={message.id} message={message} mounted={mounted} />
                ))}
                {isAgentThinking && (
                  <div className="flex items-center space-x-2 p-2 mx-2">
                    <Bot className="w-3 h-3" />
                    <TypingIndicator />
                    <span className="text-xs text-muted-foreground">Agents are working...</span>
                  </div>
                )}
              </div>
            </ScrollArea>
          )}
        </div>
        
        <Separator />
        
        {/* Message Input Area - Inline Button Design */}
        <div className="p-2">
          <div className="flex items-center space-x-2">
            {/* Input Field */}
            <div className="flex-1 relative">
              <Input
                placeholder={
                  connectionStatus !== 'connected'
                    ? "Connect to server..."
                    : mode === 'awaiting_brief'
                    ? "Enter project brief..."
                    : "Type your message..."
                }
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isInputDisabled}
                className={cn(
                  "text-xs h-8 pr-16",
                  connectionStatus !== 'connected' && "opacity-50"
                )}
                maxLength={1000}
              />
              {/* Character Counter */}
              <div className="absolute inset-y-0 right-2 flex items-center">
                <span className={cn(
                  "text-xs",
                  message.length > 900 ? "text-red-500" : 
                  message.length > 700 ? "text-yellow-500" : "text-muted-foreground"
                )}>
                  {message.length}
                </span>
              </div>
            </div>
            
            {/* Send Button - Inline */}
            <Button
              onClick={handleSendMessage}
              disabled={!canSend}
              size="sm"
              className={cn(
                "h-8 px-3 flex-shrink-0",
                !canSend && "opacity-50 cursor-not-allowed"
              )}
            >
              {isLoading ? (
                <Loader2 className="w-3 h-3 animate-spin" />
              ) : (
                <Send className="w-3 h-3" />
              )}
            </Button>
          </div>
          
          {/* Status/Helper Text */}
          {connectionStatus !== 'connected' && (
            <div className="mt-1 p-1 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
              ⚠️ Waiting for server connection...
            </div>
          )}
          {mode === 'awaiting_brief' && message.length > 0 && message.length < 10 && (
            <div className="mt-1 text-xs text-yellow-600">
              Minimum 10 characters required
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
