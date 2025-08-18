"use client"

import { MainLayout } from "@/components/main-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Upload, Save } from "lucide-react"
import { useState } from "react"

export default function SettingsPage() {
  const [maxAgents, setMaxAgents] = useState(10)
  const [healthInterval, setHealthInterval] = useState(10000)

  // Agent interaction matrix state
  const [interactions, setInteractions] = useState({
    "Agent 1": { "Agent 2": true, "Agent 3": true, "Agent 4": false },
    "Agent 2": { "Agent 1": true, "Agent 3": false, "Agent 4": true },
    "Agent 3": { "Agent 1": true, "Agent 2": false, "Agent 4": false },
    "Agent 4": { "Agent 1": false, "Agent 2": true, "Agent 3": false },
  })

  const agents = ["Agent 1", "Agent 2", "Agent 3", "Agent 4"]

  const toggleInteraction = (agent1: string, agent2: string) => {
    setInteractions((prev) => ({
      ...prev,
      [agent1]: {
        ...prev[agent1],
        [agent2]: !prev[agent1][agent2],
      },
    }))
  }

  const agentConfigs = [
    { name: "Analyst", status: "Configured", description: "Requirements analysis agent" },
    { name: "Architect", status: "Configured", description: "System design agent" },
    { name: "Developer", status: "Pending", description: "Code generation agent" },
    { name: "Tester", status: "Configured", description: "Quality assurance agent" },
    { name: "Deployer", status: "Pending", description: "Deployment management agent" },
    { name: "Monitor", status: "Error", description: "System monitoring agent" },
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Configured":
        return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
      case "Pending":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      case "Error":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getStatusIndicator = (status: string) => {
    switch (status) {
      case "Configured":
        return "bg-emerald-400"
      case "Pending":
        return "bg-yellow-400"
      case "Error":
        return "bg-red-400"
      default:
        return "bg-gray-400"
    }
  }

  const getStatusMessage = (status: string) => {
    switch (status) {
      case "Configured":
        return "Configuration loaded"
      case "Pending":
        return "Awaiting configuration"
      case "Error":
        return "Configuration error"
      default:
        return "Status unknown"
    }
  }

  return (
    <MainLayout>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Settings</h1>
            <p className="text-muted-foreground">Configure agents and system parameters</p>
          </div>
          <Button size="sm">
            <Save className="mr-2 h-4 w-4" />
            Save
          </Button>
        </div>

        {/* Agent Configuration */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Agent Configuration</CardTitle>
            <CardDescription>Upload configuration files for each agent</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {agentConfigs.map((agent) => (
                <Card key={agent.name} className="flex flex-col">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-base">{agent.name}</CardTitle>
                      <Badge variant="outline" className={`${getStatusColor(agent.status)} font-medium`}>
                        {agent.status}
                      </Badge>
                    </div>
                    <CardDescription>{agent.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="flex-1 flex flex-col">
                    <div className="flex items-center justify-between mt-auto">
                      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                        <div className={`w-2 h-2 rounded-full ${getStatusIndicator(agent.status)}`} />
                        <span>{getStatusMessage(agent.status)}</span>
                      </div>
                      <Button variant="outline" size="sm" className="h-8 w-8 p-0 bg-transparent">
                        <Upload className="h-3 w-3" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Agent Interactions Matrix */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Agent Interactions</CardTitle>
            <CardDescription>Configure which agents can interact with each other</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr>
                    <th className="border p-2 text-left font-medium"></th>
                    {agents.map((agent) => (
                      <th key={agent} className="border p-2 text-center font-medium text-sm">
                        {agent}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {agents.map((agent1) => (
                    <tr key={agent1}>
                      <td className="border p-2 font-medium text-sm">{agent1}</td>
                      {agents.map((agent2) => (
                        <td key={agent2} className="border p-2 text-center">
                          {agent1 === agent2 ? (
                            <span className="text-muted-foreground">-</span>
                          ) : (
                            <button
                              onClick={() => toggleInteraction(agent1, agent2)}
                              className={`w-6 h-6 rounded text-xs font-bold ${
                                interactions[agent1]?.[agent2]
                                  ? "bg-primary text-primary-foreground"
                                  : "bg-muted text-muted-foreground"
                              }`}
                            >
                              {interactions[agent1]?.[agent2] ? "X" : "-"}
                            </button>
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* System Configuration */}
        <Card>
          <CardHeader>
            <CardTitle>System Configuration</CardTitle>
            <CardDescription>Configure system-wide parameters</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="maxAgents">Max Agents</Label>
                <Input
                  id="maxAgents"
                  type="number"
                  value={maxAgents}
                  onChange={(e) => setMaxAgents(Number(e.target.value))}
                  className="w-full"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="healthInterval">Health Interval (ms)</Label>
                <Input
                  id="healthInterval"
                  type="number"
                  value={healthInterval}
                  onChange={(e) => setHealthInterval(Number(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
