from abc import ABC, abstractmethod

from src.model.process import Process
# from shceduler_algorithms.scheduler_interface import SchedulerInterface 


class SchedulerInterface(ABC):

    @abstractmethod
    def select_next(self, ready_queue: list[Process]) -> Process | None:
        """Every scheduler implements this method to pick the next process."""
        pass

class FCFSScheduler(SchedulerInterface):
    def select_next(self, ready_queue: list[Process]) -> Process | None:
        if not ready_queue:
            return None
        return ready_queue[0]