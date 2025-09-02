"use client"

import { useConversationStore } from "@/lib/stores/conversation-store"
import { MainLayout } from "@/components/main-layout"
import { Button } from "@/components/ui/button"
import { Zap, Trash2 } from "lucide-react"
import { EnhancedProcessSummaryMockup } from "@/components/mockups/enhanced-process-summary"
import { EnhancedChatInterface } from "@/components/chat/enhanced-chat-interface"
import { RecentActivities } from "@/components/mockups/recent-activities"

export default function HomePage() {
  const { clearMessages } = useConversationStore()

  return (
    <MainLayout>
      <div className="p-6 space-y-8">
        {/* Page Header */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-foreground">BotArmy Agentic Builder</h1>
              <p className="text-lg text-muted-foreground">
                An workflow overview with process tracking, agent communication, and activity monitoring.
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                onClick={clearMessages}
                variant="outline"
                size="sm"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Clear Chat
              </Button>
              <Button className="bg-primary hover:bg-primary/90">
                <Zap className="w-4 h-4 mr-2" />
                Start New Project
              </Button>
            </div>
          </div>
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid gap-8 grid-cols-1 xl:grid-cols-2">
          {/* Process Summary */}
          <div className="min-h-[500px]">
            <EnhancedProcessSummaryMockup />
          </div>
          
          {/* Agent Chat Interface */}
          <div className="min-h-[500px]">
            <EnhancedChatInterface />
          </div>
        </div>

        {/* Recent Activities Section */}
        <div className="space-y-4">
          <div className="border-t border-border pt-8">
            <h2 className="text-xl font-semibold text-foreground mb-4">Activity Timeline</h2>
            <RecentActivities />
          </div>
        </div>
      </div>
    </MainLayout>
  )
}
