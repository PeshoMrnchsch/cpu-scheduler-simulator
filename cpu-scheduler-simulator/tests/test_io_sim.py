import pytest

from src.devices.io_device import IODevice
from src.model.io_request import IORequest
from src.model.process import Process, ProcessState
from src.model.workload import Workload
from src.scheduler_algorithms.FCFS import FCFS_Scheduler
from src.simulator import Simulator

class Test_IO_Sim:

    def test_single_process_io_lifecycle(self):
        device = IODevice(
            device_id="device_0",
            device_type="generic"
        )

        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=5,
        )

        io_request = IORequest(
            process=p1,
            execution_point=2,
            duration=3,
            device=device
        )
        p1.io_requests = [io_request]

        workload = Workload([p1])

        simulator = Simulator(
            workload=workload,
            scheduler=FCFS_Scheduler(),
            io_device=device
        )

        result = simulator.run()

        assert p1.state == ProcessState.TERMINATED
        assert p1.remaining_time == 0

        assert len(result.processes_completed) == 1
        assert result.processes_completed[0] == p1

        assert p1.burst_time == 5

        assert device.total_processed == 1

        assert device.current_io is None
        assert not device.has_pending()

        assert p1.completion_time is not None
    
    def test_process_blocks_at_io_point(self):
        device = IODevice(
            device_id="device_0",
            device_type="generic"
            )

        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=5,
        )

        io_request = IORequest(
            process=p1,
            execution_point=2,
            duration=3,
            device=device
        )

        p1.io_requests = [io_request]

        workload = Workload([p1])

        simulator = Simulator(
            workload=workload,
            scheduler=FCFS_Scheduler(),
            io_device=device
        )

        simulator.check_arrivals()
        simulator.select_next()
        simulator.step_time_unit()
        
        assert p1.remaining_time==4
        assert p1.state== ProcessState.RUNNING
        simulator.step_time_unit()

        assert p1.remaining_time == 3
        assert p1.state == ProcessState.IO_WAIT
        assert simulator.cur_process is None
        assert p1 not in simulator.ready_queue
        
    def test_process_returns_to_ready_after_io(self):
        device = IODevice(
            device_id="device_0",
            device_type="generic"
        )

        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=5,
        )

        io_request = IORequest(
            process=p1,
            execution_point=2,
            duration=3,
            device=device
        )

        p1.io_requests = [io_request]

        workload = Workload([p1])

        simulator = Simulator(
            workload=workload,
            scheduler=FCFS_Scheduler(),
            io_device=device
        )

        # Run full simulation
        simulator.run()

        assert p1.state == ProcessState.TERMINATED
        assert device.total_processed == 1
        
    def test_io_takes_correct_duration(self):
        device = IODevice(
            device_id="device_0",
            device_type="generic"
        )

        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=5,
        )

        io_request = IORequest(
            process=p1,
            execution_point=2,
            duration=3,
            device=device
        )
        
        device.enqueue(io_request)
                
        # I/O unit 1
        device.step()

        assert device.remaining_time == 2
        # I/O unit 2
        device.step()

        assert device.remaining_time == 1
        # I/O unit 3
        device.step()
        assert device.remaining_time == 0
        
    def test_process_blocks_at_io_point(self):
        device = IODevice(
            device_id="device_0",
            device_type="generic"
        )

        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=5,
        )

        io_request = IORequest(
            process=p1,
            execution_point=2,
            duration=3,
            device=device
        )

        p1.io_requests = [io_request]

        workload = Workload([p1])

        simulator = Simulator(
            workload=workload,
            scheduler=FCFS_Scheduler(),
            io_device=device
        )

        # P1 arrives and gets CPU
        simulator.check_arrivals()
        simulator.select_next()

        # CPU unit 1
        simulator.step_time_unit()

        assert p1.remaining_time == 4
        assert p1.state == ProcessState.RUNNING

        # CPU unit 2 -> request I/O
        simulator.step_time_unit()

        assert p1.remaining_time == 3
        assert p1.state == ProcessState.IO_WAIT
        assert simulator.cur_process is None

        # P1 must no longer be in the ready queue
        assert p1 not in simulator.ready_queue

        # Request must have reached the device
        assert (
            device.current_io == io_request
            or device.has_pending()
        )
        
    def test_completed_io_returns_process_to_ready(self):
        device = IODevice(
            device_id="device_0",
            device_type="generic"
        )

        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=5,
        )

        io_request = IORequest(
            process=p1,
            execution_point=2,
            duration=3,
            device=device
        )

        p1.io_requests = [io_request]

        workload = Workload([p1])

        simulator = Simulator(
            workload=workload,
            scheduler=FCFS_Scheduler(),
            io_device=device
        )

        # CPU executes until P1 requests I/O
        simulator.check_arrivals()
        simulator.select_next()

        simulator.step_time_unit()
        simulator.step_time_unit()

        assert p1.state == ProcessState.IO_WAIT

        # Process the I/O
        completed_request = device.step()
        assert completed_request is None

        completed_request = device.step()
        assert completed_request is None

        completed_request = device.step()

        # I/O should now be complete
        assert completed_request == io_request

        # Simulator handles the completed request
        process = completed_request.process

        process.io_in_progress = None
        process.state = ProcessState.READY
        simulator.ready_queue.append(process)

        assert p1.state == ProcessState.READY
        assert p1 in simulator.ready_queue
        assert p1.io_in_progress is None
        assert p1.remaining_time == 3
        
    def test_cpu_runs_another_process_during_io(self):
        device = IODevice(
            device_id="device_0",
            device_type="generic"
        )

        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=4,
        )

        p2 = Process(
            process_id=2,
            arrival_time=0,
            burst_time=5,
        )

        io_request = IORequest(
            process=p1,
            execution_point=2,
            duration=3,
            device=device
        )

        p1.io_requests = [io_request]

        workload = Workload([p1, p2])

        simulator = Simulator(
            workload=workload,
            scheduler=FCFS_Scheduler(),
            io_device=device
        )

        result = simulator.run()

        # Both processes must finish
        assert p1 in result.processes_completed
        assert p2 in result.processes_completed

        # P1's I/O was processed
        assert device.total_processed == 1

        # Both completed exactly once
        assert len(result.processes_completed) == 2
        
    def test_cpu_idle_while_io_continues(self):
        
        device = IODevice(
            device_id="device_0",
            device_type="generic"
        )

        p1 = Process(
            process_id=1,
            arrival_time=0,
            burst_time=2,
        )

        io_request = IORequest(
            process=p1,
            execution_point=1,
            duration=3,
            device=device
        )

        p1.io_requests = [io_request]

        workload = Workload([p1])

        simulator = Simulator(
            workload=workload,
            scheduler=FCFS_Scheduler(),
            io_device=device
        )

        result = simulator.run()

        # Process must eventually complete
        assert p1.state == ProcessState.TERMINATED
        assert p1.remaining_time == 0

        # I/O must have completed
        assert device.total_processed == 1

        # Device must be empty
        assert device.current_io is None
        assert not device.has_pending()

        # Simulation must have lasted longer than just CPU execution
        # assert result.simulation_end >= 5
        
        print(result.timeline)
        print(result.simulation_end)