"use client"

import { useState, useEffect, useRef } from "react"
import { useLogStore } from "@/lib/stores/log-store"
import { websocketService } from "@/lib/websocket/websocket-service"
import { useWebSocket } from "@/hooks/use-websocket"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Zap, Send } from "lucide-react"
import { ConnectionStatus } from "@/components/connection-status"

export function EnhancedChatInterface() {
  const [message, setMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isMounted, setIsMounted] = useState(false)

  const { logs, clearLogs } = useLogStore()
  const { connectionStatus } = useWebSocket(false) // Don't auto-connect from here
  const scrollAreaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setIsMounted(true)
  }, [])

  useEffect(() => {
    // Auto-scroll the chat log to the bottom when new logs are added
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTo({ top: scrollAreaRef.current.scrollHeight, behavior: 'smooth' });
    }
  }, [logs]);

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading || !connectionStatus.connected) return

    try {
      setIsLoading(true)
      clearLogs()
      websocketService.startProject(message)
      setMessage("")
    } catch (error) {
      console.error("Failed to start project:", error)
      // Optionally, use a store to show a toast notification
    } finally {
      // Add a small delay before setting loading to false to give time for backend to respond
      setTimeout(() => setIsLoading(false), 1000)
    }
  }

  const isDisabled = isLoading || !connectionStatus.connected;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
            <div className="space-y-1">
                <CardTitle className="flex items-center space-x-2">
                  <Zap className="w-5 h-5 text-primary" />
                  <span>Agent Command & Log</span>
                </CardTitle>
                <CardDescription>View real-time logs from your agent workflow.</CardDescription>
            </div>
            <ConnectionStatus />
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[40vh] w-full border rounded-lg p-4 mb-4" ref={scrollAreaRef}>
          <div className="space-y-4">
            {logs.length === 0 && (
              <div className="text-center text-muted-foreground py-12">
                <p>No messages yet.</p>
                <p>Enter a project brief below or click "Start Test Project" to begin.</p>
              </div>
            )}
            {logs.map((log) => (
              <div key={log.id} className="flex justify-start">
                <div className="max-w-full lg:max-w-4/5 px-4 py-2 rounded-lg bg-muted text-foreground">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className={`text-xs font-bold ${log.level === 'error' ? 'text-red-500' : 'text-primary'}`}>{log.agent}</span>
                    <span className="text-xs opacity-70">
                      {isMounted ? log.timestamp.toLocaleString() : 'Loading...'}
                    </span>
                    {log.level === 'error' && <Badge variant="destructive">Error</Badge>}
                  </div>
                  <p className="text-sm whitespace-pre-wrap">{log.message}</p>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>

        <div className="flex space-x-2">
          <Input
            placeholder={
              !connectionStatus.connected
                ? "Connection lost. Please wait..."
                : "Enter a project brief and press Enter to start..."
            }
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
            className="flex-1"
            disabled={isDisabled}
          />
          <Button onClick={handleSendMessage} size="sm" disabled={isDisabled}>
            {isLoading ? (
                <div className="w-4 h-4 border-2 border-background border-t-transparent rounded-full animate-spin" />
            ) : (
                <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
