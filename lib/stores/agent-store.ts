import { create } from "zustand"
import { subscribeWithSelector, persist, createJSONStorage } from "zustand/middleware"

export interface Agent {
  id: string
  name: string
  role: string
  status: "active" | "idle" | "error" | "offline" | "thinking" | "paused"
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

  // Enhanced tracking fields
  startTime?: Date
  endTime?: Date
  totalRuntime: number // in seconds
  averageTaskTime: number // in seconds
  errorCount: number
  lastError?: string
  queue: {
    todo: number
    inProgress: number
    done: number
    failed: number
  }
  performance: {
    responseTime: number // average response time in ms
    throughput: number // tasks per hour
    efficiency: number // percentage of successful tasks
    uptime: number // percentage uptime
  }
  metadata?: Record<string, any>
}

import { WebSocketMessage } from "../websocket/websocket-service"

interface AgentMetrics {
  totalTasks: number
  activeTasks: number
  completedTasks: number
  failedTasks: number
  averageResponseTime: number
  overallSuccessRate: number
  systemUptime: number
}

interface AgentStore {
  agents: Agent[]
  activeAgentCount: number
  metrics: AgentMetrics
  isInitialized: boolean
  lastSync: Date | null

  // Core agent management
  setAgents: (agents: Agent[]) => void
  updateAgent: (id: string, updates: Partial<Agent>) => void
  updateAgentByName: (name: string, updates: Partial<Agent>) => void
  getAgentById: (id: string) => Agent | undefined
  getAgentByName: (name: string) => Agent | undefined

  // Message handling
  updateAgentFromMessage: (message: WebSocketMessage) => void
  handleAgentError: (agentName: string, error: string) => void

  // Enhanced functionality
  startAgentTask: (agentName: string, task: string) => void
  completeAgentTask: (agentName: string, success?: boolean) => void
  pauseAgent: (agentName: string) => void
  resumeAgent: (agentName: string) => void
  resetAgent: (agentName: string) => void

  // Metrics and analytics
  updateMetrics: () => void
  getAgentPerformance: (agentName: string) => Agent['performance'] | null
  getSystemHealth: () => { healthy: number; total: number; percentage: number }

  // Persistence and sync
  syncWithBackend: () => Promise<void>
  exportAgentData: () => string
  importAgentData: (data: string) => void
}

// Helper function to calculate agent performance
const calculatePerformance = (agent: Agent): Agent['performance'] => {
  const totalTasks = agent.tasksCompleted + agent.errorCount
  const efficiency = totalTasks > 0 ? (agent.tasksCompleted / totalTasks) * 100 : 100
  const uptime = agent.totalRuntime > 0 ?
    ((agent.totalRuntime - (agent.errorCount * 60)) / agent.totalRuntime) * 100 : 100

  return {
    responseTime: agent.averageTaskTime * 1000, // convert to ms
    throughput: agent.totalRuntime > 0 ? (agent.tasksCompleted / (agent.totalRuntime / 3600)) : 0,
    efficiency: Math.max(0, Math.min(100, efficiency)),
    uptime: Math.max(0, Math.min(100, uptime))
  }
}

// Default agents with enhanced data
const defaultAgents: Agent[] = [
  {
    id: "analyst",
    name: "Analyst",
    role: "Requirements Analysis",
    status: "idle",
    lastActivity: new Date(),
    tasksCompleted: 23,
    successRate: 94.2,
    totalRuntime: 3600, // 1 hour
    averageTaskTime: 180, // 3 minutes
    errorCount: 1,
    queue: { todo: 0, inProgress: 0, done: 23, failed: 1 },
    performance: {
      responseTime: 180000, // 3 minutes in ms
      throughput: 23,
      efficiency: 94.2,
      uptime: 98.5
    }
  },
  {
    id: "architect",
    name: "Architect",
    role: "System Design",
    status: "idle",
    lastActivity: new Date(Date.now() - 300000),
    tasksCompleted: 18,
    successRate: 96.8,
    totalRuntime: 2700, // 45 minutes
    averageTaskTime: 240, // 4 minutes
    errorCount: 0,
    queue: { todo: 0, inProgress: 0, done: 18, failed: 0 },
    performance: {
      responseTime: 240000,
      throughput: 24,
      efficiency: 96.8,
      uptime: 100
    }
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
    totalRuntime: 5400, // 1.5 hours
    averageTaskTime: 300, // 5 minutes
    errorCount: 3,
    queue: { todo: 2, inProgress: 1, done: 31, failed: 3 },
    performance: {
      responseTime: 300000,
      throughput: 20.7,
      efficiency: 89.7,
      uptime: 95.2
    }
  },
  {
    id: "tester",
    name: "Tester",
    role: "Quality Assurance",
    status: "idle",
    lastActivity: new Date(Date.now() - 180000),
    tasksCompleted: 15,
    successRate: 98.1,
    totalRuntime: 1800, // 30 minutes
    averageTaskTime: 120, // 2 minutes
    errorCount: 0,
    queue: { todo: 0, inProgress: 0, done: 15, failed: 0 },
    performance: {
      responseTime: 120000,
      throughput: 30,
      efficiency: 98.1,
      uptime: 100
    }
  },
  {
    id: "deployer",
    name: "Deployer",
    role: "Deployment",
    status: "idle",
    lastActivity: new Date(Date.now() - 600000),
    tasksCompleted: 8,
    successRate: 100,
    totalRuntime: 1200, // 20 minutes
    averageTaskTime: 150, // 2.5 minutes
    errorCount: 0,
    queue: { todo: 0, inProgress: 0, done: 8, failed: 0 },
    performance: {
      responseTime: 150000,
      throughput: 24,
      efficiency: 100,
      uptime: 100
    }
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
    totalRuntime: 7200, // 2 hours
    averageTaskTime: 60, // 1 minute
    errorCount: 0,
    queue: { todo: 5, inProgress: 1, done: 42, failed: 0 },
    performance: {
      responseTime: 60000,
      throughput: 21,
      efficiency: 99.2,
      uptime: 100
    }
  }
]

