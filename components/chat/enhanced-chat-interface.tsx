"use client"

import { useState, useEffect, useRef, memo } from "react"
import { useLogStore } from "@/lib/stores/log-store"
import { useAgentStore } from "@/lib/stores/agent-store"
import { websocketService } from "@/lib/websocket/websocket-service"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TypingIndicator } from "@/components/ui/typing-indicator"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { FixedSizeList as List } from 'react-window';
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Send, Loader2, Bot, User, AlertCircle, CheckCircle, Clock } from "lucide-react"
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
];

const getMessageIcon = (log: any) => {
  if (log.agent === "User") return <User className="w-4 h-4" />
  if (log.level === "error") return <AlertCircle className="w-4 h-4 text-red-500" />
  if (log.agent === "System") return <CheckCircle className="w-4 h-4 text-green-500" />
  return <Bot className="w-4 h-4" />
}

const getMessageSeverityColor = (level: string) => {
  switch (level) {
    case 'error': return 'text-red-600 bg-red-50 border-red-200'
    case 'warn': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
    case 'info': return 'text-blue-600 bg-blue-50 border-blue-200'
    default: return 'text-gray-600 bg-gray-50 border-gray-200'
  }
}

const formatTimestamp = (timestamp: string) => {
  return new Date(timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

interface EnhancedChatInterfaceProps {
  initialMessage?: string;
}

export function EnhancedChatInterface({ initialMessage = "" }: EnhancedChatInterfaceProps) {
  const [message, setMessage] = useState(initialMessage)

  useEffect(() => {
    setMessage(initialMessage);
  }, [initialMessage]);
  const [isLoading, setIsLoading] = useState(false)
  const [placeholder, setPlaceholder] = useState(placeholders[0])
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const { logs, addLog } = useLogStore()
  const { agents } = useAgentStore()

  const isAgentThinking = agents.some(agent => agent.is_thinking)

  useEffect(() => {
    const interval = setInterval(() => {
      setPlaceholder(placeholders[Math.floor(Math.random() * placeholders.length)]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [logs])

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading || message.length < 10 || message.length > 1000) return

    const userMessage = message.trim()
    setMessage("")
    setIsLoading(true)

    // Add user message to chat
    addLog({
      id: `user-${Date.now()}`,
      agent: "User",
      level: "info",
      message: userMessage,
      timestamp: new Date().toISOString(),
      metadata: { type: 'user_input' }
    })

    // Add a loading message
    addLog({
      id: `system-${Date.now()}`,
      agent: "System",
      level: "info",
      message: "Initializing agents...",
      timestamp: new Date().toISOString(),
    });

    try {
      // Send project start command
      await websocketService.startProject(userMessage)
      
      // Add confirmation message
      addLog({
        id: `system-${Date.now()}`,
        agent: "System", 
        level: "info",
        message: "🚀 Project started! Agents are beginning work...",
        timestamp: new Date().toISOString(),
        metadata: { type: 'system_confirmation' }
      })

    } catch (error: any) {
      console.error("Failed to send message:", error)
      
      // Add error message to chat
      addLog({
        id: `error-${Date.now()}`,
        agent: "System",
        level: "error", 
        message: `❌ Failed to start project: ${error.message || 'Unknown error'}`,
        timestamp: new Date().toISOString(),
        metadata: { type: 'error', error: error.message }
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }


const Row = memo(({ index, style, data }) => {
  const { logs } = data;
  const log = logs[index];
  return (
    <div style={style} className="px-4">
      <div key={log.id || index}
           className={cn(
             "flex items-start space-x-3 p-3 rounded-lg border transition-all animate-message-in",
             getMessageSeverityColor(log.level)
           )}>

        {/* Message Icon */}
        <div className="flex-shrink-0 mt-0.5">
          {getMessageIcon(log)}
        </div>

        {/* Message Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-sm">{log.agent}</span>
              {log.level === 'error' && (
                <Badge variant="destructive" className="text-xs">Error</Badge>
              )}
              {log.metadata?.type === 'user_input' && (
                <Badge variant="outline" className="text-xs">Input</Badge>
              )}
            </div>
            <span className="text-xs opacity-70">
              {formatTimestamp(log.timestamp)}
            </span>
          </div>

          <p className="text-sm whitespace-pre-wrap leading-relaxed">
            {log.message}
          </p>
        </div>
      </div>
    </div>
  );
});

export function EnhancedChatInterface({ initialMessage = "" }: EnhancedChatInterfaceProps) {
  const [message, setMessage] = useState(initialMessage)

  useEffect(() => {
    setMessage(initialMessage);
  }, [initialMessage]);
  const [isLoading, setIsLoading] = useState(false)
  const [placeholder, setPlaceholder] = useState(placeholders[0])
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const { logs, addLog } = useLogStore()
  const { agents } = useAgentStore()

  const isAgentThinking = agents.some(agent => agent.is_thinking)

  useEffect(() => {
    const interval = setInterval(() => {
      setPlaceholder(placeholders[Math.floor(Math.random() * placeholders.length)]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [logs])

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading || message.length < 10 || message.length > 1000) return

    const userMessage = message.trim()
    setMessage("")
    setIsLoading(true)

    // Add user message to chat
    addLog({
      id: `user-${Date.now()}`,
      agent: "User",
      level: "info",
      message: userMessage,
      timestamp: new Date().toISOString(),
      metadata: { type: 'user_input' }
    })

    // Add a loading message
    addLog({
      id: `system-${Date.now()}`,
      agent: "System",
      level: "info",
      message: "Initializing agents...",
      timestamp: new Date().toISOString(),
    });

    try {
      // Send project start command
      await websocketService.startProject(userMessage)

      // Add confirmation message
      addLog({
        id: `system-${Date.now()}`,
        agent: "System",
        level: "info",
        message: "🚀 Project started! Agents are beginning work...",
        timestamp: new Date().toISOString(),
        metadata: { type: 'system_confirmation' }
      })

    } catch (error: any) {
      console.error("Failed to send message:", error)

      // Add error message to chat
      addLog({
        id: `error-${Date.now()}`,
        agent: "System",
        level: "error",
        message: `❌ Failed to start project: ${error.message || 'Unknown error'}`,
        timestamp: new Date().toISOString(),
        metadata: { type: 'error', error: error.message }
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }
    const log = logs[index];
    return (
      <div style={style} className="px-4">
        <div key={log.id || index}
             className={cn(
               "flex items-start space-x-3 p-3 rounded-lg border transition-all animate-message-in",
               getMessageSeverityColor(log.level)
             )}>

          {/* Message Icon */}
          <div className="flex-shrink-0 mt-0.5">
            {getMessageIcon(log)}
          </div>

          {/* Message Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center space-x-2">
                <span className="font-semibold text-sm">{log.agent}</span>
                {log.level === 'error' && (
                  <Badge variant="destructive" className="text-xs">Error</Badge>
                )}
                {log.metadata?.type === 'user_input' && (
                  <Badge variant="outline" className="text-xs">Input</Badge>
                )}
              </div>
              <span className="text-xs opacity-70">
                {formatTimestamp(log.timestamp)}
              </span>
            </div>

            <p className="text-sm whitespace-pre-wrap leading-relaxed">
              {log.message}
            </p>
          </div>
        </div>
      </div>
    );
  });

  return (
    <Card className="min-h-[600px] flex-1 flex flex-col">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2">
          <Bot className="w-5 h-5" />
          Agent Chat
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-0">
        {/* Chat Messages Area */}
        <div className="flex-1">
          {logs.length === 0 ? (
            <div className="text-center text-muted-foreground py-8">
              <Bot className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p className="text-lg font-medium mb-2">Welcome to BotArmy!</p>
              <p>Enter your project description below to get started.</p>
            </div>
          ) : (
            <List
              height={400} // This will need to be dynamic
              itemCount={logs.length}
              itemSize={100} // This will need to be dynamic
              width="100%"
            >
              {Row}
            </List>
          )}
          {isAgentThinking && (
            <div className="flex items-center space-x-3 p-3">
              <Bot className="w-4 h-4" />
              <TypingIndicator />
            </div>
          )}
        </div>
        
        <Separator />
        
        {/* Message Input Area */}
        <div className="p-4">
          <div className="relative">
            <Input
              placeholder={placeholder}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              className="flex-1 pr-20"
              maxLength={1000}
            />
            <div className="absolute inset-y-0 right-0 flex items-center pr-3">
              <span className="text-xs text-muted-foreground">
                {message.length} / 1000
              </span>
            </div>
          </div>
          <div className="flex justify-between items-center mt-2">
            <p className="text-xs text-muted-foreground">
              Press Enter to send • Shift+Enter for new line
            </p>
            <Button
              onClick={handleSendMessage}
              disabled={!message.trim() || isLoading || message.length < 10 || message.length > 1000}
              size="sm"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Send
                </>
              )}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}