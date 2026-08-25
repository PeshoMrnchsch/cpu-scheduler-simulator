from src.model.process import Process
from src.metrics.result import SimulationResult


class Metrics:

    def __init__(self, result: SimulationResult):
        self.result = result

    def turnaround_time(self, process: Process) -> int:
        return process.completion_time - process.arrival_time

    def waiting_time(self, process: Process) -> int:
        return self.turnaround_time(process) - process.burst_time

    def average_turnaround_time(self) -> float:
        if not self.result.processes_completed:
            return 0.0

        turnaround_times = [
            self.turnaround_time(p)
            for p in self.result.processes_completed
        ]

        return sum(turnaround_times) / len(turnaround_times)

    def average_waiting_time(self) -> float:
        if not self.result.processes_completed:
            return 0.0

        waiting_times = [
            self.waiting_time(p)
            for p in self.result.processes_completed
        ]

        return sum(waiting_times) / len(waiting_times)

    def cpu_utilization(self) -> float:
        total_time = (
            self.result.simulation_end
            - self.result.simulation_start
        )

        if total_time == 0:
            return 0.0

        busy_time = sum(
            end - start
            for start, end, process in self.result.timeline
            if process is not None
        )

        return (busy_time / total_time) * 100

    def calculate(self) -> dict:
        return {
            "average_turnaround_time": self.average_turnaround_time(),
            "average_waiting_time": self.average_waiting_time(),
            "cpu_utilization": self.cpu_utilization()
        }