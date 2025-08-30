"use client"

import { EnhancedChatInterfaceMockup } from "@/components/mockups/enhanced-chat-interface"

export default function ChatInterfacePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Enhanced Chat Interface</h1>
        <p className="text-muted-foreground">
          A detailed view of the resizable chat interface with collapsible messages and overlays.
        </p>
      </div>
      <div className="h-[600px] flex items-center justify-center">
        <div className="w-full max-w-2xl">
          <EnhancedChatInterfaceMockup />
        </div>
      </div>
    </div>
  )
}
