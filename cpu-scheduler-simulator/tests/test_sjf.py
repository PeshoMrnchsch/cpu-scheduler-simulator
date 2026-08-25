import pytest

from src.model.process import Process
from src.model.workload import Workload
from src.scheduler_algorithms.SJF import SJF_Scheduler
from src.simulator import Simulator


def make_process(pid, arrival_time, burst_time):
    return Process(pid, arrival_time, burst_time)


class TestSJFScheduler:

    def test_select_shortest_process(self):
        scheduler = SJF_Scheduler()

        p1 = make_process(1, 0, 8)
        p2 = make_process(2, 0, 3)
        p3 = make_process(3, 0, 5)

        selected = scheduler.select_next([p1, p2, p3])

        assert selected == p2

    def test_select_single_process(self):
        scheduler = SJF_Scheduler()

        p1 = make_process(1, 0, 5)

        selected = scheduler.select_next([p1])

        assert selected == p1

    def test_select_empty_queue(self):
        scheduler = SJF_Scheduler()

        selected = scheduler.select_next([])

        assert selected is None

    def test_select_shortest_with_different_arrival_times(self):
        scheduler = SJF_Scheduler()

        p1 = make_process(1, 0, 8)
        p2 = make_process(2, 1, 3)
        p3 = make_process(3, 2, 5)

        selected = scheduler.select_next([p1, p2, p3])

        assert selected == p2

    def test_tie_breaks_by_pid(self):
        scheduler = SJF_Scheduler()

        p1 = make_process(1, 0, 5)
        p2 = make_process(2, 0, 5)
        p3 = make_process(3, 0, 2)

        selected = scheduler.select_next([p1, p2, p3])

        assert selected == p3

    def test_tie_between_same_burst_uses_pid(self):
        scheduler = SJF_Scheduler()

        p1 = make_process(1, 0, 5)
        p2 = make_process(2, 0, 5)

        selected = scheduler.select_next([p2, p1])

        assert selected == p1

    def test_should_not_preempt(self):
        scheduler = SJF_Scheduler()

        assert scheduler.should_preempt() is False

    def test_reset(self):
        scheduler = SJF_Scheduler()

        scheduler.reset()

        assert scheduler.should_preempt() is False

    def test_completion_order(self):
        scheduler = SJF_Scheduler()

        processes = [
            make_process(1, 0, 8),
            make_process(2, 0, 3),
            make_process(3, 0, 5),
            make_process(4, 0, 1),
        ]

        workload = Workload(processes)
        simulator = Simulator(workload, scheduler)

        result = simulator.run()

        completion_order = [
            p.pid for p in result.processes_completed
        ]

        expected_order = [4, 2, 3, 1]

        assert completion_order == expected_order
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2, 3, 4}

    def test_sjf_does_not_preempt_running_process(self):
        scheduler = SJF_Scheduler()

        p1 = make_process(1, 0, 8)
        p2 = make_process(2, 1, 2)

        workload = Workload([p1, p2])
        simulator = Simulator(workload, scheduler)

        result = simulator.run()

        completion_order = [
            p.pid for p in result.processes_completed
        ]

        # P1 starts first and SJF is non-preemptive.
        assert completion_order == [1, 2]

    def test_zero_burst_process(self):
        scheduler = SJF_Scheduler()

        p1 = make_process(1, 0, 0)
        p2 = make_process(2, 0, 5)

        selected = scheduler.select_next([p1, p2])

        assert selected == p1