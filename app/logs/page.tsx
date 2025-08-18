"use client"

import { useState, useEffect } from "react"
import { MainLayout } from "@/components/main-layout"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Download, Search, Filter } from "lucide-react"

interface LogEntry {
  id: string
  timestamp: string
  agent: string
  task: string
  status: "ok" | "running" | "done" | "error" | "warning"
  message?: string
  details?: any
}

export default function LogsPage() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState<string>("all")

  // Mock log data - in real app this would come from WebSocket or API
  useEffect(() => {
    const mockLogs: LogEntry[] = [
      {
        id: "1",
        timestamp: new Date().toISOString(),
        agent: "System",
        task: "boot",
        status: "ok",
        message: "System initialization complete",
      },
      {
        id: "2",
        timestamp: new Date(Date.now() - 60000).toISOString(),
        agent: "Analyst",
        task: "requirements_analysis",
        status: "running",
        message: "Analyzing user requirements for new feature",
      },
      {
        id: "3",
        timestamp: new Date(Date.now() - 120000).toISOString(),
        agent: "Architect",
        task: "system_design",
        status: "done",
        message: "Architecture design completed successfully",
      },
      {
        id: "4",
        timestamp: new Date(Date.now() - 180000).toISOString(),
        agent: "Developer",
        task: "code_generation",
        status: "error",
        message: "Failed to generate component due to missing dependencies",
      },
      {
        id: "5",
        timestamp: new Date(Date.now() - 240000).toISOString(),
        agent: "System",
        task: "health_check",
        status: "ok",
        message: "All agents responding normally",
      },
      {
        id: "6",
        timestamp: new Date(Date.now() - 300000).toISOString(),
        agent: "Tester",
        task: "unit_testing",
        status: "warning",
        message: "Tests passed with minor warnings",
      },
    ]
    setLogs(mockLogs)
  }, [])

  const filteredLogs = logs.filter((log) => {
    const matchesSearch =
      log.agent.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.task.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.message?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "all" || log.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case "ok":
        return "bg-green-500/20 text-green-400 border-green-500/30"
      case "running":
        return "bg-blue-500/20 text-blue-400 border-blue-500/30"
      case "done":
        return "bg-cyan-500/20 text-cyan-400 border-cyan-500/30"
      case "error":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      case "warning":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const exportLogs = () => {
    const jsonlData = filteredLogs.map((log) => JSON.stringify(log)).join("\n")
    const blob = new Blob([jsonlData], { type: "application/jsonl" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `botarmy-logs-${new Date().toISOString().split("T")[0]}.jsonl`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <MainLayout>
      <div className="p-6">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Logs</h1>
            <p className="text-muted-foreground">Real-time agent activity and system events</p>
          </div>
          <Button onClick={exportLogs} size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export JSONL
          </Button>
        </div>

        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search logs by agent, task, or message..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4 text-muted-foreground" />
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="bg-background border border-border rounded-md px-3 py-2 text-sm"
                >
                  <option value="all">All Status</option>
                  <option value="ok">OK</option>
                  <option value="running">Running</option>
                  <option value="done">Done</option>
                  <option value="error">Error</option>
                  <option value="warning">Warning</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Log Viewer */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Log Entries ({filteredLogs.length})</span>
              <Badge variant="outline" className="text-xs">
                Live Feed
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 max-h-[600px] overflow-y-auto">
              {filteredLogs.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">No logs match your current filters</div>
              ) : (
                filteredLogs.map((log) => (
                  <div
                    key={log.id}
                    className="flex items-start gap-4 p-4 rounded-lg border bg-card/50 hover:bg-card/80 transition-colors"
                  >
                    <div className="text-xs text-muted-foreground font-mono min-w-[140px]">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </div>
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline" className="text-xs">
                          {log.agent}
                        </Badge>
                        <Badge className={`text-xs ${getStatusColor(log.status)}`}>{log.status.toUpperCase()}</Badge>
                        <span className="text-sm font-medium">{log.task}</span>
                      </div>
                      {log.message && <p className="text-sm text-muted-foreground">{log.message}</p>}
                    </div>
                    <div className="text-xs text-muted-foreground font-mono">#{log.id}</div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
