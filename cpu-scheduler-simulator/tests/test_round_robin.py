import pytest

from src.model.workload import Workload
from src.model.process import Process, ProcessState
from src.scheduler_algorithms.RoundRobin import RoundRobin_Scheduler
from src.simulator import Simulator


class TestRoundRobinScheduler:
    
    @staticmethod
    def turnaround_time_calc(p: Process):
        """Completion time - arrival time."""
        return p.completion - p.arrival_time

    @staticmethod
    def wait_time(p: Process):
        """Turnaround time - burst time."""
        return p.completion - p.arrival_time - p.burst_time

    def test_quantum_one(self):
        scheduler = RoundRobin_Scheduler(quantum=1)

        scheduler.on_time_unit()
        assert scheduler.should_preempt() is True
    
    def test_before_quantum_expires(self):
        scheduler = RoundRobin_Scheduler(quantum=3)

        scheduler.on_time_unit()
        scheduler.on_time_unit()

        assert scheduler.should_preempt() is False
        
    def test_at_quantum_expiration(self):
        scheduler = RoundRobin_Scheduler(quantum=3)

        scheduler.on_time_unit()
        scheduler.on_time_unit()
        scheduler.on_time_unit()

        assert scheduler.should_preempt() is True
            
    def test_reset(self):
        scheduler = RoundRobin_Scheduler(quantum=2)

        scheduler.on_time_unit()
        scheduler.on_time_unit()

        assert scheduler.should_preempt() is True

        scheduler.reset()

        assert scheduler.time_used_in_slice == 0
        assert scheduler.should_preempt() is False
        
    def test_zero_quantum(self):
        with pytest.raises(ValueError):
            RoundRobin_Scheduler(quantum=0)
            
    def test_negative_quantum(self):
            with pytest.raises(ValueError):
                RoundRobin_Scheduler(quantum=-1)
        
    
class TestRoundRobinSimulator:
    def test_process_shorter_than_quantum(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=1)

        workload = Workload([p1])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()
        
        assert p1.state == ProcessState.TERMINATED
        assert p1.remaining_time == 0
        assert p1.completion_time == 1
        assert len(simulator.completed) == 1
        
    def test_process_equal_to_quantum(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=2)

        workload = Workload([p1])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert p1.state == ProcessState.TERMINATED
        assert p1.remaining_time == 0
        assert p1.completion_time == 2
        
        assert simulator.ready_queue==[]
        assert len(simulator.completed) == 1
        
    def test_process_longer_than_quantum(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=5)

        workload = Workload([p1])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert p1.state == ProcessState.TERMINATED
        assert p1.remaining_time == 0
        assert p1.completion_time == 5
        assert len(simulator.completed) == 1
        
    def test_multiple_processes_round_robin(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=4)
        p2 = Process(process_id=2, arrival_time=0, burst_time=4)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert p1.state == ProcessState.TERMINATED
        assert p2.state == ProcessState.TERMINATED

        assert p1.remaining_time == 0
        assert p2.remaining_time == 0

        assert len(simulator.completed) == 2
        assert simulator.cur_time == 8
        
    def test_same_arrival_time(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=2)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)
        p3 = Process(process_id=3, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2, p3])
        scheduler = RoundRobin_Scheduler(quantum=1)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert all(
            process.state == ProcessState.TERMINATED
            for process in [p1, p2, p3]
        )

        assert len(simulator.completed) == 3
        assert simulator.cur_time == 6
        
    def test_arrival_during_quantum(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=5)
        p2 = Process(process_id=2, arrival_time=1, burst_time=2)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=3)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert p1.state == ProcessState.TERMINATED
        assert p2.state == ProcessState.TERMINATED

        # P1 should finish at time 7
        assert p1.completion_time == 7

        # P2 should get CPU after P1's first quantum
        assert p2.start == 3
        
    def test_cpu_idle_before_first_process(self):
        p1 = Process(process_id=1, arrival_time=5, burst_time=2)

        workload = Workload([p1])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert p1.start == 5
        assert p1.completion_time == 7
        assert simulator.cur_time == 7
        
    def test_cpu_idle_between_processes(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=1)
        p2 = Process(process_id=2, arrival_time=10, burst_time=1)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert p1.completion_time == 1
        assert p2.start == 10
        assert p2.completion_time == 11

        assert simulator.cur_time == 11
        assert len(simulator.completed) == 2
        
