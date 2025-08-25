import { useAgentStore } from "../stores/agent-store"
import { useLogStore } from "../stores/log-store"

// --- TYPE DEFINITIONS ---

export interface WebSocketMessage {
  type: string
  data?: any
  agent_name?: string
  content?: string
  timestamp: string
}

export interface ConnectionStatus {
  connected: boolean
  reconnecting: boolean
  lastConnected?: Date
  error?: string
}

// --- SIMPLIFIED WEB-SOCKET SERVICE ---

class SimpleWebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 2000
  private shouldAutoConnect = false
  private connectionStatus: ConnectionStatus = { 
    connected: false, 
    reconnecting: false
  }
  private statusCallbacks: ((status: ConnectionStatus) => void)[] = []

  constructor() {
    this.connect = this.connect.bind(this)
    this.handleMessage = this.handleMessage.bind(this)
    this.updateConnectionStatus = this.updateConnectionStatus.bind(this)
  }

  private getWebSocketUrl(): string {
    // Always use the environment variable or fallback to known working URL
    const envUrl = process.env.NEXT_PUBLIC_WEBSOCKET_URL
    if (envUrl) {
      console.log(`[WebSocket] Using environment URL: ${envUrl}`)
      return envUrl
    }
    
    const url = 'ws://localhost:8000/api/ws'
    console.log(`[WebSocket] Using default URL: ${url}`)
    return url
  }

  enableAutoConnect() {
    this.shouldAutoConnect = true
    this.connect()
  }

  connect() {
    if (typeof window === "undefined") {
      console.log("[WebSocket] Skipping connection: not in browser")
      return
    }

    if (this.ws && this.ws.readyState !== WebSocket.CLOSED) {
      console.log("[WebSocket] Already connected or connecting")
      return
    }

    const url = this.getWebSocketUrl()
    console.log(`[WebSocket] Connecting to: ${url}`)

    try {
      this.ws = new WebSocket(url)
      this.updateConnectionStatus({ connected: false, reconnecting: true })

      this.ws.onopen = () => {
        console.log("[WebSocket] Connected successfully!")
        this.reconnectAttempts = 0
        this.updateConnectionStatus({
          connected: true,
          reconnecting: false,
          lastConnected: new Date(),
          error: undefined
        })
      }

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          this.handleMessage(message)
        } catch (error) {
          console.error("[WebSocket] Failed to parse message:", error)
        }
      }

      this.ws.onclose = (event) => {
        console.log(`[WebSocket] Connection closed. Code: ${event.code}`)
        this.updateConnectionStatus({ 
          connected: false, 
          reconnecting: false,
          error: `Connection closed (${event.code})`
        })
        
        useLogStore.getState().addLog({
          agent: "System",
          level: "error",
          message: `Connection closed (Code: ${event.code})`
        })

        // Attempt reconnect if not a clean close
        if (event.code !== 1000 && this.shouldAutoConnect && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.attemptReconnect()
        }
      }

      this.ws.onerror = (event) => {
        console.error("[WebSocket] Connection error:", event)
        this.updateConnectionStatus({
          connected: false,
          reconnecting: false,
          error: "Connection failed"
        })
        
        useLogStore.getState().addLog({
          agent: "System",
          level: "error",
          message: "WebSocket connection failed"
        })
      }

    } catch (error) {
      console.error("[WebSocket] Failed to create connection:", error)
      this.updateConnectionStatus({
        connected: false,
        reconnecting: false,
        error: error instanceof Error ? error.message : "Unknown error"
      })
    }
  }

  private attemptReconnect() {
    this.reconnectAttempts++
    console.log(`[WebSocket] Reconnecting... attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts}`)
    
    this.updateConnectionStatus({ connected: false, reconnecting: true })
    
    setTimeout(() => {
      this.connect()
    }, this.reconnectDelay)
  }

  private handleMessage(message: WebSocketMessage) {
    console.log("[WebSocket] Received:", message)
    
    const { type, data, agent_name, content } = message

    // Add all messages to log store
    const agent = agent_name || (data && data.agent_name) || "System"
    const msgContent = content || (data && (data.content || data.message)) || "No message content"
    
    useLogStore.getState().addLog({ 
      agent, 
      level: type === 'error' ? 'error' : 'info', 
      message: msgContent 
    })

    // Handle specific message types
    switch (type) {
      case 'system':
        if (data?.event === 'connected') {
          console.log(`[WebSocket] Connected with client_id: ${data.client_id}`)
        }
        break
      case 'agent_response':
        // Already logged above
        break
      default:
        console.log(`[WebSocket] Received message type: ${type}`)
    }
  }

  private updateConnectionStatus(status: Partial<ConnectionStatus>) {
    this.connectionStatus = { ...this.connectionStatus, ...status }
    this.statusCallbacks.forEach((callback) => callback(this.connectionStatus))
  }

  onStatusChange(callback: (status: ConnectionStatus) => void) {
    this.statusCallbacks.push(callback)
    return () => {
      const index = this.statusCallbacks.indexOf(callback)
      if (index > -1) this.statusCallbacks.splice(index, 1)
    }
  }

  getConnectionStatus(): ConnectionStatus {
    return { ...this.connectionStatus }
  }

  private send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const fullMessage = {
        ...message,
        timestamp: new Date().toISOString(),
        session_id: "global_session"
      }
      this.ws.send(JSON.stringify(fullMessage))
      console.log("[WebSocket] Sent:", fullMessage)
    } else {
      console.warn("[WebSocket] Cannot send message: not connected")
      useLogStore.getState().addLog({
        agent: "System",
        level: "error",
        message: "Cannot send message: WebSocket not connected"
      })
    }
  }

  // Public API methods
  startProject(brief: string) {
    this.send({
      type: "user_command",
      data: {
        command: "start_project",
        brief: brief
      }
    })
  }

  testBackendConnection() {
    this.send({
      type: "user_command",
      data: {
        command: "ping"
      }
    })
  }

  testOpenAI() {
    this.send({
      type: "user_command",
      data: {
        command: "test_openai",
        message: "This is a test message to verify OpenAI integration is working properly."
      }
    })
  }

  disconnect() {
    console.log("[WebSocket] Disconnecting...")
    this.shouldAutoConnect = false
    if (this.ws) {
      this.ws.close(1000, "Manual disconnect")
    }
  }
}

export const websocketService = new SimpleWebSocketService()
