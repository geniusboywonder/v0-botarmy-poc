"use client"

import { Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface LoadingStateProps {
  message: string
  className?: string
}

export function LoadingState({ message, className }: LoadingStateProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center gap-4 p-8 text-muted-foreground", className)}>
      <Loader2 className="w-8 h-8 animate-spin" />
      <p className="text-sm text-center">{message}</p>
    </div>
  )
}
