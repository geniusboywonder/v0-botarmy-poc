import { useAgentStore } from "../stores/agent-store"
import { useLogStore } from "../stores/log-store"
import { useConversationStore } from "../stores/conversation-store"
import { useProcessStore } from "../stores/process-store"

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

// Enhanced error information interface
interface WebSocketErrorInfo {
  message: string
  code?: number
  reason?: string
  type: 'connection' | 'protocol' | 'network' | 'timeout' | 'unknown'
}

// --- ENHANCED WEB-SOCKET SERVICE WITH BETTER ERROR HANDLING ---

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
  private heartbeatInterval: NodeJS.Timeout | null = null
  private reconnectTimeout: NodeJS.Timeout | null = null
  private isManualDisconnect = false
  private connectionTimeoutId: NodeJS.Timeout | null = null
  private lastPongReceived: Date | null = null
  private pingsSentWithoutPong = 0
  private maxPingsWithoutPong = 3

  constructor() {
    this.connect = this.connect.bind(this)
    this.handleMessage = this.handleMessage.bind(this)
    this.updateConnectionStatus = this.updateConnectionStatus.bind(this)
    this.startHeartbeat = this.startHeartbeat.bind(this)
    this.stopHeartbeat = this.stopHeartbeat.bind(this)
    
    // Handle page visibility changes to manage connections efficiently
    if (typeof window !== "undefined") {
      document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this))
      window.addEventListener('beforeunload', this.disconnect.bind(this))
      
      // Handle network status changes
      window.addEventListener('online', this.handleNetworkOnline.bind(this))
      window.addEventListener('offline', this.handleNetworkOffline.bind(this))
    }
  }

  private handleVisibilityChange() {
    if (document.visibilityState === 'visible') {
      console.log("[WebSocket] Page became visible, ensuring connection...")
      if (this.shouldAutoConnect && !this.connectionStatus.connected && !this.connectionStatus.reconnecting) {
        this.connect()
      }
    } else {
      console.log("[WebSocket] Page became hidden, maintaining connection with reduced activity...")
      // Keep connection alive but reduce heartbeat frequency when hidden
    }
  }

  private handleNetworkOnline() {
    console.log("[WebSocket] Network came online, ensuring connection...")
    if (this.shouldAutoConnect && !this.connectionStatus.connected) {
      this.reconnectAttempts = 0 // Reset attempts when network comes back
      this.connect()
    }
  }

  private handleNetworkOffline() {
    console.log("[WebSocket] Network went offline")
    this.updateConnectionStatus({ 
      connected: false, 
      reconnecting: false,
      error: "Network connection lost"
    })
  }

  private getWebSocketUrl(): string {
    // Always use the environment variable or fallback to known working URL
    const envUrl = process.env.NEXT_PUBLIC_WEBSOCKET_URL
    if (envUrl) {
      console.log(`[WebSocket] Using environment URL: ${envUrl}`)
      return envUrl
    }
    
    // Use the correct FastAPI WebSocket endpoint from backend/main.py
    const url = 'ws://localhost:8000/api/ws'
    console.log(`[WebSocket] Using default URL: ${url}`)
    return url
  }

  enableAutoConnect() {
    this.shouldAutoConnect = true
    this.isManualDisconnect = false
    this.connect()
  }

  private startHeartbeat() {
    this.stopHeartbeat() // Clear any existing heartbeat
    
    // Send ping every 30 seconds to keep connection alive
    this.heartbeatInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        try {
          this.ws.send(JSON.stringify({
            type: "ping",
            timestamp: new Date().toISOString()
          }))
          
          this.pingsSentWithoutPong++
          console.log(`[WebSocket] Heartbeat ping sent (${this.pingsSentWithoutPong}/${this.maxPingsWithoutPong})`)
          
          // Check if we've sent too many pings without response
          if (this.pingsSentWithoutPong >= this.maxPingsWithoutPong) {
            console.warn("[WebSocket] Too many pings sent without pong response, connection may be stale")
            this.handleStaleConnection()
          }
          
        } catch (error) {
          console.warn("[WebSocket] Failed to send heartbeat ping:", this.getErrorMessage(error))
          this.handleConnectionError(error, 'heartbeat')
        }
      } else if (this.ws && this.ws.readyState !== WebSocket.OPEN) {
        console.log(`[WebSocket] Connection not open (state: ${this.getReadyStateString()}), stopping heartbeat`)
        this.stopHeartbeat()
      }
    }, 30000) // 30 seconds
  }

  private handleStaleConnection() {
    console.log("[WebSocket] Detected stale connection, forcing reconnect...")
    this.disconnect()
    if (this.shouldAutoConnect) {
      setTimeout(() => this.connect(), 1000)
    }
  }

  private stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval)
      this.heartbeatInterval = null
    }
    this.pingsSentWithoutPong = 0
  }

  private getReadyStateString(): string {
    if (!this.ws) return 'null'
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING: return 'CONNECTING'
      case WebSocket.OPEN: return 'OPEN'
      case WebSocket.CLOSING: return 'CLOSING'
      case WebSocket.CLOSED: return 'CLOSED'
      default: return 'UNKNOWN'
    }
  }

  // Enhanced error message extraction
  private getErrorMessage(error: any): string {
    if (!error) return 'Unknown error occurred'
    
    if (typeof error === 'string') return error
    
    if (error instanceof Error) return error.message
    
    if (typeof error === 'object') {
      // Handle various error object structures
      if (error.message) return error.message
      if (error.reason) return error.reason
      if (error.code) return `Error code: ${error.code}`
      if (error.type) return `Error type: ${error.type}`
      
      // If it's an object with properties, try to extract meaningful info
      const keys = Object.keys(error)
      if (keys.length === 0) return 'Empty error object - connection issue'
      
      return `Error object: ${keys.join(', ')}`
    }
    
    return 'Unrecognized error format'
  }

  // Enhanced error classification
  private classifyError(error: any, context?: string): WebSocketErrorInfo {
    const message = this.getErrorMessage(error)
    
    // Network-related errors
    if (message.includes('Failed to establish') || message.includes('connection refused') || message.includes('ECONNREFUSED')) {
      return {
        message: 'Backend server is not responding. Please ensure the server is running on port 8000.',
        type: 'network',
        code: error?.code
      }
    }
    
    // Timeout errors
    if (message.includes('timeout') || context === 'timeout') {
      return {
        message: 'Connection timeout. The server may be overloaded or unreachable.',
        type: 'timeout'
      }
    }
    
    // Protocol errors
    if (message.includes('protocol') || message.includes('handshake')) {
      return {
        message: 'WebSocket protocol error. There may be a version mismatch.',
        type: 'protocol'
      }
    }
    
    // Connection errors
    if (context === 'connection' || message.includes('connection')) {
      return {
        message: 'Connection error. The network connection may be unstable.',
        type: 'connection'
      }
    }
    
    // Empty or undefined errors
    if (!error || (typeof error === 'object' && Object.keys(error).length === 0)) {
      return {
        message: 'Connection interrupted unexpectedly. This may be due to network instability.',
        type: 'connection'
      }
    }
    
    return {
      message: message || 'An unknown error occurred',
      type: 'unknown'
    }
  }

  private handleConnectionError(error: any, context?: string) {
    const errorInfo = this.classifyError(error, context)
    
    this.updateConnectionStatus({
      connected: false,
      reconnecting: false,
      error: errorInfo.message
    })

    // Only log error if we're not already in an error state to avoid spam
    if (this.connectionStatus.connected || this.connectionStatus.reconnecting) {
      useLogStore.getState().addLog({
        agent: "WebSocket",
        level: "error",
        message: errorInfo.message,
        metadata: {
          errorType: errorInfo.type,
          context: context || 'unknown',
          readyState: this.getReadyStateString()
        }
      })
    }
  }

  connect() {
    if (typeof window === "undefined") {
      console.log("[WebSocket] Skipping connection: not in browser")
      return
    }

    if (this.ws && this.ws.readyState !== WebSocket.CLOSED) {
      console.log(`[WebSocket] Already connected or connecting (state: ${this.getReadyStateString()})`)
      return
    }

    const url = this.getWebSocketUrl()
    console.log(`[WebSocket] Connecting to: ${url}`)

    try {
      this.ws = new WebSocket(url)
      this.updateConnectionStatus({ connected: false, reconnecting: true })

      // Set connection timeout
      this.connectionTimeoutId = setTimeout(() => {
        if (this.ws && this.ws.readyState === WebSocket.CONNECTING) {
          console.warn("[WebSocket] Connection timeout after 10 seconds")
          this.ws.close()
          this.handleConnectionError(new Error('Connection timeout'), 'timeout')
        }
      }, 10000) // 10 second timeout

      this.ws.onopen = () => {
        console.log("[WebSocket] Connected successfully!")
        
        // Clear connection timeout
        if (this.connectionTimeoutId) {
          clearTimeout(this.connectionTimeoutId)
          this.connectionTimeoutId = null
        }
        
        this.reconnectAttempts = 0
        this.pingsSentWithoutPong = 0
        this.lastPongReceived = new Date()
        
        this.updateConnectionStatus({
          connected: true,
          reconnecting: false,
          lastConnected: new Date(),
          error: undefined
        })
        
        this.startHeartbeat()
        
        // Log successful connection
        useLogStore.getState().addLog({
          agent: "WebSocket",
          level: "info",
          message: "Connected to backend successfully"
        })
      }

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          this.handleMessage(message)
        } catch (parseError) {
          console.error("[WebSocket] Failed to parse message:", this.getErrorMessage(parseError))
          useLogStore.getState().addLog({
            agent: "WebSocket",
            level: "error",
            message: `Failed to parse message: ${this.getErrorMessage(parseError)}`
          })
        }
      }

      this.ws.onclose = (event) => {
        this.stopHeartbeat()
        
        // Clear connection timeout
        if (this.connectionTimeoutId) {
          clearTimeout(this.connectionTimeoutId)
          this.connectionTimeoutId = null
        }
        
        const wasClean = event.code === 1000
        const reason = event.reason || (wasClean ? 'Normal closure' : 'Unexpected closure')
        
        console.log(`[WebSocket] Connection closed. Code: ${event.code}, Reason: ${reason}, Clean: ${wasClean}`)
        
        this.updateConnectionStatus({ 
          connected: false, 
          reconnecting: false,
          error: wasClean ? undefined : `Connection closed: ${reason} (${event.code})`
        })
        
        useLogStore.getState().addLog({
          agent: "WebSocket",
          level: wasClean ? "info" : "warning", 
          message: `Connection ${reason} (Code: ${event.code})`
        })

        // Auto-reconnect if not a clean manual disconnect
        if (!this.isManualDisconnect && this.shouldAutoConnect && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.attemptReconnect()
        } else if (this.reconnectAttempts >= this.maxReconnectAttempts) {
          console.error("[WebSocket] Max reconnection attempts reached")
          useLogStore.getState().addLog({
            agent: "WebSocket",
            level: "error",
            message: "Connection failed after maximum retry attempts. Please refresh the page or check your network connection."
          })
        }
      }

      this.ws.onerror = (event) => {
        this.stopHeartbeat()
        
        // Clear connection timeout
        if (this.connectionTimeoutId) {
          clearTimeout(this.connectionTimeoutId)
          this.connectionTimeoutId = null
        }
        
        console.error(`[WebSocket] Error occurred (readyState: ${this.getReadyStateString()}):`, event)
        
        // Handle the error properly with enhanced error information
        this.handleConnectionError(event, 'connection')
      }

    } catch (error) {
      console.error("[WebSocket] Failed to create connection:", this.getErrorMessage(error))
      this.handleConnectionError(error, 'creation')
    }
  }

  private attemptReconnect() {
    if (this.isManualDisconnect || this.reconnectAttempts >= this.maxReconnectAttempts) {
      return
    }

    this.reconnectAttempts++
    const delay = Math.min(this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1), 30000) // Exponential backoff, max 30s
    
    console.log(`[WebSocket] Reconnecting in ${delay}ms... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
    
    this.updateConnectionStatus({ connected: false, reconnecting: true })
    
    useLogStore.getState().addLog({
      agent: "WebSocket",
      level: "info",
      message: `Reconnecting in ${Math.ceil(delay/1000)}s... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`
    })
    
    this.reconnectTimeout = setTimeout(() => {
      if (this.shouldAutoConnect && !this.isManualDisconnect) {
        this.connect()
      }
    }, delay)
  }

  private handleMessage(message: WebSocketMessage) {
    console.log("[WebSocket] Received:", message)

    const { type, data, agent_name, content } = message
    const agent = agent_name || (data && data.agent_name) || "System"
    const msgContent = content || (data && (data.content || data.message)) || "No message content"

    // Route messages to the appropriate store
    switch (type) {
      case 'pong':
        // Handle pong response to our ping - connection is alive
        console.log("[WebSocket] Received pong from server")
        this.lastPongReceived = new Date()
        this.pingsSentWithoutPong = Math.max(0, this.pingsSentWithoutPong - 1)
        break

      case 'agent_response':
        useConversationStore.getState().addMessage({
          agent: agent,
          content: msgContent,
          type: agent === 'user' ? 'user' : 'agent',
        })
        break

      case 'agent_status':
      case 'agent_progress':
        useAgentStore.getState().updateAgentFromMessage(message)
        break

      case 'stage_update':
        if (data && data.stage_id && data.updates) {
            useProcessStore.getState().updateStage(data.stage_id, data.updates)
        }
        break

      case 'heartbeat':
        this.sendHeartbeatResponse()
        break

      case 'system':
      case 'error':
      default:
        // Default to logging everything else in the log store
        useLogStore.getState().addLog({
          agent,
          level: type === 'error' ? 'error' : 'info',
          message: msgContent,
        })
        break
    }
  }

  private updateConnectionStatus(status: Partial<ConnectionStatus>) {
    this.connectionStatus = { ...this.connectionStatus, ...status }
    this.statusCallbacks.forEach((callback) => {
      try {
        callback(this.connectionStatus)
      } catch (error) {
        console.error("[WebSocket] Status callback error:", this.getErrorMessage(error))
      }
    })
  }

  sendAgentCommand(agentName: string, command: string) {
    this.send({
      type: "agent_command",
      data: {
        agent_name: agentName,
        command: command
      }
    });
  }

  sendArtifactPreference(artifactId: string, isEnabled: boolean) {
    this.send({
      type: "user_command",
      data: {
        command: "set_artifact_preference",
        artifact_id: artifactId,
        is_enabled: isEnabled
      }
    });
  }

  sendChatMessage(message: string) {
    this.send({
      type: "user_command",
      data: {
        command: "chat_message",
        text: message
      }
    });
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
      try {
        const fullMessage = {
          ...message,
          timestamp: new Date().toISOString(),
          session_id: "global_session"
        }
        this.ws.send(JSON.stringify(fullMessage))
        console.log("[WebSocket] Sent:", fullMessage)
      } catch (error) {
        console.error("[WebSocket] Failed to send message:", this.getErrorMessage(error))
        useLogStore.getState().addLog({
          agent: "WebSocket",
          level: "error",
          message: `Failed to send message: ${this.getErrorMessage(error)}`
        })
      }
    } else {
      const state = this.getReadyStateString()
      console.warn(`[WebSocket] Cannot send message: connection state is ${state}`)
      useLogStore.getState().addLog({
        agent: "WebSocket",
        level: "warning",
        message: `Cannot send message: WebSocket state is ${state}`
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

  private sendHeartbeatResponse() {
    this.send({
      type: "heartbeat_response"
    })
  }

  disconnect() {
    console.log("[WebSocket] Manual disconnect requested")
    this.shouldAutoConnect = false
    this.isManualDisconnect = true
    this.stopHeartbeat()
    
    if (this.connectionTimeoutId) {
      clearTimeout(this.connectionTimeoutId)
      this.connectionTimeoutId = null
    }
    
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout)
      this.reconnectTimeout = null
    }
    
    if (this.ws) {
      this.ws.close(1000, "Manual disconnect")
      this.ws = null
    }
    
    this.updateConnectionStatus({
      connected: false,
      reconnecting: false,
      error: undefined
    })
  }

  // Utility methods for debugging
  getDebugInfo() {
    return {
      connected: this.connectionStatus.connected,
      reconnecting: this.connectionStatus.reconnecting,
      readyState: this.getReadyStateString(),
      reconnectAttempts: this.reconnectAttempts,
      shouldAutoConnect: this.shouldAutoConnect,
      isManualDisconnect: this.isManualDisconnect,
      lastPongReceived: this.lastPongReceived,
      pingsSentWithoutPong: this.pingsSentWithoutPong
    }
  }
}

export const websocketService = new SimpleWebSocketService()
