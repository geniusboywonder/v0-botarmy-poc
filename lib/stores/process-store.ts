import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'
import type { ProcessStage, ProcessFlow, Task, Artifact, HITLRequest } from '@/lib/types'

interface ProcessState {
  // Current process flow
  currentFlow: ProcessFlow | null
  
  // Stages data
  stages: ProcessStage[]
  currentStageId: string | null
  
  // HITL requests
  hitlRequests: HITLRequest[]
  
  // Loading states
  isLoading: boolean
  error: string | null
}

interface ProcessActions {
  // Process flow actions
  setCurrentFlow: (flow: ProcessFlow) => void
  updateFlowStatus: (status: ProcessFlow['status']) => void
  
  // Stage actions
  setStages: (stages: ProcessStage[]) => void
  updateStage: (stageId: string, updates: Partial<ProcessStage>) => void
  setCurrentStage: (stageId: string) => void
  getStageByName: (name: string) => ProcessStage | undefined
  getStageById: (id: string) => ProcessStage | undefined
  
  // Task actions
  updateTask: (stageId: string, taskId: string, updates: Partial<Task>) => void
  addTask: (stageId: string, task: Task) => void
  removeTask: (stageId: string, taskId: string) => void
  
  // Artifact actions
  updateArtifact: (stageId: string, artifactId: string, updates: Partial<Artifact>) => void
  addArtifact: (stageId: string, artifact: Artifact) => void
  removeArtifact: (stageId: string, artifactId: string) => void
  
  // HITL actions
  addHITLRequest: (request: HITLRequest) => void
  respondToHITL: (requestId: string, response: any) => void
  removeHITLRequest: (requestId: string) => void
  
  // Control actions
  pauseStage: (stageId: string) => void
  resumeStage: (stageId: string) => void
  
  // Loading and error actions
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  
  // Utility actions
  reset: () => void
  initializeDemo: () => void
}

type ProcessStore = ProcessState & ProcessActions

