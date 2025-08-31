"use client"

import React, { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
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
  ClipboardCheck,
  DraftingCompass,
  Construction,
  TestTube2,
  Rocket,
  Clock,
  Play,
} from "lucide-react"
import { cn } from "@/lib/utils"

// --- Role-based Icon Mapping ---
const getRoleIcon = (agent: string, sizeAndColor = "w-6 h-6") => {
  const agentLower = agent.toLowerCase()
  if (agentLower.includes('analyst')) return <ClipboardCheck className={sizeAndColor.includes('text-white') ? sizeAndColor : `${sizeAndColor} text-analyst`} />
  if (agentLower.includes('architect')) return <DraftingCompass className={sizeAndColor.includes('text-white') ? sizeAndColor : `${sizeAndColor} text-architect`} />
  if (agentLower.includes('developer')) return <Construction className={sizeAndColor.includes('text-white') ? sizeAndColor : `${sizeAndColor} text-developer`} />
  if (agentLower.includes('tester')) return <TestTube2 className={sizeAndColor.includes('text-white') ? sizeAndColor : `${sizeAndColor} text-tester`} />
  if (agentLower.includes('deployer')) return <Rocket className={sizeAndColor.includes('text-white') ? sizeAndColor : `${sizeAndColor} text-deployer`} />
  return <User className={sizeAndColor.includes('text-white') ? sizeAndColor : `${sizeAndColor} text-muted-foreground`} /> // Default
}

// --- Status Overlay Icon ---
const getStatusIcon = (status: string, size = "w-3 h-3") => {
  switch (status) {
    case 'done':
      return <CheckCircle className={`${size} text-white`} />
    case 'wip':
      return <Play className={`${size} text-white`} />
    case 'queued':
      return <Clock className={`${size} text-white`} />
    case 'waiting':
      return <AlertTriangle className={`${size} text-white`} />
    default:
      return <Circle className={`${size} text-white`} />
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'done': return 'bg-tester'
    case 'wip': return 'bg-analyst' 
    case 'queued': return 'bg-muted'
    case 'waiting': return 'bg-amber'
    default: return 'bg-muted'
  }
}

const stageIcons = {
  done: <CheckCircle className="w-8 h-8 text-tester" />,
  wip: <Loader className="w-8 h-8 text-analyst animate-spin" />,
  queued: <Circle className="w-8 h-8 text-muted" />,
}

