import pytest

from src.devices.io_device import IODevice
from src.model.io_request import IORequest


class TestIODevice(IODevice):
    pass


def test_io_request_initializes_and_resets_remaining_time():
    device = TestIODevice("disk-1", "disk")
    request = IORequest(process_id=7, execution_point=3, duration=5, device=device)

    assert request.process_id == 7
    assert request.execution_point == 3
    assert request.duration == 5
    assert request.remaining_time == 5

    request.remaining_time = 1
    request.reset()

    assert request.remaining_time == 5


def test_io_request_rejects_non_positive_duration():
    device = TestIODevice("disk-1", "disk")

    with pytest.raises(ValueError, match="Duration must be positive"):
        IORequest(process_id=7, execution_point=3, duration=0, device=device)