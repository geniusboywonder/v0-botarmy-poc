import { create } from "zustand"

export interface Task {
  id: string
  name: string
  agent: string
  status: "pending" | "in-progress" | "completed" | "failed"
  priority: "low" | "medium" | "high"
  progress: number
  startTime: Date
  estimatedCompletion?: Date
  dependencies?: string[]
}

interface TaskStore {
  tasks: Task[]
  addTask: (task: Omit<Task, "id">) => void
  updateTask: (id: string, updates: Partial<Task>) => void
  removeTask: (id: string) => void
  getTasksByAgent: (agent: string) => Task[]
  getTasksByStatus: (status: Task["status"]) => Task[]
}

export const useTaskStore = create<TaskStore>((set, get) => ({
  tasks: [
    {
      id: "1",
      name: "Analyze Requirements Document",
      agent: "Analyst",
      status: "completed",
      priority: "high",
      progress: 100,
      startTime: new Date(Date.now() - 3600000),
      estimatedCompletion: new Date(Date.now() - 1800000),
    },
    {
      id: "2",
      name: "Design System Architecture",
      agent: "Architect",
      status: "in-progress",
      priority: "high",
      progress: 75,
      startTime: new Date(Date.now() - 1800000),
      estimatedCompletion: new Date(Date.now() + 900000),
      dependencies: ["1"],
    },
    {
      id: "3",
      name: "Implement User Authentication",
      agent: "Developer",
      status: "in-progress",
      priority: "medium",
      progress: 45,
      startTime: new Date(Date.now() - 900000),
      estimatedCompletion: new Date(Date.now() + 1800000),
      dependencies: ["2"],
    },
    {
      id: "4",
      name: "Write Unit Tests",
      agent: "Tester",
      status: "pending",
      priority: "medium",
      progress: 0,
      startTime: new Date(),
      dependencies: ["3"],
    },
    {
      id: "5",
      name: "Deploy to Staging",
      agent: "Deployer",
      status: "pending",
      priority: "low",
      progress: 0,
      startTime: new Date(),
      dependencies: ["4"],
    },
  ],
  addTask: (task) =>
    set((state) => ({
      tasks: [...state.tasks, { ...task, id: Date.now().toString() }],
    })),
  updateTask: (id, updates) =>
    set((state) => ({
      tasks: state.tasks.map((task) => (task.id === id ? { ...task, ...updates } : task)),
    })),
  removeTask: (id) =>
    set((state) => ({
      tasks: state.tasks.filter((task) => task.id !== id),
    })),
  getTasksByAgent: (agent) => get().tasks.filter((task) => task.agent === agent),
  getTasksByStatus: (status) => get().tasks.filter((task) => task.status === status),
}))
