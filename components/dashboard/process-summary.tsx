"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, AlertCircle, Loader, PauseCircle, XCircle, Play, ChevronRight, User } from "lucide-react"
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
        <Card className="flex-1 min-w-0 h-48">
            <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                    <CardTitle className="text-base truncate">{stage.name}</CardTitle>
                    <StatusIcon className={cn("w-5 h-5 flex-shrink-0", statusConfigEntry.color)} />
                </div>
                <CardDescription className="text-xs">{statusConfigEntry.label}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2 pt-0">
                <div className="flex items-center text-xs">
                    <User className="w-3 h-3 mr-1 flex-shrink-0" />
                    <span className="truncate">{stage.agentName}</span>
                </div>
                <p className="text-xs text-muted-foreground truncate" title={stage.currentTask}>
                    {stage.currentTask}
                </p>
                <div>
                    <p className="text-xs">Tasks: {completedTasks} / {totalTasks}</p>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                        <div
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${progress}%` }}
                        ></div>
                    </div>
                </div>
                {stage.hitlRequired && (
                    <Badge variant="destructive" className="flex items-center gap-1 text-xs">
                        <AlertCircle className="w-3 h-3" />
                        HITL Required
                    </Badge>
                )}
                <div className="flex gap-1 pt-1">
                    <Button size="sm" variant="outline" className="flex-1 text-xs h-7">
                        <Play className="w-3 h-3 mr-1" />
                        Resume
                    </Button>
                     <Button size="sm" variant="destructive" className="flex-1 text-xs h-7">
                        <PauseCircle className="w-3 h-3 mr-1" />
                        Pause
                    </Button>
                </div>
            </CardContent>
        </Card>
    )
}


export function ProcessSummary() {
  const stages = useProcessStore((state) => state.stages)

  const renderSkeletons = () => (
    <div className="flex items-center space-x-3">
        {[...Array(5)].map((_, i) => (
            <div key={`skeleton-${i}`} className="flex items-center flex-1">
                <Card className="flex-1 h-48">
                    <CardHeader className="pb-2">
                        <Skeleton className="h-5 w-3/4" />
                        <Skeleton className="h-3 w-1/2" />
                    </CardHeader>
                    <CardContent className="space-y-2 pt-0">
                        <Skeleton className="h-3 w-full" />
                        <Skeleton className="h-3 w-full" />
                        <Skeleton className="h-6 w-full" />
                    </CardContent>
                </Card>
                {i < 4 && <ChevronRight key={`arrow-${i}`} className="w-6 h-6 text-muted-foreground mx-2 flex-shrink-0" />}
            </div>
        ))}
    </div>
  )

  return (
    <div>
        <CardHeader>
            <CardTitle>Process Summary</CardTitle>
            <CardDescription>
                Overview of the entire SDLC process stages.
            </CardDescription>
        </CardHeader>
        <CardContent>
            <div className="pb-4">
                {stages.length === 0 ? (
                    renderSkeletons()
                ) : (
                    <div className="flex items-center space-x-3">
                        {stages.map((stage, index) => (
                            <div key={`stage-${stage.id}-${index}`} className="flex items-center flex-1">
                                <StageCard stage={stage} />
                                {index < stages.length - 1 && (
                                    <ChevronRight key={`stage-arrow-${stage.id}-${index}`} className="w-6 h-6 text-muted-foreground mx-2 flex-shrink-0" />
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </CardContent>
    </div>
  )
}
