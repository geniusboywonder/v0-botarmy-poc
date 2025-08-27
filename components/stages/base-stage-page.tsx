"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, Pause, Play, User, Bot } from "lucide-react"
import dynamic from "next/dynamic"
import { Skeleton } from "@/components/ui/skeleton"

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
    <div className="p-4 md:p-8 space-y-6">
      {/* Stage Banner */}
      <Card>
        <CardHeader>
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <CardTitle className="text-2xl">{stageName} Stage</CardTitle>
              <CardDescription className="mt-1">
                Current Task: <span className="font-semibold text-foreground">{currentTask}</span>
              </CardDescription>
            </div>
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                    <Bot className="w-5 h-5" />
                    <span className="font-semibold">{agentName}</span>
                </div>
                {hitlRequired && (
                    <Badge variant="destructive" className="text-base p-2">
                        <AlertCircle className="w-5 h-5 mr-2" />
                        Action Required
                    </Badge>
                )}
                <Button variant="outline" onClick={onPause}><Pause className="w-4 h-4 mr-2" /> Pause</Button>
                <Button onClick={onResume}><Play className="w-4 h-4 mr-2" /> Resume</Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Main Content Tabs */}
      <Tabs defaultValue="progress" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="progress">Progress</TabsTrigger>
          <TabsTrigger value="config">Configuration</TabsTrigger>
        </TabsList>
        <TabsContent value="progress">
            <div className="grid md:grid-cols-2 gap-6 mt-6">
                <div className="md:col-span-1">
                    <TasksList tasks={tasks} />
                </div>
                <div className="md:col-span-1">
                    <ArtifactsList artifacts={artifacts} />
                </div>
            </div>
        </TabsContent>
        <TabsContent value="config">
            <div className="mt-6">
                <DynamicStageConfig />
            </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
