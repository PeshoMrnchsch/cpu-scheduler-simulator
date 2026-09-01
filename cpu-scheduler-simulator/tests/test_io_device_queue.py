from src.devices.io_device_queue import IODeviceQueue


def test_new_queue_is_empty():
    queue = IODeviceQueue()

    assert queue.get_queue() is None
    assert queue.dequeue() is None
    assert queue.has_pending() is False
    assert queue.get_queue_depth() == 0


def test_enqueue_and_dequeue_preserve_fifo_order():
    queue = IODeviceQueue()
    first = object()
    second = object()

    queue.enqueue(first)
    queue.enqueue(second)

    assert queue.get_queue() == [first, second]
    assert queue.dequeue() is first
    assert queue.dequeue() is second
    assert queue.dequeue() is None


def test_clear_removes_all_pending_requests():
    queue = IODeviceQueue()
    queue.enqueue(object())
    queue.enqueue(object())

    queue.clear()

    assert queue.get_queue() is None
    assert queue.has_pending() is False
    assert queue.get_queue_depth() == 0


def test_repr_reports_pending_request_count():
    queue = IODeviceQueue()
    queue.enqueue(object())

    assert repr(queue) == "IODeviceQueue(1 pending)"