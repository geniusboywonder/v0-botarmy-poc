import { useAgentStore } from "../stores/agent-store"
import { useTaskStore } from "../stores/task-store"
import { useLogStore } from "../stores/log-store"

export interface WebSocketMessage {
  type: "agent_update" | "task_update" | "log_entry" | "system_status"
  data: any
  timestamp: string
}

export interface ConnectionStatus {
  connected: boolean
  reconnecting: boolean
  lastConnected?: Date
  error?: string
}

class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private connectionStatus: ConnectionStatus = { connected: false, reconnecting: false }
  private statusCallbacks: ((status: ConnectionStatus) => void)[] = []
  private shouldAutoConnect = false
  private isDevelopment = false
  private mockUpdateInterval: NodeJS.Timeout | null = null

  constructor() {
    this.updateConnectionStatus = this.updateConnectionStatus.bind(this)
    this.handleMessage = this.handleMessage.bind(this)
    this.attemptReconnect = this.attemptReconnect.bind(this)
    this.setupEventHandlers = this.setupEventHandlers.bind(this)

    if (typeof window !== "undefined") {
      this.isDevelopment = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    }
  }

  connect(url = "ws://localhost:8000/ws") {
    if (typeof window === "undefined") {
      console.log("[v0] WebSocket not available in server environment")
      return
    }

    if (this.isDevelopment) {
      console.log("[v0] Development mode detected - WebSocket creation disabled")
      if (!this.connectionStatus.connected) {
        this.simulateConnection()
      }
      return
    }

    if (!this.shouldAutoConnect) {
      console.log("[v0] Auto-connect disabled")
      return
    }

    try {
      this.ws = new WebSocket(url)
      this.setupEventHandlers()
      this.updateConnectionStatus({ connected: false, reconnecting: true })
    } catch (error) {
      console.error("[v0] WebSocket connection failed:", error)
      this.updateConnectionStatus({
        connected: false,
        reconnecting: false,
        error: error instanceof Error ? error.message : "Connection failed",
      })
    }
  }

  enableAutoConnect() {
    this.shouldAutoConnect = true
    if (!this.isDevelopment) {
      this.connect()
    } else {
      console.log("[v0] Auto-connect enabled but using simulation in development")
      this.simulateConnection()
    }
  }

  simulateConnection() {
    console.log("[v0] Simulating WebSocket connection for development")
    this.updateConnectionStatus({
      connected: true,
      reconnecting: false,
      lastConnected: new Date(),
    })

    this.startMockUpdates()
  }

  private startMockUpdates() {
    if (typeof window === "undefined" || this.mockUpdateInterval) return

    this.mockUpdateInterval = setInterval(() => {
      if (this.connectionStatus.connected) {
        const agents = useAgentStore.getState().agents
        const randomAgent = agents[Math.floor(Math.random() * agents.length)]
        if (randomAgent) {
          this.handleMessage({
            type: "agent_update",
            data: {
              id: randomAgent.id,
              status: Math.random() > 0.7 ? "busy" : randomAgent.status,
              lastActive: new Date().toISOString(),
            },
            timestamp: new Date().toISOString(),
          })
        }
      }
    }, 5000)
  }

  private setupEventHandlers() {
    if (!this.ws) return

    this.ws.onopen = () => {
      console.log("[v0] WebSocket connected")
      this.reconnectAttempts = 0
      this.updateConnectionStatus({
        connected: true,
        reconnecting: false,
        lastConnected: new Date(),
      })
    }

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data)
        this.handleMessage(message)
      } catch (error) {
        console.error("[v0] Failed to parse WebSocket message:", error)
      }
    }

    this.ws.onclose = () => {
      console.log("[v0] WebSocket disconnected")
      this.updateConnectionStatus({ connected: false, reconnecting: false })
      this.attemptReconnect()
    }

    this.ws.onerror = (error) => {
      const errorMessage = error instanceof ErrorEvent ? error.message : "Connection error"
      console.error("[v0] WebSocket error:", errorMessage)
      this.updateConnectionStatus({
        connected: false,
        reconnecting: false,
        error: errorMessage,
      })
    }
  }

  private handleMessage(message: WebSocketMessage) {
    const { type, data } = message

    switch (type) {
      case "agent_update":
        useAgentStore.getState().updateAgent(data.id, data)
        break

      case "task_update":
        useTaskStore.getState().updateTask(data.id, data)
        break

      case "log_entry":
        useLogStore.getState().addLog(data)
        break

      case "system_status":
        console.log("[v0] System status update:", data)
        break

      default:
        console.warn("[v0] Unknown message type:", type)
    }
  }

  private attemptReconnect() {
    if (this.isDevelopment) {
      console.log("[v0] Reconnection skipped - development mode")
      return
    }

    if (!this.shouldAutoConnect) {
      console.log("[v0] Reconnection skipped - auto-connect disabled")
      return
    }

    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error("[v0] Max reconnection attempts reached")
      this.updateConnectionStatus({
        connected: false,
        reconnecting: false,
        error: "Max reconnection attempts reached",
      })
      return
    }

    this.reconnectAttempts++
    this.updateConnectionStatus({ connected: false, reconnecting: true })

    setTimeout(() => {
      console.log(`[v0] Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      this.connect()
    }, this.reconnectDelay * this.reconnectAttempts)
  }

  private updateConnectionStatus(status: Partial<ConnectionStatus>) {
    this.connectionStatus = { ...this.connectionStatus, ...status }
    this.statusCallbacks.forEach((callback) => callback(this.connectionStatus))
  }

  onStatusChange(callback: (status: ConnectionStatus) => void) {
    this.statusCallbacks.push(callback)
    return () => {
      const index = this.statusCallbacks.indexOf(callback)
      if (index > -1) {
        this.statusCallbacks.splice(index, 1)
      }
    }
  }

  send(message: Omit<WebSocketMessage, "timestamp">) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const fullMessage: WebSocketMessage = {
        ...message,
        timestamp: new Date().toISOString(),
      }
      this.ws.send(JSON.stringify(fullMessage))
    } else {
      console.warn("[v0] WebSocket not connected, message not sent:", message)
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    if (this.mockUpdateInterval) {
      clearInterval(this.mockUpdateInterval)
      this.mockUpdateInterval = null
    }
    this.statusCallbacks = []
  }

  getConnectionStatus(): ConnectionStatus {
    return this.connectionStatus
  }
}

export const websocketService = new WebSocketService()

if (typeof window !== "undefined") {
  const isDev = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  if (isDev) {
    setTimeout(() => {
      websocketService.simulateConnection()
    }, 1000)
  }
}
