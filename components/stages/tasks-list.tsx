"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, AlertCircle, Loader, User } from "lucide-react"
import { cn } from "@/lib/utils"
import type { Task } from "@/lib/types"

const mockTasks: Task[] = [
    { id: 'task-01', description: 'Analyze user requirements from prompt', agent: 'Analyst', status: 'done', timestamp: '10:05 AM', hitl: false },
    { id: 'task-02', description: 'Generate System Requirements Specification', agent: 'Analyst', status: 'done', timestamp: '10:30 AM', hitl: false },
    { id: 'task-03', description: 'Create use case diagrams', agent: 'Analyst', status: 'wip', timestamp: '11:15 AM', hitl: true },
    { id: 'task-04', description: 'Perform risk analysis', agent: 'Analyst', status: 'queued', timestamp: '11:20 AM', hitl: false },
]

const statusConfig = {
    done: { icon: CheckCircle, color: "text-green-500" },
    wip: { icon: Loader, color: "text-blue-500 animate-spin" },
    queued: { icon: AlertCircle, color: "text-gray-500" },
}

export function TasksList({ tasks = mockTasks }: { tasks?: Task[] }) {
  return (
    <Card>
        <CardHeader>
            <CardTitle>Tasks</CardTitle>
            <CardDescription>
                A chronological list of tasks performed in this stage.
            </CardDescription>
        </CardHeader>
        <CardContent>
            <div className="space-y-4">
                {tasks && tasks.length > 0 ? (
                    tasks.map((task) => {
                        const StatusIcon = statusConfig[task.status].icon
                        return (
                            <div key={task.id} className={cn("flex items-start gap-4 p-3 rounded-lg border", task.hitl && "border-yellow-500 bg-yellow-50")}>
                                <StatusIcon className={cn("w-5 h-5 mt-1", statusConfig[task.status].color)} />
                                <div className="flex-1">
                                    <p className="font-medium">{task.description}</p>
                                    <div className="text-sm text-muted-foreground flex items-center gap-4 mt-1">
                                        <div className="flex items-center gap-1">
                                            <User className="w-3 h-3" />
                                            <span>{task.agent}</span>
                                        </div>
                                        <span>{task.timestamp}</span>
                                        {task.hitl && <Badge variant="destructive">HITL</Badge>}
                                    </div>
                                </div>
                            </div>
                        )
                    })
                ) : (
                    <div className="text-center text-muted-foreground py-8">
                        <p>No tasks for this stage yet.</p>
                    </div>
                )}
            </div>
        </CardContent>
    </Card>
  )
}
