import pytest

from src.model.process import Process
from src.scheduler_algorithms.SRTF import SRTF_Scheduler


def make_process(pid, arrival_time, burst_time, remaining_time=None):
    p = Process(
        process_id=pid,
        arrival_time=arrival_time,
        burst_time=burst_time
    )

    if remaining_time is not None:
        p.remaining_time = remaining_time

    return p


# ---------------------------------------------------------
# select_next
# ---------------------------------------------------------

def test_select_empty_queue():
    scheduler = SRTF_Scheduler()

    assert scheduler.select_next([]) is None


def test_select_single_process():
    scheduler = SRTF_Scheduler()

    p1 = make_process(1, 0, 5)

    assert scheduler.select_next([p1]) == p1


def test_select_shortest_remaining_time():
    scheduler = SRTF_Scheduler()

    p1 = make_process(1, 0, 8)
    p2 = make_process(2, 0, 3)
    p3 = make_process(3, 0, 5)

    selected = scheduler.select_next([p1, p2, p3])

    assert selected == p2


def test_select_process_after_remaining_time_changes():
    scheduler = SRTF_Scheduler()

    p1 = make_process(1, 0, 10, 2)
    p2 = make_process(2, 0, 5, 5)

    selected = scheduler.select_next([p1, p2])

    assert selected == p1


def test_select_zero_remaining_time():
    scheduler = SRTF_Scheduler()

    p1 = make_process(1, 0, 5, 0)
    p2 = make_process(2, 0, 2, 2)

    selected = scheduler.select_next([p1, p2])

    assert selected == p1


# ---------------------------------------------------------
# Tie-breaking
# ---------------------------------------------------------

def test_equal_remaining_time_uses_pid():
    scheduler = SRTF_Scheduler()

    p1 = make_process(5, 0, 4)
    p2 = make_process(2, 0, 4)
    p3 = make_process(8, 0, 4)

    selected = scheduler.select_next([p1, p2, p3])

    assert selected == p2


def test_equal_remaining_time_and_pid_order_does_not_matter():
    scheduler = SRTF_Scheduler()

    p1 = make_process(1, 0, 4)
    p2 = make_process(2, 0, 4)

    assert scheduler.select_next([p2, p1]) == p1
    assert scheduler.select_next([p1, p2]) == p1


# ---------------------------------------------------------
# should_preempt
# ---------------------------------------------------------

def test_preempt_when_shorter_process_exists():
    scheduler = SRTF_Scheduler()

    current = make_process(1, 0, 10, 8)
    shorter = make_process(2, 3, 3)

    assert scheduler.should_preempt(current, [shorter]) is True


def test_do_not_preempt_when_ready_process_is_longer():
    scheduler = SRTF_Scheduler()

    current = make_process(1, 0, 5, 3)
    longer = make_process(2, 1, 8)

    assert scheduler.should_preempt(current, [longer]) is False


def test_do_not_preempt_when_remaining_time_is_equal():
    scheduler = SRTF_Scheduler()

    current = make_process(1, 0, 5, 5)
    equal = make_process(2, 1, 5)

    assert scheduler.should_preempt(current, [equal]) is False


def test_preempt_if_any_process_is_shorter():
    scheduler = SRTF_Scheduler()

    current = make_process(1, 0, 10)

    p2 = make_process(2, 1, 20)
    p3 = make_process(3, 2, 15)
    p4 = make_process(4, 3, 2)

    assert scheduler.should_preempt(current, [p2, p3, p4]) is True


def test_do_not_preempt_with_empty_ready_queue():
    scheduler = SRTF_Scheduler()

    current = make_process(1, 0, 5)

    assert scheduler.should_preempt(current, []) is False


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------

def test_negative_remaining_time():
    scheduler = SRTF_Scheduler()

    p1 = make_process(1, 0, 5, -1)
    p2 = make_process(2, 0, 3)

    assert scheduler.select_next([p1, p2]) == p1


def test_many_processes():
    scheduler = SRTF_Scheduler()

    processes = [
        make_process(1, 0, 100),
        make_process(2, 1, 50),
        make_process(3, 2, 1),
        make_process(4, 3, 75),
        make_process(5, 4, 20),
        make_process(6, 5, 10),
    ]

    selected = scheduler.select_next(processes)

    assert selected.pid == 3


def test_scheduler_does_not_modify_ready_queue():
    scheduler = SRTF_Scheduler()

    p1 = make_process(1, 0, 10)
    p2 = make_process(2, 1, 3)
    p3 = make_process(3, 2, 5)

    queue = [p1, p2, p3]
    original = queue.copy()

    scheduler.select_next(queue)

    assert queue == original


# ---------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------

def test_on_time_unit_does_not_crash():
    scheduler = SRTF_Scheduler()

    scheduler.on_time_unit()


def test_reset_does_not_crash():
    scheduler = SRTF_Scheduler()

    scheduler.reset()