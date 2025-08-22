"use client"

import { usePerformanceMetrics } from "@/hooks/use-performance-metrics"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function PerformanceMetricsOverlay() {
  const metrics = usePerformanceMetrics()

  const formatUptime = (seconds: number) => {
    const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
    const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
    const s = Math.floor(seconds % 60).toString().padStart(2, '0');
    return `${h}:${m}:${s}`;
  }

  return (
    <Card className="fixed bottom-4 right-4 w-72 bg-background/80 backdrop-blur-sm z-50">
      <CardHeader>
        <CardTitle className="text-sm">Performance Metrics</CardTitle>
      </CardHeader>
      <CardContent className="text-xs space-y-2">
        <div className="flex justify-between">
          <span>Message Count:</span>
          <span>{metrics.messageCount}</span>
        </div>
        <div className="flex justify-between">
          <span>Avg. Latency:</span>
          <span>{metrics.averageLatency.toFixed(2)} ms</span>
        </div>
        <div className="flex justify-between">
          <span>Uptime:</span>
          <span>{formatUptime(metrics.uptime)}</span>
        </div>
      </CardContent>
    </Card>
  )
}