class TestEdgeCaseTesting:
    def test_completion_order_shortest_process_finishes_first(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=5)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)
        p3 = Process(process_id=3, arrival_time=0, burst_time=1)

        workload = Workload([p1, p2, p3])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [2, 3, 1]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2, 3}


    def test_completion_order_same_arrival_same_burst(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=2)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)
        p3 = Process(process_id=3, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2, p3])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [1, 2, 3]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2, 3}


    def test_completion_order_quantum_one(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=3)
        p2 = Process(process_id=2, arrival_time=0, burst_time=1)
        p3 = Process(process_id=3, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2, p3])
        scheduler = RoundRobin_Scheduler(quantum=1)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [2, 3, 1]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2, 3}


    def test_completion_order_late_arrival_finishes_first(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=6)
        p2 = Process(process_id=2, arrival_time=1, burst_time=1)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [2, 1]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2}


    def test_completion_order_exact_quantum(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=4)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)
        p3 = Process(process_id=3, arrival_time=0, burst_time=1)

        workload = Workload([p1, p2, p3])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [2, 3, 1]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2, 3}


    def test_completion_order_single_process(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=10)

        workload = Workload([p1])
        scheduler = RoundRobin_Scheduler(quantum=1)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [1]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1}


    def test_completion_order_with_idle_cpu(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=1)
        p2 = Process(process_id=2, arrival_time=5, burst_time=1)
        p3 = Process(process_id=3, arrival_time=5, burst_time=2)

        workload = Workload([p1, p2, p3])
        scheduler = RoundRobin_Scheduler(quantum=1)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        completion_order = [p.pid for p in simulator.completed]

        assert completion_order == [1, 2, 3]
        assert len(completion_order) == len(set(completion_order))
        assert set(completion_order) == {1, 2, 3}
        
class TestCompleteOrder:
    def test_execution_order_basic_round_robin(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=4)
        p2 = Process(process_id=2, arrival_time=0, burst_time=4)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert simulator.execution_timeline == [
            1, 1,
            2, 2,
            1, 1,
            2, 2
        ]


    def test_execution_order_quantum_one(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=3)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=1)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert simulator.execution_timeline == [
            1, 2, 1, 2, 1
        ]


    def test_execution_order_process_finishes_before_quantum(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=1)
        p2 = Process(process_id=2, arrival_time=0, burst_time=5)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=3)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert simulator.execution_timeline == [
            1,
            2, 2, 2,
            2, 2
        ]


    def test_execution_order_arrival_during_quantum(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=5)
        p2 = Process(process_id=2, arrival_time=1, burst_time=2)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=3)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert simulator.execution_timeline == [
            1, 1, 1,
            2, 2,
            1, 1
        ]


    def test_execution_order_same_arrival_time(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=2)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)
        p3 = Process(process_id=3, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2, p3])
        scheduler = RoundRobin_Scheduler(quantum=1)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert simulator.execution_timeline == [
            1, 2, 3,
            1, 2, 3
        ]


    def test_execution_order_long_process_multiple_preemptions(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=7)
        p2 = Process(process_id=2, arrival_time=0, burst_time=2)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert simulator.execution_timeline == [
            1, 1,
            2, 2,
            1, 1,
            1, 1, 1
        ]


    def test_execution_order_late_arrival(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=3)
        p2 = Process(process_id=5, arrival_time=5, burst_time=2)

        workload = Workload([p1, p2])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        assert simulator.execution_timeline == [
            1, 1, 1,
            5, 5
        ]


    def test_execution_timeline_contains_every_cpu_time_unit(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=5)
        p2 = Process(process_id=2, arrival_time=0, burst_time=3)
        p3 = Process(process_id=3, arrival_time=1, burst_time=2)

        workload = Workload([p1, p2, p3])
        scheduler = RoundRobin_Scheduler(quantum=2)
        simulator = Simulator(workload, scheduler)

        simulator.run()

        total_burst_time = 5 + 3 + 2

        assert len(simulator.execution_timeline) == total_burst_time
