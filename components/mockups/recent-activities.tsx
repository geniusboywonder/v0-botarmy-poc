"use client"

import React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  CheckCircle,
  Clock,
  User,
  AlertTriangle,
  ClipboardCheck,
  DraftingCompass,
  Construction,
  TestTube2,
  Rocket,
} from "lucide-react"
import { cn } from "@/lib/utils"

const getRoleIcon = (role: string, size = "w-4 h-4") => {
  const roleLower = role.toLowerCase()
  if (roleLower.includes('analyst')) return <ClipboardCheck className={`${size} text-blue-500`} />
  if (roleLower.includes('architect')) return <DraftingCompass className={`${size} text-purple-500`} />
  if (roleLower.includes('developer')) return <Construction className={`${size} text-orange-500`} />
  if (roleLower.includes('tester')) return <TestTube2 className={`${size} text-green-500`} />
  if (roleLower.includes('deployer')) return <Rocket className={`${size} text-red-500`} />
  if (roleLower === 'human' || roleLower === 'user') return <User className={`${size} text-indigo-500`} />
  return <CheckCircle className={`${size} text-gray-500`} />
}

const getActivityIcon = (type: string) => {
  switch (type) {
    case 'completed': return <CheckCircle className="w-3 h-3 text-green-500" />
    case 'approved': return <CheckCircle className="w-3 h-3 text-blue-500" />
    case 'waiting': return <Clock className="w-3 h-3 text-amber-500" />
    case 'alert': return <AlertTriangle className="w-3 h-3 text-orange-500" />
    default: return <Clock className="w-3 h-3 text-gray-400" />
  }
}

const recentActivities = [
  { 
    id: "1", 
    time: "14:32", 
    actor: "Analyst", 
    action: "completed requirements analysis", 
    type: "completed" 
  },
  { 
    id: "2", 
    time: "14:30", 
    actor: "Human", 
    action: "approved database schema design", 
    type: "approved" 
  },
  { 
    id: "3", 
    time: "14:28", 
    actor: "Architect", 
    action: "submitted database schema for review", 
    type: "completed" 
  },
  { 
    id: "4", 
    time: "14:25", 
    actor: "Architect", 
    action: "started database schema design", 
    type: "completed" 
  },
  { 
    id: "5", 
    time: "14:22", 
    actor: "System", 
    action: "workflow initiated with 5 agents", 
    type: "completed" 
  },
  { 
    id: "6", 
    time: "14:20", 
    actor: "Developer", 
    action: "initialized project structure", 
    type: "completed" 
  },
  { 
    id: "7", 
    time: "14:18", 
    actor: "Tester", 
    action: "prepared testing environment", 
    type: "completed" 
  },
  { 
    id: "8", 
    time: "14:15", 
    actor: "Deployer", 
    action: "configured deployment pipeline", 
    type: "completed" 
  }
]

export function RecentActivities() {
  return (
    <Card className="h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold">Recent Activities</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-20">
          <div className="px-6 pb-4 space-y-3">
            {recentActivities.map((activity, index) => (
              <div key={activity.id} className={cn(
                "flex items-start space-x-3",
                index >= 3 && "opacity-75 scale-95" // Make older activities slightly less prominent
              )}>
                {/* Timeline dot */}
                <div className="flex flex-col items-center">
                  <div className={cn(
                    "flex items-center justify-center rounded-full border-2 border-white ring-1 ring-gray-200",
                    index < 3 ? "w-6 h-6 bg-gray-100" : "w-5 h-5 bg-gray-50" // First 3 are larger
                  )}>
                    {getActivityIcon(activity.type)}
                  </div>
                  {index < recentActivities.length - 1 && (
                    <div className="w-px h-6 bg-gray-200 mt-1" />
                  )}
                </div>
                
                {/* Activity content */}
                <div className="flex-1 min-w-0 space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-gray-500 font-mono">
                      {activity.time}
                    </span>
                    <div className="flex items-center space-x-1">
                      {getRoleIcon(activity.actor, "w-3 h-3")}
                      <span className={cn(
                        "font-semibold text-gray-800",
                        index < 3 ? "text-sm" : "text-xs" // First 3 are larger text
                      )}>
                        {activity.actor}
                      </span>
                    </div>
                    <Badge 
                      variant="outline" 
                      className={cn(
                        "text-xs",
                        activity.type === "completed" && "border-green-200 text-green-700",
                        activity.type === "approved" && "border-blue-200 text-blue-700", 
                        activity.type === "waiting" && "border-amber-200 text-amber-700",
                        activity.type === "alert" && "border-orange-200 text-orange-700"
                      )}
                    >
                      {activity.type}
                    </Badge>
                  </div>
                  <p className={cn(
                    "text-gray-700 leading-relaxed font-medium",
                    index < 3 ? "text-sm" : "text-xs" // First 3 are larger text
                  )}>
                    {activity.action}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}