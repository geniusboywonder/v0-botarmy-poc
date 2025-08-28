"use client"

import { useLogStore } from "@/lib/stores/log-store"
import { websocketService } from "@/lib/websocket/websocket-service"
import { MainLayout } from "@/components/main-layout"
import { Button } from "@/components/ui/button"
import { Zap } from "lucide-react"
import { useEffect } from "react"
import { ProcessSummary } from "@/components/dashboard/process-summary"
import { GlobalStatistics } from "@/components/dashboard/global-statistics"
import { EnhancedChatInterface } from "@/components/chat/enhanced-chat-interface"

export default function HomePage() {
  const { clearLogs } = useLogStore()

  useEffect(() => {
    // On mount, connect the WebSocket. It's important to only do this once.
    websocketService.enableAutoConnect()

    // On unmount, disconnect the WebSocket
    return () => {
      websocketService.disconnect()
    }
  }, []) // Empty dependency array ensures this runs only once on mount

  return (
    <MainLayout>
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
            <p className="text-muted-foreground">
              Welcome to the new process-based dashboard.
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Button className="bg-primary hover:bg-primary/90">
              <Zap className="w-4 h-4 mr-2" />
              Start New Project
            </Button>
          </div>
        </div>

        {/* Process Summary - now with smaller, uniform blocks */}
        <ProcessSummary />

        {/* Chat Interface - span full width above the fold */}
        <div className="w-full">
          <EnhancedChatInterface />
        </div>

        {/* Global Statistics below the fold */}
        <div className="mt-6">
          <GlobalStatistics />
        </div>

      </div>
    </MainLayout>
  )
}
