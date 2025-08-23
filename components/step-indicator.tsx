"use client"

import { cn } from "@/lib/utils"
import { Check, Loader, Circle } from "lucide-react"

type StepStatus = "completed" | "active" | "pending"

interface StepProps {
  status: StepStatus
  children: React.ReactNode
}

function Step({ status, children }: StepProps) {
  const getStatusIcon = () => {
    switch (status) {
      case "completed":
        return <Check className="h-5 w-5 text-green-500" />
      case "active":
        return <Loader className="h-5 w-5 animate-spin text-blue-500" />
      case "pending":
        return <Circle className="h-5 w-5 text-gray-400" />
    }
  }

  return (
    <div className="flex items-center space-x-2">
      <div className="flex-shrink-0">{getStatusIcon()}</div>
      <span
        className={cn(
          "text-sm font-medium",
          status === "completed" && "text-green-600",
          status === "active" && "text-blue-600",
          status === "pending" && "text-gray-500"
        )}
      >
        {children}
      </span>
    </div>
  )
}

interface StepIndicatorProps {
  steps: { name: string; status: StepStatus }[]
}

export function StepIndicator({ steps }: StepIndicatorProps) {
  return (
    <div className="flex items-center justify-between space-x-4">
      {steps.map((step, index) => (
        <>
          <Step key={step.name} status={step.status}>
            {step.name}
          </Step>
          {index < steps.length - 1 && (
            <div className="flex-1 h-px bg-gray-300" />
          )}
        </>
      ))}
    </div>
  )
}
