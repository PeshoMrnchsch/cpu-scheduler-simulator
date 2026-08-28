from src.metrics.comparison import Comparison
from src.model.process import Process
from src.model.workload import Workload
from src.scheduler_algorithms.FCFS import FCFS_Scheduler
from src.scheduler_algorithms.RoundRobin import RoundRobin_Scheduler
from src.scheduler_algorithms.SJF import SJF_Scheduler
from src.scheduler_algorithms.SRTF import SRTF_Scheduler
from src.visualization.gantt_chart import GanttChart
from src.visualization.metrics_table import MetricsTable


def main():
    workload = Workload([
        Process(process_id=1, arrival_time=0, burst_time=2),
        Process(process_id=2, arrival_time=6, burst_time=3),
        Process(process_id=3, arrival_time=7, burst_time=1),
    ])

    algorithms = [
        FCFS_Scheduler(),
        SJF_Scheduler(),
        SRTF_Scheduler(),
        RoundRobin_Scheduler(quantum=2),
    ]

    comparison_results = Comparison(workload, algorithms).compare()

    MetricsTable(comparison_results).render()

    for algorithm, data in comparison_results.items():
        print(f"\n{algorithm}")
        print("CPU:")
        GanttChart(data["result"].cpu_timeline, "cpu").render()
        print("I/O:")
        GanttChart(data["result"].io_timeline, "io").render()


if __name__ == "__main__":
    main()