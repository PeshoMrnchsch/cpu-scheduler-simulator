import pytest

from src.model.workload import Workload
from src.model.process import Process, ProcessState
from src.shceduler_algorithms.FCFS import FCFSScheduler
from src.simulator import Simulator

class TestFCFSSimulator:

    @staticmethod
    def turnaround_time_calc(p: Process):
        """Completion time - arrival time."""
        return p.completion - p.arrival_time

    @staticmethod
    def wait_time(p: Process):
        """Turnaround time - burst time."""
        return p.completion - p.arrival_time - p.burst_time
    
    def test_standard_fcfs_execution(self):
        p1 = Process(process_id=1, arrival_time=0, burst_time=5)
        p2 = Process(process_id=2, arrival_time=1, burst_time=3)
        p3 = Process(process_id=3, arrival_time=2, burst_time=1)
        
        workload = Workload([p1,p2,p3])
        
        sim = Simulator(workload=workload, scheduler=FCFSScheduler())
        sim.run()
        assert sim.cur_time==9
        assert len(sim.completed)==3
        
        # Validate individual process metrics
        # P1: Start=0, Completion=5, Turnaround=5, Waiting=0
        assert p1.start== 0
        assert p1.completion == 5
        assert TestFCFSSimulator.turnaround_time_calc(p1) == 5
        assert TestFCFSSimulator.wait_time(p1)==0
        
        assert p2.start== 5
        assert p2.completion == 8
        assert TestFCFSSimulator.turnaround_time_calc(p2) == 7
        assert TestFCFSSimulator.wait_time(p2)==4
        
        assert p3.start==8
        assert p3.completion == 9
        assert TestFCFSSimulator.turnaround_time_calc(p3) == 7
        assert TestFCFSSimulator.wait_time(p3)==6
    
    def test_process_arriving_after_time_zero(self):
     """Test that simulation handles an initially idle CPU."""

    p1 = Process(
        process_id=1,
        arrival_time=5,
        burst_time=3
    )

    workload = Workload([p1])

    sim = Simulator(
        workload=workload,
        scheduler=FCFSScheduler()
    )

    sim.run()
    
     # Simulation should jump to the arrival time
    assert p1.start == 5
    assert p1.completion == 8
    assert sim.cur_time == 8

    # Process should be completed
    assert len(sim.completed) == 1
    assert p1.state == ProcessState.TERMINATED
    
    def test_large_idle_gap_between_processes(self):
     """Test simulation with a large CPU idle gap."""

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

    sim = Simulator(
        workload=workload,
        scheduler=FCFSScheduler()
    )

    sim.run()

    # P1 executes immediately
    assert p1.start == 0
    assert p1.completion == 2

    # CPU is idle from time 2 until P2 arrives at time 10
    assert p2.start == 10
    assert p2.completion == 13

    # Final simulation time
    assert sim.cur_time == 13

    # Both processes should be completed
    assert len(sim.completed) == 2
    
    def test_processes_same_arr_time(self):
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
        workload = Workload([p1,p2])
        
        sim = Simulator(workload, FCFSScheduler())
        sim.run()
        
        assert p1.start == 0
        assert p1.completion == 2
        
        assert p2.start == 2
        assert p2.completion == 8
        
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
        workload = Workload([p1,p2])
        
        sim = Simulator(workload, FCFSScheduler())
        sim.run()
        
        assert p1.start == 0
        assert p1.completion == 2
        
        assert p2.start == 2
        assert p2.completion == 8
    def test_empty_workload(self):
        with pytest.raises(ValueError):
            workload = Workload([])
            
            sim = Simulator(workload, FCFSScheduler())
            sim.run()
        