"""Show a comparison chart with a separate color for every process."""

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
        Process(1, 0, 8),
        Process(2, 0, 3),
        Process(3, 0, 6),
        Process(4, 1, 4),
        Process(5, 1, 7),
      
    ])

    algorithms = [
        FCFS_Scheduler(),
        SJF_Scheduler(),
        SRTF_Scheduler(),
        RoundRobin_Scheduler(quantum=2),
    ]

    results = Comparison(workload, algorithms).compare()
    SimulationReportVisualizer(results).show()


if __name__ == "__main__":
    main()