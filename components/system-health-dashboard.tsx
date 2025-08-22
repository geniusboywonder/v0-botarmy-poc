"use client"

import { useSystemHealth, ServiceStatus } from "@/hooks/use-system-health"
import { cn } from "@/lib/utils"
import { Wifi, Server } from "lucide-react"

const statusConfig = {
  operational: {
    text: "Operational",
    color: "text-green-500",
    bgColor: "bg-green-500/10",
  },
  degraded: {
    text: "Degraded",
    color: "text-yellow-500",
    bgColor: "bg-yellow-500/10",
  },
  outage: {
    text: "Outage",
    color: "text-red-500",
    bgColor: "bg-red-500/10",
  },
}

function StatusIndicator({ status }: { status: ServiceStatus }) {
  const { text, color, bgColor } = statusConfig[status]
  return (
    <div className={cn("flex items-center space-x-2 rounded-full px-2 py-1 text-xs", bgColor)}>
      <span className={cn("h-2 w-2 rounded-full", color.replace("text-", "bg-"))} />
      <span className={color}>{text}</span>
    </div>
  )
}

export function SystemHealthDashboard() {
  const health = useSystemHealth()

  return (
    <div className="space-y-2 text-sm">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2 text-muted-foreground">
          <Server className="h-4 w-4" />
          <span>Backend</span>
        </div>
        <StatusIndicator status={health.backend} />
      </div>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2 text-muted-foreground">
          <Wifi className="h-4 w-4" />
          <span>WebSocket</span>
        </div>
        <StatusIndicator status={health.websocket} />
      </div>
    </div>
  )
}
