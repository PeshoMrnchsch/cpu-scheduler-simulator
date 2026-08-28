from src.devices.io_device import IODevice
from src.model.io_request import IORequest


def test_start_next_moves_request_from_queue_to_device():
    device = IODevice("disk-1", "disk")
    request = IORequest(1, 0, 3, device)

    device.enqueue(request)

    assert device.start_next() is True
    assert device.current_io is request
    assert device.remaining_time == 3
    assert device.get_queue_depth() == 0


def test_step_completes_request_and_counts_it_once():
    device = IODevice("disk-1", "disk")
    request = IORequest(1, 0, 2, device)
    device.enqueue(request)

    device.step()
    assert device.remaining_time == 2
    assert device.total_processed == 0

    device.step()
    assert device.remaining_time == 1
    assert device.total_processed == 0

    device.step()
    assert device.remaining_time == 0
    assert device.current_is_complete() is True
    assert device.total_processed == 1


def test_reset_clears_requests_and_device_state():
    device = IODevice("disk-1", "disk")
    request = IORequest(1, 0, 1, device)
    device.enqueue(request)
    device.step()
    device.total_wait_time = 4

    device.reset()

    assert device.current_io is None
    assert device.remaining_time == 0
    assert device.get_queue_depth() == 0
    assert device.total_processed == 0
    assert device.total_wait_time == 0


def test_repr_includes_device_type_id_and_queue_depth():
    device = IODevice("disk-1", "disk")

    assert repr(device) == "Disk(disk-1): 0 queued"