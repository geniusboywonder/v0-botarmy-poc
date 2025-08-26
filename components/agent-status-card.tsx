"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { 
  Bot, 
  Play, 
  Pause, 
  Square, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  Zap,
  Loader2
} from "lucide-react"
import { cn } from "@/lib/utils"

import { TypingIndicator } from "@/components/ui/typing-indicator"

export interface Agent {
  id: string
  name: string
  role: string
  status: "active" | "idle" | "working" | "error" | "offline" | "paused"
  currentTask?: string
  lastActivity: Date | string
  tasksCompleted: number
  successRate: number
  progress?: number
  progress_stage?: string
  progress_current?: number
  progress_total?: number
  progress_estimated_time_remaining?: number
  is_thinking?: boolean
}

interface AgentStatusCardProps {
  agent: Agent
}

export function AgentStatusCard({ agent }: AgentStatusCardProps) {
  const getStatusColor = (status: Agent['status']) => {
    switch (status) {
      case 'active':
      case 'working':
        return 'bg-green-500' // WIP
      case 'idle':
        return 'bg-gray-400' // Queued
      case 'paused':
        return 'bg-yellow-500' // Waiting
      case 'error':
        return 'bg-red-500' // Error
      // Assuming 'completed' is a possible status
      case 'completed':
        return 'bg-blue-500' // Done
      default:
        return 'bg-gray-400'
    }
  }

  const handlePauseResume = () => {
    // TODO: Implement pause/resume functionality via websocket
    console.log(`${agent.status === 'paused' ? 'Resuming' : 'Pausing'} agent:`, agent.name)
  }

  return (
    <Card className="h-full">
      <CardContent className="p-3 flex flex-col justify-between h-full space-y-2">
        {/* Top line: Status Icon, Agent Role, Play/Pause Button */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span
              className={cn('h-3 w-3 rounded-full', getStatusColor(agent.status))}
              title={`Status: ${agent.status}`}
            />
            <span className="font-semibold text-sm truncate" title={agent.role}>
              {agent.role}
            </span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="h-6 w-6 p-0"
            onClick={handlePauseResume}
          >
            {agent.status === 'paused' ? (
              <Play className="w-4 h-4" />
            ) : (
              <Pause className="w-4 h-4" />
            )}
          </Button>
        </div>

        {/* Middle line: Task Description */}
        <div className="text-xs text-muted-foreground truncate" title={agent.currentTask || 'No active task'}>
          {agent.currentTask || 'Idle'}
        </div>

        {/* Bottom line: Task Progress */}
        <div className="text-xs font-medium">
          {agent.progress_current !== undefined && agent.progress_total !== undefined ? (
            <span>
              Task: {agent.progress_current}/{agent.progress_total}
            </span>
          ) : (
            <span>&nbsp;</span> // Placeholder for alignment
          )}
        </div>
      </CardContent>
    </Card>
  )
}

export function AgentStatusCardSkeleton() {
  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-3">
            <Avatar className="w-8 h-8">
              <div className="w-full h-full bg-muted rounded-full animate-pulse" />
            </Avatar>
            <div className="flex-1 min-w-0 space-y-1">
              <div className="h-4 bg-muted rounded w-3/4 animate-pulse" />
              <div className="h-3 bg-muted rounded w-1/2 animate-pulse" />
            </div>
          </div>
        </div>
        <div className="flex items-center justify-between mb-3">
          <div className="h-5 bg-muted rounded w-1/4 animate-pulse" />
          <div className="h-3 bg-muted rounded w-1/4 animate-pulse" />
        </div>
        <div className="space-y-2">
          <div className="h-3 bg-muted rounded w-full animate-pulse" />
          <div className="h-3 bg-muted rounded w-5/6 animate-pulse" />
        </div>
      </CardContent>
    </Card>
  )
}