// Initial demo data
const createDemoStages = (): ProcessStage[] => [
  // Requirements Stage
  {
    id: 'requirements',
    name: 'Requirements',
    description: 'Gather and analyze project requirements',
    status: 'done',
    agentName: 'Business Analyst',
    agentType: 'analyst',
    currentTask: 'Requirements analysis completed',
    hitlRequired: false,
    progress: 100,
    tasks: [
      {
        id: 'req-1',
        name: 'Gather initial requirements',
        status: 'done',
        assignedTo: 'Business Analyst',
        createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        completedAt: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        progress: 100
      },
      {
        id: 'req-2',
        name: 'Create user stories',
        status: 'done',
        assignedTo: 'Business Analyst',
        createdAt: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        completedAt: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        progress: 100
      },
      {
        id: 'req-3',
        name: 'Define acceptance criteria',
        status: 'done',
        assignedTo: 'Business Analyst',
        createdAt: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        completedAt: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
        progress: 100
      }
    ],
    artifacts: [
      {
        id: 'req-doc-1',
        name: 'Requirements Document',
        type: 'document',
        status: 'done',
        createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        createdBy: 'Business Analyst',
        downloadUrl: '/api/artifacts/req-doc-1'
      },
      {
        id: 'user-stories-1',
        name: 'User Stories',
        type: 'document',
        status: 'done',
        createdAt: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        createdBy: 'Business Analyst',
        downloadUrl: '/api/artifacts/user-stories-1'
      }
    ],
    startedAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    completedAt: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
    estimatedDuration: 2 * 60 * 60 * 1000,
    nextStage: 'design'
  },

  // Design Stage  
  {
    id: 'design',
    name: 'Design',
    description: 'Create system architecture and design specifications',
    status: 'wip',
    agentName: 'System Architect',
    agentType: 'architect',
    currentTask: 'Creating database schema and API specifications',
    hitlRequired: true,
    progress: 65,
    tasks: [
      {
        id: 'design-1',
        name: 'Create system architecture',
        status: 'done',
        assignedTo: 'System Architect',
        createdAt: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        completedAt: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
        progress: 100
      },
      {
        id: 'design-2',
        name: 'Design database schema',
        status: 'wip',
        assignedTo: 'System Architect',
        createdAt: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
        progress: 80
      },
      {
        id: 'design-3',
        name: 'Create API specifications',
        status: 'todo',
        assignedTo: 'System Architect',
        createdAt: new Date().toISOString(),
        progress: 0
      }
    ],
    artifacts: [
      {
        id: 'arch-diagram-1',
        name: 'System Architecture Diagram',
        type: 'diagram',
        status: 'done',
        createdAt: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
        createdBy: 'System Architect',
        downloadUrl: '/api/artifacts/arch-diagram-1'
      }
    ],
    startedAt: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
    estimatedDuration: 3 * 60 * 60 * 1000,
    nextStage: 'development'
  },

  // Development Stage
  {
    id: 'development', 
    name: 'Development',
    description: 'Implement the solution based on design specifications',
    status: 'queued',
    agentName: 'Full Stack Developer',
    agentType: 'developer',
    currentTask: 'Waiting for design approval',
    hitlRequired: false,
    progress: 0,
    tasks: [
      {
        id: 'dev-1',
        name: 'Set up development environment',
        status: 'todo',
        assignedTo: 'Full Stack Developer',
        createdAt: new Date().toISOString(),
        progress: 0
      },
      {
        id: 'dev-2',
        name: 'Implement backend APIs',
        status: 'todo',
        assignedTo: 'Full Stack Developer',
        createdAt: new Date().toISOString(),
        progress: 0
      },
      {
        id: 'dev-3',
        name: 'Create frontend components',
        status: 'todo',
        assignedTo: 'Full Stack Developer',
        createdAt: new Date().toISOString(),
        progress: 0
      }
    ],
    artifacts: [],
    startedAt: undefined,
    estimatedDuration: 6 * 60 * 60 * 1000,
    nextStage: 'testing'
  },

  // Testing Stage
  {
    id: 'testing',
    name: 'Testing', 
    description: 'Validate solution quality and functionality',
    status: 'queued',
    agentName: 'QA Engineer',
    agentType: 'tester',
    currentTask: 'Waiting for development completion',
    hitlRequired: false,
    progress: 0,
    tasks: [
      {
        id: 'test-1',
        name: 'Create test plan',
        status: 'todo',
        assignedTo: 'QA Engineer', 
        createdAt: new Date().toISOString(),
        progress: 0
      },
      {
        id: 'test-2',
        name: 'Execute unit tests',
        status: 'todo',
        assignedTo: 'QA Engineer',
        createdAt: new Date().toISOString(),
        progress: 0
      },
      {
        id: 'test-3',
        name: 'Perform integration testing',
        status: 'todo',
        assignedTo: 'QA Engineer',
        createdAt: new Date().toISOString(),
        progress: 0
      }
    ],
    artifacts: [],
    startedAt: undefined,
    estimatedDuration: 4 * 60 * 60 * 1000,
    nextStage: 'deployment'
  },

  // Deployment Stage
  {
    id: 'deployment',
    name: 'Deployment',
    description: 'Deploy solution to production environment',
    status: 'queued', 
    agentName: 'DevOps Engineer',
    agentType: 'deployer',
    currentTask: 'Waiting for testing completion',
    hitlRequired: false,
    progress: 0,
    tasks: [
      {
        id: 'deploy-1',
        name: 'Prepare deployment environment',
        status: 'todo',
        assignedTo: 'DevOps Engineer',
        createdAt: new Date().toISOString(),
        progress: 0
      },
      {
        id: 'deploy-2', 
        name: 'Deploy to staging',
        status: 'todo',
        assignedTo: 'DevOps Engineer',
        createdAt: new Date().toISOString(),
        progress: 0
      },
      {
        id: 'deploy-3',
        name: 'Deploy to production',
        status: 'todo',
        assignedTo: 'DevOps Engineer',
        createdAt: new Date().toISOString(),
        progress: 0
      }
    ],
    artifacts: [],
    startedAt: undefined,
    estimatedDuration: 2 * 60 * 60 * 1000,
    nextStage: undefined
  }
]

