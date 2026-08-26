import pytest

from src.model.workload import Workload
from src.model.process import Process, ProcessState
from src.scheduler_algorithms.FCFS import FCFS_Scheduler
from src.simulator import Simulator


class TestFCFSSimulator:

    def test_standard_fcfs_execution(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=5)
        p2 = Process(process_id=2, arrival_time=1, burst_time=3)
        p3 = Process(process_id=3, arrival_time=2, burst_time=1)

        workload = Workload([p1, p2, p3])
        simulator = Simulator(workload, FCFS_Scheduler())

        simulator.run()

        assert simulator.cur_time == 9
        assert len(simulator.completed) == 3

        assert simulator.timeline == [
            (0, 5, 1),
            (5, 8, 2),
            (8, 9, 3)
        ]

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [1, 2, 3]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2, 3}

        assert p1.start == 0
        assert p1.completion_time == 5

        assert p2.start == 5
        assert p2.completion_time == 8

        assert p3.start == 8
        assert p3.completion_time == 9

    def test_process_arriving_after_time_zero(self):
        p1 = Process(
            process_id=1,
            arrival_time=5,
            burst_time=3
        )

        workload = Workload([p1])
        simulator = Simulator(workload, FCFS_Scheduler())

        simulator.run()

        assert simulator.timeline == [
            (0, 5, None),
            (5, 8, 1)
        ]

        assert p1.start == 5
        assert p1.completion_time == 8
        assert simulator.cur_time == 8

        assert len(simulator.completed) == 1
        assert p1.state == ProcessState.TERMINATED

    def test_large_idle_gap_between_processes(self):
        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=2
        )

        p2 = Process(
            process_id=2,
            arrival_time=10,
            burst_time=3
        )

        workload = Workload([p1, p2])
        simulator = Simulator(workload, FCFS_Scheduler())

        simulator.run()

        assert simulator.timeline == [
            (0, 2, 1),
            (2, 10, None),
            (10, 13, 2)
        ]

        assert p1.start == 0
        assert p1.completion_time == 2

        assert p2.start == 10
        assert p2.completion_time == 13

        assert simulator.cur_time == 13

    def test_processes_same_arrival_time(self):
        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=2
        )

        p2 = Process(
            process_id=2,
            arrival_time=0,
            burst_time=6
        )

        workload = Workload([p1, p2])
        simulator = Simulator(workload, FCFS_Scheduler())

        simulator.run()

        assert simulator.timeline == [
            (0, 2, 1),
            (2, 8, 2)
        ]

        assert p1.start == 0
        assert p1.completion_time == 2

        assert p2.start == 2
        assert p2.completion_time == 8

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [1, 2]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2}

    def test_finishing_exactly_when_another_arrives(self):
        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=2
        )

        p2 = Process(
            process_id=2,
            arrival_time=2,
            burst_time=6
        )

        workload = Workload([p1, p2])
        simulator = Simulator(workload, FCFS_Scheduler())

        simulator.run()

        assert simulator.timeline == [
            (0, 2, 1),
            (2, 8, 2)
        ]

        assert p1.start == 0
        assert p1.completion_time == 2

        assert p2.start == 2
        assert p2.completion_time == 8

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [1, 2]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2}

    def test_single_process(self):
        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=5
        )

        workload = Workload([p1])
        simulator = Simulator(workload, FCFS_Scheduler())

        simulator.run()

        assert simulator.timeline == [(0, 5, 1)]

        assert [p.pid for p in simulator.completed] == [1]

        assert p1.start == 0
        assert p1.completion_time == 5

    def test_empty_workload(self):
        with pytest.raises(ValueError):
            Workload([])

    def test_fcfs_does_not_preempt(self):
        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=5
        )

        p2 = Process(
            process_id=2,
            arrival_time=1,
            burst_time=1
        )

        workload = Workload([p1, p2])
        simulator = Simulator(workload, FCFS_Scheduler())

        simulator.run()

        assert simulator.timeline == [
            (0, 5, 1),
            (5, 6, 2)
        ]

        assert p1.completion_time == 5
        assert p2.start == 5

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [1, 2]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2}