export const useAgentStore = create<AgentStore>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
        agents: defaultAgents.map(agent => ({
          ...agent,
          performance: calculatePerformance(agent)
        })),
        activeAgentCount: 2,
        metrics: {
          totalTasks: 0,
          activeTasks: 0,
          completedTasks: 0,
          failedTasks: 0,
          averageResponseTime: 0,
          overallSuccessRate: 0,
          systemUptime: 0
        },
        isInitialized: false,
        lastSync: null,

        // Core agent management
        setAgents: (agents) => {
          const enhancedAgents = agents.map(agent => ({
            ...agent,
            performance: calculatePerformance(agent)
          }))
          set({
            agents: enhancedAgents,
            activeAgentCount: enhancedAgents.filter(a => a.status === "active").length,
          })
          get().updateMetrics()
        },

        updateAgent: (id, updates) => {
          set((state) => {
            const updatedAgents = state.agents.map((agent) => {
              if (agent.id === id) {
                const updatedAgent = {
                  ...agent,
                  ...updates,
                  lastActivity: new Date(),
                  performance: calculatePerformance({ ...agent, ...updates })
                }
                return updatedAgent
              }
              return agent
            })

            return {
              agents: updatedAgents,
              activeAgentCount: updatedAgents.filter(a => a.status === "active").length,
            }
          })
          get().updateMetrics()
        },

        updateAgentByName: (name, updates) => {
          set((state) => {
            const updatedAgents = state.agents.map((agent) => {
              if (agent.name.toLowerCase() === name.toLowerCase()) {
                const updatedAgent = {
                  ...agent,
                  ...updates,
                  lastActivity: new Date(),
                  performance: calculatePerformance({ ...agent, ...updates })
                }
                return updatedAgent
              }
              return agent
            })

            return {
              agents: updatedAgents,
              activeAgentCount: updatedAgents.filter(a => a.status === "active").length,
            }
          })
          get().updateMetrics()
        },

        getAgentById: (id) => get().agents.find((agent) => agent.id === id),

        getAgentByName: (name) =>
          get().agents.find((agent) => agent.name.toLowerCase() === name.toLowerCase()),

        // Enhanced message handling
        updateAgentFromMessage: (message) => {
          const { agent_name, type, metadata, timestamp } = message
          if (!agent_name) return

          const agent = get().getAgentByName(agent_name)
          if (!agent) return

          let updates: Partial<Agent> = {
            lastActivity: new Date(timestamp),
          }

          switch (type) {
            case 'agent_status':
              if (metadata) {
                updates = {
                  ...updates,
                  status: metadata.status,
                  currentTask: metadata.task,
                }
              }
              break

            case 'agent_progress':
              if (metadata) {
                updates = {
                  ...updates,
                  progress: (metadata.current / metadata.total) * 100,
                  progress_stage: metadata.stage,
                  progress_current: metadata.current,
                  progress_total: metadata.total,
                  progress_estimated_time_remaining: metadata.estimated_time_remaining,
                  status: 'active'
                }
              }
              break

            case 'agent_thinking':
              updates = {
                ...updates,
                is_thinking: true,
                status: 'thinking'
              }
              break

            case 'agent_response':
              updates = {
                ...updates,
                is_thinking: false,
                status: 'active'
              }
              break

            case 'agent_error':
              updates = {
                ...updates,
                is_thinking: false,
                status: 'error',
                lastError: metadata?.error || 'Unknown error',
                errorCount: agent.errorCount + 1
              }
              break

            case 'task_complete':
              updates = {
                ...updates,
                tasksCompleted: agent.tasksCompleted + 1,
                queue: {
                  ...agent.queue,
                  inProgress: Math.max(0, agent.queue.inProgress - 1),
                  done: agent.queue.done + 1
                },
                status: 'idle'
              }
              break

            case 'task_start':
              updates = {
                ...updates,
                currentTask: metadata?.task || 'Working...',
                startTime: new Date(),
                queue: {
                  ...agent.queue,
                  todo: Math.max(0, agent.queue.todo - 1),
                  inProgress: agent.queue.inProgress + 1
                },
                status: 'active'
              }
              break
          }

          get().updateAgentByName(agent_name, updates)
        },

        handleAgentError: (agentName, error) => {
          const agent = get().getAgentByName(agentName)
          if (!agent) return

          const updates: Partial<Agent> = {
            status: "error",
            currentTask: error,
            lastError: error,
            errorCount: agent.errorCount + 1,
            queue: {
              ...agent.queue,
              inProgress: Math.max(0, agent.queue.inProgress - 1),
              failed: agent.queue.failed + 1
            }
          }
          get().updateAgentByName(agentName, updates)
        },

        // Enhanced functionality
        startAgentTask: (agentName, task) => {
          const agent = get().getAgentByName(agentName)
          if (!agent) return

          const updates: Partial<Agent> = {
            status: 'active',
            currentTask: task,
            startTime: new Date(),
            queue: {
              ...agent.queue,
              todo: Math.max(0, agent.queue.todo - 1),
              inProgress: agent.queue.inProgress + 1
            }
          }
          get().updateAgentByName(agentName, updates)
        },

        completeAgentTask: (agentName, success = true) => {
          const agent = get().getAgentByName(agentName)
          if (!agent) return

          const taskDuration = agent.startTime ?
            (Date.now() - agent.startTime.getTime()) / 1000 : agent.averageTaskTime

          const newAverageTime = agent.tasksCompleted > 0 ?
            (agent.averageTaskTime * agent.tasksCompleted + taskDuration) / (agent.tasksCompleted + 1) :
            taskDuration

          const updates: Partial<Agent> = {
            status: 'idle',
            currentTask: undefined,
            endTime: new Date(),
            tasksCompleted: success ? agent.tasksCompleted + 1 : agent.tasksCompleted,
            errorCount: success ? agent.errorCount : agent.errorCount + 1,
            averageTaskTime: newAverageTime,
            totalRuntime: agent.totalRuntime + taskDuration,
            queue: {
              ...agent.queue,
              inProgress: Math.max(0, agent.queue.inProgress - 1),
              done: success ? agent.queue.done + 1 : agent.queue.done,
              failed: success ? agent.queue.failed : agent.queue.failed + 1
            }
          }
          get().updateAgentByName(agentName, updates)
        },

        pauseAgent: (agentName) => {
          get().updateAgentByName(agentName, { status: 'paused' })
        },

        resumeAgent: (agentName) => {
          get().updateAgentByName(agentName, { status: 'active' })
        },

        resetAgent: (agentName) => {
          const defaultAgent = defaultAgents.find(a => a.name === agentName)
          if (defaultAgent) {
            get().updateAgentByName(agentName, {
              ...defaultAgent,
              performance: calculatePerformance(defaultAgent)
            })
          }
        },

        // Metrics and analytics
        updateMetrics: () => {
          const { agents } = get()
          const totalTasks = agents.reduce((sum, agent) => sum + agent.tasksCompleted, 0)
          const activeTasks = agents.filter(agent => agent.status === 'active').length
          const completedTasks = agents.reduce((sum, agent) => sum + agent.queue.done, 0)
          const failedTasks = agents.reduce((sum, agent) => sum + agent.queue.failed, 0)
          const avgResponseTime = agents.reduce((sum, agent) => sum + agent.performance.responseTime, 0) / agents.length
          const overallSuccessRate = agents.reduce((sum, agent) => sum + agent.successRate, 0) / agents.length
          const systemUptime = agents.reduce((sum, agent) => sum + agent.performance.uptime, 0) / agents.length

          set({
            metrics: {
              totalTasks,
              activeTasks,
              completedTasks,
              failedTasks,
              averageResponseTime: avgResponseTime,
              overallSuccessRate,
              systemUptime
            }
          })
        },

        getAgentPerformance: (agentName) => {
          const agent = get().getAgentByName(agentName)
          return agent?.performance || null
        },

        getSystemHealth: () => {
          const { agents } = get()
          const healthy = agents.filter(agent =>
            agent.status === 'active' || agent.status === 'idle'
          ).length
          const total = agents.length
          return {
            healthy,
            total,
            percentage: total > 0 ? (healthy / total) * 100 : 100
          }
        },

        // Persistence and sync
        syncWithBackend: async () => {
          try {
            const response = await fetch('/api/agents/status')
            if (response.ok) {
              const data = await response.json()
              if (data.agents) {
                get().setAgents(data.agents)
                set({ lastSync: new Date() })
              }
            }
          } catch (error) {
            console.error('Failed to sync with backend:', error)
          }
        },

        exportAgentData: () => {
          const { agents, metrics } = get()
          return JSON.stringify({ agents, metrics, exportDate: new Date() }, null, 2)
        },

        importAgentData: (data) => {
          try {
            const parsed = JSON.parse(data)
            if (parsed.agents) {
              get().setAgents(parsed.agents)
            }
          } catch (error) {
            console.error('Failed to import agent data:', error)
          }
        }
      }),
      {
        name: 'agent-store',
        storage: createJSONStorage(() => localStorage),
        partialize: (state) => ({
          agents: state.agents,
          metrics: state.metrics,
          lastSync: state.lastSync
        }),
        version: 1,
      }
    )
  )
)