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

let logQueue: Omit<LogEntry, "id" | "timestamp">[] = [];
let debounceTimer: NodeJS.Timeout | null = null;

export const useLogStore = create<LogStore>((set, get) => ({
  logs: [],
  addLog: (log) => {
    logQueue.push(log);
    if (!debounceTimer) {
      debounceTimer = setTimeout(() => {
        set((state) => ({
          logs: [
            ...state.logs,
            ...logQueue.map(l => ({ ...l, id: Date.now().toString(), timestamp: new Date() }))
          ].slice(-1000)
        }));
        logQueue = [];
        debounceTimer = null;
      }, 100);
    }
  },
  clearLogs: () => set({ logs: [] }),
  getLogsByAgent: (agent) => get().logs.filter((log) => log.agent === agent),
  getLogsByLevel: (level) => get().logs.filter((log) => log.level === level),
}))
