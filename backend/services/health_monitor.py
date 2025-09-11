import time
from collections import deque

class ConnectionHealth:
    """Tracks health metrics for a WebSocket connection."""

    def __init__(self, client_id: str):
        self.client_id = client_id
        self.connected_at = time.time()
        self.last_heartbeat = time.time()
        self.last_message = time.time()
        self.messages_sent = 0
        self.messages_received = 0
        self.errors = 0
        self.disconnections = 0
        self.latency_samples = deque(maxlen=10)  # Keep last 10 latency measurements

    def record_message_sent(self):
        self.messages_sent += 1
        self.last_message = time.time()

    def record_message_received(self):
        self.messages_received += 1
        self.last_message = time.time()

    def record_heartbeat(self):
        self.last_heartbeat = time.time()

    def record_error(self):
        self.errors += 1

    def record_latency(self, latency_ms: float):
        self.latency_samples.append(latency_ms)

    def get_average_latency(self) -> float:
        if not self.latency_samples:
            return 0.0
        return sum(self.latency_samples) / len(self.latency_samples)

    def get_uptime(self) -> float:
        return time.time() - self.connected_at

    def is_healthy(self, heartbeat_timeout: float = 60.0) -> bool:
        """Check if connection is healthy based on recent heartbeat."""
        return (time.time() - self.last_heartbeat) < heartbeat_timeout
