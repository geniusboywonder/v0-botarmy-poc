"use client"

import { useAgentStore } from "@/lib/stores/agent-store"
import { useLogStore } from "@/lib/stores/log-store"
import { websocketService } from "@/lib/websocket/websocket-service"
import { EnhancedChatInterface } from "@/components/chat/enhanced-chat-interface"
import ChatErrorBoundary from "@/components/chat/chat-error-boundary"
import { demoScenarios } from "@/lib/demo-scenarios"
import { AgentStatusCard, AgentStatusCardSkeleton } from "@/components/agent-status-card"
import { PerformanceMetricsOverlay } from "@/components/performance-metrics-overlay"
import { MainLayout } from "@/components/main-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Zap, RefreshCw, Wifi, Brain } from "lucide-react"
import { useEffect } from "react"

import { useState } from "react"

export default function HomePage() {
  const { agents } = useAgentStore()
  const { clearLogs } = useLogStore()
  const [chatMessage, setChatMessage] = useState("")
  const [showMetrics, setShowMetrics] = useState(false)

  useEffect(() => {
    // On mount, connect the WebSocket. It's important to only do this once.
    websocketService.enableAutoConnect()

    // On unmount, disconnect the WebSocket
    return () => {
      // On unmount, disconnect the WebSocket
      websocketService.disconnect()
    }
  }, []) // Empty dependency array ensures this runs only once on mount

  const handleStartTestProject = (brief: string) => {
    clearLogs()
    setChatMessage(brief)
  }

  const handleTestBackend = () => {
    clearLogs()
    websocketService.testBackendConnection()
  }

  const handleTestOpenAI = () => {
    clearLogs()
    websocketService.testOpenAI()
  }

  return (
    <MainLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
            <div className="flex items-center gap-4 mt-1">
              <p className="text-muted-foreground">Start a new project and see your AI agents work in real-time.</p>
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
            <Button variant="outline" onClick={() => setShowMetrics(!showMetrics)}>
              {showMetrics ? "Hide" : "Show"} Metrics
            </Button>
            <Button className="bg-primary hover:bg-primary/90" onClick={() => handleStartTestProject(demoScenarios[0].brief)}>
              <Zap className="w-4 h-4 mr-2" />
              Start Test Project
            </Button>
          </div>
        </div>

        {showMetrics && <PerformanceMetricsOverlay />}

        {/* Agent Status - Horizontal Grid Below Chat */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Agent Status</CardTitle>
            <CardDescription>Live status of all agents in the system.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
              {agents.length > 0 ? (
                agents.map((agent) => (
                  <AgentStatusCard key={agent.id} agent={agent} />
                ))
              ) : (
                Array.from({ length: 6 }).map((_, index) => (
                  <AgentStatusCardSkeleton key={index} />
                ))
              )}
            </div>
          </CardContent>
        </Card>

        {/* Main Content: Chat/Log - Full Width */}
        <div className="mb-6">
          <ChatErrorBoundary>
            <EnhancedChatInterface initialMessage={chatMessage} />
          </ChatErrorBoundary>
        </div>

        {/*
        <div className="mb-6">
          <Card>
            <CardHeader>
              <CardTitle>Demo Scenarios</CardTitle>
              <CardDescription>
                Click a scenario to load it into the chat input.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-2">
              {demoScenarios.map((scenario) => (
                <Button
                  key={scenario.title}
                  variant="outline"
                  onClick={() => handleStartTestProject(scenario.brief)}
                >
                  {scenario.title}
                </Button>
              ))}
            </CardContent>
          </Card>
        </div>
         */}
      </div>
    </MainLayout>
  )
}
