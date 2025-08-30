"use client"

import React, { useState, useCallback, useRef, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Bot,
  User,
  CheckCircle,
  ChevronDown,
  ChevronsRightLeft,
  Send,
  Loader,
  X,
  Wifi,
} from "lucide-react"
import { cn } from "@/lib/utils"

// --- Mock Data and Types ---
type MessageType = "user" | "agent" | "system"
interface ChatMessage {
  id: string
  type: MessageType
  sender: string
  content: string | React.ReactNode
  timestamp: string
  collapsed?: boolean
}

const mockMessages: ChatMessage[] = [
  { id: "1", type: "user", sender: "User", content: "Create a todo application with React frontend", timestamp: "15:32", collapsed: true },
  { id: "2", type: "system", sender: "System", content: "Starting new project workflow...", timestamp: "15:33" },
  { id: "3", type: "agent", sender: "Analyst", content: (
    <ul className="list-disc list-inside space-y-1">
      <li>I'll analyze your requirements...</li>
      <li>- User authentication needed</li>
      <li>- CRUD operations for todos</li>
      <li>- React frontend preference noted</li>
    </ul>
  ), timestamp: "15:33" },
  { id: "4", type: "user", sender: "User", content: "Also add user preferences and themes", timestamp: "15:34" },
  { id: "5", type: "agent", sender: "Analyst", content: "✅ Analysis complete. Key features identified.", timestamp: "15:35", collapsed: true },
  { id: "6", type: "agent", sender: "Architect", content: "⚡ Currently designing system architecture...", timestamp: "15:36" },
]

// --- Resizable Hook ---
const useResizable = (initialHeight: number) => {
  const [height, setHeight] = useState(initialHeight)
  const handleRef = useRef<HTMLDivElement>(null)

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    const startY = e.clientY
    const startHeight = height

    const handleMouseMove = (moveEvent: MouseEvent) => {
      const deltaY = startY - moveEvent.clientY // Inverted for bottom handle
      setHeight(Math.max(200, Math.min(800, startHeight + deltaY)))
    }

    const handleMouseUp = () => {
      document.removeEventListener("mousemove", handleMouseMove)
      document.removeEventListener("mouseup", handleMouseUp)
    }

    document.addEventListener("mousemove", handleMouseMove)
    document.addEventListener("mouseup", handleMouseUp)
  }, [height])

  return { height, handleRef, handleMouseDown }
}

// --- Message Component ---
const MessageItem = ({ message, onToggleCollapse }: { message: ChatMessage; onToggleCollapse: (id: string) => void }) => {
  const icons = {
    user: <User className="w-4 h-4" />,
    agent: <Bot className="w-4 h-4" />,
    system: <CheckCircle className="w-4 h-4" />,
  }
  const colors = {
    user: "bg-blue-50 border-blue-200",
    agent: "bg-gray-50 border-gray-200",
    system: "bg-green-50 border-green-200",
  }

  return (
    <div className={cn("p-2 rounded-lg border", colors[message.type])}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          {icons[message.type]}
          <span className="font-semibold text-sm">{message.sender}</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-xs text-muted-foreground">{message.timestamp}</span>
          <Button size="icon" variant="ghost" className="h-6 w-6" onClick={() => onToggleCollapse(message.id)}>
            <ChevronDown className={cn("w-4 h-4 transition-transform", !message.collapsed && "rotate-180")} />
          </Button>
        </div>
      </div>
      {!message.collapsed && (
        <div className="pt-2 pl-6 text-sm whitespace-pre-wrap">{message.content}</div>
      )}
    </div>
  )
}

// --- Overlay Component ---
const TemporaryOverlay = ({ onDismiss }: { onDismiss: () => void }) => {
  return (
    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-black/70 text-white p-4 rounded-lg shadow-lg flex items-center space-x-3">
      <Loader className="w-5 h-5 animate-spin" />
      <div>
        <p className="font-semibold">Architect is thinking...</p>
        <p className="text-sm opacity-80">ETA: 30 seconds</p>
      </div>
      <Button size="icon" variant="ghost" className="h-6 w-6 text-white hover:bg-white/20" onClick={onDismiss}>
        <X className="w-4 h-4" />
      </Button>
    </div>
  )
}

// --- Main Chat Interface Mockup ---
export function EnhancedChatInterfaceMockup() {
  const { height, handleRef, handleMouseDown } = useResizable(400)
  const [messages, setMessages] = useState(mockMessages)
  const [showOverlay, setShowOverlay] = useState(false)

  useEffect(() => {
    // Show overlay for demonstration
    const timer = setTimeout(() => setShowOverlay(true), 2000)
    return () => clearTimeout(timer)
  }, [])

  const toggleCollapse = (id: string) => {
    setMessages(msgs =>
      msgs.map(msg => (msg.id === id ? { ...msg, collapsed: !msg.collapsed } : msg))
    )
  }

  return (
    <Card style={{ height: `${height}px` }} className="flex flex-col relative overflow-hidden">
      <CardHeader className="flex-shrink-0">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Bot className="w-5 h-5" />
            <span>Agent Chat</span>
          </CardTitle>
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Wifi className="w-4 h-4 text-green-500" />
            <span>Connected</span>
          </div>
        </div>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col p-0 overflow-y-hidden">
        <div className="flex-1 relative">
          <ScrollArea className="h-full">
            <div className="p-4 space-y-4">
              {messages.map(msg => (
                <MessageItem key={msg.id} message={msg} onToggleCollapse={toggleCollapse} />
              ))}
            </div>
          </ScrollArea>
          {showOverlay && <TemporaryOverlay onDismiss={() => setShowOverlay(false)} />}
        </div>

        <div className="p-4 border-t flex-shrink-0">
          <div className="flex items-center space-x-2">
            <Input placeholder="Type your message..." className="flex-1" />
            <Button>
              <Send className="w-4 h-4 mr-2" />
              Send
            </Button>
          </div>
        </div>
      </CardContent>

      <div
        ref={handleRef}
        onMouseDown={handleMouseDown}
        className="absolute bottom-0 right-0 w-4 h-4 cursor-nwse-resize"
      >
        <ChevronsRightLeft className="w-3 h-3 absolute bottom-0 right-0 text-muted-foreground/50" />
      </div>
    </Card>
  )
}
