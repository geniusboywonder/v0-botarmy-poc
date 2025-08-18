import { useAgentStore } from "../stores/agent-store"
import { useTaskStore } from "../stores/task-store"
import { useLogStore } from "../stores/log-store"

export interface WebSocketMessage {
  type:
    | "agent_update"
    | "task_update"
    | "log_entry"
    | "system_status"
    | "agent_message"
    | "agent_thinking"
    | "workflow_progress"
  data: any
  timestamp: string
}

export interface ConnectionStatus {
  connected: boolean
  reconnecting: boolean
  lastConnected?: Date
  error?: string
}

function isDevelopmentEnvironment(): boolean {
  if (typeof window === "undefined") return true // Server-side, assume dev

  const hostname = window.location.hostname
  const isDev =
    hostname === "localhost" ||
    hostname === "127.0.0.1" ||
    hostname.includes("vercel.app") ||
    hostname.includes("v0.app") ||
    hostname.includes("preview") ||
    process.env.NODE_ENV === "development"

  console.log(`[v0] Environment check: ${isDev ? "DEVELOPMENT" : "PRODUCTION"} (hostname: ${hostname})`)
  return isDev
}

class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private connectionStatus: ConnectionStatus = { connected: false, reconnecting: false }
  private statusCallbacks: ((status: ConnectionStatus) => void)[] = []
  private shouldAutoConnect = false
  private isDevelopment = true // Always default to true for safety
  private mockUpdateInterval: NodeJS.Timeout | null = null

  constructor() {
    this.updateConnectionStatus = this.updateConnectionStatus.bind(this)
    this.handleMessage = this.handleMessage.bind(this)
    this.attemptReconnect = this.attemptReconnect.bind(this)
    this.setupEventHandlers = this.setupEventHandlers.bind(this)

    this.isDevelopment = isDevelopmentEnvironment()
    console.log(`[v0] WebSocketService initialized in ${this.isDevelopment ? "DEVELOPMENT" : "PRODUCTION"} mode`)
  }

  connect(url = "ws://localhost:8000/ws/agui") {
    console.log(`[v0] Connect called - isDevelopment: ${this.isDevelopment}`)

    if (typeof window === "undefined") {
      console.log("[v0] WebSocket not available in server environment")
      return
    }

    if (this.isDevelopment || isDevelopmentEnvironment()) {
      console.log("[v0] DEVELOPMENT MODE: WebSocket creation completely blocked")
      if (!this.connectionStatus.connected) {
        this.simulateConnection()
      }
      return
    }

    const hostname = window.location.hostname
    if (
      hostname === "localhost" ||
      hostname === "127.0.0.1" ||
      hostname.includes("vercel") ||
      hostname.includes("v0.app")
    ) {
      console.log("[v0] SAFETY CHECK: Blocking WebSocket creation on development hostname:", hostname)
      this.simulateConnection()
      return
    }

    if (!this.shouldAutoConnect) {
      console.log("[v0] Auto-connect disabled")
      return
    }

    try {
      console.log("[v0] PRODUCTION MODE: Creating WebSocket connection to:", url)
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
    console.log(`[v0] EnableAutoConnect called - isDevelopment: ${this.isDevelopment}`)
    this.shouldAutoConnect = true

    if (this.isDevelopment || isDevelopmentEnvironment()) {
      console.log("[v0] DEVELOPMENT MODE: Using simulation instead of real WebSocket")
      this.simulateConnection()
    } else {
      console.log("[v0] PRODUCTION MODE: Attempting real WebSocket connection")
      this.connect()
    }
  }

  simulateConnection() {
    console.log("[v0] Starting WebSocket simulation for development")

    this.updateConnectionStatus({
      connected: true,
      reconnecting: false,
      lastConnected: new Date(),
      error: undefined,
    })

    this.startMockUpdates()
  }

  private startMockUpdates() {
    if (typeof window === "undefined" || this.mockUpdateInterval) return

    console.log("[v0] Starting mock data updates every 10 seconds")
    this.mockUpdateInterval = setInterval(() => {
      if (this.connectionStatus.connected) {
        const agents = useAgentStore.getState().agents
        const randomAgent = agents[Math.floor(Math.random() * agents.length)]
        if (randomAgent) {
          const mockStatuses = ["active", "idle", "busy"]
          const randomStatus = mockStatuses[Math.floor(Math.random() * mockStatuses.length)]

          this.handleMessage({
            type: "agent_update",
            data: {
              agent: randomAgent.name,
              status: randomStatus,
              timestamp: new Date().toISOString(),
              current_task: randomStatus === "active" ? "Processing mock task" : undefined,
              progress: randomStatus === "active" ? Math.floor(Math.random() * 100) : undefined,
            },
            timestamp: new Date().toISOString(),
          })
        }
      }
    }, 10000)
  }

  private setupEventHandlers() {
    if (!this.ws) return

    this.ws.onopen = () => {
      console.log("[v0] WebSocket connected to BotArmy backend")
      this.reconnectAttempts = 0
      this.updateConnectionStatus({
        connected: true,
        reconnecting: false,
        lastConnected: new Date(),
      })

      this.send({
        type: "system_status",
        data: { command: "get_agent_status" },
      })
    }

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
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

  private handleMessage(message: any) {
    const { type, data, agent_name, content } = message

    switch (type) {
      case "agent_update":
        if (data?.agent && data?.status) {
          useAgentStore.getState().updateAgentByName(data.agent, {
            status: data.status,
            lastActivity: new Date(),
            currentTask: data.current_task,
            progress: data.progress,
          })
        }
        break

      case "agent_status_update":
        if (agent_name) {
          useAgentStore.getState().updateAgentByName(agent_name, {
            status: data?.state || "idle",
            lastActivity: new Date(),
            currentTask: data?.current_task,
            progress: data?.progress,
          })
        }
        break

      case "agent_message":
        if (agent_name && content) {
          useLogStore.getState().addLog({
            id: `msg_${Date.now()}`,
            timestamp: message.timestamp,
            level: "info",
            agent: agent_name,
            message: content,
            status: "completed",
          })
        }
        break

      case "agent_thinking":
        if (agent_name && data?.thought) {
          useLogStore.getState().addLog({
            id: `thinking_${Date.now()}`,
            timestamp: message.timestamp,
            level: "debug",
            agent: agent_name,
            message: `Thinking: ${data.thought}`,
            status: "in-progress",
          })
        }
        break

      case "workflow_progress":
        if (data?.workflow_id && data?.phase) {
          useTaskStore.getState().updateTask(data.workflow_id, {
            status: data.phase === "completed" ? "completed" : "in-progress",
            progress: data.progress || 0,
            phase: data.phase,
          })
        }
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

      case "connection_ack":
        console.log("[v0] Connection acknowledged:", data?.message)
        break

      case "heartbeat":
        console.log("[v0] Heartbeat received")
        break

      default:
        console.warn("[v0] Unknown message type:", type)
    }
  }

  private attemptReconnect() {
    if (this.isDevelopment || isDevelopmentEnvironment()) {
      console.log("[v0] Reconnection skipped - development mode uses simulation only")
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

  send(message: any) {
    if (this.isDevelopment || isDevelopmentEnvironment()) {
      console.log("[v0] Mock send (development mode):", message.type)
      return
    }

    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const fullMessage = {
        ...message,
        timestamp: new Date().toISOString(),
      }
      this.ws.send(JSON.stringify(fullMessage))
    } else {
      console.warn("[v0] WebSocket not connected, message not sent:", message)
    }
  }

  sendChatMessage(content: string, targetAgent?: string) {
    if (this.isDevelopment || isDevelopmentEnvironment()) {
      console.log(`[v0] Mock chat message to ${targetAgent || "any agent"}: ${content}`)
    }

    this.send({
      type: "user_message",
      content,
      target_agent: targetAgent,
      timestamp: new Date().toISOString(),
    })
  }

  startProject(description: string, requirements: any = {}) {
    if (this.isDevelopment || isDevelopmentEnvironment()) {
      console.log(`[v0] Mock project start: ${description}`)
    }

    this.send({
      type: "user_command",
      data: {
        command: "start_project",
        description,
        requirements,
      },
    })
  }

  requestAgentStatus() {
    this.send({
      type: "user_command",
      data: {
        command: "get_agent_status",
      },
    })
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
  if (isDevelopmentEnvironment()) {
    console.log("[v0] Development environment detected - starting simulation only")
    setTimeout(() => {
      websocketService.simulateConnection()
    }, 1000)
  } else {
    console.log("[v0] Production environment detected - WebSocket will be available")
  }
}
