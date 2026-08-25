from src.scheduler_algorithms.SchedulerInterface import SchedulerInterface
from src.model.process import Process

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
    
    def should_preempt(self, current_process=None, ready_queue=None):
        return False

    def reset(self):
        pass
    def get_name(self):
        return "SJF"
