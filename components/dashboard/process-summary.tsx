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
        <Card className="w-64 flex-shrink-0">
            <CardHeader>
                <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{stage.name}</CardTitle>
                    <StatusIcon className={cn("w-6 h-6", statusConfigEntry.color)} />
                </div>
                <CardDescription>{statusConfigEntry.label}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
                <div className="flex items-center text-sm">
                    <User className="w-4 h-4 mr-2" />
                    <span>{stage.agentName}</span>
                </div>
                <p className="text-sm text-muted-foreground truncate" title={stage.currentTask}>
                    Current: {stage.currentTask}
                </p>
                <div>
                    <p className="text-sm">Tasks: {completedTasks} / {totalTasks}</p>
                    <div className="w-full bg-gray-200 rounded-full h-2.5 mt-1">
                        <div
                            className="bg-blue-600 h-2.5 rounded-full"
                            style={{ width: `${progress}%` }}
                        ></div>
                    </div>
                </div>
                {stage.hitlRequired && (
                    <Badge variant="destructive" className="flex items-center gap-1">
                        <AlertCircle className="w-3 h-3" />
                        Human-in-the-Loop Required
                    </Badge>
                )}
                <div className="flex gap-2 pt-2">
                    <Button size="sm" variant="outline">
                        <Play className="w-4 h-4 mr-2" />
                        Resume
                    </Button>
                     <Button size="sm" variant="destructive">
                        <PauseCircle className="w-4 h-4 mr-2" />
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
    <div className="flex items-center space-x-4">
        {[...Array(5)].map((_, i) => (
            <div key={`skeleton-${i}`} className="flex items-center">
                <Card className="w-64 flex-shrink-0">
                    <CardHeader>
                        <Skeleton className="h-6 w-3/4" />
                        <Skeleton className="h-4 w-1/2" />
                    </CardHeader>
                    <CardContent className="space-y-3">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-8 w-full" />
                    </CardContent>
                </Card>
                {i < 4 && <ChevronRight key={`arrow-${i}`} className="w-8 h-8 text-muted-foreground" />}
            </div>
        ))}
    </div>
  )

  return (
    <Card>
        <CardHeader>
            <CardTitle>Process Summary</CardTitle>
            <CardDescription>
                Overview of the entire SDLC process. Scroll horizontally to see all stages.
            </CardDescription>
        </CardHeader>
        <CardContent>
            <div className="flex items-center pb-4">
                <div className="flex-1 overflow-x-auto">
                    {stages.length === 0 ? (
                        renderSkeletons()
                    ) : (
                        <div className="flex items-center space-x-4">
                            {stages.map((stage, index) => (
                                <div key={`stage-${stage.id}-${index}`} className="flex items-center">
                                    <StageCard stage={stage} />
                                    {index < stages.length - 1 && (
                                        <ChevronRight key={`stage-arrow-${stage.id}-${index}`} className="w-8 h-8 text-muted-foreground" />
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </CardContent>
    </Card>
  )
}