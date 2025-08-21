"use client"

import { MainLayout } from "@/components/main-layout"
import { EnhancedChatInterface } from "@/components/chat/enhanced-chat-interface"
import { useWebSocket } from "@/hooks/use-websocket"
import { websocketService } from "@/lib/websocket/websocket-service"
import { Button } from "@/components/ui/button"
import { useLogStore } from "@/lib/stores/log-store"

export default function LogsPage() {
  // Use the hook to manage WebSocket connection
  useWebSocket(true) // auto-connect

  const { clearLogs } = useLogStore()

  const handleTestBackend = () => {
    websocketService.testBackendConnection()
  }

  const handleTestOpenAI = () => {
    websocketService.testOpenAI()
  }

  return (
    <MainLayout>
      <div className="p-6 flex flex-col gap-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Logs</h1>
            <p className="text-muted-foreground">
              Real-time agent activity and system events
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button onClick={handleTestBackend} variant="outline" size="sm">
              Test Backend
            </Button>
            <Button onClick={handleTestOpenAI} variant="outline" size="sm">
              Test OpenAI
            </Button>
            <Button onClick={clearLogs} variant="destructive" size="sm">
              Clear Logs
            </Button>
          </div>
        </div>

        {/* Enhanced Chat Interface */}
        <div className="flex-1">
          <EnhancedChatInterface />
        </div>
      </div>
    </MainLayout>
  )
}
