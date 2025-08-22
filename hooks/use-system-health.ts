import { useState, useEffect } from 'react';
import { websocketService } from '@/lib/websocket/websocket-service';

export type ServiceStatus = 'operational' | 'degraded' | 'outage';

export interface SystemHealth {
  backend: ServiceStatus;
  websocket: ServiceStatus;
}

export function useSystemHealth() {
  const [health, setHealth] = useState<SystemHealth>({
    backend: 'operational',
    websocket: 'operational',
  });

  useEffect(() => {
    const checkHealth = () => {
      // Backend health check (dummy)
      // In a real app, this would be an API call
      const backendHealth = Math.random() > 0.1 ? 'operational' : 'degraded';

      // WebSocket health check
      const wsStatus = websocketService.getConnectionStatus();
      const websocketHealth = wsStatus.connected ? 'operational' : 'outage';

      setHealth({
        backend: backendHealth,
        websocket: websocketHealth,
      });
    };

    const interval = setInterval(checkHealth, 5000); // Check every 5 seconds
    checkHealth(); // Initial check

    return () => clearInterval(interval);
  }, []);

  return health;
}