const initialState: ProcessState = {
  currentFlow: null,
  stages: [],
  currentStageId: null,
  hitlRequests: [],
  isLoading: false,
  error: null
}

export const useProcessStore = create<ProcessStore>()(
  subscribeWithSelector((set, get) => ({
    ...initialState,

    // Process flow actions
    setCurrentFlow: (flow) => set({ currentFlow: flow }),
    
    updateFlowStatus: (status) => set((state) => ({
      currentFlow: state.currentFlow ? { ...state.currentFlow, status } : null
    })),

    // Stage actions
    setStages: (stages) => set({ stages }),
    
    updateStage: (stageId, updates) => set((state) => ({
      stages: state.stages.map(stage => 
        stage.id === stageId ? { ...stage, ...updates } : stage
      )
    })),
    
    setCurrentStage: (stageId) => set({ currentStageId: stageId }),
    
    getStageByName: (name) => get().stages.find(stage => 
      stage.name.toLowerCase() === name.toLowerCase()
    ),
    
    getStageById: (id) => get().stages.find(stage => stage.id === id),

    // Task actions
    updateTask: (stageId, taskId, updates) => set((state) => ({
      stages: state.stages.map(stage => 
        stage.id === stageId 
          ? {
              ...stage,
              tasks: stage.tasks.map(task =>
                task.id === taskId ? { ...task, ...updates } : task
              )
            }
          : stage
      )
    })),
    
    addTask: (stageId, task) => set((state) => ({
      stages: state.stages.map(stage => 
        stage.id === stageId 
          ? { ...stage, tasks: [...stage.tasks, task] }
          : stage
      )
    })),
    
    removeTask: (stageId, taskId) => set((state) => ({
      stages: state.stages.map(stage => 
        stage.id === stageId 
          ? { ...stage, tasks: stage.tasks.filter(task => task.id !== taskId) }
          : stage
      )
    })),

    // Artifact actions
    updateArtifact: (stageId, artifactId, updates) => set((state) => ({
      stages: state.stages.map(stage => 
        stage.id === stageId 
          ? {
              ...stage,
              artifacts: stage.artifacts.map(artifact =>
                artifact.id === artifactId ? { ...artifact, ...updates } : artifact
              )
            }
          : stage
      )
    })),
    
    addArtifact: (stageId, artifact) => set((state) => ({
      stages: state.stages.map(stage => 
        stage.id === stageId 
          ? { ...stage, artifacts: [...stage.artifacts, artifact] }
          : stage
      )
    })),
    
    removeArtifact: (stageId, artifactId) => set((state) => ({
      stages: state.stages.map(stage => 
        stage.id === stageId 
          ? { ...stage, artifacts: stage.artifacts.filter(artifact => artifact.id !== artifactId) }
          : stage
      )
    })),

    // HITL actions
    addHITLRequest: (request) => set((state) => ({
      hitlRequests: [...state.hitlRequests, request]
    })),
    
    respondToHITL: (requestId, response) => set((state) => ({
      hitlRequests: state.hitlRequests.map(request =>
        request.id === requestId 
          ? { ...request, status: 'responded', response, respondedAt: new Date().toISOString() }
          : request
      )
    })),
    
    removeHITLRequest: (requestId) => set((state) => ({
      hitlRequests: state.hitlRequests.filter(request => request.id !== requestId)
    })),

    // Control actions
    pauseStage: (stageId) => set((state) => ({
      stages: state.stages.map(stage => 
        stage.id === stageId ? { ...stage, status: 'waiting' as const } : stage
      )
    })),
    
    resumeStage: (stageId) => set((state) => ({
      stages: state.stages.map(stage => 
        stage.id === stageId ? { ...stage, status: 'wip' as const } : stage
      )
    })),

    // Loading and error actions
    setLoading: (loading) => set({ isLoading: loading }),
    setError: (error) => set({ error }),

    // Utility actions
    reset: () => set(initialState),
    
    initializeDemo: () => {
      const demoStages = createDemoStages()
      set({
        stages: demoStages,
        currentStageId: 'requirements'
      })
    }
  }))
)

// Initialize demo data on store creation
useProcessStore.getState().initializeDemo()
