"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, AlertCircle, Loader, PauseCircle, XCircle, ChevronRight, User, Pause } from "lucide-react"
import { cn } from "@/lib/utils"
import { useProcessStore, ProcessStage } from "@/lib/stores/process-store"
import { Skeleton } from "@/components/ui/skeleton"

const statusConfig = {
    done: { icon: CheckCircle, color: "text-green-500", label: "Done" },
    wip: { icon: Loader, color: "text-blue-500 animate-spin", label: "In Progress" },
    queued: { icon: PauseCircle, color: "text-gray-500", label: "Queued" },
    error: { icon: XCircle, color: "text-red-500", label: "Error" },
    waiting: { icon: AlertCircle, color: "text-yellow-500", label: "Waiting" },
}

function StageCard({ stage }: { stage: ProcessStage }) {
    const statusConfigEntry = statusConfig[stage.status]
    if (!statusConfigEntry) {
        console.error('Unknown stage status:', stage.status)
        return null
    }
    
    const StatusIcon = statusConfigEntry.icon
    const completedTasks = stage.tasks.filter(t => t.status === 'done').length
    const totalTasks = stage.tasks.length
    const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0

    return (
        <Card className="flex-1 h-32 min-w-0 border-2">
            <CardContent className="p-3 h-full flex flex-col justify-between">
                {/* Header Row: Stage Name + Icons */}
                <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-semibold truncate pr-2">{stage.name}</h3>
                    <div className="flex items-center gap-1 flex-shrink-0">
                        <Pause className="w-3 h-3 text-gray-400 cursor-pointer hover:text-gray-600" />
                        <StatusIcon className={cn("w-4 h-4", statusConfigEntry.color)} />
                    </div>
                </div>

                {/* Agent Row */}
                <div className="flex items-center text-xs text-muted-foreground mb-2">
                    <User className="w-3 h-3 mr-1 flex-shrink-0" />
                    <span className="truncate">{stage.agentName}</span>
                </div>

                {/* Current Task */}
                <div className="text-xs text-muted-foreground mb-2 line-clamp-1" title={stage.currentTask}>
                    {stage.currentTask || "No active task"}
                </div>

                {/* Tasks Counter and Progress Bar */}
                <div className="space-y-1">
                    <div className="flex items-center justify-between">
                        <span className="text-xs">Tasks: {completedTasks} / {totalTasks}</span>
                        {stage.hitlRequired && (
                            <Badge variant="destructive" className="text-xs px-1 py-0 h-4">
                                HITL
                            </Badge>
                        )}
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1.5">
                        <div
                            className="bg-blue-600 h-1.5 rounded-full" 
                            style={{ width: `${progress}%` }}
                        ></div>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}

export function ProcessSummary() {
  const stages = useProcessStore((state) => state.stages)

  const renderSkeletons = () => (
    <div className="flex items-center space-x-2">
        {[...Array(5)].map((_, i) => (
            <div key={`skeleton-${i}`} className="flex items-center flex-1">
                <Card className="flex-1 h-32 border-2">
                    <CardContent className="p-3 h-full flex flex-col justify-between">
                        <div className="space-y-2">
                            <Skeleton className="h-4 w-3/4" />
                            <Skeleton className="h-3 w-full" />
                            <Skeleton className="h-3 w-2/3" />
                            <Skeleton className="h-2 w-full" />
                        </div>
                    </CardContent>
                </Card>
                {i < 4 && <ChevronRight key={`arrow-${i}`} className="w-4 h-4 text-muted-foreground mx-1 flex-shrink-0" />}
            </div>
        ))}
    </div>
  )

  return (
    <Card>
        <CardHeader className="pb-3">
            <CardTitle className="text-lg">Process Summary</CardTitle>
            <CardDescription>
                Overview of the entire SDLC process stages.
            </CardDescription>
        </CardHeader>
        <CardContent>
            {stages.length === 0 ? (
                renderSkeletons()
            ) : (
                <div className="flex items-center space-x-2">
                    {stages.map((stage, index) => (
                        <div key={`stage-${stage.id}-${index}`} className="flex items-center flex-1">
                            <StageCard stage={stage} />
                            {index < stages.length - 1 && (
                                <ChevronRight key={`stage-arrow-${stage.id}-${index}`} className="w-4 h-4 text-muted-foreground mx-1 flex-shrink-0" />
                            )}
                        </div>
                    ))}
                </div>
            )}
        </CardContent>
    </Card>
  )
}
