import { create } from 'zustand';

export interface Alert {
  id: string;
  message: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  stage?: string;
}

interface NotificationState {
  alerts: Alert[];
  addAlert: (alert: Alert) => void;
  dismissAlert: (alertId: string) => void;
  clearAlerts: () => void;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  alerts: [
    {
      id: 'hitl-001',
      message: 'System design needs human approval before implementation',
      priority: 'high' as const,
      stage: 'Design'
    },
    {
      id: 'hitl-002', 
      message: 'Bug reports require human triage and prioritization',
      priority: 'urgent' as const,
      stage: 'Validate'
    }
  ],
  addAlert: (alert) =>
    set((state) => ({
      alerts: [...state.alerts, alert],
    })),
  dismissAlert: (alertId) =>
    set((state) => ({
      alerts: state.alerts.filter((a) => a.id !== alertId),
    })),
  clearAlerts: () => set({ alerts: [] }),
}));
