"use client"

import { MainLayout } from "@/components/main-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Zap, Send, RefreshCw, Wifi, Brain } from "lucide-react"
import { useState, useEffect, useRef } from "react"
import { useAgentStore } from "@/lib/stores/agent-store"
import { useLogStore } from "@/lib/stores/log-store"
import { websocketService } from "@/lib/websocket/websocket-service"
import { ConnectionStatus } from "@/components/connection-status"

export default function HomePage() {
  const [message, setMessage] = useState("")
  const [isMounted, setIsMounted] = useState(false)
  const { agents } = useAgentStore()
  const { logs, clearLogs } = useLogStore()
  const scrollAreaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setIsMounted(true)
  }, [])

  useEffect(() => {
    // On mount, connect the WebSocket. It's important to only do this once.
    websocketService.enableAutoConnect()

    // On unmount, disconnect the WebSocket
    return () => {
      // On unmount, disconnect the WebSocket
      websocketService.disconnect()
    }
  }, []) // Empty dependency array ensures this runs only once on mount

  useEffect(() => {
    // Auto-scroll the chat log to the bottom when new logs are added
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTo({ top: scrollAreaRef.current.scrollHeight, behavior: 'smooth' });
    }
  }, [logs]);

  const handleSendMessage = () => {
    if (message.trim()) {
      clearLogs()
      websocketService.startProject(message)
      setMessage("")
    }
  }

  const handleStartTestProject = () => {
    const defaultBrief = "Create a simple Python Flask API that has one endpoint and returns 'Hello, World!'."
    clearLogs()
    websocketService.startProject(defaultBrief)
  }

  const handleTestBackend = () => {
    clearLogs()
    websocketService.testBackendConnection()
  }

  const handleTestOpenAI = () => {
    clearLogs()
    websocketService.testOpenAI()
  }
  
  // Helper functions to determine styling based on agent status
  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
      case "working":
      case "thinking":
        return "bg-blue-500/20 text-blue-400 border-blue-500/30"
      case "idle":
      case "completed":
        return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
      case "error":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getStatusIndicator = (status: string) => {
    switch (status) {
      case "active":
      case "working":
      case "thinking":
        return "bg-blue-400"
      case "idle":
      case "completed":
        return "bg-emerald-400"
      case "error":
        return "bg-red-400"
      default:
        return "bg-gray-400"
    }
  }

  return (
    <MainLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
            <div className="flex items-center gap-4 mt-1">
              <p className="text-muted-foreground">Start a new project and see your AI agents work in real-time.</p>
              <ConnectionStatus />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Button variant="outline" onClick={clearLogs}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Clear Log
            </Button>
            <Button variant="outline" onClick={handleTestBackend}>
              <Wifi className="w-4 h-4 mr-2" />
              Test Backend
            </Button>
            <Button variant="outline" onClick={handleTestOpenAI}>
              <Brain className="w-4 h-4 mr-2" />
              Test OpenAI
            </Button>
            <Button className="bg-primary hover:bg-primary/90" onClick={handleStartTestProject}>
              <Zap className="w-4 h-4 mr-2" />
              Start Test Project
            </Button>
          </div>
        </div>

        {/* Main Content: Chat/Log - Full Width */}
        <div className="mb-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Zap className="w-5 h-5 text-primary" />
                  <span>Agent Command & Log</span>
                </CardTitle>
                <CardDescription>View real-time logs from your agent workflow.</CardDescription>
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

        {/* Agent Status - Horizontal Grid Below Chat */}
        <Card>
          <CardHeader>
            <CardTitle>Agent Status</CardTitle>
            <CardDescription>Live status of all agents in the system.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
              {agents.map((agent) => (
                <Card key={agent.id} className="flex flex-col">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-base">{agent.name}</CardTitle>
                      <Badge variant="outline" className={`${getStatusColor(agent.status)} font-medium`}>
                        {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
                      </Badge>
                    </div>
                    <CardDescription>{agent.role}</CardDescription>
                  </CardHeader>
                  <CardContent className="flex-1 flex flex-col">
                    <div className="flex items-center space-x-2 text-sm text-muted-foreground mt-auto">
                      <div className={`w-2 h-2 rounded-full ${getStatusIndicator(agent.status)}`} />
                      <span>{agent.currentTask || agent.status}</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
