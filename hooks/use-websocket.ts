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
      console.log("[WebSocket] Auto-connecting...")
      websocketService.enableAutoConnect()
    }

    return () => {
      unsubscribe()
    }
  }, [autoConnect])

  const connect = (url?: string) => {
    console.log("[WebSocket] Manual connection requested - enabling auto-connect")
    websocketService.enableAutoConnect()
  }

  const disconnect = () => websocketService.disconnect()
  
  // Create a safe send function that won't cause SSR issues
  const send = (message: any) => {
    if (typeof window !== "undefined") {
      // Add send method check here if needed
      websocketService.startProject(message)
    }
  }

  const sendRequirementAnswers = (answers: Record<string, string>) => {
    if (typeof window !== "undefined") {
      websocketService.sendRequirementAnswers(answers)
    }
  }

  const sendApprovalResponse = (response: 'approved' | 'rejected') => {
    if (typeof window !== "undefined") {
      websocketService.sendApprovalResponse(response)
    }
  }

  return {
    connectionStatus,
    connect,
    disconnect,
    send,
    sendRequirementAnswers,
    sendApprovalResponse,
    isConnected: connectionStatus.connected,
    isReconnecting: connectionStatus.reconnecting,
  }
}
