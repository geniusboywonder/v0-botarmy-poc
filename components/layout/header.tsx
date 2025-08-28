"use client"

import { useState } from "react"
import Link from "next/link"
import {
  Bell,
  MessageSquare,
  Search,
  User as UserIcon,
  Bot,
} from "lucide-react"

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

  return (
    <>
        <header className="flex h-16 items-center border-b bg-card px-4 md:px-6">
        
        {/* Site Title / Logo */}
        <div className="flex items-center gap-4 flex-shrink-0">
            <Link href="/" className="flex items-center gap-2">
                <Bot className="h-6 w-6" />
                <span className="text-lg font-semibold hidden md:block">BotArmy</span>
            </Link>
        </div>

        {/* Search Bar - Center */}
        <div className="flex-1 max-w-sm mx-4">
            <div className="relative w-full">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                    type="search"
                    placeholder="Search tasks, artifacts, or agents..."
                    className="pl-10"
                />
            </div>
        </div>

        {/* Actions - Right Side */}
        <div className="flex items-center gap-2 flex-shrink-0">
            <Button variant="ghost" size="icon" onClick={() => setIsChatOpen(true)}>
                <MessageSquare className="h-5 w-5" />
                <span className="sr-only">Open Chat</span>
            </Button>

            <Button variant="ghost" size="icon">
                <Bell className="h-5 w-5" />
                <span className="sr-only">Notifications</span>
            </Button>

            <div className="hidden md:block ml-2">
                <SystemHealthIndicator />
            </div>

            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="rounded-full ml-2">
                        <Avatar className="h-8 w-8">
                            <AvatarImage src="/placeholder-user.jpg" alt="@username" />
                            <AvatarFallback>U</AvatarFallback>
                        </Avatar>
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                    <DropdownMenuLabel>My Account</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem>Settings</DropdownMenuItem>
                    <DropdownMenuItem>Support</DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem>Logout</DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
        
        </header>
        <GlobalChatModal isOpen={isChatOpen} onOpenChange={setIsChatOpen} />
    </>
  )
}
