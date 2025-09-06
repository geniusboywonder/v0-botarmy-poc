"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, AlertCircle, Loader, PauseCircle, XCircle, ChevronRight, User } from "lucide-react"
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
        <Card className="h-14 w-48 border border-border bg-card text-card-foreground shadow-sm mx-2">
            <CardContent className="p-2 h-full flex flex-col justify-between">
                {/* Header Row: Stage Name + Status Icon - Reduced spacing */}
                <div className="flex items-center justify-between mb-1">
                    <h3 className="text-xs font-semibold overflow-hidden whitespace-nowrap text-ellipsis pr-1 flex-1">{stage.name}</h3>
                    <div className="flex-shrink-0">
                        <StatusIcon className={cn("w-3 h-3", statusConfigEntry.color)} />
                    </div>
                </div>

                {/* Combined Agent + Task Row - More compact */}
                <div className="flex items-center text-xs text-muted-foreground mb-1 min-h-0">
                    <User className="w-2 h-2 mr-1 flex-shrink-0" />
                    <span className="overflow-hidden whitespace-nowrap text-ellipsis flex-1">{stage.agentName}</span>
                </div>

                {/* Tasks Counter and Progress Bar - Simplified */}
                <div className="flex items-center justify-between">
                    <span className="text-xs">{completedTasks}/{totalTasks}</span>
                    <div className="flex items-center gap-1">
                        {stage.hitlRequired && (
                            <Badge variant="destructive" size="sm">
                                HITL
                            </Badge>
                        )}
                        <div className="w-8 bg-gray-200 rounded-full h-1">
                            <div
                                className="bg-blue-600 h-1 rounded-full" 
                                style={{ width: `${progress}%` }}
                            ></div>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}

export function ProcessSummary() {
  const stages = useProcessStore((state) => state.stages)
  const currentFlow = useProcessStore((state) => state.currentFlow)

  const renderSkeletons = () => (
    <div className="flex items-center justify-between">
        {[...Array(5)].map((_, i) => (
            <div key={`skeleton-${i}`} className="flex items-center">
                <Card className="h-14 w-48 border border-border bg-card shadow-sm mx-2">
                    <CardContent className="p-2 h-full flex flex-col justify-between">
                        <div className="space-y-1">
                            <Skeleton className="h-3 w-3/4" />
                            <Skeleton className="h-2 w-full" />
                            <Skeleton className="h-1 w-full" />
                        </div>
                    </CardContent>
                </Card>
                {i < 4 && <ChevronRight key={`arrow-${i}`} className="w-4 h-4 text-muted-foreground mx-1 flex-shrink-0" />}
            </div>
        ))}
    </div>
  )

  return (
    <Card className="border border-border bg-card text-card-foreground shadow-sm">
        <CardHeader className="pb-3">
            <CardTitle className="text-lg">Process Summary</CardTitle>
            <CardDescription>
                {currentFlow?.description || "No active process"}
            </CardDescription>
        </CardHeader>
        <CardContent className="pb-4">
            {stages.length === 0 ? (
                renderSkeletons()
            ) : (
                <div className="flex items-center justify-between">
                    {stages.map((stage, index) => (
                        <div key={`stage-${stage.id}-${index}`} className="flex items-center">
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