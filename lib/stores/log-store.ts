import { create } from "zustand"

export interface LogEntry {
  id: string
  timestamp: Date
  agent: string
  level: "info" | "warning" | "error" | "success"
  message: string
  task?: string
  metadata?: Record<string, any>
}

interface LogStore {
  logs: LogEntry[]
  addLog: (log: Omit<LogEntry, "id" | "timestamp">) => void
  clearLogs: () => void
  getLogsByAgent: (agent: string) => LogEntry[]
  getLogsByLevel: (level: LogEntry["level"]) => LogEntry[]
}

export const useLogStore = create<LogStore>((set, get) => ({
  logs: [
    {
      id: "1",
      timestamp: new Date(Date.now() - 300000),
      agent: "Analyst",
      level: "success",
      message: "Requirements analysis completed successfully",
      task: "Analyze Requirements Document",
      metadata: { duration: "45m", confidence: 0.94 },
    },
    {
      id: "2",
      timestamp: new Date(Date.now() - 240000),
      agent: "Architect",
      level: "info",
      message: "Starting system architecture design",
      task: "Design System Architecture",
      metadata: { complexity: "medium" },
    },
    {
      id: "3",
      timestamp: new Date(Date.now() - 180000),
      agent: "Developer",
      level: "info",
      message: "Implementing authentication middleware",
      task: "Implement User Authentication",
      metadata: { progress: 0.45 },
    },
    {
      id: "4",
      timestamp: new Date(Date.now() - 120000),
      agent: "Monitor",
      level: "warning",
      message: "High memory usage detected on Developer agent",
      metadata: { memory_usage: "85%" },
    },
    {
      id: "5",
      timestamp: new Date(Date.now() - 60000),
      agent: "Developer",
      level: "error",
      message: "Database connection timeout during authentication setup",
      task: "Implement User Authentication",
      metadata: { error_code: "DB_TIMEOUT", retry_count: 2 },
    },
  ],
  addLog: (log) =>
    set((state) => ({
      logs: [
        {
          ...log,
          id: Date.now().toString(),
          timestamp: new Date(),
        },
        ...state.logs,
      ].slice(0, 1000), // Keep only last 1000 logs
    })),
  clearLogs: () => set({ logs: [] }),
  getLogsByAgent: (agent) => get().logs.filter((log) => log.agent === agent),
  getLogsByLevel: (level) => get().logs.filter((log) => log.level === level),
}))
