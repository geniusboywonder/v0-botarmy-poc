"use client"

import { useState, useEffect } from "react"
import { websocketService, type ConnectionStatus } from "../lib/websocket/websocket-service"

const defaultConnectionStatus: ConnectionStatus = {
  connected: false,
  reconnecting: false,
}

export function useWebSocket(autoConnect = true) {
  // Initialize with default status to avoid SSR issues
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>(defaultConnectionStatus)

  useEffect(() => {
    // Only access websocketService after component mounts (client-side)
    const currentStatus = websocketService.getConnectionStatus()
    setConnectionStatus(currentStatus)

    const unsubscribe = websocketService.onStatusChange(setConnectionStatus)

    if (autoConnect && !currentStatus.connected && !currentStatus.reconnecting) {
      // Check if we're in development and should use simulation instead
      if (typeof window !== "undefined" && window.location.hostname === "localhost") {
        console.log("[v0] Using simulated WebSocket connection in development")
        // Don't call connect() - let the simulation handle it
      } else {
        websocketService.connect()
      }
    }

    return () => {
      unsubscribe()
    }
  }, [autoConnect])

  const connect = (url?: string) => {
    if (typeof window !== "undefined" && window.location.hostname === "localhost") {
      console.log("[v0] Manual connection requested - enabling auto-connect")
      websocketService.enableAutoConnect()
    } else {
      websocketService.connect()
    }
  }

  const disconnect = () => websocketService.disconnect()
  
  // Create a safe send function that won't cause SSR issues
  const send = (message: any) => {
    if (typeof window !== "undefined") {
      // Add send method check here if needed
      websocketService.startProject(message)
    }
  }

  return {
    connectionStatus,
    connect,
    disconnect,
    send,
    isConnected: connectionStatus.connected,
    isReconnecting: connectionStatus.reconnecting,
  }
}
