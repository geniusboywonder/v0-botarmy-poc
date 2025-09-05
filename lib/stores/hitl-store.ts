import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

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
          get().filterChatByAgent(request.agentName);
        }
      },

      // This is a placeholder. The actual implementation will depend on the chat UI.
      filterChatByAgent: (agentName) => {
        console.log(`Filtering chat by agent: ${agentName}`);
        // In a real application, this would interact with the chat store or component state.
      },
    }),
    {
      name: 'hitl-store',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        requests: state.requests,
        // Don't persist activeRequest as it's a UI state
      }),
      version: 1,
    }
  )
);
