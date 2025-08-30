"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  LayoutDashboard,
  FileText,
  Settings,
  Bot,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  DraftingCompass,
  Construction,
  TestTube2,
  Rocket,
  AlertCircle,
  CheckCircle,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { SystemHealthIndicator } from "@/components/system-health-indicator"

const enhancedNavigation = [
  { name: 'Dashboard', path: '/bot-army-ux-review/dashboard', icon: LayoutDashboard },
  { name: 'Analyze', path: '#', icon: ClipboardCheck, alerts: { ready: 3 } },
  { name: 'Design', path: '#', icon: DraftingCompass, alerts: { hitl: 2 } },
  { name: 'Build', path: '#', icon: Construction, alerts: { error: 1 } },
  { name: 'Validate', path: '#', icon: TestTube2 },
  { name: 'Launch', path: '#', icon: Rocket },
  { name: 'Logs', path: '#', icon: FileText },
  { name: 'Settings', path: '#', icon: Settings },
]

const AlertBadge = ({ alerts }) => {
  if (!alerts) return null
  if (alerts.hitl) {
    return <Badge className="bg-yellow-500 hover:bg-yellow-600">{alerts.hitl} HITL</Badge>
  }
  if (alerts.error) {
    return <Badge variant="destructive">{alerts.error} Error</Badge>
  }
  if (alerts.ready) {
    return <Badge className="bg-green-500 hover:bg-green-600">{alerts.ready} Ready</Badge>
  }
  return null
}

export function EnhancedSidebarMockup() {
  const [isCollapsed, setIsCollapsed] = useState(false)

  return (
    <div
      className={cn(
        "flex flex-col bg-card border-r border-border transition-all duration-300",
        isCollapsed ? "w-16" : "w-64",
      )}
    >
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-8 h-8 bg-primary rounded-lg">
                <Bot className="w-5 h-5 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-foreground">BotArmy</h1>
                <p className="text-xs text-muted-foreground">UX Mockups</p>
              </div>
            </div>
          )}
          <Button variant="ghost" size="sm" onClick={() => setIsCollapsed(!isCollapsed)} className="h-8 w-8 p-0">
            {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </Button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-2 flex-1">
        <div className="space-y-1">
          {enhancedNavigation.map((item) => {
            const Icon = item.icon
            // A simple way to determine active state for the mockup
            const isActive = item.name === 'Dashboard'

            return (
              <Link key={item.name} href={item.path}>
                <Button
                  variant={isActive ? "secondary" : "ghost"}
                  className={cn(
                    "w-full justify-start h-10 relative",
                    isCollapsed ? "px-2" : "px-3",
                    isActive && "bg-primary/10 text-primary hover:bg-primary/20",
                  )}
                >
                  <Icon className={cn("w-4 h-4", !isCollapsed && "mr-3")} />
                  {!isCollapsed && <span>{item.name}</span>}
                  {!isCollapsed && item.alerts && (
                    <div className="absolute right-2 top-1/2 -translate-y-1/2">
                      <AlertBadge alerts={item.alerts} />
                    </div>
                  )}
                </Button>
              </Link>
            )
          })}
        </div>
      </nav>

      {/* System Health Section */}
      <div className="p-4 border-t border-border">
        {!isCollapsed && (
           <div className="space-y-2">
             <h4 className="text-sm font-semibold">System Health</h4>
             <SystemHealthIndicator />
           </div>
        )}
      </div>
    </div>
  )
}
