"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { RefreshCw, Wifi, WifiOff, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"
import { websocketService } from "@/lib/websocket/websocket-service"

export function ConnectionStatus() {
  const [connectionStatus, setConnectionStatus] = useState('disconnected')
  const [isRefreshing, setIsRefreshing] = useState(false)

  const checkConnection = () => {
    try {
      const status = websocketService.getConnectionStatus()
      setConnectionStatus(status.connected ? 'connected' : status.reconnecting ? 'connecting' : 'disconnected')
    } catch (error) {
      setConnectionStatus('disconnected')
    }
  }

  useEffect(() => {
    checkConnection()
    const interval = setInterval(checkConnection, 2000)
    return () => clearInterval(interval)
  }, [])

  const handleRefresh = () => {
    setIsRefreshing(true)
    websocketService.disconnect()
    setTimeout(() => {
      websocketService.enableAutoConnect()
      websocketService.connect()
      setIsRefreshing(false)
    }, 1000)
  }

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'text-green-600'
      case 'connecting': return 'text-yellow-600'
      default: return 'text-red-600'
    }
  }

  const getStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected': return <Wifi className="w-4 h-4" />
      case 'connecting': return <Loader2 className="w-4 h-4 animate-spin" />
      default: return <WifiOff className="w-4 h-4" />
    }
  }

  return (
    <div className="space-y-2">
       <div className="font-semibold text-xs text-muted-foreground">Connection</div>
       <div className="flex items-center justify-between text-xs">
        <div className={cn("flex items-center gap-2", getStatusColor())}>
          {getStatusIcon()}
          <span className="font-semibold">
            {connectionStatus.charAt(0).toUpperCase() + connectionStatus.slice(1)}
          </span>
        </div>
        <span className="text-muted-foreground">
          {connectionStatus === 'connected' ? 'Real-time active' : 'Inactive'}
        </span>
      </div>
      <Button
        variant="outline"
        size="sm"
        className="w-full"
        onClick={handleRefresh}
        disabled={isRefreshing}
      >
        <RefreshCw className={cn("w-4 h-4 mr-2", isRefreshing && "animate-spin")} />
        Refresh Status
      </Button>
    </div>
  )
}
