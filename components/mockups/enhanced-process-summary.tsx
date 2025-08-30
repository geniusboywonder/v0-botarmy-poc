"use client"

import React, { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  CheckCircle,
  Loader,
  Circle,
  ChevronRight,
  ChevronDown,
  AlertCircle,
  AlertTriangle,
  User,
  Database,
  FileCode,
  Component,
  Lock,
  Server,
} from "lucide-react"
import { cn } from "@/lib/utils"

const stageIcons = {
  done: <CheckCircle className="w-8 h-8 text-green-500" />,
  wip: <Loader className="w-8 h-8 text-blue-500 animate-spin" />,
  queued: <Circle className="w-8 h-8 text-gray-400" />,
}

const stagesData = [
  { id: "analyze", name: "Analyze", status: "done", agent: "Analyst", tasks: "5/5" },
  { id: "design", name: "Design", status: "wip", agent: "Architect", tasks: "2/4" },
  { id: "build", name: "Build", status: "queued", agent: "Developer", tasks: "0/8" },
  { id: "test", name: "Test", status: "queued", agent: "Tester", tasks: "0/4" },
  { id: "deploy", name: "Deploy", status: "queued", agent: "Deployer", tasks: "0/0" },
]

const designTasks = [
  { icon: <Database className="w-4 h-4" />, name: "Database schema", status: "wip" },
  { icon: <FileCode className="w-4 h-4" />, name: "API routes", status: "queued" },
  { icon: <Component className="w-4 h-4" />, name: "React components", status: "queued" },
  { icon: <Lock className="w-4 h-4" />, name: "Auth flow", status: "queued" },
]

const parallelDevOpsTask = {
  icon: <Server className="w-4 h-4" />,
  name: "DevOps",
  description: "Setting up environments",
  tasks: "2/3",
}

export function EnhancedProcessSummaryMockup() {
  const [isDesignExpanded, setIsDesignExpanded] = useState(false)

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle>Process Summary</CardTitle>
        <CardDescription>High-level view of workflow progress.</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col justify-between">
        <div>
          {/* High-level workflow progress */}
          <div className="mb-6">
            <div className="flex items-center justify-between px-4">
              {stagesData.map((stage, index) => (
                <React.Fragment key={stage.id}>
                  <div className="flex flex-col items-center space-y-1">
                    <div
                      className={cn(
                        "w-12 h-12 rounded-full flex items-center justify-center",
                        stage.status === "done" && "bg-green-100",
                        stage.status === "wip" && "bg-blue-100",
                        stage.status === "queued" && "bg-gray-100"
                      )}
                    >
                      {stageIcons[stage.status]}
                    </div>
                    <span className="text-xs font-medium">{stage.name}</span>
                  </div>
                  {index < stagesData.length - 1 && (
                    <ChevronRight className="w-6 h-6 text-muted-foreground -mt-4" />
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>

          {/* Current Stage Details */}
          <Card className="bg-muted/50">
            <CardContent className="p-4">
              <p className="text-sm">
                <span className="font-semibold">Current Stage:</span> Design (Architect reviewing requirements...)
              </p>
              <div className="flex items-center mt-2">
                <AlertCircle className="w-5 h-5 text-yellow-500 mr-2" />
                <p className="text-sm font-semibold text-yellow-600">
                  Action Required: Waiting for human approval
                </p>
                <Button size="sm" variant="outline" className="ml-4 h-7">
                  Review & Approve
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Expandable Card Section */}
          <div className="mt-6">
            <h4 className="text-sm font-semibold mb-2">Detailed View</h4>
            <div className="border rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <User className="w-4 h-4" />
                  <span className="font-semibold">Design Stage</span>
                  <Badge variant={isDesignExpanded ? "default" : "secondary"}>
                    {isDesignExpanded ? "Expanded" : "Collapsed"}
                  </Badge>
                </div>
                <Button variant="ghost" size="sm" onClick={() => setIsDesignExpanded(!isDesignExpanded)}>
                  {isDesignExpanded ? "Collapse" : "Expand"}
                  <ChevronDown
                    className={cn("w-4 h-4 ml-2 transition-transform", isDesignExpanded && "rotate-180")}
                  />
                </Button>
              </div>

              {isDesignExpanded && (
                <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Design Tasks */}
                  <div>
                    <h5 className="font-semibold mb-2 text-sm">Architect Tasks (2/4)</h5>
                    <ul className="space-y-2">
                      {designTasks.map(task => (
                        <li key={task.name} className="flex items-center space-x-2 text-sm">
                          {task.icon}
                          <span>{task.name}</span>
                          {task.status === "wip" && (
                            <Loader className="w-4 h-4 text-blue-500 animate-spin" />
                          )}
                        </li>
                      ))}
                    </ul>
                    <div className="mt-4 p-2 rounded-md bg-yellow-50 border border-yellow-200">
                      <p className="text-xs font-bold text-yellow-800">
                        <AlertTriangle className="w-4 h-4 inline-block mr-1" />
                        HITL REQUIRED: Approve DB Schema
                      </p>
                      <Button size="xs" variant="link" className="p-0 h-auto">Review Now</Button>
                    </div>
                  </div>

                  {/* Parallel DevOps Task */}
                  <div className="bg-muted/50 p-3 rounded-lg">
                    <h5 className="font-semibold mb-2 text-sm flex items-center">
                      <Badge variant="secondary" className="mr-2">Parallel Work</Badge>
                      {parallelDevOpsTask.name}
                    </h5>
                    <div className="flex items-center space-x-2 text-sm">
                      {parallelDevOpsTask.icon}
                      <span>{parallelDevOpsTask.description}</span>
                    </div>
                    <p className="text-xs mt-2">Tasks: {parallelDevOpsTask.tasks}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
