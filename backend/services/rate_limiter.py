import time
from collections import defaultdict, deque
from typing import Dict

class RateLimiter:
    def __init__(self, rate_limit_window: float = 60.0, rate_limit_max_messages: int = 100):
        self.rate_limits: Dict[str, deque] = defaultdict(lambda: deque(maxlen=rate_limit_max_messages))
        self.rate_limit_window = rate_limit_window
        self.rate_limit_max_messages = rate_limit_max_messages

    def check_rate_limit(self, client_id: str) -> bool:
        now = time.time()
        window_start = now - self.rate_limit_window

        client_history = self.rate_limits[client_id]
        while client_history and client_history[0] < window_start:
            client_history.popleft()

        if len(client_history) >= self.rate_limit_max_messages:
            return False

        client_history.append(now)
        return True
