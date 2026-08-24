import src
from src.model.workload import Workload
from src.model.process import Process, ProcessState
from src.shceduler_algorithms.FCFS import FCFSScheduler


class Simulator:

    def __init__(self, workload: Workload, scheduler: FCFSScheduler):
        """Initialize simulation state and process collections."""

        self.cur_time = 0
        self.cur_process = None

        # Processes waiting to arrive, sorted by arrival time
        self.unarrived = workload.get_sorted_by_arrival()

        # Processes ready for CPU execution
        self.ready_queue = []

        # Finished processes
        self.completed = []

        self.status = None
        self.scheduler = scheduler


    def check_arrivals(self):
        """Move arrived processes from unarrived to ready queue."""

        for p in list(self.unarrived):
            if p.arrival_time <= self.cur_time and p.state == ProcessState.NEW:
                p.state = ProcessState.READY
                self.ready_queue.append(p)
                self.unarrived.remove(p)


    def dispatch(self, p: Process):
        """Move a selected process from READY to RUNNING."""

        if p.state == ProcessState.READY:
            p.state = ProcessState.RUNNING

            # Record first CPU execution
            if p.start is None:
                p.start = self.cur_time

            self.cur_process = p


    def step_time_unit(self):
        """Execute the current process for one time unit."""

        if self.cur_process is not None:
            self.cur_process.remaining_time -= 1
            self.cur_time += 1

            # Handle process completion
            if self.cur_process.remaining_time == 0:
                self.cur_process.state = ProcessState.TERMINATED
                self.cur_process.completion = self.cur_time
                self.completed.append(self.cur_process)
                self.cur_process = None

        


    def select_next(self):
        """Ask the scheduler to select and dispatch the next process."""

        if self.cur_process is None and self.ready_queue:
            self.cur_process = self.scheduler.select_next(self.ready_queue)
            self.ready_queue.remove(self.cur_process)
            self.dispatch(p=self.cur_process)


    def run(self):
        """Run the simulation until all processes are completed."""

        while self.unarrived or self.ready_queue or self.cur_process:

            # Move new arrivals into the ready queue
            self.check_arrivals()

            # Select a process if CPU is free
            self.select_next()

            # Execute one simulation step
            if self.cur_process:
                self.step_time_unit()
            # Handle CPU idle time
            elif self.cur_process is None and not self.ready_queue and self.unarrived:
                self.cur_time = self.unarrived[0].arrival_time
                self.check_arrivals()

