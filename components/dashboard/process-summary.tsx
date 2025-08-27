
---SAVE FILE: process_summary_WIP_20241218_104500.tsx---

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
        <Card className="flex-1 min-w-0 h-48"> {/* Changed: flex-1 for equal width distribution, fixed height h-48 (192px) */}
            <CardHeader className="pb-2"> {/* Changed: Reduced padding bottom */}
                <div className="flex items-center justify-between">
                    <CardTitle className="text-base truncate">{stage.name}</CardTitle> {/* Changed: text-base instead of text-lg, added truncate */}
                    <StatusIcon className={cn("w-5 h-5 flex-shrink-0", statusConfigEntry.color)} /> {/* Changed: w-5 h-5 instead of w-6 h-6, added flex-shrink-0 */}
                </div>
                <CardDescription className="text-xs">{statusConfigEntry.label}</CardDescription> {/* Changed: text-xs instead of default */}
            </CardHeader>
            <CardContent className="space-y-2 pt-0"> {/* Changed: space-y-2 instead of space-y-3, pt-0 for tighter spacing */}
                <div className="flex items-center text-xs"> {/* Changed: text-xs instead of text-sm */}
                    <User className="w-3 h-3 mr-1 flex-shrink-0" /> {/* Changed: w-3 h-3 instead of w-4 h-4, mr-1 instead of mr-2 */}
                    <span className="truncate">{stage.agentName}</span> {/* Added truncate */}
                </div>
                <p className="text-xs text-muted-foreground truncate" title={stage.currentTask}> {/* Changed: text-xs instead of text-sm */}
                    {stage.currentTask}
                </p>
                <div>
                    <p className="text-xs">Tasks: {completedTasks} / {totalTasks}</p> {/* Changed: text-xs instead of text-sm */}
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-1"> {/* Changed: h-2 instead of h-2.5 */}
                        <div
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${progress}%` }}
                        ></div>
                    </div>
                </div>
                {stage.hitlRequired && (
                    <Badge variant="destructive" className="flex items-center gap-1 text-xs"> {/* Added text-xs */}
                        <AlertCircle className="w-3 h-3" /> {/* Changed: w-3 h-3 instead of w-3 h-3 */}
                        HITL Required
                    </Badge>
                )}
                <div className="flex gap-1 pt-1"> {/* Changed: gap-1 instead of gap-2, pt-1 instead of pt-2 */}
                    <Button size="sm" variant="outline" className="flex-1 text-xs h-7"> {/* Changed: Added flex-1, text-xs, h-7 for smaller height */}
                        <Play className="w-3 h-3 mr-1" /> {/* Changed: w-3 h-3 instead of w-4 h-4, mr-1 instead of mr-2 */}
                        Resume
                    </Button>
                     <Button size="sm" variant="destructive" className="flex-1 text-xs h-7"> {/* Changed: Added flex-1, text-xs, h-7 */}
                        <PauseCircle className="w-3 h-3 mr-1" /> {/* Changed: w-3 h-3 instead of w-4 h-4, mr-1 instead of mr-2 */}
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
    <div className="flex items-center space-x-3"> {/* Changed: space-x-3 instead of space-x-4 */}
        {[...Array(5)].map((_, i) => (
            <div key={`skeleton-${i}`} className="flex items-center flex-1"> {/* Added flex-1 */}
                <Card className="flex-1 h-48"> {/* Changed: flex-1 instead of w-64, h-48 for fixed height */}
                    <CardHeader className="pb-2"> {/* Added pb-2 for consistent spacing */}
                        <Skeleton className="h-5 w-3/4" /> {/* Changed: h-5 instead of h-6 */}
                        <Skeleton className="h-3 w-1/2" /> {/* Changed: h-3 instead of h-4 */}
                    </CardHeader>
                    <CardContent className="space-y-2 pt-0"> {/* Changed: space-y-2, pt-0 */}
                        <Skeleton className="h-3 w-full" /> {/* Changed: h-3 instead of h-4 */}
                        <Skeleton className="h-3 w-full" />
                        <Skeleton className="h-6 w-full" /> {/* Changed: h-6 instead of h-8 */}
                    </CardContent>
                </Card>
                {i < 4 && <ChevronRight key={`arrow-${i}`} className="w-6 h-6 text-muted-foreground mx-2 flex-shrink-0" />} {/* Added mx-2, flex-shrink-0 */}
            </div>
        ))}
    </div>
  )

  return (
    <Card>
        <CardHeader>
            <CardTitle>Process Summary</CardTitle>
            <CardDescription>
                Overview of the entire SDLC process stages.
            </CardDescription>
        </CardHeader>
        <CardContent>
            <div className="pb-4"> {/* Removed flex wrapper to allow proper flex behavior inside */}
                {stages.length === 0 ? (
                    renderSkeletons()
                ) : (
                    <div className="flex items-center space-x-3"> {/* Changed: space-x-3 instead of space-x-4 */}
                        {stages.map((stage, index) => (
                            <div key={`stage-${stage.id}-${index}`} className="flex items-center flex-1"> {/* Added flex-1 */}
                                <StageCard stage={stage} />
                                {index < stages.length - 1 && (
                                    <ChevronRight key={`stage-arrow-${stage.id}-${index}`} className="w-6 h-6 text-muted-foreground mx-2 flex-shrink-0" /> {/* Added mx-2, flex-shrink-0 */}
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </CardContent>
    </Card>
  )
}
