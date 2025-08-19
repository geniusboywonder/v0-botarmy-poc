"use client"

import { MainLayout } from "@/components/main-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Zap, Plus, Send, RefreshCw } from "lucide-react"
import { useState, useEffect, useRef } from "react"
import { useAgentStore } from "@/lib/stores/agent-store"
import { useLogStore } from "@/lib/stores/log-store"
import { websocketService } from "@/lib/websocket/websocket-service"

export default function HomePage() {
  const [message, setMessage] = useState("")
  const { agents } = useAgentStore()
  const { logs, clearLogs } = useLogStore()
  const scrollAreaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Clear any mock/previous logs when the component mounts
    clearLogs()
    websocketService.enableAutoConnect()

    return () => {
      websocketService.disconnect()
    }
  }, [clearLogs])

  useEffect(() => {
    // Auto-scroll to the bottom when new logs are added
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTo({ top: scrollAreaRef.current.scrollHeight, behavior: 'smooth' });
    }
  }, [logs]);


  const handleSendMessage = () => {
    if (message.trim()) {
      // For now, we only have the start project command.
      // This could be extended to send other commands.
      websocketService.startProject(message)
      setMessage("")
    }
  }

  const handleStartProject = () => {
    // A default project brief for the button click
    const defaultBrief = "Create a simple Flask API that returns 'Hello, World!'."
    clearLogs() // Clear logs before starting a new project
    websocketService.startProject(defaultBrief)
  }

  return (
    <MainLayout>
      <div className="p-6">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
            <p className="text-muted-foreground">Start a new project and see your AI agents work in real-time.</p>
          </div>
          <div className="flex items-center space-x-2">
            <Button variant="outline" onClick={clearLogs}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Clear Log
            </Button>
            <Button className="bg-primary hover:bg-primary/90" onClick={handleStartProject}>
              <Zap className="w-4 h-4 mr-2" />
              Start Test Project
            </Button>
          </div>
        </div>

        <div className="space-y-6">
          {/* Chat Interface */}
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="w-5 h-5 text-primary" />
                <span>Agent Command & Log</span>
              </CardTitle>
              <CardDescription>View real-time logs from your agent workflow.</CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-96 w-full border rounded-lg p-4 mb-4" ref={scrollAreaRef}>
                <div className="space-y-4">
                  {logs.length === 0 && (
                    <div className="text-center text-muted-foreground py-12">
                      <p>No messages yet.</p>
                      <p>Click "Start Test Project" to begin.</p>
                    </div>
                  )}
                  {logs.map((log) => (
                    <div key={log.id} className="flex justify-start">
                      <div className="max-w-full lg:max-w-4/5 px-4 py-2 rounded-lg bg-muted text-foreground">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className={`text-xs font-bold ${log.level === 'error' ? 'text-red-500' : 'text-primary'}`}>{log.agent}</span>
                          <span className="text-xs opacity-70">{new Date(log.timestamp).toLocaleTimeString()}</span>
                          {log.level === 'error' && <Badge variant="destructive">Error</Badge>}
                        </div>
                        <p className="text-sm whitespace-pre-wrap">{log.message}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>

              {/* Chat Input */}
              <div className="flex space-x-2">
                <Input
                  placeholder="Enter a project brief and press Enter to start..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                  className="flex-1"
                />
                <Button onClick={handleSendMessage} size="sm">
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </MainLayout>
  )
}
