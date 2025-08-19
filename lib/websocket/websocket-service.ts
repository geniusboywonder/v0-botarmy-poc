import { useAgentStore } from "../stores/agent-store"
import { useLogStore } from "../stores/log-store"
import { useArtifactStore } from "../stores/artifact-store"

// --- TYPE DEFINITIONS ---

export interface WebSocketMessage {
  type: string
  // Based on AG-UI protocol, most data is in a nested object.
  data?: any
  // Fields from AG-UI that can appear at the top level
  agent_name?: string;
  content?: string;
  payload?: any;
  timestamp: string
}

export interface ConnectionStatus {
  connected: boolean
  reconnecting: boolean
  lastConnected?: Date
  error?: string
}


// --- WEB-SOCKET SERVICE ---

class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 10
  private reconnectDelay = 1000 // start with 1s, then increase
  private connectionStatus: ConnectionStatus = { connected: false, reconnecting: false }
  private statusCallbacks: ((status: ConnectionStatus) => void)[] = []

  // This flag is controlled by the UI to enable/disable auto-connection.
  private shouldAutoConnect = false

  constructor() {
    this.updateConnectionStatus = this.updateConnectionStatus.bind(this)
    this.handleMessage = this.handleMessage.bind(this)
    this.attemptReconnect = this.attemptReconnect.bind(this)
    this.setupEventHandlers = this.setupEventHandlers.bind(this)
  }

  private getWebSocketUrl(): string {
    if (typeof window !== 'undefined') {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        // Use environment variable for production WebSocket URL, otherwise default to localhost
        const host = process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'localhost:8000';
        const url = `${protocol}//${host}/ws`;
        console.log(`[WebSocket] URL set to: ${url}`);
        return url;
    }
    // Default for non-browser environments
    return 'ws://localhost:8000/ws';
  }

  connect() {
    if (typeof window === "undefined" || this.ws) {
      console.log("[WebSocket] Connection skipped: Not in browser or already connected/connecting.");
      return
    }

    if (!this.shouldAutoConnect) {
      console.log("[WebSocket] Connection skipped: Auto-connect is disabled.")
      return
    }

    const url = this.getWebSocketUrl();
    console.log(`[WebSocket] Attempting to connect to: ${url}`)

    try {
      this.ws = new WebSocket(url)
      this.setupEventHandlers()
      this.updateConnectionStatus({ connected: false, reconnecting: true })
    } catch (error) {
      console.error("[WebSocket] Connection failed to initiate:", error)
      this.updateConnectionStatus({
        connected: false,
        reconnecting: false,
        error: error instanceof Error ? error.message : "Connection failed",
      })
    }
  }

  // This should be called by the UI to start the connection process.
  enableAutoConnect() {
    this.shouldAutoConnect = true
    this.connect()
  }

  private setupEventHandlers() {
    if (!this.ws) return

    this.ws.onopen = () => {
      console.log("[WebSocket] Connection established.")
      this.reconnectAttempts = 0
      this.updateConnectionStatus({
        connected: true,
        reconnecting: false,
        lastConnected: new Date(),
        error: undefined,
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

    this.ws.onclose = () => {
      console.log("[WebSocket] Connection closed.")
      this.updateConnectionStatus({ connected: false, reconnecting: false })
      this.attemptReconnect()
    }

    this.ws.onerror = (event) => {
      console.error("[WebSocket] An error occurred.", event)
      this.updateConnectionStatus({
        connected: false,
        reconnecting: false,
        error: "A WebSocket error occurred. Check the console.",
      })
    }
  }

  private handleMessage(message: WebSocketMessage) {
    console.log("[WebSocket] Received:", message);
    const { type, data, agent_name, content } = message;

    // Use AG-UI protocol fields where available
    const agent = agent_name || (data && data.agent_name) || "System";
    const msgContent = content || (data && (data.content || data.thought || data.error)) || "No message content.";

    // Push almost everything to the log store for visibility
    useLogStore.getState().addLog({
      agent: agent,
      level: type === 'system_error' ? 'error' : 'info',
      message: msgContent,
    });

    // Handle specific message types for other stores
    switch (type) {
      case "agent_status":
        if (data?.agent_name && data?.state) {
          useAgentStore.getState().updateAgentByName(data.agent_name, {
            status: data.state,
            currentTask: data.current_task,
          });
        }
        break;

      case "artifacts_update":
        if (message.payload) {
          useArtifactStore.getState().setArtifacts(message.payload);
        }
        break;

      default:
        // The log was already added above, so we just log a console warning for unknown types.
        console.warn("[WebSocket] Unhandled specific message type:", type);
    }
  }


  private attemptReconnect() {
    if (!this.shouldAutoConnect) {
      return
    }
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error("[WebSocket] Max reconnection attempts reached.")
      this.updateConnectionStatus({
        connected: false,
        reconnecting: false,
        error: "Connection failed after multiple retries.",
      })
      return
    }

    this.reconnectAttempts++
    this.updateConnectionStatus({ connected: false, reconnecting: true })

    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts)
    console.log(`[WebSocket] Reconnecting in ${delay}ms...`)
    setTimeout(() => this.connect(), delay)
  }

  private updateConnectionStatus(status: Partial<ConnectionStatus>) {
    this.connectionStatus = { ...this.connectionStatus, ...status }
    this.statusCallbacks.forEach((callback) => callback(this.connectionStatus))
  }

  onStatusChange(callback: (status: ConnectionStatus) => void) {
    this.statusCallbacks.push(callback)
    // Return a function to unsubscribe
    return () => {
      const index = this.statusCallbacks.indexOf(callback)
      if (index > -1) this.statusCallbacks.splice(index, 1)
    }
  }

  private send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const fullMessage = {
        ...message,
        timestamp: new Date().toISOString(),
        session_id: "global_session" // Example session ID for now
      }
      this.ws.send(JSON.stringify(fullMessage))
    } else {
      // Maybe queue the message or show an error to the user
      console.warn("[WebSocket] Connection not open. Message not sent:", message)
      useLogStore.getState().addLog({
          agent: "System",
          level: "error",
          message: "Connection to server lost. Please check your connection and refresh.",
        })
    }
  }

  startProject(brief: string) {
    this.send({
      type: "user_command",
      data: {
        command: "start_project",
        brief: brief,
      },
    })
  }

  disconnect() {
    this.shouldAutoConnect = false
    if (this.ws) {
      this.ws.close()
    }
  }
}

export const websocketService = new WebSocketService()
