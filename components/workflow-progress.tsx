"use client"

import { useWorkflowStore } from "@/lib/stores/workflow-store"
import { Progress } from "@/components/ui/progress"
import { StepIndicator } from "./step-indicator"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"

export function WorkflowProgress() {
  const { progressPercentage, currentStep, steps } = useWorkflowStore()

  return (
    <Card>
      <CardHeader>
        <CardTitle>Workflow Progress</CardTitle>
        <CardDescription>
          Overall progress of the agent workflow. Current step:{" "}
          <span className="font-bold text-primary">{currentStep}</span>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <Progress value={progressPercentage} className="w-full transition-all duration-500" />
        </div>
        <StepIndicator steps={steps} currentStepName={currentStep} />
      </CardContent>
    </Card>
  )
}
