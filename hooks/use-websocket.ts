"use client"

import { useState, useEffect } from "react"
import { websocketService, type ConnectionStatus } from "../lib/websocket/websocket-service"

export function useWebSocket(autoConnect = true) {
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>(websocketService.getConnectionStatus())

  useEffect(() => {
    const unsubscribe = websocketService.onStatusChange(setConnectionStatus)

    if (autoConnect && !connectionStatus.connected && !connectionStatus.reconnecting) {
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
      websocketService.connect(url)
    }
  }

  const disconnect = () => websocketService.disconnect()
  const send = (message: Parameters<typeof websocketService.send>[0]) => websocketService.send(message)

  return {
    connectionStatus,
    connect,
    disconnect,
    send,
    isConnected: connectionStatus.connected,
    isReconnecting: connectionStatus.reconnecting,
  }
}
