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
}

interface AgentStatusCardProps {
  agent: Agent
}

export function AgentStatusCard({ agent }: AgentStatusCardProps) {
  const getStatusColor = (status: Agent['status']) => {
    switch (status) {
      case 'active': 
      case 'working': 
        return 'bg-green-500'
      case 'idle': 
        return 'bg-yellow-500'
      case 'paused': 
        return 'bg-blue-500'
      case 'error': 
        return 'bg-red-500'
      case 'offline': 
        return 'bg-gray-400'
      default: 
        return 'bg-gray-400'
    }
  }

  const getStatusIcon = (status: Agent['status']) => {
    switch (status) {
      case 'working': 
        return <Loader2 className="w-3 h-3 animate-spin" />
      case 'active': 
        return <CheckCircle className="w-3 h-3" />
      case 'idle': 
        return <Clock className="w-3 h-3" />
      case 'paused': 
        return <Pause className="w-3 h-3" />
      case 'error': 
        return <AlertTriangle className="w-3 h-3" />
      case 'offline': 
        return <Square className="w-3 h-3" />
      default: 
        return <Bot className="w-3 h-3" />
    }
  }

  const getStatusText = (status: Agent['status']) => {
    switch (status) {
      case 'working': return 'Working'
      case 'active': return 'Active'
      case 'idle': return 'Idle'
      case 'paused': return 'Paused'
      case 'error': return 'Error'
      case 'offline': return 'Offline'
      default: return 'Unknown'
    }
  }

  const getAgentIcon = (role: string) => {
    const roleKey = role.toLowerCase()
    if (roleKey.includes('analyst')) return '🔍'
    if (roleKey.includes('architect')) return '🏗️'
    if (roleKey.includes('developer')) return '👨‍💻'
    if (roleKey.includes('tester')) return '🧪'
    if (roleKey.includes('deploy')) return '🚀'
    return '🤖'
  }

  const formatLastActivity = (lastActivity: Date | string) => {
    const date = typeof lastActivity === 'string' ? new Date(lastActivity) : lastActivity
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / (1000 * 60))
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours}h ago`
    const diffDays = Math.floor(diffHours / 24)
    return `${diffDays}d ago`
  }

  const handlePauseResume = () => {
    // TODO: Implement pause/resume functionality
    console.log(`${agent.status === 'paused' ? 'Resuming' : 'Pausing'} agent:`, agent.name)
  }

  return (
    <Card className={cn(
      "relative transition-all duration-200 hover:shadow-md",
      agent.status === 'working' && "ring-2 ring-green-500/20 ring-offset-1",
      agent.status === 'error' && "ring-2 ring-red-500/20 ring-offset-1"
    )}>
      <CardContent className="p-4">
        {/* Header with Avatar and Status */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Avatar className="w-8 h-8">
                <AvatarImage src={`/api/placeholder/32/32?text=${agent.name[0]}`} />
                <AvatarFallback className="text-xs">
                  {getAgentIcon(agent.role)}
                </AvatarFallback>
              </Avatar>
              {/* Status indicator dot */}
              <div className={cn(
                "absolute -top-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-background",
                getStatusColor(agent.status)
              )} />
            </div>
            
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-sm truncate">{agent.name}</h3>
              <p className="text-xs text-muted-foreground truncate">{agent.role}</p>
            </div>
          </div>

          {/* Pause/Resume Button */}
          <Button
            variant="ghost"
            size="sm"
            className="h-6 w-6 p-0"
            onClick={handlePauseResume}
          >
            {agent.status === 'paused' ? (
              <Play className="w-3 h-3" />
            ) : (
              <Pause className="w-3 h-3" />
            )}
          </Button>
        </div>

        {/* Status Badge */}
        <div className="flex items-center justify-between mb-3">
          <Badge 
            variant={agent.status === 'error' ? 'destructive' : 'outline'}
            className="text-xs"
          >
            <span className="mr-1">{getStatusIcon(agent.status)}</span>
            {getStatusText(agent.status)}
          </Badge>

          <span className="text-xs text-muted-foreground">
            {formatLastActivity(agent.lastActivity)}
          </span>
        </div>

        {/* Current Task */}
        {agent.currentTask && (
          <div className="mb-3">
            <p className="text-xs text-muted-foreground mb-1">Current Task:</p>
            <p className="text-xs font-medium truncate" title={agent.currentTask}>
              {agent.currentTask}
            </p>
            
            {/* Progress bar if available */}
            {agent.progress !== undefined && (
              <Progress value={agent.progress} className="mt-2 h-1" />
            )}
          </div>
        )}

        {/* Stats */}
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <div className="flex items-center space-x-3">
            <span>✓ {agent.tasksCompleted}</span>
            <span>{agent.successRate}% success</span>
          </div>
          
          {agent.status === 'working' && (
            <div className="flex items-center space-x-1">
              <Zap className="w-3 h-3" />
              <span>Active</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}