from src.model.process import Process, ProcessState
from src.model.workload import Workload
from src.scheduler_algorithms.SchedulerInterface import SchedulerInterface
from src.metrics.result import SimulationResult
from src.devices.io_device import IODevice

class Simulator:
    """Coordinate one simulation clock and all per-tick state transitions.

    A simulation tick represents the interval from time ``t`` to ``t + 1``.
    During that interval the CPU and each active I/O device execute one unit.
    At the tick boundary, I/O completions are handled before the next CPU
    scheduling decision. Only this class advances ``cur_time``.
    """

    def __init__(self, workload: Workload, scheduler:SchedulerInterface, io_device:IODevice | None = None):
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
        
        self.cpu_timeline = []
        self.io_timeline = []
        
        # IO Device
        self.io_device = io_device
        
        if workload.has_io() and io_device is None:
            raise ValueError(
                "An I/O device is required when the workload contains I/O requests."
            )

    def add_cpu_timeline_entry(self, process:Process):
        """Helper to add a process to the timeline"""
        if self.cpu_timeline and self.cpu_timeline[-1][2] == process.pid:
            self.cpu_timeline[-1] = (self.cpu_timeline[-1][0], self.cur_time + 1, self.cur_process.pid)
        else:
            self.cpu_timeline.append((self.cur_time, self.cur_time + 1, self.cur_process.pid))
            
    def add_io_timeline_entry(self, request):
        entry = (
            self.cur_time,
            self.cur_time + 1,
            request.process.pid,
            request.device.device_id,
        )

        if self.io_timeline and self.io_timeline[-1][2:] == entry[2:]:
            self.io_timeline[-1] = (
                self.io_timeline[-1][0],
                entry[1],
                *entry[2:],
            )
        else:
            self.io_timeline.append(entry)

    def add_idle_timeline_entry(self, end_time: int):
        """Record the interval while the CPU waits for the next arrival."""
        if self.cpu_timeline and self.cpu_timeline[-1][2] is None:
            self.cpu_timeline[-1] = (self.cpu_timeline[-1][0], end_time, None)
        else:
            idle_start = self.cpu_timeline[-1][1] if self.cpu_timeline else self.cur_time
            if idle_start < end_time:
                self.cpu_timeline.append((idle_start, end_time, None))

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

        # Add to exec timeline
        self.add_cpu_timeline_entry(self.cur_process)
        
        # Execute process
        self.cur_process.remaining_time -= 1
        
        # Checks if process reach I/O point
        if self.cur_process.should_request_io():
            request = self.cur_process.start_io()
            self.cur_process.state = ProcessState.IO_WAIT
            request.device.enqueue(request)
            self.cur_process = None
            self.scheduler.reset()
            return
        
        self.scheduler.on_time_unit()

        # Handle process completion
        if self.cur_process.remaining_time == 0:
            self.cur_process.state = ProcessState.TERMINATED
            self.cur_process.completion_time = self.cur_time + 1

            self.completed.append(self.cur_process)
            self.cur_process = None

            self.scheduler.reset()

        # Handle Preemption
        elif self.scheduler.should_preempt(self.cur_process,self.ready_queue):
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

    def process_arrivals(self):
        """Process all processes that have arrived at the current time."""
        self.check_arrivals()

    def process_io(self):
        """Advance the I/O device by one time unit."""
        if self.io_device is None:
            return None

        active_request = self.io_device.get_active_request()
        
        if active_request is None and self.io_device.has_pending():
            self.io_device.start_next()
            active_request = self.io_device.get_active_request()
        
        if active_request is not None:
            self.add_io_timeline_entry(active_request)
            
    def handle_io_completions(self, completed_request):
        """Move a process whose I/O completed back to the ready queue."""
        if completed_request is None:
            return

        process = completed_request.process
        process.finish_io()
        process.state = ProcessState.READY
        self.ready_queue.append(process)

    def schedule_cpu(self):
        """Select the next process for CPU execution."""
        self.select_next()

    def execute_cpu(self):
        """Execute the selected process for one time unit."""
        self.step_time_unit()

    def advance_time(self):
        """Record an idle CPU unit when needed, then advance one tick."""
        has_active_io = (
            self.io_device is not None
            and (
                self.io_device.is_busy()
                or self.io_device.has_pending()
            )
        )

        if self.cur_process is None and not self.ready_queue and (
            self.unarrived or has_active_io
        ):
            self.add_idle_timeline_entry(self.cur_time + 1)

        self.cur_time += 1

    def run(self):
        """`Run the simulation until all processes are completed."""

        while (
            self.unarrived
            or self.ready_queue
            or self.cur_process
            or (
                self.io_device is not None
                and (
                    self.io_device.is_busy()
                    or self.io_device.has_pending()
                )
            )
        ):

            self.process_arrivals()
            completed_request = self.process_io()
            self.handle_io_completions(completed_request)
            self.schedule_cpu()
            self.execute_cpu()
            self.advance_time()

        return SimulationResult(
            processes_completed=self.completed,
            cpu_timeline=self.cpu_timeline,
            io_timeline=self.io_timeline,
            simulation_start=0,
            simulation_end=self.cur_time
        )