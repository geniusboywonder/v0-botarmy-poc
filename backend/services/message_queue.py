from typing import Dict, List

class MessageQueue:
    def __init__(self, max_queue_size: int = 100):
        self.message_queue: Dict[str, List[str]] = {}
        self.max_queue_size = max_queue_size

    def queue_message(self, client_id: str, message: str):
        if client_id not in self.message_queue:
            self.message_queue[client_id] = []

        if len(self.message_queue[client_id]) >= self.max_queue_size:
            self.message_queue[client_id].pop(0)  # Remove oldest message

        self.message_queue[client_id].append(message)

    def get_queued_messages(self, client_id: str) -> List[str]:
        return self.message_queue.pop(client_id, [])

    def has_queued_messages(self, client_id: str) -> bool:
        return client_id in self.message_queue and len(self.message_queue[client_id]) > 0
