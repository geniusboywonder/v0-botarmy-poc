"use client"

import { MainLayout } from "@/components/main-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
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
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[1, 2, 3].map((agentNum) => (
                <div key={agentNum} className="border rounded-lg p-4 space-y-3">
                  <h3 className="font-medium">Agent {agentNum}</h3>
                  <Button variant="outline" className="w-full bg-transparent">
                    <Upload className="mr-2 h-4 w-4" />
                    Upload File
                  </Button>
                </div>
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
