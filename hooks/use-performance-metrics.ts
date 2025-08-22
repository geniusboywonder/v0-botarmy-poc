import { useState, useEffect } from 'react';
import { useLogStore } from '@/lib/stores/log-store';

export interface PerformanceMetrics {
  messageCount: number;
  averageLatency: number;
  uptime: number;
}

export function usePerformanceMetrics() {
  const [metrics, setMetrics] = useState<PerformanceMetrics>({
    messageCount: 0,
    averageLatency: 0,
    uptime: 0,
  });

  const logs = useLogStore((state) => state.logs);

  useEffect(() => {
    const startTime = Date.now();

    const interval = setInterval(() => {
      const now = Date.now();
      const uptimeInSeconds = Math.floor((now - startTime) / 1000);

      // Dummy latency calculation
      const latencies = logs.map(log => Math.random() * 100);
      const averageLatency = latencies.reduce((a, b) => a + b, 0) / (latencies.length || 1);

      setMetrics({
        messageCount: logs.length,
        averageLatency: averageLatency,
        uptime: uptimeInSeconds,
      });
    }, 1000); // Update every second

    return () => clearInterval(interval);
  }, [logs]);

  return metrics;
}
