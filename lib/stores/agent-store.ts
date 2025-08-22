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
  progress?: number
  progress_stage?: string
  progress_current?: number
  progress_total?: number
  progress_estimated_time_remaining?: number
  is_thinking?: boolean
  currentStep?: string
}

import { WebSocketMessage } from "../websocket/websocket-service"

interface AgentStore {
  agents: Agent[]
  activeAgentCount: number
  setAgents: (agents: Agent[]) => void
  updateAgent: (id: string, updates: Partial<Agent>) => void
  updateAgentByName: (name: string, updates: Partial<Agent>) => void
  getAgentById: (id: string) => Agent | undefined
  updateAgentFromMessage: (message: WebSocketMessage) => void
  handleAgentError: (agentName: string, error: string) => void
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
    updateAgentByName: (name, updates) =>
      set((state) => ({
        agents: state.agents.map((agent) =>
          agent.name.toLowerCase() === name.toLowerCase() ? { ...agent, ...updates, lastActivity: new Date() } : agent,
        ),
        activeAgentCount: state.agents.filter((a) =>
          a.name.toLowerCase() === name.toLowerCase()
            ? (updates.status || a.status) === "active"
            : a.status === "active",
        ).length,
      })),
    getAgentById: (id) => get().agents.find((agent) => agent.id === id),
    updateAgentFromMessage: (message) => {
      const { agent_name, type, metadata, timestamp } = message;
      if (!agent_name) return;

      if (type === 'agent_status' && metadata) {
        const updates: Partial<Agent> = {
          status: metadata.status,
          currentTask: metadata.task,
          lastActivity: new Date(timestamp),
        };
        get().updateAgentByName(agent_name, updates);
      } else if (type === 'agent_progress' && metadata) {
        const updates: Partial<Agent> = {
          progress: (metadata.current / metadata.total) * 100,
          progress_stage: metadata.stage,
          progress_current: metadata.current,
          progress_total: metadata.total,
          progress_estimated_time_remaining: metadata.estimated_time_remaining,
          lastActivity: new Date(timestamp),
        };
        get().updateAgentByName(agent_name, updates);
      } else if (type === 'agent_thinking') {
        const updates: Partial<Agent> = {
          is_thinking: true,
          lastActivity: new Date(timestamp),
        };
        get().updateAgentByName(agent_name, updates);
      } else if (type === 'agent_response' || type === 'agent_error') {
        const updates: Partial<Agent> = {
          is_thinking: false,
          lastActivity: new Date(timestamp),
        };
        get().updateAgentByName(agent_name, updates);
      }
    },
    handleAgentError: (agentName, error) => {
      const updates: Partial<Agent> = {
        status: "error",
        currentTask: error,
      };
      get().updateAgentByName(agentName, updates);
    },
  })),
)
