from src.model.workload import Workload
from src.model.process import Process, ProcessState
from src.scheduler_algorithms.SchedulerInterface import SchedulerInterface

class Simulator:

    def __init__(self, workload: Workload, scheduler:SchedulerInterface):
        """Initialize simulation state and process collections."""

        self.cur_time = 0
        self.cur_process = None

        # Processes waiting to arrive, sorted by arrival time
        self.unarrived = workload.get_sorted_by_arrival()

        # Processes ready for CPU execution
        self.ready_queue = []

        # Finished processes
        self.completed = []

        self.scheduler = scheduler
        
        # TODO - Remove Testing - add to exec timeline
        self.execution_timeline = []

    def check_arrivals(self):
        """Move arrived processes from unarrived to ready queue."""

        for process in list(self.unarrived):
            if (
                process.arrival_time <= self.cur_time
                and process.state == ProcessState.NEW
            ):
                process.state = ProcessState.READY
                self.ready_queue.append(process)
                self.unarrived.remove(process)

    def dispatch(self, process: Process):
        """Move a selected process from READY to RUNNING."""

        if process.state == ProcessState.READY:
            process.state = ProcessState.RUNNING

            # Record first CPU execution
            if process.start is None:
                process.start = self.cur_time

            self.cur_process = process

    def step_time_unit(self):
        """Execute the current process for one time unit."""

        if self.cur_process is None:
            return

        # TODO - Remove Testing - add to exec timeline
        self.execution_timeline.append(self.cur_process.pid)
        
        # Execute process
        self.cur_process.remaining_time -= 1
        self.cur_time += 1

        self.scheduler.on_time_unit()

        # Handle process completion
        if self.cur_process.remaining_time == 0:
            self.cur_process.state = ProcessState.TERMINATED
            self.cur_process.completion_time = self.cur_time

            self.completed.append(self.cur_process)
            self.cur_process = None

            self.scheduler.reset()

        # Handle Preemption
        elif self.scheduler.should_preempt():
                self.cur_process.state = ProcessState.READY
                self.ready_queue.append(self.cur_process)
                self.cur_process = None
                self.scheduler.reset()

    def select_next(self):
        """Ask the scheduler to select and dispatch the next process."""

        if self.cur_process is not None or not self.ready_queue:
            return

        selected = self.scheduler.select_next(self.ready_queue)

        if selected is not None:
            self.ready_queue.remove(selected)
            self.dispatch(selected)

    def run(self):
        """Run the simulation until all processes are completed."""

        while self.unarrived or self.ready_queue or self.cur_process:

            # Move newly arrived processes into the ready queue
            self.check_arrivals()

            # Select a process if CPU is free
            if self.cur_process == None:
                self.select_next()

            # Execute one time unit
            if self.cur_process:
                self.step_time_unit()

            # CPU is idle: jump to the next arrival
            elif self.unarrived:
                self.cur_time = self.unarrived[0].arrival_time