"use client"

import React, { createContext, useContext, useEffect, useRef } from 'react'
import { websocketService } from '@/lib/websocket/websocket-service'

interface WebSocketContextType {
  service: typeof websocketService
  isConnected: boolean
}

const WebSocketContext = createContext<WebSocketContextType | null>(null)

export function WebSocketProvider({ children }: { children: React.ReactNode }) {
  const connectionInitialized = useRef(false)
  const lastUrl = useRef<string>("")

  useEffect(() => {
    // Initialize connection only once per app session
    if (!connectionInitialized.current) {
      console.log('[WebSocketProvider] Initializing global WebSocket connection')
      websocketService.enableAutoConnect()
      connectionInitialized.current = true
      lastUrl.current = window.location.href
    }

    // Monitor URL changes for SPA navigation detection
    const checkForNavigation = () => {
      const currentUrl = window.location.href
      if (currentUrl !== lastUrl.current) {
        console.log(`[WebSocketProvider] Navigation detected: ${lastUrl.current} → ${currentUrl}`)
        lastUrl.current = currentUrl
        handleNavigation()
      }
    }

    // Check for navigation changes more frequently
    const navigationInterval = setInterval(checkForNavigation, 1000)

    // Don't disconnect on unmount - keep connection alive for the entire app session
    // Only disconnect when the browser tab/window is actually closed
    const handleBeforeUnload = () => {
      console.log('[WebSocketProvider] Browser closing, disconnecting WebSocket')
      websocketService.disconnect()
    }

    const handleVisibilityChange = () => {
      if (document.hidden) {
        console.log('[WebSocketProvider] Page hidden, maintaining connection')
        // Keep connection alive but could reduce heartbeat frequency
      } else {
        console.log('[WebSocketProvider] Page visible, ensuring connection')
        // Ensure connection is active when page becomes visible
        websocketService.ensureConnection()
      }
    }

    // Add navigation change detection for SPA routing
    const handleNavigation = () => {
      console.log('[WebSocketProvider] Navigation detected, ensuring connection')
      // Reset reconnection state and ensure connection after navigation
      websocketService.resetReconnectionState()
      setTimeout(() => {
        websocketService.ensureConnection()
      }, 500) // Small delay to allow page transition
    }

    // Listen for Next.js route changes
    const handleRouteChange = () => {
      handleNavigation()
    }

    // Add event listeners
    window.addEventListener('beforeunload', handleBeforeUnload)
    document.addEventListener('visibilitychange', handleVisibilityChange)
    
    // Listen for navigation changes (hashchange and popstate for SPA routing)
    window.addEventListener('hashchange', handleNavigation)
    window.addEventListener('popstate', handleNavigation)

    // Cleanup event listeners and navigation interval
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
      window.removeEventListener('hashchange', handleNavigation)
      window.removeEventListener('popstate', handleNavigation)
      clearInterval(navigationInterval)
    }
  }, [])

  return (
    <WebSocketContext.Provider value={{ 
      service: websocketService, 
      isConnected: true // This will be dynamic later
    }}>
      {children}
    </WebSocketContext.Provider>
  )
}

export function useWebSocketContext() {
  const context = useContext(WebSocketContext)
  if (!context) {
    throw new Error('useWebSocketContext must be used within WebSocketProvider')
  }
  return context
}
