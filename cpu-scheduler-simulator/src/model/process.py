from enum import Enum, auto

from src.model.io_request import IORequest

class ProcessState(Enum):
    NEW = auto()
    READY = auto()
    RUNNING = auto()
    TERMINATED = auto()
    IO_WAIT = auto()
    
class Process:
    def __init__(
        self,
        process_id: int | str,
        arrival_time: int,
        burst_time: int,
        io_requests: list[IORequest] | None = None
    ):
        self.pid = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time

        # Process state
        self.state = ProcessState.NEW
        self.remaining_time = self.burst_time

        # Timing
        self.start=None
        self.completion_time=None
        
        # I/O configuration
        self.io_requests = io_requests or [] # All I/O operations
        
        # I/O runtime state
        self.current_io_index = 0 # Which I/O we're on (tracks progress)
        self.io_in_progress: IORequest | None = None
        
        # I/O metrics
        total_io_wait_time = 0 # Accumulate for metrics
        
    
    # IO Methods - Process knows when it needs I/O
    def get_next_io_request(self) -> IORequest | None:
        """Return the next planned I/O request."""
        
        if self.current_io_index >= len(self.io_requests):
            return None

        return self.io_requests[self.current_io_index]
    
    def should_request_io(self) -> bool : 
        """
        Checks if the process has reached the 
        execution point the next I/O request.
        """
        next_io = self.get_next_io_request()
        
        if next_io is None:
            return False
        
        expected_cpu_time = self.burst_time - self.remaining_time
        return expected_cpu_time == next_io.execution_point
    
    def start_io(self) -> IORequest | None:
        """
        Marks the next request as active.
        """
        request = self.get_next_io_request()
        
        if not request:
            return None
        
        self.io_in_progress=request
        self.current_io_index += 1
        return request
    
    def finish_io(self) -> None:
        """
        Call when the device completes the I/O
        """
        
        self.io_in_progress=None    
    
    def get_next_io_execution_point() -> int | None:
        
        # When (in CPU time) is the next I/O?
        # Useful for lookahead in scheduler)
        pass
    
    
    def reset(self):
            self.state = ProcessState.NEW
            self.remaining_time = self.burst_time
            self.start = None
            self.completion_time = None          
            
    def is_completed(self):
        """Returns if process is completed;"""
        return self.remaining_time == 0
    
    def __repr__(self):
        return f"Process (P{self.pid}, State={self.state.name}, Rem={self.remaining_time}/{self.burst_time})"
    
    
    
process1 = Process(process_id=11, arrival_time=0, burst_time=5)
print(process1) 