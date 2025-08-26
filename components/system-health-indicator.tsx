"use client"

import { useState, useEffect } from "react"
import { Badge } from "@/components/ui/badge"
import { Activity } from "lucide-react"
import { cn } from "@/lib/utils"

const getStatusColor = (status: string) => {
  switch (status) {
    case 'healthy':
      return 'text-green-600'
    case 'degraded':
      return 'text-yellow-600'
    case 'unhealthy':
      return 'text-red-600'
    default:
      return 'text-gray-600'
  }
}

export function SystemHealthIndicator() {
  const [status, setStatus] = useState('unknown')
  const [lastUpdated, setLastUpdated] = useState("")
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    // In a real app, this would fetch from a health endpoint
    setStatus('healthy')
    setLastUpdated(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }))
  }, [])

  if (!mounted) {
    return (
      <div className="text-xs text-muted-foreground">
        System Health: <span className="font-semibold">Loading...</span>
      </div>
    )
  }

  return (
    <div className="space-y-1 text-xs text-muted-foreground">
      <div>
        System Health:{" "}
        <span className={cn("font-semibold", getStatusColor(status))}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </span>
      </div>
      <div>
        Last Updated: <span className="font-semibold">{lastUpdated}</span>
      </div>
    </div>
  )
}
