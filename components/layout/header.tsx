"use client"

import { useState } from "react"
import Link from "next/link"
import {
  Bell,
  MessageSquare,
  Search,
  User as UserIcon,
  Bot,
  AlertTriangle,
  X,
  ChevronDown,
} from "lucide-react"
import { useNotificationStore } from "@/lib/stores/notification-store"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { SystemHealthIndicator } from "@/components/system-health-indicator"
import { GlobalChatModal } from "@/components/chat/global-chat-modal"

export function Header() {
    const [isChatOpen, setIsChatOpen] = useState(false)
    const { alerts, dismissAlert } = useNotificationStore()
    const [expandedAlerts, setExpandedAlerts] = useState<string[]>([])

    const visibleAlerts = alerts.slice(0, 2)

    const toggleExpanded = (alertId: string) => {
      setExpandedAlerts(prev => 
        prev.includes(alertId) 
          ? prev.filter(id => id !== alertId)
          : [...prev, alertId]
      )
    }

  return (
    <>
        <header className="bg-card border-b">
          {/* Main Header */}
          <div className="flex h-14 items-center px-6">
        
        {/* Site Title / Logo - Fixed width */}
        <div className="flex items-center gap-2 flex-shrink-0 w-32">
            <Link href="/" className="flex items-center gap-2">
                <Bot className="h-6 w-6 flex-shrink-0" />
                <span className="text-lg font-semibold hidden md:block whitespace-nowrap">BotArmy</span>
            </Link>
        </div>

        {/* Search Bar - Center with fixed width */}
        <div className="flex-1 px-8 max-w-lg mx-auto">
            <div className="relative w-full">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground flex-shrink-0" />
                <Input
                    type="search"
                    placeholder="Search tasks, artifacts..."
                    className="pl-10 text-sm w-full"
                />
            </div>
        </div>

        {/* Actions - Right Side with better spacing and fixed overlapping */}
        <div className="flex items-center gap-2 flex-shrink-0 min-w-0">
            {/* Chat Button */}
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={() => setIsChatOpen(true)}
              className="flex-shrink-0"
              title="Open Chat"
            >
                <MessageSquare className="h-5 w-5" />
                <span className="sr-only">Open Chat</span>
            </Button>

            {/* Notifications Button */}
            <Button 
              variant="ghost" 
              size="icon"
              className="flex-shrink-0"
              title="Notifications"
            >
                <Bell className="h-5 w-5" />
                <span className="sr-only">Notifications</span>
            </Button>

            {/* System Health Indicator - Better responsive handling */}
            <div className="hidden md:flex items-center flex-shrink-0">
                <SystemHealthIndicator />
            </div>

            {/* User Menu - Improved spacing */}
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="rounded-full flex-shrink-0"
                    >
                        <Avatar className="h-8 w-8">
                            <AvatarImage src="/placeholder-user.jpg" alt="@username" />
                            <AvatarFallback>U</AvatarFallback>
                        </Avatar>
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-48">
                    <DropdownMenuLabel>My Account</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem>Settings</DropdownMenuItem>
                    <DropdownMenuItem>Support</DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem>Logout</DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
        
        {/* HITL Alert Bar - Using Architect thinking pattern */}
        {visibleAlerts.length > 0 && (
          <div className="border-b border-border px-6 py-2 bg-card">
            <div className="flex items-center space-x-3">
              {visibleAlerts.map((alert) => {
                const isExpanded = expandedAlerts.includes(alert.id)
                const shortMessage = `${alert.stage || 'General'}`
                
                return (
                  <div key={alert.id} className="flex items-center space-x-2 bg-amber/10 border border-amber/20 text-amber px-3 py-1 rounded-full">
                    <AlertTriangle className="w-4 h-4 text-amber" />
                    <button
                      onClick={() => toggleExpanded(alert.id)}
                      className="flex items-center space-x-1 hover:bg-amber/10 rounded transition-colors"
                    >
                      <span className="text-sm font-medium">
                        {isExpanded ? alert.message : shortMessage}
                      </span>
                      <ChevronDown className={`w-3 h-3 text-amber transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
                    </button>
                    <Button 
                      size="icon" 
                      variant="ghost" 
                      className="h-5 w-5 text-amber hover:bg-amber/10" 
                      onClick={() => dismissAlert(alert.id)}
                      title="Dismiss alert"
                    >
                      <X className="w-3 h-3" />
                    </Button>
                  </div>
                )
              })}
            </div>
          </div>
        )}
        </header>
        <GlobalChatModal isOpen={isChatOpen} onOpenChange={setIsChatOpen} />
    </>
  )
}