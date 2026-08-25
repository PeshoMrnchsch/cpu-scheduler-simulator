from src.model.process import Process
from src.model.workload import Workload
from src.simulator import Simulator


def create_simulator():
    p = Process(process_id=99, arrival_time=0, burst_time=1)
    workload = Workload([p])
    return Simulator(workload, None)


def test_add_timeline_entry_first_process():
    simulator = create_simulator()

    p1 = Process(process_id=1, arrival_time=0, burst_time=3)

    simulator.cur_time = 0
    simulator.cur_process = p1

    simulator.add_timeline_entry(p1)
    print(*simulator.timeline)
    assert simulator.timeline == [
        (0, 1, 1)
    ]


def test_add_timeline_entry_extends_same_process():
    simulator = create_simulator()

    p1 = Process(process_id=1, arrival_time=0, burst_time=3)

    simulator.cur_time = 0
    simulator.cur_process = p1
    simulator.add_timeline_entry(p1)

    simulator.cur_time = 1
    simulator.cur_process = p1
    simulator.add_timeline_entry(p1)

    simulator.cur_time = 2
    simulator.cur_process = p1
    simulator.add_timeline_entry(p1)

    assert simulator.timeline == [
        (0, 3, 1)
    ]


def test_add_timeline_entry_new_process():
    simulator = create_simulator()

    p1 = Process(process_id=1, arrival_time=0, burst_time=2)
    p2 = Process(process_id=2, arrival_time=0, burst_time=1)

    simulator.cur_time = 0
    simulator.cur_process = p1
    simulator.add_timeline_entry(p1)

    simulator.cur_time = 1
    simulator.cur_process = p1
    simulator.add_timeline_entry(p1)

    simulator.cur_time = 2
    simulator.cur_process = p2
    simulator.add_timeline_entry(p2)

    assert simulator.timeline == [
        (0, 2, 1),
        (2, 3, 2)
    ]