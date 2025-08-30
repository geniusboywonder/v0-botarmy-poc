"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { AlertTriangle, Bot, Clock } from "lucide-react"
import { EnhancedProcessSummaryMockup } from "@/components/mockups/enhanced-process-summary"

import { EnhancedChatInterfaceMockup } from "@/components/mockups/enhanced-chat-interface"

// The HITL Alert Bar component from the mockup
function HITLAlertBar() {
  return (
    <Card className="mb-6 bg-yellow-50 border-yellow-200">
      <CardHeader className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="w-6 h-6 text-yellow-600" />
            <div>
              <CardTitle className="text-base text-yellow-800">URGENT: Architecture Review Required</CardTitle>
              <CardDescription className="text-yellow-700">
                The Architect needs your approval on the database schema to proceed.
              </CardDescription>
            </div>
          </div>
          <div className="space-x-2">
            <Button variant="outline" size="sm">View Details</Button>
            <Button size="sm">Quick Approve</Button>
          </div>
        </div>
      </CardHeader>
    </Card>
  )
}

// The Recent Activities component from the mockup
function RecentActivities() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Activities</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-3">
          <li className="flex items-center space-x-3">
            <Clock className="w-4 h-4 text-muted-foreground" />
            <p className="text-sm">
              <span className="font-semibold">Analyst</span> completed requirements analysis.
              <span className="text-xs text-muted-foreground ml-2">14:32</span>
            </p>
          </li>
          <li className="flex items-center space-x-3">
            <Clock className="w-4 h-4 text-muted-foreground" />
            <p className="text-sm">
              <span className="font-semibold">Human</span> approved user story priorities.
              <span className="text-xs text-muted-foreground ml-2">14:30</span>
            </p>
          </li>
          <li className="flex items-center space-x-3">
            <Clock className="w-4 h-4 text-muted-foreground" />
            <p className="text-sm">
              User started new project: <span className="font-semibold">Todo Application</span>.
              <span className="text-xs text-muted-foreground ml-2">14:25</span>
            </p>
          </li>
        </ul>
      </CardContent>
    </Card>
  )
}


export default function DashboardMockupPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Redesigned Dashboard</h1>
        <p className="text-muted-foreground">
          A mockup of the new dashboard layout with improved information hierarchy.
        </p>
      </div>

      {/* 1. HITL Alert Bar */}
      <HITLAlertBar />

      {/* 2. Above the fold: Process Summary and Chat Interface */}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="min-h-[400px]">
          <EnhancedProcessSummaryMockup />
        </div>
        <div className="min-h-[400px]">
          <EnhancedChatInterfaceMockup />
        </div>
      </div>

      {/* 3. Below the fold: Recent Activities */}
      <div className="mt-6">
        <RecentActivities />
      </div>
    </div>
  )
}
