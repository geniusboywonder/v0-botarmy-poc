"use client"

import { useState, useEffect, useRef } from "react"
import { useLogStore } from "@/lib/stores/log-store"
import { websocketService } from "@/lib/websocket/websocket-service"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
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

export function EnhancedChatInterface() {
  const [message, setMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const { logs, addLog } = useLogStore()

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [logs])

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading) return

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

  return (
    <Card className="h-[600px] flex flex-col">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2">
          <Bot className="w-5 h-5" />
          Agent Chat
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-0">
        {/* Chat Messages Area */}
        <ScrollArea className="flex-1 px-4" ref={scrollAreaRef}>
          <div className="space-y-4 py-4">
            {logs.length === 0 ? (
              <div className="text-center text-muted-foreground py-8">
                <Bot className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p className="text-lg font-medium mb-2">Welcome to BotArmy!</p>
                <p>Enter your project description below to get started.</p>
              </div>
            ) : (
              logs.map((log, index) => (
                <div key={log.id || index} 
                     className={cn(
                       "flex items-start space-x-3 p-3 rounded-lg border transition-all",
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
              ))
            )}
            
            {/* Loading indicator */}
            {isLoading && (
              <div className="flex items-center space-x-3 p-3 rounded-lg border bg-blue-50 border-blue-200">
                <Loader2 className="w-4 h-4 text-blue-500 animate-spin" />
                <div className="flex-1">
                  <span className="font-semibold text-sm text-blue-600">System</span>
                  <p className="text-sm text-blue-600">Processing your request...</p>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
        
        <Separator />
        
        {/* Message Input Area */}
        <div className="p-4">
          <div className="flex space-x-2">
            <Input
              placeholder="Describe your project (e.g., 'Create a simple todo app with React and Node.js')"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              className="flex-1"
            />
            <Button 
              onClick={handleSendMessage}
              disabled={!message.trim() || isLoading}
              size="icon"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </Button>
          </div>
          
          <p className="text-xs text-muted-foreground mt-2">
            Press Enter to send • Shift+Enter for new line
          </p>
        </div>
      </CardContent>
    </Card>
  )
}