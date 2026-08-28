from src.model.io_request import IORequest

class IODeviceQueue: # Holds requests waiting for the device
    def __init__(self):
        self.queue: list[IORequest] = []
        
    def get_queue(self) -> list[IORequest] | None:
        if not self.queue:
            return None
        
        return self.queue
    
    def enqueue(self, request: IORequest) -> None:
        """Add a request to the queue."""
        self.queue.append(request)
        
    def dequeue(self)-> IORequest|None:
        """Remove and return the next request."""
        if not self.queue:
            return None
        
        return self.queue.pop(0)
    
    def has_pending(self) -> bool:
        """Return True if requests are waiting."""
        return len(self.queue) > 0

    def get_queue_depth(self) -> int:
        """Return the number of waiting requests."""
        return len(self.queue)
    
    def clear(self) -> None:
        """Remove all pending requests."""
        self.queue.clear()

    def __repr__(self) -> str:
        return f"IODeviceQueue({len(self.queue)} pending)"