from abc import ABC, abstractmethod
from src.model.process import Process, ProcessState

class SchedulerInterface(ABC):

    @abstractmethod
    def select_next(self, ready_queue: list[Process]) -> Process | None:
        """Every scheduler implements this method to pick the next process."""
        pass
    
    @abstractmethod
    def on_time_unit(self):
        """Update internal state after CPU time unit"""
        pass
    
    @abstractmethod
    def should_preempt(\
        self,
        current_process: Process,
        ready_queue: list[Process]
        )-> bool:
        """Return True if the current process should be preempted."""
        pass
    
    @abstractmethod
    def reset(self):
        """Reset scheduler state for a new time slice/process."""
        pass