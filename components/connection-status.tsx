"use client"

import { useWebSocket } from "../hooks/use-websocket"
import { Badge } from "./ui/badge"

export function ConnectionStatus() {
  const { connectionStatus } = useWebSocket(false) // Don't auto-connect from status component

  const getStatusColor = () => {
    if (connectionStatus.connected) return "bg-green-500"
    if (connectionStatus.reconnecting) return "bg-yellow-500"
    return "bg-red-500"
  }

  const getStatusText = () => {
    if (connectionStatus.connected) return "Connected"
    if (connectionStatus.reconnecting) return "Reconnecting..."
    return "Disconnected"
  }

  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${getStatusColor()}`} />
      <Badge variant="outline" className="text-xs">
        {getStatusText()}
      </Badge>
      {connectionStatus.lastConnected && (
        <span className="text-xs text-muted-foreground">
          Last: {connectionStatus.lastConnected.toLocaleTimeString()}
        </span>
      )}
    </div>
  )
}
