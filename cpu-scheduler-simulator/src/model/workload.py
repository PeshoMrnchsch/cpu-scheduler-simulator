from .process import Process,ProcessState
class Workload:
    def __init__(self, processes : list[Process]):
       self.processes = processes
       self._validate()
       
    def _validate(self):
        if not self.processes:
            raise ValueError("Collection must contain at least one process.")

        seen_ids = set()
        for p in self.processes:
            if p.pid in seen_ids:
                raise ValueError("Process with such id exists")
            seen_ids.add(p.pid)
            
            if p.arrival_time<0:
                raise ValueError(f"Process P{p.id} has invalid negative arrival time")
            if p.burst_time <= 0:
                raise ValueError(f"Process P{p.id} must have a burst time greater than 0")
            
    def reset_all(self):
        for p in self.processes:
            p.reset()
            
    def get_sorted_by_arrival(self):
       return sorted(self.processes, key=lambda p: (p.arrival_time, p.pid))
        
    def __len__(self):
        return len(self.processes)
    
    def __repr__(self):
        return f"Workload({len(self.processes)} processes)"
    

