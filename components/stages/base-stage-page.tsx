"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, Pause, Play, User, Bot } from "lucide-react"
import dynamic from "next/dynamic"
import { Skeleton } from "@/components/ui/skeleton"
import { MainLayout } from "@/components/main-layout"

import { ArtifactsList } from "./artifacts-list"
import type { Artifact } from "@/lib/types"
import { TasksList } from "./tasks-list"
import type { Task } from "@/lib/types"

const DynamicStageConfig = dynamic(() => import("./stage-config").then(mod => mod.StageConfig), {
    loading: () => <Skeleton className="w-full h-[400px]" />,
    ssr: false
})


export interface BaseStagePageProps {
  stageName: string
  currentTask: string
  agentName: string
  hitlRequired: boolean
  artifacts?: Artifact[]
  tasks?: Task[]
  onPause?: () => void
  onResume?: () => void
}

export function BaseStagePage({
  stageName,
  currentTask,
  agentName,
  hitlRequired,
  artifacts,
  tasks,
  onPause,
  onResume,
}: BaseStagePageProps) {
  return (
    <MainLayout>
      <div className="p-4 md:p-8 space-y-6">
        {/* Stage Banner */}
        <Card>
          <CardHeader>
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <CardTitle className="text-2xl">{stageName} Stage</CardTitle>
                <CardDescription className="mt-2">
                  Current task: {currentTask}
                </CardDescription>
              </div>
              <div className="flex items-center gap-2">
                {hitlRequired && (
                  <Badge variant="destructive" className="flex items-center gap-1">
                    <AlertCircle className="w-3 h-3" />
                    Human-in-the-Loop Required
                  </Badge>
                )}
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" onClick={onResume}>
                    <Play className="w-4 h-4 mr-2" />
                    Resume
                  </Button>
                  <Button variant="secondary" size="sm" onClick={onPause}>
                    <Pause className="w-4 h-4 mr-2" />
                    Pause
                  </Button>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-4 mt-4">
              <div className="flex items-center gap-2">
                <User className="w-4 h-4 text-muted-foreground" />
                <span className="text-sm">Agent: {agentName}</span>
              </div>
              <div className="flex items-center gap-2">
                <Bot className="w-4 h-4 text-muted-foreground" />
                <span className="text-sm text-green-600">Active</span>
              </div>
            </div>
          </CardHeader>
        </Card>

        {/* Main Content Tabs */}
        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="tasks">Tasks</TabsTrigger>
            <TabsTrigger value="artifacts">Artifacts</TabsTrigger>
            <TabsTrigger value="config">Configuration</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div>
              <Card>
                <CardHeader>
                  <CardTitle>Stage Overview</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <h4 className="font-semibold mb-2">Current Status</h4>
                      <p className="text-sm text-muted-foreground">{currentTask}</p>
                    </div>
                    <div>
                      <h4 className="font-semibold mb-2">Assigned Agent</h4>
                      <p className="text-sm text-muted-foreground">{agentName}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="tasks">
            {tasks ? <TasksList tasks={tasks} /> : <div>No tasks available.</div>}
          </TabsContent>

          <TabsContent value="artifacts">
            {artifacts ? <ArtifactsList artifacts={artifacts} /> : <div>No artifacts available.</div>}
          </TabsContent>

          <TabsContent value="config">
            <DynamicStageConfig stageName={stageName} />
          </TabsContent>
        </Tabs>
      </div>
    </MainLayout>
  )
}
