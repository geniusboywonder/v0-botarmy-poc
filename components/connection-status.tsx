"use client"

import { useState, useEffect } from "react"
import { useWebSocket } from "../hooks/use-websocket"
import { Badge } from "./ui/badge"

import { Wifi, WifiOff, AlertTriangle } from "lucide-react"

export function ConnectionStatus() {
  const { connectionStatus } = useWebSocket(false) // Don't auto-connect from status component
  const [mounted, setMounted] = useState(false)
  const [lastConnectedTime, setLastConnectedTime] = useState<string>("")

  // Fix hydration issues - only show time after mounting
  useEffect(() => {
    setMounted(true)
  }, [])

  // Update last connected time only on client
  useEffect(() => {
    if (mounted && connectionStatus.lastConnected) {
      setLastConnectedTime(connectionStatus.lastConnected.toLocaleTimeString())
    }
  }, [connectionStatus.lastConnected, mounted])

  const getStatusInfo = () => {
    if (connectionStatus.connected) {
      return {
        color: "text-green-500",
        icon: <Wifi className="w-4 h-4" />,
        text: "Connected",
      }
    }
    if (connectionStatus.reconnecting) {
      return {
        color: "text-yellow-500",
        icon: <WifiOff className="w-4 h-4 animate-pulse" />,
        text: "Connecting...",
      }
    }
    if (connectionStatus.error) {
        return {
            color: "text-red-500",
            icon: <AlertTriangle className="w-4 h-4" />,
            text: "Error",
        }
    }
    return {
      color: "text-red-500",
      icon: <WifiOff className="w-4 h-4" />,
      text: "Disconnected",
    }
  }

  const { color, icon, text } = getStatusInfo()

  return (
    <div className={`flex items-center gap-2 text-xs ${color}`}>
      {icon}
      <span className="font-medium">{text}</span>
      {mounted && connectionStatus.lastConnected && lastConnectedTime && (
        <span className="text-xs text-muted-foreground">
          Last: {lastConnectedTime}
        </span>
      )}
    </div>
  )
}
