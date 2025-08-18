import { create } from "zustand"
import { subscribeWithSelector } from "zustand/middleware"

export interface Agent {
  id: string
  name: string
  role: string
  status: "active" | "idle" | "error" | "offline"
  currentTask?: string
  lastActivity: Date
  tasksCompleted: number
  successRate: number
}

interface AgentStore {
  agents: Agent[]
  activeAgentCount: number
  setAgents: (agents: Agent[]) => void
  updateAgent: (id: string, updates: Partial<Agent>) => void
  getAgentById: (id: string) => Agent | undefined
}

export const useAgentStore = create<AgentStore>()(
  subscribeWithSelector((set, get) => ({
    agents: [
      {
        id: "analyst",
        name: "Analyst",
        role: "Requirements Analysis",
        status: "active",
        currentTask: "Analyzing user requirements",
        lastActivity: new Date(),
        tasksCompleted: 23,
        successRate: 94.2,
      },
      {
        id: "architect",
        name: "Architect",
        role: "System Design",
        status: "idle",
        lastActivity: new Date(Date.now() - 300000),
        tasksCompleted: 18,
        successRate: 96.8,
      },
      {
        id: "developer",
        name: "Developer",
        role: "Code Generation",
        status: "active",
        currentTask: "Implementing API endpoints",
        lastActivity: new Date(),
        tasksCompleted: 31,
        successRate: 89.7,
      },
      {
        id: "tester",
        name: "Tester",
        role: "Quality Assurance",
        status: "idle",
        lastActivity: new Date(Date.now() - 180000),
        tasksCompleted: 15,
        successRate: 98.1,
      },
      {
        id: "deployer",
        name: "Deployer",
        role: "Deployment",
        status: "idle",
        lastActivity: new Date(Date.now() - 600000),
        tasksCompleted: 8,
        successRate: 100,
      },
      {
        id: "monitor",
        name: "Monitor",
        role: "System Monitoring",
        status: "active",
        currentTask: "Health check monitoring",
        lastActivity: new Date(),
        tasksCompleted: 42,
        successRate: 99.2,
      },
    ],
    activeAgentCount: 3,
    setAgents: (agents) =>
      set({
        agents,
        activeAgentCount: agents.filter((a) => a.status === "active").length,
      }),
    updateAgent: (id, updates) =>
      set((state) => ({
        agents: state.agents.map((agent) => (agent.id === id ? { ...agent, ...updates } : agent)),
        activeAgentCount: state.agents.filter((a) =>
          a.id === id ? (updates.status || a.status) === "active" : a.status === "active",
        ).length,
      })),
    getAgentById: (id) => get().agents.find((agent) => agent.id === id),
  })),
)
