import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { useSystemHealth } from './use-system-health';
import { websocketService } from '@/lib/websocket/websocket-service';
import { useAgentStore } from '@/lib/stores/agent-store';
import { useLogStore } from '@/lib/stores/log-store';

// Mock all external dependencies
vi.mock('@/lib/websocket/websocket-service');
vi.mock('@/lib/stores/agent-store');
vi.mock('@/lib/stores/log-store');

// Mock global fetch
const mockFetch = vi.fn();
vi.stubGlobal('fetch', mockFetch);

describe('useSystemHealth Hook', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.clearAllMocks();

    // Mock dependencies' return values
    (websocketService.getConnectionStatus as vi.Mock).mockReturnValue({ connected: true });
    (useAgentStore as any).getState = vi.fn().mockReturnValue({
      getSystemHealth: () => ({ percentage: 100, total: 5, healthy: 5 }),
      agents: [{ status: 'active' }],
    });
    (useLogStore as any).getState = vi.fn().mockReturnValue({
      getRecentLogs: () => [],
    });

    // Mock a successful fetch response for the backend health check
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'healthy' }),
    });
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it('should start monitoring automatically and perform an initial health check', async () => {
    // Arrange & Act
    const { result } = renderHook(() => useSystemHealth({ autoStart: true, services: ['backend'] }));

    // Let the initial async operations in the hook complete
    await act(async () => {
      vi.runAllTimers();
    });

    // Assert
    expect(result.current.isMonitoring).toBe(true);
    expect(mockFetch).toHaveBeenCalledWith('/api/health', expect.any(Object));
    expect(result.current.health.overall).toBe('healthy');
    expect(result.current.health.services).toHaveLength(1);
    expect(result.current.health.services[0].status).toBe('healthy');
  });

  it('should update health status based on service checks', async () => {
    // Arrange
    // Make the backend check return 'unhealthy'
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error'
    });

    const { result } = renderHook(() => useSystemHealth({ services: ['backend', 'websocket'] }));

    // Act
    await act(async () => {
      vi.runAllTimers();
    });

    // Assert
    expect(result.current.health.overall).toBe('unhealthy');
    expect(result.current.health.services).toHaveLength(2);
    const backendService = result.current.health.services.find(s => s.name === 'Backend API');
    const websocketService = result.current.health.services.find(s => s.name === 'WebSocket');
    expect(backendService?.status).toBe('unhealthy');
    expect(websocketService?.status).toBe('healthy');
  });

  it('should perform health checks at the specified interval', async () => {
    // Arrange
    const { result } = renderHook(() => useSystemHealth({ refreshInterval: 5000, services: ['backend'] }));

    // Act: Initial check
    await act(async () => {
      vi.runAllTimers();
    });
    expect(mockFetch).toHaveBeenCalledTimes(1);

    // Act: Advance time to trigger the next interval
    await act(async () => {
      vi.advanceTimersByTime(5000);
    });

    // Assert
    expect(mockFetch).toHaveBeenCalledTimes(2);
  });
});
