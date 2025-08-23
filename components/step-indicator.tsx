"use client"

import { cn } from "@/lib/utils"
import { Check, Loader2, AlertTriangle, SkipForward } from "lucide-react"
import { WorkflowStep } from "@/lib/stores/workflow-store"

interface StepIndicatorProps {
  steps: WorkflowStep[];
  currentStepName: string;
}

const statusIcons = {
  pending: <div className="w-3 h-3 rounded-full bg-gray-300" />,
  active: <Loader2 className="w-4 h-4 animate-spin text-blue-500" />,
  completed: <Check className="w-4 h-4 text-green-500" />,
  error: <AlertTriangle className="w-4 h-4 text-red-500" />,
  skipped: <SkipForward className="w-4 h-4 text-gray-500" />,
}

export function StepIndicator({ steps, currentStepName }: StepIndicatorProps) {
  return (
    <div className="flex items-center justify-between w-full">
      {steps.map((step, index) => (
        <>
          <div key={step.name} className="flex flex-col items-center">
            <div
              className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center border-2",
                step.status === "active" && "border-blue-500",
                step.status === "completed" && "border-green-500",
                step.status === "error" && "border-red-500",
                step.status === "skipped" && "border-gray-500",
                step.status === "pending" && "border-gray-300"
              )}
            >
              {statusIcons[step.status]}
            </div>
            <p className="text-xs mt-2 text-center">{step.name}</p>
          </div>
          {index < steps.length - 1 && (
            <div className="flex-1 h-0.5 bg-gray-200 mx-2" />
          )}
        </>
      ))}
    </div>
  )
}
