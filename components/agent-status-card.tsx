"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import type { Agent } from "@/lib/stores/agent-store"
import { TypingIndicator } from "./typing-indicator"

// Helper functions to determine styling based on agent status
// These are moved from page.tsx to be self-contained
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

interface AgentStatusCardProps {
  agent: Agent
}

export function AgentStatusCard({ agent }: AgentStatusCardProps) {
  const isActive = agent.status === 'active' || agent.status === 'working' || agent.status === 'thinking';

  return (
    <Card key={agent.id} className={cn(
      "flex flex-col p-4 transition-all duration-300",
      isActive && "ring-2 ring-blue-500 shadow-lg",
      agent.status === 'error' && "ring-2 ring-red-500 shadow-lg"
    )}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-3">
          <div className={`w-2 h-2 rounded-full ${getStatusIndicator(agent.status)}`} />
          <h3 className="font-semibold">{agent.name}</h3>
        </div>
        <Badge variant="outline" className={`${getStatusColor(agent.status)} font-medium`}>
          {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
        </Badge>
      </div>

      <div className="text-sm text-muted-foreground mb-4">{agent.role}</div>

      <div className="flex-1 flex flex-col justify-end">
        <div className="h-10 flex items-center space-x-2 text-sm text-muted-foreground">
          {isActive && agent.currentTask ? (
            <>
              <TypingIndicator />
              <span>{agent.currentTask}</span>
            </>
          ) : (
            <span>{agent.currentTask || 'Idle'}</span>
          )}
        </div>
      </div>
    </Card>
  )
}
