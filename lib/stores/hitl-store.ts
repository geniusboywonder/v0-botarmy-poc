import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

// Safe storage implementation with error handling
const createSafeStorage = () => {
  const storage = {
    getItem: (name: string): string | null => {
      try {
        if (typeof window === 'undefined') return null
        return window.localStorage.getItem(name)
      } catch (error) {
        console.warn(`Failed to read from localStorage: ${error}`)
        return null
      }
    },
    setItem: (name: string, value: string): void => {
      try {
        if (typeof window === 'undefined') return
        window.localStorage.setItem(name, value)
      } catch (error) {
        console.warn(`Failed to write to localStorage: ${error}`)
        if (error instanceof DOMException && error.code === 22) {
          try {
            window.localStorage.clear()
            window.localStorage.setItem(name, value)
          } catch (retryError) {
            console.error('localStorage completely unavailable:', retryError)
          }
        }
      }
    },
    removeItem: (name: string): void => {
      try {
        if (typeof window === 'undefined') return
        window.localStorage.removeItem(name)
      } catch (error) {
        console.warn(`Failed to remove from localStorage: ${error}`)
      }
    }
  }
  return storage
}

interface HITLRequest {
  id: string;
  agentName: string;
  decision: string;
  context: any;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  timestamp: Date;
  status: 'pending' | 'approved' | 'rejected' | 'modified';
  response?: string;
}

interface HITLStore {
  requests: HITLRequest[];
  activeRequest: HITLRequest | null;

  addRequest: (request: Omit<HITLRequest, 'id' | 'timestamp' | 'status'>) => void;
  resolveRequest: (id: string, status: 'approved' | 'rejected' | 'modified', response?: string) => void;
  getRequestsByAgent: (agentName: string) => HITLRequest[];
  getPendingCount: () => number;

  // Navigation helpers
  navigateToRequest: (id: string) => void;
  filterChatByAgent: (agentName: string) => void;
}

export const useHITLStore = create<HITLStore>()(
  persist(
    (set, get) => ({
      requests: [],
      activeRequest: null,

      addRequest: (request) => {
        const newRequest: HITLRequest = {
          ...request,
          id: `hitl-${Date.now()}-${Math.random()}`,
          timestamp: new Date(),
          status: 'pending',
        };
        set((state) => ({ requests: [...state.requests, newRequest] }));
      },

      resolveRequest: (id, status, response) => {
        set((state) => ({
          requests: state.requests.map((req) =>
            req.id === id ? { ...req, status, response } : req
          ),
          activeRequest: state.activeRequest?.id === id ? null : state.activeRequest,
        }));
      },

      getRequestsByAgent: (agentName) => {
        return get().requests.filter((req) => req.agentName === agentName);
      },

      getPendingCount: () => {
        return get().requests.filter((req) => req.status === 'pending').length;
      },

      navigateToRequest: (id) => {
        const request = get().requests.find((req) => req.id === id);
        if (request) {
          set({ activeRequest: request });
        }
      },

      // Chat filtering is handled by the chat component's agent filter state
      filterChatByAgent: (agentName) => {
        // This is handled by the chat component's useEffect that responds to activeRequest changes
        console.log(`Chat should filter by agent: ${agentName}`);
      },
    }),
    {
      name: 'hitl-store',
      storage: createJSONStorage(() => createSafeStorage()),
      partialize: (state) => ({
        requests: state.requests,
        // Don't persist activeRequest as it's a UI state
      }),
      version: 1,
    }
  )
);
