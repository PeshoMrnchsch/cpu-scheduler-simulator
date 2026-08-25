from src.model.process import Process
from src.scheduler_algorithms.SchedulerInterface import SchedulerInterface

class SRTF_Scheduler(SchedulerInterface):
    def select_next(self, ready_queue):
        if not ready_queue:
                    return None
                
        return min(
            ready_queue,
            key=lambda p: (p.remaining_time, p.pid)
        )
    def on_time_unit(self):
        pass
    
    def should_preempt(self, current_process, ready_queue):
        return any(
            process.remaining_time < current_process.remaining_time
            for process in ready_queue
        )
          
    def reset(self):
        pass
    
    def get_name(self):
         return "SRTF"