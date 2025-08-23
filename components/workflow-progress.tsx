"use client"

import { useWorkflowStore } from "@/lib/stores/workflow-store"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { StepIndicator } from "./step-indicator"

type StepStatus = "completed" | "active" | "pending"

const AGENT_STEPS = ["Analyst", "Architect", "Developer", "Tester", "Deployer"]

export function WorkflowProgress() {
  const { currentStepIndex, overallProgress, currentTask } = useWorkflowStore();

  const steps = AGENT_STEPS.map((name, index) => {
    let status: StepStatus = "pending"
    if (index < currentStepIndex) {
      status = "completed"
    } else if (index === currentStepIndex) {
      status = "active"
    }
    return { name, status }
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle>Workflow Progress</CardTitle>
        <CardDescription>
          {currentTask}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="flex justify-between mb-1">
            <span className="text-sm font-medium">Overall Progress</span>
            <span className="text-sm font-medium">{Math.round(overallProgress)}%</span>
          </div>
          <Progress value={overallProgress} />
        </div>
        <StepIndicator steps={steps} />
      </CardContent>
    </Card>
  )
}
