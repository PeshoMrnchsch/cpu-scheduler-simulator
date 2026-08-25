from src.model.process import Process
from src.model.workload import Workload
from src.metrics.comparison import Comparison

from src.scheduler_algorithms.FCFS import FCFS_Scheduler
from src.scheduler_algorithms.SJF import SJF_Scheduler
from src.scheduler_algorithms.SRTF import SRTF_Scheduler
from src.scheduler_algorithms.RoundRobin import RoundRobin_Scheduler


class TestComparison:

    def test_compare_returns_all_algorithms(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=4)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2])

        algorithms = [
            FCFS_Scheduler(),
            SJF_Scheduler(),
            SRTF_Scheduler(),
            RoundRobin_Scheduler(quantum=2)
        ]

        comparison = Comparison(workload, algorithms)

        results = comparison.compare()

        assert set(results.keys()) == {
            "FCFS",
            "SJF",
            "SRTF",
            "Round Robin"
        }


    def test_compare_contains_metrics_and_result(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=4)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2])

        algorithms = [
            FCFS_Scheduler(),
            SJF_Scheduler(),
            SRTF_Scheduler(),
            RoundRobin_Scheduler(quantum=2)
        ]

        comparison = Comparison(workload, algorithms)

        results = comparison.compare()

        for algorithm_result in results.values():
            assert "metrics" in algorithm_result
            assert "result" in algorithm_result


    def test_compare_preserves_timeline(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=4)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2])

        algorithms = [
            FCFS_Scheduler(),
            SJF_Scheduler(),
            SRTF_Scheduler(),
            RoundRobin_Scheduler(quantum=2)
        ]

        comparison = Comparison(workload, algorithms)

        results = comparison.compare()

        for algorithm_result in results.values():
            result = algorithm_result["result"]

            assert result.timeline
            assert len(result.timeline) > 0


    def test_compare_does_not_modify_original_workload(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=4)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2])

        original_processes = [
            (p.pid, p.arrival_time, p.burst_time)
            for p in workload.processes
        ]

        algorithms = [
            FCFS_Scheduler(),
            SJF_Scheduler(),
            SRTF_Scheduler(),
            RoundRobin_Scheduler(quantum=2)
        ]

        comparison = Comparison(workload, algorithms)

        comparison.compare()

        assert [
            (p.pid, p.arrival_time, p.burst_time)
            for p in workload.processes
        ] == original_processes