const stagesData = [
  { 
    id: "analyze", 
    name: "Analyze", 
    status: "done", 
    agent: "Analyst", 
    tasks: "5/5",
    artifacts: [
      { name: "Requirements Doc", status: "done", role: "Analyst", task: "Requirements gathering" },
      { name: "User Stories", status: "done", role: "Analyst", task: "Story creation" },
      { name: "Acceptance Criteria", status: "done", role: "Analyst", task: "Criteria definition" }
    ]
  },
  { 
    id: "design", 
    name: "Design", 
    status: "wip", 
    agent: "Architect", 
    tasks: "2/4",
    artifacts: [
      { name: "Database Schema", status: "wip", role: "Architect", task: "Schema design" },
      { name: "API Specification", status: "queued", role: "Architect", task: "API planning" },
      { name: "System Architecture", status: "queued", role: "Architect", task: "Architecture design" }
    ]
  },
  { 
    id: "build", 
    name: "Build", 
    status: "queued", 
    agent: "Developer", 
    tasks: "0/8",
    artifacts: [
      { name: "Frontend Components", status: "queued", role: "Developer", task: "UI development" },
      { name: "Backend API", status: "queued", role: "Developer", task: "API implementation" },
      { name: "Database Setup", status: "queued", role: "Developer", task: "DB implementation" }
    ]
  },
  { 
    id: "test", 
    name: "Test", 
    status: "queued", 
    agent: "Tester", 
    tasks: "0/4",
    artifacts: [
      { name: "Unit Tests", status: "queued", role: "Tester", task: "Unit testing" },
      { name: "Integration Tests", status: "queued", role: "Tester", task: "Integration testing" }
    ]
  },
  { 
    id: "deploy", 
    name: "Deploy", 
    status: "queued", 
    agent: "Deployer", 
    tasks: "0/2",
    artifacts: [
      { name: "Production Config", status: "queued", role: "Deployer", task: "Environment setup" },
      { name: "CI/CD Pipeline", status: "queued", role: "Deployer", task: "Pipeline creation" }
    ]
  },
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
  const [selectedStage, setSelectedStage] = useState("design") // Default to current active stage
  const [expandedArtifacts, setExpandedArtifacts] = useState<string[]>([])
  
  const currentStage = stagesData.find(stage => stage.id === selectedStage)
  const progressPercentage = currentStage ? (parseInt(currentStage.tasks.split('/')[0]) / parseInt(currentStage.tasks.split('/')[1])) * 100 : 0

  const toggleArtifact = (artifactName: string) => {
    setExpandedArtifacts(prev => 
      prev.includes(artifactName) 
        ? prev.filter(name => name !== artifactName)
        : [...prev, artifactName]
    )
  }

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-bold">Process Summary</CardTitle>
        <CardDescription className="text-sm">Workflow progress overview</CardDescription>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col space-y-4">
        {/* Compact Stage Icons */}
        <div className="flex items-center justify-between gap-1 px-2">
          {stagesData.map((stage, index) => (
            <React.Fragment key={stage.id}>
              <button
                onClick={() => setSelectedStage(stage.id)}
                className={cn(
                  "flex flex-col items-center space-y-1 p-2 rounded-lg transition-all flex-1",
                  selectedStage === stage.id 
                    ? "bg-teal ring-2 ring-teal/60 text-white" 
                    : "hover:bg-secondary"
                )}
              >
                <div className="relative w-full flex justify-center">
                  <div className={cn(
                    "w-12 h-12 rounded-full flex items-center justify-center",
                    selectedStage === stage.id
                      ? "bg-teal/80"
                      : stage.status === "done" && "bg-tester/10",
                    selectedStage === stage.id
                      ? "bg-teal/80"
                      : stage.status === "wip" && "bg-analyst/10", 
                    selectedStage === stage.id
                      ? "bg-teal/80"
                      : stage.status === "queued" && "bg-secondary"
                  )}>
                    {selectedStage === stage.id 
                      ? getRoleIcon(stage.agent, "w-6 h-6 text-white") 
                      : getRoleIcon(stage.agent, "w-6 h-6")
                    }
                    {/* Status overlay - top right */}
                    <div className={cn(
                      "absolute top-0 right-2 w-5 h-5 rounded-full flex items-center justify-center border-2 border-white",
                      getStatusColor(stage.status)
                    )}>
                      {getStatusIcon(stage.status, "w-3 h-3")}
                    </div>
                  </div>
                </div>
                <span className={cn(
                  "text-xs font-medium text-center",
                  selectedStage === stage.id ? "text-white" : "text-gray-700"
                )}>{stage.name}</span>
              </button>
              {index < stagesData.length - 1 && (
                <ChevronRight className="w-4 h-4 text-muted-foreground flex-shrink-0" />
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Always Expanded Detailed View */}
        <div className="border rounded-lg p-3 flex-1">
          {currentStage && (
            <div className="space-y-3">
              {/* Stage Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {getRoleIcon(currentStage.agent, "w-5 h-5")}
                  <h3 className="font-semibold">{currentStage.name} Stage</h3>
                  <Badge variant={currentStage.status === "wip" ? "default" : "secondary"}>
                    {currentStage.status.toUpperCase()}
                  </Badge>
                </div>
              </div>

              {/* Task Summary */}
              <div className="space-y-2 pb-3 border-b">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium">Progress: {currentStage.tasks}</span>
                  <span className="text-muted-foreground">{Math.round(progressPercentage)}%</span>
                </div>
                <Progress value={progressPercentage} className="h-2" />
              </div>

              {/* Artifacts Section - Separated */}
              <div className="pt-3">
                <div className="space-y-2">
                  <h4 className="text-sm font-semibold border-l-4 border-teal pl-2">Stage Artifacts</h4>
                  <div className="space-y-1 bg-secondary rounded-lg p-3 border">
                    {currentStage.artifacts.map((artifact) => (
                      <div key={artifact.name} className="bg-card border border-border rounded p-3 shadow-sm">
                        <button 
                          onClick={() => toggleArtifact(artifact.name)}
                          className="w-full flex items-center justify-between text-left"
                        >
                          <div className="flex items-center space-x-2">
                            <div className={cn(
                              "w-3 h-3 rounded-full flex items-center justify-center",
                              getStatusColor(artifact.status)
                            )}>
                              {getStatusIcon(artifact.status, "w-2 h-2")}
                            </div>
                            <span className="text-sm font-medium text-foreground">{artifact.name}</span>
                            <Badge variant="outline" className="text-xs text-muted-foreground border-border">
                              {artifact.status}
                            </Badge>
                          </div>
                          <ChevronDown 
                            className={cn(
                              "w-4 h-4 transition-transform text-muted-foreground",
                              expandedArtifacts.includes(artifact.name) && "rotate-180"
                            )} 
                          />
                        </button>
                        
                        {expandedArtifacts.includes(artifact.name) && (
                          <div className="mt-2 pl-5 border-l-2 border-border">
                            <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                              {getRoleIcon(artifact.role, "w-3 h-3")}
                              <span><strong>{artifact.role}:</strong> {artifact.task}</span>
                              <div className={cn(
                                "w-2 h-2 rounded-full",
                                getStatusColor(artifact.status)
                              )} />
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}