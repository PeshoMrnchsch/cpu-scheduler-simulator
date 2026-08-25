from src.model.process import Process
from src.scheduler_algorithms.SchedulerInterface import SchedulerInterface

class RoundRobin_Scheduler(SchedulerInterface):
    """
    Round Robin scheduler with preemption.
    Each process gets a time quantum to execute before being moved to the back of the queue.
    """
    def __init__(self, quantum: int = 2):
        if quantum <=0:
            raise ValueError("Quantum must be more than 0")
        
        self.quantum = quantum
        self.time_used_in_slice = 0  
    
        
    def select_next(self, ready_queue: list[Process]) -> Process | None:
        """
        Returns the first process (FIFO order).
        """
        
        if not ready_queue:
            return None
        return ready_queue[0]
    
    def on_time_unit(self):
        """Increment internal CPU time used in slice"""
        self.time_used_in_slice += 1
        
    def should_preempt(self, current_process=None, ready_queue=None):
        return self.time_used_in_slice >= self.quantum
    
    def reset(self):
        self.time_used_in_slice=0
    
    def get_name(self):
        return "Round Robin"