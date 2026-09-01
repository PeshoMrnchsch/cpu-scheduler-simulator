"""Open a comparison visualization for the same workload and all schedulers."""

from src.metrics.comparison import Comparison
from src.model.process import Process
from src.model.workload import Workload
from src.scheduler_algorithms.FCFS import FCFS_Scheduler
from src.scheduler_algorithms.RoundRobin import RoundRobin_Scheduler
from src.scheduler_algorithms.SJF import SJF_Scheduler
from src.scheduler_algorithms.SRTF import SRTF_Scheduler
from src.visualization.comparison_visualiser import SimulationReportVisualizer


def main():
    workload = Workload([
        Process(process_id=1, arrival_time=0, burst_time=8),
        Process(process_id=2, arrival_time=0, burst_time=3),
        Process(process_id=3, arrival_time=1, burst_time=5),
        Process(process_id=4, arrival_time=2, burst_time=2),
    ])

    algorithms = [
        FCFS_Scheduler(),
        SJF_Scheduler(),
        SRTF_Scheduler(),
        RoundRobin_Scheduler(quantum=2),
    ]

    comparison_results = Comparison(workload, algorithms).compare()

    print("Opening comparison chart for the same workload...")
    SimulationReportVisualizer(comparison_results).show()


if __name__ == "__main__":
    main()
