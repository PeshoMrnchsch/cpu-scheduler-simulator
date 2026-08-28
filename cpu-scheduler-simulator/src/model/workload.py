from .process import Process,ProcessState
from src.model.io_request import IORequest

class Workload:
    def __init__(self, processes : list[Process]):
       self.processes = processes
       self._validate()
       
    def _validate(self):
        if not self.processes:
            raise ValueError("Collection must contain at least one process.")

        seen_ids = set()
        for p in self.processes:
            
            # Process ID
            if p.pid in seen_ids:
                raise ValueError("Process with such id exists")
            seen_ids.add(p.pid)
            
            # Basic process validation
            if p.arrival_time<0:
                raise ValueError(f"Process P{p.pid} has invalid negative arrival time")
            if p.burst_time <= 0:
                raise ValueError(f"Process P{p.pid} must have a burst time greater than 0")
            
            # I/O validation
            self._validate_io_requests(p)
    
    # I/O validations       
    def _validate_io_requests(self, process:Process):
        previous_execution_point = -1
        
        for request in process.io_requests:
            if request.duration <= 0:
                raise ValueError(
                    f"Process P{process.pid} has an I/O request "
                    f"with invalid duration."
                )
            
            if request.execution_point < 0:
                raise ValueError(
                    f"Process P{process.pid} has an I/O request "
                    f"with invalid execution point."
                )
                        
            if request.execution_point >= process.burst_time:
                raise ValueError(
                    f"Process P{process.pid} has an I/O request "
                    f"at execution point {request.execution_point}, "
                    f"but burst time is {process.burst_time}."
                )
            
            # Execution points must be ordered
            if request.execution_point <= previous_execution_point:
                  raise ValueError(
                    f"Process P{process.pid} has I/O requests "
                    f"that are not in increasing execution order."
                )
                  
            # Check if device exist
            if request.device is None:
                raise ValueError(
                    f"Process P{process.pid} has an I/O request "
                    f"without a device."
                )
                
            previous_execution_point = request.execution_point
            
            
    def has_io(self) -> bool:
        """
            Checks if the process has any io requests
        """
        
        return any(p.io_requests for p in self.processes)
      
    def reset_all(self):
        for p in self.processes:
            p.reset()
            
    def get_sorted_by_arrival(self):
       return sorted(self.processes, key=lambda p: (p.arrival_time, p.pid))
        
    def __len__(self):
        return len(self.processes)
    
    def __repr__(self):
        return f"Workload({len(self.processes)} processes)"

