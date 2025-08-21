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
  private reconnectDelay = 1000 // start with 1s
  private maxReconnectDelay = 30000 // max delay of 30s
  private connectionStatus: ConnectionStatus = { connected: false, reconnecting: false }
  private statusCallbacks: ((status: ConnectionStatus) => void)[] = []
  private messageQueue: any[] = []

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
        // Check if we have environment variables from Next.js
        const envWebSocketUrl = process.env.NEXT_PUBLIC_WEBSOCKET_URL;
        if (envWebSocketUrl) {
            console.log(`[WebSocket] Using environment URL: ${envWebSocketUrl}`);
            return envWebSocketUrl;
        }
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        
        // For localhost development
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
            const url = `${protocol}//localhost:8000/ws`;
            console.log(`[WebSocket] Development URL: ${url}`);
            return url;
        }
        
        // For Vercel and other production deployments
        // Use the same host but with WebSocket protocol and the /api path
        const url = `${protocol}//${window.location.host}/api/ws`;
        console.log(`[WebSocket] Production URL: ${url}`);
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
      // Process any queued messages
      this.processMessageQueue()
      this.requestArtifacts()
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
      const reason = event.reason || 'No reason provided'
      const code = event.code
      const wasClean = event.wasClean
      
      console.log(`[WebSocket] Connection closed. Code: ${code}, Reason: ${reason}, Clean: ${wasClean}`)
      
      // Add detailed error message based on close code
      let errorMessage = `Connection closed (Code: ${code})`
      if (code === 1006) {
        errorMessage += ' - Backend server unreachable. Check if backend is running on port 8000.'
      } else if (code === 1000) {
        errorMessage += ' - Normal closure'
      } else if (reason) {
        errorMessage += ` - ${reason}`
      }
      
      useLogStore.getState().addLog({
        agent: "System",
        level: "error",
        message: errorMessage,
      })
      
      this.updateConnectionStatus({ connected: false, reconnecting: false, error: errorMessage })
      this.attemptReconnect()
    }

    this.ws.onerror = (event) => {
      console.error("[WebSocket] An error occurred.", event)
      const errorMsg = "WebSocket error occurred. This usually means the backend server is not running or not accessible on port 8000."
      
      useLogStore.getState().addLog({
        agent: "System",
        level: "error",
        message: errorMsg,
      })
      
      this.updateConnectionStatus({
        connected: false,
        reconnecting: false,
        error: errorMsg,
      })
    }
  }

  private handleMessage(message: WebSocketMessage) {
    console.log("[WebSocket] Received:", message);
    const { type, data, agent_name, content } = message;

    // The log store is our central sink for all messages for now.
    // In the future, specific handlers might choose not to log.
    const log = (level: 'info' | 'error' = 'info', overrideContent?: string) => {
        const agent = agent_name || (data && data.agent_name) || "System";
        const msgContent = overrideContent || content || (data && (data.content || data.thought || data.error)) || "No message content.";
        useLogStore.getState().addLog({ agent, level, message: msgContent });
    }

    switch (type) {
      case 'heartbeat':
        this.send({ type: 'heartbeat_response' });
        // No need to log heartbeats
        break;

      case 'agent_status':
        useAgentStore.getState().updateAgentFromMessage(message);
        // We can still log it for debugging if needed
        log('info', `Agent ${agent_name} is now ${data?.status}. Task: ${data?.task}`);
        break;

      case 'agent_response':
        log();
        break;

      case 'error':
        const errorContent = data?.error || content || "Unknown error";
        if (agent_name) {
          useAgentStore.getState().handleAgentError(agent_name, errorContent);
        }
        log('error', errorContent);
        break;

      case 'system':
        // Handle system messages, e.g., the welcome message with client_id
        if (data?.event === 'connected') {
            console.log(`[WebSocket] Connected with client_id: ${data.client_id}`);
        }
        log();
        break;

      default:
        console.warn(`[WebSocket] Received unknown message type: ${type}`);
        log();
        break;
    }
  }


  private attemptReconnect() {
    if (!this.shouldAutoConnect) {
      return
    }

    this.reconnectAttempts++
    this.updateConnectionStatus({ connected: false, reconnecting: true })

    // Exponential backoff with a cap
    const delay = Math.min(this.reconnectDelay * Math.pow(2, this.reconnectAttempts), this.maxReconnectDelay)

    console.log(`[WebSocket] Reconnecting in ${delay}ms... (Attempt ${this.reconnectAttempts})`)
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

  getConnectionStatus(): ConnectionStatus {
    return { ...this.connectionStatus }
  }

  private processMessageQueue() {
    if (this.messageQueue.length > 0) {
      console.log(`[WebSocket] Processing ${this.messageQueue.length} queued messages...`)
      // Send all messages in the queue
      while (this.messageQueue.length > 0) {
        const message = this.messageQueue.shift()
        this.send(message)
      }
    }
  }

  private send(message: any) {
    // If the connection is open, send immediately.
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const fullMessage = {
        ...message,
        timestamp: new Date().toISOString(),
        session_id: "global_session" // Using a global session for now
      }
      this.ws.send(JSON.stringify(fullMessage))
      return
    }

    // If the connection is not open, queue the message.
    console.warn("[WebSocket] Connection not open. Queuing message:", message)
    this.messageQueue.push(message);

    // If we are not currently in a reconnect cycle, start one.
    if (!this.connectionStatus.reconnecting) {
        console.log("[WebSocket] Triggering reconnect due to queued message.")
        this.connect()
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

  testOpenAI() {
    this.send({
      type: "user_command",
      data: {
        command: "test_openai",
      },
    })
  }

  testBackendConnection() {
    this.send({
      type: "user_command",
      data: {
        command: "ping",
      },
    })
  }

  requestArtifacts() {
    this.send({
      type: "artifacts_get_all",
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
