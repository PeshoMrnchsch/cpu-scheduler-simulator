import pytest

from src.devices.io_device import IODevice
from src.model.io_request import IORequest
from src.model.process import Process
from src.model.workload import Workload


def test_workload_accepts_cpu_and_io_definition_before_simulation():
    device = IODevice("disk-1", "disk")
    process_one = Process(
        process_id=1,
        arrival_time=0,
        burst_time=5,
        io_requests=[IORequest(1, execution_point=2, duration=3, device=device)],
    )
    process_two = Process(process_id=2, arrival_time=0, burst_time=4)

    workload = Workload([process_one, process_two])

    assert workload.processes == [process_one, process_two]
    assert process_one.arrival_time == 0
    assert process_one.burst_time == 5
    assert process_one.io_requests[0].execution_point == 2
    assert process_one.io_requests[0].duration == 3
    assert process_two.arrival_time == 0
    assert process_two.burst_time == 4
    assert process_two.io_requests == []


def test_workload_accepts_multiple_io_requests_in_execution_order():
    device = IODevice("disk-1", "disk")
    process = Process(
        process_id=1,
        arrival_time=0,
        burst_time=8,
        io_requests=[
            IORequest(1, execution_point=2, duration=3, device=device),
            IORequest(1, execution_point=6, duration=1, device=device),
        ],
    )

    workload = Workload([process])

    assert [request.execution_point for request in workload.processes[0].io_requests] == [2, 6]


@pytest.mark.parametrize(
    "io_requests, error_message",
    [
        (
            [
                IORequest(1, execution_point=4, duration=1, device=IODevice("disk-1", "disk")),
                IORequest(1, execution_point=2, duration=1, device=IODevice("disk-1", "disk")),
            ],
            "increasing execution order",
        ),
        (
            [IORequest(1, execution_point=-1, duration=1, device=IODevice("disk-1", "disk"))],
            "invalid execution point",
        ),
        (
            [IORequest(1, execution_point=2, duration=1, device=None)],
            "without a device",
        ),
    ],
)
def test_workload_rejects_invalid_io_behavior(io_requests, error_message):
    process = Process(process_id=1, arrival_time=0, burst_time=5, io_requests=io_requests)

    with pytest.raises(ValueError, match=error_message):
        Workload([process])


def test_workload_sorts_processes_by_arrival_then_pid():
    processes = [
        Process(process_id=2, arrival_time=1, burst_time=3),
        Process(process_id=1, arrival_time=0, burst_time=2),
        Process(process_id=3, arrival_time=1, burst_time=1),
    ]

    workload = Workload(processes)

    assert len(workload) == 3
    assert workload.get_sorted_by_arrival() == [processes[1], processes[0], processes[2]]
    assert repr(workload) == "Workload(3 processes)"


def test_workload_rejects_empty_or_duplicate_processes():
    with pytest.raises(ValueError, match="at least one process"):
        Workload([])

    process = Process(process_id=1, arrival_time=0, burst_time=2)
    with pytest.raises(ValueError, match="such id exists"):
        Workload([process, Process(process_id=1, arrival_time=1, burst_time=1)])


@pytest.mark.parametrize(
    "arrival_time, burst_time",
    [(-1, 2), (0, 0)],
)
def test_workload_rejects_invalid_process_timing(arrival_time, burst_time):
    process = Process(process_id=1, arrival_time=arrival_time, burst_time=burst_time)

    with pytest.raises(ValueError):
        Workload([process])


def test_workload_rejects_invalid_io_requests():
    device = IODevice("disk-1", "disk")
    process = Process(
        process_id=1,
        arrival_time=0,
        burst_time=5,
        io_requests=[IORequest(1, 5, 1, device)],
    )

    with pytest.raises(ValueError, match="burst time"):
        Workload([process])


def test_reset_all_resets_each_process():
    processes = [
        Process(process_id=1, arrival_time=0, burst_time=3),
        Process(process_id=2, arrival_time=1, burst_time=2),
    ]
    workload = Workload(processes)
    processes[0].remaining_time = 1
    processes[0].start = 2
    processes[0].completion_time = 3

    workload.reset_all()

    assert [(p.remaining_time, p.start, p.completion_time) for p in processes] == [
        (3, None, None),
        (2, None, None),
    ]