"use client"

import { useState } from "react"
import { MainLayout } from "@/components/main-layout"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { RefreshCw, Filter, Search } from "lucide-react"

// Mock task data based on the mockup
const mockTasks = [
  {
    id: 1,
    name: "Scrape sites",
    status: "Done",
    agentRole: "Researcher",
    duration: "2m 10s",
    timestamp: "2024-01-15 14:30:00",
  },
  {
    id: 2,
    name: "Draft post",
    status: "WIP",
    agentRole: "Writer",
    duration: "-",
    timestamp: "2024-01-15 14:32:00",
  },
  {
    id: 3,
    name: "Analyze data",
    status: "Error",
    agentRole: "Analyst",
    duration: "1m 45s",
    timestamp: "2024-01-15 14:28:00",
  },
  {
    id: 4,
    name: "Generate report",
    status: "Queued",
    agentRole: "Writer",
    duration: "-",
    timestamp: "2024-01-15 14:35:00",
  },
  {
    id: 5,
    name: "Train model",
    status: "Done",
    agentRole: "Developer",
    duration: "5m 30s",
    timestamp: "2024-01-15 14:25:00",
  },
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

export default function TasksPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("All")

  const filteredTasks = mockTasks.filter((task) => {
    const matchesSearch =
      task.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.agentRole.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "All" || task.status === statusFilter
    return matchesSearch && matchesStatus
  })

  return (
    <MainLayout>
      <div className="p-6">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Tasks</h1>
            <p className="text-muted-foreground">Monitor and track all agent tasks in real-time</p>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" size="sm">
              <Filter className="h-4 w-4 mr-2" />
              Filter
            </Button>
            <Button variant="outline" size="sm">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="flex items-center gap-4 mb-6">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="All">All Status</option>
            <option value="Done">Done</option>
            <option value="WIP">In Progress</option>
            <option value="Error">Error</option>
            <option value="Queued">Queued</option>
          </select>
        </div>

        {/* Tasks Table */}
        <div className="border border-border rounded-lg overflow-hidden mb-4">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-muted/50 border-b border-border">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground">Task Name</th>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground">Agent Role</th>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground">Duration</th>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground">Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {filteredTasks.map((task, index) => (
                  <tr
                    key={task.id}
                    className={`border-b border-border hover:bg-muted/30 transition-colors ${
                      index === filteredTasks.length - 1 ? "border-b-0" : ""
                    }`}
                  >
                    <td className="py-3 px-4">
                      <div className="font-medium text-foreground">{task.name}</div>
                    </td>
                    <td className="py-3 px-4">
                      <Badge variant="outline" className={`${getStatusColor(task.status)} font-medium`}>
                        {task.status}
                      </Badge>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-muted-foreground">{task.agentRole}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-muted-foreground font-mono text-sm">{task.duration}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-muted-foreground text-sm">{new Date(task.timestamp).toLocaleString()}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Results Summary */}
        <div className="text-sm text-muted-foreground">
          Showing {filteredTasks.length} of {mockTasks.length} tasks
        </div>
      </div>
    </MainLayout>
  )
}
