"use client"

import { MainLayout } from "@/components/main-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Zap, Plus, Send } from "lucide-react"
import { useState } from "react"

export default function HomePage() {
  const [message, setMessage] = useState("")

  // Mock chat messages
  const chatMessages = [
    {
      id: 1,
      sender: "Analyst",
      content: "I've analyzed the requirements and identified 3 key user personas for this project.",
      timestamp: "10:30 AM",
      isAgent: true,
    },
    {
      id: 2,
      sender: "User",
      content: "Great! Can you provide more details about the primary persona?",
      timestamp: "10:32 AM",
      isAgent: false,
    },
    {
      id: 3,
      sender: "Architect",
      content:
        "Based on the analysis, I recommend a microservices architecture with React frontend and Node.js backend.",
      timestamp: "10:35 AM",
      isAgent: true,
    },
    {
      id: 4,
      sender: "User",
      content: "That sounds good. What about the database design?",
      timestamp: "10:37 AM",
      isAgent: false,
    },
    {
      id: 5,
      sender: "Developer",
      content: "I can implement PostgreSQL with Prisma ORM for type-safe database operations.",
      timestamp: "10:40 AM",
      isAgent: true,
    },
  ]

  const agents = [
    { name: "Analyst", status: "Done", description: "Requirements analysis" },
    { name: "Architect", status: "WIP", description: "System design" },
    { name: "Developer", status: "WIP", description: "Code generation" },
    { name: "Tester", status: "Queued", description: "Quality assurance" },
    { name: "Deployer", status: "Queued", description: "Deployment management" },
    { name: "Monitor", status: "Error", description: "System monitoring" },
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Done":
        return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
      case "WIP":
        return "bg-blue-500/20 text-blue-400 border-blue-500/30"
      case "Error":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      case "Queued":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getStatusIndicator = (status: string) => {
    switch (status) {
      case "Done":
        return "bg-emerald-400"
      case "WIP":
        return "bg-blue-400"
      case "Error":
        return "bg-red-400"
      case "Queued":
        return "bg-yellow-400"
      default:
        return "bg-gray-400"
    }
  }

  const getStatusMessage = (status: string) => {
    switch (status) {
      case "Done":
        return "Task completed"
      case "WIP":
        return "Processing tasks"
      case "Error":
        return "Error occurred"
      case "Queued":
        return "Waiting for tasks"
      default:
        return "Status unknown"
    }
  }

  const handleSendMessage = () => {
    if (message.trim()) {
      // Handle message sending logic here
      setMessage("")
    }
  }

  return (
    <MainLayout>
      <div className="p-6">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
              <p className="text-muted-foreground">Communicate with your AI agents in real-time</p>
            </div>
          </div>
          <Button className="bg-primary hover:bg-primary/90">
            <Zap className="w-4 h-4 mr-2" />
            Start New Project
          </Button>
        </div>

        <div className="space-y-6">
          {/* Chat Interface */}
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="w-5 h-5 text-primary" />
                <span>Agent Chat</span>
              </CardTitle>
              <CardDescription>Communicate with your AI agents in real-time</CardDescription>
            </CardHeader>
            <CardContent>
              {/* Chat Messages Area */}
              <ScrollArea className="h-56 w-full border rounded-lg p-4 mb-4">
                <div className="space-y-4">
                  {chatMessages.map((msg) => (
                    <div key={msg.id} className={`flex ${msg.isAgent ? "justify-start" : "justify-end"}`}>
                      <div
                        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                          msg.isAgent ? "bg-muted text-foreground" : "bg-primary text-primary-foreground"
                        }`}
                      >
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="text-xs font-medium">{msg.sender}</span>
                          <span className="text-xs opacity-70">{msg.timestamp}</span>
                        </div>
                        <p className="text-sm">{msg.content}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>

              {/* Chat Input */}
              <div className="flex space-x-2">
                <Button variant="outline" size="sm">
                  <Plus className="w-4 h-4" />
                </Button>
                <Input
                  placeholder="Type your message to the agents..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                  className="flex-1"
                />
                <Button onClick={handleSendMessage} size="sm">
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Agent Status Cards */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => (
              <Card key={agent.name}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-base">{agent.name}</CardTitle>
                    <Badge variant="outline" className={`${getStatusColor(agent.status)} font-medium`}>
                      {agent.status}
                    </Badge>
                  </div>
                  <CardDescription>{agent.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                    <div className={`w-2 h-2 rounded-full ${getStatusIndicator(agent.status)}`} />
                    <span>{getStatusMessage(agent.status)}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  )
}
