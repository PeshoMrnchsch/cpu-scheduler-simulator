from model.process import Process
from model.process import ProcessState
from model.workload import Workload

class Simulator:
    def __init__(self, workload:Workload, scheduler):
        self.cur_time = 0
        self.cur_process=None
        # Get processes sorted chronologically
        self.unarrived = workload.get_sorted_by_arrival()
        self.ready_queue = []
        self.completed =[]
        self.status = None
        
        self.scheduler = scheduler
        
    def check_arrivals(self):
        """Scans arrived processes and moves arrived ones to READY state."""
        # Loop over a copy of arrived in workload
        for p in list(self.unarrived):
            if p.arrival_time <= self.cur_time and p.state == ProcessState.NEW:
                p.state = ProcessState.READY
                self.ready_queue.append(p)
                self.unarrived.remove(p)
            
    def dispatch(self, p:Process):
        if p.state == ProcessState.READY:
            p.state = ProcessState.RUNNING
            if p.start is None:
                # first time execution
                p.start = self.cur_time
            
            self.cur_process = p
    
    def step_time_unit(self):
        if(self.cur_process is not None):
            self.cur_process.remaining_time -= 1
            self.cur_time +=1
            
            if(self.cur_process.remaining_time == 0):
                self.cur_process.state = ProcessState.TERMINATED
                self.cur_process.completion = self.cur_time
                self.completed.append(self.cur_process)
                self.cur_process = None
            
        if self.cur_process is None and not self.ready_queue:
            # if no current process and empty ready queue => select next unarrived
            self.cur_time = self.unarrived[0].arrival_time
            # populate the ready queue
            self.check_arrivals()
        
        
    def select_next(self):
        if self.cur_process is None and self.ready_queue:
                self.cur_process= self.scheduler.select_next(self.ready_queue)
                self.ready_queue.remove(self.cur_process)
                self.dispatch(self.cur_process)
                
    def run(self):
        while self.unarrived is not None:
            self.check_arrivals()
            self.select_next()
            if self.cur_process:
                self.step_time_unit()
