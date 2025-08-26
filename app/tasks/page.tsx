"use client"

import { useState } from "react"
import { MainLayout } from "@/components/main-layout"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { RefreshCw, Filter, Search } from "lucide-react"
import { useTaskStore, Task } from "@/lib/stores/task-store"
import { useAgentStore } from "@/lib/stores/agent-store"
import { Progress } from "@/components/ui/progress"

const getStatusColor = (status: Task['status']) => {
  switch (status) {
    case "completed":
      return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
    case "in-progress":
      return "bg-blue-500/20 text-blue-400 border-blue-500/30"
    case "failed":
      return "bg-red-500/20 text-red-400 border-red-500/30"
    case "pending":
      return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
    default:
      return "bg-gray-500/20 text-gray-400 border-gray-500/30"
  }
}

export default function TasksPage() {
  const { tasks } = useTaskStore()
  const { agents } = useAgentStore()
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("All")
  const [agentFilter, setAgentFilter] = useState("All")

  const agentRoles = ["All", ...Array.from(new Set(agents.map(agent => agent.role)))]

  const filteredTasks = tasks.filter((task) => {
    const matchesSearch =
      task.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.agent.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "All" || task.status === statusFilter
    const matchesAgent = agentFilter === "All" || task.agent === agentFilter
    return matchesSearch && matchesStatus && matchesAgent
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
            <option value="All">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="in-progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>
          <select
            value={agentFilter}
            onChange={(e) => setAgentFilter(e.target.value)}
            className="px-3 py-2 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          >
            {agentRoles.map(role => (
              <option key={role} value={role}>{role === "All" ? "All Agents" : role}</option>
            ))}
          </select>
        </div>

        {/* Tasks Table */}
        <div className="border border-border rounded-lg overflow-hidden mb-4">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-muted/50 border-b border-border">
                <tr>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground">Task Name</th>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground w-[120px]">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground">Agent</th>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground w-[200px]">Progress</th>
                  <th className="text-left py-3 px-4 font-medium text-sm text-muted-foreground">Start Time</th>
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
                      <span className="text-muted-foreground">{task.agent}</span>
                    </td>
                    <td className="py-3 px-4">
                       <Progress value={task.progress} className="h-2" />
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-muted-foreground text-sm">{new Date(task.startTime).toLocaleString()}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Results Summary */}
        <div className="text-sm text-muted-foreground">
          Showing {filteredTasks.length} of {tasks.length} tasks
        </div>
      </div>
    </MainLayout>
  )
}
