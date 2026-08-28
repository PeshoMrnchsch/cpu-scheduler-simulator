from abc import ABC, abstractmethod

from src.model.io_request import IORequest
from src.devices.io_device_queue import IODeviceQueue


class IODevice():  # Executes the I/O

    def __init__(self, device_id: str, device_type: str):
        self.device_id = device_id
        self.device_type = device_type

        self.queue = IODeviceQueue()
        self.current_io: IORequest | None = None
        self.remaining_time = 0

        self.total_processed = 0
        self.total_wait_time = 0

    
    # @abstractmethod
    def step(self) -> IORequest | None:
        """
        Advance the device by one simulation time unit.
        
        Returns:
            The completed I/O request, or None if nothing completed.
        """
        
        # Nothing currently running -> try to start one
        if self.current_io is None:
            self.start_next()
            
            if self.current_io is None:
                return None
        
        # Execute one time unit
        self.remaining_time  -= 1
        
        # I/O finished
        if self.remaining_time <= 0:
            completed_request = self.current_io
            
            self.current_io = None
            self.remaining_time = 0

            self.total_processed += 1
    
            return completed_request
    
    
    def enqueue(self, request: IORequest) -> None:
        """Add an I/O request to the device."""
        self.queue.enqueue(request)


    def dequeue(self) -> IORequest | None:
        """Remove the next request from the device queue."""
        return self.queue.dequeue()

    def start_next(self) -> bool:
        """Start the next waiting I/O request."""
        if self.current_io is not None:
            return False

        request = self.dequeue()
        
        if request is None:
            return False
        
        self.current_io = request
        self.remaining_time = request.duration
        
        return True

    
    def has_pending(self) -> bool:
        return self.queue.get_queue_depth() > 0
    
    def is_busy(self)->bool:
        return self.current_io is not None

    def get_queue_depth(self) -> int:
        return self.queue.get_queue_depth()
    
    def get_active_request(self) -> IORequest | None:
        return self.current_io

    def reset(self) -> None:
        self.queue.clear()
        self.current_io = None
        self.remaining_time = 0
        self.total_processed = 0
        self.total_wait_time = 0
        
        
    def __repr__(self) -> str:
        return (
            f"{self.device_type.capitalize()}({self.device_id}): "
            f"{self.get_queue_depth()} queued"
        )