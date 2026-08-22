from enum import Enum, auto

class ProcessState(Enum):
    NEW = auto()
    READY = auto()
    RUNNING = auto()
    TERMINATED = auto()
    
class Process:
    def __init__(self, process_id: int | str, arrival_time : int,burst_time : int, priority=0):
        self.pid = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        self.state = ProcessState.NEW
        self.remaining_time = self.burst_time
        self.start=None
        self.completion=None
        
    def reset(self):
        self.state = ProcessState.NEW
        self.remaining_time = self.burst_time
        self.start = None
        self.completion = None
    
    # def execute(self, time_step, current_time):
    #     """Executes a command for editing the remaining and start time"""
    #     if self.start is None:
    #         self.start = current_time
    #     self.remaining -= time_step
        
    #     if self.remaining <= 0:
    #         self.remaining = 0
    #         self.completion = current_time + time_step
    
    def is_completed(self):
        """Returns if process is completed;"""
        return self.remaining_time == 0
    
    def __repr__(self):
        return f"Process (P{self.pid}, State={self.state.name}, Rem={self.remaining_time}/{self.burst_time}, {self.priority})"
    
    
    
process1 = Process(process_id=11, arrival_time=0, burst_time=5)
print(process1) 