from src.scheduler_algorithms.SchedulerInterface import SchedulerInterface
from src.model.process import Process
# from scheduler_algorithms.scheduler_interface import SchedulerInterface 




class FCFS_Scheduler(SchedulerInterface):
    def select_next(self, ready_queue: list[Process]) -> Process | None:
        if not ready_queue:
            return None
        
        return ready_queue[0]
    
    def on_time_unit(self):
        pass

    def should_preempt(self) -> bool:
        return False

    def reset(self):
        pass
    
    
    
class SJF_Scheduler(SchedulerInterface):
    def select_next(self, ready_queue:list[Process]):
        if not ready_queue:
            return None
        
        return min(
            ready_queue,
            key=lambda p: (p.burst_time, p.pid)
        )
    
    def on_time_unit(self):
            pass
    
    def should_preempt(self) -> bool:
        return False

    def reset(self):
        pass

